import os
import shutil
import zipfile
from datetime import datetime
from rich.console import Console

# Exclusion rules per component
EXCLUDE_FILES = {
    "UI": {"", "", ""},
    "API": {"", ""},
    "Storage": {""},
    "Identity": {""},
    "SignalRHub": {""},
    # Add more if needed
}

# Initialize the rich console
console = Console()


def main():
    # Prompt for input
    base_dir = input("Enter the full path to the directory: ").strip()
    component = input("Enter the component name (e.g. UI, API): ").strip()

    original_path = os.path.join(base_dir, component)
    backup_path = f"{original_path}-{datetime.now().strftime('%Y%m%d')}"
    zip_path = None

    # Find the zip file dynamically
    for filename in os.listdir(base_dir):
        if filename.startswith(component) and filename.endswith(".zip"):
            zip_path = os.path.join(base_dir, filename)
            break

    if not os.path.isdir(original_path):
        console.print(f"[bold red]Original folder '{component}' not found![/bold red]")
        return

    if not zip_path or not os.path.isfile(zip_path):
        console.print(f"[bold red]No matching zip file found for '{component}'.[/bold red]")
        return

    # Backup the original folder
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)
    shutil.copytree(original_path, backup_path)
    console.print(f"[bold green]Backed up '{component}' to '{backup_path}'[/bold green]")

    # Extract the zip
    extract_path = os.path.join(base_dir, f"{component}-extracted")
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Determine excluded files
    excluded_files = EXCLUDE_FILES.get(component, set())

    # Copy files over, skipping excluded ones
    total_files = 0
    skipped_files = 0

    for root, _, files in os.walk(extract_path):
        for file in files:
            total_files += 1
            if file in excluded_files:
                skipped_files += 1
                continue

            rel_path = os.path.relpath(os.path.join(root, file), extract_path)
            dest_path = os.path.join(original_path, rel_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(os.path.join(root, file), dest_path)

    # Summary output
    console.print(f"[bold cyan]Deployment of '{component}' complete![/bold cyan]")
    console.print(f"Total files processed: [bold yellow]{total_files}[/bold yellow]")
    console.print(f"Files skipped due to exclusion: [bold magenta]{skipped_files}[/bold magenta]")

    # Excluded files list
    if excluded_files:
        console.print(f"[bold blue]Excluded files for '{component}':[/bold blue]")
        for file in excluded_files:
            console.print(f"- {file}")


if __name__ == "__main__":
    main()
