from PIL import Image
import os

def slice_assets(image_path, output_dir):
    img = Image.open(image_path)
    width, height = img.size
    
    # Grid is 4x2
    cell_w = width // 4
    cell_h = height // 2
    
    names = [
        "cloud_small", "cloud_medium", "cloud_rain", "cloud_storm",
        "icon_check", "icon_calendar", "icon_plus", "icon_gear"
    ]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for i, name in enumerate(names):
        row = i // 4
        col = i % 4
        
        left = col * cell_w
        top = row * cell_h
        right = left + cell_w
        bottom = top + cell_h
        
        asset = img.crop((left, top, right, bottom))
        # Optional: crop further to remove white space if needed, 
        # but let's keep it simple for now.
        asset.save(os.path.join(output_dir, f"{name}.png"))
        print(f"Saved {name}.png")

if __name__ == "__main__":
    # Path from the previous tool output
    image_path = "C:/Users/Khwaish/.gemini/antigravity/brain/f97a57ab-62e7-4266-b9d2-e3e701114c79/pixel_cloud_assets_kit_1768984589349.png"
    output_dir = "c:/Users/Khwaish/.vscode/AIPlanner/frontend/assets/ui"
    slice_assets(image_path, output_dir)
