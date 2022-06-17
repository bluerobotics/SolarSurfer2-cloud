import struct
import serial
import time
from adafruit_rockblock import RockBlock, mo_status_message

ser = serial.Serial(
    '/dev/ttyUSB0',
    baudrate=19200,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1,
)

rb = RockBlock(ser)
rb.reset()

# Get some info from the satellite modem
print(f"Model: {rb.model}")
print(f"Revision: {rb.revision}")
print(f"Serial number: {rb.serial_number}")

# Try to get signal from the satellite
retries = 0
max_retries = 10
# while True:
#     sq = rb.signal_quality
#     print(f"Signal quality: {sq}")
#     if sq != 0:
#         break
#     time.sleep(0.1)
#     retries += 1
#     if retries >= max_retries:
#         raise RuntimeError("Could not get signal from the satellite. Aborting operation.")

print(f"Modem Terminated (MT) message in the buffer: {rb.data_in}")
print(f"Modem Originated (MO) message in the buffer: {rb.data_out}")
print(f"Geolocation: {rb.geolocation}")
print(f"Energy monitor: {rb.energy_monitor}")

data = struct.pack("1f", 6.6)
print("Trying talking to the satellites...")
rb.data_out = data
retries = 0
max_retries = 10
while retries < max_retries:
    status = rb.satellite_transfer()
    print(retries, status)
    if status[0] <= 5:
        print(f"Sucessfully sent message. Status of {status[0]} ({mo_status_message[status[0]]}).")
        break
    print(f"Failed to send message. Status of {status[0]} ({mo_status_message[status[0]]}). Retrying...")
    time.sleep(0.1)
    retries += 1

ser.close()
