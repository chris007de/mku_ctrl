#!/usr/bin/python3

# MIT License
#
# Copyright (c) 2021 Christian Obersteiner, DL1COM
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import serial

class MKU_UP_2424_B(object):

    read_commands = {
        "forward_power": "f",
        "lo_frequency": "i",
        "pll_lock": "l",
        "converter_state": "o",
        "converter_mode": "p",
        "reverse_power": "r",
        "temperature": "t",
        "software_version": "v",
    }

    def __init__(self):
        self.busy = False
        self.__serial = None
        self.__baudrate = 115200

    def set_serial_port(self, port):
        self.port = port

    def _readline(self):
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.__serial.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)

    def serial_function(self, foo):
        self.busy = True
        reply = ""
        try:
            if self.__serial is None:
                self.__serial = serial.Serial(self.port,
                                              self.__baudrate)
            self.__serial.write(foo)
            reply = self._readline()
            reply = reply[:-1].decode('utf-8')
        except:
            pass
        self.busy = False
        return reply

    def parse_response(self, status, ret):
        # Turn converter responses into human readable information

        if status == "converter_state":
            if ret == "0":
                ret = "OFF"
            elif ret == "1":
                ret = "ON"

        if status == "pll_lock":
            if ret == "0":
                ret = "not locked"
            elif ret == "1":
                ret = "locked"

        if status == "converter_mode":
            if ret == "0":
                ret = "receive"
            elif ret == "1":
                ret = "transmit"

        if status == "lo_frequency":
            if ret == "0":
                ret = "2256 MHz"
            elif ret == "1":
                ret = "2255 MHz"
            elif ret == "2":
                ret = "2254 MHz"
            elif ret == "3":
                ret = "2253 MHz"
            elif ret == "4":
                ret = "1968 MHz"
            elif ret == "5":
                ret = "1967 MHz"
            elif ret == "6":
                ret = "1966 MHz"
            elif ret == "7":
                ret = "1965 MHz"

        return ret

    def read_status(self, status):
        if status == "statusmessage":
            if self.__serial is not None:
                ret = "Connected to " + self.port
            else:
                ret = "Not connected to converter (please check port " + self.port + ")"
        else:
            cmd = self.read_commands[status]
            while (self.busy):
                pass
            ret = self.serial_function(str.encode(cmd + '\r'))
        print(ret)
        
        return ret, self.parse_response(status, ret)

    def set_converter_state(self, state: int):
        if state == 0:
            cmd = "O0"
        elif state == 1:
            cmd = "O1"
        else:
            raise ConverterError(state, "Invalid State, only 0 or 1 allowed")

        ret = self.serial_function(str.encode(cmd + '\r'))
        print(ret)
        return ret

class ConverterError(Exception):
    def __init__(self, expression: str, message: str):
        self.expression = expression
        self.message = message
