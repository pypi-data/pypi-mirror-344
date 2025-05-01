import subprocess
import logging

# Set up logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create and configure the twamp logger
log = logging.getLogger('twamp')
log.setLevel(logging.INFO)

# Also silence pyroute2 debug messages
logging.getLogger('pyroute2').setLevel(logging.WARNING)

# Now import the plugin after logging is configured
from plugins.twamp.onyx import (
    dscpTable,
    twl_sender,
    twl_responder,
    start_sender,
    start_responder
)

# Expose the logger to the plugin
import plugins.twamp.onyx as onyx
onyx.log = log

# --- Standardized Command Tree ---
def get_command_tree():
    """Return the command tree structure for twamp commands."""
    # Options common to sender/responder
    common_options = {
        "padding": None,
        "ttl": None,
        "tos": None,
        "do-not-fragment": None # Flag
    }
    # Options specific to sender
    sender_options = {
        "destination-ip": None, # Required, handled in handle()
        "port": None,           # Required, handled in handle()
        "count": None,
        "interval": None,
        **common_options # Merge common options
    }
    # Options specific to responder
    responder_options = {
        "port": None,           # Required, handled in handle()
        **common_options # Merge common options
    }

    command_tree = {
        "dscptable": None, # Simple command
        "ipv4": {
            "sender": sender_options,
            "responder": responder_options
        },
        "ipv6": {
            # Assuming IPv6 options are structurally the same
            "sender": sender_options, # Re-use sender_options
            "responder": responder_options # Re-use responder_options
        }
    }
    return command_tree

# --- Standardized Descriptions ---
def get_descriptions():
    """Return the description tree for twamp commands."""
    # Descriptions for common options
    common_desc = {
        "padding": {
            "": "Enter padding size in bytes",
            "_options": ["<0-9000>"]
        },
        "ttl": {
            "": "Enter TTL value",
            "_options": ["<1-255>"]
        },
        "tos": {
            "": "Enter ToS value",
            "_options": ["<0-255>"]
        },
        "do-not-fragment": {
            "": "Set the DF (Do Not Fragment) bit"
            # No _options needed for a flag
        }
    }
    # Descriptions for sender options (base for IPv4/IPv6)
    sender_base_desc = {
        "": "Configure TWAMP sender parameters",
        "port": {
            "": "Enter destination port number (REQUIRED)",
            "_options": ["<1024-65535>"]
        },
        "count": {
            "": "Enter number of packets to send",
            "_options": ["<1-9999>"]
        },
        "interval": {
            "": "Enter packet interval in milliseconds",
            "_options": ["<10-1000>"]
        },
        **common_desc # Merge common descriptions
    }

    # Descriptions specific to IPv4 sender
    ipv4_sender_desc = {
        **sender_base_desc, # Start with base
        "destination-ip": {
            "": "Enter destination IPv4 address (REQUIRED)",
            "_options": ["<ip-address>"]
        }
    }

    # Descriptions specific to IPv6 sender
    ipv6_sender_desc = {
        **sender_base_desc, # Start with base
        "destination-ip": {
            "": "Enter destination IPv6 address (REQUIRED)",
            "_options": ["<ipv6-address>"]
        }
    }

    # Descriptions for responder options (same for IPv4/IPv6)
    responder_desc = {
        "": "Configure TWAMP responder parameters",
        "port": {
            "": "Enter listening port number (REQUIRED)",
            "_options": ["<1024-65535>"]
        },
        **common_desc # Merge common descriptions
    }

    descriptions = {
        "": "Configure and manage TWAMP sessions",
        "dscptable": {
            "": "Show the DSCP value table"
        },
        "ipv4": {
            "": "Configure IPv4 TWAMP",
            "sender": ipv4_sender_desc,
            "responder": responder_desc
        },
        "ipv6": {
            "": "Configure IPv6 TWAMP",
            "sender": ipv6_sender_desc,
            "responder": responder_desc
        }
    }
    return descriptions

# --- Handle Function (Adjusted for Standardized Parsing) ---
def handle(args, username, hostname):
    """Handle twamp commands"""
    prompt = f"{username}/{hostname}@vMark-node> "

    if not args:
        return f"{prompt}Usage: twamp [dscptable|ipv4|ipv6] ..."

    if args[0] == "dscptable":
        try:
            # Assuming dscpTable() returns a string or can be printed
            table_output = dscpTable()
            return f"{prompt}DSCP Table:\n{table_output}"
        except Exception as e:
            log.error(f"Error getting DSCP table: {e}")
            return f"{prompt}Error retrieving DSCP table: {e}"

    elif args[0] in ["ipv4", "ipv6"]:
        ip_version = args[0]
        if len(args) < 2 or args[1] not in ["sender", "responder"]:
            return f"{prompt}Usage: twamp {ip_version} [sender|responder] ..."

        mode = args[1]
        # Get the relevant command tree branch for validation/parsing aid
        try:
            command_options = get_command_tree()[ip_version][mode]
        except KeyError:
             # Should not happen if args[0]/args[1] are validated, but good practice
             return f"{prompt}Internal error: Command structure not found for {ip_version} {mode}"

        params = {} # Dictionary to store parsed parameters
        i = 2
        while i < len(args):
            param_name = args[i] # Keep original kebab-case for user feedback
            param_key = param_name.replace('-', '_') # Convert for internal use/kwargs

            # Check if the parameter exists in the defined options
            if param_name not in command_options:
                return f"{prompt}Unknown parameter '{param_name}' for {ip_version} {mode}"

            # Check if it's a flag (value is None and no _options in description)
            # A more robust check might involve looking at descriptions too
            is_flag = command_options.get(param_name) is None and param_key == "do_not_fragment" # Example

            if is_flag:
                 params[param_key] = True
                 i += 1
            elif i + 1 < len(args):
                 # Parameter expects a value
                 params[param_key] = args[i+1]
                 i += 2
            else:
                 return f"{prompt}Missing value for parameter: {param_name}"

        # --- Parameter Validation and Execution ---
        log.info(f"Attempting to start TWAMP {ip_version} {mode} with params: {params}")

        if mode == "sender":
            required = ["destination_ip", "port"]
            if not all(p in params for p in required):
                 missing = [p.replace('_', '-') for p in required if p not in params]
                 return f"{prompt}Missing required sender parameters: {', '.join(missing)}"
            try:
                # Prepare arguments for start_sender, converting types as needed
                sender_args = {
                    "ip_version": ip_version,
                    "destination_ip": params["destination_ip"],
                    "port": int(params["port"]),
                    "count": int(params.get("count", 10)), # Default count
                    "interval": int(params.get("interval", 100)), # Default interval
                    "padding": int(params.get("padding", 0)),
                    "ttl": int(params.get("ttl", 64)),
                    "tos": int(params.get("tos", 0)),
                    "do_not_fragment": params.get("do_not_fragment", False)
                }
                result = start_sender(**sender_args)
                log.info(f"start_sender result: {result}")
                # Assuming start_sender returns status or output string
                return f"{prompt}{result}"
            except ValueError as e:
                 log.error(f"Invalid parameter value for sender: {e}")
                 return f"{prompt}Invalid value provided for a parameter: {e}"
            except Exception as e:
                 log.exception(f"Error starting TWAMP sender: {e}")
                 return f"{prompt}Error starting TWAMP sender: {e}"

        elif mode == "responder":
            required = ["port"]
            if not all(p in params for p in required):
                 missing = [p.replace('_', '-') for p in required if p not in params]
                 return f"{prompt}Missing required responder parameters: {', '.join(missing)}"
            try:
                # Prepare arguments for start_responder
                 responder_args = {
                    "ip_version": ip_version,
                    "port": int(params["port"]),
                    "padding": int(params.get("padding", 0)),
                    "ttl": int(params.get("ttl", 64)), # Responder might not use TTL directly
                    "tos": int(params.get("tos", 0)),
                    "do_not_fragment": params.get("do_not_fragment", False) # Might not be used by responder
                 }
                 result = start_responder(**responder_args)
                 log.info(f"start_responder result: {result}")
                 # Assuming start_responder returns status or output string
                 return f"{prompt}{result}"
            except ValueError as e:
                 log.error(f"Invalid parameter value for responder: {e}")
                 return f"{prompt}Invalid value provided for a parameter: {e}"
            except Exception as e:
                 log.exception(f"Error starting TWAMP responder: {e}")
                 return f"{prompt}Error starting TWAMP responder: {e}"

    else:
        return f"{prompt}Unknown command: twamp {args[0]}"

    # Should not be reached if all paths return
    return f"{prompt}Command processed."