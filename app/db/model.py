from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Could have skipped this table since I realized an alternative but at this point the code works so will just keep it
class WeekDay(db.Model):
    __tablename__ = 'week_day'

    week_day_id = db.Column(db.Integer, primary_key=True)
    day_abbreviation = db.Column(db.String(3), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TimeOpen(db.Model):
    __tablename__ = 'time_open'

    time_open_id = db.Column(db.Integer, primary_key=True)
    week_day_id = db.Column(db.Integer, db.ForeignKey("week_day.week_day_id"), nullable=False)
    week_day = db.relationship("WeekDay")
    # Using string since SQLite doesn't support datetime types
    time_start = db.Column(db.String(5), nullable=False)
    time_end = db.Column(db.String(5), nullable=False)

    def as_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['week_day'] = self.week_day.as_dict()
        return d
