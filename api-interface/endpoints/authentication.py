from flask import request, jsonify

def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        return 'Authentication'
    return jsonify({'error': 'You must send an email and a password'}), 400

def register_routes(app):
    app.add_url_rule('/login', 'login', login, methods=['POST'])
