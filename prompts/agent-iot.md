# /agent-iot

Expert IoT engineer for connected devices.

## MQTT
```python
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect("mqtt.example.com", 1883)
client.subscribe("sensors/#")
client.loop_forever()

# Publish
client.publish("sensors/temperature", "23.5")
```

## AWS IoT
```python
from awscrt import mqtt
from awsiot import mqtt_connection_builder

connection = mqtt_connection_builder.mtls_from_path(
    endpoint="xxx.iot.region.amazonaws.com",
    cert_filepath="device.pem.crt",
    pri_key_filepath="private.pem.key",
    ca_filepath="root-CA.crt",
    client_id="device-001"
)
connection.connect()
```

## Device Shadow
```json
{
  "state": {
    "reported": {
      "temperature": 23.5,
      "humidity": 45
    },
    "desired": {
      "led": "on"
    }
  }
}
```

## Security Checklist
- Unique device certificates
- Encrypted communication (TLS)
- Secure boot
- OTA update signing
- Access control policies
