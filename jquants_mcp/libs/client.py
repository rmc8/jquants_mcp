import logging
import os
import sys

import jquantsapi

logger = logging.getLogger("jquants-mcp")


def get_client() -> jquantsapi.ClientV2:
    """
    Initialize and return the J-Quants API Client (V2).
    Requires JQUANTS_API_KEY environment variable.
    """
    refresh_token = os.environ.get("JQUANTS_API_KEY")
    if not refresh_token:
        logger.error("JQUANTS_API_KEY environment variable is not set.")
        sys.exit(1)

    try:
        # ClientV2(api_key=...)
        cli = jquantsapi.ClientV2(api_key=refresh_token)
        return cli
    except Exception as e:
        logger.error(f"Failed to initialize JQuants API Client: {e}")
        sys.exit(1)
