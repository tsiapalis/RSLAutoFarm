# Raid: Shadow Legends Automated Farming Script
This Python script automates the farming process for level up in the game *"Raid: Shadow Legends"*. 

It interacts with the game window, simulates mouse clicks, and manages pre-made teams to optimize farming efficiency.

## Features
- Automates repetitive farming tasks
- Manages multiple teams and switches between them
- Customizable farming difficulty
- Adjustable run times

## Requirements

### For Executable
- Windows OS
### For Script
- Python 3.11.4
- ***pyautogui*** library
- ***pygetwindow*** library

## Installation

### Using the Executable
1) Download the executable from here.

2) Run the executable:
   - Double-click the *RSLAutoFarm.exe* file to start the program.
   - Follow the on-screen prompts to configure your farming setup.

### Using the Python Script
1) **Clone the repository:**
    ```console
    git clone https://github.com/tsiapalis/RSLAutoFarm.git
    cd RSLAutoFarm
    ```
2) **Install the required libraries:**
   ```console
   pip install pyautogui pygetwindow
   ```
3) **Run the script:**
    ```console
    python RSLAutoFarm.py
    ```

4) **Follow the prompts** to configure your farming setup.

### Usage
1) Open *Raid: Shadow Legends* app from the official Plarium client.

2) Start the program:
   - If using the executable, double-click the *RSLAutoFarm.exe* file.
   - If using the Python script, run python *RSLAutoFarm.py* in your terminal.
    
3) Follow the prompts to configure your farming setup:
   -  Number of teams
   -  Farming difficulty
   -  XP boost status
   -  Average farming time

4) **The script will start farming**, switching teams as necessary until the maximum level is achieved for all specified teams.

## Configuration
Button positions and other configurations are currently hardcoded in the script. You can modify these values in the button_pos dictionary and other relevant sections of the script if needed.

### Example
Here’s a quick example of the prompts you might encounter when running the script:
```console
How many teams will farm? 3
At what difficulty do you farm? [Normal(1), Hard(2), Brutal(3)]: 3
Do you have an active XP BOOST? (Y/N): Y
How long does it take you to clear the stage? (enter time in MM:SS format): 02:30
How many champions does your team 1 have and what is their rank? 3x1
How many champions does your team 2 have and what is their rank? 3x3
How many champions does your team 3 have and what is their rank? 2x1
You have 3 seconds to open the RSL window.
3
2
1
```

## Functions Overview
### In Use
- **WindowDimensions(window_title)** : Sets the game window dimensions and positions it on the screen.
- **UserInput()** : Collects and returns user input functions for farming setup.
  - **Teams(prompt)** : Gets the number of farming teams.
  - **StageDifficulty(prompt)** : Gets the farming stage difficulty.
  - **XpBoost(prompt)** : Gets if there is an active XP boost.
  - **FarmingTime(prompt)** : Gets the average farming time.
- **TeamInfoUpdate(n_t, f_d, xp)**: Updates team information based on user input.
  - **TeamDetails(prompt)**: Gets the details of each team. Amount of Champions and their rank.
  - **Repeats(team, f, xp)** : Calculates the number of repeats required for leveling up.
- **ButtonClick(b)** : Simulates a mouse click on the specified button after a short and random countdown.
- **TeamChange(team)** : Selects the next team for the Team Setup section.
- **Drag()** : Drags the team selection screen to display teams 8-14 section.
- **StartFarming()**: Initiates the farming process.
- **Main()**: Main function of RSLAutoFarm.

### Comment Out
- ~~**PlayerEnegry(prompt)**: *Gets the player’s energy (future feature).*~~ Will be included in future commit.
- ~~**GetMousePosition()** : Captures and returns the current mouse position.~~ For development/debugging purposes.

## Notes
  - **Intended Usage**: The program is designed to work best when the computer is not in use, such as during the night. This ensures that there are no interruptions or unexpected changes to the game window.
  - **Window Management**: Minimizing the game window will disrupt the automation process. Ensure that the game window remains active throughout the duration of the script.
  - **Failsafe**: The script includes a failsafe mechanism. If the mouse is moved to the upper-left corner of the screen, pyautogui will raise a pyautogui.FailSafeException and stop the script to prevent unwanted actions.
  - **Ending the Program**: To stop the script, either close the terminal or command prompt window running the script, or press Ctrl+C. This will terminate its execution immediately.

## License
***This project is licensed under the MIT License - see the LICENSE file for details.***

## Version History

- **Version 1.0** (2024-05-26):
  - Initial release.
