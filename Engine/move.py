import json
from enum import Enum
import requests


class MoveCategory(Enum):
    PHYSICAL = "physical"
    SPECIAL = "special"
    STATUS = "status"


class Move:
    def __init__(self, name: str, pp: str, is_disabled: bool, move_type=None, power=None, accuracy=None, priority=None,
                 category=None):
        self.name = name
        self.pp = pp
        self.disabled = is_disabled
        self.url = "https://pokeapi.co/api/v2/move/" + self.name.lower().replace(" ", "-")

        if move_type is None and power is None and accuracy is None and priority is None and category is None:
            self.fill_data_fields()
        else:
            self.type = move_type
            self.power = power
            self.accu = accuracy
            self.priority = priority
            self.move_category = category

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
        self.set_move_category(response.get("damage_class", {}).get("name"))

    def set_move_category(self, category_name: str):  # TODO: add test
        if category_name == "physical":
            self.move_category = MoveCategory.PHYSICAL
        elif category_name == "special":
            self.move_category = MoveCategory.SPECIAL
        elif category_name == "status":
            self.move_category = MoveCategory.STATUS
        else:
            raise ValueError(f'The move {self.name} does not have a legal category')

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
