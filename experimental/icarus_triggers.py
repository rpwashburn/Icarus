import re
import telnet_values
import time
from twisted.internet import reactor
import triggers.system_queue

# Command for doing tempTimer stuff:
# reactor.callLater(10, icarus.send_command, "stand")


def process_triggers(icarus, regex_line):
    regex_line = regex_line.strip('\r')
    print("---------------------REGEX LINE------------------------")
    print telnet_values.sub_telnet_codes(regex_line)
    print("--------------------------------------------------------")
    triggers.system_queue.trigger(icarus, regex_line)
