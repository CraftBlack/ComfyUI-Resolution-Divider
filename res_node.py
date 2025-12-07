import re
import os
import folder_paths

class ResolutionDivider:
    """
    Smart Resolution Divider Node.
    Parses resolution strings or image files and calculates a downscaled resolution 
    based on a divisor value. 
    
    This node is designed as a visual utility helper (calculator), primarily for 
    optimizing VRAM usage in Image-to-Video workflows like Wan 2.2.
    It does not output data to other nodes, but displays results in real-time via the UI.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        # Get list of files in the input directory for the dropdown
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        
        return {
            "required": {
                # 1. Top Position: The resolution string input
                "res_string": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "dynamicPrompts": False,
                    "tooltip": "Enter resolution (e.g., 1920x1080) or select an image below."
                }),
                
                # 2. Middle Position: The divisor value (Float)
                "divider": ("FLOAT", {
                    "default": 1.5, 
                    "min": 0.1, 
                    "max": 10.0, 
                    "step": 0.01, 
                    "display": "number",
                    "tooltip": "The value to divide the resolution by (e.g., 1.5 for Wan 2.2 optimization)."
                }),

                # 3. Bottom Position: Image selector & Upload button
                "image": (sorted(files), {"image_upload": True}),
            },
        }

    # No output slots (Visual-only node)
    RETURN_TYPES = ()
    RETURN_NAMES = ()

    # Treat this as an output node so ComfyUI executes it even without connections
    OUTPUT_NODE = True

    FUNCTION = "calculate_smart"
    
    CATEGORY = "Resolution Utils"

    def calculate_smart(self, res_string, divider, image):
        # Handle empty input case to prevent errors
        if not res_string.strip():
            return {} 

        # Regex to clean input: replace 'x', 'X', '*', and ',' with space
        clean_str = re.sub(r'[xX*,]', ' ', res_string)
        
        # Extract numbers from the string
        parts = [int(s) for s in clean_str.split() if s.isdigit()]

        if len(parts) >= 2:
            width = parts[0]
            height = parts[1]
            
            # Prevent division by zero
            if divider == 0: divider = 1.0

            # Calculate new dimensions (integer)
            new_w = int(width / divider)
            new_h = int(height / divider)
            
            # Print info to the console (useful for debugging history)
            print(f"[ResDivider] File: {image} | Original: {width}x{height} | Divisor: {divider} | Result: {new_w}x{new_h}")
        
        # Return empty dictionary as this is an OUTPUT_NODE with no outputs
        return {"ui": {"text": ["Calculation Done"]}}
