import logging
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from subprocess import DEVNULL
from typing import List

import grapejuice_common.variables as variables
from grapejuice_common.log_util import log_on_call, log_function

LOG = logging.getLogger(__name__)

space_version_ptn = re.compile(r"wine-(.+?)\s+")
non_space_version_ptn = re.compile(r"wine-(.+)")
space = " "


class ProcessWrapper:
    def __init__(self, proc: subprocess.Popen):
        self.proc = proc

    @property
    def exited(self):
        proc = self.proc

        if proc.returncode is None:
            proc.poll()

        return proc.returncode is not None

    def kill(self):
        if not self.exited:
            os.kill(self.proc.pid, signal.SIGINT)

    def __del__(self):
        del self.proc


processes: List[ProcessWrapper] = []
is_polling = False


@log_on_call("Preparing for Wine")
def prepare():
    prefix_dir = variables.wineprefix_dir()
    os.environ["WINEPREFIX"] = prefix_dir
    os.environ["WINEARCH"] = "win64"

    if not os.path.exists(prefix_dir):
        os.makedirs(prefix_dir)


@log_on_call("Running Wine configuration")
def winecfg():
    prepare()
    os.spawnlp(os.P_NOWAIT, variables.wine_binary(), variables.wine_binary(), "winecfg")


@log_on_call("Running registry editor")
def regedit():
    prepare()
    os.spawnlp(os.P_NOWAIT, variables.wine_binary(), variables.wine_binary(), "regedit")


@log_on_call("Running Windows Explorer")
def explorer():
    prepare()
    os.spawnlp(os.P_NOWAIT, variables.wine_binary(), variables.wine_binary(), "explorer")


def load_reg(srcfile):
    LOG.info(f"Loading registry file {srcfile} into the wineprefix")
    prepare()
    target_filename = str(int(time.time())) + ".reg"
    target_path = os.path.join(variables.wine_temp(), target_filename)
    shutil.copyfile(srcfile, target_path)

    winreg = "C:\\windows\\temp\\{}".format(target_filename)
    os.spawnlp(os.P_WAIT, variables.wine_binary(), variables.wine_binary(), "regedit", "/S", winreg)
    os.spawnlp(os.P_WAIT, variables.wine_binary_64(), variables.wine_binary_64(), "regedit", "/S", winreg)

    os.remove(target_path)


def load_regs(s: [str], patches: dict = None):
    prepare()
    target_filename = str(int(time.time())) + ".reg"
    target_path = os.path.join(variables.wine_temp(), target_filename)

    with open(target_path, "w+") as fp:
        if patches is None:
            fp.write("\r\n".join(s))
        else:
            out_lines = []
            for line in s:
                for k, v in patches.items():
                    varkey = "$" + k
                    if varkey in line:
                        line = line.replace(varkey, v)

                out_lines.append(line)

            fp.writelines(out_lines)

    winreg = "C:\\windows\\temp\\{}".format(target_filename)
    os.spawnlp(os.P_WAIT, variables.wine_binary(), variables.wine_binary(), "regedit", "/S", winreg)
    os.spawnlp(os.P_WAIT, variables.wine_binary_64(), variables.wine_binary_64(), "regedit", "/S", winreg)

    os.remove(target_path)


@log_on_call("Running Winetricks")
def wine_tricks():
    prepare()
    os.spawnlp(os.P_NOWAIT, "winetricks", "winetricks")


@log_on_call("Disabling MIME associations in wineprefix")
def disable_mime_assoc():
    load_reg(os.path.join(variables.assets_dir(), "disable_mime_assoc.reg"))


def set_roblox_document_path():
    src_path = os.path.join(variables.assets_dir(), "roblox_documents_folder.reg")
    patches = dict()

    documents_dir = "Z:" + variables.xdg_documents().replace("/", "\\\\")
    patches["DOCUMENTS_DIR"] = documents_dir
    LOG.info(f"Setting the roblox documents directory to '{documents_dir}'")

    with open(src_path, "r") as fp:
        load_regs(fp.readlines(), patches)


@log_on_call("Loading DLL overrides")
def load_dll_overrides():
    load_reg(os.path.join(variables.assets_dir(), "dll_overrides.reg"))


@log_on_call("Sandboxing user directories in the wineprefix")
def sandbox():
    user_dir = variables.wine_user()

    if os.path.exists(user_dir) and os.path.isdir(user_dir):
        for file in os.listdir(user_dir):
            p = os.path.join(user_dir, file)

            if os.path.islink(p):
                LOG.info(f"Sandboxing {file}")
                os.remove(p)
                os.makedirs(p, exist_ok=True)


@log_on_call("Configuring the wineprefix")
def configure_prefix():
    disable_mime_assoc()
    sandbox()
    load_dll_overrides()
    set_roblox_document_path()


@log_on_call("Creating the wineprefix")
def create_prefix():
    configure_prefix()


@log_function
def prefix_exists():
    return os.path.exists(variables.wineprefix_dir())


@log_function
def run_exe(exe_path, *args):
    prepare()
    if len(args) > 0:
        os.spawnlp(os.P_NOWAIT, variables.wine_binary(), variables.wine_binary(), exe_path, *args)
    else:
        os.spawnlp(os.P_NOWAIT, variables.wine_binary(), variables.wine_binary(), exe_path)


@log_function
def run_exe_nowait(exe_path, *args) -> ProcessWrapper:
    prepare()

    command = [variables.wine_binary(), exe_path, *args]
    p = subprocess.Popen(command, stdin=DEVNULL, stdout=sys.stdout, stderr=sys.stderr, close_fds=True)

    wrapper = ProcessWrapper(p)
    processes.append(wrapper)

    poll_processes()

    return wrapper


def _poll_processes() -> bool:
    """
    Makes sure zombie launchers are taken care of
    :return: Whether or not processes remain
    """
    global is_polling
    exited = []

    for proc in processes:
        if proc.exited:
            exited.append(proc)

    for proc in exited:
        processes.remove(proc)
        del proc

    processes_left = len(processes) > 0
    if not processes_left:
        is_polling = False

    return processes_left


def poll_processes():
    global is_polling
    if is_polling:
        return

    from gi.repository import GObject
    GObject.timeout_add(100, _poll_processes)


@log_function
def wine_ok(system_wine: str = None, show_dialog=True):
    from grapejuice_common.settings import settings
    if settings.ignore_wine_version.value:
        return True

    from grapejuice_common.dbus_client import dbus_connection
    from grapejuice_common.gtk.gtk_stuff import dialog

    def prepare_version(s):
        from packaging import version

        if space in s:
            match = space_version_ptn.match(s)

        else:
            match = non_space_version_ptn.match(s)

        assert match is not None

        return version.parse(match.group(1))

    if system_wine is None:
        system_wine = prepare_version(dbus_connection().wine_version())

    else:
        system_wine = prepare_version(system_wine)

    required_wine = prepare_version(variables.required_wine_version())

    def version_to_string(v):
        if v.public:
            return v.public

        if v.base_version:
            return v.base_version

        return repr(v)

    if system_wine < required_wine:
        if show_dialog:
            msg = "Your system has Wine version {} installed, you need at least Wine version {} in order to run Roblox." \
                .format(version_to_string(system_wine), version_to_string(required_wine))

            dialog(msg)

        return False

    return True
