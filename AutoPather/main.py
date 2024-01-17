# main.py

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dependency_tracker import DependencyTracker

# Initialize Dependency Tracking
def initialize_dependency_tracking():
    # Adapt to handle project folders within Google Drive synced locations
    # Maintain a configuration file with updated paths reflecting the Google Drive folder structure
    # Create and return an initial dependency dictionary
    config_file_path = "google_drive_config.json"
    dependency_tracker = DependencyTracker(config_file_path)
    return dependency_tracker

# User Input for Projects
def user_input_for_projects(dependency_tracker):
    # Enhance the user interface to accommodate input for Google Drive synced folder paths
    # Implement validation to ensure paths are within the Google Drive synced locations
    while True:
        project_path = input("Enter the path of a project folder within Google Drive (or type 'exit' to finish): ")
        if project_path.lower() == 'exit':
            break
        if os.path.exists(project_path) and project_path.startswith("/content/drive/"):
            # Path validation passed
            dependency_tracker.add_project(project_path)
            print(f"Project '{project_path}' added successfully.")
        else:
            print("Invalid path. Make sure the path exists and starts with '/content/drive/'.")

# Real-Time Monitoring of Changes
def start_file_system_watcher(dependency_tracker):
    class FileChangeHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            if event.is_directory or not event.src_path.endswith(".py"):  # Consider only Python files
                return
            if event.event_type == 'created':
                print(f"File {event.src_path} was created.")
                handle_file_change(event.src_path, dependency_tracker)
            elif event.event_type == 'deleted':
                print(f"File {event.src_path} was deleted.")
                handle_file_change(event.src_path, dependency_tracker)
            elif event.event_type == 'modified':
                print(f"File {event.src_path} was modified.")
                handle_file_change(event.src_path, dependency_tracker)
            elif event.event_type == 'moved':
                print(f"File {event.src_path} was moved to {event.dest_path}.")
                handle_file_change(event.dest_path, dependency_tracker)

    # Create an observer and start monitoring the Google Drive synced folder
    observer = Observer()
    observer.schedule(FileChangeHandler(), path="/content/drive/", recursive=True)
    observer.start()
    print("File system watcher is active. Press Ctrl+C to stop.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Handling File Changes
def handle_file_change(file_path, dependency_tracker):
    # Adapt scanning algorithms for compatibility with Google Drive's file structure
    # Ensure real-time updates in dependency tracking as files sync with Google Drive
    dependency_tracker.scan_file_for_dependencies(file_path)

# Entry point
if __name__ == "__main__":
    # Initialize Dependency Tracking
    dependency_tracker = initialize_dependency_tracking()

    # User Input for Projects
    user_input_for_projects(dependency_tracker)

    # Real-Time Monitoring of Changes
    start_file_system_watcher(dependency_tracker)
