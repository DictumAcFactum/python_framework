from webob import Request, Response
from parse import parse
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
from middleware import Middleware

import os
import inspect


class API:
    def __init__(self, templates_dir="templates", static_dir="static"):
        # self.routes - dict for paths our app
        # self.templates_env - directory for html templates
        # self.exception_handler - default exception handler
        # self.whitenoise - static file serving class. Wraps an WSGI our app
        # self.middleware - it's a wrapper around our WSGI app that have the ability to modify requests and responses

        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        path_info = environ['PATH_INFO']

        # static file request case
        if path_info.startswith("/static"):
            # cut the "/static" prefix:
            # instead of - http://localhost:8000/static/main.css
            # it will be - http://localhost:8000/main.css
            environ['PATH_INFO'] = path_info[len("/static"):]
            return self.whitenoise(environ, start_response)

        # If not static file request
        # We are delegating the job of being an entrypoint to the middleware now
        return self.middleware(environ, start_response)

    def wsgi_app(self, environ, start_response):
        """
        environ: a dictionary with environment variables
        start_response:  a callback function that will be used to send
                         HTTP status and HTTP headers to the server
        """

        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()

        # kwargs - parsed arguments
        handler, kwargs = self.find_handler(request_path=request.path)

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    # class handler case
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError("Method not allowed.", request.method)
                    handler(request, response, **kwargs)

                # fuction handler case
                handler(request, response, **kwargs)
            else:
                self.default_response(response)

        except Exception as e:
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)

        return response

    def route(self, path):
        # decorator for application handlers
        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def test_session(self, base_url="http://testserver"):
        # session for testing
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
