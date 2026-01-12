from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.routes import profiles_bp
from app.models import User
from config import ALLOWED_IMG_EXTENSIONS
from app import db
import os

@profiles_bp.route("/profil/<int:user_id>")
def profile_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("profiles/profile_detail.html", user=user)

@profiles_bp.route("/profili_duzenle", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        pfp = request.files.get("pfp")
        bio = request.form.get("bio")

        if bio:
            current_user.bio = bio
            db.session.commit()

        if pfp:
            extension = pfp.filename.rsplit(".", 1)[1].lower()
            if not extension in ALLOWED_IMG_EXTENSIONS:
                flash("Resminizin uzantısı desteklenmiyor.", "error")
                return redirect(url_for("profiles.edit_profile"))
            
            if current_user.pfp != "web/defaultpfp.jpg":
                os.remove(f"app/static/{current_user.pfp}")

            current_user.pfp = f"images/pfps/{current_user.id}.{extension}"
            pfp.save(os.path.join(f"app/static/{current_user.pfp}"))
            db.session.commit()

        flash("Düzenlemeler kaydedildi!", "success")
        return redirect(url_for("profiles.profile_detail", user_id=current_user.id))
    return render_template("profiles/edit_profile.html")
