import logging
import requests

class PostToDiscordError(Exception):
    """Exception raised when posting to Discord fails."""
    pass

class DiscordPoster:
    """A lightweight client for posting messages to a Discord webhook."""

    def __init__(
            self,
            webhook_url: str,
            log_exceptions: bool = True,
            raise_exceptions: bool = True
    ):
        self.log_exceptions = log_exceptions
        self.raise_exceptions = raise_exceptions

        if not webhook_url:
            self.handle_error(ValueError("Webhook URL must be provided"))
        self.webhook_url = webhook_url


    def handle_error(self, exception: Exception):
        if self.log_exceptions:
            logging.error(str(exception))
        if self.raise_exceptions:
            raise exception

    def post_to_discord(self, message: str) -> bool:
        """Post a message to the Discord webhook.

        Returns True if successful, False otherwise.
        """
        try:
            response = requests.post(
                self.webhook_url,
                json={"content": message},
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            self.handle_error(PostToDiscordError(f"Error posting message to Discord: {e}"))
            return False
