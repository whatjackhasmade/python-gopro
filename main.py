import glob
import os
import time
import subprocess
from open_gopro import WiredGoPro
from rich.console import Console

def combine_mp4_files(input_files, output_file):
    # Convert filenames to lowercase with .mp4 extension
    input_files = [file.lower() for file in input_files]

    # Prepare the FFMPEG command with re-encoding
    ffmpeg_cmd = ["ffmpeg"]
    for file in input_files:
        ffmpeg_cmd.extend(["-i", file])
    ffmpeg_cmd.extend(["-filter_complex", f"concat=n={len(input_files)}:v=1:a=1", "-c:v", "libx264", "-c:a", "aac", output_file])

    # Run the FFMPEG command using subprocess
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"MP4 files successfully combined into {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while combining MP4 files: {e}")

# rich consoler printer
console = Console()

serial_number = "C3441327598451"
last_4_characters_of_serial_number = serial_number[-4:]

# Connect to the camera
gopro = WiredGoPro(last_4_characters_of_serial_number)
gopro.open()
gopro.http_command.set_turbo_mode(mode=True)

# Empty out the output directory of any .mp4 files
files = glob.glob('./output/*.MP4')
for f in files:
	os.remove(f)

# Download all of the files from the camera
media_list = [x["n"] for x in gopro.http_command.get_media_list().flatten]
for file in media_list:
			output = f"./output/{file}"

			# Get the media info
			info = gopro.http_command.get_media_info(file=file)
			cre = info["cre"]

			console.print(f"••• Downloading the media {file}")
			gopro.http_command.download_file(camera_file=file, local_file=output)
			console.print(f"✓ File has been downloaded to {output}")

# Wait for 5 seconds
console.print("Waiting for 5 seconds...")
time.sleep(5)

files = glob.glob('./output/*.MP4')
# get files as an array
files.sort()

combine_mp4_files(files, f"./output/Final.MP4")