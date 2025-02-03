# Home Assistant UserTRMNL Integration

This is a custom Home Assistant integration for sending data to **UserTRMNL** via a webhook.

## Installation

1. Clone this repository into your Home Assistant's `custom_components` folder:

    ```bash
    git clone https://github.com/yourusername/home-assistant-usertrmnl.git /config/custom_components/usertrmnl
    ```

2. Restart Home Assistant.

## Configuration

1. Go to **Configuration > Integrations**.
2. Add the **UserTRMNL** integration.
3. Provide your **Webhook URL**.

## Example Usage

To send data to UserTRMNL, you can call the service:

```yaml
service: usertrmnl.send_data
data:
  field_1: "value1"
  field_2: "value2"