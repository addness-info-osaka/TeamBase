from flask import Blueprint, request, jsonify
from .models import db, Company, User, Plan
from datetime import datetime, timedelta

api = Blueprint('api', __name__)

@api.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    
    # 会社情報の登録
    company = Company(
        name=data['company_name'],
        email=data['company_email'],
        phone=data['phone'],
        address=data['address'],
        status='new'  # 新規ステータスを追加
    )
    db.session.add(company)
    
    # ユーザー情報の登録
    user = User(
        email=data['email'],
        name=data['name'],
        role='admin',
        company=company
    )
    db.session.add(user)
    
    # プラン情報の登録
    plan = Plan(
        name=data['plan_name'],
        company=company,
        price=data['plan_price'],
        start_date=datetime.utcnow(),
        status='active'
    )
    db.session.add(plan)
    
    try:
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '登録が完了しました',
            'company_id': company.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@api.route('/api/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'phone': c.phone,
        'address': c.address,
        'status': c.status,
        'created_at': c.created_at.isoformat(),
        'users': [{
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'role': u.role
        } for u in c.users]
    } for c in companies])

@api.route('/api/companies/<int:company_id>/status', methods=['PUT'])
def update_company_status(company_id):
    data = request.json
    company = Company.query.get_or_404(company_id)
    company.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'ステータスを更新しました'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
