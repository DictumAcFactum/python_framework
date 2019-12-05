from api import API

app = API()

@app.route("/home")
def home(request, response):
	response.text = "Hello from HOME page"


@app.route("/about")
def about(request, response):
	response.text = "Hello from ABOUT page"


@app.route("/hello/{name}")
def say_hello(request, response, name):
	response.text = f"Hello, {name}"


@app.route("/{author}/{book}")
class BookHandler:
	def get(self, request, response, author, book):
		response.text = f"{book} is written by {author}"


@app.route("/template")
def template_handler(request, response):
	response.body = app.template("index.html", context={'title': 'Best framework',
														'name': 'Django-killer'}).encode()