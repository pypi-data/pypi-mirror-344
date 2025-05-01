import os
import logging
import subprocess # Use subprocess for better control
import shlex # For safer command splitting if needed

log = logging.getLogger('system') # Optional: configure logging

# --- Standardized Command Tree ---
def get_command_tree():
    """Return the command tree structure for system commands."""
    return {
        "run": None # Expects a shell command string as value
    }

# --- Standardized Descriptions ---
def get_descriptions():
    """Return the description tree for system commands."""
    return {
        "": "Execute system-level commands",
        "run": {
            "": "Execute a shell command on the underlying OS",
            "_options": ["<shell_command>"] # Hint for completion
        }
    }

# --- Handle Function ---
def handle(args, username, hostname):
    """Handle system commands"""
    prompt = f"{username}/{hostname}@vMark-node> "
    if not args:
        return f"{prompt}Usage: system run <shell_command>"

    if args[0] == "run":
        if len(args) < 2:
            return f"{prompt}Usage: system run <shell_command>"

        # Join the rest of the arguments to form the shell command
        shell_command = " ".join(args[1:])
        log.info(f"Executing system command: '{shell_command}'")

        # Security Warning: Executing arbitrary shell commands is dangerous.
        # Ensure this feature is appropriately secured or restricted in a production environment.
        try:
            # Using subprocess is generally safer than os.popen/os.system
            # Capture stdout and stderr
            result = subprocess.run(shell_command, shell=True, check=False, # Set check=True to raise error on non-zero exit
                                    capture_output=True, text=True, timeout=30) # Add timeout

            output = f"Exit Code: {result.returncode}\n"
            if result.stdout:
                output += f"--- stdout ---\n{result.stdout.strip()}\n"
            if result.stderr:
                output += f"--- stderr ---\n{result.stderr.strip()}\n"

            log.debug(f"Command '{shell_command}' finished with code {result.returncode}")
            return f"{prompt}Command output:\n{output.strip()}"

        except subprocess.TimeoutExpired:
            log.warning(f"Command '{shell_command}' timed out.")
            return f"{prompt}Error: Command timed out after 30 seconds."
        except Exception as e:
            log.exception(f"Error executing command '{shell_command}': {e}")
            return f"{prompt}Error executing command: {e}"
    else:
        return f"{prompt}Unknown system command: {args[0]}"