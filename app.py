import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# دیتابیس کامل کاربران
users_db = {
    "user123": {
        "password": "123",
        "username": "user123",
        "total": 50,
        "used": 18.4,
        "remaining": 31.6,
        "days": 14,
        "signal": "4.5G عالی",
        "percent": 36,
        "private_message": "لطفاً جهت تمدید بسته ماهانه اقدام کنید."
    }
}

# دیتابیس چت‌ها
chats_db = {
    "user123": [
        {"is_admin": True, "message": "سلام! چطور می‌توانیم کمک‌تان کنیم؟"},
        {"is_admin": False, "message": "سلام، بسته من کی فعال میشه؟"}
    ]
}

@app.route('/')
def index():
    return render_template('index_new.html')

# --- بخش ورود و کاربران ---
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if username in users_db and users_db[username]['password'] == password:
        user_data = users_db[username].copy()
        user_data['success'] = True
        return jsonify(user_data)
    
    return jsonify({"success": False, "message": "نام کاربری یا رمز عبور اشتباه است!"})

# --- بخش چت زنده ---
@app.route('/api/chat/get/<username>', methods=['GET'])
def get_chat(username):
    chats = chats_db.get(username, [])
    return jsonify({"success": True, "chats": chats})

@app.route('/api/chat/send', methods=['POST'])
def send_chat():
    data = request.get_json() or {}
    username = data.get('username')
    message = data.get('message')
    is_admin = data.get('isAdmin', False)

    if username not in chats_db:
        chats_db[username] = []
    
    chats_db[username].append({"is_admin": is_admin, "message": message})
    return jsonify({"success": True})

# --- بخش خرید بسته ---
@app.route('/api/order', methods=['POST'])
def api_order():
    data = request.get_json() or {}
    package_name = data.get('packageName')
    price = data.get('price')
    return jsonify({
        "success": True, 
        "message": f"بسته {package_name} با موفقیت ثبت شد. مبلغ: {price} تومان"
    })

# --- بخش ادمین (رفع کامل ارورهای 404 و 405 لاگ) ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        return jsonify({"success": True, "message": "عملیات ادمین انجام شد"})
    return "پنل مدیریت فعال است"

@app.route('/admin/broadcast', methods=['GET', 'POST'])
def broadcast():
    if request.method == 'GET':
        return "روت برودکست فعال است"
    return jsonify({"success": True, "message": "پیام همگانی ارسال شد"})

@app.route('/admin/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    return jsonify({"success": True, "message": f"اطلاعات کاربر {user_id} بروزرسانی شد"})

@app.route('/admin/private_msg/<user_id>', methods=['POST'])
def private_msg(user_id):
    return jsonify({"success": True, "message": f"پیام اختصاصی فرستاده شد"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
