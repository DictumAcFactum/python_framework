import pytest

from api import API


def test_basic_route(api):
	@api.route("/home")
	def home(req, resp):
		resp.text = "YOLO"


def test_route_overlap_throws_exceprions(api):
	@api.route("/home")
	def home(req, resp):
		resp.text = "YOLO"

	with pytest.raises(AssertionError):
		@api.route("/home")
		def home2(req, resp):
			resp.text = "YOLO"




def test_client_can_send_requests(api, client):
	RESPONSE_TEXT = "THIS IS COOL"

	@api.route("/hey")
	def cool(req, resp):
		resp.text = RESPONSE_TEXT

	assert client.get("http://testserver/hey").text == RESPONSE_TEXT


def test_parameterized_route(api, client):
	@api.route("/{name}")
	def hello(req, resp, name):
		resp.text = f"Hey, {name}"

	assert client.get("http://testserver/alex").text == "Hey, alex"


def test_default_404_response(api, client):
	response = client.get("http://testserver/doesnotexist")

	assert response.status_code == 404
	assert response.text == "Not found."


def test_class_base_handlers_POST_GET(api, client):
	@api.route("/unicorn")
	class Unicorn:
		def get(self, req, resp):
			resp.text = "Pink unicorn"

		def post(self, req, resp):
			resp.text = "Green unicorn"


	assert client.get("http://testserver/unicorn").text == "Pink unicorn"
	assert client.post("http://testserver/unicorn").text == "Green unicorn"


def test_class_handlers_method_not_allowed(api, client):
	@api.route("/gunicorn")
	class Gunicorn:
		def put(self, req, resp):
			resp.text = "Put not allowed."

	assert client.put("http://testserver/gunicorn").text == "Put not allowed."