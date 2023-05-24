from flask import Flask, render_template,request,redirect
from pymongo import MongoClient

#實體化Flask物件
app = Flask(__name__)
#設定金鑰
app.secret_key = 'your_secret_key'

# 連接Mongo的database
client = MongoClient("mongodb+srv://root:root123@cluster0.0y6vcg2.mongodb.net/?retryWrites=true&w=majority") 
db = client['test'] #選擇要操作的database名稱
collection = db['users']  #選擇要操作的collection

#設定登入頁面路由
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        #檢查使用者帳號是否存在
        existing_user = collection.find_one({'username': username,'password':password})
        if existing_user:
            return redirect('/dashboard')
        
        return redirect('/login_failed')
    return render_template('login.html')

#設定dashboard路由
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#設定註冊頁面路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 檢查帳號是否已存在
        existing_user = collection.find_one({'username': username})
        if existing_user:
            return redirect('/register_failed')

        # 將使用者資料插入資料庫
        new_user = {'username': username, 'password': password}
        collection.insert_one(new_user)

        return redirect('/register_success')

    return render_template('register.html')

#設定登入失敗頁面路由
@app.route('/login_failed')
def failed1():
    return render_template('login_failed.html')

#設定註冊成功頁面路由
@app.route('/register_success')
def success():
    return render_template('register_success.html')

#設定註冊失敗頁面路由
@app.route('/register_failed')
def failed2():
    return render_template('register_failed.html')

#啟動網站
if __name__ == '__main__':
  app.run(debug=True)