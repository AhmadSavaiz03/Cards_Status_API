from flask import Blueprint, request, jsonify
from models.card import Card
from sqlalchemy.exc import SQLAlchemyError
import re
import logging

bp = Blueprint('api', __name__)
logging.basicConfig(level=logging.INFO)

@bp.route('/get_card_status', methods=['GET'])
def get_card_status():
    try:
        card_id = request.args.get('card_id')
        user_phone = request.args.get('user_phone')

        # Validate card_id format
        if card_id and not re.match(r'^[A-Z0-9]+$', card_id):
            return jsonify({"error": "Invalid card ID format"}), 400
        
        # Validate user_phone format
        if user_phone and not re.match(r'^\d{9}$', user_phone):
            return jsonify({"error": "Invalid phone number format"}), 400
        
        # Build query filters based on provided parameters
        query_filters = []
        if card_id:
            query_filters.append(Card.card_id == card_id)
        if user_phone:
            query_filters.append(Card.user_phone == user_phone)

        if not query_filters:
            return jsonify({"error": "Missing card_id or user_phone parameters"}), 400

        try:
            card = Card.query.filter(*query_filters).first()

            if card:
                return jsonify({
                    "card_id": card.card_id, 
                    "user_phone": card.user_phone, 
                    "status": card.status, 
                    "last_updated": card.last_updated.isoformat()
                })
            else:
                return jsonify({"error": "Card not found"}), 404
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError occurred: {e}")
            return jsonify({"error": "An error occurred while processing your request"}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
