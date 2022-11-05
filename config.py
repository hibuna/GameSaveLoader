import os
from typing import List
from configparser import ConfigParser

class Config:
    def __init__(self, file: str) -> None:
        self.CWD = os.getcwd()
        self.APP_DATA = str(os.getenv("LOCALAPPDATA"))

        get = ConfigParser()
        with open(file, 'r') as f:
            get.read_file(f)

        self.GAMES_ROOT: str = get["FILES"]["GAMES_ROOT"].strip('"')
        self.SAVE_DIR: str = get["FILES"]["SAVE_DIR"].strip('"')
        self.GAMES_INFO: str = get["FILES"]["GAMES_INFO"].strip('"')

        self.SAVE_DATE_FORMAT: str = get["DEFAULTS"]["SAVE_DATE_FORMAT"]
        self.SAVE_FILE_FORMAT: str = get["DEFAULTS"]["SAVE_FILE_FORMAT"]

        _list = lambda str_: str_.replace(' ', '').split(',')
        self.ARGS_START: List[str] = _list(get["COMMANDS"]["START"])
        self.ARGS_SAVE:  List[str] = _list(get["COMMANDS"]["SAVE"])
        self.ARGS_LOAD: List[str] = _list(get["COMMANDS"]["LOAD"])
        self.ARGS_ALLOWED: List[str] = (
            self.ARGS_START 
            + self.ARGS_SAVE 
            + self.ARGS_LOAD
        )