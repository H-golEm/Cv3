import os

def create_project_structure(base_path):
    # Define the structure
    directories = ["css", "js", "assets"]
    files = {
        "": ["index.html", "README.md"],
        "css": ["styles.css"],
        "js": ["main.js"]
    }

    # Create directories
    for directory in directories:
        os.makedirs(os.path.join(base_path, directory), exist_ok=True)

    # Create files with basic structure
    for directory, file_list in files.items():
        for file in file_list:
            file_path = os.path.join(base_path, directory, file)
            with open(file_path, 'w') as f:
                if file == "index.html":
                    f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>3D Interactive Page</title>\n</head>\n<body>\n</body>\n</html>")
                elif file == "styles.css":
                    f.write("/* CSS file */")
                elif file == "main.js":
                    f.write("// JavaScript file")
                elif file == "README.md":
                    f.write("# 3D Interactive Page Project")

create_project_structure(r"C:\Users\william\Documents\GitHub\Cv3D")
