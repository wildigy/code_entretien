# Code Entretien
# Common
1) Go to the base of the project code_entretien from your console.
2) Chose an python environment in version 3.10 or superior.
3) Run in console "python -m pip install -r app/requirements.txt" (python must correspond to point 2).
4) Run in console "export PYTHONPATH=${PWD}".
## Launch application
5) Make sure port 8000 is free on localhost.
6) Run in console "python app/__init__.py" (python must correspond to point 2).
### See if currently open
7) Open browser of choice.
8) Go to http://localhost:8000/time_open/is_open_on (check swagger doc at http://localhost:8000 if needed).
### See if next opening
7) Open browser of choice.
8) Go to http://localhost:8000/time_open/next_opening_date (check swagger doc at http://localhost:8000 if needed).
## Alter opening times
5) Run in console (NOT IDE CONSOLE!) "python script/alter_open.py" (python must correspond to point 2).
6) Follow instructions in console.
