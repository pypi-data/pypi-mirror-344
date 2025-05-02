import os
import platform
import subprocess
import logging
from pathlib import Path

log = logging.getLogger(__name__)

def run_preparation(state):
    """
    Performs environment preparation specific to PowerPoint.
    Opens a specific template file located on the user's desktop.
    """
    system_platform = platform.system()
    log.info(f"PowerPoint preparation: Starting on {system_platform} platform...")

    try:
        # Determine the desktop path based on platform
        if system_platform == "Windows":
            try:
                # Get the Windows username from environment variables
                username = os.environ.get("USERNAME", "")
                if not username:
                    log.error("Could not determine Windows username from environment")
                    return
                
                log.info(f"Using Windows username: {username}")
                # Construct path to user's desktop
                desktop_path = Path(f"C:/Users/{username}/Desktop")
                
                # Check if path exists
                if not desktop_path.exists():
                    log.error(f"Desktop path not found at: {desktop_path}")
                    # Try alternative locations if needed
                    alt_path = Path(f"C:/Documents and Settings/{username}/Desktop")
                    if alt_path.exists():
                        desktop_path = alt_path
                        log.info(f"Using alternative desktop path: {desktop_path}")
                    else:
                        log.error("Failed to find user's desktop directory")
                        return
                
            except Exception as e:
                log.error(f"Error determining Windows user desktop: {e}", exc_info=True)
                return
                
        elif system_platform == "Darwin":  # macOS
            # On macOS we can use a simpler approach
            desktop_path = Path.home() / "Desktop"
            log.info(f"Using macOS desktop path: {desktop_path}")
        else:
            log.warning(f"Platform {system_platform} not specifically supported. Attempting generic approach.")
            desktop_path = Path.home() / "Desktop"
            
        # Construct path to template file
        template_file = desktop_path / "template.txt"
        log.info(f"Looking for template file at: {template_file}")

        if not template_file.exists():
            log.error(f"Template file not found at: {template_file}")
            return

        # Open the file with appropriate command based on platform
        if system_platform == "Windows":
            log.info(f"Attempting to open {template_file} with PowerPoint on Windows...")
            try:
                # Use start command on Windows
                cmd = ['cmd', '/c', 'start', 'powerpnt', str(template_file)]
                result = subprocess.run(cmd, check=False, capture_output=True, text=True)
                
                if result.returncode == 0:
                    log.info(f"Successfully launched PowerPoint with {template_file}")
                else:
                    log.error(f"Error opening PowerPoint: {result.stderr.strip()}")
            except Exception as e:
                log.error(f"Exception opening PowerPoint on Windows: {e}", exc_info=True)
                
        elif system_platform == "Darwin":  # macOS
            log.info(f"Attempting to open {template_file} with PowerPoint on macOS...")
            cmd = ['open', '-a', 'Microsoft PowerPoint', str(template_file)]
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            
            if result.returncode == 0:
                log.info(f"Successfully opened {template_file} with PowerPoint.")
            else:
                log.error(f"Failed to open {template_file} with PowerPoint. Error: {result.stderr.strip()}")
        else:
            log.warning(f"Opening PowerPoint on {system_platform} not explicitly supported")

    except Exception as e:
        log.error(f"An unexpected error occurred during PowerPoint preparation: {e}", exc_info=True) 