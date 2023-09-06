import json
import requests


class Move:
    def __init__(self, name: str, pp: str, is_disabled: bool):
        self.name = name
        self.pp = pp
        self.disabled = is_disabled
        self.url = "https://pokeapi.co/api/v2/" + "move/" + self.name.lower().replace(" ", "-")  # Shadow Sneak -> shadow-sneak
        # Data:
        self.type = None
        self.power = None
        self.accu = None
        self.priority = None
        self.fill_data_fields()

    def fill_data_fields(self):
        response = requests.get(self.url).json()
        self.type = response.get("type", {}).get("name")
        power = response.get("power")
        if power is None:
            self.power = 0
        else:
            self.power = int(power)
        accu = response.get("accuracy")
        if accu is None:
            self.accu = 100.0
        else:
            self.accu = float(accu) / 100.0
        self.priority = int(response.get("priority"))

    def is_move_disabled(self):
        return self.disabled

    def disable_move(self):
        self.disabled = True

    def enable_move(self):
        self.disabled = False

    def is_possible(self):
        print("1: ", self.disabled is False, "/", 0 < int(self.pp))
        return (self.disabled is False) and (0 < int(self.pp))


def create_active_moves_list(json_data) -> list[Move]:
    data = json.loads(json_data.replace("|request|", ""))

    # Extract the "active" section from the JSON data
    active_section = data.get("active", [])
    active_moves_list = []

    # Iterate through the known_moves in the "active" section
    for move_data in active_section[0].get("moves", [])[:4]:
        move_name = move_data.get("move", '')
        move_pp = move_data.get("pp", 0)
        move_disabled = move_data.get("disabled", False)

        # Create a Move object and add it to the list
        move = Move(move_name, move_pp, move_disabled)
        active_moves_list.append(move)

    if len(active_moves_list) == 0:
        raise RuntimeError("Couldn't upload the moves of the active pokemon")

    return active_moves_list


def create_move(move_name: str) -> Move:
    """Uses for enemy's known_moves"""
    move = Move(move_name, "30", False)  # 30 - a temp number till I find if extracting it is possible
    # move.pp -= 1
    return move
