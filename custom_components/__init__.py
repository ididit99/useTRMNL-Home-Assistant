import logging
import requests
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)

# Set up the integration with Webhook URL configuration
async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the UserTRMNL integration."""
    _LOGGER.info("Setting up UserTRMNL integration via webhook...")
    
    # Webhook URL to send data to
    webhook_url = config.get("webhook_url")
    if webhook_url is None:
        _LOGGER.error("Webhook URL is required!")
        return False
    
    # Test the webhook URL with a basic request to check if it's reachable
    try:
        response = requests.get(webhook_url)
        if response.status_code != 200:
            _LOGGER.error(f"Failed to reach the Webhook URL: {response.status_code}")
            return False
    except Exception as e:
        _LOGGER.error(f"Error during Webhook connection: {str(e)}")
        return False

    # Successful setup
    hass.data["usertrmnl"] = {"webhook_url": webhook_url}
    return True

# Service to send data to UserTRMNL via Webhook
async def send_data_to_usertrmnl(hass: HomeAssistant, service: str, data: dict):
    """Send data to UserTRMNL via Webhook."""
    webhook_url = hass.data.get("usertrmnl", {}).get("webhook_url")
    if not webhook_url:
        _LOGGER.error("Webhook URL not found!")
        return
    
    # Prepare the payload to be sent to the webhook
    payload = data
    headers = {
        "Content-Type": "application/json",
    }
    
    try:
        # Send the POST request to the webhook URL
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code == 200:
            _LOGGER.info("Data sent successfully to UserTRMNL via webhook")
        else:
            _LOGGER.error(f"Failed to send data: {response.status_code}, {response.text}")
    except Exception as e:
        _LOGGER.error(f"Error while sending data to webhook: {str(e)}")