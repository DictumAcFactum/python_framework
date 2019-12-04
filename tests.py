import pytest

from api import API

@pytest.fixture
def api():
	return API()


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