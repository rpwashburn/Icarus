import re
import time
from twisted.internet import reactor
from aliases.buy import buy


def process_aliases(icarus, icarus_command):
    if icarus_command == "bash":
        icarus.send_attack(icarus.character.my_class.get_bash_command())
    elif 'settarget-' in icarus_command:
        split_command = icarus_command.split('-')
        icarus.set_target(split_command[1])
    elif 'learn-' in icarus_command:
        match_object = re.search(r'learn-(\w+)', icarus_command)
        if match_object:
            icarus.send_command("learn 15 " + match_object.group(1) + " from " + icarus.character.tutor)
        else:
            print("Not sure what to do with " + icarus_command)
    elif 'farsee-' in icarus_command:
        match_object = re.search(r'farsee-(\w+)', icarus_command)
        if match_object:
            print("Farsee " + match_object.group(1))
            icarus.send_command("farsee " + match_object.group(1))
        else:
            print("Not sure what to do with " + icarus_command)
    elif 'buy-' in icarus_command:
        buy(icarus, icarus_command)
    else:
        icarus.send_command(icarus_command)
