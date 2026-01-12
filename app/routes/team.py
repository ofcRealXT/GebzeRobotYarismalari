from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from flask_mail import Message
from app.models import User, UserRole, Team, TeamMember, TeamRole, Category
from app.utils import role_required
from app.routes import team_bp
from app import db

@team_bp.route("/takim/olustur", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        your_role = request.form.get("your_role")
        edc_level = request.form.get("edc_level")
        full_school = request.form.get("school")

        if not name or not your_role or not edc_level or not full_school:
            flash("Formun tamamını doldurmalısınız.", "error")

        new_team = Team(
            name=name,
            description=description,
            edc_level=edc_level.upper(),
            full_school=full_school
        )
        db.session.add(new_team)
        db.session.commit()

        new_team_member = TeamMember(
            user_id=current_user.id,
            team_id=new_team.id
        )
        db.session.add(new_team_member)

        if your_role == "captain":
            new_team_member.role = TeamRole.CAPTAIN
        else:
            new_team_member.role = TeamRole.MENTOR
        
        current_user.team_id=new_team.id
        current_user.role = UserRole.PARTICIPANT
        db.session.commit()
        flash("Takımınız başarıyla kuruldu!", "success")
        return redirect(url_for("team.dashboard"))
    return render_template("team/create.html")

@team_bp.route("/takimim")
@role_required(UserRole.PARTICIPANT)
@login_required
def dashboard():
    team_member = TeamMember.query.filter_by(user_id=current_user.id).first()
    if not team_member:
        flash("Henüz bir takımınız yok.", "info")
        return redirect(url_for("home.homepage"))

    team = Team.query.get(team_member.team_id)
    members = TeamMember.query.filter_by(team_id=team.id).all()
    return render_template("team/dashboard.html", team=team, members=members)

@team_bp.route("/takim/uye_ekle", methods=["GET", "POST"])
@role_required(UserRole.PARTICIPANT)
@login_required
def add_member():
    if request.method == "POST":
        email = request.form.get("email")
        target_user = User.query.filter_by(email=email).first()
        if not target_user:
            flash("Bu e-postaya ait bir kullanıcı bulunamadı.", "error")
            return redirect(url_for("team.dashboard"))
        
        target_user.role = UserRole.PARTICIPANT
        target_user.team_id = current_user.team_id
        new_team_member = TeamMember(
            user_id=target_user.id,
            team_id= current_user.team_id,
            role = TeamRole.MEMBER
        )

        db.session.add(new_team_member)
        db.session.commit()
        flash("Üye eklendi.", "success")
        return redirect(url_for("team.dashboard"))

@team_bp.route("/takim/uye_kaldir/<int:team_id>/<int:member_id>", methods=["POST"])
@role_required(UserRole.PARTICIPANT)
@login_required
def remove_member(team_id, member_id):
    current_tmember = TeamMember.query.filter_by(user_id=current_user.id).first()
    if not current_tmember or current_tmember.role == TeamRole.MEMBER:
        flash("Bu işlem için yetkiniz yok!", "error")
        return redirect(url_for("home.homepage"))
    
    target_tmember = TeamMember.query.filter_by(user_id=member_id, team_id=team_id).first()
    if not target_tmember:
        flash("Belirtilen takımda belirtilen üye bulunamadı.", "error")
        return redirect(url_for("team.dashboard"))
    
    db.session.delete(target_tmember)
    db.session.commit()
    flash("Üye kaldırıldı.", "success")
    return redirect(url_for("team.dashboard"))

@team_bp.route("/takim/basvur")
def apply():
    return "Henüz hazır değil."
