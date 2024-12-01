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
import requests

### MODEL
from typing import List
from pydantic import BaseModel

class Assessment(BaseModel):
    filename: str
    comment: str

class Assessments(BaseModel):
    assesments: List[Assessment]


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

def get_commit_message():
    """Get the commit message being used."""
    try:
        with open(".git/COMMIT_EDITMSG", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Commit message file not found."

def get_current_commit_hash():
    """Get the current commit hash (HEAD)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "HEAD not yet committed."

def call_openai_api(content):
    """Send the code changes to OpenAI for review."""
    
    from openai import OpenAI
    client = OpenAI()

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are a code reviewer. Point out any issues or suggestions for improvement. Multiple assessment in one file is possible."},
                {"role": "user", "content": f"Please review the following code changes:\n\n{content}"}
            ],
        response_format=Assessments,
    )

    openai_result =  completion.choices[0].message.parsed
    print('MESS: ', openai_result)
    return openai_result.model_dump()


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
    reviews = call_openai_api(diff)
    
    # Print OpenAI's response
    print("\n--- OpenAI Review ---\n")
    print(reviews)

    # Send to server
    assesments = reviews.get('assesments')
    if len(assesments) > 0:
        commit_message = get_commit_message()
        commit_hash = get_current_commit_hash()
        for a in assesments:
            data = {
                "filename": a.get('filename', ''),
                "comment": a.get('comment', ''),
                "commit_message": commit_message,
                "commit_hash": commit_hash,
            }
            print('DATA: ', data)

            url = os.environ.get('COCOMASS_API_URL', 'http://127.0.0.1:5000/assessments')
            headers = {"Content-Type": "application/json"}
            data = data
            response = requests.post(url, headers=headers, json=data)

    
    # Allow or block the commit
    BLOCK_COMMIT = False
    if BLOCK_COMMIT:
        return 1  # Block the commit
    return 0  # Allow the commit to proceed

if __name__ == "__main__":
    main()
