import logging
import subprocess
import sys
import os
import pathlib
from facefusion import wording
from tqdm import tqdm

logger = logging.getLogger(__name__)

def test_image_to_image() -> None:
	commands = [ sys.executable, 'run.py', '-s', '.assets/examples/source.jpg', '-t', '.assets/examples/target.jpg', '-o', '.assets/examples/output/target.jpg', '--headless' ]
	run = subprocess.run(commands, stdout = subprocess.PIPE)

	logger.info(run.stdout.decode())


def test_image_to_video() -> None:
	commands = [ sys.executable, 'run.py', '-s', '.assets/examples/source.jpg', '-t', '.assets/examples/target-1080p.mp4', '-o', '.assets/examples', '--trim-frame-end', '10', '--headless' ]
	run = subprocess.run(commands, stdout = subprocess.PIPE)

	assert run.returncode == 0
	assert wording.get('processing_video_succeed') in run.stdout.decode()


def rename_exts():
	folders = ["D:/p/s", "D:/p/s-o"]
	extensions = (".webp", ".jpeg")

	for folder in folders:
		for root, dirs, files in os.walk(folder):
			for file in files:
				if file.lower().endswith(extensions):
					old_path = os.path.join(root, file)
					new_name = os.path.splitext(file)[0] + ".jpg"
					new_path = os.path.join(root, new_name)
					os.rename(old_path, new_path)
					logger.info(f"Renamed: {old_path} -> {new_path}")

	logger.info("Renaming complete.")


def filter_tests(folder):
    src = "D:/swap/f/_vc/3.jpg"
    target_folders = ["D:/p/s", "D:/p/s-o"]
    
    for tar in target_folders:
        jpg_files = [f for root, dirs, files in os.walk(tar) for f in files if f.lower().endswith('.jpg')]
        total_files = len(jpg_files)
        
        logger.info(f"\nProcessing folder: {tar}")
        for i, file in enumerate(jpg_files, 1):
            tar_path = os.path.join(tar, file).replace('\\', '/')
            out = f'D:/p/tests_filter/{file}'
            predict(src, tar_path, out)
            logger.info(f"Processed {i} of {total_files} items in {tar} \n")

        logger.info(f"Completed processing folder: {tar}")


def rename_images(folder_path):
    # Get a list of all .jpg files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
    
    # Sort files to ensure proper order
    files.sort()

    # Add a temporary prefix to avoid name collisions
    for file_name in files:
        temp_name = f"x_{file_name}"
        os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, temp_name))
    
    # Get the list again with the new names
    files = [f for f in os.listdir(folder_path) if f.startswith("x_")]

    # Rename each file sequentially from 1.jpg to n.jpg
    for index, file_name in enumerate(files, start=1):
        new_name = f"{index}.jpg"
        os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_name))


def predict(s, t, o):
	# s = "D:/swap/f/_vc/3.jpg"
	# t = "D:/p/s/332lf0.jpg"
	# o = "D:/swap/ff-out/output.jpg"
	commands = [ sys.executable, 'run.py', '-s', s, '-t', t, '-o', o, '--headless' ]

	run = subprocess.run(commands, stdout = subprocess.PIPE)
	# logger.info(run.stdout.decode())


def predict_batch(src_folder, test_folders):
    main_test_folder, sub_test_folder = test_folders 
    # main_test_folder, sub_test_folder = 'D:/p/small_test', 'D:/p/small_test/weird'
    main_folder_name = os.path.basename(main_test_folder)
	
    test_folders = [main_test_folder, sub_test_folder]

    image_files = [f for f in os.listdir(src_folder) if f.endswith(('.jpg', '.png'))]

    for file_name in tqdm(image_files, desc=f"Processing {src_folder}/{file_name} in {test_folder}", unit="test files"):
        # Full path of the file
        s = os.path.join(src_folder, file_name)
        
        # Extract the file name without the extension
        file_base_name = os.path.splitext(file_name)[0]
        
        for test_folder in test_folders:
            t = test_folder
            test_folder_name = os.path.basename(test_folder)
            
            if "weird" in test_folder_name.lower():
                o = os.path.join(src_folder, f"{file_base_name}_{main_folder_name}", "weird")
            else:
                o = os.path.join(src_folder, f"{file_base_name}_{main_folder_name}")
            os.makedirs(o, exist_ok=True)
            
            predict(s, t, o)


'''
def predict_batch(folder):
    """
    base_dir = "D:/batches"

	subfolders = [os.path.join(base_dir, subfolder_name) for subfolder_name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, subfolder_name))]

	for subfolder_path in subfolders:
		predict_batch(subfolder_path)

    """
    main_test_folder, sub_test_folder = 'D:/p/tests', 'D:/p/tests/weird'
    # main_test_folder, sub_test_folder = 'D:/p/small_test', 'D:/p/small_test/weird'
    main_folder_name = os.path.basename(main_test_folder)
	
    test_folders = [main_test_folder, sub_test_folder]

    image_files = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.png'))]

    for file_name in image_files:
        # Full path of the file
        s = os.path.join(folder, file_name)
        
        # Extract the file name without the extension
        file_base_name = os.path.splitext(file_name)[0]
        
        for test_folder in test_folders:
            # Loop through all test images in the test folder with progress bar
            test_images = [f for f in os.listdir(test_folder) if f.endswith(('.jpg', '.png', '.mp4'))]
            for test_file_name in tqdm(test_images, desc=f"Processing {folder}/{file_name} in {test_folder}", unit="test files"):
                # Full path to the test image
                t = os.path.join(test_folder, test_file_name)
                
                # Determine the output directory
                test_folder_name = os.path.basename(test_folder)
                
                if "weird" in test_folder_name.lower():
                    output_directory = os.path.join(folder, f"{file_base_name}_{main_folder_name}", "weird")
                else:
                    output_directory = os.path.join(folder, f"{file_base_name}_{main_folder_name}")
                
                # Ensure the output directory exists
                os.makedirs(output_directory, exist_ok=True)
                
                # Full path for the output file
                # o = os.path.join(output_directory, f"{file_base_name}_{os.path.splitext(test_file_name)[0]}.jpg")
                if test_file_name.endswith('.mp4'):
                    o = os.path.join(output_directory, f"{file_base_name}_{os.path.splitext(test_file_name)[0]}.mp4")
                else:
                    o = os.path.join(output_directory, f"{file_base_name}_{os.path.splitext(test_file_name)[0]}.jpg")
				
                # Run the predict function
                predict(s, t, o)
'''


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
	# main()
	# filter_tests()
	# base_dir = "D:/to_test"
	base_dir = "D:/batches"
	# test_folders = ['D:/p/tests', 'D:/p/tests/weird']
	test_folders = ['D:/p/small_test', 'D:/p/small_test/weird']
	subfolders = [os.path.join(base_dir, subfolder_name) for subfolder_name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, subfolder_name))]

	for subfolder_path in subfolders:
		rename_images(subfolder_path)
		predict_batch(subfolder_path, test_folders)
