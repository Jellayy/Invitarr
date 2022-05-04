from configparser import ConfigParser


# Init parser
parser = ConfigParser()

# Generate config
parser['Discord'] = {
    'Command Prefix': '.',
    'Bot Token': '',
}

parser['Plex'] = {
    'Email': '',
    'Password': '',
    'Server': '',
}

parser['Role Monitoring'] = {
    'Enable': '1',
    'Monitored Role': 'testing'
}

# Write config
with open('../../config.ini', 'w') as f:
    parser.write(f)
