import keyboard, time

try: import json
except ImportError: import ujson as json

with open("configuration.json", 'r') as f:
    config = json.load(f)

delay = config["delay"]
    
#Command types
def multiple(value):
    time.sleep(delay)
    keyboard.press_and_release('backspace')
    time.sleep(delay)
    keyboard.write(value)

class command:
    def __init__(self, key, type, value):
        self.key = key
        self.type = type
        self.value = value

    def run(self):
        if self.type == "single":
            multiple(self.value)
            time.sleep(delay)
            keyboard.press_and_release('enter')
        elif self.type == "multiple":
            multiple(self.value)
        elif self.type == "print":
            print(self.value)
        else:
            print(f'Command type is "{self.type}"')
            print("Incorrect command type!")

#Parse config
print("Loading configuration")
if len(config["players"]) > 6:
    raise AssertionError("Too many players!")

print(f'You\'r nickname on 0')
commands = [command("0", "single", config["self"])]
for key, plr in enumerate(config["players"], 4):
    print(f'Player "{plr}" on key {key}')
    commands.append(command(str(key), "single", plr))

print()

for key, cmd in config["commands"].items():
    print(f'Registred {cmd["type"]} command "{cmd["value"]}" on key {key}')
    commands.append(command(key, cmd["type"], cmd["value"]))

print()

#Run
print('working...\npress "-" to pause\npress "+" to resume')
try:
    while True:
        for cmd in commands: keyboard.add_hotkey(cmd.key, cmd.run)
        keyboard.wait("-")
        keyboard.remove_all_hotkeys()
        keyboard.wait("+")
except: print("stop!")