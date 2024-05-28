import sqlite3
import inquirer

from app.config import db_path


class SQLITEInteract:

    def __init__(self):
        """
        Setup connection to SQLite file.
        """
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        # Entries of openings in DB as list of dict
        self.db_data_open = []

        # SQL request here since it should only append once for this table (week_day)
        db_entries_weekday = self.cur.execute(
            "SELECT * "
            "FROM week_day "
            "ORDER BY week_day_id"
        ).fetchall()

        # Transform DB data into dict format
        self.db_data_weekday = [dict(row) for row in db_entries_weekday]

    def __exit__(self):
        """
        Close connection to SQLite file once done.
        """
        self.con.close()

    def get_data_db(self):
        """
        Fetch entries in table time_open with only relevant data from DB.

        :return: Dict
        """
        db_entries = self.cur.execute(
            "SELECT * "
            "FROM time_open tTO "
            "INNER JOIN week_day tWD ON tTO.week_day_id = tWD.week_day_id "
            "ORDER BY tWD.week_day_id, tTO.time_start"
        ).fetchall()

        # Transform DB data into dict format
        self.db_data_open = [dict(row) for row in db_entries]

    def __weekday_to_id(self, weekday):
        """
        Get the matching id of the weekday based the given the weekday abbreviation.

        :param weekday: str
        :return: int
        """
        week_day_id = 0

        # Fetch the id matching the given weekday abbreviation
        for db_entry_day in self.db_data_weekday:
            if db_entry_day["day_abbreviation"] == weekday:
                week_day_id = db_entry_day["week_day_id"]
                break

        return week_day_id

    # Using snake case since it's the naming convention for python. Also changed a bit from instructions since
    # there is another function that takes care of removing hours. Made it so since it's clean in our case.
    def set_opening_hours(self, weekday, time_start, time_end):
        """
        Add entry into DB at table time_open.

        :param weekday: str
        :param time_start: str
        :param time_end: str
        """
        # Add new entry into db
        self.cur.execute(
            "INSERT INTO time_open (week_day_id, time_start, time_end) "
            "VALUES ({0}, '{1}', '{2}')"
            .format(self.__weekday_to_id(weekday), time_start, time_end)
        )
        self.con.commit()

    def remove_opening_hours(self, weekday, time_start, time_end):
        """
        Remove from DB entry in table open_time where all parameters match.

        :param weekday: str
        :param time_start: str
        :param time_end: str
        :return:
        """
        # Remove new entry into db
        self.cur.execute(
            "DELETE "
            "FROM time_open "
            "WHERE week_day_id={0} AND time_start='{1}' AND time_end='{2}'"
            .format(self.__weekday_to_id(weekday), time_start, time_end)
        )
        self.con.commit()


# Just here to be reused
def list_text_data_db(db_data_open):
    list_text_choice = []
    # To have list of element in this format (Mon: 08:00-08:00)
    for dict_entry in db_data_open:
        list_text_choice.append(
            dict_entry["day_abbreviation"] +
            ": " +
            dict_entry["time_start"] +
            "-" +
            dict_entry["time_end"]
        )

    return list_text_choice


# Check that format time is always something like 00:00
def check_time_format(str_time):
    valid_time = True

    # If there is an error than user put time wrong
    try:
        # Making it five to avoid possible trouble with main app
        assert len(str_time) == 5

        hour, minute = str_time.split(":")

        assert 0 <= int(hour) < 24
        assert 0 <= int(minute) < 60

    except Exception as e:
        valid_time = False

    return valid_time


# Execute this from console not from the IDE. Inquirer doesn't support IDE consoles
# Script and stuff is seperated from the rest of the project to isolate it a maximum
if __name__ == "__main__":
    db_control = SQLITEInteract()

    # Will loop until Exit is chosen
    while True:
        db_control.get_data_db()

        action_choice = ['Show', 'Add', 'Exit']
        # Put Delete option in list if there is any entry in table time_open of DB
        if db_control.db_data_open:
            action_choice = ['Show', 'Add', 'Delete', 'Exit']

        chosen_action = inquirer.list_input("Selected desired action", choices=action_choice)

        if chosen_action == "Show":
            list_text_choice = []
            # To have list of element in this format (Mon: 08:00-08:00)
            for dict_entry in db_control.db_data_open:
                list_text_choice.append(
                    dict_entry["day_abbreviation"] +
                    ": " +
                    dict_entry["time_start"] +
                    "-" +
                    dict_entry["time_end"]
                )

            print("\nCurrent entries in the DB:\n")
            [print(element) for element in list_text_choice]
            print("\n\n")

        elif chosen_action == "Add":
            weekday_choice = [key["day_abbreviation"] for key in db_control.db_data_weekday]

            chosen_weekday = inquirer.list_input("Selected desired weekday", choices=weekday_choice)

            # Loop until correctly start_time < end_time
            while True:
                # Loop until correctly writing time
                while True:
                    start_time = inquirer.text(message="Enter start time (exemple: 07:23)")
                    # If start_time is valid then continue to next stage
                    if check_time_format(start_time):
                        break
                    else:
                        print("\nPlease verify that starting time is valid and in range (00:00-24:00)")

                # Loop until correctly writing time
                while True:
                    end_time = inquirer.text(message="Enter end time (exemple: 19:54)")
                    # If end_time is valid then continue to next stage
                    if check_time_format(end_time):
                        break
                    else:
                        print("\nPlease verify that ending time is valid and in range (00:00-24:00)")

                if start_time < end_time:
                    break
                else:
                    print("\nStarting time must be before ending time!")

            db_control.set_opening_hours(chosen_weekday, start_time, end_time)

            print("\nEntry '{}' was added to the DB.\n\n".format(chosen_weekday + ": " + start_time + "-" + end_time))

        elif chosen_action == "Delete":
            chosen_deletion = inquirer.list_input(
                "Selected entry to delete",
                choices=list_text_data_db(db_control.db_data_open)
            )

            # Extract data from the string
            day = chosen_deletion.split(":", 1)[0]
            start = chosen_deletion.split(" ")[-1].split("-")[0]
            end = chosen_deletion.split(" ")[-1].split("-")[-1]

            db_control.remove_opening_hours(day, start, end)

            print("Entry '{}' was removed from the DB.\n\n".format(day + ": " + start + "-" + end))

        elif chosen_action == "Exit":
            break
