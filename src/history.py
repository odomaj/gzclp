import sqlite3 as sql
from base64 import b64encode, b64decode
from proto.workout_pb2 import Workout


MAX_PROTOBUF_LENGTH = 511


class Database:
    def __init__(self) -> None:
        self.connection = sql.connect("../data/workout_history.db")
        cursor = self.connection.cursor()
        table = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'AND"
            " name='HISTORY';"
        ).fetchall()
        if table == []:
            cursor.execute(
                "CREATE TABLE HISTORY(YEAR int, MONTH int, DAY int, SPLIT_ID"
                f" CHAR(2), WORKOUT VARCHAR({MAX_PROTOBUF_LENGTH}));"
            )

    def __del__(self) -> None:
        self.connection.close()

    def save_workout(self, workout: Workout) -> None:
        cursor = self.connection.cursor()
        encoded_workout = b64encode(workout.SerializeToString()).decode()
        cursor.execute(
            "INSERT INTO HISTORY(YEAR, MONTH, DAY, SPLIT_ID, WORKOUT)"
            f" VALUES({workout.year}, {workout.month}, {workout.day},"
            f" '{workout.split_id}',"
            f" '{encoded_workout}')"
        )
        self.connection.commit()

    def last_workout(self, split_id: str) -> Workout:
        cursor = self.connection.cursor()
        history = list(
            cursor.execute(
                "SELECT YEAR, MONTH, DAY, WORKOUT FROM HISTORY WHERE SPLIT_ID"
                f" = '{split_id}'"
            )
        )
        if len(history) == 0:
            return None
        latest_workout = history[0]
        # get the workout with the largest date (YEAR, MONTH, DAY)
        for workout in history[1:]:
            if workout[0] > latest_workout[0]:
                latest_workout = workout
            elif workout[0] == latest_workout[0]:
                if workout[1] > latest_workout[1]:
                    latest_workout = workout
                elif workout[1] == latest_workout[1]:
                    if workout[2] > latest_workout[2]:
                        latest_workout = workout
        # deserialize the saved protobuf string and output the result
        encoded_workout = b64decode(latest_workout[3].encode())
        output = Workout()
        output.ParseFromString(encoded_workout)
        return output
