# -*- coding:utf-8 -*-
#  Copyright (C) 2016- BOUFFALO LAB (NANJING) CO., LTD.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import re
import os
import sys
import time
import binascii
import subprocess
import serial
import pylink
import cklink
import config as gol
from libs import bflb_utils
from libs.bflb_utils import printf
from serial.tools.list_ports import comports


class BLSerialUart(object):
    """
    Bouffalolab serial package
    """

    def __init__(self, rts_state=False, dtr_state=False):
        self._device = "COM1"
        self._baudrate = 115200
        self._isp_baudrate = 2000000
        self._ser = None
        self._handshake_flag = False
        self._chiptype = "bl602"
        self.rts_state = rts_state
        self.dtr_state = dtr_state
        self._password = None

    def set_password(self, password):
        self._password = password

    def if_get_rate(self):
        return self._baudrate

    def repeat_init(self, device, rate=0, _chip_type="bl602", _chip_name="bl602"):
        try:
            if not rate:
                rate = self._isp_baudrate
            if self._ser is None:
                self._baudrate = rate

                if " (" in device:
                    dev = device[: device.find(" (")]
                else:
                    dev = device
                self._device = dev.upper()

                for _ in range(3):
                    try:
                        self._ser = serial.Serial(
                            dev,
                            rate,
                            timeout=2.0,
                            xonxoff=False,
                            rtscts=False,
                            write_timeout=None,
                            dsrdtr=False,
                        )

                    except Exception as error:
                        printf(error)
                        time.sleep(1)
                    else:
                        break
            else:
                self._ser.baudrate = rate
                self._baudrate = rate
            self._602a0_dln_fix = False
            self._chiptype = _chip_type
            self._chipname = _chip_name
        except Exception as error:
            printf("Error: {}".format(error))

    def write(self, message):
        if self._ser:
            self._ser.write(message)

    def if_write(self, data_send):
        # bflb_utils.printf("sending ", binascii.hexlify(data_send))
        if self._ser:
            self._ser.write(data_send)

    def read(self, length=1):
        try:
            data = bytearray(0)
            received = 0
            while received < length:
                val = self._ser.read(length - received)
                if len(val) == 0:
                    break
                data += val
                received += len(val)

            if len(data) != length:
                return 0, data
            return 1, data
        except Exception as error:
            printf("Error: {}".format(error))

    def raw_read(self):
        return self._ser.read(self._ser.in_waiting or 1)

    def clear_buf(self):
        if self._ser:
            self._ser.read_all()

    def close(self):
        if self._ser:
            self._ser.close()

    def if_close(self):
        self.close()

    def _is_bouffalo_chip(self):
        bl_sign = False
        if sys.platform.startswith("win"):
            for port, data, info in comports():
                if "Virtual" in data or not port:
                    continue
                if self._device.upper() == port.upper():
                    if "PID=FFFF" in info.upper() or "PID=42BF:B210" in info.upper():
                        bl_sign = True
                        break
        elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            for port, data, info in comports():
                if not port:
                    continue
                if self._device.upper() == port.upper():
                    if "PID=FFFF" in info.upper() or "PID=42BF:B210" in info.upper():
                        bl_sign = True
                        break
        else:
            bl_sign = False
        return bl_sign

    def bl_usb_serial_write(self, cutoff_time, reset_revert):
        try:
            boot_revert = 0
            printf("USB serial port")
            if cutoff_time != 0:
                boot_revert = 0
                if cutoff_time > 1000:
                    boot_revert = 1
            data = bytearray()
            specialstr = bflb_utils.string_to_bytearray("BOUFFALOLAB5555RESET")
            for b in specialstr:
                data.append(b)
            data.append(boot_revert)
            data.append(reset_revert)
            self._ser.write(data)
            time.sleep(0.05)
        except Exception as error:
            printf("Error: {}".format(error))

    '''
    def set_dtr(self, dtr):
        """
        dtr: If dtr is 1, it shows high. If dtr is 0, it shows low.
        """
        try:
            if sys.platform.startswith("darwin"):
                self._ser.write(b"BOUFFALOLAB5555DTR" + str(dtr).encode())
                self.clear_buf()
                if dtr == 1:
                    self._ser.setDTR(0)
                elif dtr == 0:
                    self._ser.setDTR(1)
            else:
                bl_sign = self._is_bouffalo_chip()
                if bl_sign:
                    self._ser.write(b"BOUFFALOLAB5555DTR" + str(dtr).encode())
                else:
                    if dtr == 1:
                        self._ser.setDTR(0)
                    elif dtr == 0:
                        self._ser.setDTR(1)
        except:
            pass
    '''

    def set_dtr(self, dtr):
        self._ser.setDTR(dtr)

    '''
    def set_rts(self, rts):
        """
        rts: If rts is 1, it shows high. If rts is 0, it shows low.
        """
        try:
            if sys.platform.startswith("darwin"):
                self._ser.write(b"BOUFFALOLAB5555RTS" + str(rts).encode())
                self.clear_buf()
                if rts == 1:
                    self._ser.setRTS(0)
                elif rts == 0:
                    self._ser.setRTS(1)
            else:
                bl_sign = self._is_bouffalo_chip()
                if bl_sign:
                    self._ser.write(b"BOUFFALOLAB5555RTS" + str(rts).encode())
                else:
                    if rts == 1:
                        self._ser.setRTS(0)
                    elif rts == 0:
                        self._ser.setRTS(1)
        except:
            pass
    '''

    def set_rts(self, rts):
        self._ser.setRTS(rts)

    def reset(self):
        if sys.platform.startswith("darwin"):
            self._ser.write(b"BOUFFALOLAB5555DTR0")
            time.sleep(0.05)
            self._ser.write(b"BOUFFALOLAB5555RTS0")
            time.sleep(0.05)
            self._ser.write(b"BOUFFALOLAB5555RTS1")
            self.clear_buf()
            self._ser.setDTR(1)
            time.sleep(0.05)
            self._ser.setRTS(1)
            time.sleep(0.05)
            self._ser.setRTS(0)
        else:
            bl_sign = self._is_bouffalo_chip()
            if bl_sign:
                self._ser.write(b"BOUFFALOLAB5555DTR0")
                time.sleep(0.05)
                self._ser.write(b"BOUFFALOLAB5555RTS0")
                time.sleep(0.05)
                self._ser.write(b"BOUFFALOLAB5555RTS1")
            else:
                self._ser.setDTR(1)
                time.sleep(0.05)
                self._ser.setRTS(1)
                time.sleep(0.05)
                self._ser.setRTS(0)

    def set_isp_baudrate(self, baudrate):
        printf("isp mode speed: ", baudrate)
        self._isp_baudrate = baudrate

    def set_timeout(self, timeout):
        self._ser.timeout = timeout

    def get_timeout(self):
        return self._ser.timeout

    def get_baudrate(self):
        if self._ser:
            return self._ser.baudrate

    def set_baudrate(self, baudrate):
        if self._ser:
            self._baudrate = self._ser.baudrate
            self._ser.baudrate = baudrate

    def deal_ack(self, dmy_data=True):
        try:
            success, ack = self.read(2)
            if success == 0:
                printf("The ack data is {}".format(binascii.hexlify(ack)))
                return ack.decode("utf-8")
            if ack.find(b"\x4F") != -1 or ack.find(b"\x4B") != -1:
                return "OK"
            elif ack.find(b"\x50") != -1 or ack.find(b"\x44") != -1:
                return "PD"
            success, err_code = self.read(2)
            if success == 0:
                printf("err code is ", str(binascii.hexlify(err_code)))
                return "FL"
            err_code_str = str(binascii.hexlify(err_code[1:2] + err_code[0:1]).decode("utf-8"))
            ack = "FL"
            try:
                ret = ack + err_code_str + "(" + bflb_utils.get_error_code_bflb(err_code_str) + ")"
            except Exception:
                ret = ""
            if err_code_str == "0a0a":
                bflb_utils.printf("Error: chip is protected or closed")
                return "FL"
            else:
                bflb_utils.printf(ret)
            return ret
        except Exception as error:
            printf("Error: {}".format(error))

    # this function return bytearray or bytes type
    def deal_response(self):
        try:
            ack = self.deal_ack()
            if ack == "OK":
                success, len_bytes = self.read(2)
                if success == 0:
                    printf("Get length error")
                    printf("len error is ", binascii.hexlify(len_bytes))
                    return "Get length error", len_bytes
                val = bflb_utils.bytearray_reverse(len_bytes)
                data_len = bflb_utils.bytearray_to_int(val)
                success, data_bytes = self.read(data_len)
                if success == 0 or len(data_bytes) != data_len:
                    printf("Read data error,maybe not get excepted length")
                    return "Read data error,maybe not get excepted length", data_bytes
                return ack, data_bytes
            printf("Not ack OK")
            printf(ack)
            return ack, None
        except Exception as error:
            printf("Error: {}".format(error))


class BLSerialJLink(object):
    def __init__(
        self,
        device,
        speed,
        jlink_shake_hand_addr,
        jlink_data_addr,
        jlink_set_tif,
        jlink_core_type,
        jlink_run_addr,
    ):
        self.device = device
        self.speed = speed
        self.jlink_shake_hand_addr = jlink_shake_hand_addr
        self.jlink_data_addr = jlink_data_addr
        self.jlink_run_addr = jlink_run_addr
        self._rx_timeout = 10000
        self._chiptype = "bl602"

        if sys.platform == "win32":
            obj_dll = pylink.Library(dllpath=bflb_utils.path_dll)
            self._jlink = pylink.JLink(lib=obj_dll)
            self.jlink_path = os.path.join(bflb_utils.app_path, "utils/jlink", "JLink.exe")
        else:
            self._jlink = pylink.JLink()
            self.jlink_path = "JLinkExe"
        match = re.search("\d{8,10}", device, re.I)
        if match is not None:
            self._jlink.open(serial_no=int(self.device))
        else:
            self._jlink.open()
        self._jlink.set_tif(jlink_set_tif)
        self._jlink.connect(jlink_core_type, self.speed)

    def set_chip_type(self, chiptype):
        self._chiptype = chiptype

    def write(self, message):
        self.raw_write(self.jlink_data_addr, message)
        # write flag
        data_list = []
        data_list.append(int("59445248", 16))
        self._jlink.memory_write(int(self.jlink_shake_hand_addr, 16), data_list, nbits=32)

    def raw_write(self, addr, data_send):
        addr_int = int(addr, 16)
        len2 = len(data_send) % 4
        len1 = len(data_send) - len2
        # using 32bits write
        if len1 != 0:
            data_list = []
            for i in range(int(len1 / 4)):
                data_list.append(
                    data_send[4 * i]
                    + (data_send[4 * i + 1] << 8)
                    + (data_send[4 * i + 2] << 16)
                    + (data_send[4 * i + 3] << 24)
                )
            self._jlink.memory_write(addr_int, data_list, nbits=32)
        # using 8bits write
        if len2 != 0:
            data_list = []
            for i in range(len2):
                data_list.append(data_send[len1 + i])
            self._jlink.memory_write(addr_int + len1, data_list, nbits=8)

    def raw_write_8(self, addr, data_send):
        data_list = []
        for data in data_send:
            data_list.append(data)
        self._jlink.memory_write(int(addr, 16), data_list, nbits=8)

    def raw_write_16(self, addr, data_send):
        data_list = []
        for i in range(int(len(data_send) / 2)):
            data_list.append(data_send[2 * i] + (data_send[2 * i + 1] << 8))
        self._jlink.memory_write(int(addr, 16), data_list, nbits=16)

    def raw_write_32(self, addr, data_send):
        data_list = []
        for i in range(int(len(data_send) / 4)):
            data_list.append(
                data_send[4 * i]
                + (data_send[4 * i + 1] << 8)
                + (data_send[4 * i + 2] << 16)
                + (data_send[4 * i + 3] << 24)
            )
        self._jlink.memory_write(int(addr, 16), data_list, nbits=32)

    def read(self, length):
        start_time = time.time() * 1000
        while True:
            ready = self._jlink.memory_read(int(self.jlink_shake_hand_addr, 16), 1, nbits=32)
            if len(ready) >= 1:
                # printf("receiving ", ready)
                if ready[0] == int("4B434153", 16):
                    break
            elapsed = (time.time() * 1000) - start_time
            if elapsed >= self._rx_timeout:
                return "waiting response time out".encode("utf-8")
            time.sleep(0.001)

        data = self._raw_read(self.jlink_data_addr, length)

        if len(data) != length:
            return 0, data
        return 1, data

    def _raw_read(self, addr, data_len):
        addr_int = int(addr, 16)
        if addr_int % 4 == 0:
            # word align, try to read using nbits=32
            len2 = data_len % 4
            len1 = data_len - len2
            data1 = bytearray(0)
            data2 = bytearray(0)
            if len1 != 0:
                data1 = self._jlink.memory_read(addr_int, int(len1 / 4), nbits=32)
            # for left, using nbits=8
            if len2 != 0:
                data2 = self._jlink.memory_read(addr_int + len1, len2, nbits=8)

            data = bytearray(0)
            for item in data1:
                data += bflb_utils.int_to_4bytearray_l(item)
            data += bytearray(data2)
            return data
        else:
            return self._raw_read8(addr, data_len)

    def _raw_read8(self, addr, data_len):
        data = self._jlink.memory_read(int(addr, 16), data_len, nbits=8)
        return bytearray(data)

    def _raw_read16(self, addr, data_len):
        raw_data = self._jlink.memory_read(int(addr, 16), data_len / 2, nbits=16)
        data = bytearray(0)
        for item in raw_data:
            data += bflb_utils.int_to_2bytearray_l(item)
        return bytearray(data)

    def _raw_read32(self, addr, data_len):
        raw_data = self._jlink.memory_read(int(addr, 16), data_len / 4, nbits=32)
        data = bytearray(0)
        for item in raw_data:
            data += bflb_utils.int_to_4bytearray_l(item)
        return bytearray(data)

    def set_rx_timeout(self, val):
        self._rx_timeout = val * 1000

    def halt_cpu(self):
        if self._jlink.halted() is False:
            self._jlink.halt()
        if self._jlink.halted():
            return True
        else:
            printf("couldn't halt cpu")
            return False

    def reset_cpu(self, ms=0, halt=True):
        if self._chiptype != "bl60x":
            self._jlink.set_reset_pin_low()
            self._jlink.set_reset_pin_high()
        return self._jlink.reset(ms, False)

    def set_pc_msp(self, pc, msp):
        if self._jlink.halted() is False:
            self._jlink.halt()
        if self._jlink.halted():
            if self._chiptype == "bl602" or self._chiptype == "bl702" or self._chiptype == "bl702l":
                jlink_script = "jlink.cmd"
                cmd = "h\r\nSetPC " + str(self._jlink_run_addr) + "\r\nexit"
                printf(cmd)
                with open(jlink_script, "w+") as fp:
                    fp.write(cmd)
                # jlink_cmd=r'C:/Keil_v5/ARM/Segger/JLink.exe -device Cortex-M4 -Speed 4000 -IF SWD  -JTAGConf -1,-1 -CommanderScript jlink.cmd'
                if self._device:
                    jlink_cmd = (
                        self.jlink_path
                        + " -device RISC-V -Speed {0} -SelectEmuBySN {1} \
                    -IF JTAG -jtagconf -1,-1 -autoconnect 1 -CommanderScript jlink.cmd".format(
                            str(self._speed), str(self._device)
                        )
                    )
                else:
                    jlink_cmd = (
                        self.jlink_path
                        + " -device RISC-V -Speed {0} \
                    -IF JTAG -jtagconf -1,-1 -autoconnect 1 -CommanderScript jlink.cmd".format(
                            str(self._speed)
                        )
                    )
                printf(jlink_cmd)
                p = subprocess.Popen(
                    jlink_cmd,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                out, err = p.communicate()
                printf(out, err)
                os.remove(jlink_script)
            else:
                self._jlink.register_write(15, int(pc, 16))
                self._jlink.register_write(13, int(msp, 16))
                self._jlink.restart()
        else:
            printf("couldn't halt cpu")

    def shakehand(
        self,
        do_reset=False,
        reset_hold_time=100,
        shake_hand_delay=100,
        reset_revert=True,
        cutoff_time=0,
        shake_hand_retry=2,
        isp_timeout=0,
        boot_load=False,
    ):
        self.write(bytearray(1))

        success, ack = self.if_read(2)
        printf(binascii.hexlify(ack))
        if ack.find(b"\x4F") != -1 or ack.find(b"\x4B") != -1:
            time.sleep(0.03)
            return "OK"
        return "FL"

    def deal_ack(self):
        success, ack = self.read(2)
        if success == 0:
            printf("ack:" + str(binascii.hexlify(ack)))
            return ack.decode("utf-8")
        if ack.find(b"\x4F") != -1 or ack.find(b"\x4B") != -1:
            return "OK"
        elif ack.find(b"\x50") != -1 or ack.find(b"\x44") != -1:
            return "PD"
        success, err_code = self.read(4)
        if success == 0:
            printf("err_code:" + str(binascii.hexlify(err_code)))
            return "FL"
        err_code_str = str(binascii.hexlify(err_code[3:4] + err_code[2:3]).decode("utf-8"))
        ack = "FL"
        try:
            ret = ack + err_code_str + "(" + bflb_utils.get_error_code_bflb(err_code_str) + ")"
        except Exception:
            ret = ""
        if err_code_str == "0a0a":
            bflb_utils.printf("Error: chip is protected or closed")
            return "FL"
        else:
            bflb_utils.printf(ret)
        return ret

    def deal_response(self):
        ack = self.deal_ack()
        if ack == "OK":
            success, len_bytes = self.read(4)
            if success == 0:
                printf("Get length error")
                printf(binascii.hexlify(len_bytes))
                return "Get length error", len_bytes
            # byte 2 and 3 is length
            val = bflb_utils.bytearray_reverse(len_bytes[2:4])
            data_len = bflb_utils.bytearray_to_int(val)
            success, data_bytes = self.read(data_len + 4)
            if success == 0:
                printf("Read data error")
                return "Read data error", data_bytes
            # remove thr first 4 bytes
            data_bytes = data_bytes[4:]
            if len(data_bytes) != data_len:
                printf("Not get excepted length")
                return "Not get excepted length", data_bytes
            return ack, data_bytes
        printf("Not ack OK")
        printf(ack)
        return ack, None

    def close(self):
        self._jlink.close()


class BLSerialCKLink(object):
    def __init__(
        self,
        device,
        serial,
        speed,
        rx_timeout,
        cklink_shake_hand_addr="20000000",
        cklink_data_addr="20000004",
        cklink_run_addr="22010000",
    ):
        self.device = device
        self.serial = serial
        self._speed = speed
        self._rx_timeout = rx_timeout
        self._inited = False
        self._cklink_reg_pc = 32
        self._cklink_shake_hand_addr = cklink_shake_hand_addr
        self._cklink_data_addr = cklink_data_addr
        self._cklink_run_addr = cklink_run_addr
        self._chiptype = "bl602"
        self.link = gol.obj_cklink
        self.temp_init()

    def temp_init(self):
        if self._inited is False:
            dev = self.device.split("|")
            vid = int(dev[0].replace("0x", ""), 16)
            pid = int(dev[1].replace("0x", ""), 16)
            printf("SN is " + str(self.serial))
            self._cklink_vid = vid
            self._cklink_pid = pid
            self._inited = True
            if not self.link:
                self.link = cklink.CKLink(
                    dlldir=bflb_utils.cklink_dll,
                    vid=self._cklink_vid,
                    pid=self._cklink_pid,
                    sn=serial,
                    arch=2,
                    cdi=0,
                )
                gol.obj_cklink = self.link
            self.link.open()
            if self.link.connected():
                self.link.reset(1)
            return False

    def set_chip_type(self, chiptype):
        self._chiptype = chiptype

    def set_rx_timeout(self, val):
        self._rx_timeout = val * 1000

    def halt_cpu(self):
        return self.link.halt()

    def resume_cpu(self):
        return self.link.resume()

    def reset_cpu(self):
        return self.link.reset(1)

    def set_pc_msp(self):
        self.halt_cpu()
        if self._chiptype == "bl602" or self._chiptype == "bl702" or self._chiptype == "bl702l":
            addr = int(self._cklink_run_addr, 16)
            self.link.write_cpu_reg(self._cklink_reg_pc, addr)
            # self.link.resume()

    def write(self, message):
        self.if_raw_write(self._cklink_data_addr, message)
        # write flag
        self.if_raw_write(self._cklink_shake_hand_addr, binascii.unhexlify("48524459"))

    def _raw_write(self, addr, data_send):
        self.halt_cpu()
        addr_int = int(addr, 16)
        data_send = bytes(data_send)
        self.link.write_memory(addr_int, data_send)
        self.resume_cpu()

    def read(self, length):
        start_time = time.time() * 1000
        while True:
            self.halt_cpu()
            ready = self.link.read_memory(int(self._cklink_shake_hand_addr, 16), 4)
            if len(ready) >= 1:
                ready = binascii.hexlify(ready).decode()
                # printf("receiving ", ready)
                if ready == "5341434b":
                    self.resume_cpu()
                    break
            elapsed = (time.time() * 1000) - start_time
            # time out judgment
            if elapsed >= self._rx_timeout:
                return 0, "waiting response time out".encode("utf-8")
            self.resume_cpu()
            time.sleep(0.001)

        data = self._raw_read(self._cklink_data_addr, length)
        if len(data) != length:
            return 0, data
        return 1, data

    def _raw_read(self, addr, data_len):
        return self.if_raw_read8(addr, data_len)

    def _raw_read8(self, addr, data_len):
        self.halt_cpu()
        data = self.link.read_memory(int(addr, 16), data_len)
        self.resume_cpu()
        return bytearray(data)

    def if_shakehand(self):
        self.if_write(bytearray(1))
        success, ack = self.read(2)
        printf(binascii.hexlify(ack))
        if ack.find(b"\x4F") != -1 or ack.find(b"\x4B") != -1:
            if self._password:
                cmd = bflb_utils.hexstr_to_bytearray("2400")
                cmd += bflb_utils.int_to_2bytearray_l(len(self._password) // 2)
                cmd += bflb_utils.hexstr_to_bytearray(self._password)
                self.write(cmd)
                success, ack = self.read(2)
                bflb_utils.printf("Set pswd ack is ", binascii.hexlify(ack).decode("utf-8"))
            time.sleep(0.03)
            return "OK"
        return "FL"

    def deal_ack(self):
        success, ack = self.read(2)
        if success == 0:
            printf("ack:" + str(binascii.hexlify(ack)))
            return ack.decode("utf-8")
        if ack.find(b"\x4F") != -1 or ack.find(b"\x4B") != -1:
            return "OK"
        elif ack.find(b"\x50") != -1 or ack.find(b"\x44") != -1:
            return "PD"
        success, err_code = self.if_read(4)
        if success == 0:
            printf("err_code:" + str(binascii.hexlify(err_code)))
            return "FL"
        err_code_str = str(binascii.hexlify(err_code[3:4] + err_code[2:3]).decode("utf-8"))
        ack = "FL"
        try:
            ret = ack + err_code_str + "(" + bflb_utils.get_error_code_bflb(err_code_str) + ")"
        except Exception:
            ret = ""
        if err_code_str == "0a0a":
            bflb_utils.printf("Error: chip is protected or closed")
            return "FL"
        else:
            bflb_utils.printf(ret)
        return ret

    def deal_response(self):
        ack = self.deal_ack()
        if ack == "OK":
            success, len_bytes = self.read(16)
            if success == 0:
                printf("Get length error")
                printf(binascii.hexlify(len_bytes))
                return "Get length error", len_bytes
            # byte 2 and 3 is length
            val = bflb_utils.bytearray_reverse(len_bytes[2:4])
            data_len = bflb_utils.bytearray_to_int(val)
            success, data_bytes = self.if_read(data_len + 4)
            if success == 0:
                printf("Read data error")
                return "Read data error", data_bytes
            # remove thr first 4 bytes
            data_bytes = data_bytes[4:]
            if len(data_bytes) != data_len:
                printf("Not get excepted length")
                return "Not get excepted length", data_bytes
            return ack, data_bytes
        printf("Not ack OK")
        printf(ack)
        return ack, None


if __name__ == "__main__":
    pass
