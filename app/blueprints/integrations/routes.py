from flask import jsonify, request
from flask_login import current_user, login_required
from app import db, csrf
from app.models.telegram import TelegramLinkToken
from . import telegram_bp
from app.services.telegram_service import TelegramIntegrationService
import logging


logger = logging.getLogger(__name__)


@telegram_bp.route("/link-token", methods=["POST"])
@login_required
def generate_link_token():
    """
    Genera un token temporal para vincular la cuenta de Telegram.
    """
    # Eliminar tokens anteriores no usados
    TelegramLinkToken.query.filter_by(user_id=current_user.id, used_at=None).delete()
    
    new_token = TelegramLinkToken(user_id=current_user.id)
    db.session.add(new_token)
    db.session.commit()

    return jsonify({
        "status": "success",
        "token": new_token.token,
        "expires_at": new_token.expires_at.isoformat()
    }), 201


@telegram_bp.route("/webhook", methods=["POST"])
@csrf.exempt
def webhook():
    """
    Endpoint para recibir webhooks de Telegram.
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "no data"}), 400

    logger.info(f"Telegram webhook received: {data}")

    # Procesar datos de forma asíncrona podrías ser mejor,
    # pero por ahora lo manejamos directo en el request
    try:
        TelegramIntegrationService.process_webhook_data(data)
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")

    return jsonify({"status": "received"}), 200
