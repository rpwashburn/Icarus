import re


def trigger(icarus, line):
    match_object = re.search(r'[System]: Running queued balance command: (.*)', line)
    if match_object:
        print("Running command: " + match_object.group(1))
        # icarus.send_to_mudlet("running command + " + match_object.group(1))