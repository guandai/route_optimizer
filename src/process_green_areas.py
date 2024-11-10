import cv2
import numpy as np
import random
import os

# Ensure the processed folder exists
PROCESSED_FOLDER = 'static/processed'
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
OUTPUT_PATH = os.path.join(PROCESSED_FOLDER, 'output_image.jpg')

def process_green_areas(image_path):
    """
    Processes the uploaded image to isolate green areas and fill each detected area with a unique color.
    
    Args:
        image_path (str): Path to the input image file.
    
    Returns:
        str: Path to the processed output image.
    """
    # Load the uploaded image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Invalid image file")

    # Convert the image to HSV color space to isolate green color
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for green color
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Create a mask for green areas
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Dilate the green mask to enhance the green areas
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated_green = cv2.dilate(green_mask, kernel, iterations=2)

    # Find contours of green areas
    contours, _ = cv2.findContours(cv2.bitwise_not(dilated_green), 
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an overlay and fill each detected contour with a random color
    overlay = image.copy()
    for contour in contours:
        random_color = [random.randint(0, 255) for _ in range(3)]
        cv2.drawContours(overlay, [contour], -1, random_color, thickness=cv2.FILLED)

    # Blend the overlay with the original image to create the output
    output_image = cv2.addWeighted(overlay, 0.4, image, 0.6, 0)
    cv2.imwrite(OUTPUT_PATH, output_image)

    return OUTPUT_PATH  # Return the static file path
