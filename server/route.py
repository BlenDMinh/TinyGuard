from view.index import index, test_api

route = {
    "/": {
        "endpoint": "index",
        "view": index,
        "methods": ["GET"]
    },
    "/api/test": {
        "endpoint": "api - test",
        "view": test_api,
        "methods": ["GET"]
    }
}
