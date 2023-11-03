# ShowdownBot

###### (This project is a work in progress and may contain known bugs; additional features and improvements are planned for future updates)

ShowdownBot is a Python-based bot, designed to enhance your Pokemon battles within the [Showdown](https://play.pokemonshowdown.com/) platform. This versatile tool efficiently utilizes Showdown's protocol to access crucial information and execute precise commands, providing a strategic edge in every battle. Behind the scenes, ShowdownBot boasts a sophisticated engine that facilitates intricate calculations and utilities, empowering each bot with enhanced strategic capabilities. Its modular design invites users to inherit from the abstract "BattleBot" class and implement the "make_action()" method, offering a customizable experience for all.

Beyond its impressive features, ShowdownBot underscores the significance of strong Object-Oriented Programming (OOP) principles, ensuring reliability and extensibility. Furthermore, it seamlessly integrates with APIs to provide access to crucial Pokémon data, enriching your decision-making process. Whether you are a seasoned programmer or a newcomer to Pokémon battles, ShowdownBot's user-friendly and modular approach ensures accessibility. Harness the power of OOP and gain insights from Pokémon data through APIs with ShowdownBot, fostering a professional and efficient approach to strategic battles.

### Current Features
* **Modular Design:** ShowdownBot is built with modularity in mind, making it easy to create custom bots with different behaviors.
* **RandomBot**: Includes a sample bot called "RandomBot" that makes random battle decisions.
* **GreedyBot**: Includes a sample bot called "GreedyBot" that uses utility calculations to make strategic battle decisions.

---

## Installation, usage and technical details

### Dependencies
1. Python 3.x
2. Other dependencies are listed in the requirements.txt file.
3. Two Showdown user accounts

### Installation
1. Clone this repository to your local machine.

`git clone https://github.com/AlonMesh/ShowdownBot.git`

2. Install the required dependencies by running:

`pip install -r requirements.txt`

### Usage
To test ShowdownBot, follow these steps:

1. **Set Up Showdown Accounts:** Begin by creating two Showdown accounts - one for the bot and one for yourself. You will need to insert the bot account's username and password into the `config.ini` file, as well as specifying your username (under the "player" section). Ensure that all fields in the `config.ini` file are properly filled.

2. **Configure Bot Mode:** In the `config.ini` file, you shall specify the BOT_MODE setting as "accept". This mode is required for testing.

3. **Prepare Showdown Sessions:** Open two separate browser windows or use incognito mode to log in to both Showdown accounts.

4. **Initiate a Challenge:** From your player account, challenge the bot by typing `/challenge <bot_username>, <battle_format>`. Replace `<bot_username>` with the bot's username and `<battle_format>` with your desired battle format.

5. **Run ShowdownBot:** Launch ShowdownBot, which will automatically accept the challenge from your player account. Enjoy the show!

By following these steps, you can effectively test and interact with ShowdownBot within the Showdown environment, ensuring a smooth and engaging experience.

| Config |  Explain  | Type |
|:-----|:--------:|------:|
| USERNAME | The username of the user controlled by the bot | String |
| PASSWORD |  The password of the user controlled by the bot  | String |
| PLAYER | The username of the player will stand against the bot | String |
| URI | URI of showdown protocol | String |
| BOT_MODE | How to start a battle - `accept`, `search` or `challenge` | String |
| BOT_TYPE | Which bot will be selected - `greedy` or `random` | String |
| BATTLE_FORMAT | Format of the battle - Only `gen9randombattle` | String |
| RUN_X_TIMES | How many battles the bot will run before its shut down | int |



### How it Works
1. **Establishing Communication:** The system begins by creating a socket connection between the program and the Showdown protocol. This connection serves as the bridge for all communication with the Showdown server.
2. **Message Handling:** Incoming messages from Showdown are processed by the `handle_showdown_messages(...)` function. Additionally, a dedicated tool, known as the `Sender`, is used to send messages and commands back to Showdown.
3. **Command-Based Processing:** Each message received from Showdown includes a `battle_ID` and a corresponding `command` and `context`. The `communication_manager.py` module is responsible for interpreting these commands and applying the appropriate functionality based on the context provided.
4. **Bot Interaction:** The program utilizes the abstract base class `BattleBot` and its derived classes to relay information to the bot and instruct it to execute the requested moves during battles.
5. **Leveraging the Engine:** The bots rely on the classes within the `Engine` folder, which facilitate battle order determination, expand data through API usage, and enable complex functionality within the battles.

---

### License
This project is licensed under the MIT License - see the LICENSE file for details.