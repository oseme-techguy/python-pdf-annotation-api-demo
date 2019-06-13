"""PDF Annotation API - runner."""

def run_api(application):
    """Run the web application API
    Arguments:
        application -- The injected application
    """
    web_api = application.webapi()

    web_api.add_route(application.index_webhandler, '/')
    web_api.add_route(application.login_webhandler, '/login', methods=['POST'])
    web_api.add_route(application.get_users_webhandler, '/users/<user_id>', methods=['GET'])
    web_api.add_route(application.get_users_webhandler, '/users', methods=['GET'])
    web_api.add_route(application.create_user_webhandler, '/users', methods=['POST'])
    # web_api.add_route(application.interactive_message_webhandler, '/im')
    # web_api.add_route(application.init_survey_webhandler, '/users/initialise-survey/<service_id>', methods=['POST'])
    # web_api.add_route(application.start_survey_webhandler, '/users/survey-participants')

    web_api.run(
        host=application.config.api.host(),
        port=application.config.api.port(),
        debug=application.config.api.debug(),
    )
