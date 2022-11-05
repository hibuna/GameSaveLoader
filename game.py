import os, sys, json, shutil, subprocess
from typing import List

from config import Config
from command_parser import CLI

CONFIG_FILE = "config.txt"
Cf = Config(CONFIG_FILE)

class Game:

    def __init__(self, title) -> None:
        with open(os.path.join(Cf.CWD, Cf.GAMES_INFO), "r") as f:
            game_info: dict = json.load(f)[title]

        self.title: str = title
        self.in_menu: bool = game_info["in_menu"]

        self.save_manual: str = game_info["save_manual"]
        self.save_exit: str = game_info["save_exit"]
        self.save_auto: str = game_info["save_auto"]
        self.files: List[str] = game_info["files"]

        self.game_root = os.path.join(game_info["game_root"], game_info["exe"])
        self.app_data_root = os.path.join(Cf.APP_DATA, game_info["app_data_root"])
        self.save_root = os.path.join(self.app_data_root, game_info["characters"])
        self._exe: str = os.path.join(Cf.GAMES_ROOT, self.game_root)

    def handle(self, command: str) -> None:
        if command in Cf.ARGS_START:
            CLI.print_(f"Launching {self.title}")
            self._launch()
            condition = "in main menu" if self.in_menu else "game is closed()"
            CLI.print_(f"Most recent exitsave can be saved or loaded while {condition}.")

        elif command in Cf.ARGS_SAVE:
            CLI.print_("Copying exitsave...")
            self._save()
            CLI.print_("Exitsave copied")

        elif command in Cf.ARGS_LOAD:
            CLI.print_("Loading...")
            self._load()
            CLI.print_("Loaded most recent exitsave")

    def _launch(self):
        subprocess.Popen(self._exe)

    def _save(self):
        destination = os.path.join(self.save_root, Cf.SAVE_DIR)
        save_nr = str(len(os.listdir(destination))+1)
        destination = os.path.join(destination, f"{self.save_exit} {save_nr}")

        shutil.copytree(
            os.path.join(self.save_root, self.save_exit),
            destination,
        )

    def _load(self):
        origin = os.path.join(self.save_root, Cf.SAVE_DIR)
        save_nr = str(len(os.listdir(origin)))
        origin = os.path.join(origin, f"{self.save_exit} {save_nr}")

        shutil.copytree(
            origin,
            os.path.join(self.save_root, self.save_exit),
            dirs_exist_ok=True,
        )

def main():
    user_input = sys.argv[1:]
    prompt = CLI(2, Cf.ARGS_ALLOWED)
    prompt.verify_valid_input(user_input)
    
    prompt.parse(user_input, sigil='')
    title = prompt.args[0]
    command = prompt.args[1]
    
    game = Game(title)
    game.handle(command)

if __name__ == "__main__":
    main()
