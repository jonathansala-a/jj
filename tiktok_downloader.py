import yt_dlp
import os
import sys

# --- Prerequisites ---
# To run this script, you need to install the yt-dlp library:
# pip install yt-dlp

def download_tiktok_video(url: str, output_path: str = "downloads") -> None:
   """
   Downloads a TikTok video using yt-dlp.

   Args:
       url (str): The full URL of the TikTok video.
       output_path (str): The directory where the video should be saved.
                          Defaults to 'downloads'.
   """
   # 1. Ensure the output directory exists
   if not os.path.exists(output_path):
       os.makedirs(output_path)
       print(f"Created output directory: {output_path}")

   # 2. Define yt-dlp options
   # These options are crucial for customizing the download behavior
   ydl_opts = {
       # Template for the filename: saves to {output_path}/TikTok_Video_ID.mp4
       'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
       
       # Verbose progress tracking
       'logger': yt_dlp.postprocessor.common.PostProcessor.to_screen,
       
       # Prioritize the highest quality video stream available
       'format': 'best',
       
       # Do not overwrite the file if it already exists
       'noplaylist': True,
       'skip_download': False,
       
       # User agent to mimic a mobile browser, which sometimes helps access better streams
       'http_headers': {
           'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
           'Referer': 'https://www.tiktok.com/',
       },
       
       # Suppress standard output messages from yt-dlp unless there is an error
       'quiet': False,
       
       # Configure the name of the final downloaded file
       'postprocessors': [{
           'key': 'FFmpegMetadata',
           'add_metadata': False,
       }],
   }

   try:
       print(f"\nAttempting to download video from: {url}")
       
       # Use a context manager for the YD_dlp object
       with yt_dlp.YoutubeDL(ydl_opts) as ydl:
           # Extract info and download the video
           info_dict = ydl.extract_info(url, download=True)
           
           # The actual path of the downloaded file (only after successful download)
           # We get the filename from the downloaded_files key in the info_dict if it exists
           downloaded_files = info_dict.get('requested_downloads', [])
           if downloaded_files:
               final_filepath = downloaded_files[0]
               print(f"\n✅ Successfully downloaded video to: {final_filepath}")
           else:
                print("\n✅ Download completed, but could not retrieve final file path.")

   except yt_dlp.DownloadError as e:
       print(f"\n❌ A download error occurred: {e}", file=sys.stderr)
       print("Please ensure the URL is correct and the video is publicly accessible.", file=sys.stderr)
   except Exception as e:
       print(f"\n❌ An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
   # Example usage: Replace this URL with the actual TikTok link you want to download.
   # Note: To get a video *without* a watermark, yt-dlp attempts to find the best source,
   # but TikTok sometimes makes the watermark-free stream difficult or impossible to access.
   # In most cases, it finds a high-quality stream that is often watermark-free or
   # has minimal watermark presence.
   tiktok_url = "https://www.tiktok.com/@tiktok/video/7300729731454170369"
   
   # You can pass the URL as a command-line argument for a more flexible script
   if len(sys.argv) > 1:
       tiktok_url = sys.argv[1]

   # The video will be saved in a subfolder named 'downloads'
   download_tiktok_video(tiktok_url, output_path="tiktok_downloads")
