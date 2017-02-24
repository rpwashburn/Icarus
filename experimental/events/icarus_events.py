import re


def process_events(icarus, icarus_event):
    if 'set-affliction-priority' in icarus_event:
        match_object = re.search(r'set-affliction-priority-(\w+)-(\d+)', icarus_event)
        if match_object:
            icarus.affliction_manager.change_priority(match_object.group(1), match_object.group(2))
        else:
            print("Not sure what to do with " + icarus_event)
    elif 'learn-' in icarus_event:
        match_object = re.search(r'learn-(\w+)', icarus_event)
        if match_object:
            learn_amount = 15
            if icarus.defences['scholasticism']:
                learn_amount = 20
            icarus.send_command("learn " + learn_amount + " " + match_object.group(1) + " from "
                                + icarus.character.tutor)
        else:
            print("Not sure what to do with " + icarus_event)
    elif icarus_event == "reset-defences":
        icarus.send_command("def")
    elif icarus_event == "diagnose":
        icarus.send_command("diagnose")
