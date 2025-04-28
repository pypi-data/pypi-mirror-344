"""
The functions in this module are the implemenations of the functions exposed
to Excel in the pyxll module.

They are separated into this module to minimize the time taken to import the
pyxll module, as that is done when starting Excel.
"""
from ..widgets import JupyterQtWidget, QApplication, QMessageBox
from ..kernel import launch_jupyter
from ..onedrive import get_onedrive_path
from pyxll import XLCell, xlcAlert, get_config, xl_app, create_ctp, schedule_call
from functools import partial
import ctypes.wintypes
import logging
import sys
import os

_log = logging.getLogger(__name__)


def _get_qt_app():
    """Get or create the Qt application"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def _get_notebook_path(cfg):
    """Return the path to open the Jupyter notebook in."""
    # Use the path of the active workbook if use_workbook_dir is set
    use_workbook_dir = False
    if cfg.has_option("JUPYTER", "use_workbook_dir"):
        try:
            use_workbook_dir = bool(int(cfg.get("JUPYTER", "use_workbook_dir")))
        except (ValueError, TypeError):
            _log.error("Unexpected value for JUPYTER.use_workbook_dir.")

    if use_workbook_dir:
        xl = xl_app(com_package="win32com")
        wb = xl.ActiveWorkbook
        if wb is not None and wb.FullName:
            path = wb.FullName

            # If the workbook path exists then use it
            if os.path.exists(path):
                return os.path.dirname(path)

            # Otherwise see if it's a OneDrive link and try to resolve it
            lpath = path.lower()
            if lpath.startswith("https://"):
                try:
                    onedrive_path = get_onedrive_path(path)
                    if onedrive_path:
                        if os.path.exists(onedrive_path):
                            return os.path.dirname(onedrive_path)
                        _log.warning(f"OneDrive path '{onedrive_path}' does not exist")
                except Exception as e:
                    _log.warn(f"Unable to get local OneDrive path from URL '{path}'", exc_info=True)

            # If we can't use this path then log a warning
            _log.warning(f"Workbook path '{path}' not found and cannot be used as the Jupyter folder.")

    # Otherwise use the path option
    if cfg.has_option("JUPYTER", "notebook_dir"):
        path = cfg.get("JUPYTER", "notebook_dir").strip("\"\' ")
        if os.path.exists(path):
            return os.path.normpath(path)
        _log.warning(f"Notebook path '{path}' does not exist")

    # And if that's not set use My Documents
    CSIDL_PERSONAL = 5  # My Documents
    SHGFP_TYPE_CURRENT = 0  # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value


def _get_jupyter_timeout(cfg):
    """Return the timeout in seconds to use when starting Jupyter."""
    timeout = 60.0
    if cfg.has_option("JUPYTER", "timeout"):
        try:
            timeout = float(cfg.get("JUPYTER", "timeout"))
            _log.debug("Using a timeout of %.1fs for starting the Jupyter notebook." % timeout)
        except (ValueError, TypeError):
            _log.error("Unexpected value for JUPYTER.timeout.")
    return max(timeout, 1.0)


def _get_jupyter_subcommand(cfg, default="notebook"):
    """Return the name of the Juputer subcommand to use to launch the Jupyter notebook server."""
    subcommand = default
    if cfg.has_option("JUPYTER", "subcommand"):
        subcommand = cfg.get("JUPYTER", "subcommand")
    return subcommand


def _get_notebook_kwargs(initial_path=None, notebook_path=None, subcommand=None):
    """Get the kwargs for calling launch_jupyter.

    :param initial_path: Path to open Jupyter in.
    :param notebook_path: Path of Jupyter notebook to open.
    :param subcommand: Jupyter subcommand to use to launch the notebook server.
    """
    if initial_path is not None and notebook_path is not None:
        raise RuntimeError("'initial_path' and 'notebook_path' cannot both be set.")

    if notebook_path is not None:
        if not os.path.exists(notebook_path):
            raise RuntimeError("Notebook path '%s' not found." % notebook_path)
        if not os.path.isfile(notebook_path):
            raise RuntimeError("Notebook path '%s' is not a file." % notebook_path)
        notebook_path = os.path.abspath(notebook_path)

    cfg = get_config()
    timeout = _get_jupyter_timeout(cfg)
    subcommand = subcommand or _get_jupyter_subcommand(cfg)

    if subcommand not in ("notebook", "lab"):
        raise ValueError(f"Unexpected value '{subcommand}' for Jupyter subcommand. "
                         "Expected 'notebook' or 'lab'.")

    if notebook_path is None and initial_path is None:
        initial_path = _get_notebook_path(cfg)
    if initial_path and not os.path.exists(initial_path):
        raise RuntimeError("Directory '%s' does not exist.")
    if initial_path and not os.path.isdir(initial_path):
        raise RuntimeError("Path '%s' is not a directory.")

    return {
        "initial_path": initial_path,
        "notebook_path": notebook_path,
        "subcommand": subcommand,
        "timeout": timeout
    }


def open_jupyter_notebook(*args, initial_path=None, notebook_path=None):
    """Ribbon action function for opening the Jupyter notebook
    browser control in a custom task pane.

    :param initial_path: Path to open Jupyter in.
    :param notebook_path: Path of Jupyter notebook to open.
    """
    # Get the Qt Application
    app = _get_qt_app()

    
    # Get the browser args from the config
    cfg = get_config()

    private_browser = False
    if cfg.has_option("JUPYTER", "private_browser"):
        try:
            private_browser = bool(int(cfg.get("JUPYTER", "private_browser")))
        except:
            raise ValueError(f"Unexpected value for JUPYTER.private_browser '{cfg.get('JUPYTER', 'private_browser')}'")

    allow_cookies = True
    if cfg.has_option("JUPYTER", "allow_cookies"):
        try:
            allow_cookies = bool(int(cfg.get("JUPYTER", "allow_cookies")))
        except:
            raise ValueError(f"Unexpected value for JUPYTER.allow_cookies '{cfg.get('JUPYTER', 'allow_cookies')}'")

    storage_path = None
    if cfg.has_option("JUPYTER", "storage_path"):
        storage_path = cfg.get("JUPYTER", "storage_path")
        if not os.path.exists(storage_path) or not os.path.isdir(storage_path):
            raise ValueError(f"Invalid JUPYTER.storage_path '{storage_path}'")

    cache_path = None
    if cfg.has_option("JUPYTER", "cache_path"):
        cache_path = cfg.get("JUPYTER", "cache_path")
        if not os.path.exists(cache_path) or not os.path.isdir(cache_path):
            raise ValueError(f"Invalid JUPYTER.cache_path '{cache_path}'")

    pause_on_focus_lost = True
    if cfg.has_option("JUPYTER", "pause_on_focus_lost"):
        try:
            pause_on_focus_lost = bool(int(cfg.get("JUPYTER", "pause_on_focus_lost")))
        except:
            raise ValueError(f"Unexpected value for JUPYTER.pause_on_focus_lost '{cfg.get('JUPYTER', 'pause_on_focus_lost')}'")

    # Get the notebook args
    kwargs = _get_notebook_kwargs(initial_path=initial_path, notebook_path=notebook_path)

    # Create the Jupyter web browser widget
    widget = JupyterQtWidget(private_browser=private_browser,
                             allow_cookies=allow_cookies,
                             storage_path=storage_path,
                             cache_path=cache_path,
                             pause_on_focus_lost=pause_on_focus_lost,
                             **kwargs)

    # Show it in a CTP
    create_ctp(widget, width=800)


def open_jupyter_notebook_in_browser(*args, initial_path=None, notebook_path=None):
    """Ribbon action function for opening the Jupyter notebook in a web browser.

    :param initial_path: Path to open Jupyter in.
    :param notebook_path: Path of Jupyter notebook to open.
    """
    kwargs = _get_notebook_kwargs(initial_path=initial_path, notebook_path=notebook_path)

    # We don't do anything with the token here as we don't know when the kernel and
    # Jupyter server process is no longer needed.
    token, url = launch_jupyter(no_browser=False, **kwargs)


def set_selection_in_ipython(*args):
    """Gets the value of the selected cell and copies it to
    the globals dict in the IPython kernel.
    """
    try:
        if not getattr(sys, "_ipython_app", None) or not sys._ipython_kernel_running:
            raise Exception("IPython kernel not running")

        # Get the current selected range
        xl = xl_app(com_package="win32com")
        selection = xl.Selection
        if not selection:
            raise Exception("Nothing selected")

        # Check to see if it looks like a pandas DataFrame
        try_dataframe = False
        has_index = False
        if selection.Rows.Count > 1 and selection.Columns.Count > 1:
            try:
                import pandas as pd
            except ImportError:
                pd = None
                pass

            if pd is not None:
                # If the top left corner is empty assume the first column is an index.
                try_dataframe = True
                top_left = selection.Cells[1].Value
                if top_left is None:
                    has_index = True

        # Get an XLCell object from the range to make it easier to get the value
        cell = XLCell.from_range(selection)

        # Get the value using PyXLL's dataframe converter, or as a plain value.
        value = None
        if try_dataframe:
            try:
                type_kwargs = {"index": 1 if has_index else 0}
                value = cell.options(type="dataframe", type_kwargs=type_kwargs).value
            except:
                _log.warning("Error converting selection to DataFrame", exc_info=True)

        if value is None:
            value = cell.value

        # set the value in the shell's locals
        sys._ipython_app.shell.user_ns["_"] = value
        print("\n\n>>> Selected value set as _")
    except:
        app = _get_qt_app()
        QMessageBox.warning(None, "Error", "Error setting selection in Excel")
        _log.error("Error setting selection in Excel", exc_info=True)


def OpenJupyterNotebook(path=None, browser=False):
    """
    Open a Jupyter notebook in a new task pane.

    :param path: Path to Jupyter notebook file or directory.
    :param browser: Set to true to open in a browser instead of a task pane.
    :return: True on success
    """
    try:
        if path:
            if not os.path.isabs(path):
                # Try and get the absolute path relative to the active workbook
                xl = xl_app(com_package="win32com")
                wb = xl.ActiveWorkbook
                if wb is not None and wb.FullName and os.path.exists(wb.FullName):
                    abs_path = os.path.join(os.path.dirname(wb.FullName), path)
                    if os.path.exists(abs_path):
                        path = abs_path
            if not os.path.exists(path):
                raise RuntimeError(f"Path '{path}' not found.")

        initial_path = None
        notebook_path = None
        if path:
            if os.path.isdir(path):
                initial_path = path
            elif os.path.isfile(path):
                notebook_path = path
            else:
                raise RuntimeError(f"Something is wrong with the path '{path}'.")

        open_jupyter = open_jupyter_notebook_in_browser if browser else open_jupyter_notebook

        # Use schedule_call to actually open the notebook since if this was called
        # from a Workbook.Open macro Excel may not yet be ready to open a CTP.
        schedule_call(partial(open_jupyter,
                                initial_path=initial_path,
                                notebook_path=notebook_path))

        return True
    except Exception as e:
        xlcAlert(f"Error opening Jupyter notebook: {e}")
        raise
