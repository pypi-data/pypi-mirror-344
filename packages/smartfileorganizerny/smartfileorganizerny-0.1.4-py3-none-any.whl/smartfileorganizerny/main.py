import os
import argparse
import logging
from smartfileorganizerny.utils.organizer import organize_files
from smartfileorganizerny.utils.logger import setup_logging

setup_logging()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Organize files in a folder')
    parser.add_argument('--path', type=str, help='Path to the folder')
    parser.add_argument('--method', choices=["1",'2','3'], help='Method to organize files (1: By type, 2: By date, 3: Both)')
    parser.add_argument('--exclude', type=str, help='Comma-separated list of file extensions to exclude (e.g., .ini,.sys)')
    
    return parser.parse_args()

args = parse_arguments()

def get_folder_path():
    while True:
        folder_path = (args.path.strip("'") if args.path else input("Enter the folder path to organize: "))
        
        if not os.path.isdir(folder_path):
            logging.error(f"Invalid directory: {folder_path}")
            print('⚠️ The folder you entered is Invalid. Please try again.\n')
            args.path = None
        else:
            return folder_path

def get_method_choice():
    if args.method:
        return args.method
    while True:
        print("\nHow would you like to organize your files?")
        print("1. By file type")
        print("2. By date")
        print("3. By both")
        
        method = input("Choose an option (1/2/3): ").strip()
        
        if method not in ["1", "2", "3"]:
            logging.error("Invalid organization method selected.")
            print(f'There is not choice as {method}. Please select an valid choice.\n')
        else:
            return method

def get_excluded_extensions():
    if args.exclude:
        return [ext.strip() for ext in args.exclude.split(',')]
    excluded_extensions = []
    exclude_choice = input("\nDo you want to exclude specific file extensions? (y/n): ").strip().lower()

    if exclude_choice == 'y':
        extensions = input("Enter extensions to exclude (e.g., .ini, .sys, .bak): ").strip()
        excluded_extensions = [ext.strip() for ext in extensions.split(",") if ext.strip()]

    return excluded_extensions

def main():
    while True:
        try:
            folder_path = get_folder_path()
            method = get_method_choice()
            excluded_extensions = get_excluded_extensions()

            organize_files(folder_path, method, excluded_extensions)
            print("\n✅ Files have been organized successfully!\n")

            another = input('Do you want to organize another folder? (y/n): ').strip().lower()
            if another != 'y':
                print('👋 Exiting the progam. Goodbye!')
                break

            args.path = None
            args.method = None
            args.exclude = None

        except Exception as e:
            logging.error(f'An unexpected error occured: {str(e)}')
            print('⚠️ An unexpected error occured. Please try agian.\n')

if __name__ == "__main__":
    main()