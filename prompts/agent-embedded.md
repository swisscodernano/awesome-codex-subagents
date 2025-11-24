# /agent-embedded

Expert embedded systems engineer.

## Arduino
```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
```

## ESP32 (MicroPython)
```python
from machine import Pin, PWM
import time

led = Pin(2, Pin.OUT)
pwm = PWM(Pin(5), freq=1000)

while True:
    for duty in range(0, 1024, 10):
        pwm.duty(duty)
        time.sleep_ms(10)
```

## RTOS Task
```c
void vTaskFunction(void *pvParameters) {
    for (;;) {
        // Task code here
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

xTaskCreate(vTaskFunction, "TaskName", 1024, NULL, 1, NULL);
```

## Best Practices
- Minimize memory allocation
- Use interrupts for real-time
- Implement watchdog timers
- Handle power management
- Document hardware connections
