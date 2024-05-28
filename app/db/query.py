from app.db.model import *


class Query:
    # ----- ALL -----
    @staticmethod
    def db_commit():
        db.session.commit()

    # ----- TIME_OPEN -----
    @staticmethod
    def get_open_current(week_day_abbrev, hour_minutes):
        open_current = (
            TimeOpen.query
            .join(WeekDay, TimeOpen.week_day_id == WeekDay.week_day_id)
            .filter_by(day_abbreviation=week_day_abbrev)
            .filter(TimeOpen.time_start <= hour_minutes, TimeOpen.time_end >= hour_minutes)
            .first()
        )

        return open_current

    @staticmethod
    def get_open_next_today(week_day_abbrev, hour_minutes):
        open_next = (
            TimeOpen.query
            .join(WeekDay, TimeOpen.week_day_id == WeekDay.week_day_id)
            .filter_by(day_abbreviation=week_day_abbrev)
            .filter(TimeOpen.time_start > hour_minutes)
            .order_by(TimeOpen.time_start)
            .first()
        )

        return open_next

    @staticmethod
    def get_open_next_day(week_day_abbrev):
        open_next = (
            TimeOpen.query
            .join(WeekDay, TimeOpen.week_day_id == WeekDay.week_day_id)
            .filter_by(day_abbreviation=week_day_abbrev)
            .order_by(TimeOpen.time_start)
            .first()
        )

        return open_next

    @staticmethod
    def post_event(dict_event):
        event = TimeOpen(**dict_event)

        db.session.add(event)
        db.session.commit()

    @staticmethod
    def delete_event(event):
        db.session.delete(event)

        db.session.commit()
