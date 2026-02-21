import json


def save_exchange_state(state, filepath):
    with open(filepath, "w") as file:
        json.dump(state, file, indent=2)


def load_exchange_state(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


# states should only have
# dict/list/str/int/float/bool/None
