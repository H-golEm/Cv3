import os
import json
import re
from collections import defaultdict

class DependencyTracker:
    def __init__(self, project_folders):
        self.project_folders = project_folders
        self.dependency_dict = self.initialize_dependency_tracking()

    def initialize_dependency_tracking(self):
        # Create or load a configuration file containing project folder paths
        config_path = "config.json"

        if os.path.exists(config_path):
            # Load existing configuration file
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        else:
            # Create a new configuration file with empty dependency dictionary
            initial_dependency_dict = defaultdict(list)
            with open(config_path, 'w') as config_file:
                json.dump(initial_dependency_dict, config_file)
            return initial_dependency_dict

    def scan_files_for_dependencies(self):
        for folder in self.project_folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Use regular expressions to identify dependencies
                        # For example, you can modify this pattern based on your specific coding patterns
                        dependencies = re.findall(r'"([^"]*)"', content)

                        # Update the dependency dictionary
                        for dependency in dependencies:
                            self.dependency_dict[dependency].append(file_path)

    def update_dependencies(self, file_or_folder, new_name):
        # Update dependencies when a file or folder is renamed
        if file_or_folder in self.dependency_dict:
            dependencies = self.dependency_dict[file_or_folder]
            del self.dependency_dict[file_or_folder]

            # Update the file or folder name in dependencies
            for dependency in dependencies:
                updated_dependency = dependency.replace(file_or_folder, new_name)
                self.dependency_dict[new_name].append(updated_dependency)

    def handle_spaces_in_names(self, file_or_folder):
        # Implement a mechanism to handle spaces in file or folder names
        if ' ' in file_or_folder:
            new_name = file_or_folder.replace(' ', '_')  # Replace spaces with underscores (modify as needed)
            self.update_dependencies(file_or_folder, new_name)

    def manage_changes_in_folder_structure(self, file_or_folder, new_path):
        # Update paths in all dependent files when a file or folder is moved
        if file_or_folder in self.dependency_dict:
            dependencies = self.dependency_dict[file_or_folder]
            del self.dependency_dict[file_or_folder]

            # Update the file or folder path in dependencies
            for dependency in dependencies:
                updated_dependency = dependency.replace(file_or_folder, new_path)
                self.dependency_dict[file_or_folder].append(updated_dependency)

    def dynamic_handling_of_name_changes(self, file_or_folder):
        # Ensure the system dynamically adapts to changes in file or folder names
        for dependency, files in self.dependency_dict.items():
            for file in files:
                if file_or_folder.lower() in file.lower():
                    # Update the file_or_folder name in dependencies
                    updated_dependency = dependency.replace(file_or_folder, file_or_folder + '_updated')
                    self.dependency_dict[file_or_folder + '_updated'].extend(self.dependency_dict.pop(file_or_folder))

    def handle_file_encoding_changes(self, file_path):
        # Implement a check for changes in file encoding
        pass  # Modify the function as needed

    def case_sensitivity_handling(self, file_or_folder):
        # Account for case sensitivity in file or folder names
        for dependency, files in self.dependency_dict.items():
            for file in files:
                if file_or_folder.lower() == file.lower():
                    # Update the file_or_folder name in dependencies
                    updated_dependency = dependency.replace(file_or_folder, file_or_folder + '_updated')
                    self.dependency_dict[file_or_folder + '_updated'].extend(self.dependency_dict.pop(file_or_folder))

    def trigger_dependency_update(self):
        # Implement the logic to update dependencies here
        # Call functions to update dependencies based on the outlined steps
        print("Project folder opened or modified. Updating dependencies...")
        self.scan_files_for_dependencies()
