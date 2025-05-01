from inquirer import prompt, List
from .utils import init_files, init_packages

questions = [
    List('dimensions', 'How many dimensions would you like to create your game with?', ['2D', '3D'] ),
    List('files', 'Would you like default folders and files to be created?', ['Yes', 'No'] )
]

def run():
    response = prompt(questions)
    if response:
        if response['files'] == 'Yes':
            init_files()

        if response['dimensions'] == '2D':
            packages = ['pygame-ce', 'pygame-gui']
            init_packages(packages)
        else:
            packages = ['pygame-ce', 'pygame-gui', 'moderngl', 'pyglm']
            init_packages(packages)