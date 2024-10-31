# Crate local virtual environment for Python
python -m venv venv

# Activate virtual env
source venv/bin/active

# Update local pip
venv/bin/python -m pip install --upgrade pip

# Install dependencies
venv/bin/pip install -r requirements.txt
