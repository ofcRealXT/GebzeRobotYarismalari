from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum
from app import db

class UserRole(Enum):
    ADMIN = "admin"
    PARTICIPANT = "participant"
    MENTOR = "mentor"
    USER = "user"

class TeamRole(Enum):
    CAPTAIN = "Kaptan"
    MENTOR = "Danışman"
    MEMBER = "Üye"

class EducationLevel(Enum):
    PRIMARY = "İlkokul"
    SECONDARY = "Ortaokul"
    HIGHSCHOOL = "Lise"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    pfp = db.Column(db.String(500), default="web/defaultpfp.jpg")
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER)
    bio = db.Column(db.String(500), nullable=True)
    school = db.Column(db.String(100), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.Integer, nullable=True)
    code_expiry = db.Column(db.DateTime, nullable=True)
    is_banned = db.Column(db.Boolean, default=False)
    banned_at = db.Column(db.DateTime, nullable=True)
    ban_note = db.Column(db.String(500), nullable=True)
    banned_until = db.Column(db.DateTime, nullable=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    team = db.relationship("Team", foreign_keys=[team_id], backref=db.backref("team_members_direct", lazy='dynamic'))

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)

    def check_password(self, target_password):
        return check_password_hash(self.password, target_password)
    
    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)
    banner = db.Column(db.String(100), default="web/wwp1.png")
    guide = db.Column(db.String(100), default="docs/ornekSartname.pdf")


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    edc_level = db.Column(db.Enum(EducationLevel), nullable=False)
    full_school = db.Column(db.String(150), nullable=True)
    captain_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    captain = db.relationship(
        "User",
        foreign_keys=[captain_id],
        backref=db.backref("teams_captained", lazy='dynamic')
    )
    mentor = db.relationship(
        "User",
        foreign_keys=[mentor_id],
        backref=db.backref("teams_mentored", lazy='dynamic')
    )
    members = db.relationship(
        "TeamMember",
        backref="team",
        cascade="all, delete-orphan"
    )
    applications = db.relationship(
        "Application",
        back_populates="team",
        cascade="all, delete-orphan"
    )


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    role = db.Column(db.Enum(TeamRole), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="team_memberships")


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(50), default="pending")
    submitted_at = db.Column(db.DateTime, nullable=False)

    team = db.relationship("Team", back_populates="applications")


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(800), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship("User")
