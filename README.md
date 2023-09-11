## ShowdownBot

###### (This project is a work in progress and may contain known bugs; additional features and improvements are planned for future updates)

ShowdownBot is a Python-based bot designed to play Pokemon battles in [Showdown](https://play.pokemonshowdown.com/). This project allows you to create and customize bots that can autonomously participate in Showdown battles.

### Features
* **Modular Design:** ShowdownBot is built with modularity in mind, making it easy to create custom bots with different behaviors.
* **RandomBot**: Includes a sample bot called "RandomBot" that makes random battle decisions.
* **GreedyBot**: Includes a sample bot called "GreedyBot" that uses utility calculations to make strategic battle decisions.

### Installation
1. Clone this repository to your local machine.

`git clone https://github.com/AlonMesh/ShowdownBot.git`

2. Install the required dependencies by running:

`pip install -r requirements.txt`

### Usage
To use ShowdownBot, follow these steps:

1. Configure the bot's behavior by creating your custom bot class, inheriting from `BattleBot` and implementing the `make_action` method.
2. Update the bot's logic in your custom bot class to make decisions during battles.
3. Run the bot by initiating a battle on Showdown and providing the battle information to your bot.

### How it Works
1. **Establishing Communication:** The system begins by creating a socket connection between the program and the Showdown protocol. This connection serves as the bridge for all communication with the Showdown server.
2. **Message Handling:** Incoming messages from Showdown are processed by the `handle_showdown_messages(...)` function. Additionally, a dedicated tool, known as the `Sender`, is used to send messages and commands back to Showdown.
3. **Command-Based Processing:** Each message received from Showdown includes a `battle_ID` and a corresponding `command` and `context`. The `communication_manager.py` module is responsible for interpreting these commands and applying the appropriate functionality based on the context provided.
4. **Bot Interaction:** The program utilizes the abstract base class `BattleBot` and its derived classes to relay information to the bot and instruct it to execute the requested moves during battles.
5. **Leveraging the Engine:** The bots rely on the classes within the `Engine` folder, which facilitate battle order determination, expand data through API usage, and enable complex functionality within the battles.

### Directory Structure
The project directory structure is organized as follows:
```
ShowdownBot/
│
├── BattleBots/
│   ├── battle_bot.py
│   ├── random_bot.py
│   └── greedy_bot.py
│
├── Engine/
│   ├── move.py
│   ├── pokemon.py
│   ├── team.py
│   ├── type.py
│   └── utility_calculator.py
│
├── web_socket/
│   ├── main.py
│   └── ... (other relevant files)
│
├── requirements.txt
├── config.ini
└── README.md
```
### Dependencies
1. Python 3.x
2. Other dependencies are listed in the requirements.txt file.

### Contributing
Contributions to ShowdownBot are welcome! If you have improvements or new features to propose, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them thoroughly.
4. Submit a pull request to the main repository.

### License
This project is licensed under the MIT License - see the LICENSE file for details.