import RPi.GPIO as GPIO
import time
import spidev
from lib_nrf24 import NRF24

# Use BCM numbering (GPIO pin numbers)
GPIO.setmode(GPIO.BCM)

# Define radio pipes (addresses)
pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]

# Create radio object
radio = NRF24(GPIO, spidev.SpiDev())

# Begin radio: CE pin = 25, CSN = 0 (SPI CE0)
radio.begin(0, 25)

# Radio configuration
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

# Open writing pipe (this must match the receiver’s reading pipe)
radio.openWritingPipe(pipes[0])

# Print details (good for debugging)
radio.printDetails()

# Message to send
sendMessage = [ord(c) for c in "Hi..Arduino UNO"]
while len(sendMessage) < 32:
    sendMessage.append(0)

# Main loop
while True:
    start = time.time()
    radio.write(sendMessage)
    print(
        "Sent the message: {}".format("".join([chr(x) for x in sendMessage if x != 0]))
    )
    print("Transmission time: {:.2f} s".format(time.time() - start))
    time.sleep(3)
