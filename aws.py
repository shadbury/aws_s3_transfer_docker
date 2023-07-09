import os
from configparser import ConfigParser

def get_profiles():
    config = ConfigParser()
    aws_folder = os.path.expanduser("~/.aws")
    config_files = [
        os.path.join(aws_folder, "config"),
        os.path.join(aws_folder, "credentials")
    ]
    config.read(config_files)

    # Retrieve profiles from the [profile <name>] sections in the config file
    profiles = []
    for section in config.sections():
        if section.startswith("profile "):
            profile_name = section.split(" ")[1]
            profiles.append(profile_name)

    # Retrieve profiles from the [profile <name>] sections in the credentials file
    credentials_profiles = config.sections()
    for profile in credentials_profiles:
        if profile not in profiles:
            profiles.append(profile)

    # Retrieve the 'default' profile if it exists
    if 'default' in config:
        profiles.append('default')

    return profiles
