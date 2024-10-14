import cv2
import numpy as np

def enhance_fish_among_coral(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Step 1(improve contrast in areas like coral and fish)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))  # Slightly increased clip limit for better contrast
    l_enhanced = clahe.apply(l)

    lab_enhanced = cv2.merge((l_enhanced, a, b))
    img_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

    # Step 2: Red Channel Boost
    b_channel, g_channel, r_channel = cv2.split(img_enhanced)
    fish_boost = np.clip(r_channel + (g_channel // 2), 0, 255).astype(np.uint8)
    img_color_boosted = cv2.merge((b_channel, g_channel, fish_boost))

    # Step 3: a bit of gentle sharpening for edges (fish vs coral distinction)
    sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img_sharpened = cv2.filter2D(img_color_boosted, -1, sharpening_kernel)

    return img_sharpened

def process_fish_coral_image(img_path, output_path):
    img = cv2.imread(img_path)

    img_enhanced = enhance_fish_among_coral(img)

    cv2.imwrite(output_path, img_enhanced)

input_image_path = r'C:\Users\danie\PycharmProjects\DC3\Data\7434_F1_f000350.jpg'
output_image_path = r'C:\Users\danie\PycharmProjects\DC3\Data\7434_F1_f000350_enhanced_final.png'

process_fish_coral_image(input_image_path, output_image_path)

print(f"Enhanced image saved to: {output_image_path}")
