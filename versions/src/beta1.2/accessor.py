import pickle
import json
import os.path
import os
import shutil
from debug import *

class SavesManager:
    def __init__(self):
        self.saves = []
        self.current = None

    def set_current(self, name):
        self.current = name
        return True

    def add_save(self, name):
        if name not in self.saves:
            self.saves.append(name)
            self.current = name
            return True
        return False

    def remove_save(self, name):
        if name in self.saves:
            self.saves.remove(name)
            return True
        return False

    def __str__(self):
        return "current save: " + str(self.current) + ", saves: " + str(self.saves)

def set_current_game(name):
    sm = None
    res = None
    with open("save/saves.object", 'rb') as saves:
        sm = pickle.load(saves)
        res = sm.set_current(name)

    with open("save/saves.object", 'wb') as saves:
        pickle.dump(sm, saves, pickle.HIGHEST_PROTOCOL)
        return res

def get_current_game():
    with open("save/saves.object", 'rb') as saves:
        return pickle.load(saves).current

def add_save(name, world):
    sm = None
    res = None

    # read file and make changes
    with open("save/saves.object", 'rb') as saves:
        sm = pickle.load(saves)
        res = sm.add_save(name)

    # write to file
    with open("save/saves.object", "wb") as saves:
        pickle.dump(sm, saves, pickle.HIGHEST_PROTOCOL)

    # if successfully changed the current save to the new slot, then will put world in that slot
    if res:
        save_world(world)
    else:
        dprint("unable to add save")

    return res

def finish_current_game():
    sm = None
    # read file and make changes
    with open("save/saves.object", 'rb') as saves:
        sm = pickle.load(saves)

    sm.remove_save(sm.current)

    # write to file
    with open("save/saves.object", "wb") as saves:
        pickle.dump(sm, saves, pickle.HIGHEST_PROTOCOL)

def get_saves():
    if os.path.isfile("save/saves.object"):
        with open("save/saves.object", 'rb') as saves:
            return pickle.load(saves).saves
    else:
        reset_saves()
        with open("save/saves.object", 'rb') as saves:
            return pickle.load(saves).saves

def reset_saves():
    try:
        shutil.rmtree('save')
    except:
        pass

    os.makedirs('save')
    
    with open("save/saves.object", 'wb+') as saves:
        sm = SavesManager()
        pickle.dump(sm, saves, pickle.HIGHEST_PROTOCOL)

# utility for opening json files
def get_json(name):
    with open('assets/data/' + name + '.json') as json_file:
        return json.load(json_file)

# utility for accessing the saved world
def save_world(world):
    with open('save/' + get_current_game() + '_world.object','wb+') as world_file:
        pickle.dump(world, world_file, pickle.HIGHEST_PROTOCOL)
    return get_world() 

def get_world():
    with open('save/' + get_current_game() + '_world.object','rb') as world_file:
        return pickle.load(world_file)

def computer_files(name):
    return get_json('game_files')[name]

def all_actions():
    return get_json('actions')

def all_dialogues():
    return get_json('dialogues')

def get_password(name):
    passwords = get_json("passwords")
    if name in passwords:
        return passwords[name]
    return False

def get_program(compname, programname):
    ps = get_json("programs")
    if compname + " " + programname in ps:
        return ps[compname + " " + programname]
    return False

# ------other useful function------------------------------------------ #

def get_trial_num():
    tn = None
    with open('assets/data/trial_number.object','rb') as tnfile:
        tn = int(pickle.load(tnfile))

    with open('assets/data/trial_number.object', 'wb') as tnfile:
        pickle.dump(tn + 1, tnfile, pickle.HIGHEST_PROTOCOL)

    return tn

def set_trial_num():
    with open('assets/data/trial_number.object', 'wb+') as tnfile:
        pickle.dump(1265, tnfile, pickle.HIGHEST_PROTOCOL)