import subprocess
import os

def run_git_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def git_add_commit_push(commit_message, branch='master'):
    # Change directory to your repo path
    repo_path = 'C:\\Users\\william\\Documents\\GitHub\\Cv3D'
    os.chdir(repo_path)

    # Running git commands
    run_git_command('git add .')
    run_git_command(f'git commit -m "{commit_message}"')
    run_git_command(f'git push origin {branch}')

# Example usage
commit_msg = input("Your commit message here")
git_add_commit_push(commit_msg)
