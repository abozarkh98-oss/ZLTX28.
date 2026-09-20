from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

users_db = {
    "user123": {
        "password": "123",
        "username": "user123",
        "total": 50,
        "used": 18.4,
        "remaining": 31.6
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users_db and users_db[username]['password'] == password:
        user_data = users_db[username].copy()
        user_data['success'] = True
        return jsonify(user_data)
    
    return jsonify({"success": False, "message": "نام کاربری یا رمز عبور اشتباه است!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
