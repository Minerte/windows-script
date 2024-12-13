import os
import requests
import tkinter as tk
import zipfile
from tkinter import filedialog
from zipfile import ZipFile

def list_options(options, prompt):
    """Helper funtion to display list of options"""
    print(prompt)
    for i, option in enumerate(options, 1):
        print (f"{i}. {option}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Please enter a valid number.")

def download_modpack(server_url, modpack, destination):
    """Fetch the modpack zip file from the Apache2 server."""
    if modpack == "Fabric-0.16.0-1.20.1":
        url = f"{server_url}/{modpack}/Fabric.zip"
    elif modpack == "Forge-47.3.0-1.20.1":
        url = f"{server_url}/{modpack}/Forge.zip"
    else:
        print("Failed to fetch file or could not determine the URL")
        return
    
    try:
        print(f"Downloading {modpack} from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filepath = os.path.join(destination, f"{modpack}.zip")
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"{modpack} has been downloaded to {filepath}")
    except requests.RequestException as e:
        print(f"Failed to download {modpack}: {e}")

def choose_directory():
    """Open a directory picker dialog and return the selected path."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    appdata_path = os.getenv("APPDATA")
    print("Please select a directory to save the modpack:")
    selected_directory = filedialog.askdirectory(title="Select Destination Directory", initialdir=appdata_path)
    if selected_directory:
        return selected_directory
    else:
        print("No directory selected. Exiting.")
        exit()

def choose_zip_and_extract():
    """Let the user choose a zip file and extract its contents."""
    # Initialize the Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    appdata_path = os.getenv("APPDATA")

    # Let the user choose the zip file
    zip_file = filedialog.askopenfilename(
        title="Select a Zip File",
        filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
    )
    
    if zip_file:  # If the user selects a file
        # Ask the user where to extract the contents
        extract_to = os.path.join(os.path.dirname(zip_file), "mods")
        
        if extract_to:  # If a destination folder is chosen
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
                print(f"Contents extracted to: {extract_to}")

                os.remove(zip_file)
                print(f"Zip file {zip_file} has been deleted")

            except zipfile.BadZipFile:
                print(f"The file {zip_file} is not a valid zip file.")
        else:
            print("No destination folder selected. Exiting.")
    else:
        print("No zip file selected. Exiting.")

def main():
    # Configuration
    modpacks = ["Fabric-0.16.0-1.20.1", "Forge-47.3.0-1.20.1"]
    launchers = ["MinecraftDefault", "PrismLauncher"]
    server_url = "http://192.168.1.215:8080"  # Change this to your Apache2 server's URL

    print("Welcome to the Minecraft Modpack Downloader!")

    # User selects a modpack
    selected_modpack = list_options(modpacks, "Choose a modpack to download:")

    # User selects a launcher
    selected_launcher = list_options(launchers, "Choose a launcher:")

    # Determine the destination directory based on the launcher
    destination = choose_directory()

    # Ensure the directory exists
    os.makedirs(destination, exist_ok=True)

    # Download the modpack
    download_modpack(server_url, selected_modpack, destination)

    # Extract file
    choose_zip_and_extract()

if __name__ == "__main__":
    main()
