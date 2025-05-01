import cv2
import os
import argparse
import sys
from tqdm import tqdm
from ReFrame.utils import create_output_dir

def resize_image_files(image_path, output_dir, output_format, width=None, height=None, ratio=None, focal_point=None, multiplier=None):
    """
    resizes an image.

    Arguments:
        image_path (str): Path to the input image file or directory.
        output_dir (str): Directory where the converted image(s) will be saved.
        output_format (str, optional): The desired output format (e.g., 'png', 'jpg', 'jpeg', 'webp', 'heic').
        width (int): The desired width of the output image.
        height (int): The desired height of the output image.
        ratio (str, optional if specified heightxwidth): The desired aspect ratio (e.g., '1:1', '1:2', '3:4').
        focal_point (str, optional): The focal point for resizing ('left', 'right', 'top', 'bottom', 'center', 'auto').
        multiplier (float, optional): The resizing multiplier (e.g., 2 for 2x).
    """

    #output_format validation
    if output_format is not None and output_format.lower() not in ['png', 'jpg', 'jpeg']:
        print(f"Error: Unsupported output format '{output_format}'. Only 'png', 'jpg', and 'jpeg' are supported.")
        return

    #focal_point validation
    if focal_point is not None and focal_point.lower() not in ['left', 'right', 'top', 'bottom', 'center', 'auto']:
        print(f"Error: Invalid focal point '{focal_point}'.  Please choose 'left', 'right', 'top', 'bottom', 'center', or 'auto(for automatic image focal point detection)'.")
        return

    #ratio validation
    if ratio is not None:
        if not is_valid_ratio(ratio):
            print(f"Error: Invalid ratio '{ratio}'. Please use one of the allowed ratios.")
            return

    #multiplier valdation
    if multiplier is not None and multiplier <= 0:
        print(f"Error: Multiplier must be greater than 0.  Got {multiplier}")
        return

    #handling directories for batch resizing
    if os.path.isdir(image_path):
        process_directory(image_path, output_dir, output_format, width, height, ratio, focal_point, multiplier)
    elif os.path.isfile(image_path):
        process_file(image_path, output_dir, output_format, width, height, ratio, focal_point, multiplier)
    else:
        print(f"Error: Invalid image path.  Must be a file or directory: {image_path}")
        return



def process_file(image_file, output_dir, output_format, width, height, ratio, focal_point, multiplier, is_bulk = False):
    """
    Processes a single image file.

    Args:
        image_file (str): Path to the image file.
        output_dir (str): Directory to save the converted image.
        output_format (str, optional): The desired output format.
        width (int): The desired width of the output image.
        height (int): The desired height of the output image.
        ratio (str, optional if specified heightxwidth): The desired aspect ratio (e.g., '1:1', '1:2', '3:4').
        focal_point (str, optional): The focal point for resizing ('left', 'right', 'top', 'bottom', 'center', 'auto').
        multiplier (float, optional): The resizing multiplier (e.g., 2 for 2x).
    """
    #check if the input image is valid or not
    if not os.path.exists(image_file):
        print(f"Error: Image file not found at {image_file}")
        if is_bulk:
            sys.exit(1)
        return
    
    #check for unsupported input formats
    if image_file.lower().endswith(('.heif', '.heic')):
        print(f"Error: Unsupported input format '{os.path.splitext(image_file)[1]}'. Please use the 'convert' feature to convert the image to 'png', 'jpg', or 'jpeg' first.")
        if is_bulk:
            sys.exit(1)
        return

    #load using cv2.imread
    try:
        img = cv2.imread(image_file)
        if img is None:
            print(f"Warning: Could not read image file: {image_file}. Skipping.")
            if is_bulk:
                sys.exit(1)
            return
    except Exception as e:
        print(f"Error: Could not read image file: {image_file}. Details: {e}")
        if is_bulk:
            sys.exit(1)
        return

    #the output file name
    replace_original = False
    original_format = os.path.splitext(image_file)[1][1:]  #getting the original file extension like png or jpg
    final_format = output_format.lower() if output_format else original_format.lower()  #use original format if not specified
    
    if output_dir == os.path.dirname(image_file) or output_dir is None:
        output_file = os.path.splitext(image_file)[0] + "." + final_format
        replace_original = True
    else:
        #validating the output directory exists
        if not create_output_dir(output_dir):
            return
        
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(image_file))[0] + "." + final_format)

    #perform resizing
    try:
        img = resize_image(img, width, height, ratio, focal_point, multiplier)
    except Exception as e:
        print(f"Error: Could not resize image: {image_file}. Details: {e}")
        if is_bulk:
            sys.exit(1)
        return

    #convert the image based on the specified output format
    try:
        if final_format in ['jpg', 'jpeg']:
            cv2.imwrite(output_file, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        elif final_format == 'png':
            cv2.imwrite(output_file, img)
        else:
            print(f"Error: Unsupported output format '{final_format}', You can later use the convert feature to convert your images to any output format of your choice.")
            if is_bulk:
                sys.exit(1)
            return
        if not is_bulk and not replace_original:
            print(f"Resized {image_file} to {output_file}")
    except Exception as e:
        print(f"Error: Could not resize image: {image_file}. Details: {e}")
        if is_bulk:
            sys.exit(1)
        return
    #replace with original image
    if replace_original:
        try:
            os.remove(image_file)
        except Exception as e:
            print(f"Error: Could not delete original image file {image_file}. Details: {e}")
            if is_bulk:
                sys.exit(1)
            return


def process_directory(image_dir, output_dir, output_format, width, height, ratio, focal_point, multiplier):
    """
    Processes all image files in a directory.

    Args:
        image_dir (str): Path to the directory containing images.
        output_dir (str): Directory to save converted images.
        output_format (str, optional): The desired output format.
        width (int): The desired width of the output image.
        height (int): The desired height of the output image.
        ratio (str, optional if specified heightxwidth): The desired aspect ratio (e.g., '1:1', '1:2', '3:4').
        focal_point (str, optional): The focal point for resizing ('left', 'right', 'top', 'bottom', 'center', 'auto', default: auto).
        multiplier (float, optional): The resizing multiplier (e.g., 2 for 2x).
    """
    #create the output directory if it doesn't exist and only when a different output dir is specified
    if output_dir != image_dir and output_dir is not None:
        if not create_output_dir(output_dir):
            return

    #get files
    files = [file for file in os.listdir(image_dir) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_files = len(files)
    
    if total_files == 0:
        print("No valid image files found in the directory.")
        return
    
    #handle unsupported files
    unsupported_files = [file for file in files if file.lower().endswith(('.heif', '.heic'))]
    if unsupported_files:
        print(f"Error: Unsupported input formats detected: {', '.join(unsupported_files)}")
        print("Please use the 'convert' feature to convert these files to 'png', 'jpg', or 'jpeg' first.")
        return
    
    #progress bar
    with tqdm(total=total_files, desc="Resizing images", unit="image") as pbar:
        for file in files:
            file_path = os.path.join(image_dir, file)
            if os.path.isfile(file_path):
                process_file(file_path, output_dir, output_format, width, height, ratio, focal_point, multiplier, is_bulk=True)
                pbar.update(1) #update bar

    print(f"\nFinished resizing {total_files} images.")



def resize_image(img, width=None, height=None, ratio=None, focal_point=None, multiplier=None):
    """
    Resizes an image, handling both dimensions and aspect ratios with focal point control.

    Args:
        img (numpy.ndarray): The image to resize (OpenCV format).
        width (int): The desired width.
        height (int): The desired height.
        ratio (str, optional if specified heightxwidth): The aspect ratio (e.g., '1:1', '1:2').
        focal_point (str, optional): The focal point for cropping ('left', 'right', 'top', 'bottom', 'center', 'auto'). Defaults to 'auto', which behaves like 'center'.
        multiplier (float, optional): The resizing multiplier (e.g., 2 for 2x). Overrides width, height, and ratio.

    Returns:
        numpy.ndarray: The resized image.
    """

    original_height, original_width = img.shape[:2]
    
    #at least one of width, height, ratio, or multiplier should be provided
    if not any([width, height, ratio, multiplier]):
        raise ValueError("At least one of width, height, ratio, or multiplier must be provided.")
    
    #calculate new dimensions if using multiplier
    if multiplier:
        width = int(original_width * multiplier)
        height = int(original_height * multiplier)
        
    #calculate dimension if using ratios
    if ratio:
        try:
            ratio_width, ratio_height = map(int, ratio.split(':'))
        except ValueError:
            raise ValueError(f"Invalid ratio format: {ratio}.  Use 'width:height' (e.g., '1:1').")

        if not width and not height:
             #calculating width and height based on the ratio
            if original_width / original_height > ratio_width / ratio_height:
                height = original_height
                width = int(height * ratio_width / ratio_height)
            else:
                width = original_width
                height = int(width * ratio_height / ratio_width)
        elif not width:
            width = int(height * ratio_width / ratio_height)
        elif not height:
            height = int(width * ratio_height / ratio_width)

    #if width or height is NONE, calculate the missing value to maintain aspect ratio
    if not width:
        width = int(height * original_width / original_height)
    if not height:
        height = int(width * original_height / original_width)

    #calculate the aspect ratio of the input image
    image_aspect_ratio = original_width / original_height
    target_aspect_ratio = width / height
    
    #resize based on aspect ratio
    if image_aspect_ratio == target_aspect_ratio:
        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        return resized_img

    elif image_aspect_ratio > target_aspect_ratio:
        #image is wider than the target aspect ratio; crop horizontally
        new_width = int(height * image_aspect_ratio)
        resized_img = cv2.resize(img, (new_width, height), interpolation=cv2.INTER_AREA)
        crop_width = int(new_width - width)
        
        #finding the cropping coordinates based on focal point
        focal_point = focal_point or 'auto' #'auto will be used as default, if not specified
        if focal_point.lower() in ['center', 'auto']:
            x1 = crop_width // 2
            x2 = x1 + width
        elif focal_point.lower() == 'left':
            x1 = 0
            x2 = width
        elif focal_point.lower() == 'right':
            x1 = new_width - width
            x2 = new_width
        else:
            raise ValueError(f"Invalid focal point: {focal_point}")
        return resized_img[:, x1:x2]

    else:
        #image is taller than the target aspect ratio; crop vertically
        new_height = int(width / image_aspect_ratio)
        resized_img = cv2.resize(img, (width, new_height), interpolation=cv2.INTER_AREA)
        crop_height = int(new_height - height)
        
        focal_point = focal_point or 'auto'
        if focal_point.lower() in ['center', 'auto']:
            y1 = crop_height // 2
            y2 = y1 + height
        elif focal_point.lower() == 'top':
            y1 = 0
            y2 = height
        elif focal_point.lower() == 'bottom':
            y1 = new_height - height
            y2 = new_height
        else:
            raise ValueError(f"Invalid focal point: {focal_point}")
        return resized_img[y1:y2, :]



def is_valid_ratio(ratio):
    """
    Checks if a given ratio string is valid.

    Args:
        ratio (str): The ratio string (e.g., '1:1', '1:2').

    Returns:
        bool: True if the ratio is valid, False otherwise.
    """
    allowed_ratios = ['1:1', '1:2', '3:4', '1:3', '9:16', '2:3', '4:5',
                        '2:1', '4:3', '3:1', '16:9', '3:2', '5:4']
    return ratio in allowed_ratios



def main():
    """
    Main function to parse command line arguments and call the resize_image_files function.
    """
    parser = argparse.ArgumentParser(description="Convert and resize an image.")
    parser.add_argument("image_path", help="Path to the image file or directory to convert.")
    parser.add_argument("output_dir", nargs='?', default=None, help="Directory to save the converted image(s). If not provided, images are replaced in-place.")
    parser.add_argument("-wh", "--width", type=int, help="The desired width of the output image.")
    parser.add_argument("-ht", "--height", type=int, help="The desired height of the output image.")
    parser.add_argument("-ratio", "--ratio", type=str, help="The desired aspect ratio (e.g., '1:1', '1:2', '3:4').")
    parser.add_argument("-fp", "--focal_point", type=str,
                        help="The focal point for resizing (left, right, top, bottom, center, auto, default: auto).")
    parser.add_argument("-f", "--format", type=str, choices=["png", "jpg", "jpeg"],
                        help="The desired output format (png, jpg, jpeg).")
    parser.add_argument("-multi", "--multiplier", type=float,
                        help="The resizing multiplier (e.g., 2 for 2x).")

    args = parser.parse_args()
    resize_image_files(
        image_path=args.image_path,
        output_dir=args.output_dir,
        output_format=args.format,
        width=args.width,
        height=args.height,
        ratio=args.ratio,
        focal_point=args.focal_point,
        multiplier=args.multiplier
    )

if __name__ == "__main__":
    main()
