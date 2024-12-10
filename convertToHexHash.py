import os
import hashlib
from PIL import Image


# Function to calculate the hash of an image
def hash_image(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Convert to bytes (you can also consider other formats like 'RGB', 'L', etc.)
        img_bytes = img.tobytes()

    # Hash the bytes using sha256 (128-bit hash)
    sha_hash = hashlib.sha256(img_bytes).hexdigest()  # Hexadecimal string

    return hash


# Function to read all jpg images in a folder and hash them
def hash_images_in_folder(folder_path):
    hex_hashes = []

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a .jpg file
        if filename.lower().endswith('.jpg'):
            file_path = os.path.join(folder_path, filename)
            file_hash = hash_image(file_path)
            hex_hashes.append(file_hash)  # Append hexadecimal hash

    return hex_hashes


# Specify the folder containing jpg images
folder_path = 'captured_images'

# Get the list of hexadecimal hashes for all jpg images
image_hex_hashes = hash_images_in_folder(folder_path)

# Write the hexadecimal hashes to a file, each on a new line
with open('image_hex_hashes.txt', 'w') as file:
    for hex_hash in image_hex_hashes:
        file.write(hex_hash + '\n')  # Write each hex hash on a new line

print("Hexadecimal hashes written to image_hex_hashes.txt")
