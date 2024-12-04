import os
import re
from organizer import Organizer
from dynamic_extension import add_new_category
from logger import logger

if __name__ == "__main__":
    base_directory = input("Enter the path of the directory to organize (leave blank for current working directory): ").strip()
    
    if not base_directory:  # Use current working directory if input is blank
        base_directory = os.getcwd()
        logger.info(f"No directory path provided. Using the current working directory: {base_directory}")
    
    if not os.path.exists(base_directory):
        logger.error(f"Directory does not exist: {base_directory}")
    elif not re.match(r'^[A-Za-z0-9_\\/\-:.]+$', base_directory):
        logger.error("Invalid directory path format")
    else:
        # Example usage of adding a new file type dynamically
        add_new_category('Scripts', ['.py', '.sh'])  # Adding new category before organizing
       
        # Initialize and run the organizer
        organizer = Organizer(base_directory)
        organizer.organize()
