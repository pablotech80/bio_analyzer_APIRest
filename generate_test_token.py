from app import create_app, db
from app.models.user import User
from app.models.telegram import TelegramLinkToken
import sys

def generate():
    app = create_app()
    with app.app_context():
        # Buscar usuario de prueba o el primero disponible
        user = User.query.filter_by(email='testuser@coachbodyfit360.com').first()
        if not user:
            user = User.query.first()
        
        if not user:
            print("❌ No hay usuarios en la base de datos. Registra uno primero.")
            return

        # Eliminar tokens anteriores
        TelegramLinkToken.query.filter_by(user_id=user.id, used_at=None).delete()
        
        new_token = TelegramLinkToken(user_id=user.id)
        db.session.add(new_token)
        db.session.commit()
        
        print(f"✅ Token generado para {user.email}:")
        print(f"👉 {new_token.token}")
        print(f"⏳ Expira en 10 minutos.")
        print(f"⌨️  Escribe en Telegram: /link {new_token.token}")

if __name__ == "__main__":
    generate()
