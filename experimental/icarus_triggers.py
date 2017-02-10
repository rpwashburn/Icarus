import re
import time
from twisted.internet import reactor


def process_triggers(icarus, regex_lines):
    if re.search('(\w+) sit yourself down\.', regex_lines):
        # reactor.callLater(10, icarus.send_command, "stand")
        icarus.send_command("stand")
