import csv
import os
from logger import logger

def add_new_category(category_name, extensions):
    # Path to the categories CSV
    csv_path = "categories.csv"

    # Check if the category already exists in the CSV
    existing_categories = {}
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_categories[row['Category']] = row['Extensions'].split()

    # If the category exists, check if extensions are already included
    if category_name in existing_categories:
        current_extensions = set(existing_categories[category_name])
        new_extensions = set(extensions)
        if new_extensions.issubset(current_extensions):
            logger.info(f"Category '{category_name}' with extensions {extensions} already exists.")
            return
        else:
            # Add missing extensions to the category
            existing_categories[category_name] = list(current_extensions.union(new_extensions))
            logger.info(f"Added new extensions {new_extensions - current_extensions} to category '{category_name}'.")
    else:
        # Add new category to the dictionary
        existing_categories[category_name] = extensions
        logger.info(f"Added new category: {category_name} with extensions: {extensions}")

    # Write the updated categories back to the CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Extensions'])
        for category, ext_list in existing_categories.items():
            writer.writerow([category, ' '.join(ext_list)])

