# To avoid false positives for nothing!!
Just 2 false postitive, which can go up to 5 if you do not follow the steps
_____________________________________
- install inno by the menu, reinstall inno if defender sends you notification
- after first conversion, enter your icon.ico in the file where the python code is located
- main.py is the launch file
- Icon = 803x829
- Installer background = 750x1024

_____________________________________
## Recommended code for your main.py



### Deleted CMD for your interface tkinter
```python
import subprocess
import importlib
import json
import os

# Path to the JSON file, which is used to save that the modules have been installed and opens the python .py file directly
json_file = 'modules_installed.json'

# Function to check and install modules
def check_and_install_modules(modules):
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"{module} is already installed.")
        except ImportError:
            print(f"{module} is not installed, install in progress...")
            subprocess.check_call(['pip', 'install', module])

# List of required modules
required_modules = [
    'tkinter',
    'ctypes',
    'setuptools'     # Add setuptools which includes distutils
]

# Check if the JSON file exists to avoid installing them again
if not os.path.exists(json_file):
    # Vérifier et installer les modules nécessaires
    check_and_install_modules(required_modules)
    
    # Créer le fichier JSON pour indiquer que les modules sont installés
    with open(json_file, 'w') as file:
        json.dump({"modules_installed": True}, file)

# Update the setuptools module to ensure distutils is up to date
subprocess.check_call(['pip', 'install', '--upgrade', 'setuptools'])

# Run the desired Python script
subprocess.run(['python', 'Your-Interface-Tkinter.py']) 
```




