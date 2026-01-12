from flask import render_template
from flask_login import current_user
from app.routes import categories_bp
from app.models import Category

@categories_bp.route("/kategoriler/<int:ct_id>")
def ct_detail(ct_id):
    category = Category.query.get_or_404(ct_id)
    return render_template("categories/ct_detail.html", ct=category)

@categories_bp.route("/sartname_indir/<int:ct_id>")
def download_ct_guide(ct_id):
    category = Category.query.get_or_404(ct_id)
    guide = category.guide
    return "Hazır değil."
