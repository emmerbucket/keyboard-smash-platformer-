from PIL import Image
import os

# Root folder containing the player subfolders
root_folder = "./Player"

# Output folder for PNG frames
output_root = "./Player/frames"

for subdir, dirs, files in os.walk(root_folder):
    for filename in files:
        if filename.lower().endswith(".gif"):
            gif_path = os.path.join(subdir, filename)
            
            # Determine relative path to keep folder structure
            rel_path = os.path.relpath(subdir, root_folder)
            output_folder = os.path.join(output_root, rel_path)
            os.makedirs(output_folder, exist_ok=True)
            
            im = Image.open(gif_path)
            frame_number = 0
            
            while True:
                frame_filename = f"{os.path.splitext(filename)[0]}_frame{frame_number}.png"
                frame_path = os.path.join(output_folder, frame_filename)
                im.save(frame_path)
                
                frame_number += 1
                try:
                    im.seek(frame_number)
                except EOFError:
                    break  # No more frames

print("All GIFs converted to PNG frames!")