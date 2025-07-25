from flask import Blueprint, request, jsonify
from backend.utils.coach_prompt import get_motivational_prompt

coach_bp = Blueprint("coach", __name__)

@coach_bp.route("/coach/prompt", methods=["POST"])
def coach_prompt():
    data = request.get_json()
    domain = data.get("domain", "").lower()
    
    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    prompt = get_motivational_prompt(domain)
    return jsonify({"prompt": prompt})
