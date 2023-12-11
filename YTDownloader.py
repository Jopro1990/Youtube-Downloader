import os
from pytube import YouTube
from colorama import Fore, Style
import subprocess

def download_youtube_video():
    max_retries = 3

    try:
        # Prompt user for YouTube video URL
        video_url = input("Enter the YouTube video URL: ")

        # Create a YouTube object
        yt = YouTube(video_url)

        # Get streams with desired resolutions and file format
        resolutions = ['720p', '1080p', '1440p', '2160p']
        video_streams = yt.streams.filter(file_extension='webm', resolution=resolutions)

        # Print available resolutions
        print("Available Resolutions:")
        for i, stream in enumerate(video_streams):
            print(f"{i + 1}. {stream.resolution}")

        # Prompt user to choose resolution
        choice = int(input("\nEnter the number corresponding to the desired resolution: ")) - 1
        selected_stream = video_streams[choice]

        # Set output path to the current working directory
        output_path = os.getcwd()

        retry_count = 0
        while retry_count < max_retries:
            try:
                # Print video details for the selected stream
                print(f"\nSelected Resolution: {selected_stream.resolution}")
                print(f"File size: {round(selected_stream.filesize / (1024 * 1024), 2)} MB")

                # Download the video
                selected_stream.download(output_path)

                print(Fore.GREEN + "\nDownload completed successfully!" + Style.RESET_ALL)
                break  # Break out of the loop if download is successful

            except Exception as e:
                retry_count += 1
                print(Fore.YELLOW + f"Retry {retry_count}/{max_retries}: {str(e)}" + Style.RESET_ALL)

        if retry_count == max_retries:
            print(Fore.RED + "Failed to download after multiple retries. Please try again later." + Style.RESET_ALL)

        # Download the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path, filename=f'{yt.title}_audio.webm')

        print(Fore.GREEN + "\nAudio download completed successfully!" + Style.RESET_ALL)

        # Combine video and audio using FFmpeg
        video_path = os.path.join(output_path, f'{yt.title}.webm')
        audio_path = os.path.join(output_path, f'{yt.title}_audio.webm')
        output_path = os.path.join(output_path, f'{yt.title}.mp4')

        try:
            subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, '-c', 'copy', output_path], check=True)
            print("Video and audio combined successfully.")

            # Delete video and audio files
            os.remove(video_path)
            os.remove(audio_path)

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while combining video and audio: {e}")

    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)

if __name__ == "__main__":
    download_youtube_video()

    # Wait for the user to press Enter before closing the command prompt
    input("Press Enter to close the command prompt.")
