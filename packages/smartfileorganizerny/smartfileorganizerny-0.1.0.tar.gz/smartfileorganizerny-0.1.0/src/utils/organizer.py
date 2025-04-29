import os
import shutil
import logging
from datetime import datetime

def organize_by_type(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            file_extension = filename.split('.')[-1]
            type_folder = os.path.join(folder_path, file_extension)
            
            if not os.path.exists(type_folder):
                os.mkdir(type_folder)
            
            shutil.move(file_path, os.path.join(type_folder, filename))
            logging.info(f"Moved {filename} to {file_extension}/")

def organize_by_date(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            date_folder = datetime.fromtimestamp(mod_time).strftime('%Y-%m')
            
            date_folder_path = os.path.join(folder_path, date_folder)
            
            if not os.path.exists(date_folder_path):
                os.mkdir(date_folder_path)
            
            shutil.move(file_path, os.path.join(date_folder_path, filename))
            logging.info(f"Moved {filename} to {date_folder}/")

def organize_files(folder_path, method, excluded_extensions):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith('.'):
                logging.info(f'Skipping file: {file}')
                continue

            if any(file.endswith(ext) for ext in excluded_extensions):
                logging.info(f'Skipping file with excluded extensions: {file}')
                continue

            file_path = os.path.join(root, file)

    if method == "1":
        logging.info(f"Organizing files by type in {folder_path}")
        organize_by_type(folder_path)
    elif method == "2":
        logging.info(f"Organizing files by date in {folder_path}")
        organize_by_date(folder_path)
    elif method == "3":
        logging.info(f"Organizing files by both type and date in {folder_path}")
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path):
                file_extension = filename.split('.')[-1]
                mod_time = os.path.getmtime(file_path)
                date_folder = datetime.fromtimestamp(mod_time).strftime('%Y-%m')
                
                type_folder = os.path.join(folder_path, file_extension, date_folder)
                
                if not os.path.exists(type_folder):
                    os.makedirs(type_folder)
                
                shutil.move(file_path, os.path.join(type_folder, filename))
                logging.info(f"Moved {filename} to {file_extension}/{date_folder}/")

    logging.info("Files have been organized successfully!")