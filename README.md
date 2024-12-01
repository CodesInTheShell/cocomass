# cocomass

pre-commit AI assistant and code reviewer.

Review your code before it reaches your remote repository.

### How this works
Everytime you trigger git commit to commit your code changes, this will use AI to review your code and store its assessments to the cocomass server.

Cocomass is a two piece software.
1. The script - It uses the pre-commit bash script and the pre-commit-hook.py to run the code review then send the assessments to the cocomass server.

2. The server - It is the pre-commit-server.py where you can view the code assessments.

### Instructions
1. Copy the pre-commit file of this repo to .get/hooks/pre-commit and be sure it is executable.
chmod +x .git/hooks/pre-commit

2. Set the environment variables and path on the .git/hooks/pre-commit file
export OPENAI_API_KEY="sk-proj-YOUR_OPEN_AI_API_KEY"
PYTHON_SCRIPT="/home/dantebytes/path/to/cocomass/pre-commit-hook.py"
VENV_PATH="/home/dantebytes/path/to/cocomass/venv/bin/python"

3. Run the server (assuming you have a docker installed). If no docker, it is just a python flask app and mongodb. Create a venv and pip install requirements.txt and install mongodb, might need to check mongodb uri. Preferred to use docker.

docker compose up --build

Contact the author for more details or just drop an ticket or issue.
www.dantebytes.com