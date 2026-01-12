from flask import render_template, redirect, url_for, flash, request, session, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from datetime import datetime, timedelta
from app.models import User, UserRole
from app.routes import auth_bp
from config import Config
from app import db, mail
import random

@auth_bp.route("/girisyap", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Geçersiz e-posta veya şifre.", "error")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash(f"Hoşgeldiniz, {user.firstname}!", "success")
        return redirect(url_for("home.homepage"))
    return render_template("auth/login.html")

@auth_bp.route("/kayitol", methods=["GET", "POST"])
def register():
    flash("[TEST] Kayıt sayfası yüklendi.", "info")
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if User.query.filter_by(email=email).first():
            flash("Bu e-posta zaten kayıtlı.", "error")
            return redirect(url_for("auth.register"))
        
        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            role=UserRole.USER if role == "student" else UserRole.MENTOR
        )
        if not Config.EMAIL_VERIFICATION_ENABLED:
            new_user.is_verified = True
            new_user.set_password(password)
            if User.query.count() == 0:
                new_user.role = UserRole.ADMIN
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash(f"Hoşgeldiniz, {new_user.firstname}!", "success")
            return redirect(url_for("home.homepage"))

        if User.query.count() == 0:
            new_user.role = UserRole.ADMIN

        new_user.set_password(password)

        session["pending_user_email"] = email
        verification_code = random.randint(100000, 999999)
        code_expiry = datetime.utcnow() + timedelta(minutes=10)
        msg = Message(subject="RoboGeb E-posta Doğrulama Kodu", sender=mail.default_sender, recipients=[email])
        msg.html = render_template("emails/verify_email.html", code=verification_code, firstname=firstname)
        try:
            mail.send(msg)
        except Exception as e:
            flash("Doğrulama e-postası gönderilirken bir hata oluştu. Lütfen tekrar deneyin.", "error")
            print(f"\033[31m[HATA] E-posta gönderilemedi: {e}\033[0m")
            return abort(500)

        new_user.verification_code = verification_code
        new_user.code_expiry = code_expiry

        db.session.add(new_user)
        db.session.commit()
        flash("Kayıt başarılı! Şimdi e-posta adresinizi doğrulayın.", "success")
        return redirect(url_for("auth.verify_email"))
    return render_template("auth/register.html")

@auth_bp.route("/eposta_dogrulama", methods=["GET", "POST"])
def verify_email():
    if request.method == "POST":
        input_code = int(request.form.get("full_code"))
        email = session.get("pending_user_email")
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Önce kayıt olmalısınız!", "error")
            return redirect(url_for("auth.register"))
        
        if datetime.utcnow() > user.code_expiry:
            flash("Doğrulama kodunuz süresi doldu. Lütfen tekrar kayıt olun.", "error")
            session.pop("pending_user_email", None)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("auth.register"))
        
        if user.verification_code != input_code:
            flash("Yanlış doğrulama kodu. Lütfen tekrar deneyin.", "error")
            flash(f"[DEBUG] Doğru kod: {user.verification_code} Alınan kod: {input_code}", "info")
            return redirect(url_for("auth.verify_email"))
        
        user.is_verified = True
        user.verification_code = None
        user.code_expiry = None
        session.pop("pending_user_email", None)
        db.session.commit()
        flash(f"Her şey hazır! Hoşgeldiniz, {user.firstname}.", "success")
        login_user(user)
        return redirect(url_for("home.homepage"))
    return render_template("auth/verify_email.html")


@auth_bp.route("/cikisyap")
@login_required
def logout():
    logout_user()
    flash("Başarıyla çıkış yaptınız.", "success")
    return redirect(url_for("home.homepage"))
