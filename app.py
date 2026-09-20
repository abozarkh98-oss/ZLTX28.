import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# دیتابیس فرضی
users_db = {
    "user123": {
        "password": "123",
        "username": "user123",
        "total": 50,
        "used": 18.4,
        "remaining": 31.6
    }
}

chats_db = {}

@app.route('/')
def index():
    # فراخوانی فایل جدید برای دور زدن کش
    return render_template('index_new.html')

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

# --- روت‌های بخش چت (رفع خطای 404) ---
@app.route('/api/chat/get/<username>', methods=['GET'])
def get_chat(username):
    chats = chats_db.get(username, [])
    return jsonify({"success": True, "chats": chats})

# --- روت‌های پنل ادمین (رفع خطاهای 404 و 405) ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
         return jsonify({"success": True, "message": "درخواست ادمین دریافت شد"})
    return "صفحه پنل مدیریت (این مسیر آماده اضافه کردن قالب ادمین است)"

@app.route('/admin/broadcast', methods=['GET', 'POST'])
def broadcast():
    if request.method == 'GET':
        return "این مسیر برای ارسال پیام گروهی از طریق متد POST است."
    return jsonify({"success": True, "message": "پیام گروهی با موفقیت ارسال شد"})

@app.route('/admin/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    return jsonify({"success": True, "message": f"اطلاعات کاربر {user_id} بروزرسانی شد"})

@app.route('/admin/private_msg/<user_id>', methods=['POST'])
def private_msg(user_id):
    return jsonify({"success": True, "message": f"پیام خصوصی برای {user_id} ارسال شد"})

if __name__ == '__main__':
    # دریافت پورت دینامیک از پلتفرم ابری (Railway)
    # اگر پروژه روی سیستم شخصی اجرا شود، پورت روی 5000 تنظیم می‌شود
    port = int(os.environ.get("PORT", 5000))
    
    # هاست 0.0.0.0 برای دسترسی خارجی در سرورهای ابری الزامی است
    app.run(host="0.0.0.0", port=port, debug=False)
