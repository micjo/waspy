from pathlib import Path

path = Path(".")
files = [file for file in sorted(path.iterdir()) if file.is_file()]



for file in files:
    file_parts = file.name.split("_")
    base_file = "_".join(file_parts[0:3])
    print(base_file)

