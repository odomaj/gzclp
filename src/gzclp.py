import toml
import sys
from get_file import get_file
from history import Database
from proto.workout_pb2 import Set, Exercise, Workout


TOML_FILE_PATH = "../config/schedule.toml"
UNITS = "lbs"


def pounds_to_kilos(pounds: int) -> int:
    return int(pounds / 2.2)


def kilos_to_pounds(kilos: int) -> int:
    return int(kilos * 2.2)


class Gzclp:
    def __init__(self, config: dict) -> None:
        self.history = Database()
        self.lower = []
        self.upper = []
        for workout in config:
            self.add_workout(workout, config)
        if not self.validate():
            print("[WARNING] error occured when parsing config")

    def add_workout(self, workout: str, config: dict) -> None:
        split = self.upper_lower(workout)
        index = self.workout_number(workout) - 1
        if split == "":
            print(
                f"[WARNING] config has entry [{workout}]\n entries should be"
                " labeled as [Upper] or [Lower] followed by a number\n ex."
                " [Upper1]"
            )
        elif split == "upper":
            self.resize_list(self.upper, index + 1)
            if self.upper[index] is not None:
                print(f"[WARNING] multiple [Upper{index+1}] entries")
            self.upper[index] = self.workout_from_config(
                config[workout], f"u{index+1}"
            )
        elif split == "lower":
            self.resize_list(self.lower, index + 1)
            if self.lower[index] is not None:
                print(f"[WARNING] multiple [Lower{index+1}] entries")
            self.lower[index] = self.workout_from_config(
                config[workout], f"l{index+1}"
            )
        else:
            print(
                "[ERROR] unexpected output from Gzclp.upper_lower with"
                f' input "{workout}"'
            )

    def upper_lower(self, key: str) -> str:
        if len(key) < 5:
            return ""
        if key[:5] == "Upper":
            return "upper"
        if key[:5] == "Lower":
            return "lower"

    def workout_number(self, key: str) -> int:
        if len(key) < 6:
            return 0
        return int(key[5:])

    def resize_list(self, list_: list, length: int) -> None:
        while len(list_) < length:
            list_.append(None)

    def validate(self) -> bool:
        for workout in self.lower:
            if workout is None:
                return False
        for workout in self.upper:
            if workout is None:
                return False
        return True

    def workout_from_config(
        self, workout_config: dict, split_id: str
    ) -> Workout:
        workout = Workout()
        workout.split_id = split_id
        exercise = Exercise()
        exercise.name = workout_config["T1"]
        exercise.priority = 1
        workout.exercise.append(exercise)

        exercise.priority = 2
        for exercise_name in workout_config["T2"]:
            exercise.name = exercise_name
            workout.exercise.append(exercise)

        exercise.priority = 3
        for exercise_name in workout_config["T3"]:
            exercise.name = exercise_name
            workout.exercise.append(exercise)

        return workout

    def setup(self) -> None:
        pass

    def same_exercise(
        self, first_exercise: Exercise, second_exercise: Exercise
    ) -> bool:
        if first_exercise.name != second_exercise.name:
            return False
        if first_exercise.priority != second_exercise.priority:
            return False
        if first_exercise.split != second_exercise.split:
            return False
        return True

    def same_workout(
        self, first_workout: Workout, second_workout: Workout
    ) -> bool:
        if first_workout.split_id != second_workout.split_id:
            return False
        if len(first_workout.exercise) != len(second_workout.exercise):
            return False
        for i in range(len(first_workout.exercise)):
            if self.same_exercise(
                first_workout.exercise[i], second_workout.exercise[i]
            ):
                return False
        return True

    def update_exercise(self, exercise: Exercise) -> Exercise:
        new_exercise = Exercise()
        return new_exercise

    def fill_workout(self, workout: Workout) -> Workout:
        last_workout = self.history.last_workout(workout.split_id)
        if not self.same_workout(workout, last_workout):
            return None
        for i in range(len(workout.exercise)):
            workout.exercise[i] = self.update_exercise(
                last_workout.exercise[i]
            )
        return workout


if __name__ == "__main__":
    if UNITS != "lbs" and UNITS != "kgs":
        print("[ERROR] units must be lbs or kgs")
        sys.exit()
    with get_file(TOML_FILE_PATH).open("r") as file:
        gzclp = Gzclp(toml.load(file))
