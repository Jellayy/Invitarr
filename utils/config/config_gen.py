from configparser import ConfigParser


def gen_empty_config():
    # Init parser
    parser = ConfigParser()

    # Generate config
    parser['Discord'] = {
        'Command Prefix': '.',
        'Bot Token': '',
    }

    parser['Plex Accounts'] = {
        'Num Accounts': '1'
    }

    parser['Plex Account 0'] = {
        'User': '',
        'Password': '',
        'Num Servers': '1',
        'Server 0': '',
    }

    parser['Role Monitoring'] = {
        'Enable': '1',
        'Monitored Role': 'testing'
    }

    # Write config
    with open('/config/config.ini', 'w') as f:
        parser.write(f)


if __name__ == "__main__":
    main()
