from flask_jwt import jwt_required
from flask import flash, request
import flask_restful
from werkzeug.utils import secure_filename
from logger.logger import get_logger
from reprepro_tools.reprepro import Reprepro
from config.config import get_config
from subprocess import Popen, PIPE

import repomd;

import os
config_app = get_config()
logger = get_logger(__name__)

target_repo_path = "/usr/share/nginx/html/repo/"

target_platform = "rhel-8-server-rpms/"


repo = repomd.load('ftp://' + target_repo_path)


class Ping(flask_restful.Resource):
    decorators = [jwt_required()]

    def get(self):
        logger.info("ping")
        return "pong", 200


class RepreproListPackages(flask_restful.Resource):
    decorators = [jwt_required()]

    def get(self):
        logger.info("ping")

        # list_packages  = repo.findall()
        
        return "list_packages"

        # reprepro = Reprepro()
        # list_packages = reprepro.reprepro_list_packages()
        # return list_packages
        


ALLOWED_EXTENSIONS = {'deb', 'udeb'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class IncludePackage(flask_restful.Resource):
    decorators = [jwt_required()]

    def post(self):
        logger.info("IncludeDeb")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part', 403
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No selected file', 403
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(config_app["app"]["upload_dir"], filename)
            file.save(file_path)

            Popen(["mkdir","-p",target_repo_path + target_platform])
            Popen(["mv","-f",file_path,target_repo_path + target_platform])
            Popen(["createrepo" ,"-d" ,"--update",target_repo_path])


            # reprepro = Reprepro()
            # status = reprepro.reprepro_include_package(file_path=file_path)

            return "OK"
        return 403, "error. try again"


class RemovePackage(flask_restful.Resource):
    decorators = [jwt_required()]

    def delete(self):
        data = request.get_json()
        name = data.get("package_name", None)
        if not name:
            return "key:package_name not found", 400
        # reprepro = Reprepro()
        # status = reprepro.reprepro_remove_package(package_name=name)
        return "not prepared yet"
