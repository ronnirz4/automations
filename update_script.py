import os
import shutil
import zipfile

# Exclusion rules per component
EXCLUDE_FILES = {
    "UI": {"", "", ""},
    "API": {"", "secrets."},
    "Storage": {""},
    "Identity": {""},
    "SignalRHub": {""},
    # Add more if needed
}

def main():
    base_dir = input("Enter the full path to the directory: ").strip()
    component = input("Enter the component name (e.g. UI, API): ").strip()

    original_path = os.path.join(base_dir, component)
    backup_path = f"{original_path}-backup"
    zip_path = None

    # Find the zip file dynamically
    for filename in os.listdir(base_dir):
        if filename.startswith(component) and filename.endswith(".zip"):
            zip_path = os.path.join(base_dir, filename)
            break

    if not os.path.isdir(original_path):
        print(f"Original folder '{component}' not found.")
        return

    if not zip_path or not os.path.isfile(zip_path):
        print(f"No matching zip file found for '{component}'.")
        return

    # Backup the original folder
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)
    shutil.copytree(original_path, backup_path)
    print(f"Backed up '{component}' to '{component}-backup'.")

    # Extract the zip
    extract_path = os.path.join(base_dir, f"{component}-extracted")
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Determine excluded files
    excluded_files = EXCLUDE_FILES.get(component, set())

    # Copy files over, skipping excluded ones
    for root, _, files in os.walk(extract_path):
        for file in files:
            if file in excluded_files:
                continue

            rel_path = os.path.relpath(os.path.join(root, file), extract_path)
            dest_path = os.path.join(original_path, rel_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(os.path.join(root, file), dest_path)

    print(f"Deployment of '{component}' complete. Excluded files: {excluded_files}")

if __name__ == "__main__":
    main()
