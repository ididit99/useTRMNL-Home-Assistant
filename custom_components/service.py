from homeassistant.helpers import service
from homeassistant.core import HomeAssistant
import logging

_LOGGER = logging.getLogger(__name__)

async def async_send_data_service(call):
    """Handle sending data to UserTRMNL from Home Assistant via Webhook."""
    data = call.data
    hass = call.hass

    # Call the function from __init__.py to send data
    await send_data_to_usertrmnl(hass, "send_data", data)

def setup(hass: HomeAssistant, config: dict):
    """Set up the service to send data."""
    hass.services.async_register(
        "usertrmnl", "send_data", async_send_data_service
    )
    return True