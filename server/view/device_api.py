from http import HTTPStatus
from flask import jsonify, request, Response
from flask_socketio import emit, send
from config import socketio
from container import container, Component, Event
from model.predict_model import ImagePredict
from service.device_service import DeviceService


def image_input():
    image = request.files.get['imageFile']
    if not image:
        return Response(status=HTTPStatus.NOT_FOUND)
    device_service: DeviceService = container.get(Component.DeviceService)
    prediction: ImagePredict = device_service.predict_image(image)
    emit(Event.ImagePrediction, prediction.to_json(),
         namespace="/", broadcast=True)
    return jsonify(prediction.to_json())
