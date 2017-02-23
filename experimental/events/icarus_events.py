import re


def process_events(icarus, icarus_event):
    if icarus_event == "sitting":
        icarus.send_command("stand")
    elif 'set-affliction-priority' in icarus_event:
        match_object = re.search(r'set-affliction-priority-(\w+)-(\d+)', icarus_event)
        if match_object:
            icarus.affliction_manager.change_priority(match_object.group(1), match_object.group(2))
        else:
            print("Not sure what to do with " + icarus_event)