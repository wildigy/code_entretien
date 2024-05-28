from flask import render_template, make_response
from datetime import datetime, timedelta

from app.db.query import Query


class TimeOpenController:
    # Need this to avoid accidents with localization of date. Decided it made more sense here than in DB.
    # Just realized way later near finishing my code i could have juste avoid my problem and the need to do this
    # by using isoweekday() instead of weekday() on the datetime.now(). Keeping as it now since it works
    dict_link_week_day = {
        0: "Lun",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun"
    }

    def __init__(self):
        pass

    # Using snake case since it's the naming convention for python
    def is_open_on(self, moment):
        """
        Check if there is an entry in the DB matching the day of the week with the current hours and minutes between
        time start and end. All based of the given moment parameter.

        :param moment: Datetime
        :return: Boolean
        """
        # Fetch the first matching entry in table time_open based on current moment if there is one else will be None
        current_opening = Query.get_open_current(self.dict_link_week_day[moment.weekday()], moment.strftime("%H:%M"))

        return bool(current_opening)

    # Using snake case since it's the naming convention for python
    def next_opening_date(self, moment):
        """
        Get the next entry in DB based on day of the week and the time if there is one.
        All based of the given moment parameter.

        :param moment: Datetime
        :return: Datetime or None
        """
        next_opening_datetime = None

        # Need to for index() use list() not keys(). In this case taking directly moment.weekday() value also work
        # list(self.dict_link_week_day).index(moment.weekday())

        # Split the dict into two seperated based on the index of before and after of the weekday of today
        dict_first_part = {key: value for key, value in self.dict_link_week_day.items() if key >= moment.weekday()}
        dict_sec_part = {key: value for key, value in self.dict_link_week_day.items() if key < moment.weekday()}

        # Order the dict into one starting with current day for weekday
        dict_weekday_reordered = dict_first_part | dict_sec_part

        for index_position, weekday in enumerate(dict_weekday_reordered.values()):
            # Need to separate into two different Query because of specific possibility where time_start is 00:00
            if index_position:
                # Fetch the first matching entry in time_open table based on weekday start without the time
                next_time_open = Query.get_open_next_day(weekday)
            else:
                # Fetch the first next entry in time_open table based on current date and time of today
                next_time_open = Query.get_open_next_today(weekday, moment.strftime("%H:%M"))

            # Will stay None if there is nothing in the time_open table
            if next_time_open:
                # Get the next date matching the weekday
                next_datetime_raw = moment + timedelta(days=index_position)
                # Extract time details
                hour, minute = next_time_open.time_start.split(":")
                # Remove left over details from parameter moment
                next_opening_datetime = next_datetime_raw.replace(
                    hour=int(hour),
                    minute=int(minute),
                    second=0,
                    microsecond=0
                )

                break

        return next_opening_datetime

    def get_open_currently(self):
        '''
        Check if current opening in DB and return html page with info for if open currently

        :return: Html page
        '''
        current_status_text = "Currently Closed!"

        open_currently = self.is_open_on(datetime.now())

        if open_currently:
            current_status_text = "Currently Open!"

        # Create html page. Normally for a real frontend we create a seperated project and use a framework
        page = make_response(render_template(
            "open_info/open_info.html",
            headers={'Content-Type': 'text/html'},
            titleText="Store Status:",
            wantedInfo=current_status_text
        ))

        return page

    def get_open_next(self):
        '''
        Fetch next opening in DB and return html page with info for next opening

        :return: Html page
        '''
        # Will only show Never if nothing in DB for the time_open table
        next_opening_text = "Never"

        next_opening = self.next_opening_date(datetime.now())

        if next_opening:
            # Can also directly use str() in for this format
            next_opening_text = next_opening.strftime("%d/%m/%y %H:%M:%S")

        # Create html page. Normally for a real frontend we create a seperated project and use a framework
        page = make_response(render_template(
            "open_info/open_info.html",
            headers={'Content-Type': 'text/html'},
            titleText="Next Opening:",
            wantedInfo=next_opening_text
        ))

        return page
