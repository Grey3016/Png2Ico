import os
from PIL import Image
from nodes import NODE_CLASS, ComfyNode

# Custom node for converting PNG to ICO
class PNGToICONode(ComfyNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_image_path": ("STRING", {
                    "default": "",
                    "placeholder": "Path to the PNG file (e.g., /path/to/image.png)"
                }),
                "icon_size": ("INT", {
                    "default": 256,
                    "min": 16,
                    "max": 256,
                    "step": 16,
                    "placeholder": "Size of the ICO icon (16, 32, 48, 256, etc.)"
                }),
            }
        }

    @classmethod
    def OUTPUT_TYPES(cls):
        return {
            "output_image_path": ("STRING",)
        }

    def run(self, input_image_path, icon_size):
        if not input_image_path or not os.path.isfile(input_image_path):
            raise ValueError("Invalid file path provided for the PNG image.")

        # Load the PNG image using PIL
        try:
            image = Image.open(input_image_path)
        except Exception as e:
            raise ValueError(f"Failed to open the image. Error: {str(e)}")

        # Ensure the image has an alpha channel (RGBA)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Prepare the output file path with the .ico extension
        output_file_path = os.path.splitext(input_image_path)[0] + '.ico'

        # Convert and save the image as an ICO file
        try:
            image.save(output_file_path, format='ICO', sizes=[(icon_size, icon_size)])
        except Exception as e:
            raise ValueError(f"Failed to save the ICO file. Error: {str(e)}")

        return (output_file_path,)

# Register the node with ComfyUI
NODE_CLASS.register_node("PNGToICONode", PNGToICONode)
