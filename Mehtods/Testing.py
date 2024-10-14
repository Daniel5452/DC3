import cv2
import numpy as np


# Function for fish-coral enhanced underwater image processing
def enhance_fish_among_coral(img):
    # Convert to LAB color space to enhance lightness and colors separately
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE to the lightness channel (improves contrast in areas like coral and fish)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l)

    # Merge enhanced L channel with A and B
    lab_enhanced = cv2.merge((l_enhanced, a, b))
    img_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

    # Step 2: Targeted color boost
    # Coral tends to have more reds and oranges, so we will enhance fish colors without boosting coral too much.
    b_channel, g_channel, r_channel = cv2.split(img_enhanced)

    # Increase red channel slightly to restore some lost colors underwater but avoid oversaturation of coral
    fish_boost = np.clip(r_channel + (g_channel // 2), 0, 255).astype(np.uint8)

    # Merge the color channels back
    img_color_boosted = cv2.merge((b_channel, g_channel, fish_boost))

    # Step 3: Selective sharpening for edges (fish vs coral distinction)
    # Coral has a lot of texture, so we will apply moderate sharpening to avoid over-sharpening coral textures
    sharpening_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img_sharpened = cv2.filter2D(img_color_boosted, -1, sharpening_kernel)

    return img_sharpened


# Function to load, enhance, and save an image
def process_fish_coral_image(img_path, output_path):
    # Load image
    img = cv2.imread(img_path)

    # Enhance the image
    img_enhanced = enhance_fish_among_coral(img)

    # Save the enhanced image as a PNG
    cv2.imwrite(output_path, img_enhanced)


# Define the paths (provided by the user)
input_image_path = r'C:\Users\danie\PycharmProjects\DC3\Data\7434_F1_f000350.jpg'
output_image_path = r'C:\Users\danie\PycharmProjects\DC3\Data\7434_F1_f000350_enhanced_coral.png'

# Process the image and save the enhanced version
process_fish_coral_image(input_image_path, output_image_path)

# Notify that the process is complete
print(f"Enhanced image saved to: {output_image_path}")

