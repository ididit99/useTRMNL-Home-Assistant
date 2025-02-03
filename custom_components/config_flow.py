import logging
import requests
from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_WEBHOOK_URL

_LOGGER = logging.getLogger(__name__)

class UserTRMNLConfigFlow(config_entries.ConfigFlow, domain="usertrmnl"):
    """Handle a config flow for UserTRMNL via Webhook."""

    def __init__(self):
        self.webhook_url = None

    async def async_step_user(self, user_input=None):
        """Handle the user input step."""
        if user_input is None:
            # Show a form asking for the webhook URL
            return self.async_show_form(step_id="user", data_schema=vol.Schema({
                vol.Required("webhook_url"): str,
            }))
        
        self.webhook_url = user_input["webhook_url"]
        
        # Test the Webhook URL by making a test request
        try:
            response = requests.get(self.webhook_url)
            if response.status_code == 200:
                return self.async_create_entry(title="UserTRMNL", data={"webhook_url": self.webhook_url})
            else:
                return self.async_show_form(errors={"base": "Invalid Webhook URL"})
        except Exception:
            return self.async_show_form(errors={"base": "Failed to connect to the Webhook URL"})