# Home Assistant Integration with TRMNL Plugin (unfinished incomplete)

This guide will walk you through setting up Home Assistant to send sensor data to a TRMNL plugin. It includes installation, configuration, and troubleshooting steps for common issues.

---

## **📌 Prerequisites**
- A working **Home Assistant** setup
- A **TRMNL device** or TRMNL plugin API key
- Basic knowledge of **YAML** and **Python**
- **Python 3.9+** installed on your system

---

## **🛠 Step 1: Setting Up the Home Assistant Configuration**

1. Open your **Home Assistant `configuration.yaml`** file.
2. Add the following code to define REST commands to send data to TRMNL:

```yaml
rest_command:
  send_to_trmnl:
    url: "http://IP-TO-Server/receive"
    method: "post"
    headers:
      Content-Type: "application/json"
    payload: >
      {
        "temperature": "{{ states('sensor.air_sensor_temperature') | float }}",
        "pm25": "{{ states('sensor.air_sensor_current_pm2_5') | float }}"
      }
    content_type: "application/json"
```

3. Save and restart **Home Assistant** to apply the changes.

---

## **🖥 Step 2: Creating the Python Server to Handle Requests**

Create a `server.py` file to receive data from Home Assistant and send it to TRMNL.

### **📌 Install Required Packages**
Run the following command to install dependencies:
```bash
pip install flask requests
```

### **📌 Create `server.py` File**
```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TRMNL_URL = "https://usetrmnl.com/api/custom_plugins/YOUR_PLUGIN_ID"

@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.get_json()
    temperature = data.get("temperature", "N/A")
    pm25 = data.get("pm25", "N/A")
    
    html_content = f'''
        <div class="layout layout--col gap--space-between">
          <div class="grid grid--cols-1 gap--xlarge" style="max-width: 85%;">
            <div class="grid grid--cols-2">
              <div class="item">
                <div class="content">
                  <span class="value value--large">{temperature}°C</span>
                  <span class="label label--large">Current Temperature</span>
                </div>
              </div>
              <div class="item">
                <div class="content">
                  <span class="value value--large">{pm25} µg/m³</span>
                  <span class="label label--large">PM2.5 Level</span>
                </div>
              </div>
            </div>
          </div>
        </div>
    '''
    
    trmnl_payload = {
        "merge_variables": [
            {"content": html_content}
        ]
    }
    
    response = requests.post(TRMNL_URL, json=trmnl_payload, headers={"Content-Type": "application/json"})
    return jsonify({"TRMNL Response": response.status_code, "Details": response.json()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

4. **Run the server:**
```bash
python server.py
```

---

## **🚀 Step 3: Automate Sending Data from Home Assistant**

1. Open **Home Assistant UI** and go to `Automations`.
2. Click **Create Automation** and set it up as follows:
    - **Trigger:** Every minute
    - **Action:** Call `rest_command.send_to_trmnl`
3. Save and restart Home Assistant.

---

## **🛠 Troubleshooting Common Issues**

### **❌ Issue: "Template error: float got invalid input 'unknown'"**
✅ **Fix:** Modify the payload to include a default value:
```yaml
payload: >
  {
    "temperature": "{{ states('sensor.air_sensor_temperature') | float(default=0) }}",
    "pm25": "{{ states('sensor.air_sensor_current_pm2_5') | float(default=0) }}"
  }
```

### **❌ Issue: "Client error occurred when calling resource"**
✅ **Fix:** Ensure the `server.py` is running and reachable from Home Assistant.
Try:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"temperature": 22.5, "pm25": 12.7}' "http://192.168.1.169:5000/receive"
```
If this fails, restart the server and check network connectivity.

### **❌ Issue: "Must be nested inside a merge_variables payload object"**
✅ **Fix:** Ensure the payload follows the required format:
```python
trmnl_payload = {
    "merge_variables": [
        {"content": html_content}
    ]
}
```

### **❌ Issue: TRMNL Screen Not Updating**
✅ **Fix:** Try sending a test request directly to TRMNL:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"merge_variables": [{"content": "<h2>🌡 Temp: 22.5°C</h2><h2>💨 PM2.5: 12.7 µg/m³</h2>"}]}' \
     "https://usetrmnl.com/api/custom_plugins/YOUR_PLUGIN_ID"
```
If this does not update the display, restart TRMNL and check for API restrictions.

---

## **🎯 Final Steps**
- **Ensure Home Assistant & TRMNL are communicating**
- **Restart Home Assistant and TRMNL** after any changes
- **Check Home Assistant logs** for automation execution
- **Check `server.py` logs** for errors

---

### 🎉 **Congratulations!** 🎉
You have successfully integrated **Home Assistant** with **TRMNL**! 🚀

