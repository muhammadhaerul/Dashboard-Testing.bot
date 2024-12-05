import os

def get_txt_sorted_files(directory, extension=".txt"):
    """
    Get a sorted list of files from a directory with a specific extension.
    """
    return sorted([f for f in os.listdir(directory) if f.endswith(extension)])
