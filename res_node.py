import re
import os
import folder_paths

class ResolutionDivider:
    """
    Smart Resolution Divider Node.
    Parses resolution strings or image files and divides them by a float value.
    Useful for VRAM optimization in workflows like Wan 2.2 I2V.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        # Get list of files in input directory
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        
        return {
            "required": {
                # 1. Top Position: The resolution string
                "res_string": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "dynamicPrompts": False,
                    "tooltip": "Example format: 1920x1080 or 1024 1024"
                }),
                
                # 2. Middle Position: The divisor value
                "divider": ("FLOAT", {
                    "default": 1.5, 
                    "min": 0.1, 
                    "max": 10.0, # Increased max just in case
                    "step": 0.01, 
                    "display": "number",
                    "tooltip": "The value to divide the resolution by (e.g., 1.5 or 2.0)"
                }),

                # 3. Bottom Position (in Python list): Image selector & Upload button
                "image": (sorted(files), {"image_upload": True}),
            },
        }

    RETURN_TYPES = ("RESULT", "STRING")
    RETURN_NAMES = ("result_display", "info_str")
    FUNCTION = "calculate_smart"
    
    # NEW CATEGORY NAME
    CATEGORY = "Resolution Utils"

    def calculate_smart(self, res_string, divider, image):
        # Handle empty input
        if not res_string.strip():
            return ("0 x 0", "Empty Input")

        # Regex to clean input: replace x, X, *, and commas with space
        clean_str = re.sub(r'[xX*,]', ' ', res_string)
        # Extract numbers
        parts = [int(s) for s in clean_str.split() if s.isdigit()]

        if len(parts) < 2:
            return ("Error", "Invalid Format")

        width = parts[0]
        height = parts[1]
        
        # Prevent division by zero
        if divider == 0: divider = 1.0

        # Calculate new dimensions (integer)
        new_w = int(width / divider)
        new_h = int(height / divider)

        # Simple result for display
        simple_result = f"{new_w} x {new_h}"
        
        # Detailed info for logging
        full_info = f"File: {image} | Original: {width}x{height} | Div: {divider} | Result: {new_w}x{new_h}"
        
        # Console Log
        print(f"[ResDivider] {full_info}")
        
        return (simple_result, full_info)