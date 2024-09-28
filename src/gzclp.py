import toml
import sys
from get_file import get_file
from proto.workout_pb2 import Set, Exercise, Workout


TOML_FILE_PATH = "../config/schedule.toml"
UNITS = "lbs"


def pounds_to_kilos(pounds: int) -> int:
    return int(pounds / 2.2)


def kilos_to_pounds(kilos: int) -> int:
    return int(kilos * 2.2)


class Gzclp:
    def __init__(self, config: dict) -> None:
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
        workout.exercises.append(exercise)

        exercise.priority = 2
        for exercise_name in workout_config["T2"]:
            exercise.name = exercise_name
            workout.exercises.append(exercise)

        exercise.priority = 3
        for exercise_name in workout_config["T3"]:
            exercise.name = exercise_name
            workout.exercises.append(exercise)

        return workout


if __name__ == "__main__":
    if UNITS != "lbs" and UNITS != "kgs":
        print("[ERROR] units must be lbs or kgs")
        sys.exit()
    with get_file(TOML_FILE_PATH).open("r") as file:
        gzclp = Gzclp(toml.load(file))
