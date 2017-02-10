import json
import telnet_values


def get_initial_gmcp():
    gmcp = {
        'Char': {
            'Vitals': {},
            'Items': {
                'List': {},
                'Add': {},
                'Remove': {}
            },
            'Afflictions': {
                'Add': {},
                'Remove': {},
                'List': []
            },
            'Defences': {
                'Add': {},
                'Remove': {},
                'List': []
            },
            'Name': {},
            'Skills': {
                'Groups': []
            },
            'Status': {},
            'StatusVars': {}
        },
        'Room': {
            'Players': [],
            'Info': {},
            'AddPlayer': {},
            'RemovePlayer': ""
        }
    }
    return gmcp


def process_gmcp(icarus, gmcp_lines):

    for gmcp_line in gmcp_lines:
        if 'Char.Afflictions.Add' in gmcp_line:
            icarus.gmcp = char_afflictions_add(icarus.gmcp, gmcp_line)
        elif 'Char.Afflictions.Remove' in gmcp_line:
            icarus.gmcp = char_afflictions_remove(icarus.gmcp, gmcp_line)
        elif 'Char.Afflictions.List' in gmcp_line:
            icarus.gmcp = char_afflictions_list(icarus.gmcp, gmcp_line)
        elif 'Char.Defences.Add' in gmcp_line:
            icarus.gmcp = char_defences_add(icarus.gmcp, gmcp_line)
        elif 'Char.Defences.Remove' in gmcp_line:
            icarus.gmcp = char_defences_remove(icarus.gmcp, gmcp_line)
        elif 'Char.Defences.List' in gmcp_line:
            icarus.gmcp = char_defences_list(icarus.gmcp, gmcp_line)
        elif 'Char.Items.List' in gmcp_line:
            icarus.gmcp = char_items_list(icarus.gmcp, gmcp_line)
        elif 'Char.Items.Add' in gmcp_line:
            icarus.gmcp = char_items_add(icarus.gmcp, gmcp_line)
        elif 'Char.Items.Remove' in gmcp_line:
            icarus.gmcp = char_items_remove(icarus.gmcp, gmcp_line)
        elif 'Char.Name' in gmcp_line:
            icarus.gmcp = char_name(icarus.gmcp, gmcp_line)
        elif 'Char.Skills.Groups' in gmcp_line:
            icarus.gmcp = char_skills_groups(icarus.gmcp, gmcp_line)
        elif 'Char.StatusVars' in gmcp_line:
            icarus.gmcp = char_status_vars(icarus.gmcp, gmcp_line)
        elif 'Char.Status' in gmcp_line:
            icarus.gmcp = char_status(icarus.gmcp, gmcp_line)
        elif 'Char.Vitals' in gmcp_line:
            icarus.gmcp = char_vitals(icarus.gmcp, gmcp_line)
        elif 'Room.Info' in gmcp_line:
            icarus.gmcp = room_info(icarus.gmcp, gmcp_line)
        elif 'Room.Players' in gmcp_line:
            icarus.gmcp = room_players(icarus.gmcp, gmcp_line)
        elif 'Room.AddPlayer' in gmcp_line:
            icarus.gmcp = room_add_player(icarus.gmcp, gmcp_line)
        elif 'Room.RemovePlayer' in gmcp_line:
            icarus.gmcp = room_remove_player(icarus.gmcp, gmcp_line)
        else:
            print("Unknown GMCP:")
            print telnet_values.sub_telnet_codes(gmcp_line)
            print("\n\n\n\n")


def char_afflictions_add(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Afflictions.Add ')
    gmcp['Char']['Afflictions']['Add'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_afflictions_remove(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Afflictions.Remove ')
    gmcp['Char']['Afflictions']['Remove'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_afflictions_list(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Afflictions.List ')
    gmcp['Char']['Afflictions']['List'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_defences_add(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Defences.Add ')
    gmcp['Char']['Defences']['Add'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_defences_remove(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Defences.Remove ')
    gmcp['Char']['Defences']['Remove'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_defences_list(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Defences.List ')
    gmcp['Char']['Defences']['List'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_items_list(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Items.List ')
    gmcp['Char']['Items']['List'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_items_add(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Items.Add ')
    gmcp['Char']['Items']['Add'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_items_remove(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Items.Remove ')
    gmcp['Char']['Items']['Remove'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_name(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Name ')
    gmcp['Char']['Name'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_skills_groups(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Skills.Groups ')
    gmcp['Char']['Skills']['Groups'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_status(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Status ')
    gmcp['Char']['Status'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_status_vars(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.StatusVars ')
    gmcp['Char']['StatusVars'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def char_vitals(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Vitals ')
    gmcp['Char']['Vitals'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def room_info(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Room.Info ')
    gmcp['Room']['Info'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def room_players(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Room.Players ')
    gmcp['Room']['Players'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def room_add_player(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Room.AddPlayer ')
    gmcp['Room']['AddPlayer'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp


def room_remove_player(gmcp, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Room.RemovePlayer ')
    gmcp['Room']['RemovePlayer'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return gmcp

