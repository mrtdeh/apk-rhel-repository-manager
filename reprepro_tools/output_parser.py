
from logger.logger import get_logger
logger = get_logger(__name__)


def reprepro_list_packages_parser(command_out_put, status):
    list_packages = list()
    packages_info = dict()
    try:
        for line in status.split("\n"):
            logger.debug(line)
            template = {"package_name": None, "architectures": None,
                        "codename": None, "component": None}
            info, package_name, version = line.split(" ")
            info_list = info.split("|")
            codename = info_list[0]
            component = info_list[1]
            architectures = info_list[2]
            template["package_name"] = package_name
            template["codename"] = codename
            template["component"] = component
            template["architectures"] = architectures
            template["version"] = version
            list_packages.append(template)
        len_packages = len(list_packages)
        packages_info["count"] = len_packages
        packages_info["packages"] = list_packages
        return packages_info, 200
    except Exception:
        logger.error("an error in parse list packages:", exc_info=True)
        return "error in parse output command", 500


def reprepro_include_package_parser(command_out_put, status):
    if not status:
        if "as it has already" in command_out_put:
            return "package with this version already exists.(for replace\
                 first use delete api)", 400
        if "Premature end of reading" in command_out_put:
            # return "can not read package file. There have been errors"
            return "Premature end of reading package.\
                 There have been errors!", 400

    return "package successful included", 200


def reprepro_remove_package_parser(command_out_put, status):
    if "Not removed as not found" in command_out_put:
        return command_out_put, 400
    if "Deleting files no longer reference" in command_out_put:
        return "package was successful deleted", 200
    return "done"
