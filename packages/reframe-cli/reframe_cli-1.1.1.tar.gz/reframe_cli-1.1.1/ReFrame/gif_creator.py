import cv2
import os 
import imageio #for creating the GIF
import argparse
from tqdm import tqdm
from ReFrame.utils import create_output_dir

def create_gif(image_path, output_dir, duration=100):
    """
    creates an animated GIF by stacking up images.

    Arguments:
        image_path (str): Path to the directory containing the images.
        output_dir (str): Path + the file extension to save the output GIF file. (ex. home/xyz/trial/test1.gif)
        duration (int, optional): Duration of each frame in the GIF in milliseconds. Defaults to 100ms.
    """
    
    #validate duration
    if duration <= 0:
        print("Error: Duration must be a positive integer.")
        return
    
    #verify output path
    if not output_dir.lower().endswith('.gif'):
        print("Error: Output path must have a .gif extension.")
        return
    
    #verify the image directory exists or not
    if not os.path.exists(image_path):
        print(f"Error: Image directory not found at {image_path}")
        return

   #create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_dir)
    if output_dir:
        if not create_output_dir(output_dir):
            print(f"Error: Could not create output directory: {output_dir}")
            return

    #get images
    image_files = sorted([os.path.join(image_path, f) for f in os.listdir(image_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if not image_files:
        print(f"Error: No PNG or JPG images found in {image_path}")
        return

    #read the images using opencv
    images = []
    total_files = len(image_files)
    
    #progress bar
    with tqdm(total=total_files, desc="Processing images", unit="image") as pbar:
        for image_file in image_files:
            try:
                img = cv2.imread(image_file)
                if img is None:
                    print(f"Warning: Could not read image {image_file}. Skipping.")
                    continue
                #convert from BGR to RGB for imageio to process
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                images.append(img_rgb)
                pbar.update(1) #update progress bar
            except Exception as e:
                print(f"Error reading image {image_file}: {e}")
                return
    
    if not images:
        print("Error: No valid images to create a GIF.")
        return
    
    #create the GIF (using imageio)
    try:
        imageio.mimsave(output_dir, images, duration=duration / 1000.0)  #converting ms to seconds
        print(f"Created animated GIF: {output_dir}")
    except Exception as e:
        print(f"Error creating GIF: {e}")
        return

def main():
    """
    Main function to parse command line arguments and call the create_gif function.
    """
    parser = argparse.ArgumentParser(description="Create an animated GIF from a directory of images.")
    parser.add_argument("image_path", help="Path to the directory containing the images.")
    parser.add_argument("output_dir", help="Path to save the output GIF file (e.g., output.gif).")
    parser.add_argument("-d", "--duration", type=int, default=100,
                        help="Duration of each frame in the GIF in milliseconds (default: 100).")

    args = parser.parse_args()
    create_gif(args.image_path, args.output_dir, args.duration)

if __name__ == "__main__":
    main()