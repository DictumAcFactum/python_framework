from webob import Request


class Middleware:
    """
    It's a wrapper around our WSGI app that have the ability
    to modify requests and responses

    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # middleware should implement the WSGI entrypoint interface
        request = Request(environ)

        response = self.app.handle_request(request)
        return response(environ, start_response)

    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)

    def process_request(self, request):
        # will be implemented by child classes
        pass

    def process_response(self, request, response):
        # will be implemented by child classes
        pass

    def handle_request(self, request):
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response
