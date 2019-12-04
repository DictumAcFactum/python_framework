from webob import Request, Response
from parse import parse

import inspect

class API:
	def __init__(self):
		# self.routes - dict for paths our application
		self.routes = {}


	def __call__(self, environ, start_response):
		request = Request(environ)

		response = self.handle_request(request)

		return response(environ, start_response)

	def handle_request(self, request):
		response = Response()

		handler, kwargs = self.find_handler(request_path=request.path)

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
		
		return response


	def route(self, path):
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
			print("PATH:", path, "Request-path:", request_path)
			parse_result = parse(path, request_path)
			print("PARSE RESULT:", {parse_result})
			if parse_result is not None:
				return handler, parse_result.named

		return None, None
