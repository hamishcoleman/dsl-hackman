from django.conf import settings
import serial

# Interface with a card reader running
# https://github.com/hamishcoleman/arduino_cardreader

# TODO:
# - revamp this API to have a way to send messages back to the reader
#   (It would be nice to turn the green LED on to show door open, and
#   probably good to show a denied door access as well)
# - revamp to cleanly ignore repeats
# - revamp to understand what "tag=NONE" means

_conn = None
debug = True


def _open():
    global _conn
    if _conn is None:
        _conn = serial.Serial(
            settings.RFID_READER['CONFIG']['serial_port'],
            settings.RFID_READER['CONFIG']['baud_rate'],
        )
    return _conn


def get_cards():
    '''Yields calculated card ids from connected reader'''

    conn = _open()

    seen_stx = False
    buf = b''

    while True:
        ch = conn.read(1)

        if not seen_stx:
            # If not inside a message, we only look for a message start
            if ch == b'\x02':
                seen_stx = True
            continue

        if ch == b'\x04':
            msg = buf.decode('utf8')

            if debug:
                print("Serial:RX:", buf)

            key, value = msg.split("=")

            if key == "tag" and value != "NONE":
                yield (value, None)

            buf = b""
            seen_stx = False
            continue

        buf += ch


def _command(cmd):
    """Send an arbitrary command packet"""
    conn = _open()

    buf = b"\x02" + cmd.encode("utf8") + b"\x04"

    conn.write(buf)
