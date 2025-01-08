import os

def get_top_image_from_static():
    static_dir = 'C:/Users/Saray/OneDrive/Desktop/MINI PROJECT2/static'  # Directory containing image files
    image_files = [f for f in os.listdir(static_dir) if os.path.isfile(os.path.join(static_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return image_files[0]
    

# Example usage
top_image_path = get_top_image_from_static()
if top_image_path:
    print("Top-most image file:", top_image_path)
else:
    print("No image files found in the 'static' directory.")
