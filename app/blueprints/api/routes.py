# app/blueprints/api/routes.py
"""
API REST Routes
Endpoints JSON para frontend futuro
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.api import api_bp
from app.models.biometric_analysis import BiometricAnalysis
from app.models.contact_message import ContactMessage
from app import db


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'CoachBodyFit360 API',
        'version': 'v1.0.0'
    }), 200


@api_bp.route('/analysis/<int:analysis_id>', methods=['GET'])
@login_required
def get_analysis(analysis_id):
    """
    GET /api/v1/analysis/<id>
    
    Retorna análisis completo en JSON (datos + FitMaster)
    """
    analysis = BiometricAnalysis.query.get(analysis_id)
    
    if not analysis:
        return jsonify({
            'status': 'error',
            'message': 'Análisis no encontrado'
        }), 404
    
    # Verificar permisos
    if analysis.user_id != current_user.id and not current_user.is_admin:
        return jsonify({
            'status': 'error',
            'message': 'Sin permiso para ver este análisis'
        }), 403
    
    return jsonify({
        'status': 'success',
        'data': analysis.to_dict()
    }), 200


@api_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    """
    GET /api/v1/history
    
    Retorna historial de análisis del usuario en JSON
    """
    analyses = BiometricAnalysis.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'status': 'success',
        'count': len(analyses),
        'data': [analysis.to_dict() for analysis in analyses]
    }), 200


@api_bp.route('/analysis', methods=['POST'])
@login_required
def create_analysis():
    """
    POST /api/v1/analysis
    
    Crea nuevo análisis biométrico desde JSON
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['weight', 'height', 'age', 'gender', 'neck', 'waist']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Campo requerido: {field}'
                }), 400
        
        # TODO: Implementar creación desde API
        # Por ahora retorna 501 Not Implemented
        return jsonify({
            'status': 'error',
            'message': 'Endpoint en desarrollo. Usa el formulario web.'
        }), 501
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """
    GET /api/v1/profile
    
    Retorna datos del usuario actual
    """
    return jsonify({
        'status': 'success',
        'data': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'is_admin': current_user.is_admin,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None
        }
    }), 200


@api_bp.route('/contact', methods=['POST'])
@login_required
def send_message():
    """
    POST /api/v1/contact
    
    Enviar mensaje de contacto al entrenador
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('subject') or not data.get('message'):
            return jsonify({
                'status': 'error',
                'message': 'Subject y message son requeridos'
            }), 400
        
        # Crear mensaje
        message = ContactMessage(
            user_id=current_user.id,
            subject=data['subject'],
            message=data['message'],
            analysis_id=data.get('analysis_id')  # Opcional
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Mensaje enviado correctamente',
            'data': message.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/admin/messages', methods=['GET'])
@login_required
def get_messages():
    """
    GET /api/v1/admin/messages
    
    Ver todos los mensajes (solo admin)
    """
    if not current_user.is_admin:
        return jsonify({
            'status': 'error',
            'message': 'Acceso denegado. Solo administradores.'
        }), 403
    
    # Filtros opcionales
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    
    query = ContactMessage.query
    
    if unread_only:
        query = query.filter_by(is_read=False)
    
    messages = query.order_by(ContactMessage.created_at.desc()).all()
    
    return jsonify({
        'status': 'success',
        'count': len(messages),
        'unread_count': ContactMessage.query.filter_by(is_read=False).count(),
        'data': [msg.to_dict() for msg in messages]
    }), 200


@api_bp.route('/admin/messages/<int:message_id>', methods=['PATCH'])
@login_required
def mark_message_read(message_id):
    """
    PATCH /api/v1/admin/messages/<id>
    
    Marcar mensaje como leído (solo admin)
    """
    if not current_user.is_admin:
        return jsonify({
            'status': 'error',
            'message': 'Acceso denegado. Solo administradores.'
        }), 403
    
    message = ContactMessage.query.get(message_id)
    
    if not message:
        return jsonify({
            'status': 'error',
            'message': 'Mensaje no encontrado'
        }), 404
    
    message.mark_as_read()
    
    return jsonify({
        'status': 'success',
        'message': 'Mensaje marcado como leído',
        'data': message.to_dict()
    }), 200
