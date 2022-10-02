from os import environ, path, mkdir
from json import load, dump

from pluralkit import Client, Unauthorized as UnauthorisedAccess
from appdirs import AppDirs

import menubuilder as mb

dirs = AppDirs("PluralkitCLI", "MFC")
config_file = path.join(dirs.user_data_dir, 'config.json')

pk_token = environ.get("PKTOKEN")

config = {"pk_token":None}

def generate_config():
    if path.isfile(dirs.user_data_dir):
        print(f"{mb.WARNING}The file at {dirs.user_data_dir} needs to be deleted as this should be a directory!", end=mb.ENDC+'\n')
        raise SystemExit
    elif path.isdir(dirs.user_data_dir):
        pass
    else:
        mkdir(dirs.user_data_dir)
    with open(config_file, 'w+') as f:
        config['pk_token'] = input(f"{mb.OKGREEN}Please enter your PluralKit token! (do `pk!token` in PluralKit's DM): ")
        print(end=mb.ENDC) # Reset terminal colour
        dump(config, f)


if pk_token:
    pass
elif path.isfile(config_file):
    with open(config_file) as f:
        config = load(f)
else:
    print(f"{mb.WARNING}There's no token for PluralKit provided in the config or environment variable!", end=mb.ENDC+'\n')
    generate_config()


if not isinstance(config.get("pk_token", None), str) and (not isinstance(pk_token, str) and pk_token != None):
    print(f"{mb.WARNING}The token provided in the config invalid! Please provide a valid token!", end=mb.ENDC+'\n')
    generate_config()
elif not isinstance(pk_token, str) and pk_token != None:
    print(f"{mb.WARNING}The token provided is invalid! Please provide a valid token!", end=mb.ENDC+'\n')
    raise SystemExit


pk = Client(config['pk_token'], async_mode=False)


try:
    system = pk.get_system()
except UnauthorisedAccess as e:
    print(e)
    raise SystemExit("Your PluralKit token is either invalid or something went wrong!")


print(f"Welcome {system.name}!")
mb.menu("What would you like to do?")

