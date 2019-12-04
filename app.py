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

