import json
import os
import shutil

class ConfigManager:
    def __init__(self):
        self.config_path = "config.json"

    def load_project_folders(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                config_data = json.load(config_file)
                return config_data.get("project_folders", [])
        else:
            return []

    def add_project_folder(self, folder_path):
        config_data = {"project_folders": self.load_project_folders() + [folder_path]}
        with open(self.config_path, 'w') as config_file:
            json.dump(config_data, config_file)

    def remove_project_folder(self, folder_path):
        project_folders = self.load_project_folders()
        if folder_path in project_folders:
            project_folders.remove(folder_path)
            config_data = {"project_folders": project_folders}
            with open(self.config_path, 'w') as config_file:
                json.dump(config_data, config_file)

    def add_to_startup(self, script_path):
        # Add script to Windows startup
        startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        startup_script_path = os.path.join(startup_folder, "watcher_script.bat")
        shutil.copy(script_path, startup_script_path)
