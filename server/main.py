from flask import Flask

app = Flask("Baby recognition")

if __name__ == "__main__":
    from config import config
    from route import route
    for url, handler in route.items():
        app.add_url_rule(
            url, endpoint=handler["endpoint"], view_func=handler["view"], methods=handler["methods"])
    app.run(
        debug=config["debug"],
        port=config["port"],
        host=config["host"]
    )
