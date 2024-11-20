import os
import re
from random import randint
from datetime import datetime

def rename_file(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]

    # Remove special characters and replace spaces with underscores
    filename = re.sub(r'[^a-zA-Z0-9 ]', '', filename)  # Keep only alphanumeric and spaces
    filename = filename.replace(' ', '_')  # Replace spaces with underscores

    # Generate a random 7-digit number
    random_number = randint(1000000, 9999999)

    # Get the current date
    current_date = datetime.now().strftime('%Y%m%d')

    # Create the new filename
    new_filename = f"{filename}_{random_number}_{current_date}.{ext}"

    # Optional: Store in a specific subdirectory
    return os.path.join('uploads', new_filename)
