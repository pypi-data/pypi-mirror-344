from pyroute2 import IPDB
import subprocess
import re
import ipaddress  # Ensure this is imported once at the top
import logging # Add logging if needed

log = logging.getLogger('config') # Optional: configure logging

# Define descriptions with proper _options for parameters
descriptions = {
    "interface": {
        "": "Configure network interfaces",
        "<ifname>": {
            "": "Interface name",
            "mtu": {
                "": "Set MTU size",
                "_options": ["<1-10000>"],  # Common MTU values
            },
            "speed": {
                "": "Set interface speed",
                "_options": ["10M", "100M", "1G", "10G"],
            },
            "status": {
                "": "Set interface status",
                "_options": ["up", "down"],
            },
            "auto-nego": {
                "": "Enable or disable auto-negotiation",
                "_options": ["on", "off"],
            },
            "duplex": {
                "": "Set duplex mode",
                "_options": ["half", "full"],
            },
        }
    },
    "new-interface": {
        "": "Create a new interface",
        "<ifname>": {
            "": "New interface name",
            "parent-interface": {
                "": "Parent interface name (REQUIRED)",
                "_options": ["<parent-ifname>"],
            },
            "cvlan-id": {
                "": "Customer VLAN ID (C-TAG)",
                "_options": ["<1-4000>"],
            },
            "svlan-id": {
                "": "Service VLAN ID (S-TAG)",
                "_options": ["<1-4000>"],
            },
            "mtu": {
                "": "Set MTU size",
                "_options": ["<1000-10000>"],
            },
            "status": {
                "": "Set interface status",
                "_options": ["up", "down"],
            },
            "ipv4address": {
                "": "Set IPv4 address (REQUIRED)",
                "_options": ["<x.x.x.x>"],
                "format": "Enter IPv4 address in dotted decimal format (e.g., 192.168.1.1)"
            },
            "netmask": {
                "": "Set network mask (REQUIRED)",
                "_options": ["</xx>", "<x.x.x.x>"],
                "format": "Enter CIDR format (e.g., /24) or dotted decimal (e.g., 255.255.255.0)"
            },
        }
    },
    "delete-interface": {
        "": "Delete a network interface",
        "<ifname>": {
            "": "Name of interface to delete"
        }
    }
}

# --- Helper to get interface names ---
def _get_interface_names():
    """Returns a list of current interface names."""
    try:
        with IPDB() as ipdb:
            # Filter out loopback, docker, etc. if desired, or keep all
            return [
                str(name) for name in ipdb.interfaces.keys()
                if isinstance(name, str) # and not name.startswith('lo') and not name.startswith('docker')
            ]
    except Exception as e:
        log.error(f"Error getting interface names: {e}")
        return [] # Handle errors gracefully

# --- Standardized Command Tree ---
def get_command_tree():
    """Return the command tree structure for config commands."""
    if_names = _get_interface_names()
    # Create a structure {ifname: options_dict} for existing interfaces
    existing_interface_tree = {}
    interface_options = {
        "status": None, # Expects 'up' or 'down'
        "mtu": None,    # Expects <number>
        "auto-nego": None, # Expects 'on' or 'off'
        "speed": None,  # Expects <speed> | 'auto'
        "duplex": None, # Expects 'full' | 'half' | 'auto'
        # Add other relevant interface config options
    }
    for name in if_names:
        existing_interface_tree[name] = interface_options

    # Options for 'config new-interface <ifname> ...'
    new_interface_options = {
        "parent-interface": {name: None for name in if_names}, # Nested dynamic options {parent_if: None}
        "ipv4address": None, # Expects <ip-address>
        "netmask": None,     # Expects <netmask>
        "mtu": None,         # Expects <number>
        "svlan-id": None,    # Expects <vlan-id>
        "cvlan-id": None,    # Expects <vlan-id>
        "status": None       # Expects 'up' or 'down'
        # Add other options for new interfaces
    }

    # Structure for delete-interface {ifname: {confirm: None}}
    delete_interface_tree = {}
    for name in if_names:
        delete_interface_tree[name] = {"confirm": None}

    command_tree = {
        "interface": {
            "<ifname>": interface_options, # Placeholder for completion hint
            **existing_interface_tree # Merge actual interfaces
        },
        "new-interface": {
            "<ifname>": new_interface_options # Placeholder for completion hint
            # The shell needs to know this expects a *new* name, not existing one
        },
        "delete-interface": {
            "<ifname>": {"confirm": None}, # Placeholder for completion hint
            **delete_interface_tree # Merge actual interfaces
        }
        # Add other config commands like 'save', 'load', 'commit' if they exist
        # "commit": None,
        # "discard": None,
    }
    # Note: The shell.py completer needs special handling for <ifname> placeholders,
    # especially for 'new-interface' where it shouldn't suggest existing names,
    # and for 'interface'/'delete-interface' where it *should* suggest existing names.
    return command_tree

# --- Standardized Descriptions ---
def get_descriptions():
    """Return the description tree for config commands."""
    if_names = _get_interface_names()
    if_name_options_desc = {name: {"": f"Configure interface {name}"} for name in if_names}
    parent_if_options_desc = {name: {"": f"Use {name} as parent"} for name in if_names}

    interface_options_desc = {
        "": "Configure parameters for an existing interface",
        "status": {
            "": "Set interface administrative status",
            "_options": ["up|down"]
        },
        "mtu": {
            "": "Set interface Maximum Transmission Unit",
            "_options": ["<68-9000>"] # Example range
        },
        "auto-nego": {
            "": "Enable/disable auto-negotiation",
            "_options": ["on|off"]
        },
        "speed": {
            "": "Set interface speed",
            "_options": ["<speed>|auto"] # e.g., 10, 100, 1000
        },
        "duplex": {
            "": "Set interface duplex mode",
            "_options": ["full|half|auto"]
        }
    }

    new_interface_options_desc = {
        "": "Configure parameters for a new interface",
        "parent-interface": {
            "": "Specify the parent physical interface",
            **parent_if_options_desc # Dynamic interface names as options
        },
        "ipv4address": {
            "": "Set the IPv4 address",
            "_options": ["<ip-address>"]
        },
        "netmask": {
            "": "Set the IPv4 netmask",
            "_options": ["<netmask>"]
        },
        "mtu": {
            "": "Set interface Maximum Transmission Unit",
            "_options": ["<68-9000>"]
        },
        "svlan-id": {
            "": "Set the outer VLAN ID (S-VLAN/QinQ)",
            "_options": ["<1-4094>"]
        },
        "cvlan-id": {
            "": "Set the inner VLAN ID (C-VLAN/QinQ)",
            "_options": ["<1-4094>"]
        },
        "status": {
            "": "Set interface administrative status",
            "_options": ["up|down"]
        }
    }

    # Descriptions for actual interfaces under 'config interface'
    existing_interfaces_desc = {}
    for name in if_names:
        existing_interfaces_desc[name] = interface_options_desc

    # Descriptions for actual interfaces under 'config delete-interface'
    delete_interfaces_desc = {}
    for name in if_names:
        delete_interfaces_desc[name] = {
             "": f"Delete interface {name}",
             "confirm": {"": f"Confirm deletion of {name}"}
        }

    descriptions = {
        "": "Enter configuration mode commands",
        "interface": {
            "": "Configure existing network interfaces",
            "<ifname>": interface_options_desc, # Placeholder description
            **existing_interfaces_desc # Add descriptions for actual interfaces
        },
        "new-interface": {
            "": "Create and configure a new network interface (e.g., VLAN)",
            "<ifname>": new_interface_options_desc # Placeholder description for the new name
        },
        "delete-interface": {
            "": "Delete an existing network interface",
            "<ifname>": { # Placeholder description
                 "": "Specify interface to delete",
                 "confirm": {"": "Confirm interface deletion"}
            },
             **delete_interfaces_desc # Descriptions for actual interfaces
        }
        # "commit": {"": "Apply staged configuration changes"},
        # "discard": {"": "Discard staged configuration changes"},
    }
    return descriptions


# --- Handle Function (Needs Major Adjustment for Staging Config) ---
def handle(args, username, hostname):
    """Handle configuration commands"""
    # Config commands typically modify a staging area, not apply immediately.
    # This handle function should interact with that staging mechanism.
    # The actual application might happen via a 'commit' command.
    prompt = f"{username}/{hostname}@vMark-node(config)> " # Indicate config mode

    if not args:
        return f"{prompt}Available config commands: interface, new-interface, delete-interface" # Add commit, discard etc.

    command = args[0]
    if_names = _get_interface_names() # Get current names for validation

    # --- Config Interface ---
    if command == "interface":
        if len(args) < 2:
            return f"{prompt}Usage: config interface <existing-ifname> [option] [value]..."
        if_name = args[1]
        if if_name not in if_names:
             return f"{prompt}Error: Interface '{if_name}' not found."

        # Parse options and values (similar to twamp/register handle)
        params = {}
        i = 2
        # Get valid options for 'interface' from the command tree
        valid_options = get_command_tree().get("interface", {}).get(if_name, {})
        while i < len(args):
             option = args[i]
             if option not in valid_options:
                 return f"{prompt}Invalid option '{option}' for interface {if_name}"

             # Check if option expects a value (value is None in tree)
             expects_value = valid_options.get(option) is None

             if expects_value:
                 if i + 1 < len(args):
                     params[option] = args[i+1]
                     i += 2
                 else:
                     return f"{prompt}Missing value for option: {option}"
             else:
                 # Handle flags if any (though none defined here currently)
                 params[option] = True
                 i += 1

        # TODO: Stage changes for the interface using params
        # e.g., update_staged_config('interface', if_name, params)
        log.info(f"Staging config for interface '{if_name}': {params}")
        return f"{prompt}Staged config for interface '{if_name}': {params}" # Placeholder

    # --- Config New Interface ---
    elif command == "new-interface":
        if len(args) < 2:
             return f"{prompt}Usage: config new-interface <new-ifname> [option] [value]..."
        if_name = args[1]
        # Potentially check if name is valid/doesn't already exist
        if if_name in if_names:
            return f"{prompt}Error: Interface '{if_name}' already exists."
        # Add validation for valid interface name format if needed

        # Parse options and values
        params = {}
        i = 2
        # Get valid options for 'new-interface' from the command tree placeholder
        valid_options = get_command_tree().get("new-interface", {}).get("<ifname>", {})
        while i < len(args):
             option = args[i]
             if option not in valid_options:
                 return f"{prompt}Invalid option '{option}' for new-interface"

             # Special handling for parent-interface which has nested dynamic options
             if option == "parent-interface":
                 if i + 1 < len(args) and args[i+1] in if_names:
                     params[option] = args[i+1]
                     i += 2
                 else:
                     valid_parents = ", ".join(if_names)
                     return f"{prompt}Invalid or missing parent interface name after 'parent-interface'. Choose from: {valid_parents}"
             else:
                 # Check if option expects a value
                 expects_value = valid_options.get(option) is None
                 if expects_value:
                     if i + 1 < len(args):
                         params[option] = args[i+1]
                         i += 2
                     else:
                         return f"{prompt}Missing value for option: {option}"
                 else:
                     # Handle flags if any
                     params[option] = True
                     i += 1

        # TODO: Stage creation of new interface using params
        # e.g., update_staged_config('new-interface', if_name, params)
        log.info(f"Staging new interface '{if_name}': {params}")
        return f"{prompt}Staged new interface '{if_name}': {params}" # Placeholder

    # --- Config Delete Interface ---
    elif command == "delete-interface":
        if len(args) < 2:
             return f"{prompt}Usage: config delete-interface <existing-ifname> confirm"
        if_name = args[1]
        if if_name not in if_names:
             return f"{prompt}Error: Interface '{if_name}' not found."
        if len(args) != 3 or args[2] != "confirm":
             # Provide specific help if confirm is missing
             return f"{prompt}Usage: config delete-interface {if_name} confirm"

        # TODO: Stage deletion
        # e.g., update_staged_config('delete-interface', if_name, {})
        log.info(f"Staging deletion of interface '{if_name}'")
        return f"{prompt}Staged deletion of interface '{if_name}'" # Placeholder

    # --- Other Config Commands (Example) ---
    # elif command == "commit":
    #     # TODO: Apply staged changes from the staging area
    #     log.info("Attempting to commit staged configuration")
    #     # result = apply_staged_config()
    #     # clear_staged_config()
    #     # return f"{prompt}{result}" # Placeholder
    #     return f"{prompt}Configuration committed." # Placeholder
    #
    # elif command == "discard":
    #     # TODO: Clear the staging area
    #     log.info("Discarding staged configuration changes")
    #     # clear_staged_config()
    #     return f"{prompt}Staged configuration changes discarded."

    else:
        return f"{prompt}Unknown config command: {command}"

    # Fallback return, should ideally not be reached
    return f"{prompt}Config command processed."