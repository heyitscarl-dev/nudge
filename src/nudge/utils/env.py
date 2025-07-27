import os
import sys
import dotenv

dotenv.load_dotenv()

def get_environment(identifier: str, display: str):
    """
    Get an environment variable and report potential errors.

    Args:
        identifier (str): the name of the env variable
        display (str): the display name of the env variable used for error reporting
    """
    
    value = os.getenv(identifier)
    if value is None:
        sys.stderr.write(f"{display} not set. try adding '{identifier}=...' to your '.env' file.\n")
        sys.exit(1)
    else:
        return value

MAILGUN_WEBHOOK_SIGNING_KEY = get_environment("MAILGUN_WEBHOOK_SIGNING_KEY", "mailgun HTTP webhook signing key")
MAILGUN_API_KEY = get_environment("MAILGUN_API_KEY", "mailgun API key")
MAILGUN_DOMAIN = get_environment("MAILGUN_DOMAIN", "mailgun domain")

OPENAI_API_KEY = get_environment("OPENAI_API_KEY", "openAI API key")
