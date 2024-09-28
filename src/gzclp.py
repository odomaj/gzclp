import toml
from get_file import get_file

TOML_FILE_PATH = "../config/schedule.toml"

if __name__ == "__main__":
    with get_file(TOML_FILE_PATH).open("r") as file:
        config = toml.load(file)
    print(config)
