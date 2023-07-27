import glob
import os
import time
import subprocess
from open_gopro import WiredGoPro
from rich.console import Console

console = Console()
serial_number = "C3441327598451"
last_4_characters_of_serial_number = serial_number[-4:]
gopro = WiredGoPro(last_4_characters_of_serial_number)

def create_vidlist_txt_file():
		files = glob.glob(os.path.join("./output/", '*.mp4'))
		files.sort()

		# Convert file paths to lowercase and write the list of files to a text file with absolute paths and double quotes
		with open("vidlist.txt", "w") as f:
				for file in files:
						lowercase_path = os.path.abspath(file).lower()
						f.write(f"file '{lowercase_path}'\n")

def combine_mp4_files():
		output_file = "./output/video.mp4"

		# Run the FFMPEG command using subprocess with the -safe option
		try:
				subprocess.call(f"ffmpeg -f concat -safe 0 -i vidlist.txt -c copy {output_file}", shell=True)
				print(f"mp4 files successfully combined into {output_file}.")
		except subprocess.CalledProcessError as e:
				print(f"Error occurred while combining mp4 files: {e}")

# Empty out the output directory of any .mp4 files
files = glob.glob('./backup/*.mp4')
for f in files:
	os.remove(f)

# Connect to the camera
gopro.open()
gopro.http_command.set_turbo_mode(mode=True)

open_gopro_api_version = gopro.http_command.get_open_gopro_api_version()
webcam_version = gopro.http_command.get_webcam_version()


# Log the camera commands
console.print(dir(gopro.http_command))

# Download all of the files from the camera
media_list = [x["n"] for x in gopro.http_command.get_media_list().flatten]
for file in media_list:
			output = f"./backup/{file}"
			output = output.replace("MP4", "mp4")

			# Get the media info
			info = gopro.http_command.get_media_info(file=file)
			cre = info["cre"]

			console.print(f"••• Downloading the media {file}")
			gopro.http_command.download_file(camera_file=file, local_file=output)
			console.print(f"✓ File has been downloaded to {output}")
			gopro.http_command.delete_media(camera_file=file)
			console.print(f"✓ File has been deleted from the camera")

# Wait for 2 seconds
console.print("Waiting for 2 seconds...")
time.sleep(2)

create_vidlist_txt_file()
combine_mp4_files()