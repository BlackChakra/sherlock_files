import os

def find_files(search_folder, keyword):
    matches = []
    # os.walk() lets you loop through a folder and all its subfolders
    for root, dirs, files in os.walk(search_folder):
        for file in files:
            if keyword.lower() in file.lower():  # Case-insensitive match
                full_path = os.path.join(root, file)
                matches.append(full_path)
    return matches

# Example usage:
results = find_files("C:\\Users\\oaksl\\Documents", "resume")

# Print what it finds
for path in results:
    print(path)
