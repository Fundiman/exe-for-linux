#!/usr/bin/env python3
import os
import subprocess

def detect_linux_distribution():
    try:
        # Attempt to read /etc/os-release to determine Linux distribution
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.split("=")[1].strip().strip('"')
    except FileNotFoundError:
        pass  # Handle the case where /etc/os-release is not found or inaccessible
    return None

def is_wine_installed():
    try:
        subprocess.run(["wine", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_wine_ubuntu():
    try:
        subprocess.run(["sudo", "dpkg", "--add-architecture", "i386"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["sudo", "apt-get", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "wine"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_wine_fedora():
    try:
        subprocess.run(["sudo", "dnf", "install", "-y", "wine"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_wine_arch():
    try:
        subprocess.run(["sudo", "pacman", "-Sy", "--noconfirm", "wine"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_wine_silently():
    distro = detect_linux_distribution()
    if not distro:
        return False

    if distro == "ubuntu" or distro == "debian":
        return install_wine_ubuntu()
    elif distro == "fedora":
        return install_wine_fedora()
    elif distro == "arch":
        return install_wine_arch()
    else:
        return False

def main():
    # Paths
    home_dir = os.path.expanduser("~")
    script_dir = os.path.join(home_dir, "bin")
    script_path = os.path.join(script_dir, "exe-for-linux.py")
    desktop_entry_dir = os.path.join(home_dir, ".local", "share", "applications")
    desktop_entry_path = os.path.join(desktop_entry_dir, "exe-for-linux.desktop")

    # Check if Wine is installed
    if not is_wine_installed():
        # Install Wine silently
        install_wine_silently()

    # Create the script directory if it doesn't exist
    os.makedirs(script_dir, exist_ok=True)

    # Create the Python script (exe-for-linux.py)
    script_content = """#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: exe-for-linux.py <path_to_exe_file>")
        sys.exit(1)

    exe_path = sys.argv[1]

    if not os.path.isfile(exe_path):
        print(f"File not found: {exe_path}")
        sys.exit(1)

    try:
        subprocess.run(["wine", exe_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {exe_path} with wine. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""

    # Write the script content to the file
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    # Make the script executable
    os.chmod(script_path, 0o755)

    # Create the .desktop entry directory if it doesn't exist
    os.makedirs(desktop_entry_dir, exist_ok=True)

    # Create the .desktop file (exe-for-linux.desktop)
    desktop_entry_content = f"""[Desktop Entry]
Name=EXE for Linux
Exec={script_path} %f
Type=Application
Terminal=true
MimeType=application/x-ms-dos-executable
"""

    # Write the .desktop entry content to the file
    with open(desktop_entry_path, "w") as desktop_entry_file:
        desktop_entry_file.write(desktop_entry_content)

    # Update the MIME database
    subprocess.run(["update-desktop-database", desktop_entry_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print("Setup complete. You can now open .exe files with exe-for-linux by double-clicking them.")

if __name__ == "__main__":
    main()

