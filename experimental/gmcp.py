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
                'Groups': [],
                'List': {}
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
        try:
            if 'Char.Afflictions.Add' in gmcp_line:
                icarus.gmcp = char_afflictions_add(icarus, gmcp_line)
            elif 'Char.Afflictions.Remove' in gmcp_line:
                icarus.gmcp = char_afflictions_remove(icarus, gmcp_line)
            elif 'Char.Afflictions.List' in gmcp_line:
                icarus.gmcp = char_afflictions_list(icarus, gmcp_line)
            elif 'Char.Defences.Add' in gmcp_line:
                icarus.gmcp = char_defences_add(icarus, gmcp_line)
            elif 'Char.Defences.Remove' in gmcp_line:
                icarus.gmcp = char_defences_remove(icarus, gmcp_line)
            elif 'Char.Defences.List' in gmcp_line:
                icarus.gmcp = char_defences_list(icarus, gmcp_line)
            elif 'Char.Items.List' in gmcp_line:
                icarus.gmcp = char_items_list(icarus, gmcp_line)
            elif 'Char.Items.Add' in gmcp_line:
                icarus.gmcp = char_items_add(icarus, gmcp_line)
            elif 'Char.Items.Remove' in gmcp_line:
                icarus.gmcp = char_items_remove(icarus, gmcp_line)
            elif 'Char.Name' in gmcp_line:
                icarus.gmcp = char_name(icarus, gmcp_line)
            elif 'Char.Skills.Groups' in gmcp_line:
                icarus.gmcp = char_skills_groups(icarus, gmcp_line)
            elif 'Char.Skills.List' in gmcp_line:
                icarus.gmcp = char_skills_list(icarus, gmcp_line)
            elif 'Char.StatusVars' in gmcp_line:
                icarus.gmcp = char_status_vars(icarus, gmcp_line)
            elif 'Char.Status' in gmcp_line:
                icarus.gmcp = char_status(icarus, gmcp_line)
            elif 'Char.Vitals' in gmcp_line:
                icarus.gmcp = char_vitals(icarus, gmcp_line)
            elif 'Room.Info' in gmcp_line:
                icarus.gmcp = room_info(icarus, gmcp_line)
            elif 'Room.Players' in gmcp_line:
                icarus.gmcp = room_players(icarus, gmcp_line)
            elif 'Room.AddPlayer' in gmcp_line:
                icarus.gmcp = room_add_player(icarus, gmcp_line)
            elif 'Room.RemovePlayer' in gmcp_line:
                icarus.gmcp = room_remove_player(icarus, gmcp_line)
            else:
                print("Unknown GMCP:")
                print telnet_values.sub_telnet_codes(gmcp_line)
                print("\n\n\n\n")
        except Exception as e:
            print("-------------ERROR PARSING GMCP----------------")
            print(e)
            print(gmcp_line)
            print("-----------------------------------------------")


def char_afflictions_add(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Afflictions.Add ')
    icarus.gmcp['Char']['Afflictions']['Add'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    icarus.affliction_manager.affliction_added()
    return icarus.gmcp


def char_afflictions_remove(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Afflictions.Remove ')
    icarus.gmcp['Char']['Afflictions']['Remove'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    icarus.affliction_manager.affliction_removed()
    return icarus.gmcp


def char_afflictions_list(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Afflictions.List ')
    icarus.gmcp['Char']['Afflictions']['List'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_defences_add(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Defences.Add ')
    icarus.gmcp['Char']['Defences']['Add'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_defences_remove(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Defences.Remove ')
    icarus.gmcp['Char']['Defences']['Remove'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_defences_list(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Defences.List ')
    icarus.gmcp['Char']['Defences']['List'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_items_list(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Items.List ')
    icarus.gmcp['Char']['Items']['List'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_items_add(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Items.Add ')
    icarus.gmcp['Char']['Items']['Add'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_items_remove(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Items.Remove ')
    icarus.gmcp['Char']['Items']['Remove'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_name(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Name ')
    icarus.gmcp['Char']['Name'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_skills_groups(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Skills.Groups ')
    icarus.gmcp['Char']['Skills']['Groups'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_skills_list(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Skills.List ')
    icarus.gmcp['Char']['Skills']['List'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_status(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Status ')
    icarus.gmcp['Char']['Status'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_status_vars(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.StatusVars ')
    icarus.gmcp['Char']['StatusVars'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def char_vitals(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Char.Vitals ')
    icarus.gmcp['Char']['Vitals'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    icarus.reset_prompt_variables()
    return icarus.gmcp


def room_info(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Room.Info ')
    icarus.gmcp['Room']['Info'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def room_players(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Room.Players ')
    icarus.gmcp['Room']['Players'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def room_add_player(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Room.AddPlayer ')
    icarus.gmcp['Room']['AddPlayer'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp


def room_remove_player(icarus, gmcp_line):
    gmcp_split_lines = gmcp_line.split('Room.RemovePlayer ')
    icarus.gmcp['Room']['RemovePlayer'] = json.loads(gmcp_split_lines[1].split(telnet_values.IAC)[0])
    return icarus.gmcp

