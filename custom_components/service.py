from homeassistant.core import HomeAssistant, ServiceCall
import logging
import requests

_LOGGER = logging.getLogger(__name__)

async def async_send_sensor_data_service(call: ServiceCall):
    """Send temperature and PM2.5 data to UserTRMNL."""
    hass = call.hass
    temperature = call.data.get("temperature")
    pm25 = call.data.get("pm25")  # Support PM2.5

    if temperature is None and pm25 is None:
        _LOGGER.error("At least one value (temperature or pm2.5) is required")
        return

    webhook_url = hass.data["usertrmnl"].get("webhook_url")
    if not webhook_url:
        _LOGGER.error("Webhook URL is not set.")
        return

    payload = {}
    if temperature is not None:
        payload["temperature"] = temperature
    if pm25 is not None:
        payload["pm25"] = pm25  # Include PM2.5 if provided

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        _LOGGER.info(f"Successfully sent sensor data: {payload}")
    except requests.RequestException as error:
        _LOGGER.error(f"Failed to send sensor data: {error}")

async def async_setup_services(hass: HomeAssistant):
    """Register services for UserTRMNL."""
    hass.services.async_register("usertrmnl", "send_sensor_data", async_send_sensor_data_service)

def setup(hass: HomeAssistant, config: dict):
    """Set up the services."""
    hass.loop.create_task(async_setup_services(hass))  # Register services on startup
    return True