from view.user_api import testuser
from view.index import index
from view.device_api import audio_input, image_input
from view.auth_api import login, register

route = {
    "/": {
        "endpoint": "index",
        "view": index,
        "methods": ["GET"]
    },
    "/api/user/register": {
        "endpoint": "api user register",
        "view": register,
        "methods": ["POST"]
    },
    "/api/user/login": {
        "endpoint": "api user login",
        "view": login,
        "methods": ["POST"]
    },
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
        "view": audio_input,
        "methods": ["POST"]
    }
}
