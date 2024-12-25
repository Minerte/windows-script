import os
import shutil
import requests
import zipfile
import subprocess
from pathlib import Path

FORGE_VERSION = "47.3.0"
MC_VERSION = "1.20.1"
FORGE_INSTALLER_URL = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{MC_VERSION}-{FORGE_VERSION}/forge-{MC_VERSION}-{FORGE_VERSION}-installer.jar"
FABRIC_INSTALLER_URL = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.jar"

# Modpack download links
MODPACKS = {
    "Forge-47.3.0-1.20.1": "URL",
    "Fabric-0.16.0-1.20.1": "URL",
}

def list_options(options, prompt):
    """Helper to list and choose an option."""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def download_file(url, destination):
    """Download a file from a URL."""
    try:
        print(f"Downloading from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded file to: {destination}")
    except Exception as e:
        print(f"Failed to download: {e}")
        exit()

def check_forge(destination):
    """Ensure Forge is installed."""
    forge_installer_path = os.path.join(destination, "forge_installer.jar")
    print("Checking Forge installation...")
    forge_installed = os.path.exists(os.path.join(destination, "libraries", f"net/minecraftforge/forge/{MC_VERSION}-{FORGE_VERSION}"))

    if not forge_installed:
        print(f"Forge version {FORGE_VERSION} not detected. Installing Forge...")
        download_file(FORGE_INSTALLER_URL, forge_installer_path)
        try:
            subprocess.run(["java", "-jar", forge_installer_path], check=True)
            print("Forge installation complete!")
        except Exception as e:
            print(f"Error while installing Forge: {e}")
            exit()
    else:
        print(f"Forge version {FORGE_VERSION} is already installed.")

def check_fabric(destination):
    """Ensure Fabric is installed."""
    fabric_installer_path = os.path.join(destination, "fabric_installer.jar")
    print("Checking Fabric installation...")
    fabric_installed = os.path.exists(os.path.join(destination, "versions", MC_VERSION, f"fabric-{MC_VERSION}"))

    if not fabric_installed:
        print(f"Fabric loader for Minecraft {MC_VERSION} not detected. Installing Fabric...")
        download_file(FABRIC_INSTALLER_URL, fabric_installer_path)
        try:
            subprocess.run(["java", "-jar", fabric_installer_path, "client", "-dir", destination], check=True)
            print("Fabric installation complete!")
        except Exception as e:
            print(f"Error while installing Fabric: {e}")
            exit()
    else:
        print(f"Fabric loader for Minecraft {MC_VERSION} is already installed.")

def prompt_replace_folder(folder):
    """Ask user whether to replace or keep a folder."""
    if os.path.exists(folder):
        while True:
            choice = input(f"The folder '{folder}' already exists. Do you want to replace it? (yes/no): ").lower()
            if choice == "yes":
                print("Removing existing folder...")
                for root, dirs, files in os.walk(folder, topdown=False):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
                print("Folder cleared.")
                return True
            elif choice == "no":
                print("Keeping the existing folder.")
                return False
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
    return True

def choose_modpack(destination):
    """Let user choose and download a modpack."""
    selected_modpack = list_options(list(MODPACKS.keys()), "Choose a modpack to download:")
    modpack_url = MODPACKS[selected_modpack]
    zip_path = os.path.join(destination, f"{selected_modpack}.zip")

    download_file(modpack_url, zip_path)
    
    # Extract modpack
    print("Extracting modpack...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(destination, "mods"))
    print(f"Modpack extracted to {os.path.join(destination, 'mods')}")
    os.remove(zip_path)

def move_config_folder(mods_dir, appdata_path, is_prism_launcher, instance_name=None):
    """Move the config folder from mods to the correct directory."""
    config_folder_in_mods = os.path.join(mods_dir, "config")

    if os.path.exists(config_folder_in_mods):
        # Ask the user if they want to move the config folder
        choice = input(f"A 'config' folder exists in the '{mods_dir}' folder. Do you want to move it to the correct directory? (yes/no): ").lower()
        if choice == "yes":
            # Determine the destination of the config folder
            if is_prism_launcher:
                config_folder = os.path.join(appdata_path, "PrismLauncher", "instances", instance_name, "minecraft", "config")
            else:
                config_folder = os.path.join(appdata_path, ".minecraft", "config")

            # Remove the existing config folder in the destination if necessary
            if os.path.exists(config_folder):
                print(f"Removing existing config folder from {config_folder}")
                shutil.rmtree(config_folder)

            # Move the config folder from mods to the target directory
            print(f"Moving config folder to {config_folder}")
            shutil.move(config_folder_in_mods, config_folder)
            print(f"Config folder moved successfully.")
        else:
            print("Config folder move skipped.")
    else:
        print("No config folder found in mods.")

def setup_prism_launcher():
    """Handle PrismLauncher setup."""
    appdata_path = os.getenv("APPDATA")
    instances_path = os.path.join(appdata_path, "PrismLauncher", "instances")

    print("Select the PrismLauncher instance:")
    instances = [d for d in os.listdir(instances_path) if os.path.isdir(os.path.join(instances_path, d))]
    if not instances:
        print("No instances found in PrismLauncher. Exiting.")
        exit()

    selected_instance = list_options(instances, "Choose an instance:")
    destination = os.path.join(instances_path, selected_instance, "minecraft")
    mods_dir = os.path.join(destination, "mods")
    
    if prompt_replace_folder(mods_dir):
        os.makedirs(mods_dir, exist_ok=True)
        print(f"Mods will be installed to: {mods_dir}")
        choose_modpack(destination)

    # Move the config folder from mods to the appropriate place
    move_config_folder(mods_dir, appdata_path, is_prism_launcher=True, instance_name=selected_instance)

def setup_minecraft_default():
    """Handle Minecraft default setup."""
    appdata_path = os.getenv("APPDATA")
    minecraft_path = os.path.join(appdata_path, ".minecraft")
    
    print("Select a mod loader:")
    loaders = ["Forge", "Fabric"]
    selected_loader = list_options(loaders, "Choose a mod loader:")
    
    if selected_loader == "Forge":
        check_forge(minecraft_path)
    elif selected_loader == "Fabric":
        check_fabric(minecraft_path)
    else:
        print("Invalid choice. Exiting.")
        return
    
    mods_dir = os.path.join(minecraft_path, "mods")
    if prompt_replace_folder(mods_dir):
        os.makedirs(mods_dir, exist_ok=True)
        print(f"Mods will be installed to: {mods_dir}")
        choose_modpack(minecraft_path)

    # Move the config folder from mods to the appropriate place
    move_config_folder(mods_dir, appdata_path, is_prism_launcher=False)

def main():
    print("Welcome to the Minecraft Modpack Installer!")
    print("Please be ware that the mods folder and config folder will be replaced")
    print("If you want to backup, you need to do it manually!")
    launchers = ["MinecraftDefault", "PrismLauncher"]
    choice = list_options(launchers, "Choose your launcher:")
    
    if choice == "MinecraftDefault":
        setup_minecraft_default()
    elif choice == "PrismLauncher":
        setup_prism_launcher()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
