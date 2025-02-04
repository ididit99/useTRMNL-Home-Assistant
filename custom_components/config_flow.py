import logging
from homeassistant import config_entries
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

CONF_WEBHOOK_URL = "webhook_url"  # Correct key name

class UserTRMNLConfigFlow(config_entries.ConfigFlow, domain="usertrmnl"):
    """Handle a config flow for UserTRMNL integration."""

    async def async_step_user(self, user_input=None):
        """Handle user input for webhook URL."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({vol.Required(CONF_WEBHOOK_URL): str}),
            )

        webhook_url = user_input[CONF_WEBHOOK_URL]

        if not webhook_url.startswith("http"):
            return self.async_show_form(step_id="user", errors={"base": "invalid_url"})

        return self.async_create_entry(title="UserTRMNL", data={CONF_WEBHOOK_URL: webhook_url})