import shlex
import subprocess
import os
import ctypes


def get_reprepro_path():
    """
    Returns the location path where reprepro is installed
    by calling which reprepro
    """

    cmd = "which reprepro"
    args = shlex.split(cmd)
    sub_proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    try:
        output, errs = sub_proc.communicate(timeout=15)
    except Exception as e:
        print(e)
        sub_proc.kill()
    else:
        return output.decode('utf8').strip()


def get_reprepro_version():
    reprepro = get_reprepro_path()
    cmd = reprepro + " --version"

    args = shlex.split(cmd)
    sub_proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    try:
        output, errs = sub_proc.communicate(timeout=15)
    except Exception as e:
        print(e)
        sub_proc.kill()
    else:
        return output.decode('utf8').strip()


def user_is_root(func):
    def wrapper(*args, **kwargs):
        try:
            is_root_or_admin = (os.getuid() == 0)
        except AttributeError:
            is_root_or_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

        if(is_root_or_admin):
            return func(*args, **kwargs)
        else:
            return {"error": True, "msg": "You must be\
                 root/administrator to continue!"}
    return wrapper
