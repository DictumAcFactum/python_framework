from api import API
from middleware import Middleware

app = API()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, request):
        print("Processing request", request.url)

    def process_response(self, request, response):
        print("Processing response", request.url)


app.add_middleware(SimpleCustomMiddleware)


def custom_exceptions_handler(request, response, exception_cls):
    response.text = "Oops! Something went wrong."


app.add_exception_handler(custom_exceptions_handler)


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
    response.body = app.template("index.html",
                                 context={'title': 'Best framework', 'name': 'Django-killer'}).encode()
