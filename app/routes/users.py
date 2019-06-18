"""PDF Annotation API application - user routes"""

from sanic_jwt import protected, scoped


def set_user_routes(web_api, controller):
    """
        Users Endpoint
    """
    # web_api.add_route(app_controllers.user().login, '/login', methods=['POST']) # Login

    @web_api.route('/users/<user_id>', methods=['GET']) # get one
    @protected()
    @scoped('manager')
    def route_user(request, *args, **kwargs):
        return controller.get_users(request, *args, **kwargs)

    @web_api.route('/users', methods=['GET']) # get all
    @protected()
    @scoped('manager')
    def route_users(request, *args, **kwargs):
        return controller.get_users(request, *args, **kwargs)

    @web_api.route('/users', methods=['POST']) # add user
    @protected()
    @scoped('manager')
    def route_add_users(request, *args, **kwargs):
        return controller.add_users(request, *args, **kwargs)

    @web_api.route('/users/<user_id>', methods=['PATCH']) # patch user
    @protected()
    @scoped('manager')
    def route_patch_users(request, *args, **kwargs):
        return controller.update_users(request, *args, **kwargs)

    @web_api.route('/users', methods=['DELETE']) # delete user
    @protected()
    @scoped('manager')
    def route_delete_users(request, *args, **kwargs):
        return controller.delete_users(request, *args, **kwargs)
