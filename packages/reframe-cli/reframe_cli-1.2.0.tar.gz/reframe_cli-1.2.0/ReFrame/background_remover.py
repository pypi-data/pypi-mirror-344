import os
import cv2
import sys
import numpy as np
from rembg import remove
from tqdm import tqdm
from ReFrame.utils import create_output_dir
import argparse

def remove_background(image_path, output_path, background_color=None, is_bulk=False):
    """
    Removes the background from an image and optionally replaces it with a specified color.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        background_color (tuple, optional): RGB color to replace the background. If None, the background will be transparent.
        is_bulk (bool): Whether the function is being called in bulk mode (suppress individual file messages).
    """
    #read input
    try:
        with open(image_path, "rb") as img_file:
            input_image = img_file.read()
    except Exception as e:
        print(f"Error: Could not read image {image_path}. Details: {e}")
        if is_bulk:
            sys.exit(1)
        return

    #remove the background using rembg
    try:
        output_image = remove(input_image)
    except Exception as e:
        print(f"Error: Could not remove background for {image_path}. Details: {e}")
        if is_bulk:
            sys.exit(1)
        return

    #convert the output image to a numpy array
    nparr = np.frombuffer(output_image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    #if a background color is specified, replace the transparent background with the color
    if background_color is not None:
        background_color_bgr = background_color[::-1] #convert rgb to bgr cause opencv is compatible with that.
        if img.shape[2] == 4:  #check for alpha channel
            alpha_channel = img[:, :, 3]
            rgb_channels = img[:, :, :3]

            #create a background image with the specified color
            background = np.full_like(rgb_channels, background_color_bgr, dtype=np.uint8)

            #blend the foreground and background
            alpha_factor = alpha_channel[:, :, None] / 255.0
            img = (rgb_channels * alpha_factor + background * (1 - alpha_factor)).astype(np.uint8)

    #output directory
    output_dir = os.path.dirname(output_path)
    if output_dir and not create_output_dir(output_dir):
        print(f"Error: Could not create output directory {output_dir}.")
        return
        
    #save the output image
    try:
        cv2.imwrite(output_path, img)
        if not is_bulk:
            print(f"Background removed and saved to {output_path}")
    except Exception as e:
        print(f"Error: Could not save output image {output_path}. Details: {e}")
        if is_bulk:
            sys.exit(1)
        return


def process_directory(image_dir, output_dir, background_color=None):
    """
    Processes all images in a directory for background removal.

    Args:
        image_dir (str): Path to the directory containing images.
        output_dir (str): Directory to save the processed images.
        background_color (tuple, optional): RGB color to replace the background. If None, the background will be transparent.
    """
    if not create_output_dir(output_dir):
        return

    files = [file for file in os.listdir(image_dir) if file.lower().endswith((".png", ".jpg", ".jpeg"))]
    total_files = len(files)

    if total_files == 0:
        print("No valid image files found in the directory.")
        return

    # Progress bar
    with tqdm(total=total_files, desc="Removing backgrounds", unit="image") as pbar:
        for file in files:
            input_path = os.path.join(image_dir, file)
            output_path = os.path.join(output_dir, file)
            remove_background(input_path, output_path, background_color, is_bulk=True)
            pbar.update(1)

    print(f"\nFinished processing {total_files} images.")


def main():
    """
    Main function to parse command line arguments and call the appropriate functions.
    """
    parser = argparse.ArgumentParser(description="Remove the background from images and optionally replace it with a specified color.")
    parser.add_argument("-input", "--input_path", required=True, help="Path to the image file or directory")
    parser.add_argument("-output", "--output_dir", required=True, help="Directory to save the processed images")
    parser.add_argument("-color", "--background_color", type=str,
                        help="Background color to replace the transparent background (e.g., '255,255,255' for white).")

    args = parser.parse_args()

    #parse the background color
    background_color = None
    if args.background_color:
        try:
            background_color = tuple(map(int, args.background_color.split(',')))
            if len(background_color) != 3 or not all(0 <= c <= 255 for c in background_color):
                raise ValueError
        except ValueError:
            print("Error: Invalid background color. Please specify as 'R,G,B' (e.g., '255,255,255' for white).")
            return

    #check if input is a file or directorys
    if os.path.isdir(args.input_path):
        process_directory(args.input_path, args.output_dir, background_color)
    elif os.path.isfile(args.input_path):
        output_file = os.path.join(args.output_dir, os.path.basename(args.input_path))
        remove_background(args.input_path, output_file, background_color)
    else:
        print(f"Error: Invalid input path {args.input_path}. Must be a file or directory.")


if __name__ == "__main__":
    main()