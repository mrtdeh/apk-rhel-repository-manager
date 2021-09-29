import os
import shlex
import subprocess
from reprepro_tools.output_parser import reprepro_list_packages_parser,\
    reprepro_include_package_parser,\
    reprepro_remove_package_parser
from reprepro_tools.utils import get_reprepro_path
from reprepro_tools.exceptions import RepreproExecutionError
from config.config import get_config
from logger.logger import get_logger
logger = get_logger(__name__)

config_app = get_config()


class Reprepro(object):
    """
    This reprepro class allows us to use the reprepro tool from within python
    by calling reprepro.Reprepro()
    """

    def __init__(self, path=None):
        """
        Module initialization
        :param path: Path where reprepro is installed on a user system.
        On linux system it's typically on /usr/bin/reprepro.
        """

        self.reprepro_tool = path if path else get_reprepro_path()
        self.default_args = "{reprepro}  {outarg}  "
        self.raw_ouput = None
        self.as_root = False
        self.reprepro_base_dir = config_app["reprepro"]["base_dir"]
        self.code_name = "buster"

    def require_root(self, required=True):
        """
        Call this method to add "sudo" in front of reprepro call
        """
        self.as_root = required

    def default_command(self):

        if self.as_root:
            return self.default_command_privileged()

        return self.default_args.format(reprepro=self.reprepro_tool,
                                        outarg="--basedir " +
                                        self.reprepro_base_dir)

    def default_command_privileged(self):
        """
        Commands that require root privileges
        """
        return self.default_args.format(reprepro="sudo " + self.reprepro_tool,
                                        outarg="--basedir " +
                                        self.reprepro_base_dir)

    def reprepro_version(self):
        """
        Returns reprepro version and build details
        """
        output, status = self.run_command([self.reprepro_tool, '--version'])
        version_data = {}
        for line in output.splitlines():
            version_string = line.split(' ')
            version_data['reprepro'] = tuple(
                [int(_) for _ in version_string.split(' ')])
        return version_data

    def run_command(self, cmd, timeout=None):

        if (os.path.exists(self.reprepro_tool)):
            sub_proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                output, errs = sub_proc.communicate(timeout=timeout)
            except Exception as e:
                logger.error(e)
                sub_proc.kill()
                return errs.decode('utf8'), False
            else:
                if 0 != sub_proc.returncode:
                    logger.error(RepreproExecutionError(
                        'Error during command: "' + ' '.join(cmd) +
                        '"\n\n' + errs.decode('utf8')))
                    return errs.decode('utf8'), False

                # Response is bytes so decode the output and return
                return errs.decode('utf8'), output.decode('utf8').strip()
        else:
            logger.error("reprepro not installed")
            return "Reprepro Not Installed", False

    def reprepro_list_packages(self, code_name=None, args=None, timeout=None):
        if code_name:
            self.code_name = code_name
        if (args):
            assert (isinstance(args, str)
                    ), "Expected string got {0} instead".format(type(args))

        reprepro_list_args = "list {code_name}  ".format(
            code_name=self.code_name)
        scan_command = self.default_command() + reprepro_list_args
        if (args):
            scan_command += " {0}".format(args)
        scan_shlex = shlex.split(scan_command)

        # Run the command and get the output
        output, status = self.run_command(scan_shlex, timeout=timeout)
        logger.debug(status)

        check_out_put = reprepro_list_packages_parser(output, status)
        return check_out_put

    def reprepro_include_package(self, file_path, code_name=None, args=None,
                                 timeout=None):
        if code_name:
            self.code_name = code_name
        if (args):
            assert (isinstance(args, str)
                    ), "Expected string got {0} instead".format(type(args))
        file_format = file_path.split(".")[-1]
        if file_format == "deb":
            reprepro_list_args = "includedeb {code_name} {file_path} ".format(
                code_name=self.code_name, file_path=file_path)
        elif file_format == "udeb":
            reprepro_list_args = "includeudeb {code_name} {file_path} ".format(
                code_name=self.code_name, file_path=file_path)

        scan_command = self.default_command() + reprepro_list_args
        if (args):
            scan_command += " {0}".format(args)
        scan_shlex = shlex.split(scan_command)

        # Run the command and get the output
        output, status = self.run_command(scan_shlex, timeout=timeout)
        check_out_put = reprepro_include_package_parser(output, status)

        return check_out_put

    def reprepro_remove_package(self, package_name, code_name=None, args=None,
                                timeout=None):
        if code_name:
            self.code_name = code_name
        if (args):
            assert (isinstance(args, str)
                    ), "Expected string got {0} instead".format(type(args))

        reprepro_list_args = "remove {code_name} {package_name} ".format(
            code_name=self.code_name, package_name=package_name)

        scan_command = self.default_command() + reprepro_list_args
        if (args):
            scan_command += " {0}".format(args)
        scan_shlex = shlex.split(scan_command)

        # Run the command and get the output
        output, status = self.run_command(scan_shlex, timeout=timeout)
        check_out_put = reprepro_remove_package_parser(output, status)

        return check_out_put
