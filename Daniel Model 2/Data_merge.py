import os
import random

# Paths to the main Classification folder
classification_dir = r'C:\Users\danie\Downloads\DC3\DeepFish\DeepFish\Classification'

# Directories to store the split datasets
train_dir = os.path.join(classification_dir, 'train')
val_dir = os.path.join(classification_dir, 'val')
test_dir = os.path.join(classification_dir, 'test')

# Make the new directories for hard links
for split_dir in [train_dir, val_dir, test_dir]:
    os.makedirs(os.path.join(split_dir, 'valid'), exist_ok=True)
    os.makedirs(os.path.join(split_dir, 'empty'), exist_ok=True)

# Function to split data into train, val, test sets (70-20-10)
def split_data(images, train_ratio=0.7, val_ratio=0.2):
    random.shuffle(images)
    train_count = int(len(images) * train_ratio)
    val_count = int(len(images) * val_ratio)
    train_images = images[:train_count]
    val_images = images[train_count:train_count + val_count]
    test_images = images[train_count + val_count:]
    return train_images, val_images, test_images

# Function to create hard links if they don't already exist
def create_hard_link_if_not_exists(src, dest_dir):
    dest = os.path.join(dest_dir, os.path.basename(src))
    # Check if the hard link already exists to prevent errors
    if not os.path.exists(dest):
        os.link(src, dest)

# Iterate through each subfolder (e.g., 7117, 7268)
for folder in os.listdir(classification_dir):
    folder_path = os.path.join(classification_dir, folder)

    if os.path.isdir(folder_path):
        # Get valid images and empty images
        valid_images = [os.path.join(folder_path, 'valid', img) for img in os.listdir(os.path.join(folder_path, 'valid'))]
        empty_images = [os.path.join(folder_path, 'empty', img) for img in os.listdir(os.path.join(folder_path, 'empty'))]

        # Split valid images
        train_valid, val_valid, test_valid = split_data(valid_images)
        for img in train_valid:
            create_hard_link_if_not_exists(img, os.path.join(train_dir, 'valid'))
        for img in val_valid:
            create_hard_link_if_not_exists(img, os.path.join(val_dir, 'valid'))
        for img in test_valid:
            create_hard_link_if_not_exists(img, os.path.join(test_dir, 'valid'))

        # Split empty images
        train_empty, val_empty, test_empty = split_data(empty_images)
        for img in train_empty:
            create_hard_link_if_not_exists(img, os.path.join(train_dir, 'empty'))
        for img in val_empty:
            create_hard_link_if_not_exists(img, os.path.join(val_dir, 'empty'))
        for img in test_empty:
            create_hard_link_if_not_exists(img, os.path.join(test_dir, 'empty'))

print("Data has been split and hard links created in train, val, and test folders.")
