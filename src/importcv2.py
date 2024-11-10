import cv2
import numpy as np
import random

# Load the image
image_path = 'city_map.jpg'  # Replace with your image path
new_area_image = cv2.imread(image_path)

# Convert the image to HSV color space to better isolate the green lines
hsv_image = cv2.cvtColor(new_area_image, cv2.COLOR_BGR2HSV)

# Define HSV range for green color (adjust as needed to match the green line in the image)
lower_green = np.array([40, 40, 40])
upper_green = np.array([80, 255, 255])

# Create a mask that isolates the green lines
green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

# Use the mask to extract the green lines from the original image
green_lines = cv2.bitwise_and(new_area_image, new_area_image, mask=green_mask)

# Dilate the green lines mask to make it more continuous and connected for segmentation
kernel_green = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
dilated_green_lines = cv2.dilate(green_mask, kernel_green, iterations=2)

# Find contours based on the dilated green lines mask to detect areas divided by the green lines
contours_green_divisions, _ = cv2.findContours(cv2.bitwise_not(dilated_green_lines), 
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create an overlay to fill each detected area with a unique color
overlay_colored_areas = new_area_image.copy()

# Loop through each detected area and fill it with a different color
for i, contour in enumerate(contours_green_divisions):
    # Generate a random color for each area
    color_area = [random.randint(0, 255) for _ in range(3)]
    # Fill the area with the random color
    cv2.drawContours(overlay_colored_areas, [contour], -1, color_area, thickness=cv2.FILLED)

# Blend the overlay with the original image to apply transparency
output_colored_areas = cv2.addWeighted(overlay_colored_areas, 0.4, new_area_image, 0.6, 0)

# Save the result to a file
output_path = 'colored_city_map_output.jpg'  # Specify the output file path
cv2.imwrite(output_path, output_colored_areas)
print(f"Processed image saved to {output_path}")
