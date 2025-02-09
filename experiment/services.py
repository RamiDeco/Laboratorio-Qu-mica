import RPi.GPIO as GPIO
import board
import digitalio
import adafruit_max31865

# Configuración de GPIO y sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=1025, ref_resistor=4301, wires=2)
bandera = False

def obtenerTemperatura():
    temp = 0.13 * sensor.resistance - 104.62
    data = {
        'timestamp': time.time(),
        'temperatura': temp,
    }
    return jsonify(data)

def controlRele():
    temp = 0.13 * sensor.resistance - 104.62
    releEncendido = False
    if temp > 46:
        GPIO.output(18, 1)
        releEncendido = False
    elif temp < 30 and not releEncendido:
        GPIO.output(18, 0)
        releEncendido = True