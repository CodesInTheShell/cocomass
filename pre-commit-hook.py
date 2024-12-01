### Copy the pre-commit shell script to .git/hooks and make it executable
# pwd
# chmod +x /home/dantebytes/Documents/REPO/cocomass/.git/hooks/pre-commit


import subprocess

def get_committed_files():
    """Gets a list of files staged for the next commit."""
    try:
        result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, check=True)
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return []

# Example usage:
if __name__ == "__main__":
    print("Running Python pre-commit script...")
    files_to_commit = get_committed_files()
    if files_to_commit:
        print("Files staged for commit:")
        for file in files_to_commit:
            print(file)
    else:
        print("No files staged for commit.")