import tomllib
import sys
import os
import subprocess

CMGR_ROOT = "/var/cmgr"
#CONFIG_DIR = os.path.join(
#    os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
#    "cmgr")
#LOCAL_STORAGE_DIR = os.path.join(
#    os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share")),
#                   "cmgr")
#CONFIG_FILE = os.path.join(CONFIG_DIR, "config.toml")
#STORAGE_DIR = "/var/cmgr"
CONFIG_DIR = "/etc/cmgr"
CONFIG_FILE = "/etc/cmgr/config.toml"

class Config:
    '''Class to handle the configuration file settings'''
    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            os.makedirs(CONFIG_DIR)
            with open(CONFIG_FILE, "w", encoding="utf_8") as config:
                config.write("[cmgr]\n")

        #if not os.path.isdir(LOCAL_STORAGE_DIR):
        #    os.makedirs(LOCAL_STORAGE_DIR)

        self.data = self.load_config()


    def lookup_key(self, key):
        return self.data['cmgr'][key]

        
    def load_config(self):
        '''Loads the config from the TOML file'''
        with open(CONFIG_FILE, "rb") as config:
            return tomllib.load(config)

    def get_root_dir(self):
        try:
            return self.data['cmgr']['root_dir']
        except KeyError:
            return CMGR_ROOT
        
    def get_storage_dir(self):
        try:
            return self.data['cmgr']['storage_dir']
        except KeyError:
            print("storage_dir key not found!")
            sys.exit(1)

    def get_source_stage3(self):
        try:
            return self.data['cmgr']['source_stage3']
        except KeyError:
            print("source_files key not found!")
            sys.exit(1)

    def get_local_storage(self):
        try:
            return self.data['cmgr']['stage3_storage']
        except KeyError:
            return LOCAL_STORAGE_DIR
