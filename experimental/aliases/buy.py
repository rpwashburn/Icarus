import re


def buy(icarus, icarus_command):
    match_object = re.search(r'buy-(\w+)', icarus_command)
    if match_object:
        icarus.send_command("get sovereigns from " + icarus.character.inventory['pack'] +
                            "/buy " + match_object.group(1) + "/put sovereigns in " +
                            icarus.character.inventory['pack'])
    else:
        print("Not sure what to do with " + icarus_command)
