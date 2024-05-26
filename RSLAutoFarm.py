import pyautogui
import pygetwindow as gw
import time
import random
import logging

__version__ = '0.1.0'

window_title = "Raid: Shadow Legends"

intro = [
    "Welcome to RAID: Shadow Legends AutoFarm!", 
    "For the farming process to start, you will have to prepare the RSL app and then provide some info.",
    "First open RSL app and go to the stage/difficulty you are planning to farm on.",
    "RSLAutoFarm assumes you are farming at stage 12-6 (Normal and Brutal), or any stage from 12-1 to 12-6 (Hard).",
    "Then, go to Team Setup and setup the team you would like to farm.",
    "Every team should contain the Farmer, and one up to three lvl 1 champions of the same rank.",
    "When you finish with the team setup, DO NOT forget to have Team 1 as the selected team.",
    "Check README.md for more details. Happy Farming!!"
]

# Hardcoded positions for all mouse movement/clicks.
button_pos = {
    'Replay' : (990,960),
    'Edit Team' : (1100, 960),
    'Team Setup' : (520, 590),
    'Start' : (1325, 960),
    'Empty Space' : (1420, 726), # failsafe click for pop up windows, such is level up.
    'Team 1' : (520, 160),
    'Team 2' : (520, 295),
    'Team 3' : (520, 425),
    'Team 4' : (520, 560),
    'Team 5' : (520, 695),
    'Team 6' : (520, 825),
    'Team 7' : (520, 960)
}
# Dict about the teams details. Updated through users input.
teams_details = {}
# XP a champion needs to reach max level, based on it's rank.
xp_for_lvl_up = {
    "1" : 22761,
    "2" : 81326,
    "3" : 200681,
    "4" : 449082,
    "5" : 963806
}
# XP earned based on the difficulty of a stage. 
stage_dif = {
    'Normal' : {'xp' : 7336, 'energy' : 4},
    'Hard' : {'xp' : 11800, 'energy' : 6},
    'Brutal' : {'xp' : 17600, 'energy' : 8},
    'Debug' : {'xp' : 100000, 'energy' : 2}
}
# Questions for users inputs. 
prompts = {
    'Teams' : "Q1: - How many teams will farm? ",
    'Difficulty' : "Q2: - At what difficulty do you farm? [Normal(1), Hard(2), Brutal(3)]: ",
    'XP Boots' : "Q3: - Do you an active XP BOOST? (Y/N): ",
    'FarmTime' : "Q4: - How long does it take you to clear the stage? (enter time in MM:SS format): "
}

# Create a custom logger
logger = logging.getLogger('RaidAutoLogger')
logger.setLevel(logging.DEBUG)
# Create handlers and set their levels. Create formatters and add them to handlers. Add handlers to logger.
file_handler = logging.FileHandler('RaidAuto.log')
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_format = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def GetMousePosition(): 
    """Prints mouse's position until KeyboardInterrupt. On KeyboardInterrupt returns mouse position."""
    logging.info("Move your mouse to the desired position and press Ctrl+C to capture the position.")
    try:
        while True:
            x, y = pyautogui.position()
            position_str = f"Position captured: X={x}, Y={y}"
            print(position_str, end="\r")
    except KeyboardInterrupt:
        print("\nPosition captured successfully.")
        return x, y

def WindowDimensions(window_title): 
    """Modifies RSL window's position, width and height properties. Exits program if window not found."""
    win = gw.getWindowsWithTitle(window_title)
    if win:
        win[0].width = 1000
        win[0].height = 1020
        win[0].left = (pyautogui.size()[0] - win[0].width) / 2
        win[0].top = (pyautogui.size()[1] - win[0].height) / 2 - 20
        logging.info(f"Window '{window_title}' resized and repositioned.")
        # win[0].activate() // Returns an error. Will fix it later.
    else:
        logging.error(f"Window with title '{window_title}' not found.")
        time.sleep(2)
        quit()

def Teams(prompt):
    """Prompts user for the number of teams and returns the number if valid."""    
    while True:
        try:
            user_input = int(input(prompt))
            if user_input <= 14: return int(user_input)
            else: logger.error("Invalid input. You must enter a number from 1-14.")
        except: logger.error("Invalid input. You must enter a number from 1-14.")

def StageDifficulty(prompt):
    """Prompts user for stage difficulty and returns corresponding value."""
    while True:
        user_input = input(prompt)
        if user_input in ['0', '1', '2', '3']:
            match user_input:
                case '0': return 'Debug'
                case '1': return 'Normal'
                case '2': return 'Hard'
                case '3': return 'Brutal'
        elif user_input.capitalize() in ['Normal', 'Hard', 'Brutal']: 
            return user_input.capitalize()
        else: logger.error("Invalid input. You must enter a number. [Normal(1), Hard(2), Brutal(3)")

def XpBoost(prompt): 
    """Checks for an active XP Boost. Returns multiplier based on user input."""
    while True:
        user_input = input(prompt).upper()  # Convert to uppercase
        if len(user_input) == 1:
            if user_input == 'Y': return 2
            elif user_input == 'N': return 1
            else: logger.error("Invalid input. Please enter 'Y' for yes or 'N' for no.")
        else: logger.error("Invalid input. You entered more than one character.")

def FarmingTime(prompt):
    """Prompts user for average farming time in MM:SS format and returns total seconds."""
    while True:
        try:
            farm_time = input(prompt)
            if ':' in farm_time and len(farm_time) == 5:
                ft_list = farm_time.split(':')
                if int(ft_list[0]) < 12 and int(ft_list[1]) < 60:
                    total_seconds = (int(ft_list[0]) * 60) + int(ft_list[1])
                    if total_seconds < 30: return total_seconds + 10
                    elif total_seconds >= 30 and total_seconds < 60: return total_seconds + 20
                    elif total_seconds >= 60: return total_seconds + 30
                else: logger.error("Invalid input: Please enter correct a run time. (less than 12:00)") 
            else: logger.error("Invalid input: Please enter correct a run time.")
        except ValueError: logger.error("Invalid input: Please enter correct a run time.")

def PlayerEnegry(prompt):
    """Prompts user for available energy and returns the value if valid."""
    while True:
        try:
            energy = int(input(prompt))
            if energy < 10000: 
                logger.info(f"User has {energy}")
                return energy
        except ValueError: logger.error("Invalid input: Please enter a number less than 9999.")  

def TeamDetails(prompt):
    """Prompts user for team details in format 'Champions'x'Rank'. Returns valid input."""
    while True:
        try:
            user_input = input(prompt) # Format should be 'Champions'x'Rank'. Example: for a team of three 4 rank champions, you should enter 3x4.
            if len(user_input) == 3 and user_input[1] == 'x':
                if int(user_input[0]) < 4 and int(user_input[2]) < 6:
                    user_input = str((int(user_input[0]) + 1)) + user_input[1:]
                    logger.info(f"Team {prompt.split(' ')[6]} has {user_input[0]} Champions of {user_input[2]} rank. 'Champions'x'Rank'")
                    return user_input
                else: logger.error("Invalid input. Enter the number of champions in your team and their rank. Don't include the Farmer")
            else: logger.error("Invalid input. Enter the number of champions in your team and their rank. Don't include the Farmer")
        except: logger.error("Invalid input. Enter the number of champions in your team and their rank. Don't include the Farmer")

def TeamInfoUpdate(n_t, f_d, xp):
    """Updates team details with user input. n_t = number of teams, f_d = farming difficulty, xp = XP Boost."""
    for i in range(n_t):
        info = TeamDetails(f"Q5: - How many champions does your team {i + 1} have and what is their rank? ")
        teams_details['Team ' + str(i + 1)] = {}
        teams_details['Team ' + str(i + 1)]['Champions'] = info[0]
        teams_details['Team ' + str(i + 1)]['Rank'] = info[2]
        teams_details['Team ' + str(i + 1)]['Repeats'] = Repeats(teams_details['Team ' + str(i + 1)], f_d, xp)

def Repeats(team, f, xp): 
    """Calculates and returns the number of repeats required for team to level up. t = team_details[0], f = farm dif."""
    repeat = int(xp_for_lvl_up[team['Rank']] / ((stage_dif[f]['xp'] / int(team['Champions'])) * xp)) + 1
    return repeat

def ButtonClick(b):
    """Simulates a mouse click on the specified button ('b' argument) after random delay."""
    x = random.randint(1, 4)
    time.sleep(x)
    logger.info(f"Mouse move from ButtonClick() occurs after {x} seconds")
    pyautogui.moveTo(b)
    time.sleep(random.randint(1, 4)/2)
    logger.info(f"Mouse click from ButtonClick() occurs after {x/2} seconds")
    pyautogui.click(b)

def TeamChange(team):
    """Selects the next team. If the next team is on the between 8-14 calls the Drag() first."""
    ButtonClick(button_pos['Edit Team'])
    ButtonClick(button_pos['Team Setup'])
    if int(team.split(' ')[1]) < 7:
        ButtonClick(button_pos['Team ' + str(int(team.split(' ')[1]) + 1)])
    else:
        Drag()
        ButtonClick(button_pos['Team ' + str(int(team.split(' ')[1]) - 6)])

def Drag(): 
    """Drags the team selection screen to display teams 8-14."""
    time.sleep(3)
    pyautogui.moveTo(button_pos['Team 7'][0], button_pos['Team 7'][1] + 40)
    pyautogui.mouseDown()
    pyautogui.moveTo(515, 62, 8)
    time.sleep(1)
    pyautogui.mouseUp()

def UserInput():
    """Collects and return a list of user input for the number of teams, farming difficulty, XP boost, and average farming time."""
    no_of_teams = Teams(prompts['Teams'])
    farm_diff = StageDifficulty(prompts['Difficulty'])
    xp_boost = XpBoost(prompts['XP Boots'])
    avg_farm_time = FarmingTime(prompts['FarmTime'])
    if xp_boost == 2: 
        logger.info(f"{no_of_teams} teams. {farm_diff} difficulty. {avg_farm_time} sec/stage. Active XP Boost.")
    else: logger.info(f"{no_of_teams} teams. {farm_diff} difficulty. {avg_farm_time} sec/stage. Inactive XP Boost.")
    # energy_to_spend = PlayerEnegry("How much enegry do you have? ") // Will add it on later version.
    return [no_of_teams, farm_diff, xp_boost, avg_farm_time]

def StartFarming():
    """Initiates the farming process after a short countdown, giving time to the user to activate the RSL window"""
    logging.debug("You have 3 seconds to open the RSL window.")
    print("You have 3 seconds to open the RSL window.")
    x = 3
    while x > 0:
        logging.debug(x)
        print(x)
        x -= 1
        time.sleep(1)

def Main(): 
    """Main function that manages farming process.
    Gets user's input, and gives 3 seconds to the user to make RSL window active.
    Iterates through every team. Ensures the position and dimensions of the window are correct.
    Failsafe clicks first and then starts the process.
    After the first rep, enters the nested iteration until the current team reaches max level.
    TeamChange() is called and the whole process is repeated until every team reaches max level.
    """
    us_in = UserInput()
    TeamInfoUpdate(us_in[0], us_in[1], us_in[2])
    StartFarming()
    for team in teams_details:
        WindowDimensions(window_title) 
        ButtonClick(button_pos['Empty Space']) 
        ButtonClick(button_pos['Start']) 
        logger.debug(team, 'is farming.')
        print(team, 'is farming.')
        rep = teams_details[team]['Repeats'] - 1
        time.sleep(us_in[3]) 
        for _ in range(rep): 
            WindowDimensions(window_title)
            ButtonClick(button_pos['Empty Space']) 
            ButtonClick(button_pos['Replay'])
            logger.debug(teams_details[team], 'is farming.')
            print(team, 'is farming.')
            time.sleep(us_in[3])
        TeamChange(team)

logger.info("Program Starts.")
for line in intro:
    print(line)

if __name__ == '__main__':
    Main()
