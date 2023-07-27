import glob
import subprocess
import os

def create_vidlist_txt_file():
		files = glob.glob(os.path.join("./output/", '*.mp4'))
		files.sort()

		# Convert file paths to lowercase and write the list of files to a text file with absolute paths and double quotes
		with open("vidlist.txt", "w") as f:
				for file in files:
						lowercase_path = os.path.abspath(file).lower()
						f.write(f"file '{lowercase_path}'\n")

def combine_mp4_files(output_file):
		output_file = "./output_concatenated_video.mp4"

		# Run the FFMPEG command using subprocess with the -safe option
		try:
				subprocess.call(f"ffmpeg -f concat -safe 0 -i vidlist.txt -c copy {output_file}", shell=True)
				print(f"mp4 files successfully combined into {output_file}.")
		except subprocess.CalledProcessError as e:
				print(f"Error occurred while combining mp4 files: {e}")


if __name__ == "__main__":
		create_vidlist_txt_file()
		combine_mp4_files()
