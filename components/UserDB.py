import json
import os
from utils.singleton import SingletonMeta
from utils.files_mgmt import res_dir

DEAFAULT_GENERAL_USERDB_PATH = os.path.join(res_dir, "db/general_userdb.json")

class _UserDB(metaclass=SingletonMeta):

    theme_day_night_setting = "theme_day_night_setting"

    def __init__(self, userdb_path=DEAFAULT_GENERAL_USERDB_PATH):
        self.__userdb_path = userdb_path
        with open(self.__userdb_path, "r+") as userdb:
            # self.__userdb = userdb
            self.__user_setting = json.load(userdb)

    def save_userdb(self, key=None, value=None):
        if key:
            self.__user_setting[key] = value
        with open(self.__userdb_path, "w+") as userdb:
            json.dump(self.__user_setting, userdb)

    def get_user_setting(self, key):
        try:
            return self.__user_setting[key]
        except KeyError:
            return None
    

user_db = _UserDB()