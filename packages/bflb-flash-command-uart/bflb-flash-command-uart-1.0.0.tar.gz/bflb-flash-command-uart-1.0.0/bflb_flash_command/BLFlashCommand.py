# -*- coding: utf-8 -*-
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
import argparse
import binascii
import configparser
import traceback
import subprocess
import shutil
from fnmatch import fnmatch

from libs import bflb_utils
from libs import bflb_img_loader
from libs.bflb_eflash_loader import *
from libs.bflb_configobj import BFConfigParser

try:
    from debug import *
except ImportError:
    NUM_ERROR_LOG = 5

platform = "windows"
if sys.platform.startswith("win"):
    platform = "windows"
elif sys.platform.startswith("linux"):
    platform = "linux"
elif sys.platform.startswith("darwin"):
    platform = "macos"

if getattr(sys, "frozen", False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(__file__)
sys.path.append(app_path)


def hex_type(x):
    if x.startswith("0x"):
        return x
    raise argparse.ArgumentTypeError('Invalid hex value (must start with "0x")')


def flash_command_parser_init():
    parser = argparse.ArgumentParser(description="flash-command")
    parser.add_argument("--port", dest="port", help="serial port to use")
    parser.add_argument("--chipname", dest="chipname", default="BL616", help="chip name")
    parser.add_argument("--baudrate", dest="baudrate", default=2000000, type=int, help="the speed of communicate")
    parser.add_argument("--config", dest="config", default="", help="run config")
    parser.add_argument("--firmware", dest="firmware", default="", help="firmware to write")
    parser.add_argument("--efusefile", dest="efusefile", default="", help="efusefile to write")
    parser.add_argument("--cpu_id", dest="cpu_id", default="", help="cpu id")
    parser.add_argument("--key", dest="key", default="", help="aes key")
    parser.add_argument("--iv", dest="iv", default="", help="aes iv")
    parser.add_argument("--pk", dest="pk", help="ecc public key")
    parser.add_argument("--sk", dest="sk", default="", help="ecc private key")
    parser.add_argument("--pk_str", dest="pk_str", help="ecc public key string")
    parser.add_argument("--sk_str", dest="sk_str", help="ecc private key string")
    parser.add_argument("--flash", dest="flash", action="store_true", help="indicate flash operation")
    parser.add_argument("--flash_otp", dest="flash_otp", action="store_true", help="indicate flash otp operation")
    parser.add_argument("--otpindex", type=int, help="flash otp index 0/1/2")
    parser.add_argument("--lock", action="store_true", help="indicate flash otp lock")
    parser.add_argument("--efuse", action="store_true", help="indicate read or write efuse")
    parser.add_argument("--erase", dest="erase", action="store_true", help="indicate erase flash")
    parser.add_argument("--build", dest="build", action="store_true", help="indicate build pack")
    parser.add_argument("--read", dest="read", action="store_true", help="indicate read from flash or efuse")
    parser.add_argument("--write", dest="write", action="store_true", help="indicate write to flash or efuse")
    parser.add_argument("--start", type=hex_type, help="start address (hex, e.g., 0x1A2B)")
    parser.add_argument("--end", type=hex_type, help="end address (hex, e.g., 0x1A2C)")
    parser.add_argument("--len", type=hex_type, help="length (hex, e.g., 0x100)")
    parser.add_argument("--file", dest="file", help="file for reading or writing")
    parser.add_argument("--ram", dest="ram", action="store_true", help="download image to RAM")
    parser.add_argument("--reset", dest="reset", action="store_true", help="reset cpu after download")
    parser.add_argument("--efuse_encrypted", dest="efuse_encrypted", help="encrypted data to write")
    parser.add_argument("--addr", dest="addr", help="address to write")
    parser.add_argument("--whole_chip", dest="whole_chip", action="store_true", help="indicate erase whole flash")
    return parser


class BflbEflashLoader(object):
    def __init__(self):
        self._temp_task_num = None

    def print_error_code(self, code):
        bflb_utils.set_error_code(code, self._temp_task_num)
        bflb_utils.printf(
            '{"ErrorCode": "{0}","ErrorMsg":"{1}"}'.format(code, bflb_utils.eflash_loader_error_code[code])
        )

    def get_chip_type(self, interface, device, chip_type, callback):
        if interface.lower() == "uart" or interface == "sdio":
            boot_speed = 500000
        else:
            if chip_type == "bl606p":
                return "bl808"
            return chip_type
        _bflb_com_img_loader = bflb_img_loader.BflbImgLoader(
            device, boot_speed, boot_speed, interface.lower(), callback=callback
        )
        bflb_serial_object = _bflb_com_img_loader.bflb_serial_object
        try:
            ret, bootinfo = _bflb_com_img_loader.img_get_bootinfo(
                boot_speed,
                boot_speed,
                callback=callback,
                do_reset=True,
                reset_hold_time=5,
                shake_hand_delay=100,
                reset_revert=False,
                cutoff_time=100,
                shake_hand_retry=2,
                isp_mode_sign=False,
                isp_timeout=0,
                boot_load=True,
            )
            bootinfo = bootinfo.decode("utf-8")
            bflb_serial_object.close()

            if ret is False:
                _bflb_com_img_loader = bflb_img_loader.BflbImgLoader(
                    device,
                    boot_speed,
                    boot_speed,
                    interface.lower(),
                    "bl808",
                    callback=callback,
                )
                bflb_serial_object = _bflb_com_img_loader.bflb_serial_object
                ret, bootinfo = _bflb_com_img_loader.img_get_bootinfo(
                    boot_speed,
                    boot_speed,
                    callback=callback,
                    do_reset=True,
                    reset_hold_time=5,
                    shake_hand_delay=100,
                    reset_revert=False,
                    cutoff_time=100,
                    shake_hand_retry=2,
                    isp_mode_sign=False,
                    isp_timeout=0,
                    boot_load=True,
                )
                bootinfo = bootinfo.decode("utf-8")
                bflb_serial_object.close()
                if ret is False:
                    self.print_error_code("0003")
                    return "Error: Can not detect the chip type"

            if "01000000" in bootinfo:
                return "bl602"
            elif "01000207" in bootinfo:
                return "bl702"
            elif "01001606" in bootinfo:
                return "bl616"
            elif "01000808" in bootinfo:
                return "bl808"
            else:
                return "Error: Can not detect the chip type"
        except Exception:
            self.print_error_code("0003")
            return "Error: Can not detect the chip type"

    def pre_process(self, config):
        ret = True
        pre_program = config["param"]["pre_program"]
        pre_program_args = config["param"]["pre_program_args"]
        cpu_id = config["param"]["cpu_id"]
        if "input_path" in config:
            if "config" in config["input_path"]:
                cfg = config["input_path"]["config"]
                cfg_path = os.path.abspath(os.path.dirname(cfg))
                if pre_program:
                    try:
                        if platform == "windows":
                            exe = os.path.join(cfg_path, pre_program + ".exe")
                        elif platform == "linux":
                            exe = os.path.join(cfg_path, pre_program + "-ubuntu")
                        elif platform == "macos":
                            exe = os.path.join(cfg_path, pre_program + "-macos")
                        args = pre_program_args.split()
                        for i in range(len(args)):
                            if cpu_id:
                                args[i] = args[i].replace(
                                    "$(CHIPNAME)",
                                    config["param"]["chip_name"] + "_" + cpu_id,
                                )
                            else:
                                args[i] = args[i].replace("$(CHIPNAME)", config["param"]["chip_name"])
                            s = args[i].split("=")
                            if len(s) == 1:
                                arg = ""
                                filename1 = s[0]
                            else:
                                arg = s[0] + "="
                                filename1 = s[-1]
                            m = args[i].find("*")
                            try:
                                if m != -1:
                                    dir1 = os.path.dirname(os.path.join(cfg_path, filename1))
                                    dir2 = os.path.dirname(filename1)
                                    for file in os.listdir(dir1):
                                        filename2 = os.path.join(dir2, file)
                                        if fnmatch(filename2, filename1):
                                            args[i] = arg + os.path.join(dir1, file)
                                else:
                                    path = os.path.join(cfg_path, filename1)
                                    if os.path.exists(path):
                                        args[i] = arg + path
                            except Exception as error:
                                pass
                        bflb_utils.printf("Start pre programming")
                        bflb_utils.printf("The exe file is {}".format(exe))
                        bflb_utils.printf("The args are {}".format(args))
                        cmd = [exe] + args
                        cmd = " ".join(cmd)
                        p = subprocess.run(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                        )
                        res = p.returncode
                        if res == 0:
                            print(p.stdout.decode("utf-8", "ignore"))
                            bflb_utils.printf("Pre programming completed successfully")
                        else:
                            print(p.stdout.decode("utf-8", "ignore"))
                            print(p.stderr.decode("utf-8", "ignore"))
                            ret = False
                    except Exception as error:
                        bflb_utils.printf(error)
                        # traceback.print_exc(limit=5, file=sys.stdout)
                        ret = False
                    finally:
                        return ret
                else:
                    return True
        return ret

    def post_process(self, eflash_loader_obj, result, args, start_time):
        if result == "repeat_burn":
            eflash_loader_obj.close_serial()
            return "repeat_burn"
        if eflash_loader_obj.cpu_reset is True:
            bflb_utils.printf("Reset cpu")
            eflash_loader_obj.base_reset_cpu()
        if eflash_loader_obj.retry_delay_after_cpu_reset > 0:
            bflb_utils.printf(
                "Delay for uart timeout: ",
                eflash_loader_obj.retry_delay_after_cpu_reset,
            )
            time.sleep(eflash_loader_obj.retry_delay_after_cpu_reset)
        if result is True:
            time_cost = (time.time() * 1000) - start_time
            bflb_utils.printf("Total time cost(ms): {}".format(round(time_cost, 3)))
            time.sleep(0.1)
            if not args.none and eflash_loader_obj.bflb_serial_object is not None:
                eflash_loader_obj.close_serial()
            bflb_utils.printf("Close interface")
            bflb_utils.printf("All programming completed successfully")
            bflb_utils.local_log_save("log", eflash_loader_obj.input_macaddr)
            if eflash_loader_obj.bflb_serial_object is not None:
                eflash_loader_obj.close_serial()
            return True
        else:
            if eflash_loader_obj.bflb_serial_object is not None:
                eflash_loader_obj.close_serial()
            bflb_utils.printf("All programming failed")
            return False

    def reg_read_thread(self, config, callback=None):
        chip_type = config["param"]["chip_type"]
        try:
            bflb_utils.set_error_code("FFFF")
            eflash_loader_cfg_tmp = os.path.join(bflb_utils.chip_path, chip_type, "eflash_loader/eflash_loader_cfg.ini")
            options = ["--none", "--flash", "-c", eflash_loader_cfg_tmp]
            parser_eflash = bflb_utils.eflash_loader_parser_init()
            args = parser_eflash.parse_args(options)
            config["param"]["chip_xtal"] = "auto"
            if chip_type == "bl602":
                config["param"]["chip_xtal"] = "40m"
                eflash_loader_obj = BL602EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702l":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702LEflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl808" or chip_type == "bl606p":
                eflash_loader_obj = BL808EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl616" or chip_type == "bl616l" or chip_type == "bl616d":
                eflash_loader_obj = BL616EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl628":
                eflash_loader_obj = BL628EflashLoader(chip_type, args, config, callback)
            else:
                eflash_loader_obj = OtherEflashLoader(chip_type, args, config, callback)
            result, content = eflash_loader_obj.run_step()
            eflash_loader_obj.clear_object_status()
            cmd = config["flash"]["cmd"]
            if not bflb_utils.is_hex(cmd):
                eflash_loader_obj.close_serial()
                ret = "Error: Register read command value is not hex"
                bflb_utils.printf(ret)
                return False, ret
            length = config["flash"]["len"]
            if not length.isdigit():
                eflash_loader_obj.close_serial()
                ret = "Error: Register read length is incorrect"
                bflb_utils.printf(ret)
                return False, ret
            else:
                length = int(length)
            cmd_value = int(cmd, 16)
            if cmd_value != 0x05 and cmd_value != 0x35 and cmd_value != 0x15:
                eflash_loader_obj.close_serial()
                ret = "Error: Register read command value is incorrect"
                bflb_utils.printf(ret)
                return False, ret
            if length > 3:
                eflash_loader_obj.close_serial()
                ret = "Error: Register read length is too long"
                bflb_utils.printf(ret)
                return False, ret
            ret, data = eflash_loader_obj.flash_read_status_reg_process(cmd, length)
            if ret:
                data = binascii.hexlify(data).decode("utf-8")
                bflb_utils.printf("Successfully read register")
            else:
                bflb_utils.printf("Failed to read register")
            if eflash_loader_obj.bflb_serial_object is not None:
                eflash_loader_obj.close_serial()
            self._temp_task_num = eflash_loader_obj.task_num
            return ret, data
        except Exception as error:
            ret = str(error)
            bflb_utils.printf("Error: {}".format(ret))
            return False, ret

    def reg_write_thread(self, config, callback=None):
        ret = None
        interface = config["param"]["interface_type"]
        device = config["param"]["comport_uart"]
        chip_type = config["param"]["chip_type"]
        try:
            if not device and interface.lower() == "uart":
                ret = '{"ErrorCode":"FFFF","ErrorMsg":"BFLB INTERFACE HAS NO COM PORT"}'
                bflb_utils.printf(ret)
                return False, ret
            bflb_utils.set_error_code("FFFF")
            eflash_loader_cfg_tmp = os.path.join(bflb_utils.chip_path, chip_type, "eflash_loader/eflash_loader_cfg.ini")
            options = ["--none", "--flash", "-c", eflash_loader_cfg_tmp]
            parser_eflash = bflb_utils.eflash_loader_parser_init()
            args = parser_eflash.parse_args(options)
            config["param"]["chip_xtal"] = "auto"
            if chip_type == "bl602":
                config["param"]["chip_xtal"] = "40m"
                eflash_loader_obj = BL602EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702l":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702LEflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl808" or chip_type == "bl606p":
                eflash_loader_obj = BL808EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl616" or chip_type == "bl616l" or chip_type == "bl616d":
                eflash_loader_obj = BL616EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl628":
                eflash_loader_obj = BL628EflashLoader(chip_type, args, config, callback)
            else:
                eflash_loader_obj = OtherEflashLoader(chip_type, args, config, callback)
            # eflash_loader_obj.set_config_file(efuse_boothd_cfg, img_create_cfg)
            result, content = eflash_loader_obj.run_step()
            eflash_loader_obj.clear_object_status()
            cmd = config["flash"]["cmd"]
            if not bflb_utils.is_hex(cmd):
                eflash_loader_obj.close_serial()
                ret = "Error: Register write command value is not hex"
                bflb_utils.printf(ret)
                return False, ret
            length = config["flash"]["len"]
            if not length.isdigit():
                eflash_loader_obj.close_serial()
                ret = "Error: Register write length is incorrect"
                bflb_utils.printf(ret)
                return False, ret
            else:
                length = int(length)
            cmd_value = int(cmd, 16)
            val = config["flash"]["val"]
            if len(val) == 0:
                eflash_loader_obj.close_serial()
                ret = "Error: Register write value is null"
                bflb_utils.printf(ret)
                return False, ret
            if cmd_value != 0x01 and cmd_value != 0x31 and cmd_value != 0x11:
                eflash_loader_obj.close_serial()
                ret = "Error: Register write command value is incorrect"
                bflb_utils.printf(ret)
                return False, ret
            if length > 3:
                eflash_loader_obj.close_serial()
                ret = "Error: Register write length is too long"
                bflb_utils.printf(ret)
                return False, ret
            ret, data = eflash_loader_obj.flash_write_status_reg_process(cmd, length, val)
            if ret:
                bflb_utils.printf("Successfully write register")
            else:
                bflb_utils.printf("Failed to write register")
            eflash_loader_obj.close_serial()
            self._temp_task_num = eflash_loader_obj.task_num
            return ret, data
        except Exception as error:
            ret = str(error)
            bflb_utils.printf("Error: {}".format(ret))
            return False, ret

    def efuse_read_thread(self, config, callback=None, cmdline=None):
        ret = None
        interface = config["param"]["interface_type"]
        device = config["param"]["comport_uart"]
        chip_type = config["param"]["chip_type"]
        try:
            if not device and interface.lower() == "uart":
                ret = '{"ErrorCode":"FFFF","ErrorMsg":"BFLB INTERFACE HAS NO COM PORT"}'
                bflb_utils.printf(ret)
                return False, ret
            bflb_utils.set_error_code("FFFF")
            start_time = time.time() * 1000
            eflash_loader_cfg_tmp = os.path.join(bflb_utils.chip_path, chip_type, "eflash_loader/eflash_loader_cfg.ini")
            if bflb_utils.verify_hex_num(config["flash"]["start_addr"][2:]) is True:
                if config["flash"]["start_addr"][0:2] == "0x":
                    start = config["flash"]["start_addr"][2:]
                else:
                    bflb_utils.printf("Error: The start addr is hex data, it must begin with 0x")
                    ret = "The start addr is hex data, it must begin with 0x"
                    return ret
            else:
                bflb_utils.printf("Error: Please check the start addr hex data")
                ret = "Please check the start addr hex data"
                return ret
            if bflb_utils.verify_hex_num(config["flash"]["end_addr"][2:]) is True:
                if config["flash"]["end_addr"][0:2] == "0x":
                    end = config["flash"]["end_addr"][2:]
                else:
                    bflb_utils.printf("Error: The end addr is hex data, must begin with 0x")
                    ret = "The end addr is hex data, must begin with 0x"
                    return ret
            else:
                bflb_utils.printf("Error: Please check the end addr hex data")
                ret = "Please check the end addr hex data"
                return ret
            if int(start, 16) >= int(end, 16):
                bflb_utils.printf("Error: The start addr must be less than the end addr")
                ret = "The start addr must be less than the end addr"
                return ret
            if config.get("file") is not None:
                file_name = config["file"]
            else:
                file_name = "flash.bin"
            bflb_utils.printf("Save as {}".format(file_name))
            options = [
                "--read",
                "--efuse",
                "--start=" + start,
                "--end=" + end,
                "--file=" + file_name,
                "-c",
                eflash_loader_cfg_tmp,
            ]
            bflb_utils.printf("The args are {}".format(options))
            parser_eflash = bflb_utils.eflash_loader_parser_init()
            args = parser_eflash.parse_args(options)
            config["param"]["chip_xtal"] = "auto"
            if chip_type == "bl602":
                config["param"]["chip_xtal"] = "40m"
                eflash_loader_obj = BL602EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702l":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702LEflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl808" or chip_type == "bl606p":
                eflash_loader_obj = BL808EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl616" or chip_type == "bl616l" or chip_type == "bl616d":
                eflash_loader_obj = BL616EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl628":
                eflash_loader_obj = BL628EflashLoader(chip_type, args, config, callback)
            else:
                eflash_loader_obj = OtherEflashLoader(chip_type, args, config, callback)
            result, content = eflash_loader_obj.run_step()
            eflash_loader_obj.clear_object_status()
            self._temp_task_num = eflash_loader_obj.task_num
            res = self.post_process(eflash_loader_obj, result, args, start_time)
            if res:
                return True
            bflb_utils.local_log_save("log", eflash_loader_obj.input_macaddr)
            ret = bflb_utils.get_error_code_msg(self._temp_task_num)
        except Exception as error:
            ret = str(error)
        finally:
            if ret:
                if cmdline:
                    sys.exit(1)
                else:
                    return ret
            else:
                return True

    def flash_read_thread(self, config, callback=None, cmdline=None):
        ret = None
        interface = config["param"]["interface_type"]
        device = config["param"]["comport_uart"]
        chip_type = config["param"]["chip_type"]
        try:
            if not device and interface.lower() == "uart":
                ret = '{"ErrorCode":"FFFF","ErrorMsg":"BFLB INTERFACE HAS NO COM PORT"}'
                bflb_utils.printf(ret)
                return False, ret
            bflb_utils.set_error_code("FFFF")
            start_time = time.time() * 1000
            eflash_loader_cfg_tmp = os.path.join(bflb_utils.chip_path, chip_type, "eflash_loader/eflash_loader_cfg.ini")

            if config.get("file") is not None:
                file_name = config["file"]
            else:
                file_name = "flash.bin"
            bflb_utils.printf("Save as {}".format(file_name))

            if "flash_otp" in config["flash"] and config["flash"]["flash_otp"]:
                options_memory_type = "--flash_otp"
            else:
                options_memory_type = "--flash"

            if "mode" in config["flash"]:
                if config["flash"]["mode"] == "index":
                    config["otpindex"] = config["flash"]["otpindex1"]
                    options = [
                        "--read",
                        options_memory_type,
                        "--file=" + file_name,
                        "-c",
                        eflash_loader_cfg_tmp,
                    ]
                else:
                    start = config["flash"]["start_addr"]
                    if not bflb_utils.is_hex(start):
                        ret = "The start addr is not hex"
                        bflb_utils.printf("Error: ", ret)
                        return ret
                    end = config["flash"]["end_addr"]
                    if not bflb_utils.is_hex(end):
                        ret = "The end addr is not hex"
                        bflb_utils.printf("Error: ", ret)
                        return ret
                    if int(start, 16) >= int(end, 16):
                        bflb_utils.printf("Error: The start addr must be less than the end addr")
                        ret = "The start addr must be less than the end addr"
                        return ret
                    config["otpindex"] = None
                    options = [
                        "--read",
                        options_memory_type,
                        "--start=" + start,
                        "--end=" + end,
                        "--file=" + file_name,
                        "-c",
                        eflash_loader_cfg_tmp,
                    ]
                if "lock" in config["flash"]:
                    if config["flash"]["lock"] is True:
                        options.extend(["--lock"])

            bflb_utils.printf("The args are {}".format(options))
            parser_eflash = bflb_utils.eflash_loader_parser_init()
            args = parser_eflash.parse_args(options)
            config["param"]["chip_xtal"] = "auto"
            if chip_type == "bl602":
                config["param"]["chip_xtal"] = "40m"
                eflash_loader_obj = BL602EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702l":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702LEflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl808" or chip_type == "bl606p":
                eflash_loader_obj = BL808EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl616" or chip_type == "bl616l" or chip_type == "bl616d":
                eflash_loader_obj = BL616EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl628":
                eflash_loader_obj = BL628EflashLoader(chip_type, args, config, callback)
            else:
                eflash_loader_obj = OtherEflashLoader(chip_type, args, config, callback)
            result, content = eflash_loader_obj.run_step()
            eflash_loader_obj.clear_object_status()
            self._temp_task_num = eflash_loader_obj.task_num
            res = self.post_process(eflash_loader_obj, result, args, start_time)
            if res:
                return True
            bflb_utils.local_log_save("log", eflash_loader_obj.input_macaddr)
            ret = bflb_utils.get_error_code_msg(self._temp_task_num)
        except Exception as error:
            ret = str(error)
        finally:
            if ret:
                if cmdline:
                    sys.exit(1)
                else:
                    return ret
            else:
                return True

    def flash_read_id_thread(self, config, callback=None):
        chip_type = config["param"]["chip_type"]
        try:
            bflb_utils.set_error_code("FFFF")
            eflash_loader_cfg_tmp = os.path.join(bflb_utils.chip_path, chip_type, "eflash_loader/eflash_loader_cfg.ini")
            options = ["--none", "--flash", "-c", eflash_loader_cfg_tmp]
            parser_eflash = bflb_utils.eflash_loader_parser_init()
            args = parser_eflash.parse_args(options)
            config["param"]["chip_xtal"] = "auto"
            if chip_type == "bl602":
                config["param"]["chip_xtal"] = "40m"
                eflash_loader_obj = BL602EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702l":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702LEflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl808" or chip_type == "bl606p":
                eflash_loader_obj = BL808EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl616" or chip_type == "bl616l" or chip_type == "bl616d":
                eflash_loader_obj = BL616EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl628":
                eflash_loader_obj = BL628EflashLoader(chip_type, args, config, callback)
            else:
                eflash_loader_obj = OtherEflashLoader(chip_type, args, config, callback)
            result, content = eflash_loader_obj.run_step()
            ret, data = eflash_loader_obj.flash_read_jedec_id_process()
            eflash_loader_obj.clear_object_status()
            self._temp_task_num = eflash_loader_obj.task_num
            if ret:
                data = binascii.hexlify(data).decode("utf-8")
            if eflash_loader_obj.bflb_serial_object is not None:
                eflash_loader_obj.close_serial()
            return ret, data
        except Exception as error:
            ret = str(error)
            bflb_utils.printf("Error: {}".format(ret))
            return False, ret

    def flash_erase_thread(self, config, callback=None, cmdline=None):
        options = ""
        start = ""
        end = ""
        ret = None
        chip_type = config["param"]["chip_type"]
        start_time = time.time() * 1000
        try:
            eflash_loader_cfg_tmp = os.path.join(bflb_utils.chip_path, chip_type, "eflash_loader/eflash_loader_cfg.ini")
            if config["flash"]["whole_chip"] is True:
                options = ["--erase", "--flash", "--end=0", "-c", eflash_loader_cfg_tmp]
            else:
                if "flash_otp" in config["flash"] and config["flash"]["flash_otp"]:
                    options_memory_type = "--flash_otp"
                else:
                    options_memory_type = "--flash"

                if "mode" in config["flash"]:
                    if config["flash"]["mode"] == "index":
                        config["otpindex"] = config["flash"]["otpindex1"]
                        options = [
                            "--erase",
                            options_memory_type,
                            "-c",
                            eflash_loader_cfg_tmp,
                        ]
                    else:
                        start = config["flash"]["start_addr"]
                        if not bflb_utils.is_hex(start):
                            if config["flash"]["whole_chip"] is False:
                                ret = "The start addr is not hex"
                                bflb_utils.printf("Error: ", ret)
                                return ret
                        end = config["flash"]["end_addr"]
                        if not bflb_utils.is_hex(end):
                            if config["flash"]["whole_chip"] is False:
                                ret = "The end addr is not hex"
                                bflb_utils.printf("Error: ", ret)
                                return ret
                        config["otpindex"] = None
                        options = [
                            "--erase",
                            options_memory_type,
                            "--start=" + start,
                            "--end=" + end,
                            "-c",
                            eflash_loader_cfg_tmp,
                        ]
                    if "lock" in config["flash"]:
                        if config["flash"]["lock"] is True:
                            options.extend(["--lock"])
            bflb_utils.printf("The args are {}".format(options))
            parser_eflash = bflb_utils.eflash_loader_parser_init()
            args = parser_eflash.parse_args(options)
            config["param"]["chip_xtal"] = "auto"
            if chip_type == "bl602":
                config["param"]["chip_xtal"] = "40m"
                eflash_loader_obj = BL602EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl702l":
                config["param"]["chip_xtal"] = "32m"
                eflash_loader_obj = BL702LEflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl808" or chip_type == "bl606p":
                eflash_loader_obj = BL808EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl616" or chip_type == "bl616l" or chip_type == "bl616d":
                eflash_loader_obj = BL616EflashLoader(chip_type, args, config, callback)
            elif chip_type == "bl628":
                eflash_loader_obj = BL628EflashLoader(chip_type, args, config, callback)
            else:
                eflash_loader_obj = OtherEflashLoader(chip_type, args, config, callback)
            result, content = eflash_loader_obj.run_step()
            eflash_loader_obj.clear_object_status()
            self._temp_task_num = eflash_loader_obj.task_num
            res = self.post_process(eflash_loader_obj, result, args, start_time)
            if res:
                return True
            bflb_utils.local_log_save("log", eflash_loader_obj.input_macaddr)
            ret = bflb_utils.get_error_code_msg(self._temp_task_num)
        except Exception as error:
            bflb_utils.printf(error)
            ret = str(e)
        finally:
            if ret:
                if cmdline:
                    sys.exit(1)
                else:
                    return ret
            else:
                return True

    def flash_write_thread(self, mode, config, callback=None, cmdline=None):
        ret = None
        if "file" in config:
            if config["file"]:
                mode = "single"
        if "firmware" in config:
            mode = "single"
        if mode != "single":
            res = self.pre_process(config)
            if not res:
                ret = "Pre programming failed"
                return ret
        flash_burn_retry = 1
        bflb_utils.clear_global()
        try:
            chip_type = config["param"]["chip_type"]
            options = ["--write"]
            if mode == "multiple" or mode == "single":
                if "flash" in config:
                    if "flash_otp" in config["flash"] and config["flash"]["flash_otp"]:
                        options.extend(["--flash_otp"])
                        options.extend(["--erase"])
                    else:
                        options.extend(["--flash"])
                    if "whole_chip" in config["flash"]:
                        if config["flash"]["whole_chip"] is True:
                            config["param"]["erase"] = 2
                    if "mode" in config["flash"]:
                        if config["flash"]["mode"] == "index":
                            config["otpindex"] = config["flash"]["otpindex2"]
                        else:
                            config["otpindex"] = None
                    if "lock" in config["flash"]:
                        if config["flash"]["lock"] is True:
                            options.extend(["--lock"])
                else:
                    options.extend(["--flash"])
                if "check_box" in config:
                    if "efuse" in config["check_box"] and config["check_box"]["efuse"]:
                        if not config["input_path"]["efuse"]:
                            ret = "No efuse file found"
                            return ret
                        else:
                            options.extend(["--efuse"])
                parser_eflash = bflb_utils.eflash_loader_parser_init()
                args = parser_eflash.parse_args(options)
                bflb_utils.printf("The args are {}".format(options))
                start_time = time.time() * 1000
                if "Error" in chip_type:
                    ret = "Chip type is unknown"
                    return ret
                config["param"]["chip_xtal"] = "auto"
                if chip_type == "bl602":
                    config["param"]["chip_xtal"] = "40m"
                    eflash_loader_obj = BL602EflashLoader(chip_type, args, config, callback)
                elif chip_type == "bl702":
                    config["param"]["chip_xtal"] = "32m"
                    eflash_loader_obj = BL702EflashLoader(chip_type, args, config, callback)
                elif chip_type == "bl702l":
                    config["param"]["chip_xtal"] = "32m"
                    eflash_loader_obj = BL702LEflashLoader(chip_type, args, config, callback)
                elif chip_type == "bl808" or chip_type == "bl606p":
                    eflash_loader_obj = BL808EflashLoader(chip_type, args, config, callback)
                elif chip_type == "bl616" or chip_type == "bl616l" or chip_type == "bl616d":
                    eflash_loader_obj = BL616EflashLoader(chip_type, args, config, callback)
                elif chip_type == "bl628":
                    eflash_loader_obj = BL628EflashLoader(chip_type, args, config, callback)
                else:
                    eflash_loader_obj = OtherEflashLoader(chip_type, args, config, callback)
                while flash_burn_retry:
                    if eflash_loader_obj.bflb_serial_object is not None:
                        eflash_loader_obj.close_serial()
                    bflb_utils.printf("Start programming")
                    result, content = eflash_loader_obj.run_step()
                    self._temp_task_num = eflash_loader_obj.task_num
                    res = self.post_process(eflash_loader_obj, result, args, start_time)
                    if res:
                        return True
                    else:
                        flash_burn_retry -= 1
                        if flash_burn_retry:
                            bflb_utils.printf("Writing retry")
                bflb_utils.local_log_save("log", eflash_loader_obj.input_macaddr)
                ret = bflb_utils.get_error_code_msg(self._temp_task_num)
        except Exception as error:
            traceback.print_exc(limit=NUM_ERROR_LOG, file=sys.stdout)
            ret = str(error)
        finally:
            if ret:
                if cmdline:
                    sys.exit(1)
                else:
                    return ret
            else:
                return True

    def ram_download_thread(self, config, callback=None, cmdline=None):
        ret = None
        start_time = time.time() * 1000
        try:
            chip_type = config["param"]["chip_type"]
            chip_name = config["param"]["chip_name"]
            config_file = os.path.join(
                app_path,
                "chips",
                chip_type.lower(),
                "eflash_loader",
                "eflash_loader_cfg.ini",
            )
            if not os.path.exists(config_file):
                conf_file = config_file.replace(".ini", ".conf")
                if os.path.exists(conf_file):
                    shutil.copy(conf_file, config_file)
            if os.path.exists(config_file):
                cfg = BFConfigParser()
                cfg.read(config_file)
            else:
                bflb_utils.printf("Config file is not found")
                bflb_utils.local_log_save("log")
                ret = bflb_utils.get_error_code_msg(self._temp_task_num)
                return ret
            interface = config["param"]["interface_type"].lower()
            if interface == "openocd":
                device = cfg.get("LOAD_CFG", "openocd_config")
                speed = config["param"]["speed_jlink"]
            elif interface == "cklink":
                device = cfg.get("LOAD_CFG", "cklink_vidpid")
                speed = config["param"]["speed_jlink"]
            else:
                device = config["param"]["comport_uart"]
                speed = config["param"]["speed_uart"]
            ram_file = config["firmware"]["path"]
            speed = int(speed)
            pwd = None
            if cfg.has_option("LOAD_CFG", "password"):
                pwd = cfg.get("LOAD_CFG", "password")

            _bflb_com_img_loader = bflb_img_loader.BflbImgLoader(
                device, speed, 500000, interface, chip_type, chip_name, ram_file, "", None, True, pwd=pwd  # do reset
            )
            ret, bootinfo, res = _bflb_com_img_loader.img_load_process(
                speed, speed, None, True, reset_revert=False, post_proc=True
            )
            if ret is False:
                bflb_utils.printf("Ram load failed")
                bflb_utils.local_log_save("log")
                ret = bflb_utils.get_error_code_msg(self._temp_task_num)
            else:
                ret = None
                time_cost = (time.time() * 1000) - start_time
                bflb_utils.printf("Total time cost(ms): {}".format(round(time_cost, 3)))
        except Exception as error:
            bflb_utils.printf(error)
            ret = str(e)
        finally:
            if ret:
                if cmdline:
                    sys.exit(1)
                else:
                    return ret
            else:
                return True


class MainClass:
    def __init__(self):
        self.dict_chip = {
            "BL602": ("bl602", "bl602"),
            "BL702": ("bl702", "bl702"),
            "BL702L": ("bl702l", "bl702l"),
            "BL808": ("bl808", "bl808"),
            "BL606P": ("bl606p", "bl808"),
            "BL616": ("bl616", "bl616"),
            "BL628": ("bl628", "bl628"),
            "BL616L": ("bl616l", "bl616l"),
            "BL616D": ("bl616d", "bl616d"),
        }

    def get_addr_from_partition_by_name(self, name, parition_file, index):
        try:
            with open(parition_file, "rb") as fp:
                data = bytearray(fp.read())
                start = data.find(name.encode("utf-8"))
                if start != -1:
                    addr = data[start + 9 + index * 4 : start + 9 + 4 + index * 4]
                    addr.reverse()
                    addr = hex(int(binascii.hexlify(addr), 16))
                    return True, addr
                else:
                    return False, "0"
        except Exception as error:
            bflb_utils.printf(error)
            return False, "0"

    def get_size_from_partition_by_name(self, name, parition_file, index):
        try:
            with open(parition_file, "rb") as fp:
                data = bytearray(fp.read())
                start = data.find(name.encode("utf-8"))
                if start != -1:
                    size = data[start + 17 + index * 4 : start + 17 + 4 + index * 4]
                    size.reverse()
                    size = int(binascii.hexlify(size), 16)
                    return True, size
                else:
                    return False, "0"
        except Exception as error:
            bflb_utils.printf(error)
            return False, "0"

    def get_value(self, args):
        self.config = {}
        self.config["param"] = {}
        self.config["flash"] = {}
        self.config["check_box"] = {}
        self.config["input_path"] = {}
        self.config["param"]["interface_type"] = args.interface
        self.config["param"]["comport_uart"] = args.port
        self.config["param"]["chip"] = args.chipname.lower()
        if args.chipname.upper() not in self.dict_chip:
            bflb_utils.printf("Error: The chip name {} is incorrect".format(args.chipname))
            return None
        chip = self.dict_chip[args.chipname.upper()]
        self.config["param"]["chip_name"] = chip[0]
        self.config["param"]["chip_type"] = chip[1]
        self.config["param"]["speed_uart"] = 2000000
        self.config["param"]["speed_jlink"] = 1000
        if args.interface.lower() == "uart":
            self.config["param"]["speed_uart"] = args.baudrate
        else:
            if args.baudrate == 2000000:
                self.config["param"]["speed_jlink"] = 1000
            else:
                self.config["param"]["speed_jlink"] = args.baudrate
        try:
            self.erase = 1
            self.skip_mode = "0x0, 0x0"
            self.boot2_isp_mode = 0
            self.pre_program = ""
            self.pre_program_args = ""
            if not args.config:
                if args.firmware:
                    args.write = True
                    if not self.get_value_file("firmware", args.firmware, "0x0", args.cpu_id):
                        return None
            else:
                args.write = True
                config = configparser.ConfigParser()
                self.config["input_path"]["config"] = args.config

                if not os.path.exists(os.path.abspath(args.config)):
                    bflb_utils.printf("Error: Config file is not found")
                    return None
                config.read(os.path.abspath(args.config), encoding="utf-8")
                if config:
                    for item in config.sections():
                        if item == "cfg":
                            self.erase = config.get("cfg", "erase", fallback=1)
                            self.skip_mode = config.get("cfg", "skip_mode", fallback="0x0, 0x0")
                            self.boot2_isp_mode = config.get("cfg", "boot2_isp_mode", fallback=0)
                            self.pre_program = config.get("cfg", "pre_program", fallback="")
                            self.pre_program_args = config.get("cfg", "pre_program_args", fallback="")
                        else:
                            filedir = config.get(item, "filedir")
                            address = config.get(item, "address")
                            if not self.get_value_file(item, filedir, address, args.cpu_id):
                                return None
        except Exception as error:
            config = None
            print("ConfigParser Error: {}".format(error))
        finally:
            self.config["param"]["erase"] = self.erase
            self.config["param"]["skip_mode"] = self.skip_mode
            self.config["param"]["boot2_isp_mode"] = self.boot2_isp_mode
            self.config["param"]["pre_program"] = self.pre_program
            self.config["param"]["pre_program_args"] = self.pre_program_args
            self.config["param"]["cpu_id"] = args.cpu_id

        # encrypt and sign
        if args.key:
            self.config["check_box"]["encrypt"] = True
            self.config["param"]["aes_key"] = args.key
            self.config["param"]["aes_iv"] = args.iv
        else:
            self.config["check_box"]["encrypt"] = False
            self.config["param"]["aes_key"] = ""
            self.config["param"]["aes_iv"] = ""
        self.config["check_box"]["sign"] = False
        if args.sk:
            self.config["check_box"]["sign"] = True
            self.config["input_path"]["publickey"] = args.pk
            self.config["input_path"]["privatekey"] = args.sk
        else:
            self.config["input_path"]["publickey"] = ""
            self.config["input_path"]["privatekey"] = ""
        if args.sk_str:
            self.config["check_box"]["sign"] = True
            self.config["param"]["privatekey"] = args.sk_str
            self.config["param"]["publickey"] = args.pk_str
        else:
            self.config["param"]["privatekey"] = ""
            self.config["param"]["publickey"] = ""

        if args.build:
            self.config["param"]["build"] = True

        # flash para
        if args.start:
            self.config["flash"]["start_addr"] = args.start
        else:
            self.config["flash"]["start_addr"] = "0x0"
        if args.end:
            self.config["flash"]["end_addr"] = args.end
        elif args.len:
            self.config["flash"]["end_addr"] = hex(int(self.config["flash"]["start_addr"], 16) + int(args.len, 16) - 1)
            self.config["flash"]["length"] = args.len
        else:
            self.config["flash"]["end_addr"] = "0x0"
        if args.whole_chip:
            self.config["flash"]["whole_chip"] = True
        else:
            self.config["flash"]["whole_chip"] = False
        if args.flash_otp:
            self.config["flash"]["flash_otp"] = True
        else:
            self.config["flash"]["flash_otp"] = False
        if args.otpindex is not None:
            self.config["flash"]["mode"] = "index"
            self.config["flash"]["otpindex1"] = args.otpindex
            self.config["flash"]["otpindex2"] = args.otpindex
        else:
            self.config["flash"]["mode"] = "address"
            self.config["flash"]["otpindex1"] = None
            self.config["flash"]["otpindex2"] = None
        if args.lock:
            self.config["flash"]["lock"] = True
        else:
            self.config["flash"]["lock"] = False
        if args.file:
            self.config["file"] = args.file

        if (args.flash or args.flash_otp) and args.write:
            if not args.firmware:
                if self.config.get("file") is None:
                    bflb_utils.printf("File input is not found")
                    return None
                else:
                    self.get_value_file(
                        "firmware", self.config["file"], self.config["flash"]["start_addr"], args.cpu_id
                    )

        self.config["check_box"]["efuse"] = False
        self.config["input_path"]["efuse"] = ""
        self.config["param"]["efuse_encrypted"] = ""
        self.config["param"]["start"] = ""
        if args.efusefile:
            args.write = True
            efuse_file = os.path.abspath(args.efusefile)
            if os.path.exists(efuse_file) is False:
                bflb_utils.printf("Efuse file {} is non existent".format(efuse_file))
                return None
            self.config["check_box"]["efuse"] = True
            self.config["input_path"]["efuse"] = os.path.abspath(efuse_file)
            efusefile = self.config["input_path"]["efuse"]
            maskfile = efusefile.replace(".bin", "_mask.bin")
            if os.path.exists(maskfile) is False:
                bflb_utils.printf("Create efuse mask data")
                fp = bflb_utils.open_file(efusefile, "rb")
                efuse_data = fp.read() + bytearray(0)
                fp.close()
                efuse_len = len(efuse_data)
                mask_data = bytearray(efuse_len)
                for i in range(0, efuse_len):
                    if efuse_data[i] != 0:
                        mask_data[i] |= 0xFF
                fp = bflb_utils.open_file(maskfile, "wb+")
                fp.write(mask_data + bytearray(0))
                fp.close()
        elif args.efuse_encrypted and args.addr:
            self.config["check_box"]["efuse"] = True
            self.config["param"]["efuse_encrypted"] = args.efuse_encrypted
            self.config["param"]["start"] = args.addr

        if args.reset:
            self.config["reset"] = args.reset

        return self.config

    def get_value_file(self, name, path, addr, cpu_id=None):
        name = str(name)
        if os.path.isabs(path):
            path = os.path.abspath(path)
        else:
            try:
                config_dir = os.path.dirname(os.path.abspath(self.config["input_path"]["config"]))
                path = os.path.join(config_dir, path)
            except Exception:
                path = os.path.abspath(path)

        if cpu_id:
            path = path.replace("$(CHIPNAME)", self.config["param"]["chip_name"] + "_" + cpu_id)
        else:
            path = path.replace("$(CHIPNAME)", self.config["param"]["chip_name"])
        if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            path = path.replace("\\", "/")
        addr = str(addr)
        # print(name, addr, path)
        self.config[name] = {}
        self.config[name]["addr"] = addr
        self.config[name]["path"] = path

        # judge file path
        if not os.path.exists(path):
            dir_path = os.path.dirname(path)
            file_name = os.path.basename(path)
            try:
                all_file_list = os.listdir(dir_path)
            except Exception as error:
                bflb_utils.printf(error)
                return False
            result = []
            if "*" in file_name:
                file_name = file_name.replace(".", "\\.").replace("*", ".*[\u4e00-\u9fa5]*")
            for one_name in all_file_list:
                pattern = re.compile(file_name)
                temp_list = pattern.findall(one_name)
                if one_name in temp_list:
                    result += temp_list
            if len(result) > 1:
                bflb_utils.printf("Error: Multiple files were matched for {}".format(name))
                return False
            if len(result) == 0:
                error = "Error: Image file matched {} is non existent".format(name)
                bflb_utils.printf(error)
                return False
            else:
                self.config[name]["path"] = os.path.join(dir_path, result[0])

        # check address and size
        if addr.find("@partition") != -1:
            if "partition" in self.config:
                bflb_utils.printf(
                    "{0} get address from partition file {1}".format(name, self.config["partition"]["path"])
                )
                success, addr_pt = self.get_addr_from_partition_by_name(name, self.config["partition"]["path"], 0)
                if not success:
                    bflb_utils.printf("Fail to find {} in partition".format(name))
                    return False
                else:
                    self.config[name]["addr"] = addr_pt
                    bflb_utils.printf("Address = {}".format(addr_pt))
                    addr = addr_pt
                bflb_utils.printf("{0} get size from partition file {1}".format(name, self.config["partition"]["path"]))
                success, size_pt = self.get_size_from_partition_by_name(name, self.config["partition"]["path"], 0)
                if not success:
                    bflb_utils.printf("Fail to find {0} in partition".format(name))
                    return False
                else:
                    self.config[name]["size"] = size_pt
                    bflb_utils.printf("Size = {}".format(size_pt))
                file_size = os.path.getsize(self.config[name]["path"])
                if file_size > size_pt:
                    bflb_utils.printf("Error: {} size exceeds the partition table limit".format(name))
                    return False

        if not bflb_utils.hexstr_to_dec(addr):
            error = "Error: {} is an invalid hexadecimal value".format(addr)
            bflb_utils.printf(error)
            return False

        return True

    def main(self, argv):
        port = None
        ports = []
        for item in bflb_utils.get_serial_ports():
            ports.append(item["port"])
        if ports:
            try:
                port = sorted(ports, key=lambda x: int(re.match("COM(\\d+)", x).group(1)))[0]
            except Exception:
                port = sorted(ports)[0]
        parser = flash_command_parser_init()
        args = parser.parse_args(argv)
        args.interface = "uart"
        if args.port:
            bflb_utils.printf("Serial port is {}".format(args.port))
        elif port:
            bflb_utils.printf("Serial port is {}".format(port))
            args.port = port
        else:
            bflb_utils.printf("Serial port is not found")
        bflb_utils.printf("==================================================")
        config = self.get_value(args)
        if config:
            self.obj = BflbEflashLoader()
            if args.ram:
                ret = self.obj.ram_download_thread(config, None, 1)
                if ret is True or not ret:
                    bflb_utils.printf(ret)
            else:
                # flash operation
                if args.write:
                    self.obj.flash_write_thread("multiple", config, None, 1)
                else:
                    if args.read:
                        if args.efuse:
                            self.obj.efuse_read_thread(config, None, 1)
                        elif args.flash or args.flash_otp:
                            self.obj.flash_read_thread(config, None, 1)
                        else:
                            bflb_utils.printf("Please indicate reading flash or flash_opt or efuse")
                    elif (args.flash or args.flash_otp) and args.erase:
                        ret = self.obj.flash_erase_thread(config, None, 1)
                        if ret is True or not ret:
                            bflb_utils.printf(ret)
        else:
            bflb_utils.printf("Fail to parse para, check your input")


if __name__ == "__main__":
    app = MainClass()
    app.main(sys.argv[1:])
