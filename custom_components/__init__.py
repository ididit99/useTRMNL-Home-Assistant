async def async_setup(hass, config):
    """Set up the UserTRMNL integration."""
    hass.data.setdefault("usertrmnl", {})  # Ensure the dictionary exists

    # Import and setup services
    from . import service
    service.setup(hass, config)

    return True

async def async_setup_entry(hass, entry):
    """Set up a config entry for UserTRMNL."""
    hass.data.setdefault("usertrmnl", {})  # Ensure dictionary exists
    hass.data["usertrmnl"]["webhook_url"] = entry.data.get("webhook_url")

    return True