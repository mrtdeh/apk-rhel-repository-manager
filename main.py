import datetime
from api.api import Ping, RepreproListPackages, IncludePackage, RemovePackage
import flask
import flask_restful
from flask_cors import CORS
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp
from logger.logger import get_logger
from prometheus_flask_exporter import RESTfulPrometheusMetrics

logger = get_logger(__name__)


def create_app():

    logger.info("start api server")
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)
    CORS(app)
    metrics = RESTfulPrometheusMetrics.for_app_factory(group_by='endpoint')
    metrics.init_app(app, api)
    metrics.info('app_info', 'Application info', version='1.0.3')

    class User(object):
        def __init__(self, id, username, password):
            self.id = id
            self.username = username
            self.password = password

        def __str__(self):
            return "User(id='%s')" % self.id

    users = [
        User(1, 'APKISO', 'password'),

    ]

    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}

    def authenticate(username, password):
        user = username_table.get(username, None)
        if user and safe_str_cmp(user.password.encode('utf-8'),
                                 password.encode('utf-8')):
            logger.info("Accepted password for : {}".format(username))
            return user
        else:
            logger.warning(
                "user or password incorrect for : {}".format(username))

    def identity(payload):
        user_id = payload['identity']
        return userid_table.get(user_id, None)

    app.config['SECRET_KEY'] = 'P@ssw0rdM@t@6810'
    JWT(app, authenticate, identity)

    app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=100)

    api.add_resource(Ping, "/ping")
    api.add_resource(RepreproListPackages, "/list_packages")
    api.add_resource(IncludePackage, "/include_package")
    api.add_resource(RemovePackage, "/remove_package")

    return app
