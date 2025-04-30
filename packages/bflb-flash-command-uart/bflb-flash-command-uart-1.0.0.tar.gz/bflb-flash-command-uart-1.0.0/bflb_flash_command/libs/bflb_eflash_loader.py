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

import os
import sys
import time
import lzma
import shutil
import hashlib
import binascii
import traceback
import zipfile

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature

from libs import bflb_utils
from libs import bflb_ecdh
from libs import bflb_interface_jlink
from libs import bflb_interface_cklink
from libs import bflb_interface_openocd
from libs import bflb_img_loader
from libs import bflb_flash_select
from libs import bflb_img_create as img_create
from libs.bflb_configobj import BFConfigParser

FLASH_LOAD_HANDSHAKE = "Flash load handshake"
FLASH_ERASE_HANDSHAKE = "Flash erase handshake"
PRIVATE_KEY_RSA_HEX = """
2d2d2d2d2d424547494e205253412050524956415445204b45592d2d2d2d2d0a4d49
49435851494241414b426751436b62486e492f62337849384a4951665276434f6378
5146346e6c3541395470326b396a6a6154622b7947412b572b6857790a6c6f516b35
6f33543852574f796e4e30513562656f536a354e665430706e33574964643074792f
7159652f42495a724966576e724c736251584974325a4c55680a6a354a38486b5955
7247584c54497150774e6b4a65454863593235567a5336787764593036742f49376c
44654b70676e46466469326b6d694b774944415141420a416f47414e744874397476
57364e2b31786e617241787779544f4c376f584b7768696841656b41587133315270
52544e6d645a4f78716a5662534972646c63430a6934576e59634f704f5266396537
32494b73755a312f75586845734e7471384f43472b30562b4f4e63624a3967567854
52673636343465343932577470676e470a7a484d656c486e35796e69686541667151
574139463534747266364c53706b64344a6e584d5937335851767664723043515144
434f474b352b5a3943662b62470a426e587877524a454d4d6d74334b764479794548
555445494c3378676f554743535a644d75637375724a47736752492b735847776349
6c434b3646596174696e0a574935474c5a4366416b4541324c6d344c3766444c4b42
5a5776554f4c48576a5248795a67763943716f70673743745873656a33374f796e77
506b2f624662530a732b4f317378486133377a4467623853366147576f35572b5a37
78694543574739514a42414a2b7976587375526b586e35566e75396778544e544863
362f694a0a2b724b4431435377486945633671694a37394f78727a626e6a7170534f
3359637132506868426f5162737836453745674b6756775334786f36774543514466
310a72474e563161562b4f64524d6c6a35516d626d6a5770674368526f33354e4c57
566978763953524e37767261344d392b6b36557a564d564b4250506b623637650a77
576c6c2b646c2f58737932546250526e4d6b435151434c517a704d4d7a485477376d
626c376e497857786c6a39744c393433446158645731415956445542790a72313366
777256646341546542343156617463396d4274584c543366376842484f7338773372
4152513857590a2d2d2d2d2d454e44205253412050524956415445204b45592d2d2d
2d2d"""


class BaseEflashLoader(object):
    """
    Load the flash base execution file.
    """

    def __init__(
        self,
        chip_type,
        args,
        config,
        callback,
        macaddr_callback,
        create_simple_callback,
        create_img_callback,
        task_num,
    ):
        self.chip_type = chip_type
        self.chip_name = ""
        self.args = args
        self.config = config
        self.callback = callback
        self.macaddr_callback = macaddr_callback
        self.create_simple_callback = create_simple_callback
        self.create_img_callback = create_img_callback
        self.temp_task_num = task_num
        self.task_num = None

        self.device = ""
        self.speed = 0
        self.boot_speed = 0  # bootrom device speed
        self.bflb_serial_object = None
        self.start = ""
        self.end = ""
        self.img_file = ""
        self.address = ""
        self.macaddr = ""
        self.bootinfo = None
        self.flash_set = 0
        self.read_flash_id = 0
        self.id_valid_flag = "80"
        self.read_flash2_id = 0
        self.id2_valid_flag = "80"
        self.do_reset = True
        self.reset_hold_time = 100
        self.shake_hand_delay = 100
        self.reset_revert = True
        self.cutoff_time = 0
        self.shake_hand_retry = 2
        self.flash_burn_retry = 1
        self.ram_load = False
        self.load_function = 1
        self.macaddr_check = False
        self.NUM_ERR = 5
        self.cfg = ""
        self.eflash_loader_file = ""
        self.cpu_reset = False
        self.retry_delay_after_cpu_reset = 0
        self.input_macaddr = ""
        self.isp_mode_sign = False  # If isp_mode_sign is True, it will run isp mode
        self.create_cfg = None
        self._skip_addr = []
        self._skip_len = []
        self.address_list = []
        self.flash_file_list = []
        self.encrypt = 0
        self.sign = 0
        self.encrypt_key = None
        self.encrypt_iv = None
        self.public_key = None
        self.private_key = None
        self.public_key_str = None
        self.private_key_str = None
        self.load_file = ""

        self._mac_addr = bytearray(0)
        self._need_handshake = True
        self._isp_shakehand_timeout = 0
        self._macaddr_check = bytearray(0)
        self._default_timeout = 2.0
        self._flash2_en = False
        # self._flash1_size = 0
        # self._flash2_size = 0
        self._flash_size = 64 * 1024 * 1024
        self._flash2_size = 64 * 1024 * 1024
        self._flash_otp_size = 3 * 256 * 256
        self._flash2_select = False
        self._efuse_bootheader_file = ""
        self._img_create_file = ""
        self._com_cmds = {
            "change_rate": {"cmd_id": "20", "data_len": "0008", "callback": None},
            "reset": {"cmd_id": "21", "data_len": "0000", "callback": None},
            "clk_set": {"cmd_id": "22", "data_len": "0000", "callback": None},
            "opt_finish": {"cmd_id": "23", "data_len": "0000", "callback": None},
            "flash_erase": {"cmd_id": "30", "data_len": "0000", "callback": None},
            "flash_write": {"cmd_id": "31", "data_len": "0100", "callback": None},
            "flash_read": {"cmd_id": "32", "data_len": "0100", "callback": None},
            "flash_boot": {"cmd_id": "33", "data_len": "0000", "callback": None},
            "flash_xip_read": {"cmd_id": "34", "data_len": "0100", "callback": None},
            "flash_switch_bank": {"cmd_id": "35", "data_len": "0100", "callback": None},
            "flash_read_jid": {"cmd_id": "36", "data_len": "0000", "callback": None},
            "flash_read_status_reg": {
                "cmd_id": "37",
                "data_len": "0000",
                "callback": None,
            },
            "flash_write_status_reg": {
                "cmd_id": "38",
                "data_len": "0000",
                "callback": None,
            },
            "flash_write_check": {"cmd_id": "3a", "data_len": "0000", "callback": None},
            "flash_set_para": {"cmd_id": "3b", "data_len": "0000", "callback": None},
            "flash_chiperase": {"cmd_id": "3c", "data_len": "0000", "callback": None},
            "flash_readSha": {"cmd_id": "3d", "data_len": "0100", "callback": None},
            "flash_xip_readSha": {"cmd_id": "3e", "data_len": "0100", "callback": None},
            "flash_decompress_write": {
                "cmd_id": "3f",
                "data_len": "0100",
                "callback": None,
            },
            "flash_otp_erase": {"cmd_id": "A0", "data_len": "0000", "callback": None},
            "flash_otp_write": {"cmd_id": "A1", "data_len": "0000", "callback": None},
            "flash_otp_read": {"cmd_id": "A2", "data_len": "0000", "callback": None},
            "flash_otp_set_para": {"cmd_id": "A3", "data_len": "0000", "callback": None},
            "flash_otp_get_para": {"cmd_id": "A4", "data_len": "0000", "callback": None},
            "flash_otp_lock_by_index": {"cmd_id": "A5", "data_len": "0000", "callback": None},
            "flash_otp_lock_by_addr": {"cmd_id": "A6", "data_len": "0000", "callback": None},
            "flash_otp_erase_by_index": {"cmd_id": "A7", "data_len": "0000", "callback": None},
            "flash_otp_write_by_index": {"cmd_id": "A8", "data_len": "0000", "callback": None},
            "flash_otp_read_by_index": {"cmd_id": "A9", "data_len": "0000", "callback": None},
            "efuse_write": {"cmd_id": "40", "data_len": "0080", "callback": None},
            "efuse_read": {"cmd_id": "41", "data_len": "0000", "callback": None},
            "efuse_read_mac": {"cmd_id": "42", "data_len": "0000", "callback": None},
            "efuse_write_mac": {"cmd_id": "43", "data_len": "0006", "callback": None},
            "flash_xip_read_start": {
                "cmd_id": "60",
                "data_len": "0080",
                "callback": None,
            },
            "flash_xip_read_finish": {
                "cmd_id": "61",
                "data_len": "0000",
                "callback": None,
            },
            "log_read": {"cmd_id": "71", "data_len": "0000", "callback": None},
            "efuse_security_write": {
                "cmd_id": "80",
                "data_len": "0080",
                "callback": None,
            },
            "efuse_security_read": {
                "cmd_id": "81",
                "data_len": "0000",
                "callback": None,
            },
            "ecdh_get_pk": {"cmd_id": "90", "data_len": "0000", "callback": None},
            "ecdh_chanllenge": {"cmd_id": "91", "data_len": "0000", "callback": None},
        }
        self._resp_cmds = [
            "flash_read",
            "flash_xip_read",
            "efuse_read",
            "efuse_read_mac",
            "flash_readSha",
            "flash_xip_readSha",
            "flash_read_jid",
            "flash_read_status_reg",
            "flash_otp_read",
            "flash_otp_get_para",
            "log_read",
            "ecdh_get_pk",
            "ecdh_chanllenge",
            "efuse_security_read",
        ]

    def run_step1_load_config(self):
        """
        First step: init.
        """
        load_speed = ""
        if self.temp_task_num is None:
            bflb_utils.local_log_enable(True)
        if self.temp_task_num is not None:
            if self.temp_task_num > 256:
                self.task_num = self.temp_task_num - 256
            else:
                self.task_num = self.temp_task_num
        else:
            self.task_num = None

        bflb_utils.printf("========= eflash loader cmd args =========")
        self.interface = self.config["param"]["interface_type"].lower()
        self.chip_name = self.config["param"]["chip_name"]
        self.config_file = os.path.join(
            bflb_utils.app_path,
            "chips",
            self.chip_name.lower(),
            "eflash_loader",
            "eflash_loader_cfg.ini",
        )

        if not os.path.exists(self.config_file):
            conf_file = self.config_file.replace(".ini", ".conf")
            if os.path.exists(conf_file):
                shutil.copy(conf_file, self.config_file)

        if os.path.exists(self.config_file):
            self.cfg = BFConfigParser()
            self.cfg.read(self.config_file)
        else:
            bflb_utils.printf("Config file is not found")
            self.print_error_code("000B")
            return False, 0

        if self.interface == "openocd":
            self.device = self.cfg.get("LOAD_CFG", "openocd_config")
            self._bflb_sn_device = self.config["param"]["comport_uart"]
        elif self.interface == "cklink":
            self.device = self.cfg.get("LOAD_CFG", "cklink_vidpid")
            self._bflb_sn_device = self.cfg.get("LOAD_CFG", "cklink_type") + " " + self.config["param"]["comport_uart"]
        else:
            self.device = self.config["param"]["comport_uart"]
            self.cfg.set("LOAD_CFG", "device", self.device)

        if "check_box" in self.config:
            if "aes_key" in self.config["param"]:
                if self.config["check_box"]["encrypt"]:
                    self.encrypt_key = self.config["param"]["aes_key"]
            if "aes_iv" in self.config["param"]:
                if self.config["check_box"]["encrypt"]:
                    self.encrypt_iv = self.config["param"]["aes_iv"]
            if "input_path" in self.config and "publickey" in self.config["input_path"]:
                if self.config["check_box"]["sign"]:
                    self.public_key = self.config["input_path"]["publickey"]
            if "input_path" in self.config and "privatekey" in self.config["input_path"]:
                if self.config["check_box"]["sign"]:
                    self.private_key = self.config["input_path"]["privatekey"]
            if "publickey" in self.config["param"]:
                if self.config["check_box"]["sign"]:
                    self.public_key_str = self.config["param"]["publickey"]
            if "privatekey" in self.config["param"]:
                if self.config["check_box"]["sign"]:
                    self.private_key_str = self.config["param"]["privatekey"]
            if self.config["check_box"]["encrypt"]:
                self.encrypt = 1
            if self.config["check_box"]["sign"]:
                self.sign = 1

        self.args.build = False
        if "build" in self.config["param"]:
            if self.config["param"]["build"]:
                self.args.build = True

        xtal_type = self.config["param"]["chip_xtal"]
        if self.interface == "uart":
            if self.config["param"]["speed_uart"]:
                load_speed = int(self.config["param"]["speed_uart"])
            else:
                load_speed = int(self.cfg.get("LOAD_CFG", "speed_uart_load"))
        else:
            if self.config["param"]["speed_jlink"]:
                load_speed = int(self.config["param"]["speed_jlink"])
            else:
                load_speed = int(self.cfg.get("LOAD_CFG", "speed_jlink"))

        # 基础配置回写到eflash_loader_cfg.ini文件
        self.cfg.set("LOAD_CFG", "interface", self.interface)
        self.cfg.set("LOAD_CFG", "speed_uart_load", load_speed)
        self.cfg.write(self.config_file, "w")

        bflb_utils.printf("Serial port is {}".format(self.device))
        bflb_utils.printf("The chip type is {}".format(self.chip_type))
        try:
            if self.args.start:
                self.start = self.args.start
            if self.args.end:
                self.end = self.args.end
            if self.args.file:
                self.img_file = self.args.file
            if self.args.addr:
                self.address = self.args.addr
            if self.args.mac:
                self.macaddr = self.args.mac
            if self.args.createcfg:
                self.create_cfg = self.args.createcfg
            if self.args.loadfile:
                self.load_file = self.args.loadfile
            if self.args.usage:
                bflb_utils.printf("-e --start=00000000 --end=0000FFFF -c config.ini")
                bflb_utils.printf("-w --flash -c config.ini")
                bflb_utils.printf("-w --flash --file=1.bin,2.bin --addr=00000000,00001000 -c config.ini")
                bflb_utils.printf("-r --flash --start=00000000 --end=0000FFFF --file=flash.bin -c config.ini")
        except Exception as error:
            bflb_utils.printf(error)
            self.print_error_code("0002")
            return False, 0

        if self.cfg.has_option("LOAD_CFG", "verify"):
            if self.cfg.get("LOAD_CFG", "verify") == "1":
                self.verify = 1
            else:
                self.verify = 0
        else:
            self.verify = 0

        try:
            self.erase = int(self.config["param"]["erase"])
        except:
            self.erase = 1

        if self.cfg.has_option("LOAD_CFG", "host_rx_timeout"):
            self._default_timeout = int(self.cfg.get("LOAD_CFG", "host_rx_timeout"))
        bflb_utils.printf("The default timeout is {0}s".format(self._default_timeout))

        # Check whether it is in ISP mode
        try:
            boot2_isp_mode = int(self.config["param"]["boot2_isp_mode"])
            if int(boot2_isp_mode) == 1:
                self.isp_mode_sign = True
        except:
            pass
        if "skip_mode" in self.config["param"] and self.config["param"]["skip_mode"]:
            skip_para = self.config["param"]["skip_mode"].replace(" ", "")
            if skip_para[-1] == ";":
                skip_para = skip_para[:-1]
            skip_para_list = skip_para.split(";")
            for temp_value in skip_para_list:
                temp_list = temp_value.split(",")
                if temp_list[0][0:2] == "0x":
                    self._skip_addr.append(int(temp_list[0][2:], 16))
                else:
                    self._skip_addr.append(int(temp_list[0], 10))
                if temp_list[1][0:2] == "0x":
                    self._skip_len.append(int(temp_list[1][2:], 16))
                else:
                    self._skip_len.append(int(temp_list[1], 10))

            if len(self._skip_len) > 1 or (len(self._skip_len) == 1 and self._skip_len[0] > 0):
                if self.erase == 2:
                    bflb_utils.printf("Error: The skip mode can not set flash chiperase")
                    self.print_error_code("0044")
                    return False, 0

        if self.cfg.has_option("LOAD_CFG", "local_log"):
            if self.cfg.get("LOAD_CFG", "local_log") == "true":
                bflb_utils.printf("Enable local log ")
                bflb_utils.local_log_enable(True)
                self.input_macaddr = self.macaddr
            else:
                bflb_utils.local_log_enable(False)
                self.input_macaddr = ""
        if self.interface == "cklink":
            self._bflb_com_tx_size = 14344
        else:
            self._bflb_com_tx_size = int(self.cfg.get("LOAD_CFG", "tx_size"))

        if self.cfg.has_option("LOAD_CFG", "erase_time_out"):
            self._erase_time_out = int(self.cfg.get("LOAD_CFG", "erase_time_out"))
        if self.cfg.has_option("LOAD_CFG", "shake_hand_retry"):
            self.shake_hand_retry = int(self.cfg.get("LOAD_CFG", "shake_hand_retry"))
        if self.cfg.has_option("LOAD_CFG", "flash_burn_retry"):
            self.flash_burn_retry = int(self.cfg.get("LOAD_CFG", "flash_burn_retry"))
        if self.cfg.has_option("LOAD_CFG", "checksum_err_retry"):
            self._checksum_err_retry_limit = int(self.cfg.get("LOAD_CFG", "checksum_err_retry"))
        if self.cfg.has_option("LOAD_CFG", "cpu_reset_after_load"):
            self.cpu_reset = self.cfg.get("LOAD_CFG", "cpu_reset_after_load") == "true"
        if self.cfg.has_option("LOAD_CFG", "retry_delay_after_cpu_reset"):
            self.retry_delay_after_cpu_reset = int(self.cfg.get("LOAD_CFG", "retry_delay_after_cpu_reset"))
            bflb_utils.printf("Retry delay is {}".format(self.retry_delay_after_cpu_reset))
        if self.cfg.has_option("LOAD_CFG", "eflash_loader_file") and self.eflash_loader_file is None:
            self.eflash_loader_file = self.cfg.get("LOAD_CFG", "eflash_loader_file")

        bflb_utils.printf("The cpu reset flag is {}".format(self.cpu_reset))

        if xtal_type != "":
            self.eflash_loader_file = (
                "chips/"
                + self.chip_name.lower()
                + "/eflash_loader/eflash_loader_"
                + xtal_type.replace(".", "p").lower()
                + ".bin"
            )
        if self.load_file and not self.eflash_loader_file:
            self.eflash_loader_file = self.load_file
        elif self.eflash_loader_file is not None:
            self.eflash_loader_file = os.path.join(bflb_utils.app_path, self.eflash_loader_file)

        self.load_function = 1
        if self.cfg.has_option("LOAD_CFG", "isp_shakehand_timeout"):
            self._isp_shakehand_timeout = int(self.cfg.get("LOAD_CFG", "isp_shakehand_timeout"))

        result, address, flash_file = self.get_flash_file_and_address()
        if not result:
            return False, self.flash_burn_retry
        else:
            temp_file_list = []
            for one in flash_file:
                temp_file_list.append(os.path.join("chips", self.chip_name, "img_create", os.path.basename(one)))
            if "erase" in self.config["param"] and self.config["param"]["erase"]:
                bflb_utils.update_cfg(self.cfg, "LOAD_CFG", "erase", str(self.erase))
            if "skip_mode" in self.config["param"] and self.config["param"]["skip_mode"]:
                bflb_utils.update_cfg(self.cfg, "LOAD_CFG", "skip_mode", self.config["param"]["skip_mode"])
                # self.cfg.cfg_obj["LOAD_CFG"]["skip_mode"] = self.config['param']['skip_mode'].replace(' ','')#("LOAD_CFG", "skip_mode", self.config['param']['skip_mode'].replace('"',''))
            if "boot2_isp_mode" in self.config["param"] and self.config["param"]["boot2_isp_mode"]:
                bflb_utils.update_cfg(
                    self.cfg,
                    "LOAD_CFG",
                    "boot2_isp_mode",
                    self.config["param"]["boot2_isp_mode"],
                )
            bflb_utils.update_cfg(self.cfg, "FLASH_CFG", "file", " ".join(temp_file_list))
            bflb_utils.update_cfg(self.cfg, "FLASH_CFG", "address", " ".join(address))
            self.cfg.write(self.config_file, "w+")
            with open(self.config_file, "r", encoding="utf-8") as cf_file:
                cf_context = cf_file.read().replace('"', "")
            with open(self.config_file, "w", encoding="utf-8") as cf_file:
                cf_file.write(cf_context)
            if self.args.write:
                self.write_flash_img(address, flash_file)
        self.address_list = address[:]
        self.flash_file_list = flash_file[:]

        # 获取flash otp的地址
        if self.args.write and self.args.flash_otp:
            self.start = self.address_list[0]
            self.end = hex(int(self.start, 16) + os.path.getsize(self.flash_file_list[0]) - 1)

        if self.args.efuse:
            # 修改burn_en参数值
            if self.cfg.has_option("EFUSE_CFG", "burn_en"):
                bflb_utils.update_cfg(self.cfg, "EFUSE_CFG", "burn_en", "true")
                self.cfg.write(self.config_file, "w+")
            # 从传入参数中获取efuse文件路径
            efusefile = ""
            try:
                if self.config["input_path"]["efuse"]:
                    if "check_box" in self.config:
                        if self.config["check_box"]["efuse"]:
                            efusefile = self.config["input_path"]["efuse"]
            except:
                pass

            if efusefile:
                efuse_file = efusefile
                mask_file = efuse_file.replace(".bin", "_mask.bin")
                # 将efuse文件和mask文件的相对路径写入eflash_loader_cfg.ini中
                relpath_efuse_file = os.path.relpath(
                    os.path.join("chips", self.chip_name, "efuse_bootheader/efusedata.bin")
                )
                relpath_mask_file = os.path.relpath(
                    os.path.join("chips", self.chip_name, "efuse_bootheader/efusedata_mask.bin")
                )
                if self.cfg.has_option("EFUSE_CFG", "file"):
                    bflb_utils.update_cfg(self.cfg, "EFUSE_CFG", "file", relpath_efuse_file)
                    bflb_utils.update_cfg(self.cfg, "EFUSE_CFG", "maskfile", relpath_mask_file)
                    self.cfg.write(self.config_file, "w+")

                # 清除eflash_loader_cfg.ini文件中的双引号
                with open(self.config_file, "r", encoding="utf-8") as cf_file:
                    cf_context = cf_file.read().replace('"', "")
                with open(self.config_file, "w", encoding="utf-8") as cf_file:
                    cf_file.write(cf_context)

                # 将传入的efuse文件和mask文件复制到efuse_bootheader目录和img_create目录下，并重命名为efusedata.bin和efusedata_mask.bin
                try:
                    temp_efuse_path = os.path.join(
                        bflb_utils.chip_path, self.chip_name, "efuse_bootheader/efusedata.bin"
                    )
                    temp_mask_path = os.path.join(
                        bflb_utils.chip_path, self.chip_name, "efuse_bootheader/efusedata_mask.bin"
                    )
                    temp_efuse_path_1 = os.path.join(bflb_utils.chip_path, self.chip_name, "img_create/efusedata.bin")
                    temp_mask_path_1 = os.path.join(
                        bflb_utils.chip_path, self.chip_name, "img_create/efusedata_mask.bin"
                    )
                    if os.path.exists(efuse_file):
                        shutil.copyfile(efuse_file, temp_efuse_path)
                        shutil.copyfile(efuse_file, temp_efuse_path_1)
                    else:
                        temp_efuse_path = None
                    if os.path.exists(mask_file):
                        shutil.copyfile(mask_file, temp_mask_path)
                        shutil.copyfile(mask_file, temp_mask_path_1)
                    else:
                        temp_mask_path = None
                except Exception as error:
                    bflb_utils.printf(error)
                    self.print_error_code("0003")
                    return False, self.flash_burn_retry

                if self.temp_task_num is not None:
                    efuse_file = "task" + str(self.temp_task_num) + "/" + efuse_file

                # 生成pack，并将pack放在img_create目录下
                if self.args.write or self.args.build:
                    ret = img_create.compress_dir(
                        self.chip_name,
                        "img_create",
                        self.args.efuse,
                        address,
                        flash_file,
                        temp_efuse_path,
                        temp_mask_path,
                    )
                    if ret is not True:
                        return bflb_utils.get_error_code_msg()
            else:
                efuse_file = self.cfg.get("EFUSE_CFG", "file")
                mask_file = self.cfg.get("EFUSE_CFG", "maskfile")

        else:
            # 修改burn_en参数值
            if self.cfg.has_option("EFUSE_CFG", "burn_en"):
                bflb_utils.update_cfg(self.cfg, "EFUSE_CFG", "burn_en", "false")
                self.cfg.write(self.config_file, "w+")
            # 清除eflash_loader_cfg.ini文件中的双引号
            with open(self.config_file, "r", encoding="utf-8") as cf_file:
                cf_context = cf_file.read().replace('"', "")
            with open(self.config_file, "w", encoding="utf-8") as cf_file:
                cf_file.write(cf_context)
            # 清除efuse_bootheader目录下已有的efusedata.bin和efusedata_mask.bin
            try:
                temp_path = os.path.join(bflb_utils.chip_path, self.chip_name, "efuse_bootheader")
                os.remove(os.path.join(temp_path, "efusedata.bin"))
                os.remove(os.path.join(temp_path, "efusedata_mask.bin"))
            except:
                pass
            # 清除img_create目录下已有的efusedata.bin和efusedata_mask.bin
            try:
                temp_path = os.path.join(bflb_utils.chip_path, self.chip_name, "img_create")
                os.remove(os.path.join(temp_path, "efusedata.bin"))
                os.remove(os.path.join(temp_path, "efusedata_mask.bin"))
            except:
                pass
            # 生成pack，并将pack放在img_create目录下
            if self.args.write or self.args.build:
                ret = img_create.compress_dir(self.chip_name, "img_create", False, address, flash_file)
                if ret is not True:
                    return bflb_utils.get_error_code_msg()
        if (self.encrypt or self.sign) and (self.chip_type == "bl602" or self.chip_type == "bl702"):
            ret, encrypted_data = img_create.encrypt_loader_bin(
                self.chip_type,
                self.eflash_loader_file,
                self.sign,
                self.encrypt,
                self.encrypt_key,
                self.encrypt_iv,
                self.public_key,
                self.private_key,
                privatekey_str=self.private_key_str,
                publickey_str=self.public_key_str,
            )
            if ret is True:
                filename, ext = os.path.splitext(self.eflash_loader_file)
                file_encrypt = filename + "_encrypt" + ext
                with open(file_encrypt, "wb") as fp:
                    fp.write(encrypted_data)
                eflash_loader_file = os.path.basename(self.eflash_loader_file)
                eflash_loader_file = eflash_loader_file.split(".")[0] + "_encrypt.bin"
                zip_file = os.path.join(bflb_utils.chip_path, self.chip_name, "img_create", "whole_img.pack")
                z = zipfile.ZipFile(zip_file, "a")
                z.write(
                    os.path.join(bflb_utils.chip_path, self.chip_name, "eflash_loader", eflash_loader_file),
                    os.path.join(self.chip_name, "eflash_loader", eflash_loader_file),
                )
                z.close()

        if self.args.build:
            return True, "over"

        if self.interface == "uart" or self.interface == "sdio":
            if load_speed:
                self.speed = load_speed
            else:
                self.speed = int(self.cfg.get("LOAD_CFG", "speed_uart_load"))
            bflb_utils.printf("The com speed is {}".format(self.speed))
            self.boot_speed = int(self.cfg.get("LOAD_CFG", "speed_uart_boot"))
            self.set_boot_speed()
            if self.cfg.has_option("LOAD_CFG", "reset_hold_time"):
                self.reset_hold_time = int(self.cfg.get("LOAD_CFG", "reset_hold_time"))
            if self.cfg.has_option("LOAD_CFG", "shake_hand_delay"):
                self.shake_hand_delay = int(self.cfg.get("LOAD_CFG", "shake_hand_delay"))
            if self.cfg.has_option("LOAD_CFG", "do_reset"):
                self.do_reset = self.cfg.get("LOAD_CFG", "do_reset") == "true"
            if self.cfg.has_option("LOAD_CFG", "reset_revert"):
                self.reset_revert = self.cfg.get("LOAD_CFG", "reset_revert") == "true"
            if self.cfg.has_option("LOAD_CFG", "cutoff_time"):
                self.cutoff_time = int(self.cfg.get("LOAD_CFG", "cutoff_time"))
            bflb_utils.printf("========= interface: {} =========".format(self.interface))
            self._bflb_com_img_loader = bflb_img_loader.BflbImgLoader(
                self.device,
                self.speed,
                self.boot_speed,
                self.interface,
                self.chip_type,
                self.chip_name,
                self.eflash_loader_file,
                "",
                self.callback,
                self.do_reset,
                self.reset_hold_time,
                self.shake_hand_delay,
                self.reset_revert,
                self.cutoff_time,
                self.shake_hand_retry,
                self.isp_mode_sign,
                self._isp_shakehand_timeout,
                self.encrypt_key,
                self.encrypt_iv,
                self.public_key,
                self.private_key,
                privatekey_str=self.private_key_str,
                publickey_str=self.public_key_str,
            )
            self.bflb_serial_object = self._bflb_com_img_loader.bflb_serial_object
            if self.cfg.has_option("LOAD_CFG", "isp_mode_speed") and self.isp_mode_sign is True:
                isp_mode_speed = int(self.cfg.get("LOAD_CFG", "isp_mode_speed"))
                self._bflb_com_img_loader.set_isp_baudrate(isp_mode_speed)
        elif self.interface == "jlink":
            bflb_utils.printf("========= interface: JLink =========")
            self.bflb_serial_object = bflb_interface_jlink.BflbJLinkPort()
            if load_speed:
                self.speed = load_speed  # // 1000
                bflb_utils.printf("The com speed is %dk" % (self.speed))
            else:
                self.speed = int(self.cfg.get("LOAD_CFG", "speed_jlink"))
            self.boot_speed = self.speed
        elif self.interface == "openocd":
            bflb_utils.printf("========= interface: Openocd =========")
            self.bflb_serial_object = bflb_interface_openocd.BflbOpenocdPort()
            if load_speed:
                self.speed = load_speed  # // 1000
                bflb_utils.printf("The com speed is %dk" % (self.speed))
            else:
                self.speed = int(self.cfg.get("LOAD_CFG", "speed_jlink"))
            self.boot_speed = self.speed
        elif self.interface == "cklink":
            bflb_utils.printf("========= interface: CKLink =========")
            self.bflb_serial_object = bflb_interface_cklink.BflbCKLinkPort()
            if load_speed:
                self.speed = load_speed  # // 1000
                bflb_utils.printf("The com speed is %dk" % (self.speed))
            else:
                self.speed = int(self.cfg.get("LOAD_CFG", "speed_jlink"))
            self.boot_speed = self.speed
        else:
            bflb_utils.printf("{} is not supported".format(self.interface))
            return False, self.flash_burn_retry

        # add common config
        if self.cfg.has_option("LOAD_CFG", "password"):
            self.bflb_serial_object.set_password(self.cfg.get("LOAD_CFG", "password"))

        if self.args.chipid:
            ret, self.bootinfo, res = self.get_boot_info()
            if ret is False:
                self.print_error_code("0003")
                return False, self.flash_burn_retry
            else:
                return True, self.flash_burn_retry
        if self.cfg.has_option("LOAD_CFG", "load_function"):
            self.load_function = int(self.cfg.get("LOAD_CFG", "load_function"))
        if self.isp_mode_sign is True:
            if self._isp_shakehand_timeout == 0:
                self._isp_shakehand_timeout = 5
            self.set_load_function()
        return True, "continue"

    def run_step2_handshake(self):
        """
        Second step: handshake and load eflash_loader.bin.
        """
        try:
            if self.load_function == 0:
                bflb_utils.printf("No need load eflash_loader.bin")
            elif self.load_function == 1:
                load_bin_pass = False
                bflb_utils.printf("Eflash load bin file is {}".format(self.eflash_loader_file))
                ret, self.bootinfo, res = self.load_eflash_loader_bin(
                    privatekey_str=self.private_key_str,
                    publickey_str=self.public_key_str,
                )
                if res == "Handshake failed":
                    self.print_error_code("0050")
                if res.startswith("repeat_burn") is True:
                    return "repeat_burn", self.flash_burn_retry
                if res.startswith("error_shakehand") is True:
                    if self.cpu_reset is True:
                        self.print_error_code("0003")
                        return False, self.flash_burn_retry
                    else:
                        load_bin_pass = True
                        time.sleep(4.5)
                if ret is False and load_bin_pass is False:
                    self.print_error_code("0003")
                    return False, self.flash_burn_retry
                if self.ram_load:
                    return True, self.flash_burn_retry
            elif self.load_function == 2:
                load_bin_pass = False
                bflb_utils.printf("Bootrom load")
                ret, self.bootinfo, res = self.get_boot_info()
                if res == "Handshake failed":
                    self.print_error_code("0050")
                if res.startswith("repeat_burn") is True:
                    self.print_error_code("000A")
                    return "repeat_burn", self.flash_burn_retry
                if res.startswith("error_shakehand") is True:
                    if self.cpu_reset is True:
                        self.print_error_code("0003")
                        return False, self.flash_burn_retry
                    else:
                        load_bin_pass = True
                        time.sleep(4.5)
                if ret is False and load_bin_pass is False:
                    self.print_error_code("0050")
                    return False, self.flash_burn_retry
                self._need_handshake = False
                clock_para = bytearray(0)

                # -------------临时改，后期修改--------------
                if self.chip_type != "bl628":
                    if self.cfg.has_option("LOAD_CFG", "clock_para"):
                        clock_para_str = self.cfg.get("LOAD_CFG", "clock_para")
                        if clock_para_str != "":
                            clock_para_file = os.path.join(bflb_utils.app_path, clock_para_str)
                            bflb_utils.printf("The clock para file is {}".format(clock_para_file))
                            clock_para = self.update_clock_para(clock_para_file)
                    bflb_utils.printf("Change baudrate to {}".format(self.speed))
                    ret = self.set_clock_pll(self._need_handshake, True, clock_para)
                    if ret is False:
                        bflb_utils.printf("Failed to set pll")
                        return False, self.flash_burn_retry
            return True, "continue"
        except Exception as error:
            bflb_utils.printf(error)
            self.print_error_code("0003")
            return False, self.flash_burn_retry

    def run_step3_read_mac_addr(self):
        """
        Third step: read mac address.
        """
        time.sleep(0.1)

        if self.isp_mode_sign is True and self.cpu_reset is True:
            self.set_clear_boot_status(self._need_handshake)

        if self.cfg.has_option("LOAD_CFG", "check_mac"):
            self.macaddr_check = self.cfg.get("LOAD_CFG", "check_mac") == "true"
        if self.macaddr_check and self.isp_mode_sign is False:
            # check mac addr
            # isp mode don't support read macaddr
            check_macaddr_cnt = 5
            while True:
                ret, self._mac_addr = self.efuse_read_mac_addr_process()
                if ret is False:
                    bflb_utils.printf("Failed to read mac address")
                else:
                    break
                check_macaddr_cnt -= 1
                if check_macaddr_cnt == 0:
                    return False, self.flash_burn_retry
            bflb_utils.printf("The mac addr is {}".format(binascii.hexlify(self._mac_addr).decode("utf-8")))
            if self._mac_addr == self._macaddr_check:
                self.print_error_code("000A")
                return False, self.flash_burn_retry
            self._need_handshake = False
            self._macaddr_check_status = True
        # for mass_production tool
        if self.macaddr_callback is not None:
            (
                ret,
                self._efuse_data,
                self._efuse_mask_data,
                macaddr,
            ) = self.macaddr_callback(binascii.hexlify(self._mac_addr).decode("utf-8"))
            if ret is False:
                return False, self.flash_burn_retry
            if (self._efuse_data != bytearray(0) and self._efuse_mask_data != bytearray(0)) or macaddr != "":
                self.args.efuse = True
        if self.callback:
            self.callback(0, 100, "running", "blue")
        return True, "continue"

    def run_step4_set_flash_para(self):
        """
        Fourth step: Interact with chip, read chip ID and set flash parameter.
        """
        if self.args.flash or self.args.flash_otp:
            flash_pin = 0
            flash_clock_cfg = 0
            flash_io_mode = 0
            flash_clk_delay = 0
            if self.cfg.has_option("FLASH_CFG", "decompress_write"):
                self.decompress_write = self.cfg.get("FLASH_CFG", "decompress_write") == "true"
            self.set_decompress_write()
            if self.flash_file_list or self.args.read or self.args.erase:
                # set flash parameter
                bflb_utils.printf("========= flash set para =========")
                if self.cfg.get("FLASH_CFG", "flash_pin"):
                    flash_pin_cfg = self.cfg.get("FLASH_CFG", "flash_pin")
                    if flash_pin_cfg.startswith("0x"):
                        flash_pin = int(flash_pin_cfg, 16)
                    else:
                        flash_pin = int(flash_pin_cfg, 10)
                    if flash_pin == 0x80:
                        flash_pin = self.get_flash_pin_from_bootinfo(self.chip_type, self.bootinfo)
                        bflb_utils.printf("The flash pin cfg is 0x%02X" % (flash_pin))
                else:
                    flash_pin = self.get_flash_pin()
                if self.cfg.has_option("FLASH_CFG", "flash_clock_cfg"):
                    clock_div_cfg = self.cfg.get("FLASH_CFG", "flash_clock_cfg")
                    if clock_div_cfg.startswith("0x"):
                        flash_clock_cfg = int(clock_div_cfg, 16)
                    else:
                        flash_clock_cfg = int(clock_div_cfg, 10)
                if self.cfg.has_option("FLASH_CFG", "flash_io_mode"):
                    io_mode_cfg = self.cfg.get("FLASH_CFG", "flash_io_mode")
                    if io_mode_cfg.startswith("0x"):
                        flash_io_mode = int(io_mode_cfg, 16)
                    else:
                        flash_io_mode = int(io_mode_cfg, 10)
                if self.cfg.has_option("FLASH_CFG", "flash_clock_delay"):
                    clk_delay_cfg = self.cfg.get("FLASH_CFG", "flash_clock_delay")
                    if clk_delay_cfg.startswith("0x"):
                        flash_clk_delay = int(clk_delay_cfg, 16)
                    else:
                        flash_clk_delay = int(clk_delay_cfg, 10)

                # 0x0101ff is default set: flash_io_mode=1, flash_clock_cfg=1, flash_pin=0xff
                self.flash_set = (
                    (flash_pin << 0) + (flash_clock_cfg << 8) + (flash_io_mode << 16) + (flash_clk_delay << 24)
                )
                if self.flash_set != 0x0101FF or self.load_function == 2:
                    bflb_utils.printf("Set flash cfg to %X" % (self.flash_set))
                    ret = self.flash_set_para_main_process(self.flash_set, bytearray(0))
                    self._need_handshake = False
                    if ret is False:
                        return False, self.flash_burn_retry

                if self.args.flash_otp:
                    if self.cfg.has_option("FLASH_CFG", "flash_otp_para") and self.cfg.get(
                        "FLASH_CFG", "flash_otp_para"
                    ):
                        otp_param_file = os.path.join(bflb_utils.app_path, self.cfg.get("FLASH_CFG", "flash_otp_para"))
                        if self.flash_otp_set_para_main_process(otp_param_file) is not True:
                            return False, self.flash_burn_retry

                ret, data = self.flash_read_jedec_id_process()

                if ret:
                    self._need_handshake = False
                    data = binascii.hexlify(data).decode("utf-8")
                    self.id_valid_flag = data[6:]
                    read_id = data[0:6]
                    self.read_flash_id = read_id
                    if self.cfg.has_option("FLASH_CFG", "flash_para"):
                        if self.cfg.get("FLASH_CFG", "flash_para"):
                            flash_para_file = os.path.join(bflb_utils.app_path, self.cfg.get("FLASH_CFG", "flash_para"))
                            self.flash_para_update(flash_para_file, read_id)

                    self._flash_size = self.flash_get_size(self.read_flash_id)
                    bflb_utils.printf("The flash size is 0x%08X" % (self._flash_size))
                else:
                    self.print_error_code("0030")
                    return False, self.flash_burn_retry

                if self.args.flash_otp:
                    self._flash_otp_size = self.flash_get_otp_size()
                    if self._flash_otp_size == 0:
                        return False, self.flash_burn_retry
                    bflb_utils.printf("The flash otp size is 0x%X" % (self._flash_otp_size))

                result, content = self.run_flash_extra()
                return result, content
        return True, "continue"

    def run_step5_erase(self):
        """
        Seventh step: erase.
        """
        if self.args.erase:
            if self.args.flash_otp:
                bflb_utils.printf("Start to erase flash otp")
                if self.config["otpindex"] is not None:
                    index = int(self.config["otpindex"])
                    ret = self.flash_otp_erase_by_index_main_process(index, self._need_handshake)
                    if ret is False:
                        return False, self.flash_burn_retry
                else:
                    end_addr = int(self.end, 16)
                    if end_addr >= self._flash_size:
                        bflb_utils.printf(
                            "Error: The erase end addr 0x%08X exceeds flash size 0x%08X" % (end_addr, self._flash_size)
                        )
                        return False, self.flash_burn_retry
                    ret = self.flash_otp_erase_by_addr_main_process(
                        int(self.start, 16), int(self.end, 16) - int(self.start, 16) + 1, self._need_handshake
                    )
                    if ret is False:
                        return False, self.flash_burn_retry
            elif self.end == "0":
                bflb_utils.printf("Start to erase all flash")
                ret = self.flash_chiperase_main_process()
                if ret is False:
                    return False, self.flash_burn_retry
            else:
                bflb_utils.printf("Start to erase flash")
                ret = self.flash_erase_main_process(int(self.start, 16), int(self.end, 16), self._need_handshake)
                if ret is False:
                    return False, self.flash_burn_retry
            bflb_utils.printf("Flash erasion succeeded")
        return True, "continue"

    def run_step6_write_flash(self):
        """
        Fifth step: write flash and check.
        """
        # '--none' for eflash loader environment init
        if self.args.none:
            return True, self.flash_burn_retry
        if self.args.write:
            if not self.args.flash and not self.args.efuse and not self.args.flash_otp:
                bflb_utils.printf("No target selected")
                return False, self.flash_burn_retry
            # get program type
            if self.args.flash or self.args.flash_otp:
                if self.args.flash_otp:
                    bflb_utils.printf("Start to write flash otp")
                else:
                    bflb_utils.printf("Start to write flash")
                flash_para_file = ""
                flash2_para_file = ""
                if self.cfg.has_option("FLASH_CFG", "flash_para"):
                    if self.cfg.get("FLASH_CFG", "flash_para"):
                        flash_para_file = os.path.join(bflb_utils.app_path, self.cfg.get("FLASH_CFG", "flash_para"))
                if self.cfg.has_option("FLASH2_CFG", "flash2_para"):
                    if self.cfg.get("FLASH2_CFG", "flash2_para"):
                        flash2_para_file = os.path.join(bflb_utils.app_path, self.cfg.get("FLASH2_CFG", "flash2_para"))
                address = self.address_list
                flash_file = self.flash_file_list
                # do chip erase first
                if self.erase == 2 and self.args.flash:
                    ret = self.flash_chiperase_main_process()
                    if ret is False:
                        return False, self.flash_burn_retry
                    self._need_handshake = False
                    self.erase = 0
                # program flash
                if len(flash_file) > 0:
                    size_before = 0
                    size_all = 0
                    i = 0
                    for item in flash_file:
                        if self.temp_task_num is not None:
                            size_all += os.path.getsize(
                                os.path.join(
                                    bflb_utils.app_path,
                                    bflb_utils.convert_path("task" + str(self.temp_task_num) + "/" + item),
                                )
                            )
                        else:
                            size_all += os.path.getsize(
                                os.path.join(bflb_utils.app_path, bflb_utils.convert_path(item))
                            )
                    try:
                        ret = False
                        while i < len(flash_file):
                            if self.temp_task_num is not None:
                                flash_file[i] = "task" + str(self.temp_task_num) + "/" + flash_file[i]
                                size_current = os.path.getsize(
                                    os.path.join(bflb_utils.app_path, bflb_utils.convert_path(flash_file[i]))
                                )
                            else:
                                size_current = os.path.getsize(
                                    os.path.join(bflb_utils.app_path, bflb_utils.convert_path(flash_file[i]))
                                )
                            if self.callback:
                                self.callback(size_before, size_all, "program1")
                            if self.callback:
                                self.callback(size_current, size_all, "program2")
                            bflb_utils.printf("Processing index ", i)
                            if self.isp_mode_sign is True and self.args.flash:
                                bflb_utils.printf(
                                    "Start to write ",
                                    bflb_utils.convert_path(flash_file[i]),
                                )
                            elif self.args.flash_otp:
                                bflb_utils.printf(
                                    "Start to write ",
                                    bflb_utils.convert_path(flash_file[i]),
                                    " to flash otp 0x",
                                    address[i],
                                )
                            else:
                                bflb_utils.printf(
                                    "Start to write ",
                                    bflb_utils.convert_path(flash_file[i]),
                                    " to 0x",
                                    address[i],
                                )
                            flash1_bin = ""
                            flash1_bin_len = 0
                            flash2_bin = ""
                            flash2_bin_len = 0

                            (
                                flash1_bin,
                                flash1_bin_len,
                                flash2_bin,
                                flash2_bin_len,
                            ) = self.get_flash1_and_flash2(flash_file, address, size_current, i)

                            if flash1_bin != "" and flash2_bin != "" and self.args.flash:
                                ret = self.flash_cfg_option(
                                    self.read_flash_id,
                                    flash_para_file,
                                    self.flash_set,
                                    self.id_valid_flag,
                                    flash1_bin,
                                    self.config_file,
                                    self.cfg,
                                    self.create_img_callback,
                                    self.create_simple_callback,
                                )
                                if ret is False:
                                    return False, self.flash_burn_retry
                                bflb_utils.printf(
                                    "Start to write ",
                                    bflb_utils.convert_path(flash1_bin),
                                    " to 0x",
                                    address[i],
                                )
                                # flash write
                                ret = self.flash_load_specified(
                                    bflb_utils.convert_path(flash1_bin),
                                    int(address[i], 16),
                                    self.callback,
                                )
                                if ret is False:
                                    return False, self.flash_burn_retry
                                ret = self.flash_switch_bank_process(1)
                                self._need_handshake = False
                                if ret is False:
                                    return False, self.flash_burn_retry
                                ret = self.flash_cfg_option(
                                    self.read_flash2_id,
                                    flash2_para_file,
                                    self.flash2_set,
                                    self.id2_valid_flag,
                                    flash_file[i],
                                    self.config_file,
                                    self.cfg,
                                    self.create_img_callback,
                                    self.create_simple_callback,
                                )
                                if ret is False:
                                    return False, self.flash_burn_retry
                                bflb_utils.printf(
                                    "Start to write ",
                                    bflb_utils.convert_path(flash2_bin),
                                    " to 0x%08X" % (int(address[i], 16) + flash1_bin_len),
                                )
                                ret = self.flash_load_specified(
                                    bflb_utils.convert_path(flash2_bin),
                                    int(address[i], 16) + flash1_bin_len,
                                    self.callback,
                                )
                                if ret is False:
                                    return False, self.flash_burn_retry
                            else:
                                if self._flash2_en is False or (
                                    self._flash2_select is False and int(address[i], 16) < self._flash_size
                                ):
                                    ret = self.flash_cfg_option(
                                        self.read_flash_id,
                                        flash_para_file,
                                        self.flash_set,
                                        self.id_valid_flag,
                                        flash_file[i],
                                        self.config_file,
                                        self.cfg,
                                        self.create_img_callback,
                                        self.create_simple_callback,
                                    )
                                    if ret is False:
                                        return False, self.flash_burn_retry
                                else:
                                    if self._flash2_select is False and int(address[i], 16) >= self._flash_size:
                                        ret = self.flash_switch_bank_process(1)
                                        self._need_handshake = False
                                        if ret is False:
                                            return False, self.flash_burn_retry
                                    ret = self.flash_cfg_option(
                                        self.read_flash2_id,
                                        flash2_para_file,
                                        self.flash2_set,
                                        self.id2_valid_flag,
                                        flash_file[i],
                                        self.config_file,
                                        self.cfg,
                                        self.create_img_callback,
                                        self.create_simple_callback,
                                    )
                                    if ret is False:
                                        return False, self.flash_burn_retry
                                if self.args.flash_otp:
                                    if self.config["otpindex"] is not None:
                                        index = int(self.config["otpindex"])
                                        ret = self.flash_otp_write_by_index_main_process(
                                            index,
                                            bflb_utils.convert_path(flash_file[i]),
                                            self._need_handshake,
                                            self.callback,
                                        )
                                    else:
                                        ret = self.flash_otp_write_by_addr_main_process(
                                            int(address[i], 16),
                                            bflb_utils.convert_path(flash_file[i]),
                                            self._need_handshake,
                                            self.callback,
                                        )
                                else:
                                    ret = self.flash_load_specified(
                                        bflb_utils.convert_path(flash_file[i]),
                                        int(address[i], 16),
                                        self.callback,
                                    )
                                if ret is False:
                                    return False, self.flash_burn_retry
                            size_before += os.path.getsize(
                                os.path.join(bflb_utils.app_path, bflb_utils.convert_path(flash_file[i]))
                            )
                            i += 1
                            if self.callback:
                                self.callback(i, len(flash_file), "program")
                            self._need_handshake = False
                        if self._flash2_select is True:
                            ret = self.flash_switch_bank_process(0)
                            self._need_handshake = False
                            if ret is False:
                                return False, self.flash_burn_retry
                        bflb_utils.printf("Flash writing succeeded")
                    except Exception as error:
                        bflb_utils.printf(error)
                        traceback.print_exc(limit=self.NUM_ERR, file=sys.stdout)
                        return False, self.flash_burn_retry
                else:
                    bflb_utils.printf("Warning: No input file is found to write to flash")

        return True, "continue"

    def run_step7_write_efuse(self):
        """
        Sixth step: write efuse.
        """
        # get program type
        if self.args.efuse and self.args.write:
            efusefile = ""
            try:
                if self.config["input_path"]["efuse"]:
                    efusefile = self.config["input_path"]["efuse"]
            except:
                pass
            if efusefile:
                efuse_file = efusefile
                mask_file = efuse_file.replace(".bin", "_mask.bin")
                if self.temp_task_num is not None:
                    efuse_file = "task" + str(self.temp_task_num) + "/" + efuse_file
            else:
                efuse_file = None
                mask_file = None

            efuse_load = True
            efuse_verify = 0
            if self.cfg.has_option("EFUSE_CFG", "burn_en"):
                efuse_load = self.cfg.get("EFUSE_CFG", "burn_en") == "true"
            if self.cfg.has_option("EFUSE_CFG", "factory_mode"):
                if self.cfg.get("EFUSE_CFG", "factory_mode") == "true":
                    efuse_verify = 1
            # security_write = self.cfg.get("EFUSE_CFG", "security_write") == "true"
            if self.chip_type == "bl602" or self.chip_type == "bl702":
                security_write = False
            else:
                security_write = True

            load_efuse_encrypted = ""
            address = ""
            if "efuse_encrypted" in self.config["param"] and self.config["param"]["efuse_encrypted"]:
                load_efuse_encrypted = self.config["param"]["efuse_encrypted"]
            if "start" in self.config["param"] and self.config["param"]["start"]:
                address = self.config["param"]["start"]

            if efuse_load and self.isp_mode_sign is False:
                bflb_utils.printf("Start to write efuse")
                if load_efuse_encrypted and address:
                    write_addr = 0
                    if address[0:2] == "0x":
                        write_addr = int(address, 16)
                    else:
                        write_addr = int(address, 10)
                    bflb_utils.printf("Write encrypted efuse data {0} to {1}".format(load_efuse_encrypted, address))
                    sk = bytearray.fromhex(PRIVATE_KEY_RSA_HEX)
                    privatekey = serialization.load_pem_private_key(sk, password=None)
                    data = []
                    load_data_encrypted = bytearray.fromhex(load_data_encrypted)
                    for i in range(0, len(load_data_encrypted), 128):
                        cont = load_data_encrypted[i : i + 128]
                        data.append(privatekey.decrypt(bytes(cont), asymmetric_padding.PKCS1v15()))
                    data_decrypted = b"".join(data)
                    load_data = binascii.hexlify(data_decrypted).decode("utf-8")
                    ret = self.efuse_load_data_process(
                        load_data,
                        write_addr,
                        0,
                        self.verify,
                        False,
                        security_write,
                    )
                    if self.callback:
                        self.callback(1, 1, "APP_WR")
                    if ret is False:
                        bflb_utils.printf("Failed to write encrypted efuse data")
                        return False, self.flash_burn_retry
                    else:
                        return True, "continue"

                if efuse_file and mask_file:
                    ret = self.efuse_load_specified(
                        efuse_file,
                        mask_file,
                        bytearray(0),
                        bytearray(0),
                        efuse_verify,
                        security_write,
                    )
                    if self.callback:
                        self.callback(1, 1, "APP_WR")
                    if ret is False:
                        return False, self.flash_burn_retry
            else:
                bflb_utils.printf("Efuse load disalbed")
            self._need_handshake = False
        return True, "continue"

    def run_step8_read(self):
        """
        Eighth step: read.
        """
        if self.args.read:
            if not self.args.flash and not self.args.efuse and not self.args.flash_otp:
                bflb_utils.printf("No target selected")
                return False, self.flash_burn_retry
            if self.args.flash:
                bflb_utils.printf("Start to read flash")
                if not self.start or not self.end:
                    self.flash_read_jedec_id_process(self.callback)
                else:
                    start_addr = int(self.start, 16)
                    end_addr = int(self.end, 16)
                    if end_addr >= self._flash_size:
                        bflb_utils.printf(
                            "Error: The read end addr 0x%08X exceeds flash size 0x%08X" % (end_addr, self._flash_size)
                        )
                        return False, self.flash_burn_retry
                    ret, readdata = self.flash_read_main_process(
                        start_addr,
                        end_addr - start_addr + 1,
                        self._need_handshake,
                        self.img_file,
                        self.callback,
                    )
                    if ret is False:
                        return False, self.flash_burn_retry
            if self.args.flash_otp:
                bflb_utils.printf("Start to read flash otp")
                if self.config["otpindex"] is not None:
                    index = int(self.config["otpindex"])
                    length = self.config["flash"]["length"]
                    if not bflb_utils.is_hex(length):
                        ret = "Error: Flash otp read length is not hex"
                        bflb_utils.printf(ret)
                        return False, self.flash_burn_retry
                    else:
                        flash_data_len = int(length, 16)
                    ret, readdata = self.flash_otp_read_by_index_main_process(
                        index,
                        flash_data_len,
                        self._need_handshake,
                        self.img_file,
                        self.callback,
                    )
                    if ret is False:
                        return False, self.flash_burn_retry
                else:
                    if not self.start or not self.end:
                        self.flash_read_jedec_id_process(self.callback)
                    else:
                        start_addr = int(self.start, 16)
                        end_addr = int(self.end, 16)
                        if end_addr >= self._flash_otp_size:
                            bflb_utils.printf(
                                "Error: The read otp end addr 0x%08X exceeds flash otp size 0x%08X"
                                % (end_addr, self._flash_otp_size)
                            )
                            return False, self.flash_burn_retry
                        ret, readdata = self.flash_otp_read_by_addr_main_process(
                            start_addr,
                            end_addr - start_addr + 1,
                            self._need_handshake,
                            self.img_file,
                            self.callback,
                        )
                        if ret is False:
                            return False, self.flash_burn_retry
            if self.args.efuse:
                bflb_utils.printf("Start to read efuse")
                start_addr = int(self.start, 16)
                end_addr = int(self.end, 16)
                ret, readdata = self.efuse_read_main_process(
                    start_addr,
                    end_addr - start_addr + 1,
                    self._need_handshake,
                    self.img_file,
                )
                if ret is False:
                    return False, self.flash_burn_retry
        return True, "continue"

    def run_step9_lock(self):
        """
        Ninth step: run lock.
        """

        if self.args.flash_otp:
            if self.args.lock:
                if self.config["otpindex"] is not None:
                    lockidx = int(self.config["flash"]["otpindex2"])
                    if self.flash_otp_lock_by_index_main_process(lockidx) is not True:
                        return False, self.flash_burn_retry
                else:
                    start_addr = int(self.start, 16)
                    end_addr = int(self.end, 16)
                    if self.flash_otp_lock_by_addr_main_process(start_addr, end_addr) is not True:
                        return False, self.flash_burn_retry

        self.run_reset_cpu()
        if self.macaddr_check is True:
            self._bootinfo = self.bootinfo
        self._macaddr_check = self._mac_addr
        self._macaddr_check_status = False
        return True, self.flash_burn_retry

    def run_step(self):
        result, content = self.run_step1_load_config()
        if not result or content != "continue":
            return result, content

        result, content = self.run_step2_handshake()
        if not result or content != "continue":
            return result, content

        result, content = self.run_step3_read_mac_addr()
        if not result or content != "continue":
            return result, content

        result, content = self.run_step4_set_flash_para()
        if not result or content != "continue":
            return result, content

        result, content = self.run_step5_erase()
        if not result or content != "continue":
            return result, content

        result, content = self.run_step6_write_flash()
        if not result or content != "continue":
            return result, content

        result, content = self.run_step7_write_efuse()
        if not result or content != "continue":
            return result, content

        result, content = self.run_step8_read()
        if not result or content != "continue":
            return result, content

        result, content = self.run_step9_lock()
        return result, content

    # ===========================================Util Function===================================================

    def run_flash_extra(self):
        return True, "continue"

    def run_reset_cpu(self):
        if "reset" in self.config and self.config["reset"]:
            self.reset_cpu()

    def base_reset_cpu(self):
        if self.bflb_serial_object:
            self.bflb_serial_object.reset()

    def reset_cpu(self, shakehand=0):
        bflb_utils.printf("Reset cpu")
        bl_sign = self.bflb_serial_object._is_bouffalo_chip()
        if bl_sign:
            self.bflb_serial_object.write(b"BOUFFALOLAB5555DTR0")
            time.sleep(0.05)
            self.bflb_serial_object.write(b"BOUFFALOLAB5555RTS0")
            time.sleep(0.05)
            self.bflb_serial_object.write(b"BOUFFALOLAB5555RTS1")
        else:
            self.bflb_serial_object.set_dtr(1)
            time.sleep(0.05)
            self.bflb_serial_object.set_rts(1)
            time.sleep(0.05)
            self.bflb_serial_object.set_rts(0)

    def close_serial(self):
        if self.bflb_serial_object:
            try:
                self.bflb_serial_object.close()
            except Exception as error:
                bflb_utils.printf(error)

    def clear_all_data(self):
        if self.bflb_serial_object:
            try:
                self.bflb_serial_object.clear_buf()
            except Exception as error:
                bflb_utils.printf(error)

    def clear_object_status(self):
        self.bootinfo = None
        self._macaddr_check = bytearray(0)
        self._macaddr_check_status = False

    def clear_boot_status(self, shakehand=0):
        bflb_utils.printf("Clear boot status at hbn rsvd register")
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_ERASE_HANDSHAKE)
            if self._handshake() is False:
                return False
        # write memory, 0x2000F108=0x00000000
        data = bytearray(12)
        data[0] = 0x50
        data[1] = 0x00
        data[2] = 0x08
        data[3] = 0x00
        data[4] = 0x08
        data[5] = 0xF1
        data[6] = 0x00
        data[7] = 0x20
        data[8] = 0x00
        data[9] = 0x00
        data[10] = 0x00
        data[11] = 0x00
        self.bflb_serial_object.write(data)
        self.bflb_serial_object.deal_ack(dmy_data=False)
        return True

    def print_error_code(self, code):
        bflb_utils.set_error_code(code, self.task_num)
        bflb_utils.printf("ErrorCode: {0}, ErrorMsg: {1}".format(code, bflb_utils.eflash_loader_error_code[code]))

    def print_identify_fail(self):
        return True

    def update_clock_para(self, file):
        if os.path.isfile(file) is False:
            efuse_bootheader_path = os.path.join(bflb_utils.chip_path, self.chip_name, "efuse_bootheader")
            efuse_bh_cfg = efuse_bootheader_path + "/efuse_bootheader_cfg.conf"
            sub_module = __import__("libs." + self.chip_type, fromlist=[self.chip_type])
            section = "BOOTHEADER_GROUP0_CFG"
            with open(efuse_bh_cfg, "r") as fp:
                data = fp.read()
            if "BOOTHEADER_CFG" in data:
                section = "BOOTHEADER_CFG"
            elif "BOOTHEADER_CPU0_CFG" in data:
                section = "BOOTHEADER_CPU0_CFG"
            elif "BOOTHEADER_GROUP0_CFG" in data:
                section = "BOOTHEADER_GROUP0_CFG"
            bh_data, _ = img_create.update_data_from_cfg(
                sub_module.bootheader_cfg_keys.bootheader_cfg_keys,
                efuse_bh_cfg,
                section,
            )
            bh_data = img_create.bootheader_update_flash_pll_crc(bh_data, self.chip_type)
            with open(file, "wb+") as fp:
                self.get_new_bh_data(section, bh_data, fp)

        fp = bflb_utils.open_file(file, "rb")
        clock_para = bytearray(fp.read())
        fp.close()
        return clock_para

    def ecdh_encrypt_data(self, data):
        # 创建 AES-CBC加密器
        cipher = Cipher(algorithms.AES(bytearray.fromhex(self._ecdh_shared_key[0:32])), modes.CBC(bytearray(16)))
        encryptor = cipher.encryptor()
        # 加密数据
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return ciphertext

    def ecdh_decrypt_data(self, data):
        # 创建 AES-CBC解密器
        cipher = Cipher(algorithms.AES(bytearray.fromhex(self._ecdh_shared_key[0:32])), modes.CBC(bytearray(16)))
        decryptor = cipher.decryptor()
        # 解密数据
        plaintext = decryptor.update(data) + decryptor.finalize()
        return plaintext

    @staticmethod
    def create_flash_default_data(length):
        datas = bytearray(length)
        for i in range(length):
            datas[i] = 0xFF
        return datas

    def _handshake(self):
        isp_sh_time = self.get_isp_sh_time()
        if self.interface.lower() == "uart":
            self.bflb_serial_object.repeat_init(self.device, self.speed, self.chip_type, self.chip_name)
            if (
                self._bflb_com_img_loader.toggle_boot_or_handshake(
                    2,
                    do_reset=False,
                    reset_hold_time=100,
                    shake_hand_delay=100,
                    reset_revert=True,
                    cutoff_time=0,
                    isp_mode_sign=self.isp_mode_sign,
                    isp_timeout=isp_sh_time,
                    boot_load=False,
                    shake_hand_retry=2,
                )
                != "OK"
            ):
                self.print_error_code("0001")
                return False
        else:
            self.bflb_serial_object.if_init(self.device, self.speed, self.chip_type, self.chip_name)
            if (
                self.bflb_serial_object.if_shakehand(
                    do_reset=False,
                    reset_hold_time=100,
                    shake_hand_delay=100,
                    reset_revert=True,
                    cutoff_time=0,
                    shake_hand_retry=2,
                    isp_timeout=isp_sh_time,
                    boot_load=False,
                )
                != "OK"
            ):
                self.print_error_code("0001")
                return False
        self._need_handshake = False
        return True

    def load_eflash_loader_bin(self, **kwargs):
        """
        This function is used to load eflash loader bin file.
        """
        bflb_utils.printf("========= load eflash_loader.bin =========")
        bootinfo = None
        if self.interface == "jlink":
            bflb_utils.printf("Load eflash_loader.bin via jlink")
            self.bflb_serial_object.if_init(self.device, self.speed, self.chip_type, self.chip_name)
            self.bflb_serial_object.reset_cpu()
            imge_fp = bflb_utils.open_file(self.eflash_loader_file, "rb")
            # eflash_loader.bin has 192 bytes bootheader and seg header
            fw_data = bytearray(imge_fp.read())[192:] + bytearray(0)
            imge_fp.close()
            sub_module = __import__("libs." + self.chip_type, fromlist=[self.chip_type])
            load_addr = sub_module.jlink_load_cfg.jlink_load_addr
            self.bflb_serial_object.if_raw_write(load_addr, fw_data)
            pc = fw_data[4:8]
            pc = bytes([pc[3], pc[2], pc[1], pc[0]])
            # c.reverse()
            msp = fw_data[0:4]
            msp = bytes([msp[3], msp[2], msp[1], msp[0]])
            # msp.reverse()
            self.bflb_serial_object.set_pc_msp(binascii.hexlify(pc), binascii.hexlify(msp).decode("utf-8"))
            time.sleep(0.01)
            self.bflb_serial_object.if_close()
            return True, bootinfo, ""
        elif self.interface == "openocd":
            bflb_utils.printf("Load eflash_loader.bin via openocd")
            self.bflb_serial_object.if_init(
                self.device,
                self._bflb_sn_device,
                self.speed,
                self.chip_type,
                self.chip_name,
            )
            self.bflb_serial_object.halt_cpu()
            imge_fp = bflb_utils.open_file(self.eflash_loader_file, "rb")
            # eflash_loader.bin has 192 bytes bootheader and seg header
            fw_data = bytearray(imge_fp.read())[192:] + bytearray(0)
            imge_fp.close()
            sub_module = __import__("libs." + self.chip_type, fromlist=[self.chip_type])
            load_addr = sub_module.openocd_load_cfg.openocd_load_addr
            self.bflb_serial_object.if_raw_write(load_addr, fw_data)
            pc = fw_data[4:8]
            pc = bytes([pc[3], pc[2], pc[1], pc[0]])
            # c.reverse()
            msp = fw_data[0:4]
            msp = bytes([msp[3], msp[2], msp[1], msp[0]])
            # msp.reverse()
            self.bflb_serial_object.set_pc_msp(binascii.hexlify(pc), binascii.hexlify(msp).decode("utf-8"))
            return True, bootinfo, ""
        elif self.interface == "cklink":
            bflb_utils.printf("Load eflash_loader.bin via cklink")

            self.bflb_serial_object.if_init(
                self.device,
                self._bflb_sn_device,
                self.speed,
                self.chip_type,
                self.chip_name,
            )
            self.bflb_serial_object.halt_cpu()
            imge_fp = bflb_utils.open_file(self.eflash_loader_file, "rb")
            # eflash_loader.bin has 192 bytes bootheader and seg header
            fw_data = bytearray(imge_fp.read())[192:] + bytearray(0)
            imge_fp.close()
            sub_module = __import__("libs." + self.chip_type, fromlist=[self.chip_type])
            load_addr = sub_module.openocd_load_cfg.openocd_load_addr
            self.bflb_serial_object.if_raw_write(load_addr, fw_data)
            pc = fw_data[4:8]
            pc = bytes([pc[3], pc[2], pc[1], pc[0]])
            # c.reverse()
            msp = fw_data[0:4]
            msp = bytes([msp[3], msp[2], msp[1], msp[0]])
            # msp.reverse()
            self.bflb_serial_object.set_pc_msp(binascii.hexlify(pc), binascii.hexlify(msp).decode("utf-8"))
            self.bflb_serial_object.resume_cpu()
            return True, bootinfo, ""
        elif self.interface.lower() == "uart" or self.interface == "sdio":
            ret = True
            bflb_utils.printf("Load eflash_loader.bin via %s" % self.interface)
            start_time = time.time() * 1000
            ret, bootinfo, res = self._bflb_com_img_loader.img_load_process(
                self.boot_speed,
                self.boot_speed,
                None,
                self.do_reset,
                self.reset_hold_time,
                self.shake_hand_delay,
                self.reset_revert,
                self.cutoff_time,
                self.shake_hand_retry,
                self.isp_mode_sign,
                self._isp_shakehand_timeout,
                True,
                bootinfo,
                **kwargs,
            )
            time_cost = (time.time() * 1000) - start_time
            bflb_utils.printf("Load helper bin time cost(ms): {}".format(round(time_cost, 3)))
            return ret, bootinfo, res

    def write_flash_data(self, file, start_addr, callback):
        pass

    def write_flash_img(self, d_addrs, d_files, flash_size="1M"):
        whole_img_len = self.get_largest_addr(d_addrs, d_files)
        whole_img_data = self.create_flash_default_data(whole_img_len)
        whole_img_file = os.path.join(bflb_utils.chip_path, self.chip_name, "img_create", "whole_flash_data.bin")
        sha256_whole_img_file = os.path.join(
            bflb_utils.chip_path, self.chip_name, "img_create", "whole_flash_data.bin.hash"
        )
        # if os.path.exists(whole_img_file):
        #     os.remove(whole_img_file)
        filedatas = self.get_file_data(d_files)
        # create_whole_image_flash
        for i in range(len(d_addrs)):
            start_addr = int(d_addrs[i], 16)
            whole_img_data[start_addr : start_addr + len(filedatas[i])] = filedatas[i]
        if not os.path.exists(os.path.dirname(whole_img_file)):
            os.makedirs(os.path.dirname(whole_img_file))
        with open(whole_img_file, "wb+") as fp:
            fp.write(whole_img_data)

        sh = hashlib.sha256()
        sh.update(whole_img_data)
        fw_sha256 = sh.hexdigest()
        fw_sha256 = bflb_utils.hexstr_to_bytearray(fw_sha256)
        sha256_whole_img_data = whole_img_data + fw_sha256
        with open(sha256_whole_img_file, "wb+") as fp:
            fp.write(sha256_whole_img_data)

    def process_one_cmd(self, section, cmd_id, data_send):
        data_read = bytearray(0)
        data_len = bflb_utils.int_to_2bytearray_l(len(data_send))
        checksum = 0
        checksum += bflb_utils.bytearray_to_int(data_len[0:1]) + bflb_utils.bytearray_to_int(data_len[1:2])
        for char in data_send:
            checksum += char
        data = cmd_id + bflb_utils.int_to_2bytearray_l(checksum & 0xFF)[0:1] + data_len + data_send
        if self.interface.lower() == "uart":
            self.bflb_serial_object.write(data)
            if section in self._resp_cmds:
                res, data_read = self.bflb_serial_object.deal_response()
            else:
                res = self.bflb_serial_object.deal_ack()
        else:
            self.bflb_serial_object.if_write(data)
            if section in self._resp_cmds:
                res, data_read = self.bflb_serial_object.if_deal_response()
            else:
                res = self.bflb_serial_object.if_deal_ack()
        return res, data_read

    @staticmethod
    def get_flash_conf(flash_id):
        cfg_dir = os.path.join(bflb_utils.app_path, "utils", "flash")
        conf_name = bflb_flash_select.get_suitable_file_name(cfg_dir, flash_id)
        conf_path = os.path.join(cfg_dir, conf_name)
        if os.path.isfile(conf_path) is False:
            return False, conf_path
        else:
            return True, conf_path

    def get_flash_pin(self):
        return 0

    def get_flash1_and_flash2(self, flash_file, address, size_current, i):
        return "", 0, "", 0

    def get_mac_len(self):
        return 6

    def get_isp_sh_time(self):
        return 0

    def get_new_bh_data(self, section, bh_data, fp):
        return b""

    def get_chip_id(self, bootinfo):
        chip_id = (
            bootinfo[34:36] + bootinfo[32:34] + bootinfo[30:32] + bootinfo[28:30] + bootinfo[26:28] + bootinfo[24:26]
        )
        return chip_id

    def get_flash_pin_from_bootinfo(self, chiptype, bootinfo):
        return 0x80

    def get_flash_file_and_address(self):
        result = True
        temp_files = []
        temp_addrs = []
        temp_dict = {}
        temp_addrs_list = []
        temp_addrs_int_list = []
        temp_key_value_list = []
        for key, value_dict in self.config.items():
            if isinstance(value_dict, dict):
                if "addr" in value_dict:
                    if value_dict["addr"]:
                        try:
                            int_value_addr = int(bytes(value_dict["addr"], encoding="utf-8"), 16)
                            if int_value_addr in temp_addrs_int_list:
                                temp_position = temp_addrs_int_list.index(int_value_addr)
                                bflb_utils.printf(
                                    "Error: %s has same addresse %s with %s!"
                                    % (
                                        key,
                                        value_dict["addr"],
                                        temp_key_value_list[temp_position],
                                    )
                                )
                                return False, temp_addrs, temp_files
                            temp_dict[value_dict["addr"]] = value_dict["path"]
                            temp_addrs_list.append(value_dict["addr"])
                            temp_addrs_int_list.append(int_value_addr)
                            temp_key_value_list.append(key)
                        except Exception as error:
                            bflb_utils.printf(error)
        if temp_dict:
            temp_list = sorted(temp_dict.items(), key=lambda x: int(x[0], 16), reverse=False)
            for i in range(len(temp_list)):
                temp_addrs.append(temp_list[i][0].replace("0x", ""))
                temp_files.append(temp_list[i][1])
                if i != 0:
                    temp_length = int(temp_list[i][0], 16) - int(temp_list[i - 1][0], 16)
                    file_length = os.path.getsize(temp_list[i - 1][1])
                    if temp_length < file_length:
                        result = False
                        bflb_utils.printf(
                            "Error: path: %s  size: %s  range: %s"
                            % (temp_list[i - 1][1], str(file_length), str(temp_length))
                        )
                        bflb_utils.printf("Error: The file size exceeds the address space size")
        return result, temp_addrs, temp_files

    def get_boot_info(self):
        """
        This function is used to get boot information from chips. At the same time, it can get chip ID.
        """
        # bflb_utils.printf("========= get boot info =========")
        bootinfo = None
        if self.interface == "uart":
            ret = True
            start_time = time.time() * 1000
            """ret, bootinfo = self._bflb_com_img_loader.img_get_bootinfo(self.boot_speed, self.boot_speed, self.eflash_loader_file, self.do_reset,
                                                                       self.reset_hold_time, self.shake_hand_delay, self.reset_revert,
                                                                       self.cutoff_time, self.shake_hand_retry, self.isp_mode_sign,
                                                                       self._isp_shakehand_timeout)"""
            ret, bootinfo = self._bflb_com_img_loader.img_get_bootinfo(
                self.boot_speed,
                self.boot_speed,
                None,
                self.do_reset,
                self.reset_hold_time,
                self.shake_hand_delay,
                self.reset_revert,
                self.cutoff_time,
                self.shake_hand_retry,
                self.isp_mode_sign,
                self._isp_shakehand_timeout,
                boot_baudrate=self.boot_speed,
            )
            bootinfo = bootinfo.decode("utf-8")
            chipid = ""
            chipid = self.get_chip_id(bootinfo)
            if chipid:
                bflb_utils.printf("========= chip id: ", chipid, " =========")
                time_cost = (time.time() * 1000) - start_time
                bflb_utils.printf("Get bootinfo time cost(ms): {}".format(round(time_cost, 3)))
            return ret, bootinfo, "OK"
        else:
            bflb_utils.printf("Interface is not supported")
            return False, bootinfo, ""

    def get_ecdh_shared_key(self, shakehand=0):
        bflb_utils.printf("========= get ecdh shared key =========")
        if shakehand:
            bflb_utils.printf("Handshake")
            ret = self._handshake()
            if ret is False:
                return
        obj_ecdh = bflb_ecdh.BflbEcdh()
        self._ecdh_public_key = obj_ecdh.create_public_key()
        self._ecdh_private_key = binascii.hexlify(obj_ecdh.private_key.private_numbers().private_value.to_bytes(32, "big")).decode("utf-8")
        bflb_utils.printf("ecdh public key")
        bflb_utils.printf(self._ecdh_public_key)
        # bflb_utils.printf("ecdh private key")
        # bflb_utils.printf(self._ecdh_private_key)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("ecdh_get_pk")["cmd_id"])
        data_send = bytearray.fromhex(self._ecdh_public_key)
        ret, data_read = self.process_one_cmd("ecdh_get_pk", cmd_id, data_send)
        if ret.startswith("OK") is True:
            self._ecdh_peer_public_key = binascii.hexlify(data_read).decode("utf-8")
            bflb_utils.printf("ecdh peer key")
            bflb_utils.printf(self._ecdh_peer_public_key)
            self._ecdh_shared_key = obj_ecdh.create_shared_key(self._ecdh_peer_public_key[0:128])
            # bflb_utils.printf("ecdh shared key")
            # bflb_utils.printf(self._ecdh_shared_key)
            # challenge
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("ecdh_chanllenge")["cmd_id"])
            data_send = bytearray(0)
            ret, data_read = self.process_one_cmd("ecdh_chanllenge", cmd_id, data_send)
            if ret.startswith("OK") is True:
                bflb_utils.printf("challenge data")
                bflb_utils.printf(binascii.hexlify(data_read).decode("utf-8"))
                encrypted_data = data_read[0:32]
                signature = data_read[32:96]
                signature_r = data_read[32:64]
                signature_s = data_read[64:96]
                signature = encode_dss_signature(int.from_bytes(signature_r, "big"), int.from_bytes(signature_s, "big"))
                ret = False
                try:
                    with open(os.path.join(bflb_utils.app_path, "utils/pem/room_root_publickey_ecc.pem"), "rb") as fp:
                        key = fp.read()
                    public_key = serialization.load_pem_public_key(key)
                    public_key.verify(signature, self.ecdh_decrypt_data(encrypted_data), ec.ECDSA(hashes.SHA256()))
                    ret = True
                except Exception as error:
                    bflb_utils.printf(error)
                if ret is True:
                    return True
                else:
                    bflb_utils.printf("Failed to verify challenge")
                    return False
            else:
                bflb_utils.printf("Failed to get challenge ack")
                return False
        else:
            bflb_utils.printf("Failed to get shared key")
            return False

    @staticmethod
    def get_file_data(files):
        datas = []
        for file in files:
            if os.path.exists(file):
                temp_path = file
            else:
                temp_path = os.path.join(bflb_utils.app_path, file)
            with open(temp_path, "rb") as fp:
                data = fp.read()
            datas.append(data)
        return datas

    @staticmethod
    def get_largest_addr(addrs, files):
        maxlen = 0
        datalen = 0
        for i in range(len(addrs)):
            if int(addrs[i], 16) > maxlen:
                maxlen = int(addrs[i], 16)
                if os.path.exists(files[i]):
                    datalen = os.path.getsize(files[i])
                else:
                    datalen = os.path.getsize(os.path.join(bflb_utils.app_path, files[i]))
        return maxlen + datalen

    def set_clear_boot_status(self, shakehand=0):
        pass

    def set_boot_speed(self):
        pass

    def set_load_function(self):
        self.load_function = 2

    def set_decompress_write(self):
        pass

    def set_temp_timeout(self):
        self.bflb_serial_object.set_timeout(self._erase_time_out / 1000)

    def set_config_file(self, bootheader_file, img_create_file):
        self._efuse_bootheader_file = bootheader_file
        self._img_create_file = img_create_file

    def set_clock_pll(self, shakehand, irq_en, clk_para):
        bflb_utils.printf("Set clock pll")
        # handshake
        if shakehand:
            bflb_utils.printf("Handshake")
            if self._handshake() is False:
                return False
        start_time = time.time() * 1000
        # send command
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("clk_set")["cmd_id"])
        irq_enable = bytearray(4)
        load_speed = bytearray(4)
        if irq_en:
            irq_enable = b"\x01\x00\x00\x00"
        load_speed = bflb_utils.int_to_4bytearray_l(int(self.speed))
        data_send = irq_enable + load_speed + clk_para
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("clk_set", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                self.print_error_code("000C")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Set clock time cost(ms): {}".format(round(time_cost, 3)))
        self.bflb_serial_object.repeat_init(self.device, self.speed, self.chip_type, self.chip_name)
        self.bflb_serial_object.clear_buf()
        time.sleep(0.01)
        return True

    def efuse_load_specified(self, file, maskfile, efusedata, efusedatamask, verify=0, security_write=False):
        bflb_utils.printf("========= efuse load =========")
        if self._need_handshake:
            bflb_utils.printf("Efuse load handshake")
            ret = self._handshake()
            if ret is False:
                return False
        ret = self.efuse_load_main_process(file, maskfile, efusedata, efusedatamask, verify, security_write)
        return ret

    def efuse_load_main_process(self, file, maskfile, efusedata, efusedatamask, verify=0, security_write=False):
        if self.chip_type == "bl616":
            if self._bflb_com_img_loader.bl616_a0:
                # write memory, set bl616 a0 bootrom uart timeout to 2s
                val = bflb_utils.int_to_2bytearray_l(8)
                start_addr_tmp = bflb_utils.int_to_4bytearray_l(0x6102DF04)
                write_data = bflb_utils.int_to_4bytearray_l(0x07D01200)
                cmd_id = bflb_utils.hexstr_to_bytearray("50")
                data = cmd_id + bytearray(1) + val + start_addr_tmp + write_data
                self.bflb_serial_object.if_write(data)
                ret, data_read_ack = self.bflb_serial_object.deal_ack(dmy_data=False)
            else:
                # 03 command to set bl616 ax bootrom uart timeout to 2s
                val = bflb_utils.int_to_2bytearray_l(4)
                timeout = bflb_utils.int_to_4bytearray_l(2000)
                cmd_id = bflb_utils.hexstr_to_bytearray("23")
                data = cmd_id + bytearray(1) + val + timeout
                self.bflb_serial_object.if_write(data)
                ret, data_read_ack = self.bflb_serial_object.deal_ack(dmy_data=False)
        if efusedata != bytearray(0):
            bflb_utils.printf("Load data")
            efuse_data = efusedata
            mask_data = efusedatamask
        elif file is not None:
            bflb_utils.printf("Load file: {}".format(file))
            fp = bflb_utils.open_file(file, "rb")
            efuse_data = bytearray(fp.read()) + bytearray(0)
            fp.close()
            if len(efuse_data) > 4096:
                bflb_utils.printf("Decrypt efuse data")
                efuse_save_crc = efuse_data[0:4]
                efuse_data = efuse_data[4096:]
                cfg_key = os.path.join(bflb_utils.app_path, "cfg.bin")
                if os.path.exists(cfg_key):
                    res, security_key, security_iv = bflb_utils.get_aes_encrypted_key(cfg_key)
                    if res is False:
                        bflb_utils.printf("Failed to get encrypted aes key and iv")
                        return False
                else:
                    security_key, security_iv = bflb_utils.get_security_key()
                efuse_data = bflb_utils.img_create_decrypt_data(efuse_data, security_key, security_iv, 0)
                if not efuse_data:
                    return False
                efuse_crc = bflb_utils.get_crc32_bytearray(efuse_data)
                if efuse_crc != efuse_save_crc:
                    bflb_utils.printf("Efuse crc check failed")
                    self.print_error_code("0021")
                    return False
            try:
                bflb_utils.printf("Open {}".format(maskfile))
                fp = bflb_utils.open_file(maskfile, "rb")
                mask_data = bytearray(fp.read()) + bytearray(0)
                fp.close()
            except:
                bflb_utils.printf("{} is non existent".format(maskfile))
                bflb_utils.printf("Create efuse mask data")
                mask_data = self.efuse_create_mask_data(efuse_data)
        else:
            efuse_data = self._efuse_data
            mask_data = self._efuse_mask_data
        if security_write and (self.get_ecdh_shared_key() is not True):
            return False
        if security_write:
            cmd_name = "efuse_security_write"
        else:
            cmd_name = "efuse_write"
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(cmd_name)["cmd_id"])

        # parameter end_idx: end - 4
        def write_and_verify_except_protect_data(start_idx, end_idx):
            # load normal data
            data_send = efuse_data[start_idx:end_idx] + bytearray(4)
            if security_write:
                data_send = self.ecdh_encrypt_data(data_send)
            data_send = bflb_utils.int_to_4bytearray_l(start_idx) + data_send
            ret, dmy = self.process_one_cmd(cmd_name, cmd_id, data_send)
            if ret.startswith("OK") is False:
                bflb_utils.printf("Write failed")
                self.print_error_code("0021")
                return False
            # verify
            if verify >= 1:
                ret, read_data = self.efuse_read_main_process(
                    start_idx, end_idx - start_idx + 4, shakehand=0, file=None, security_read=security_write
                )
                if ret is True and self.efuse_compare(
                    read_data,
                    mask_data[start_idx:end_idx] + bytearray(4),
                    efuse_data[start_idx:end_idx] + bytearray(4),
                ):
                    bflb_utils.printf("Verification succeeded")
                else:
                    # bflb_utils.printf("Read: ")
                    # bflb_utils.printf(binascii.hexlify(read_data[0:end_idx - start_idx]).decode("utf-8"))
                    # bflb_utils.printf("Expected: ")
                    # bflb_utils.printf(binascii.hexlify(efuse_data[start_idx:end_idx]).decode("utf-8"))
                    bflb_utils.printf("Verify failed")
                    self.print_error_code("0022")
                    return False

            return True

        def write_and_verify_protect_data(start_idx, end_idx):
            # load read write protect data
            data_send = bytearray(12) + efuse_data[start_idx:end_idx]
            if security_write:
                data_send = self.ecdh_encrypt_data(data_send)
            data_send = bflb_utils.int_to_4bytearray_l(start_idx - 12) + data_send
            ret, dmy = self.process_one_cmd(cmd_name, cmd_id, data_send)
            if ret.startswith("OK") is False:
                bflb_utils.printf("Write failed")
                self.print_error_code("0021")
                return False
            # verify
            if verify >= 1:
                ret, read_data = self.efuse_read_main_process(
                    start_idx - 12, 16, shakehand=0, file=None, security_read=security_write
                )
                if ret is True and self.efuse_compare(
                    read_data,
                    bytearray(12) + mask_data[start_idx:end_idx],
                    bytearray(12) + efuse_data[start_idx:end_idx],
                ):
                    bflb_utils.printf("Verification succeeded")
                else:
                    # bflb_utils.printf("Read: ")
                    # bflb_utils.printf(binascii.hexlify(read_data[12:16]))
                    # bflb_utils.printf("Expected: ")
                    # bflb_utils.printf(binascii.hexlify(efuse_data[start_idx:end_idx]))
                    bflb_utils.printf("Verify failed")
                    self.print_error_code("0022")
                    return False
            return True

        def write_and_verify_all_data(start_idx, end_idx):
            # load normal data
            data_send = efuse_data[start_idx:end_idx]
            if security_write:
                data_send = self.ecdh_encrypt_data(data_send)
            data_send = bflb_utils.int_to_4bytearray_l(start_idx) + data_send
            ret, dmy = self.process_one_cmd(cmd_name, cmd_id, data_send)
            if ret.startswith("OK") is False:
                bflb_utils.printf("Write failed")
                self.print_error_code("0021")
                return False
            # verify
            if verify >= 1:
                ret, read_data = self.efuse_read_main_process(
                    start_idx, end_idx - start_idx, shakehand=0, file=None, security_read=security_write
                )
                if ret is True and self.efuse_compare(
                    read_data,
                    mask_data[start_idx:end_idx],
                    efuse_data[start_idx:end_idx],
                ):
                    bflb_utils.printf("Verification succeeded")
                else:
                    # bflb_utils.printf("Read: ")
                    # bflb_utils.printf(binascii.hexlify(read_data[0:end_idx - start_idx]).decode("utf-8"))
                    # bflb_utils.printf("Expected: ")
                    # bflb_utils.printf(binascii.hexlify(efuse_data[start_idx:end_idx]).decode("utf-8"))
                    bflb_utils.printf("Verify failed")
                    self.print_error_code("0022")
                    return False
            return True

        if self.chip_type == "bl616":
            if len(efuse_data) > 256:
                bflb_utils.printf("Load efuse remainder")
                if not write_and_verify_all_data(256, 512):
                    return False
            if len(efuse_data) > 128:
                bflb_utils.printf("Load efuse 1")
                if not write_and_verify_all_data(128, 256):
                    return False
            bflb_utils.printf("Load efuse 0")
            if not write_and_verify_all_data(0, 128):
                return False
        else:
            bflb_utils.printf("Load efuse 0")
            if not write_and_verify_except_protect_data(0, 124):
                return False
            if not write_and_verify_protect_data(124, 128):
                return False
            if len(efuse_data) > 128:
                bflb_utils.printf("Load efuse 1")
                if not write_and_verify_except_protect_data(128, 252):
                    return False
                if not write_and_verify_protect_data(252, 256):
                    return False
            if len(efuse_data) > 256:
                bflb_utils.printf("Load efuse remainder")
                if not write_and_verify_except_protect_data(256, 508):
                    return False
                if not write_and_verify_protect_data(508, 512):
                    return False
        # bflb_utils.printf("Finished")
        return True

    def efuse_load_data_process(self, data, addr, func=0, verify=0, shakehand=0, security_write=False):
        bflb_utils.printf("========= efuse data load =========")
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False
        if int(addr) > 512 or (int(addr) + len(data) // 2) > 512:
            bflb_utils.printf("The efuse data is out of range")
            return False
        start_addr = 0x0
        efuse_data = bytearray(int(addr)) + bytearray.fromhex(data)
        if (int(addr) + len(data) // 2) % 16 != 0:
            efuse_data += bytearray(16 - (int(addr) + len(data) // 2) % 16)
        efuse_maskdata = bytearray(len(efuse_data))
        for num in range(0, len(efuse_data)):
            if efuse_data[num] != 0:
                efuse_maskdata[num] |= 0xFF
        bflb_utils.printf("Load efuse data")
        try:
            if func > 0:
                bflb_utils.printf("Read and check efuse data")
                ret, read_data = self.efuse_read_main_process(
                    start_addr, len(efuse_data), 0, file=None, security_read=security_write
                )
                i = int(addr) - start_addr
                for i in range(int(addr) - start_addr, int(addr) - start_addr + int(len(data) / 2)):
                    compare_data = read_data[i] | efuse_data[i]
                    if compare_data != read_data[i]:
                        bflb_utils.printf(
                            "The efuse data to be written can't overwrite the efuse area at ",
                            i + start_addr,
                        )
                        bflb_utils.printf(read_data[i])
                        bflb_utils.printf(efuse_data[i])
                        return False
        except Exception as error:
            bflb_utils.printf(error)
            return False
        ret = self.efuse_load_specified(None, None, efuse_data, efuse_maskdata, verify, security_write)
        return ret

    def efuse_read_main_process(self, start_addr, data_len, shakehand=0, file=None, security_read=False):
        readdata = bytearray(0)
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, None
        if security_read:
            cmd_name = "efuse_security_read"
        else:
            cmd_name = "efuse_read"
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(cmd_name)["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(data_len)
        ret, data_read = self.process_one_cmd(cmd_name, cmd_id, data_send)
        bflb_utils.printf("Read efuse")
        if ret.startswith("OK") is False:
            self.print_error_code("0020")
            return False, None
        readdata += data_read
        if security_read:
            readdata = self.ecdh_decrypt_data(readdata)
        bflb_utils.printf("Finished")
        if file is not None:
            with open(file, "wb+") as fp:
                fp.write(readdata)
        return True, readdata

    @staticmethod
    def efuse_compare(read_data, maskdata, write_data):
        i = 0
        for i in range(len(read_data)):
            compare_data = read_data[i] & maskdata[i]
            if (compare_data & write_data[i]) != write_data[i]:
                bflb_utils.printf("Compare failed: ", i)
                bflb_utils.printf(read_data[i], write_data[i])
                return False
        return True

    @staticmethod
    def efuse_create_mask_data(efuse_data):
        efuse_len = len(efuse_data)
        mask_data = bytearray(efuse_len)
        for i in range(0, efuse_len):
            if efuse_data[i] != 0:
                mask_data[i] |= 0xFF
        return mask_data

    def efuse_read_mac_addr_process(self, callback=None):
        readdata = bytearray(0)
        mac_len = self.get_mac_len()
        # handshake
        if self._need_handshake:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, None
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("efuse_read_mac")["cmd_id"])
        bflb_utils.printf("Read mac addr")
        ret, data_read = self.process_one_cmd("efuse_read_mac", cmd_id, bytearray(0))
        if ret.startswith("OK") is False:
            self.print_error_code("0023")
            return False, None
        # bflb_utils.printf(binascii.hexlify(data_read))
        readdata += data_read
        crcarray = bflb_utils.get_crc32_bytearray(readdata[:mac_len])
        if crcarray != readdata[mac_len : mac_len + 4]:
            bflb_utils.printf(binascii.hexlify(crcarray))
            bflb_utils.printf(binascii.hexlify(readdata[mac_len : mac_len + 4]))
            self.print_error_code("0025")
            return False, None
        return True, readdata[:mac_len]

    def flash_set_para_main_process(self, flash_pin, flash_para):
        bflb_utils.printf("========= flash set config =========")
        if flash_para != bytearray(0):
            if flash_para[13:14] == b"\xff":
                bflb_utils.printf("Skip set flash para due to flash id is 0xFF")
                # manufacturer id is 0xff, do not need set flash para
                return True
        # handshake
        if self._need_handshake:
            bflb_utils.printf("Flash set para handshake")
            if self._handshake() is False:
                return False
        start_time = time.time() * 1000
        # send command
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_set_para")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(flash_pin) + flash_para
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_set_para", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                self.print_error_code("003B")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Set para time cost(ms): ", round(time_cost, 3))
        return True

    def flash_read_jedec_id_process(self, callback=None):
        bflb_utils.printf("========= flash read jedec id =========")
        readdata = bytearray(0)
        # handshake
        if self._need_handshake:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, None
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_read_jid")["cmd_id"])
        ret, data_read = self.process_one_cmd("flash_read_jid", cmd_id, bytearray(0))
        bflb_utils.printf("Read flash jedec id")
        if ret.startswith("OK") is False:
            self.print_error_code("0030")
            return False, None
        readdata += data_read
        bflb_utils.printf("The read data is {}".format(binascii.hexlify(readdata)))
        return True, readdata[:4]

    def flash_para_update(self, file, jedec_id):
        flash_para = bytearray(0)
        ret, conf_path = self.get_flash_conf(jedec_id)
        if ret is True:
            bflb_utils.printf("The flash config is found")
            sub_module = __import__("libs." + self.chip_type, fromlist=[self.chip_type])
            (
                offset,
                flash_cfg_len,
                flash_para,
                flash_crc_offset,
                crc_offset,
            ) = bflb_flash_select.update_flash_para_from_cfg(
                sub_module.bootheader_cfg_keys.bootheader_cfg_keys, conf_path
            )
            with open(os.path.join(bflb_utils.app_path, file), "wb+") as fp:
                fp.write(flash_para)
        else:
            bflb_utils.printf("The flash config is not found, use default")
        return flash_para

    def flash_chiperase_main_process(self):
        bflb_utils.printf("Erase all flash chip")
        # handshake
        if self._need_handshake:
            bflb_utils.printf(FLASH_ERASE_HANDSHAKE)
            if self._handshake() is False:
                bflb_utils.printf("Handshake failed")
                return False
        start_time = time.time() * 1000
        # send command
        self.set_temp_timeout()
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_chiperase")["cmd_id"])
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_chiperase", cmd_id, bytearray(0))
            if ret.startswith("OK"):
                break
            elif ret.startswith("PD"):
                bflb_utils.printf("Erase pending")
                while True:
                    ret = self.bflb_serial_object.deal_ack()
                    if ret.startswith("PD"):
                        bflb_utils.printf("Erase pending")
                    else:
                        # clear uart fifo 'PD' data
                        self.bflb_serial_object.set_timeout(0.02)
                        self.bflb_serial_object.read(1000)
                        break
                    if (time.time() * 1000) - start_time > self._erase_time_out:
                        bflb_utils.printf("Erase timeout")
                        break
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                bflb_utils.printf("Erase failed")
                self.bflb_serial_object.set_timeout(self._default_timeout)
                self.print_error_code("0033")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Chip erase time cost(ms): ", round(time_cost, 3))
        self.bflb_serial_object.set_timeout(self._default_timeout)
        return True

    def flash_cfg_option(
        self,
        read_flash_id,
        flash_para_file,
        flash_set,
        id_valid_flag,
        binfile,
        cfgfile,
        cfg,
        create_img_callback=None,
        create_simple_callback=None,
    ):
        ret = bflb_flash_select.flash_bootheader_config_check(
            self.chip_type, read_flash_id, bflb_utils.convert_path(binfile), flash_para_file
        )
        if ret is False:
            bflb_utils.printf("The flashcfg does not match")
            # recreate bootinfo.bin
            if self.get_flash_conf(read_flash_id)[0] is True:
                bflb_utils.update_cfg(cfg, "FLASH_CFG", "flash_id", read_flash_id)
                if isinstance(cfgfile, BFConfigParser) is False:
                    cfg.write(cfgfile, "w+")
                if create_img_callback is not None:
                    create_img_callback()
                elif create_simple_callback is not None:
                    create_simple_callback()
            else:
                self.print_error_code("003D")
                return False
            ret = bflb_flash_select.flash_bootheader_config_check(
                self.chip_name, read_flash_id, bflb_utils.convert_path(binfile), flash_para_file
            )
            if ret is False:
                bflb_utils.printf("The flashcfg does not match again")
                self.print_error_code("0040")
                return False
        # set flash config
        if flash_para_file and id_valid_flag != "80":
            bflb_utils.printf("The flash para file is {}".format(os.path.normpath(flash_para_file)))
            fp = bflb_utils.open_file(flash_para_file, "rb")
            flash_para = bytearray(fp.read())
            fp.close()
            ret = self.flash_set_para_main_process(flash_set, flash_para)
            self._need_handshake = False
            if ret is False:
                return False
        return ret

    def flash_switch_bank_process(self, bank):
        """When the chip has two flashes, switch the flashes according to bank."""
        bflb_utils.printf("Flash switch bank")
        # handshake
        if self._need_handshake:
            bflb_utils.printf("Flash switch bank handshake")
            if self._handshake() is False:
                bflb_utils.printf("Handshake failed")
                return False
        start_time = time.time() * 1000
        # send command
        self.bflb_serial_object.set_timeout(self._erase_time_out / 1000)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_switch_bank")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(bank)
        ret, dmy = self.process_one_cmd("flash_switch_bank", cmd_id, data_send)
        if ret.startswith("OK") is False:
            bflb_utils.printf("Switch failed")
            self.bflb_serial_object.set_timeout(self._default_timeout)
            self.print_error_code("0042")
            return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Switch bank time cost(ms): ", round(time_cost, 3))
        self.bflb_serial_object.set_timeout(self._default_timeout)
        if bank == 0:
            self._flash2_select = False
        else:
            self._flash2_select = True
        return True

    def flash_load_opt(self, file, start_addr, callback=None):
        if self._need_handshake:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False
        if self._flash2_select is True:
            # start_addr -= self._flash1_size
            start_addr -= self._flash_size
        self.write_flash_data(file, start_addr, callback)
        ret = self.flash_load_main_process(file, start_addr, callback)
        if ret is False:
            bflb_utils.printf("Flash load failed")
            return ret
        # temp var to store imgage sha-256
        fw_sha256 = ""
        fp = bflb_utils.open_file(file, "rb")
        flash_data = fp.read()
        fp.close()
        flash_data_len = len(flash_data)
        if flash_data_len > (2 * 1024 * 1024):
            # if program file size is greater than 2*1024*1024, xip read sha will use more time
            timeout = 2.0 * (flash_data_len / (2 * 1024 * 1024) + 1)
            if timeout > self._default_timeout:
                self.bflb_serial_object.set_timeout(timeout)
        sh = hashlib.sha256()
        sh.update(flash_data)
        fw_sha256 = sh.hexdigest()
        fw_sha256 = bflb_utils.hexstr_to_bytearray(fw_sha256)
        bflb_utils.printf("SHA caled by host: ", binascii.hexlify(fw_sha256).decode("utf-8"))
        del sh
        # xip mode verify
        bflb_utils.printf("XIP mode verify")
        ret, read_data = self.flash_xip_read_sha_main_process(start_addr, flash_data_len, 0, None, callback)
        try:
            bflb_utils.printf("SHA caled by dev: ", binascii.hexlify(read_data).decode("utf-8"))
        except:
            bflb_utils.printf("SHA caled by dev: ", binascii.hexlify(read_data))
        if ret is True and read_data == fw_sha256:
            bflb_utils.printf("Verification succeeded")
        else:
            bflb_utils.printf("Verify failed")
            self.flash_load_tips()
            self.print_error_code("003E")
            ret = False
        if self.verify > 0:
            fp = bflb_utils.open_file(file, "rb")
            flash_data = bytearray(fp.read())
            fp.close()
            flash_data_len = len(flash_data)
            ret, read_data = self.flash_read_main_process(start_addr, flash_data_len, 0, None, callback)
            if ret is True and read_data == flash_data:
                bflb_utils.printf("Verification succeeded")
            else:
                bflb_utils.printf("Verify failed")
                self.flash_load_tips()
                self.print_error_code("003E")
                ret = False
            # sbus mode verify
            bflb_utils.printf("Sbus mode Verify")
            ret, read_data = self.flash_read_sha_main_process(start_addr, flash_data_len, 0, None, callback)
            bflb_utils.printf("SHA caled by dev: ", binascii.hexlify(read_data).decode("utf-8"))
            if ret is True and read_data == fw_sha256:
                bflb_utils.printf("Verification succeeded")
            else:
                bflb_utils.printf("Verify failed")
                self.flash_load_tips()
                self.print_error_code("003E")
                ret = False
        self.bflb_serial_object.set_timeout(self._default_timeout)
        # os.remove(file)
        return ret

    def flash_load_specified(self, file, start_addr, callback=None):
        ret = False
        run_state = 0
        temp_start_addr = start_addr
        if len(self._skip_len) > 0 and self._skip_len[0] > 0:
            fp = bflb_utils.open_file(file, "rb")
            flash_data = fp.read()
            fp.close()
            flash_data_len = len(flash_data)
            if (
                self._skip_addr[0] > (temp_start_addr + flash_data_len)
                or self._skip_addr[-1] + self._skip_len[-1] < temp_start_addr
            ):
                ret = self.flash_load_opt(file, start_addr, callback)
                return ret
            for i in range(len(self._skip_addr)):
                if (
                    self._skip_addr[i] <= start_addr
                    and self._skip_addr[i] + self._skip_len[i] > start_addr
                    and self._skip_addr[i] + self._skip_len[i] < temp_start_addr + flash_data_len
                ):
                    addr = self._skip_addr[i] + self._skip_len[i]
                    start_addr = self._skip_addr[i] + self._skip_len[i]
                elif (
                    self._skip_addr[i] > start_addr
                    and self._skip_addr[i] + self._skip_len[i] < temp_start_addr + flash_data_len
                ):
                    bflb_utils.printf(
                        "skip flash file, skip addr 0x%08X, skip len 0x%08X" % (self._skip_addr[i], self._skip_len[i])
                    )
                    addr = start_addr
                    data = flash_data[start_addr - temp_start_addr : self._skip_addr[i] - temp_start_addr]
                    filename, ext = os.path.splitext(file)
                    file_temp = os.path.join(bflb_utils.app_path, filename + "_skip" + str(i) + ext)
                    with open(file_temp, "wb") as fp:
                        fp.write(data)
                    ret = self.flash_load_opt(file_temp, addr, callback)
                    os.remove(file_temp)
                    start_addr = self._skip_addr[i] + self._skip_len[i]
                elif (
                    self._skip_addr[i] > start_addr
                    and self._skip_addr[i] < temp_start_addr + flash_data_len
                    and self._skip_addr[i] + self._skip_len[i] >= temp_start_addr + flash_data_len
                ):
                    bflb_utils.printf(
                        "skip flash file, skip addr 0x%08X, skip len 0x%08X" % (self._skip_addr[i], self._skip_len[i])
                    )
                    addr = start_addr
                    data = flash_data[start_addr - temp_start_addr : self._skip_addr[i] - temp_start_addr]
                    filename, ext = os.path.splitext(file)
                    file_temp = os.path.join(bflb_utils.app_path, filename + "_skip" + str(i) + ext)
                    with open(file_temp, "wb") as fp:
                        fp.write(data)
                    ret = self.flash_load_opt(file_temp, addr, callback)
                    os.remove(file_temp)
                    start_addr = temp_start_addr + flash_data_len
                elif (
                    self._skip_addr[i] <= start_addr
                    and self._skip_addr[i] + self._skip_len[i] >= temp_start_addr + flash_data_len
                ):
                    bflb_utils.printf(
                        "skip flash file, skip addr 0x%08X, skip len 0x%08X" % (self._skip_addr[i], self._skip_len[i])
                    )
                    start_addr = temp_start_addr + flash_data_len
                    return True
            if start_addr < temp_start_addr + flash_data_len:
                addr = start_addr
                data = flash_data[start_addr - temp_start_addr :]
                filename, ext = os.path.splitext(file)
                file_temp = os.path.join(bflb_utils.app_path, filename + "_skip" + str(i + 1) + ext)
                with open(file_temp, "wb") as fp:
                    fp.write(data)
                ret = self.flash_load_opt(file_temp, addr, callback)
                os.remove(file_temp)
        else:
            ret = self.flash_load_opt(file, start_addr, callback)
        return ret

    def flash_load_main_process(self, file, start_addr, callback=None):
        fp = bflb_utils.open_file(file, "rb")
        flash_data = bytearray(fp.read())
        fp.close()
        flash_data_len = len(flash_data)
        flash_size = self._flash_size
        if self._flash2_select is True:
            flash_size = self._flash2_size
        if flash_size < start_addr + flash_data_len:
            bflb_utils.printf(
                "Error: Write %s to 0x%08X, but it exceeds flash size 0x%08X" % (file, start_addr, flash_size)
            )
            self.print_error_code("0045")
            return False
        i = 0
        cur_len = 0
        if self.erase == 1:
            bflb_utils.printf("Start to erase flash")
            ret = self.flash_erase_main_process(start_addr, start_addr + flash_data_len - 1)
            if ret is False:
                return False
        start_time = time.time() * 1000
        log = ""
        if self.decompress_write and flash_data_len > 4 * 1024:
            # set rx timeout to 9s to avoid chip decompress data cause timeout
            self.bflb_serial_object.set_timeout(30.0)
            start_addr |= 0x80000000
            cmd_name = "flash_decompress_write"
            ret, flash_data, flash_data_len = self.flash_load_xz_compress(file)
            if ret is False:
                bflb_utils.printf("Flash write data xz failed")
                self.bflb_serial_object.set_timeout(self._default_timeout)
                return False
            chip_isp_timeout = 2000
            if self.chip_type == "bl616":
                # bl616 has set isp timeout to 10s in bflb_img_loader.py: img_get_bootinfo
                chip_isp_timeout = 10000
            # if compress take time > 2.2s, chip timeout, reshakehand
            if (time.time() * 1000) - start_time > chip_isp_timeout * 1.1:
                bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
                if self._handshake() is False:
                    return False
            # if compress take time > 1.8s, delay 0.6s make sure chip timeout, and reshakehand
            # if compress take time <= 1.8s, no need reshakehand
            elif (time.time() * 1000) - start_time > chip_isp_timeout * 0.9:
                time.sleep(chip_isp_timeout * 0.001 * 0.3)
                bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
                if self._handshake() is False:
                    return False
            bflb_utils.printf("Decompress flash load {}".format(flash_data_len))
        else:
            cmd_name = "flash_write"
        if self.chip_type == "bl616":
            if self._bflb_com_img_loader.bl616_a0:
                # write memory, set bl616 a0 bootrom uart timeout to 2s
                val = bflb_utils.int_to_2bytearray_l(8)
                start_addr_tmp = bflb_utils.int_to_4bytearray_l(0x6102DF04)
                write_data = bflb_utils.int_to_4bytearray_l(0x07D01200)
                cmd_id = bflb_utils.hexstr_to_bytearray("50")
                data = cmd_id + bytearray(1) + val + start_addr_tmp + write_data
                self.bflb_serial_object.if_write(data)
                ret, data_read_ack = self.bflb_serial_object.deal_ack(dmy_data=False)
            else:
                # 03 command to set bl616 ax bootrom uart timeout to 2s
                val = bflb_utils.int_to_2bytearray_l(4)
                timeout = bflb_utils.int_to_4bytearray_l(2000)
                cmd_id = bflb_utils.hexstr_to_bytearray("23")
                data = cmd_id + bytearray(1) + val + timeout
                self.bflb_serial_object.if_write(data)
                ret, data_read_ack = self.bflb_serial_object.deal_ack(dmy_data=False)
        bflb_utils.printf("========= flash load =========")
        bflb_utils.printf("========= writing {0}".format(file))
        while i < flash_data_len:
            cur_len = flash_data_len - i
            if cur_len > self._bflb_com_tx_size - 8:
                cur_len = self._bflb_com_tx_size - 8
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(cmd_name)["cmd_id"])
            data_send = bflb_utils.int_to_4bytearray_l(i + start_addr) + flash_data[i : i + cur_len]
            start_addr &= 0x7FFFFFFF
            try_cnt = 0
            while True:
                ret, dmy = self.process_one_cmd(cmd_name, cmd_id, data_send)
                if ret.startswith("OK"):
                    break
                if try_cnt < self._checksum_err_retry_limit:
                    bflb_utils.printf("Retry")
                    try_cnt += 1
                else:
                    self.print_error_code("0036")
                    self.bflb_serial_object.set_timeout(self._default_timeout)
                    return False
            i += cur_len
            length = len(str(flash_data_len)) + 1
            # log = "Load{:>8}/{:<8}[{}%]".format(i, flash_data_len, (i * 100) // flash_data_len)
            log = "Load{0}/{1}[{2}%]".format(
                str(i).rjust(length), str(flash_data_len).ljust(length), (i * 100) // flash_data_len
            )
            bflb_utils.printf(log)
            if callback is not None and flash_data_len > 200:
                callback(i, flash_data_len, "APP_WR")
        bflb_utils.printf(log)
        if self.flash_write_check_main_process() is False:
            bflb_utils.printf("Flash write check failed")
            self.bflb_serial_object.set_timeout(self._default_timeout)
            return False
        self.bflb_serial_object.set_timeout(self._default_timeout)
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Flash load time cost(ms): ", round(time_cost, 3))
        # bflb_utils.printf("Finished")
        return True

    def flash_xip_read_sha_main_process(self, start_addr, flash_data_len, shakehand=0, file=None, callback=None):
        readdata = bytearray(0)
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, None
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_xip_read_start")["cmd_id"])
        ret, dmy = self.process_one_cmd("flash_xip_read_start", cmd_id, bytearray(0))
        if ret.startswith("OK") is False:
            self.print_error_code("0039")
            return False, None
        start_time = time.time() * 1000
        log = ""
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_xip_readSha")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(flash_data_len)
        try_cnt = 0
        while True:
            ret, data_read = self.process_one_cmd("flash_xip_readSha", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                bflb_utils.printf("Read failed")
                # exit xip mode
                cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_xip_read_finish")["cmd_id"])
                ret, dmy = self.process_one_cmd("flash_xip_read_finish", cmd_id, bytearray(0))
                if ret.startswith("OK") is False:
                    self.print_error_code("0039")
                    return False, None
                return False, None
        log += "Read " + "SHA256" + "/" + str(flash_data_len)
        if callback is not None:
            callback(flash_data_len, flash_data_len, "APP_VR")
        readdata += data_read
        bflb_utils.printf(log)
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Flash xip readsha time cost(ms): ", round(time_cost, 3))
        # bflb_utils.printf("Finished")
        if file is not None:
            fp = bflb_utils.open_file(file, "wb+")
            fp.write(readdata)
            fp.close()
        # exit xip mode
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_xip_read_finish")["cmd_id"])
        ret, dmy = self.process_one_cmd("flash_xip_read_finish", cmd_id, bytearray(0))
        if ret.startswith("OK") is False:
            self.print_error_code("0039")
            return False, None
        return True, readdata

    def flash_read_sha_main_process(self, start_addr, flash_data_len, shakehand=0, file=None, callback=None):
        readdata = bytearray(0)
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, None
        start_time = time.time() * 1000
        log = ""
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_readSha")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(flash_data_len)
        try_cnt = 0
        while True:
            ret, data_read = self.process_one_cmd("flash_readSha", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                self.print_error_code("0038")
                return False, None
        log += "Read " + "SHA256" + "/" + str(flash_data_len)
        if callback is not None:
            callback(flash_data_len, flash_data_len, "APP_VR")
        readdata += data_read
        bflb_utils.printf(log)
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Flash readsha time cost(ms): ", round(time_cost, 3))
        # bflb_utils.printf("Finished")
        if file is not None:
            fp = bflb_utils.open_file(file, "wb+")
            fp.write(readdata)
            fp.close()
        return True, readdata

    @staticmethod
    def flash_load_xz_compress(file):
        try:
            xz_filters = [
                {"id": lzma.FILTER_LZMA2, "dict_size": 32768},
            ]
            fp = bflb_utils.open_file(file, "rb")
            data = bytearray(fp.read())
            fp.close()
            flash_data = lzma.compress(data, check=lzma.CHECK_CRC32, filters=xz_filters)
            flash_data_len = len(flash_data)
        except Exception as error:
            bflb_utils.printf(error)
            return False, None, None
        return True, flash_data, flash_data_len

    @staticmethod
    def flash_load_tips():
        bflb_utils.printf("########################################################################")
        bflb_utils.printf("请按照以下描述排查问题：")
        bflb_utils.printf("是否降低烧录波特率到500K测试过")
        bflb_utils.printf("烧写文件的大小是否超过Flash所能存储的最大空间")
        bflb_utils.printf("Flash是否被写保护")
        bflb_utils.printf("########################################################################")

    def flash_erase_main_process(self, start_addr, end_addr, shakehand=0):
        bflb_utils.printf("========= flash erase =========")
        bflb_utils.printf("Erase flash from {0} to {1}".format(hex(start_addr), hex(end_addr)))
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_ERASE_HANDSHAKE)
            if self._handshake() is False:
                bflb_utils.printf("Handshake failed")
                return False
        start_time = time.time() * 1000
        # send command
        self.set_temp_timeout()
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_erase")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(end_addr)
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_erase", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            elif ret.startswith("PD"):
                bflb_utils.printf("Erase pending")
                while True:
                    ret = self.bflb_serial_object.deal_ack()
                    if ret.startswith("PD"):
                        bflb_utils.printf("Erase pending")
                    else:
                        # clear uart fifo 'PD' data
                        self.bflb_serial_object.set_timeout(0.02)
                        self.bflb_serial_object.read(1000)
                        break
                    if (time.time() * 1000) - start_time > self._erase_time_out:
                        bflb_utils.printf("Erase timeout")
                        break
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                bflb_utils.printf("Erase failed")
                self.bflb_serial_object.set_timeout(self._default_timeout)
                self.print_error_code("0034")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Erase time cost(ms): ", round(time_cost, 3))
        self.bflb_serial_object.set_timeout(self._default_timeout)
        return True

    def flash_read_main_process(self, start_addr, flash_data_len, shakehand=0, file=None, callback=None):
        bflb_utils.printf("========= flash read =========")
        i = 0
        cur_len = 0
        readdata = bytearray(0)
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, None
        start_time = time.time() * 1000
        log = ""
        while i < flash_data_len:
            cur_len = flash_data_len - i
            if cur_len > self._bflb_com_tx_size - 8:
                cur_len = self._bflb_com_tx_size - 8
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_read")["cmd_id"])
            data_send = bflb_utils.int_to_4bytearray_l(i + start_addr) + bflb_utils.int_to_4bytearray_l(cur_len)
            try_cnt = 0
            while True:
                ret, data_read = self.process_one_cmd("flash_read", cmd_id, data_send)
                if ret.startswith("OK"):
                    break
                if try_cnt < self._checksum_err_retry_limit:
                    bflb_utils.printf("Retry")
                    try_cnt += 1
                else:
                    self.print_error_code("0035")
                    return False, None
            i += cur_len
            log += "Read " + str(i) + "/" + str(flash_data_len)
            if len(log) > 50:
                bflb_utils.printf(log)
                log = ""
            else:
                log += "\n"
            if callback is not None:
                callback(i, flash_data_len, "APP_VR")
            readdata += data_read
        bflb_utils.printf(log)
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Flash read time cost(ms): ", round(time_cost, 3))
        # bflb_utils.printf("Finished")
        if file is not None:
            with open(file, "wb+") as fp:
                fp.write(readdata)
        return True, readdata

    def flash_write_check_main_process(self, shakehand=0):
        bflb_utils.printf("Start to check flash")
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False
        # send command
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_write_check")["cmd_id"])
        try_cnt = 0
        while True:
            retry = 0
            if self.decompress_write:
                retry = 10
            ret, dmy = self.process_one_cmd("flash_write_check", cmd_id, bytearray(0))
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit + retry:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                self.print_error_code("0037")
                return False
        return True

    @staticmethod
    def flash_get_size(jedec_id):
        bflb_utils.printf("The jedec id is {}".format(jedec_id))
        capacity_id = int(jedec_id[-2:], 16)
        bflb_utils.printf("The capacity id is {}".format(capacity_id))
        if capacity_id == 0:
            return 0
        flash_size_level = capacity_id & 0x1F
        flash_size_level -= 0x13
        flash_size = (1 << flash_size_level) * 512 * 1024
        # bflb_utils.printf("The capacity is {}M".format(flash_size / 1024 / 1024))
        return flash_size

    def flash_get_otp_size(self):
        bflb_utils.printf("Read flash otp param")
        ret, param = self.flash_otp_get_para_main_process()
        if ret is False or len(param) == 0:
            return False
        param_int = bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(param))
        region_cnt = param_int & 0x3F
        secreg_size = (param_int >> 12) & 0x3F
        flash_otp_size = region_cnt * secreg_size * 256
        return flash_otp_size

    def flash_read_status_reg_process(self, cmd, len, callback=None):
        bflb_utils.printf("========= flash read status register =========")
        readdata = bytearray(0)
        # handshake
        if self._need_handshake:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, None
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_read_status_reg")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(int(cmd, 16)) + bflb_utils.int_to_4bytearray_l(len)
        ret, data_read = self.process_one_cmd("flash_read_status_reg", cmd_id, data_send)
        bflb_utils.printf("Read flash status register")
        if ret.startswith("OK") is False:
            self.print_error_code("0031")
            return False, None
        readdata += data_read
        bflb_utils.printf("The read data is {}".format(binascii.hexlify(readdata)))
        return True, readdata

    def flash_write_status_reg_process(self, cmd, len, write_data, callback=None):
        bflb_utils.printf("========= flash write status register =========")
        # handshake
        if self._need_handshake:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, "Flash load handshake failed"

        bflb_utils.printf("write data is {}".format(write_data))
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_write_status_reg")["cmd_id"])
        data_send = (
            bflb_utils.int_to_4bytearray_l(int(cmd, 16))
            + bflb_utils.int_to_4bytearray_l(len)
            + bflb_utils.int_to_4bytearray_l(int(write_data, 16))
        )
        ret, data_read = self.process_one_cmd("flash_write_status_reg", cmd_id, data_send)
        bflb_utils.printf("Write flash status register")
        if ret.startswith("OK") is False:
            self.print_error_code("0032")
            return False, "Write failed"
        # bflb_utils.printf("Finished")
        return True, None

    def flash_otp_set_para_main_process(self, flash_otp_para_file):
        bflb_utils.printf("Set flash otp config")
        try:
            with open(flash_otp_para_file, "rb") as f:
                flash_otp_para = f.read()
        except:
            bflb_utils.printf("Flash otp param file is none existent")
            self.print_error_code("003B")
            return False
        # handshake
        if self._need_handshake:
            bflb_utils.printf("Flash set otp para handshake")
            if self._handshake() is False:
                return False
        start_time = time.time() * 1000
        # send command
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_set_para")["cmd_id"])
        ret, data_send = bflb_utils.convert_flash_otp_param_from_bytes(flash_otp_para)
        if ret is False:
            bflb_utils.printf("Error: {}".format(data_send))
            self.print_error_code("003B")
            return False
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_otp_set_para", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                self.print_error_code("003B")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Set para time cost(ms): ", round(time_cost, 3))
        return True

    def flash_otp_get_para_main_process(self):
        bflb_utils.printf("========= flash otp get param =========")
        readdata = bytearray(0)
        # handshake
        if self._need_handshake:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if self._handshake() is False:
                return False, None
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_get_para")["cmd_id"])
        ret, data_read = self.process_one_cmd("flash_otp_get_para", cmd_id, bytearray(0))
        bflb_utils.printf("Read flash otp param")
        if ret.startswith("OK") is False:
            self.print_error_code("003B")
            return False, None
        readdata += data_read
        bflb_utils.printf("The read data is {}".format(binascii.hexlify(readdata)))
        return True, readdata[:4]

    def flash_otp_erase_by_addr_main_process(self, start_addr, erase_len, shakehand=0):
        bflb_utils.printf("========= flash otp erase =========")
        bflb_utils.printf("Erase flash otp addr from {0}, the length is {1}".format(hex(start_addr), hex(erase_len)))
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_ERASE_HANDSHAKE)

            if self._handshake() is False:
                bflb_utils.printf("Handshake failed")
                return False
        start_time = time.time() * 1000
        # send command
        self.set_temp_timeout()
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_erase")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(erase_len)
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_otp_erase", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            else:
                bflb_utils.printf("Erase pending")
                while True:
                    if (time.time() * 1000) - start_time > self._erase_time_out:
                        bflb_utils.printf("Erase timeout")
                        break
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                bflb_utils.printf("Erase failed")
                self.bflb_serial_object.set_timeout(self._default_timeout)
                self.print_error_code("0034")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Erase otp time cost(ms): ", round(time_cost, 3))
        self.bflb_serial_object.set_timeout(self._default_timeout)
        return True

    def flash_otp_read_by_addr_main_process(self, start_addr, flash_data_len, shakehand=0, file=None, callback=None):
        bflb_utils.printf("========= flash otp read =========")
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if not self._handshake():
                return False, None
        start_time = time.time() * 1000
        readdata = bytearray()
        total_read = 0
        log = ""
        while total_read < flash_data_len:
            cur_len = min(self._bflb_com_tx_size - 8, flash_data_len - total_read)
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_read")["cmd_id"])
            data_send = bflb_utils.int_to_4bytearray_l(total_read + start_addr) + bflb_utils.int_to_4bytearray_l(
                cur_len
            )
            for _ in range(self._checksum_err_retry_limit):
                ret, data_read = self.process_one_cmd("flash_otp_read", cmd_id, data_send)
                if ret.startswith("OK"):
                    break
                bflb_utils.printf("Retry")
            else:
                self.print_error_code("0035")
                return False, None
            readdata += data_read
            total_read += cur_len
            log += f"Read {total_read}/{flash_data_len}\n"
            if len(log) > 50:
                bflb_utils.printf(log)
                log = ""
            if callback:
                callback(total_read, flash_data_len, "APP_VR")
        bflb_utils.printf(log)
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Flash otp read time cost(ms): ", round(time_cost, 3))
        # bflb_utils.printf("Finished")
        if file is not None:
            with open(file, "wb+") as fp:
                fp.write(readdata)
        return True, readdata

    def flash_otp_write_by_addr_main_process(self, start_addr, flash_file, shakehand=0, callback=None):
        bflb_utils.printf("========= flash otp write =========")
        with open(flash_file, "rb") as fp:
            flash_data = fp.read()
        bflb_utils.printf("Write flash otp from {0}, the length is {1}".format(hex(start_addr), hex(len(flash_data))))
        if start_addr > self._flash_otp_size or (start_addr + len(flash_data)) > self._flash_otp_size:
            bflb_utils.printf("Error: The write size is out of range.")
            return False
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_ERASE_HANDSHAKE)
            if self._handshake() is False:
                bflb_utils.printf("Handshake failed")
                return False
        start_time = time.time() * 1000
        total_written = 0
        log = ""
        block_size = self._bflb_com_tx_size
        for i in range(0, len(flash_data), block_size):
            cur_len = min(block_size, len(flash_data) - i)
            write_data = flash_data[i : i + cur_len]
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_write")["cmd_id"])
            data_send = bflb_utils.int_to_4bytearray_l(i + start_addr) + write_data
            try_cnt = 0
            while True:
                ret, dmy = self.process_one_cmd("flash_otp_write", cmd_id, data_send)
                if ret.startswith("OK"):
                    break
                if try_cnt < self._checksum_err_retry_limit:
                    bflb_utils.printf("Retry")
                    try_cnt += 1
                else:
                    self.print_error_code("0036")
                    return False
            total_written += cur_len
            log += f"Written {total_written}/{len(flash_data)}\n"
            if len(log) > 50:
                print(log)
                log = ""
            if callback is not None:
                callback(total_written, len(flash_data), "APP_VR")
        bflb_utils.printf(log)
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Flash otp write time cost(ms): ", round(time_cost, 3))
        # bflb_utils.printf("Finished")
        return True

    def flash_otp_lock_by_addr_main_process(self, start_addr, end_addr):
        bflb_utils.printf("========= flash otp lock by addr =========")
        # handshake
        if self._need_handshake:
            if self._handshake() is False:
                return False
        start_time = time.time() * 1000
        # send command
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_lock_by_addr")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(end_addr)
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_otp_lock_by_addr", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                self.print_error_code("0092")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Set flash otp lock time cost(ms): ", round(time_cost, 3))
        return True

    def flash_otp_lock_by_index_main_process(self, lock_index):
        bflb_utils.printf("========= flash otp lock by index =========")
        bflb_utils.printf("Lock index is {}".format(lock_index))
        # handshake
        if self._need_handshake:
            if self._handshake() is False:
                return False
        start_time = time.time() * 1000
        # send command
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_lock_by_index")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(lock_index)
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_otp_lock", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                self.print_error_code("0092")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Set flash otp lock time cost(ms): ", round(time_cost, 3))
        return True

    def flash_otp_erase_by_index_main_process(self, index, shakehand=0):
        bflb_utils.printf(f"========= flash otp erase index{index} =========")
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_ERASE_HANDSHAKE)
            if self._handshake() is False:
                bflb_utils.printf("Handshake failed")
                return False
        start_time = time.time() * 1000
        # send command
        self.set_temp_timeout()
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_erase_by_index")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(index)
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_otp_erase", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            else:
                bflb_utils.printf("Erase pending")
                while True:
                    if (time.time() * 1000) - start_time > self._erase_time_out:
                        bflb_utils.printf("Erase timeout")
                        break
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                bflb_utils.printf("Erase failed")
                self.bflb_serial_object.set_timeout(self._default_timeout)
                self.print_error_code("0034")
                return False
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Erase otp index time cost(ms): ", round(time_cost, 3))
        self.bflb_serial_object.set_timeout(self._default_timeout)
        return True

    def flash_otp_read_by_index_main_process(self, index, flash_data_len, shakehand=0, file=None, callback=None):
        bflb_utils.printf(f"========= flash otp read index{index} =========")
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_LOAD_HANDSHAKE)
            if not self._handshake():
                return False, None
        start_time = time.time() * 1000
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_read_by_index")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(index) + bflb_utils.int_to_4bytearray_l(flash_data_len)
        for _ in range(self._checksum_err_retry_limit):
            ret, data_read = self.process_one_cmd("flash_otp_read", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            bflb_utils.printf("Retry")
        else:
            self.print_error_code("0035")
            return False, None
        if callback:
            callback(flash_data_len, flash_data_len, "APP_VR")
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Flash otp read by index time cost(ms): ", round(time_cost, 3))
        # bflb_utils.printf("Finished")
        if file is not None:
            with open(file, "wb+") as fp:
                fp.write(data_read)
        return True, data_read

    def flash_otp_write_by_index_main_process(self, index, flash_file, shakehand=0, callback=None):
        bflb_utils.printf(f"========= flash otp write index{index} =========")
        with open(flash_file, "rb") as fp:
            flash_data = fp.read()
        bflb_utils.printf("Write flash otp len is {}".format(hex(len(flash_data))))
        if (len(flash_data)) > self._flash_otp_size:
            bflb_utils.printf("Error: The write size exceeds flash otp size")
            return False
        # handshake
        if shakehand:
            bflb_utils.printf(FLASH_ERASE_HANDSHAKE)
            if self._handshake() is False:
                bflb_utils.printf("Handshake failed")
                return False
        start_time = time.time() * 1000
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get("flash_otp_write_by_index")["cmd_id"])
        data_send = bflb_utils.int_to_4bytearray_l(index) + flash_data
        try_cnt = 0
        while True:
            ret, dmy = self.process_one_cmd("flash_otp_write", cmd_id, data_send)
            if ret.startswith("OK"):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf("Retry")
                try_cnt += 1
            else:
                self.print_error_code("0036")
                return False
        if callback is not None:
            callback(len(flash_data), len(flash_data), "APP_VR")
        time_cost = (time.time() * 1000) - start_time
        bflb_utils.printf("Flash otp write by index time cost(ms): ", round(time_cost, 3))
        # bflb_utils.printf("Finished")
        return True


class BL602EflashLoader(BaseEflashLoader):
    """
    When chip is bl602, eflash Loader
    """

    def __init__(
        self,
        chip_type,
        args,
        config,
        callback=None,
        macaddr_callback=None,
        create_simple_callback=None,
        create_img_callback=None,
        task_num=None,
    ):
        super().__init__(
            chip_type,
            args,
            config,
            callback,
            macaddr_callback,
            create_simple_callback,
            create_img_callback,
            task_num,
        )
        self.chip_type = chip_type

    def get_flash_pin(self):
        return 0xFF

    def set_boot_speed(self):
        if self.isp_mode_sign is True:
            self.boot_speed = self.speed

    def set_load_function(self):
        self.load_function = 1

    def set_temp_timeout(self):
        self.bflb_serial_object.set_timeout(self._default_timeout)

    def print_identify_fail(self):
        bflb_utils.printf("Eflash loader identify flash failed")
        self.print_error_code("0043")
        return False


class BL616EflashLoader(BaseEflashLoader):
    """
    When chip is bl616,bl616l,bl616d, eflash Loader
    """

    def __init__(
        self,
        chip_type,
        args,
        config,
        callback=None,
        macaddr_callback=None,
        create_simple_callback=None,
        create_img_callback=None,
        task_num=None,
    ):
        super().__init__(
            chip_type,
            args,
            config,
            callback,
            macaddr_callback,
            create_simple_callback,
            create_img_callback,
            task_num,
        )
        self.chip_type = chip_type

    def run_flash_extra(self):
        """
        If chip is bl616, it will run this function.
        """
        # flash2 init
        if self.cfg.has_option("FLASH2_CFG", "flash2_en"):
            self._flash2_en = self.cfg.get("FLASH2_CFG", "flash2_en") == "true"
            if self._flash2_en is True:
                # self._flash1_size = (int(self.cfg.get("FLASH2_CFG", "flash1_size")) * 1024 * 1024)
                # self._flash2_size = (int(self.cfg.get("FLASH2_CFG", "flash2_size")) * 1024 * 1024)
                bflb_utils.printf("Set flash2 para")
                flash2_pin = 0
                flash2_clock_cfg = 0
                flash2_io_mode = 0
                flash2_clk_delay = 0
                if self.cfg.get("FLASH2_CFG", "flash2_pin"):
                    flash_pin_cfg = self.cfg.get("FLASH2_CFG", "flash2_pin")
                    if flash_pin_cfg.startswith("0x"):
                        flash2_pin = int(flash_pin_cfg, 16)
                    else:
                        flash2_pin = int(flash_pin_cfg, 10)
                if self.cfg.has_option("FLASH2_CFG", "flash2_clock_cfg"):
                    clock_div_cfg = self.cfg.get("FLASH2_CFG", "flash2_clock_cfg")
                    if clock_div_cfg.startswith("0x"):
                        flash2_clock_cfg = int(clock_div_cfg, 16)
                    else:
                        flash2_clock_cfg = int(clock_div_cfg, 10)
                if self.cfg.has_option("FLASH2_CFG", "flash2_io_mode"):
                    io_mode_cfg = self.cfg.get("FLASH2_CFG", "flash2_io_mode")
                    if io_mode_cfg.startswith("0x"):
                        flash2_io_mode = int(io_mode_cfg, 16)
                    else:
                        flash2_io_mode = int(io_mode_cfg, 10)
                if self.cfg.has_option("FLASH2_CFG", "flash2_clock_delay"):
                    clk_delay_cfg = self.cfg.get("FLASH2_CFG", "flash2_clock_delay")
                    if clk_delay_cfg.startswith("0x"):
                        flash2_clk_delay = int(clk_delay_cfg, 16)
                    else:
                        flash2_clk_delay = int(clk_delay_cfg, 10)
                self.flash2_set = (
                    (flash2_pin << 0) + (flash2_clock_cfg << 8) + (flash2_io_mode << 16) + (flash2_clk_delay << 24)
                )
                if self.load_function == 2:
                    bflb_utils.printf("Set flash2 cfg: %X" % (self.flash2_set))
                    ret = self.flash_set_para_main_process(self.flash2_set, bytearray(0))
                    self._need_handshake = False
                    if ret is False:
                        return False, self.flash_burn_retry
                # switch to flash2 ctrl
                ret = self.flash_switch_bank_process(1)
                self._need_handshake = False
                if ret is False:
                    return False, self.flash_burn_retry
                # recreate bootinfo.bin
                ret, data = self.flash_read_jedec_id_process()
                if ret:
                    self._need_handshake = False
                    data = binascii.hexlify(data).decode("utf-8")
                    self.id2_valid_flag = data[6:]
                    read_id2 = data[0:6]
                    self.read_flash2_id = read_id2
                    if self.cfg.has_option("FLASH2_CFG", "flash2_para"):
                        flash2_para_file = os.path.join(bflb_utils.app_path, self.cfg.get("FLASH2_CFG", "flash2_para"))
                        self.flash_para_update(flash2_para_file, read_id2)

                        # flash2 set flash para iomode=0x11
                        fp = bflb_utils.open_file(flash2_para_file, "rb")
                        para_data = bytearray(fp.read())
                        fp.close()
                        para_data[0:1] = b"\x11"
                        fp = bflb_utils.open_file(flash2_para_file, "wb+")
                        fp.write(para_data)
                        fp.close()
                    if self.get_flash_conf(self.read_flash2_id)[0] is False:
                        self.print_error_code("003D")
                        return False, self.flash_burn_retry
                    else:
                        self._flash2_size = self.flash_get_size(self.read_flash2_id)
                        bflb_utils.printf("Get flash2 size: 0x%08X" % (self._flash2_size))

                else:
                    self.print_error_code("0030")
                    return False, self.flash_burn_retry
                # switch to default flash1 ctrl
                ret = self.flash_switch_bank_process(0)
                self._need_handshake = False
                if ret is False:
                    return False, self.flash_burn_retry
        return True, "continue"

    def get_flash1_and_flash2(self, flash_file, address, size_current, i):
        # if self._flash1_size != 0 and self._flash1_size < int(address[i], 16) + size_current and \
        #   self._flash1_size > int(address[i], 16) and self._flash2_select is False:
        if (
            self._flash_size != 0
            and self._flash_size < int(address[i], 16) + size_current
            and self._flash_size > int(address[i], 16)
            and self._flash2_select is False
            and self._flash2_en is True
        ):
            bflb_utils.printf("{} size exceeds flash1".format(flash_file[i]))
            (
                flash1_bin,
                flash1_bin_len,
                flash2_bin,
                flash2_bin_len,
            ) = self.flash_loader_cut_flash_bin(flash_file[i], int(address[i], 16), self._flash_size)
            # self.flash_loader_cut_flash_bin(flash_file[i], int(address[i], 16), self._flash1_size)
            return flash1_bin, flash1_bin_len, flash2_bin, flash2_bin_len
        else:
            return "", 0, "", 0

    def get_new_bh_data(self, section, bh_data, fp):
        if section == "BOOTHEADER_GROUP0_CFG":
            fp.write(bh_data[100 : 100 + 20])

    def get_flash_pin_from_bootinfo(self, chiptype, bootinfo):
        sw_usage_data = bootinfo[22:24] + bootinfo[20:22] + bootinfo[18:20] + bootinfo[16:18]
        sw_usage_data = int(sw_usage_data, 16)
        return (sw_usage_data >> 14) & 0x3F

    def set_clear_boot_status(self, shakehand=0):
        self.clear_boot_status(shakehand)

    def write_flash_data(self, file, start_addr, callback):
        # bl616 no need check flash rf para
        pass


class BL628EflashLoader(BaseEflashLoader):
    """
    When chip is bl628, eflash Loader
    """

    def __init__(
        self,
        chip_type,
        args,
        config,
        callback=None,
        macaddr_callback=None,
        create_simple_callback=None,
        create_img_callback=None,
        task_num=None,
    ):
        super().__init__(
            chip_type,
            args,
            config,
            callback,
            macaddr_callback,
            create_simple_callback,
            create_img_callback,
            task_num,
        )
        self.chip_type = chip_type

    def get_new_bh_data(self, section, bh_data, fp):
        if section == "BOOTHEADER_GROUP0_CFG":
            fp.write(bh_data[100 : 100 + 24])

    def set_clear_boot_status(self, shakehand=0):
        self.clear_boot_status(shakehand)

    def write_flash_data(self, file, start_addr, callback):
        # bl628 no need check flash rf para
        pass


class BL702EflashLoader(BaseEflashLoader):
    """
    When chip is bl702, eflash Loader
    """

    def __init__(
        self,
        chip_type,
        args,
        config,
        callback=None,
        macaddr_callback=None,
        create_simple_callback=None,
        create_img_callback=None,
        task_num=None,
    ):
        super().__init__(
            chip_type,
            args,
            config,
            callback,
            macaddr_callback,
            create_simple_callback,
            create_img_callback,
            task_num,
        )
        self.chip_type = chip_type

    def get_flash_pin(self):
        return 0xFF

    def print_identify_fail(self):
        bflb_utils.printf("Eflash loader identify flash failed")
        self.print_error_code("0043")
        return False

    def run_reset_cpu(self):
        if self.isp_mode_sign is True or ("reset" in self.config and self.config["reset"]):
            self.reset_cpu()

    def get_chip_id(self, bootinfo):
        chip_id = (
            bootinfo[32:34]
            + bootinfo[34:36]
            + bootinfo[36:38]
            + bootinfo[38:40]
            + bootinfo[40:42]
            + bootinfo[42:44]
            + bootinfo[44:46]
            + bootinfo[46:48]
        )
        return chip_id

    def get_mac_len(self):
        return 8

    def get_isp_sh_time(self):
        return self._isp_shakehand_timeout

    def set_temp_timeout(self):
        self.bflb_serial_object.set_timeout(self._default_timeout)

    def set_load_function(self):
        if self.chip_type == "bl702":
            self.load_function = 0

    def set_decompress_write(self):
        self.decompress_write = False


class BL702LEflashLoader(BaseEflashLoader):
    """
    When chip is bl702l, eflash Loader
    """

    def __init__(
        self,
        chip_type,
        args,
        config,
        callback=None,
        macaddr_callback=None,
        create_simple_callback=None,
        create_img_callback=None,
        task_num=None,
    ):
        super().__init__(
            chip_type,
            args,
            config,
            callback,
            macaddr_callback,
            create_simple_callback,
            create_img_callback,
            task_num,
        )
        self.chip_type = chip_type

    def run_reset_cpu(self):
        if self.isp_mode_sign is True or ("reset" in self.config and self.config["reset"]):
            self.reset_cpu()

    def get_chip_id(self, bootinfo):
        chip_id = (
            bootinfo[32:34]
            + bootinfo[34:36]
            + bootinfo[36:38]
            + bootinfo[38:40]
            + bootinfo[40:42]
            + bootinfo[42:44]
            + bootinfo[44:46]
            + bootinfo[46:48]
        )
        return chip_id

    def get_new_bh_data(self, section, bh_data, fp):
        if section == "BOOTHEADER_CFG":
            fp.write(bh_data[100 : 100 + 16])

    def get_mac_len(self):
        return 8

    def get_isp_sh_time(self):
        return self._isp_shakehand_timeout

    def get_flash_pin_from_bootinfo(self, chiptype, bootinfo):
        dev_info_data = bootinfo[30:32] + bootinfo[28:30] + bootinfo[26:28] + bootinfo[24:26]
        dev_info_data = int(dev_info_data, 16)
        flash_cfg = (dev_info_data >> 26) & 7
        sf_reverse = (dev_info_data >> 29) & 1
        sf_swap_cfg = (dev_info_data >> 22) & 3
        if flash_cfg == 0:
            return 0
        else:
            if sf_reverse == 0:
                return sf_swap_cfg + 1
            else:
                return sf_swap_cfg + 5

    def set_temp_timeout(self):
        self.bflb_serial_object.set_timeout(self._default_timeout)


class BL808EflashLoader(BaseEflashLoader):
    """
    When chip is bl808, eflash Loader
    """

    def __init__(
        self,
        chip_type,
        args,
        config,
        callback=None,
        macaddr_callback=None,
        create_simple_callback=None,
        create_img_callback=None,
        task_num=None,
    ):
        super().__init__(
            chip_type,
            args,
            config,
            callback,
            macaddr_callback,
            create_simple_callback,
            create_img_callback,
            task_num,
        )
        self.chip_type = chip_type

    def get_new_bh_data(self, section, bh_data, fp):
        if section == "BOOTHEADER_GROUP0_CFG":
            fp.write(bh_data[100 : 100 + 28])

    def get_flash_pin_from_bootinfo(self, chiptype, bootinfo):
        sw_usage_data = bootinfo[22:24] + bootinfo[20:22] + bootinfo[18:20] + bootinfo[16:18]
        sw_usage_data = int(sw_usage_data, 16)
        return (sw_usage_data >> 14) & 0x1F

    def set_clear_boot_status(self, shakehand=0):
        self.clear_boot_status(shakehand)

    def write_flash_data(self, file, start_addr, callback):
        fp = bflb_utils.open_file(file, "rb")
        flash_data = bytearray(fp.read())
        fp.close()
        flash_data_len = len(flash_data)
        end_addr = start_addr + flash_data_len - 1
        if start_addr <= 0x1000 and end_addr > 0x1000:
            ret, flash_read_data = self.flash_read_main_process(0x1000, 0x1000, 0, None, callback)
            if flash_read_data[0:4] == bflb_utils.int_to_4bytearray_b(0x424C5246):
                bflb_utils.printf("RF para already written at flash 0x1000 addr, replace it.")
                flash_data[0x1000:0x2000] = flash_read_data[0x0:0x1000]
                fp = bflb_utils.open_file(file, "wb")
                fp.write(flash_data)
                fp.close()

    def get_flash_conf(self, flash_id):
        cfg_dir = os.path.join(bflb_utils.app_path, "utils", "flash")
        conf_name = bflb_flash_select.get_suitable_file_name(cfg_dir, flash_id)
        conf_path = os.path.join(cfg_dir, conf_name)
        if os.path.isfile(conf_path) is False:
            return False, conf_path
        else:
            return True, conf_path


class OtherEflashLoader(BaseEflashLoader):
    def __init__(
        self,
        chip_type,
        args,
        config,
        callback=None,
        macaddr_callback=None,
        create_simple_callback=None,
        create_img_callback=None,
        task_num=None,
    ):
        super().__init__(
            chip_type,
            args,
            config,
            callback,
            macaddr_callback,
            create_simple_callback,
            create_img_callback,
            task_num,
        )
        self.chip_type = chip_type
