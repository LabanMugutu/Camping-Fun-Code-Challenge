from . import db

class Camper(db.Model):
    __tablename__ = "campers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # relationship to signups
    signups = db.relationship("Signup", back_populates="camper", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age}

    def to_dict_with_signups(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "signups": [s.to_dict_nested_activity() for s in self.signups]
        }


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    # cascade deletes of signups when an activity is deleted
    signups = db.relationship(
        "Signup",
        back_populates="activity",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "difficulty": self.difficulty}


class Signup(db.Model):
    __tablename__ = "signups"

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id", ondelete="CASCADE"), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    time = db.Column(db.Integer, nullable=False)  # hour 0-23

    camper = db.relationship("Camper", back_populates="signups")
    activity = db.relationship("Activity", back_populates="signups")

    def to_dict(self):
        return {
            "id": self.id,
            "camper_id": self.camper_id,
            "activity_id": self.activity_id,
            "time": self.time,
            "activity": self.activity.to_dict() if self.activity else None,
            "camper": self.camper.to_dict() if self.camper else None
        }

    def to_dict_nested_activity(self):
        # used for GET /campers/<id> signups with nested activity
        return {
            "id": self.id,
            "camper_id": self.camper_id,
            "activity_id": self.activity_id,
            "time": self.time,
            "activity": self.activity.to_dict() if self.activity else None
        }
