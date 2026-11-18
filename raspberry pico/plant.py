
from machine import ADC, Pin
import time
import dht
import requests
import connection
import env
import gc

# Sensor initialization
ldr = ADC(Pin(26))
dht_sensor = dht.DHT22(Pin(15))
soil_sensor = ADC(Pin(27))

# Http configuration
url = "http://IPv4_ADDRESS:5000/sensor-data"

# Soil sensor calibration
SOIL_DRY = 50000    # Replace with your dry soil ADC reading
SOIL_WET = 33200    # Replace with your wet soil ADC reading

# Sensor reading function
def read_dht22():
    try:
        dht_sensor.measure()

        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        return temperature, humidity

    except OSError as e:
        print("DHT22 Error:", e)
        return None, None


def read_ldr():
    light_value = ldr.read_u16()

    light_percentage = 100 - (light_value / 65535 * 100)

    return light_value, light_percentage


def read_soil():
    soil_value = soil_sensor.read_u16()

    # Convert ADC reading to voltage
    soil_voltage = (soil_value / 65535) * 3.3

    # Calculate soil moisture percentage
    moisture_percentage = (
        (SOIL_DRY - soil_value) /
        (SOIL_DRY - SOIL_WET)
    ) * 100

    # Limit percentage between 0 and 100
    moisture_percentage = max(0, min(100, moisture_percentage))

    return soil_value, soil_voltage, moisture_percentage
    
# Main program
def main():
    while True:

        # Read DHT22
        temperature, humidity = read_dht22()

        # Read LDR
        light_value, light_percentage = read_ldr()

        # Read Soil Moisture
        soil_value, soil_voltage, soil_percentage = read_soil()

        print("\n========== SENSOR READINGS ==========")

        # DHT22
        if temperature is not None:
            print("\n--- DHT22 ---")
            print("Temperature:", round(temperature, 2), "°C")
            print("Humidity:", round(humidity, 2), "%")

        # LDR
        print("\n--- LDR ---")
        print("ADC Value:", light_value)
        print("Light Intensity:", round(light_percentage, 2), "%")

        # Soil Moisture
        
        print("\n--- SOIL MOISTURE ---")
        print("ADC Value:", soil_value)
        print("Output Voltage:", round(soil_voltage, 2), "V")
        print("Soil Moisture:", round(soil_percentage, 2), "%")
        
        gc.collect()
        print()
        
        try:
            print("Sending http request...")
            response = requests.post(url, json={"temperature": round(temperature, 2), "humidity": round(humidity, 2), "light_intensity": round(light_percentage, 2), "soil_moisture": round(soil_percentage, 2)}, timeout=10)
            response.close()
            print("HTTP Response:", response.status_code, response.reason)
        except OSError as e:
            print("HTTP Error:", e)

        finally:
            gc.collect()

             
        time.sleep(20)

# Program entry point
if __name__ == "__main__":
    main()

