from http import HTTPStatus
import json
from flask import jsonify, request, Response
from flask_socketio import emit, send
from config import socketio
from container import container, Component, Event
from model.predict_model import ImagePredict
from service.device_service import DeviceService
from service.models import WrapResponseDto



def image_input():
    image = request.files.get('imageFile')
    if not image:
        return Response(
            headers={
                "Content-Type": "application/json"
            },
            response=json.dumps(WrapResponseDto.error("Bad request", "imageFile is missing").to_json()),
            status=HTTPStatus.BAD_REQUEST
        )
    
    device_service: DeviceService = container.get(Component.DeviceService)
    prediction: ImagePredict = device_service.predict_image(image)
    emit(Event.ImagePrediction, prediction.to_json(),
         namespace="/test_i", broadcast=True)
    return Response(
        headers={
            "Content-Type": "application/json"
        },
        response=json.dumps(WrapResponseDto.success(prediction.to_json(), "Successfully").to_json()),
        status=HTTPStatus.OK
    )

def audio_input():
    audio = request.files.get('audioFile')
    audio.save('audio.wav')
    return Response("OK")