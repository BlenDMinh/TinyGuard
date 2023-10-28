from http import HTTPStatus
from flask import request, Response


def image_input():
    print(request.files['imageFile'].save('current.jpg'))
    return Response(status=HTTPStatus.ACCEPTED)
