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

