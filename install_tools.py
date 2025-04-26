from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress
import subprocess

console = Console()

apps = {
    "7zip": ("7zip.7zip", "7-Zip"),
    "notepadpp": ("Notepad++.Notepad++", "Notepad++"),
    "vscode": ("Microsoft.VisualStudioCode", "VS Code"),
    "git": ("Git.Git", "Git"),
    "teamviewer": ("TeamViewer.TeamViewer", "TeamViewer"),
    "postman": ("Postman.Postman", "Postman"),
    "azurecli": ("Microsoft.AzureCLI", "Azure CLI"),
    "docker": ("Docker.DockerDesktop", "Docker Desktop"),
    "python": ("Python.Python.3", "Python"),
    "fork": ("Fork.Fork", "Fork (Git GUI)"),
    "nodejs": ("OpenJS.NodeJS.LTS", "Node.js LTS"),
    "visualstudio": ("Microsoft.VisualStudio.2022.Community", "Visual Studio 2022 Community"),
    "terraform": ("Hashicorp.Terraform", "Terraform"),
    "terragrunt": ("Gruntwork.Terragrunt", "Terragrunt"),
    "awscli": ("Amazon.AWSCLI", "AWS CLI"),
    "chocolatey": ("Chocolatey.Choco", "Chocolatey"),
}

roles = {
    "devops": ["git", "vscode", "notepadpp", "7zip", "teamviewer", "postman", "azurecli", "docker", "python", "fork", "terraform", "terragrunt", "awscli", "chocolatey"],
    "developer": ["nodejs", "git", "fork", "visualstudio", "notepadpp", "postman", "7zip"]
}

def is_installed(app_id):
    result = subprocess.run(["winget", "list"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return result.stdout and app_id.lower() in result.stdout.lower()

# Step 1: Choose Role
role = Prompt.ask("\nChoose your role", choices=["devops", "developer", "custom"], default="custom")

if role == "custom":
    # Show full table
    table = Table(title="🧰 All Available Tools", title_style="bold green")
    table.add_column("Key", justify="left", style="cyan")
    table.add_column("Name", style="magenta")

    for key, (_, name) in apps.items():
        table.add_row(key, name)
    console.print(table)

    selection = Prompt.ask("\nEnter tools to install (comma-separated keys or 'all')").strip().lower()
    selected_keys = list(apps.keys()) if selection == "all" else [
        x.strip() for x in selection.split(",") if x.strip() in apps
    ]
else:
    selected_keys = roles[role]
    # Show role's default tools
    console.print(f"\n🛠 [bold blue]{role.capitalize()} tools:[/bold blue]")
    for key in selected_keys:
        console.print(f"• {apps[key][1]}")

    answer = Prompt.ask("\nInstall all these tools?", choices=["yes", "no"], default="yes")
    if answer == "no":
        table = Table(title="🎯 Pick Specific Tools", title_style="bold yellow")
        table.add_column("Key", justify="left", style="cyan")
        table.add_column("Name", style="magenta")
        for key in selected_keys:
            table.add_row(key, apps[key][1])
        console.print(table)
        selection = Prompt.ask("\nEnter tools to install (comma-separated keys)").strip().lower()
        selected_keys = [x.strip() for x in selection.split(",") if x.strip() in selected_keys]

# Step 2: Install with checks
if not selected_keys:
    console.print("\n⚠️ [bold red]No valid selections made. Exiting.[/bold red]")
    exit()

console.print("\n🔧 Starting installation...\n", style="bold green")

with Progress() as progress:
    task = progress.add_task("[cyan]Installing tools...", total=len(selected_keys))

    for key in selected_keys:
        app_id, name = apps[key]
        if is_installed(app_id):
            console.print(f"✅ [green]{name}[/green] is already installed.\n")
        else:
            console.print(f"🔄 Installing [yellow]{name}[/yellow]...")
            result = subprocess.run([
                "winget", "install", "--id", app_id,
                "--silent", "--accept-package-agreements", "--accept-source-agreements"
            ])
            if result.returncode == 0:
                console.print(f"✅ [green]{name} installed successfully![/green]\n")
            else:
                console.print(f"❌ [red]Failed to install {name}.[/red]\n")
        progress.update(task, advance=1)

console.print("\n✅ [bold green]Done! Press Enter to exit...[/bold green]")
input()
