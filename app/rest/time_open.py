from flask_restx import Namespace, Resource

from app.controller.time_open_controller import TimeOpenController


time_open_api = Namespace("time_open", description="API for openings times")


@time_open_api.route('/is_open_on')
class IsOpenOn(Resource):

    @time_open_api.doc(description="Get html page with info of showing if currently open.")
    @time_open_api.response(200, 'Return html page with info showing if currently open.')
    def get(self):
        return TimeOpenController().get_open_currently()


@time_open_api.route('/next_opening_date')
class IsOpenOn(Resource):

    @time_open_api.doc(description="Get html page with info of showing next opening.")
    @time_open_api.response(200, 'Return html page with info showing next opening.')
    def get(self):
        return TimeOpenController().get_open_next()
