"""Packet classes for RuuviTag beacons."""
from ..utils import data_to_hexstring, data_to_binstring

class RuuviTagFrame(object):
    """RuuviTag data frame."""

    def __init__(self, packet):
        self._company_id = packet[5:7]
        assert self._company_id == b"\x99\x04"

        data = packet[7:]
        self._version = data[0]

        if self._version == 3:
            self._humidity = data[1]
            self._temperature_integer = data[2]
            self._temperature_fraction = data[3]
            self._pressure = data[4:6]
            self._acc_x = data[6:8]
            self._acc_y = data[8:10]
            self._acc_z = data[10:12]
            self._battery_mv = data[12:14]

        #self._identifier = data_to_hexstring(data['identifier'])
        #self._encrypted_metadata = data_to_binstring(data['encrypted_metadata'])

    @property
    def company_id(self):
        return self._company_id

    @property
    def properties(self):
        """Get beacon properties."""
        if self._version != 3:
            return { "company_id": self.company_id, "version": self._version, "implemented": False }
            
        return {
            "company_id": self.company_id,
            "version": self._version,
            "humidity": self._humidity,
            "temperature": (self._temperature_integer, self._temperature_fraction),
            "pressure": self._pressure,
            "acc": (self._acc_x, self._acc_y, self._acc_z),
            "battery": self._battery_mv,
        }

    def __str__(self):
        return "RuuviTagFrame<Version:%s>" % (self._version)
