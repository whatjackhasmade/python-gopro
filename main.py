from open_gopro import WiredGoPro
from rich.console import Console

# rich consoler printer
console = Console()

serial_number = "C3441327598451"
last_4_characters_of_serial_number = serial_number[-4:]

# Connect to the camera
gopro = WiredGoPro(last_4_characters_of_serial_number)
gopro.open()

# Download all of the files from the camera
media_list = [x["n"] for x in gopro.http_command.get_media_list().flatten]
for file in media_list:
			output = f"./output/{file}"

			# Get the media info
			info = gopro.http_command.get_media_info(file=file)
			console.print(f"Downloading the media {file}")
			gopro.http_command.download_file(camera_file=file, local_file=output)
			console.print(f"Success!! :smiley: File has been downloaded to {output}")