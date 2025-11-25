import yt_dlp
import os
import sys

# --- FIX: Custom Logger Class to satisfy yt-dlp requirements ---
# yt-dlp expects an object with .debug(), .warning(), and .error() methods.
# This class provides those methods, resolving the "'function' object has no attribute 'debug'" error.
class YtDlpLogger:
    """A minimal custom logger for yt-dlp."""
    def debug(self, msg):
        # Suppress most internal debug messages to keep the output clean
        if msg.startswith('[debug]'):
            pass 
        else:
            print(msg)

    def warning(self, msg):
        print(f"⚠️ WARNING: {msg}")

    def error(self, msg):
        # Print error messages clearly
        print(f"❌ ERROR: {msg}")

# --- Main download function ---
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
    ydl_opts = {
        # Template for the filename: saves to {output_path}/VideoID.ext
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        
        # Inject the instance of our custom logger class here
        'logger': YtDlpLogger(), 
        
        # Prioritize the highest quality video stream available
        'format': 'best',
        
        # Do not overwrite the file if it already exists
        'noplaylist': True,
        'skip_download': False,
        
        # Mimic a mobile user agent for potentially better stream access
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://www.tiktok.com/',
        },
        
        # We manage output via the custom logger
        'quiet': False, 
        
        'postprocessors': [{
            'key': 'FFmpegMetadata',
            'add_metadata': False,
        }],
    }

    try:
        print(f"\nAttempting to download video from: {url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info and download the video
            info_dict = ydl.extract_info(url, download=True)
            
            # Confirming the final path
            downloaded_files = info_dict.get('requested_downloads', [])
            if downloaded_files:
                final_filepath = downloaded_files[0]
                print(f"\n✅ Successfully downloaded video to: {final_filepath}")
            else:
                 print(f"\n✅ Download completed for video ID: {info_dict.get('id')}. Check {output_path} directory.")

    except yt_dlp.DownloadError as e:
        print(f"\n❌ A download error occurred: {e}", file=sys.stderr)
        print("Please ensure the URL is correct and the video is publicly accessible.", file=sys.stderr)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}", file=sys.stderr)
        # Re-raise the exception to help Render show the full traceback
        raise e


if __name__ == "__main__":
    # Example URL for testing
    tiktok_url = "https://www.tiktok.com/@tiktok/video/7300729731454170369"
    
    if len(sys.argv) > 1:
        tiktok_url = sys.argv[1]

    download_tiktok_video(tiktok_url, output_path="tiktok_downloads")

