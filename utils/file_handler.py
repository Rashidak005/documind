import os
import sys
import shutil
import uuid

# Add the parent DocuMind/ folder to Python's search path
# so we can import config.py which lives there, not in utils/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our settings from config.py
import config


def is_supported_file(file_path):
    """
    Checks whether the given file's extension is one of the types
    our system knows how to read (defined in config.SUPPORTED_EXTENSIONS).

    Returns True if supported, False if not.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension in config.SUPPORTED_EXTENSIONS:
        return True
    else:
        return False


def generate_unique_filename(original_filename):
    """
    Takes an original filename (e.g. "report.pdf") and returns a new
    filename with a short unique ID inserted before the extension
    (e.g. "report_a1b2c3d4.pdf").

    This prevents two different uploads with the same name from
    overwriting each other in the uploaded_docs folder.
    """

    # Split "report.pdf" into name="report" and extension=".pdf"
    name, extension = os.path.splitext(original_filename)

    # Generate a short random unique ID (first 8 characters of a UUID)
    unique_id = uuid.uuid4().hex[:8]

    # Build the new filename: name_uniqueid.extension
    new_filename = f"{name}_{unique_id}{extension}"

    return new_filename


def save_uploaded_file(temp_file_path):
    """
    Takes the temporary file path given by Gradio after an upload,
    validates it, and copies it into our permanent uploaded_docs/
    folder using a unique filename.

    Returns the full path to the newly saved permanent file.
    Raises a ValueError if the file type isn't supported.
    """

    # First, make sure this is a file type we actually know how to read
    if not is_supported_file(temp_file_path):
        extension = os.path.splitext(temp_file_path)[1]
        raise ValueError(f"Unsupported file type: {extension}")

    # Get just the filename part (e.g. "report.pdf") from the full temp path
    original_filename = os.path.basename(temp_file_path)

    # Generate a safe unique name so we never overwrite another file
    unique_filename = generate_unique_filename(original_filename)

    # Build the full destination path inside uploaded_docs/
    destination_path = os.path.join(config.UPLOAD_PATH, unique_filename)

    # Actually copy the file from its temp location to our permanent folder
    shutil.copy(temp_file_path, destination_path)

    print(f"Saved uploaded file to: {destination_path}")

    return destination_path


def list_uploaded_documents():
    """
    Looks inside the uploaded_docs/ folder and returns a list of
    filenames currently stored there.

    Returns an empty list if no documents have been uploaded yet.
    """

    # os.listdir gives us every item (files and folders) inside UPLOAD_PATH
    all_items = os.listdir(config.UPLOAD_PATH)

    # Filter to keep only actual files (skip subfolders, if any ever appear)
    files_only = []
    for item in all_items:
        full_path = os.path.join(config.UPLOAD_PATH, item)
        if os.path.isfile(full_path):
            files_only.append(item)

    return files_only


def delete_uploaded_document(filename):
    """
    Deletes a specific file from the uploaded_docs/ folder by filename.

    Returns True if the file was deleted successfully.
    Returns False if the file didn't exist in the first place.
    """

    # Build the full path to the file we want to delete
    file_path = os.path.join(config.UPLOAD_PATH, filename)

    # Only attempt deletion if the file actually exists
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted: {filename}")
        return True
    else:
        print(f"File not found, nothing to delete: {filename}")
        return False


# --- Quick Test ---
if __name__ == "__main__":
    print(is_supported_file("myfile.pdf"))
    print(is_supported_file("myfile.exe"))
    print(generate_unique_filename("report.pdf"))

    # Save a file
    saved_path = save_uploaded_file("../yourfile.pdf")
    print("File saved at:", saved_path)

    # List what's currently in uploaded_docs/
    print("Currently uploaded documents:", list_uploaded_documents())

    # Delete the file we just saved (using just its filename, not full path)
    saved_filename = os.path.basename(saved_path)
    delete_uploaded_document(saved_filename)

    # Confirm it's gone
    print("After deletion:", list_uploaded_documents())