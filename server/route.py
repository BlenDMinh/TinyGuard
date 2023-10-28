from view.user_api import testuser
from view.index import index, test_api
from view.device_api import image_input

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
    },
    "/api/user/register": {
        "endpoint": "api user register",
        "view": testuser,
        "methods": ["POST"]
    },
    # body: {
    #   username
    #   age
    #   phone_number
    #   email
    #   password
    # }
    # return
    # if OK:
    #   normal http response
    # else:
    #   body: {
    #       errorMessage
    #   }

    "/api/user/login": {
        "endpoint": "api user login",
        "view": None,
        "methods": ["POST"]
    },
    # body: {
    #     phone_number
    #     password
    # }
    # if OK:
    #   normal http response
    # else:
    #   body: {
    #       errorMessage
    #   }

    "/api/user/device": {
        "endpoint": "api user add device",
        "view": None,
        "methods": ["POST"]
    },
    "/api/user/device": {
        "endpoint": "api user delete device",
        "view": None,
        "methods": ["DELETE"]
    },
    "/api/device/image_prediction": {
        "endpoint": "api get image prediction",
        "view": None,
        "methods": ["GET"]
    },
    "/api/device/image_input": {
        "endpoint": "api receive image from device",
        "view": image_input,
        "methods": ["POST"]
    },
    "/api/device/audio_prediction": {
        "endpoint": "api get audio prediction",
        "view": None,
        "methods": ["GET"]
    },
    "/api/device/audio_input": {
        "endpoint": "api receive audio from device",
        "view": None,
        "methods": ["POST"]
    }
}
