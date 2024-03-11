import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]


def find_all_game_paths(source):
    game_paths = []
    
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break  # need this to run once only because we just need /data
    
    return game_paths


def create_new_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        

def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        # split every path into base path and the final dir name 
        _, dir_name = os.path.split(path)
        # remove game from dir_name
        new_names.append(dir_name.replace(to_strip, ""))
        
    return new_names
    
    
def copy_and_overwrite(src, dest):
    if os.path.exists(dest):
        # overwrite if the directory already exists
        shutil.rmtree(dest)
        
    # recursively copy dirs
    shutil.copytree(src, dest)
    
    
def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames" : game_dirs,
        "numberOfGames": len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)
    
    
def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name =  file
                break
        break # only one code file in every directory
    
    if code_file_name is None:
        print(f"No {GAME_CODE_EXTENSION} file found in {path}")
        return
    
    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)
    
    
def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)
        
    # run the commands
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True, shell=True)
    print("compile results: ", result)
    
    os.chdir(cwd)
    
    
def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    
    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")
    
    create_new_dir(target_path)
    
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)
        
    # create a json file with metadata
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)
        


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory!")
    
    source, target = sys.argv[1:]
    main(source, target)