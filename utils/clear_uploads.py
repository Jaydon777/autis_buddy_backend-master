import os
import shutil

def clear_uploads_directory(uploads_path, keep_latest=5):
    """
    Delete older files in the uploads directory, keeping only the latest ones.
    
    Args:
        uploads_path (str): Path to the uploads directory
        keep_latest (int): Number of latest files to keep (default: 5)
    """
    if not os.path.exists(uploads_path):
        print(f"Uploads directory does not exist: {uploads_path}")
        return

    # Get all files in the directory
    files = []
    for item in os.listdir(uploads_path):
        item_path = os.path.join(uploads_path, item)
        if os.path.isfile(item_path):
            files.append(item_path)
    
    # Check if we need to clean up (more files than the keep limit)
    if len(files) <= keep_latest:
        print(f"No cleanup needed. {len(files)} files found, keeping up to {keep_latest}.")
        return
        
    # Sort files by modification time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)
    
    # Keep the latest N files, delete the rest
    files_to_delete = files[keep_latest:]
    
    print(f"Keeping {keep_latest} newest files, deleting {len(files_to_delete)} older files.")
    
    # Delete the older files
    for file_path in files_to_delete:
        try:
            os.unlink(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    
    # Also clean up any directories in the uploads folder
    for item in os.listdir(uploads_path):
        item_path = os.path.join(uploads_path, item)
        if os.path.isdir(item_path):
            try:
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item_path}")
            except Exception as e:
                print(f"Error deleting directory {item_path}: {e}")