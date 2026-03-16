from flask import Blueprint, request, jsonify
from services.ml_service import get_prediction

transformer_bp = Blueprint("transformer_bp", __name__)

@transformer_bp.route("/predict", methods=["POST"])
def predict():

    data = request.json

    result = get_prediction(data)

    return jsonify(result)