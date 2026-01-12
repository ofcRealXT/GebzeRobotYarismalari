from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.utils import role_required
from app.routes import admin_bp
from app.models import User, UserRole, Team, Announcement, Category
from config import ALLOWED_IMG_EXTENSIONS
from app import db
import os

@admin_bp.route('/admin/panel')
@login_required
@role_required(UserRole.ADMIN)
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/admin/kullanicilar')
@login_required
@role_required(UserRole.ADMIN)
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)


@admin_bp.route("/admin/takimlar")
@login_required
@role_required(UserRole.ADMIN)
def manage_teams():
    teams = Team.query.all()
    return render_template("admin/manage_teams.html", teams=teams)


@admin_bp.route("/admin/kategoriler")
@login_required
@role_required(UserRole.ADMIN)
def manage_categories():
    cts = Category.query.all()
    return render_template("admin/categories.html", cts=cts)


@admin_bp.route("/admin/kategori_ekle", methods=["GET", "POST"])
@login_required
@role_required(UserRole.ADMIN)
def add_ct():
    if request.method == "POST":
        name = request.form.get("name")
        banner = request.files.get("banner")
        guide = request.files.get("guide")
        description = request.form.get("description")

        if not name or not description:
            flash("İsim ve açıklama gerekli!", "error")
            return redirect(url_for("admin.add_ct"))
        
        if Category.query.filter_by(name=name).first():
            flash("Böyle bir kategori zaten var!","error")
            return redirect(url_for("admin.manage_categories"))
        
        new_ct = Category(
            name=name,
            description=description
        )
        db.session.add(new_ct)
        db.session.commit()

        if banner:
            extension = banner.filename.rsplit(".", 1)[1].lower()
            if not extension in ALLOWED_IMG_EXTENSIONS:
                flash("Yüklediğiniz resim uzantısı desteklenmiyor.", "error")
                return redirect(url_for("admin.add_ct"))
            
            new_ct.banner = f"images/ct_banners/{new_ct.id}.{extension}"
            banner.save(os.path.join("app/static", new_ct.banner))

        if guide:
            extension = guide.filename.rsplit(".", 1)[1].lower()
            
            new_ct.guide = f"docs/categories/{new_ct.id}.{extension}"
            guide.save(os.path.join("app/static", new_ct.guide))
        
        db.session.commit()
        flash("Kategori eklendi!", "success")
        return redirect(url_for("admin.manage_categories"))
            
    return render_template("admin/add_ct.html")


@admin_bp.route("/admin/kategori_sil/<int:ct_id>")
@login_required
@role_required(UserRole.ADMIN)
def remove_ct(ct_id):
    ct = Category.query.get(ct_id)
    db.session.delete(ct)
    db.session.commit()
    flash("Kategori kaldırıldı.", "success")
    return redirect(url_for("admin.manage_categories"))


@admin_bp.route("/admin/duyuru_ekle", methods=["GET", "POST"])
@login_required
@role_required(UserRole.ADMIN)
def make_announcement():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image = request.files.get("image")

        new_announcement = Announcement(title=title, content=content, admin_id=current_user.id)
        db.session.add(new_announcement)
        db.session.commit()

        if image:
            filename = secure_filename(image.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            if extension in ALLOWED_IMG_EXTENSIONS:
                image_path = os.path.join(f"images/announcements/{new_announcement.id}.{extension}")
                image.save(os.path.join("app/static/", image_path))
                new_announcement.image = image_path
                db.session.commit()
            else:
                flash("Geçersiz resim formatı.", "error")
                return redirect(url_for("admin.make_announcement"))
            
        flash("Duyuru başarıyla oluşturuldu.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/make_announcement.html")
