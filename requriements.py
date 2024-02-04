import subprocess

# List of packages to install
packages = [
    'flask',
    'flask_sqlalchemy',
    'psycopg2',
    'openpyxl',
    'pandas',
    'sqlalchemy'
]

# Iterate over the list of packages and install each using pip
for package in packages:
    subprocess.run(['pip', 'install', package])
