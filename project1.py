import argparse
import os
import re
import shutil

class FileManager:
    def __init__(self):
        pass

    def search_files(self, pattern, directory="."):
        matching_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if re.search(pattern, file):
                    matching_files.append(os.path.join(root, file))
            for dir_name in dirs:
                if re.search(pattern, dir_name):
                    matching_files.append(os.path.join(root, dir_name))
        return matching_files

    def rename_files(self, original_name, new_name, directory="."):
        print(f"Attempting to rename '{original_name}' to '{new_name}' in directory '{directory}'")
        for root, dirs, files in os.walk(directory):
            if original_name in files:
                original_path = os.path.join(root, original_name)
                new_path = os.path.join(root, new_name)
                os.rename(original_path, new_path)
                print(f"File '{original_name}' renamed to '{new_name}'")
                return True
            elif original_name in dirs:
                original_path = os.path.join(root, original_name)
                new_path = os.path.join(root, new_name)
                os.rename(original_path, new_path)
                print(f"Directory '{original_name}' renamed to '{new_name}'")
                return True
        print(f"File or directory '{original_name}' not found in directory '{directory}'.")
        return False

    def modify_file_content(self, file_name, new_content, directory="."):
        for root, dirs, files in os.walk(directory):
            if file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'w') as file:
                    file.write(new_content)
                print(f"Content of file '{file_name}' modified.")
                return True
        print(f"File '{file_name}' not found in directory '{directory}'.")
        return False

    def copy_files(self, file_names, home_directory=".", target_directory="."):
        try:
            for file_name in file_names:
                src = os.path.join(home_directory, file_name)
                dst = os.path.join(target_directory, file_name)

                if os.path.isdir(src):
                    # Copy entire directory
                    shutil.copytree(src, dst)
                    print(f"Directory '{file_name}' copied to '{target_directory}'.")
                else:
                    # Copy individual file
                    shutil.copy(src, dst)
                    print(f"File '{file_name}' copied to '{target_directory}'.")
            return True
        except Exception as e:
            print(f"Error copying files: {e}")
            return False

    def move_files(self, file_names, home_directory=".", target_directory="."):
        try:
            for file_name in file_names:
                src = os.path.join(home_directory, file_name)
                dst = os.path.join(target_directory, file_name)

                if os.path.isdir(src):
                    # Move entire directory
                    shutil.move(src, dst)
                    print(f"Directory '{file_name}' moved to '{target_directory}'.")
                else:
                    # Move individual file
                    shutil.move(src, dst)
                    print(f"File '{file_name}' moved to '{target_directory}'.")
            return True
        except Exception as e:
            print(f"Error moving files: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="File Management Tool")

    parser.add_argument("directory", help="Directory to perform operations in")
    parser.add_argument("command", choices=["search", "rename", "modify", "copy", "move"], help="Command to execute")
    parser.add_argument("args", nargs="*", help="Arguments for the command")

    args = parser.parse_args()

    file_manager = FileManager()

    if args.command == "search":
        if len(args.args) != 1:
            print("Usage: search <pattern>")
            return
        pattern = args.args[0]
        matching_files = file_manager.search_files(pattern, args.directory)
        print("Matching files and directories:")
        for file in matching_files:
            print(file)

    elif args.command == "rename":
        if len(args.args) != 2:
            print("Usage: rename <original_name> <new_name>")
            return
        original_name, new_name = args.args
        if file_manager.rename_files(original_name, new_name, args.directory):
            print(f"Renamed '{original_name}' to '{new_name}'")
        else:
            print(f"File or directory '{original_name}' not found.")

    elif args.command == "modify":
        if len(args.args) != 2:
            print("Usage: modify <file_name> <new_content>")
            return
        file_name, new_content = args.args
        if file_manager.modify_file_content(file_name, new_content, args.directory):
            print(f"Content of '{file_name}' modified.")
        else:
            print(f"File '{file_name}' not found.")

    elif args.command == "copy":
        if len(args.args) < 3:
            print("Usage: copy <file_names> <home_directory> <target_directory>")
            return
        file_names = args.args[:-2]
        home_directory = args.args[-2]
        target_directory = args.args[-1]
        if file_manager.copy_files(file_names, home_directory, target_directory):
            print(f"Files and directories copied to '{target_directory}'")
        else:
            print("Error copying files.")

    elif args.command == "move":
        if len(args.args) < 3:
            print("Usage: move <file_names> <home_directory> <target_directory>")
            return
        file_names = args.args[:-2]
        home_directory = args.args[-2]
        target_directory = args.args[-1]
        if file_manager.move_files(file_names, home_directory, target_directory):
            print(f"Files and directories moved to '{target_directory}'")
        else:
            print("Error moving files.")

if __name__ == "__main__":
    main()
