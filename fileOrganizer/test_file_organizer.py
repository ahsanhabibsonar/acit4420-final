#test_file_organizer.py
import pytest
from organizer import Organizer
import os

def test_organize_files(tmpdir):
    # Create a temporary directory for testing
    base_dir = tmpdir.mkdir("test_dir")
    image_file = base_dir.join("test_image.jpg")
    doc_file = base_dir.join("test_doc.pdf")

    # Create dummy files
    image_file.write("dummy image content")
    doc_file.write("dummy document content")

    # Initialize Organizer
    organizer = Organizer(str(base_dir))
    organizer.organize()

    # Check if files are moved to the correct folders
    assert os.path.exists(base_dir.join("Images/test_image.jpg"))
    assert os.path.exists(base_dir.join("Documents/test_doc.pdf"))