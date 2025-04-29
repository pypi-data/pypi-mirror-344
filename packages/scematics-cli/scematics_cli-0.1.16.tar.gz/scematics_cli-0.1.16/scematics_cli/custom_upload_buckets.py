import os
import shutil
from PIL import Image
import requests
from requests.exceptions import RequestException
import time
import uuid
from pathlib import Path
from tqdm import tqdm
import math
import cv2
import json
import argparse
import boto3
from botocore.client import Config
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings


# Supported video file types
VIDEO_EXTENSIONS = {
    '.mp4': 'application/octet-stream',
    '.mov': 'application/octet-stream',
    '.avi': 'application/octet-stream',
    '.mkv': 'application/octet-stream',
    '.hevc': 'application/octet-stream'
}

def is_video_file(file_path):
    """Check if the file is a video based on extension"""
    if hasattr(file_path, 'suffix'):
        extension = file_path.suffix.lower()
    else:
        extension = os.path.splitext(file_path)[1].lower() if isinstance(file_path, str) else ""
        
    return extension in VIDEO_EXTENSIONS.keys()

def is_json_file(file_path):
    """Check if the file is a JSON file"""
    if hasattr(file_path, 'suffix'):
        extension = file_path.suffix.lower()
    else:
        extension = os.path.splitext(file_path)[1].lower() if isinstance(file_path, str) else ""
        
    return extension.lower() == '.json'

def convert_rgba_to_rgb(image):
    """Convert RGBA image to RGB with white background"""
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'RGBA':
            background.paste(image, mask=image.split()[3])
        elif image.mode == 'LA':
            background.paste(image, mask=image.split()[1])
        else:
            background.paste(image, mask=image.info['transparency'])
        return background
    return image.convert('RGB')

def cleanup_thumbnails(folder_path):
    """Clean up thumbnail folder"""
    thumbnail_folder = os.path.join(folder_path, "_thumbnail")
    try:
        if os.path.exists(thumbnail_folder):
            shutil.rmtree(thumbnail_folder)
            print(f"Cleaned up thumbnail folder")
    except Exception as e:
        print(f"Warning: Could not clean up thumbnail folder: {str(e)}")

def generate_video_thumbnail(video_path, thumbnail_path):
    """Generate thumbnail from the first frame of a video"""
    try:
        # Open the video file
        video = cv2.VideoCapture(str(video_path))
        
        # Check if video opened successfully
        if not video.isOpened():
            print(f"Could not open video {video_path}")
            return False
        
        # Read the first frame
        success, frame = video.read()
        if not success:
            print(f"Could not read first frame from {video_path}")
            return False
        
        # Convert BGR to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create PIL Image from the frame
        img = Image.fromarray(frame_rgb)
        
        # Resize for thumbnail
        img.thumbnail((200, 200))
        
        # Save thumbnail
        img.save(thumbnail_path, "JPEG", quality=85)
        
        # Release video
        video.release()
        
        return True
    except Exception as e:
        print(f"Error generating thumbnail for {video_path}: {str(e)}")
        return False

def get_video_dimensions(video_path):
    """Get video width and height"""
    try:
        video = cv2.VideoCapture(str(video_path))
        if not video.isOpened():
            return 0, 0
            
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        video.release()
        return width, height
    except Exception as e:
        print(f"Error getting video dimensions for {video_path}: {str(e)}")
        return 0, 0

def get_file_size(file_path):
    """Get file size in human-readable format"""
    try:
        size_bytes = os.path.getsize(file_path)
        # Convert to human-readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    except Exception as e:
        return "Unknown size"

def retry_request(func, pbar=None, retries=10, delay=2, *args, **kwargs):
    """Retry function execution with progress tracking - 10 retries"""
    for attempt in range(retries):
        try:
            if pbar:
                pbar.set_description(f"Attempt {attempt + 1}/{retries}...")
            result = func(*args, **kwargs)
            if result:
                return result
            # If function returns False, also retry
            if pbar:
                pbar.set_description(f"Attempt {attempt + 1} returned False, retrying...")
            if attempt < retries - 1:
                time.sleep(delay)
        except Exception as e:
            if pbar:
                pbar.set_description(f"Attempt {attempt + 1} failed with error: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
    
    # If we get here, all attempts failed
    if pbar:
        pbar.set_description(f"Failed after {retries} attempts")
    return None


import builtins
import datetime


def register_existing_s3_files(base_url, token, user_id, project_id, folder_path):
    """Register existing S3 files to a project with live logging to a file."""

    # Set up the log file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{timestamp}_uploads_log.txt"
    os.makedirs('logs', exist_ok=True)
    log_filepath = os.path.join('logs', log_filename)

    # Create a custom print function that logs to both terminal and file
    original_print = builtins.print

    def tee_print(*args, **kwargs):
        # Print to terminal
        original_print(*args, **kwargs)
        # Append to the log file
        with open(log_filepath, "a", encoding="utf-8") as f:
            f.write(" ".join(map(str, args)) + "\n")

    # Override print
    builtins.print = tee_print

    try:
        # Set up API endpoints
        list_objects_endpoint = f"{base_url}/settings/cloud_storage/list-folder-buckets/{user_id}?prefix={folder_path}"
        session_endpoint = f"{base_url}/session/"
        get_bucket_endpoint = f"{base_url}/settings/cloud_storage/{user_id}"
        register_endpoint = f"{base_url}/uploads/entry-datas/bucket?media_type=VIDEO"
        confirm_media_endpoint = f"{base_url}/uploads/confirm-upload/{{}}"
        batch_confirm_endpoint = f"{base_url}/uploads/batch-confirm/{{}}"

        headers = {'Authorization': f'Bearer {token}'}

        # Check primary bucket
        session_response = requests.get(session_endpoint, headers=headers)
        session_response.raise_for_status()
        session_data = session_response.json()

        if "access" in session_data and "cloud_storage_id" in session_data["access"]:
            current_bucket_id = session_data["access"]["cloud_storage_id"]
            if int(current_bucket_id) != int(user_id):
                print(f"Primary bucket needs to be changed from {current_bucket_id} to {user_id}")
                print(f"Log saved to {log_filepath}")
                builtins.print = original_print
                return False

        # Get bucket credentials
        response = requests.get(get_bucket_endpoint, headers=headers)
        response.raise_for_status()
        bucket_data = response.json()

        if not bucket_data or not isinstance(bucket_data, dict):
            print(f"Invalid bucket data response: {bucket_data}")
            print(f"Log saved to {log_filepath}")
            builtins.print = original_print
            return False

        bucket_name = bucket_data.get('resource_name')
        access_key = bucket_data.get('credentials', {}).get("access_key_id")
        secret_key = bucket_data.get('credentials', {}).get("secret_access_key")
        region = bucket_data.get('region')
        endpoint = bucket_data.get('endpoint_url')
        provider = bucket_data.get('provider')

        if not bucket_name or not access_key or not secret_key:
            print(f"Missing bucket credentials in response: {bucket_data}")
            print(f"Log saved to {log_filepath}")
            builtins.print = original_print
            return False

        # List objects in the bucket
        response = requests.get(list_objects_endpoint, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        s3_files = []
        if isinstance(response_data, dict):
            if 'data' in response_data:
                s3_files = response_data['data']
            else:
                for key, value in response_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        s3_files = value
                        print(f"Found files under '{key}' key: {len(s3_files)}")
                        break
        elif isinstance(response_data, list):
            s3_files = response_data

        if not s3_files and isinstance(response_data, dict):
            if 'key' in response_data or 'Key' in response_data:
                s3_files = [response_data]
                print(f"Using the entire response as a single file entry")

        if not s3_files:
            print(f"No files found in S3 with prefix: {folder_path}")
            print(f"Log saved to {log_filepath}")
            builtins.print = original_print
            return False

        if isinstance(s3_files, list) and len(s3_files) > 0:
            first_item = s3_files[0]
            if isinstance(first_item, str):
                print(f"API returned string entries, converting format...")
                s3_files = [{'key': item, 'bucket_name': bucket_name} for item in s3_files]

        # Group files by parent folder
        file_groups = {}
        for file_info in s3_files:
            if not isinstance(file_info, dict):
                continue

            if 'key' not in file_info and 'Key' in file_info:
                file_info['key'] = file_info['Key']

            if 'key' not in file_info:
                continue

            key = file_info['key']
            parent_folder = os.path.dirname(key)

            if parent_folder not in file_groups:
                file_groups[parent_folder] = []

            file_groups[parent_folder].append(file_info)
            
        # Process files by folder
        items_to_register = []
        
        print(f"Using bucket: {bucket_name}")
        
        if provider == "AZURE_BLOB_STORAGE":
            # Build Azure URL manually
            account_name = access_key  # assuming access_key is actually account_name
            account_key = secret_key
            if not endpoint:
                endpoint = f"https://{account_name}.blob.core.windows.net"

            s3_client = BlobServiceClient(
                account_url=endpoint,
                credential={"account_name": account_name, "account_key": account_key}
            )
        else:
            # Create S3 client with the retrieved credentials
            s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
                endpoint_url=endpoint,
                config=Config(signature_version='s3v4')
            )
        
        # Process each folder
        folder_pbar = tqdm(file_groups.items(), total=len(file_groups), desc="Processing folders")
        for folder, files in folder_pbar:
            folder_pbar.set_description(f"Processing folder: {folder}")
            
            # Find video files
            video_files = [f for f in files if any(f['key'].lower().endswith(ext) for ext in VIDEO_EXTENSIONS.keys())]
            
            # Find metadata files (JSON)
            json_files = [f for f in files if f['key'].lower().endswith('.json')]
            
            if video_files:
                print(f"Folder {folder}: Found {len(video_files)} videos and {len(json_files)} JSON files")
            
            # Process each video file
            for video_file in video_files:
                video_key = video_file['key']
                file_name = os.path.basename(video_key)
                base_name = os.path.splitext(file_name)[0]
                
                # Default dimensions in case we can't determine them
                width, height = 1280, 720
                
                # Start a progress bar for this specific file
                file_pbar = tqdm(total=100, desc=f"Processing {file_name}", leave=True)
                file_pbar.update(10)  # Mark start of download
                
                # Create thumbnail path with UUID to avoid name conflicts
                thumbnail_folder = os.path.join(folder, "_thumbnail")
                thumbnail_uuid = str(uuid.uuid4())[:8]  # Use first 8 chars of UUID
                thumbnail_key = f"{thumbnail_folder}/{base_name}_{thumbnail_uuid}_thumbnail.png"
                
                # Find matching JSON file - in this case, ANY JSON in the same folder will do
                matching_json = None
                if len(json_files) > 0:
                    # Take the first JSON file in this folder
                    matching_json = json_files[0]['key']
                
                # If no JSON files in this folder, check parent folders
                if not matching_json:
                    parent_parts = folder.split('/')
                    # Try parent folder
                    if len(parent_parts) > 1:
                        parent_folder = '/'.join(parent_parts[:-1])
                        parent_json_files = [f for f in s3_files if f['key'].lower().endswith('.json') and 
                                            os.path.dirname(f['key']) == parent_folder]
                        
                        if parent_json_files:
                            matching_json = parent_json_files[0]['key']
                
                # Download temporary file for dimensions and thumbnail
                temp_file = os.path.join('/tmp', file_name)
                
                try:
                    # Download video file
                    print(f"Downloading: {file_name}")
                    try:
                        if provider == "AZURE_BLOB_STORAGE":
                            
                            # Build the connection string
                            connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
                            
                            # Initialize the BlobServiceClient with the connection string
                            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
                            
                            # Access the container and blob using the blob_service_client
                            container_client = blob_service_client.get_container_client(bucket_name)
                            blob_client = container_client.get_blob_client(video_key)
                            
                            # Download the blob to the temporary file
                            with open(temp_file, "wb") as f:
                                download_stream = blob_client.download_blob()
                                f.write(download_stream.readall())
                        else:
                            # Download the file from S3 if not Azure
                            s3_client.download_file(bucket_name, video_key, temp_file)

                        # Process the downloaded file
                        file_size = get_file_size(temp_file)
                        file_pbar.update(30)  # Update progress after download (30%)
                        file_pbar.set_description(f"Processing {file_name} ({file_size})")
                    except Exception as download_err:
                        print(f"Error downloading video: {str(download_err)}")
                        file_pbar.update(30)  # 40% progress even if download fails
                        
                        # Even if download fails, try to create the thumbnail folder
                        try:
                            s3_client.put_object(Bucket=bucket_name, Key=f"{thumbnail_folder}/")
                        except:
                            pass
                            
                        # Create dummy thumbnail with UUID for registration
                        dummy_thumbnail = os.path.join('/tmp', f"{base_name}_{thumbnail_uuid}_thumbnail.png")
                        img = Image.new('RGB', (200, 200), color=(100, 100, 100))
                        img.save(dummy_thumbnail, "PNG")
                        
                        # Try to upload the dummy thumbnail
                        try:
                            if provider == "AZURE_BLOB_STORAGE":
                                container_client = blob_service_client.get_container_client(bucket_name)
                                blob_client = container_client.get_blob_client(thumbnail_key)
                                with open(dummy_thumbnail, "rb") as data:
                                    blob_client.upload_blob(
                                        data, 
                                        overwrite=True,
                                        content_settings=ContentSettings(content_type='image/png')
                                    )
                            else:
                                s3_client.upload_file(
                                    dummy_thumbnail,
                                    bucket_name,
                                    thumbnail_key,
                                    ExtraArgs={'ContentType': 'image/png'}
                                )
                            os.remove(dummy_thumbnail)
                        except:
                            # If upload fails, that's ok - we still have a valid thumbnail_key
                            pass
                            
                        file_pbar.update(60)  # Complete the progress bar
                        file_pbar.close()
                        
                        # Add to items for registration with thumbnail key
                        item = {
                            "key": video_key,
                            "thumbnail_key": thumbnail_key,
                            "file_name": file_name,
                            "width": width,
                            "height": height
                        }
                        
                        # Add metadata
                        if matching_json:
                            item["metadata"] = matching_json
                        else:
                            item["metadata"] = video_key
                            
                        items_to_register.append(item)
                        continue  # Skip the rest of the loop for this file
                    
                    # Get video dimensions
                    width, height = get_video_dimensions(temp_file)
                    file_pbar.update(10)  # 50% progress after getting dimensions
                    
                    # Generate thumbnail
                    thumbnail_temp = os.path.join('/tmp', f"{base_name}_{thumbnail_uuid}_thumbnail.png")
                    generate_video_thumbnail(temp_file, thumbnail_temp)
                    file_pbar.update(20)  # 70% progress after generating thumbnail
                    
                    # Create thumbnail folder if it doesn't exist
                    try:
                        try:
                            s3_client.head_object(Bucket=bucket_name, Key=f"{thumbnail_folder}/")
                        except:
                            # Silently create folder if it doesn't exist
                            s3_client.put_object(Bucket=bucket_name, Key=f"{thumbnail_folder}/")
                    except Exception as folder_err:
                        # Continue even if we can't create the folder - S3 is hierarchical anyway
                        pass
                    
                    # Upload thumbnail to S3
                    try:
                        if provider == "AZURE_BLOB_STORAGE":
                            container_client = blob_service_client.get_container_client(bucket_name)
                            blob_client = container_client.get_blob_client(thumbnail_key)
                            with open(thumbnail_temp, "rb") as data:
                                blob_client.upload_blob(
                                    data, 
                                    overwrite=True,
                                    content_settings=ContentSettings(content_type='image/png')
                                )
                        else:
                            s3_client.upload_file(
                                thumbnail_temp,
                                bucket_name,
                                thumbnail_key,
                                ExtraArgs={'ContentType': 'image/png'}
                            )
                        file_pbar.update(20)  # 90% progress after uploading thumbnail
                    except Exception as upload_err:
                        print(f"Failed to upload thumbnail: {str(upload_err)}")
                        # Continue with processing despite thumbnail upload failure
                        file_pbar.update(20)  # 90% progress even if upload fails
                    
                    # Clean up temp files
                    os.remove(temp_file)
                    os.remove(thumbnail_temp)
                    file_pbar.update(10)  # 100% progress when complete
                    
                except Exception as e:
                    print(f"Error processing video {file_name}: {str(e)}")
                    # If we get here, we still need to create a registration item
                    file_pbar.update(70)  # Update progress to 100%
                
                file_pbar.close()
                
                # Add to items for registration
                item = {
                    "key": video_key,
                    "thumbnail_key": thumbnail_key,
                    "file_name": file_name,
                    "width": width,
                    "height": height
                }
                
                # Simply use the first JSON file found in the folder as metadata
                if matching_json:
                    item["metadata"] = matching_json
                else:
                    # If no JSON found, use the video path itself as metadata
                    item["metadata"] = video_key
                
                items_to_register.append(item)
            
        # If we have items, send them to the API
        result = False
        if items_to_register:
            # Prepare payload
            payload = {
                "project_id": project_id,
                "items": items_to_register
            }
            
            # Log payload for debugging
            print(f"Registering {len(items_to_register)} items with API...")
            
            try:
                # Send registration request with progress bar
                api_pbar = tqdm(total=100, desc="API Registration", leave=True)
                api_pbar.update(10)  # Mark start of API registration
                
                response = requests.post(
                    register_endpoint, 
                    json=payload, 
                    headers=headers
                )
                api_pbar.update(40)  # 50% progress after request
                response.raise_for_status()
                
                # Process response
                result = response.json()
                batch_id = result.get('batch_id')
                media_items = result.get('items', [])
                api_pbar.update(10)  # 60% progress after processing response
                
                if batch_id and media_items:
                    print(f"Successfully registered {len(media_items)} items with batch ID: {batch_id}")
                    
                    # Confirm each media item one by one
                    confirmation_pbar = tqdm(media_items, desc="Confirming", leave=True)
                    
                    for item in confirmation_pbar:
                        media_id = item.get('media_id')
                        file_name = item.get('file_name')
                        
                        if not media_id:
                            continue
                        
                        confirmation_pbar.set_description(f"Confirming: {file_name}")
                        
                        # Confirm this individual media item
                        try:
                            confirm_url = confirm_media_endpoint.format(media_id)
                            confirm_response = requests.post(confirm_url, headers=headers)
                            confirm_response.raise_for_status()
                            time.sleep(30)
                            # Don't print anything for successful confirmation to keep output clean
                        except Exception as e:
                            print(f"Failed to confirm {file_name}: {str(e)}")
                            
                    # Finally, confirm the batch
                    print(f"Confirming batch: {batch_id}")
                    try:
                        batch_url = batch_confirm_endpoint.format(batch_id)
                        batch_response = requests.post(batch_url, headers=headers)
                        batch_response.raise_for_status()
                        print(f"Successfully confirmed batch: {batch_id}")
                        api_pbar.update(40)  # 100% complete
                        result = True
                    except Exception as e:
                        print(f"Failed to confirm batch {batch_id}: {str(e)}")
                        api_pbar.update(40)  # Complete the progress bar anyway
                        result = False
                else:
                    print(f"Registration completed but no batch ID or media items returned")
                    api_pbar.update(40)  # Complete the progress bar anyway
                    result = False
            
            except Exception as e:
                print(f"API request failed: {str(e)}")
                if hasattr(e, 'response'):
                    print(f"Response: {e.response.text}")
                result = False
        else:
            print(f"No items to register")
            result = False

        # Restore original print before returning
        builtins.print = original_print
        print(f"Log saved to {log_filepath}")
        return result
        
    except Exception as e:
        # Restore original print
        builtins.print = original_print
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"Log saved to {log_filepath}")
        return False
    
def process_s3_folder_files(base_url, token, user_id, project_id, folder_path, local_folder=None):
    """Legacy method for processing S3 files - implemented for backward compatibility"""
    print(f"Using legacy method for processing S3 files")
    
    try:
        # Clean up thumbnails in local folder if provided
        if local_folder:
            cleanup_thumbnails(local_folder)
            
        # This is a wrapper around the new method to maintain backward compatibility
        return register_existing_s3_files(base_url, token, user_id, project_id, folder_path)
    except Exception as e:
        print(f"Error in legacy processing method: {str(e)}")
        return False

def main():
    """Main function to handle command line arguments"""
    import datetime
    import os
    import sys
    
    # Create a log list to store output
    log_entries = []
    
    # Create a custom print function that logs to both terminal and our log list
    original_print = print
    
    def tee_print(*args, **kwargs):
        # Print to terminal normally
        original_print(*args, **kwargs)
        # Also add to our log list
        log_entries.append(" ".join(map(str, args)))
    
    # Replace print with our version
    print = tee_print
    
    try:
        parser = argparse.ArgumentParser(description='S3 Video Registration Script')
        
        # Required arguments
        parser.add_argument('--user_id', type=str, help='User ID for S3 access')
        parser.add_argument('--project_id', type=str, help='Project ID to register videos to')
        parser.add_argument('--bucket_folder_path', type=str, help='S3 folder path in bucket')
        parser.add_argument('--bucket_id', type=str, help='Bucket ID')
        
        # Optional arguments
        parser.add_argument('--base_url', type=str, default='http://127.0.0.1:8000', help='Base API URL')
        parser.add_argument('--token', type=str, help='API Authentication token')
        parser.add_argument('--local_folder', type=str, help='Local folder path (for thumbnail generation)')
        parser.add_argument('--use_new_api', action='store_true', help='Use the new bucket registration API')
        
        args = parser.parse_args()
        
        # Run the processing with selected API
        if args.use_new_api:
            print("Using new bucket registration API...")
            result = register_existing_s3_files(
                args.base_url, 
                args.token, 
                args.user_id,
                args.project_id,
                args.bucket_folder_path
            )
        else:
            print("Using legacy registration API...")
            result = process_s3_folder_files(
                args.base_url, 
                args.token, 
                args.user_id,
                args.project_id,
                args.bucket_folder_path, 
                args.local_folder
            )
        
        if result:
            print("Processing completed successfully!")
            exit_code = 0
        else:
            print("Processing encountered errors.")
            exit_code = 1
        
        # After processing completes, save the log file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{timestamp}_uploads_log.txt"
        
        # Write log entries to file
        with open(log_filename, "w") as f:
            f.write("\n".join(log_entries))
        
        # Print with original print to avoid capturing this in the log
        original_print(f"Log saved to {log_filename}")
        
        # Restore original print
        print = original_print
        
        return exit_code
        
    except Exception as e:
        # Restore original print
        print = original_print
        print(f"An error occurred: {str(e)}")
        
        # Try to save log even on error
        if log_entries:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"{timestamp}_uploads_log.txt"
            
            with open(log_filename, "w") as f:
                f.write("\n".join(log_entries))
            
            print(f"Error log saved to {log_filename}")
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)