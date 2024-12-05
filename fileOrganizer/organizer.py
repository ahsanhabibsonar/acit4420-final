
import os
import shutil
#from logger import logger
from .logger import logger

from .config import Config
import csv

class Organizer:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.file_types = Config.FILE_TYPES
        self.categories_csv = "categories.csv"
        # Explicit list of program-related files to exclude
        self.excluded_files = {
            "main.py",
            "config.py",
            "logger.py",
            "organizer.py",
            "dynamic_extension.py",
            "categories.csv"
        }

    def organize(self):
        if not os.path.exists(self.base_directory):
            logger.error(f"Directory does not exist: {self.base_directory}")
            return

        files_moved = False

        try:
            for root, _, files in os.walk(self.base_directory):
                for file in files:
                    if file.lower() in self.excluded_files:  # Check if the file is excluded
                        logger.info(f"Skipping program file: {file}")
                        continue
                    file_extension = os.path.splitext(file)[1].lower()
                    if not self.get_category(file_extension):
                        self.add_unknown_file(file_extension)
                    self.organize_file(root, file)
                    files_moved = True
        except PermissionError as e:
            logger.error(f"Permission error while accessing {e.filename}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

        if not files_moved:
            logger.info("No files were moved. The directory might be empty or contain unsupported file types.")

    def organize_file(self, root, file):
        file_extension = os.path.splitext(file)[1].lower()
        category = self.get_category(file_extension)

        if category:
            self.move_file(root, file, category)
            return True
        else:
            logger.info(f"No category found for file: {file}, skipping...")
            return False

    def get_category(self, file_extension):
        for category, extensions in self.file_types.items():
            if file_extension in extensions:
                return category
        return None

    def move_file(self, root, file, category):
        category_path = os.path.join(self.base_directory, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

        src = os.path.join(root, file)
        dest = os.path.join(category_path, file)

        try:
            shutil.move(src, dest)
            logger.info(f"Moved {file} to {category}")
        except shutil.Error as e:
            logger.error(f"Error moving file {file}: {e}")

    def add_unknown_file(self, file_extension):
        """
        Automatically adds unknown file types to a dynamically created category.
        """
        # Automatically create a category based on the file extension
        category_name = file_extension.lstrip('.').upper()  # e.g., '.tex' becomes 'TEX'

        # Add to the in-memory file_types
        if category_name not in self.file_types:
            self.file_types[category_name] = [file_extension]
            logger.info(f"Automatically added new category '{category_name}' for extension '{file_extension}'.")

        # Update categories.csv
        self.update_categories_csv(category_name, file_extension)

    def update_categories_csv(self, category_name, file_extension):
        """
        Updates the categories.csv file with the new category and extension.
        """
        csv_path = self.categories_csv

        # Load existing categories
        existing_categories = {}
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    existing_categories[row['Category']] = row['Extensions'].split()

        # Add the new category
        if category_name not in existing_categories:
            existing_categories[category_name] = [file_extension]
        else:
            existing_categories[category_name].append(file_extension)

        # Write updated categories back to the CSV
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Category', 'Extensions'])
            for category, ext_list in existing_categories.items():
                writer.writerow([category, ' '.join(ext_list)])
