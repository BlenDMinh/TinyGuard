from flask import jsonify, request, Response
from container import container, Component
from model.auth_model import LoginInfo, RegisterInfo
from service.auth_service import AuthenticationService


auth_service: AuthenticationService = container[Component.AuthenticationService]


def login():
    body = request.json
    login_info = LoginInfo.from_json(body)
    session = auth_service.login(login_info)
    return jsonify(session)


def register():
    body = request.json
    register_info = RegisterInfo.from_json(body)
    user = auth_service.register(register_info)
    return jsonify(user)
