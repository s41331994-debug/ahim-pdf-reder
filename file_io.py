import os

def get_file_name(file_path):
    """Extract filename from path."""
    return os.path.basename(file_path)

def check_extension(file_path, extensions=None):
    """Check if file has allowed extension."""
    if extensions is None:
        extensions = ['.pdf']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in extensions
