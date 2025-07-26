import os
import sys


def get_environment(identifier: str, display: str):
    """
    """
    
    value = os.getenv(identifier)
    if value is None:
        sys.stderr.write(f"{display} not set. try adding '{identifier}=...' to your '.env' file.\n")
        sys.exit(1)
    else:
        return value
