import logging

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="error.log",  # Log errors to a file
    filemode="a"  # Append to the file instead of overwriting
)

logger = logging.getLogger()
