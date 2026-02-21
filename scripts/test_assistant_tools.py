import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

from app import create_app
from app.services.fitmaster_service import FitMasterService

class Config:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = '/tmp/uploads'
    
app = create_app('development')
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

with app.app_context():
    print("Probando _tool_get_user_history (user_id=1):")
    print(FitMasterService._tool_get_user_history(1, {"limit": 2}))
    
    print("\nProbando _tool_get_current_plans (user_id=1):")
    print(FitMasterService._tool_get_current_plans(1))
