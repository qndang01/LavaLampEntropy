import os
import time
from picamera2 import Picamera2

# Initialize the camera
picam2 = Picamera2()


camera_config = picam2.create_still_configuration(main={"size":(1920,1080)}, lores={"size": (640,480)}, display="lores")

picam2.configure(camera_config)
# Start the camera
picam2.start()
# Directory to save images
output_dir = "captured_images/"
os.makedirs(output_dir, exist_ok=True)

# Set the duration for 6 hours in seconds
duration_seconds = 21600

# Capture images every second for 4 hours
start_time = time.time()

for i in range(duration_seconds):
	# Get current time to save as filename
	timestamp = time.strftime("%Y%m%d-%H%M%S")
	image_filename = f"{output_dir}image_{timestamp}.jpg"
    
	# Capture and save the image
	picam2.capture_file(image_filename)
    
	# Print a message to track progress
	print(f"Captured {image_filename}")
    
	# Wait for 1 second before taking the next picture
	time.sleep(1)

# Stop the camera after the session
picam2.stop()
print("Image capture complete.")
