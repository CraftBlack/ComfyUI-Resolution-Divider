from .res_node import ResolutionDivider

NODE_CLASS_MAPPINGS = {
    "ResolutionDividerNode": ResolutionDivider
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResolutionDividerNode": "Resolution Divider"
}

# Define web directory for JS files
WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

print("\033[34m[Resolution Utils] \033[92mLoaded Successfully!\033[0m")
