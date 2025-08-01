from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 세션 암호화 키 (실제 배포 시에는 고정값으로 바꾸세요)

# 메모리 기반 유저 저장소 (임시 DB 역할)
users = {}

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            flash("이미 존재하는 아이디입니다.")
        else:
            users[username] = password
            flash("회원가입이 완료되었습니다. 로그인해주세요.")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("mypage"))
        else:
            flash("아이디 또는 비밀번호가 올바르지 않습니다.")
    return render_template("login.html")

@app.route("/mypage")
def mypage():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("mypage.html", username=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("로그아웃 되었습니다.")
    return redirect(url_for("login"))
