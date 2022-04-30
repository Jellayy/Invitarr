from configparser import ConfigParser


# Init parser
parser = ConfigParser()

# Generate config
parser['Discord'] = {
    'Command Prefix': '.',
    'API Key': '',
    'Monitored Role': ''
}

# Write config
with open('../../config.ini', 'w') as f:
    parser.write(f)
