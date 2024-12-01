### Copy the pre-commit shell script to .git/hooks and make it executable
# pwd
# chmod +x /home/dantebytes/Documents/REPO/cocomass/.git/hooks/pre-commit


# import subprocess

# def get_committed_files():
#     """Gets a list of files staged for the next commit."""
#     try:
#         result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, check=True)
#         return result.stdout.strip().splitlines()
#     except subprocess.CalledProcessError as e:
#         print(f"Error running git diff: {e}")
#         return []

# # Example usage:
# if __name__ == "__main__":
#     print("Running Python pre-commit script...")
#     files_to_commit = get_committed_files()
#     if files_to_commit:
#         print("Files staged for commit:")
#         for file in files_to_commit:
#             print(file)
#     else:
#         print("No files staged for commit.")



#!/usr/bin/env python3

import os
import subprocess
import openai

# Configure your OpenAI API Key here
OPENAI_API_KEY = "your_openai_api_key"

def get_git_diff():
    """Get the staged changes for the current commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--unified=0", "--no-color"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error while running git diff: {e.stderr}")
        return ""

def call_openai_api(content):
    """Send the code changes to OpenAI for review."""
    
    from openai import OpenAI
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are a code reviewer. Point out any issues or suggestions for improvement."},
                {"role": "user", "content": f"Please review the following code changes:\n\n{content}"}
            ]
    )

    print('MESS: ', completion.choices[0].message)
    return completion.choices[0].message


def main():
    # Get the staged changes
    diff = get_git_diff()
    if not diff:
        print("No changes to commit.")
        return 0  # Allow the commit to proceed
    
    # Print the changes
    print("\n--- Staged Changes ---\n")
    print(diff)
    
    # Send to OpenAI for review
    print("\n--- Sending changes to OpenAI for review... ---\n")
    review = call_openai_api(diff)
    
    # Print OpenAI's response
    print("\n--- OpenAI Review ---\n")
    print(review)
    
    # Allow or block the commit
    BLOCK_COMMIT = False
    if BLOCK_COMMIT:
        return 1  # Block the commit
    return 0  # Allow the commit to proceed

if __name__ == "__main__":
    main()
