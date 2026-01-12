from flask import render_template, flash, send_from_directory
from flask_login import current_user, login_user
from app.models import User, UserRole, TeamMember, TeamRole, Category
from app.routes import home_bp
from app import db
import os

@home_bp.route("/")
def homepage():
    cts = Category.query.all()
    return render_template("home/homepage.html", cts=cts)

@home_bp.route("/hakkimizda")
def aboutus():
    return render_template("home/aboutus.html")

@home_bp.route("/iletisim")
def contact():
    return render_template("home/contact.html")

@home_bp.route("/duyurular")
def announcements():
    return render_template("home/announcements.html")

@home_bp.route("/yarislar")
def competitions():
    cts = Category.query.all()
    return render_template("home/competitions.html", cts=cts)

@home_bp.route("/sss")
def sss():
    return render_template("home/sss.html")

@home_bp.route("/kilavuz")
def download_guide():
    return send_from_directory("static/docs", "ornekSartname.pdf", as_attachment=True)

@home_bp.route("/kvkk")
def kvkk():
    return render_template("home/kvkk.html")

@home_bp.route("/debug")
def debug():
    return "Düzeltmeler yapıldı."
