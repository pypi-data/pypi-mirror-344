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
import binascii
import traceback
import threading
from libs import bflb_utils
from libs import bflb_img_create
from libs import bflb_serial


class BflbImgLoader(object):
    def __init__(
        self,
        device,
        speed,
        boot_speed,
        interface="uart",
        chip_type="bl602",
        chip_name="bl602",
        eflash_loader_file1="",
        eflash_loader_file2="",
        callback=None,
        do_reset=False,
        reset_hold_time=100,
        shake_hand_delay=100,
        reset_revert=True,
        cutoff_time=0,
        shake_hand_retry=2,
        isp_mode_sign=False,
        isp_timeout=0,
        encrypt_key=None,
        encrypt_iv=None,
        public_key=None,
        private_key=None,
        **kwargs,
    ):
        self._device = device
        self._speed = speed
        self._interface = interface.lower()
        self._chip_type = chip_type
        self._chip_name = chip_name
        self._eflash_loader_file1 = eflash_loader_file1
        self._eflash_loader_file2 = eflash_loader_file2
        self._callback = callback
        self._do_reset = do_reset
        self._reset_hold_time = reset_hold_time
        self._shake_hand_delay = shake_hand_delay
        self._reset_revert = reset_revert
        self._cutoff_time = cutoff_time
        self._shake_hand_retry = shake_hand_retry
        self._isp_mode_sign = isp_mode_sign
        self._isp_timeout = isp_timeout
        self._boot_speed = boot_speed
        self.encrypt_key = encrypt_key
        self.encrypt_iv = encrypt_iv
        self.public_key = public_key
        self.private_key = private_key

        self._boot_load = True
        self._record_bootinfo = None
        self.bflb_serial_object = None
        self._imge_fp = None
        self._segcnt = 0
        self._602a0_dln_fix = False
        self.isp_baudrate = 2000000

        self.bl616_a0 = False

        if interface == "uart":
            self.bflb_serial_object = bflb_serial.BLSerialUart(rts_state=True, dtr_state=True)
        # elif interface == "sdio":
        #    self.bflb_serial_object = bflb_interface_sdio.BflbSdioPort()

        if "pwd" in kwargs:
            self._pwd = kwargs["pwd"]
        else:
            self._pwd = None
        if self._pwd:
            self.bflb_serial_object.set_password(self._pwd)

        self._bootrom_cmds = {
            "get_chip_id": {"cmd_id": "05", "data_len": "0000", "callback": None},
            "get_boot_info": {"cmd_id": "10", "data_len": "0000", "callback": None},
            "load_boot_header": {"cmd_id": "11", "data_len": "00b0", "callback": None},
            "808_load_boot_header": {"cmd_id": "11", "data_len": "0160", "callback": None},
            "628_load_boot_header": {"cmd_id": "11", "data_len": "0100", "callback": None},
            "616_load_boot_header": {"cmd_id": "11", "data_len": "0100", "callback": None},
            "702l_load_boot_header": {"cmd_id": "11", "data_len": "00F0", "callback": None},
            "616l_load_boot_header": {"cmd_id": "11", "data_len": "0100", "callback": None},
            "616d_load_boot_header": {"cmd_id": "11", "data_len": "0100", "callback": None},
            "load_sha384_p2": {"cmd_id": "1b", "data_len": "0010", "callback": None},
            "load_publick_key": {"cmd_id": "12", "data_len": "0044", "callback": None},
            "load_publick_key_384": {"cmd_id": "12", "data_len": "0064", "callback": None},
            "load_publick_key2": {"cmd_id": "13", "data_len": "0044", "callback": None},
            "load_publick_key2_384": {"cmd_id": "13", "data_len": "0064", "callback": None},
            "load_signature": {"cmd_id": "14", "data_len": "0004", "callback": None},
            "load_signature2": {"cmd_id": "15", "data_len": "0004", "callback": None},
            "load_aes_iv": {"cmd_id": "16", "data_len": "0014", "callback": None},
            "load_seg_header": {"cmd_id": "17", "data_len": "0010", "callback": None},
            "load_seg_data": {"cmd_id": "18", "data_len": "0100", "callback": None},
            "check_image": {"cmd_id": "19", "data_len": "0000", "callback": None},
            "run_image": {"cmd_id": "1a", "data_len": "0000", "callback": None},
            "change_rate": {"cmd_id": "20", "data_len": "0008", "callback": None},
            "reset": {"cmd_id": "21", "data_len": "0000", "callback": None},
            "set_timeout": {"cmd_id": "23", "data_len": "0004", "callback": None},
            "flash_erase": {"cmd_id": "30", "data_len": "0000", "callback": None},
            "flash_write": {"cmd_id": "31", "data_len": "0100", "callback": None},
            "flash_read": {"cmd_id": "32", "data_len": "0100", "callback": None},
            "flash_boot": {"cmd_id": "33", "data_len": "0000", "callback": None},
            "efuse_write": {"cmd_id": "40", "data_len": "0080", "callback": None},
            "efuse_read": {"cmd_id": "41", "data_len": "0000", "callback": None},
            "memory_write": {"cmd_id": "50", "data_len": "0080", "callback": None},
            "memory_read": {"cmd_id": "51", "data_len": "0000", "callback": None},
        }

    def close_port(self):
        if self.bflb_serial_object is not None:
            self.bflb_serial_object.close()

    def boot_process_load_cmd(self, section, read_len):
        read_data = bytearray(0)
        if read_len != 0:
            read_data = bytearray(self._imge_fp.read(read_len))
            if len(read_data) != read_len:
                bflb_utils.printf("Read error, expected len=", read_len, "read len=", len(read_data))
                return bytearray(0)
            if section == "load_boot_header":
                val = bflb_utils.bytearray_reverse(read_data[120:124])
                self._segcnt = bflb_utils.bytearray_to_int(val)
                bflb_utils.printf("The segcnt is ", self._segcnt)
            elif section == "808_load_boot_header":
                val = bflb_utils.bytearray_reverse(read_data[140:144])
                self._segcnt = bflb_utils.bytearray_to_int(val)
                bflb_utils.printf("The segcnt is ", self._segcnt)
            elif section == "628_load_boot_header":
                val = bflb_utils.bytearray_reverse(read_data[136:140])
                self._segcnt = bflb_utils.bytearray_to_int(val)
                bflb_utils.printf("The segcnt is ", self._segcnt)
            elif section == "616_load_boot_header":
                val = bflb_utils.bytearray_reverse(read_data[132:136])
                self._segcnt = bflb_utils.bytearray_to_int(val)
                bflb_utils.printf("The segcnt is ", self._segcnt)
            elif section == "702l_load_boot_header":
                val = bflb_utils.bytearray_reverse(read_data[120:124])
                self._segcnt = bflb_utils.bytearray_to_int(val)
                bflb_utils.printf("The segcnt is ", self._segcnt)
            elif section == "616l_load_boot_header":
                val = bflb_utils.bytearray_reverse(read_data[132:136])
                self._segcnt = bflb_utils.bytearray_to_int(val)
                bflb_utils.printf("The segcnt is ", self._segcnt)
            elif section == "616d_load_boot_header":
                val = bflb_utils.bytearray_reverse(read_data[132:136])
                self._segcnt = bflb_utils.bytearray_to_int(val)
                bflb_utils.printf("The segcnt is ", self._segcnt)
            if section == "load_signature" or section == "load_signature2":
                val = bflb_utils.bytearray_reverse(read_data[0:4])
                sig_len = bflb_utils.bytearray_to_int(val)
                read_data = read_data + bytearray(self._imge_fp.read(sig_len + 4))
                if len(read_data) != (sig_len + 8):
                    bflb_utils.printf(
                        "read signature error,expected len=",
                        sig_len + 4,
                        "read len=",
                        len(read_data),
                    )
        return read_data

    def boot_process_one_cmd(self, section, cmd_id, cmd_len, baudrate=None):
        read_len = bflb_utils.bytearray_to_int(cmd_len)
        read_data = self._bootrom_cmds.get(section)["callback"](section, read_len)
        data_read = bytearray(0)
        # in case data len change for some case
        data_byte = bflb_utils.int_to_2bytearray_l(len(read_data))
        data = cmd_id + bytearray(1) + data_byte + read_data

        if self._chip_type == "bl702" and section == "run_image":
            sub_module = __import__("libs." + self._chip_type, fromlist=[self._chip_type])
            data = sub_module.chiptype_patch.img_load_create_predata_before_run_img()
        baudrate_tmp = self.bflb_serial_object.get_baudrate()
        if baudrate:
            self.bflb_serial_object.set_baudrate(baudrate)
        self.bflb_serial_object.write(data)
        if section == "get_boot_info" or section == "load_seg_header" or section == "get_chip_id":
            res, data_read = self.bflb_serial_object.deal_response()
        else:
            res = self.bflb_serial_object.deal_ack()
        if res.startswith("OK") is True:
            pass
        else:
            self.bflb_serial_object.set_baudrate(baudrate_tmp)
            try:
                bflb_utils.printf("Response: ", res)
            except IOError:
                bflb_utils.printf("Python IO error")
        return res, data_read

    def boot_process_one_section(self, section, data_len, baudrate=None):
        cmd_id = bflb_utils.hexstr_to_bytearray(self._bootrom_cmds.get(section)["cmd_id"])
        if data_len == 0:
            length = bflb_utils.hexstr_to_bytearray(self._bootrom_cmds.get(section)["data_len"])
        else:
            length = bflb_utils.int_to_2bytearray_b(data_len)

        return self.boot_process_one_cmd(section, cmd_id, length, baudrate=baudrate)

    def boot_inf_change_rate(self, comnum, section, newrate):
        cmd_id = bflb_utils.hexstr_to_bytearray(self._bootrom_cmds.get(section)["cmd_id"])
        cmd_len = bflb_utils.hexstr_to_bytearray(self._bootrom_cmds.get(section)["data_len"])
        bflb_utils.printf(
            "process",
            section,
            ",cmd=",
            binascii.hexlify(cmd_id),
            ",data len=",
            binascii.hexlify(cmd_len),
        )
        baudrate = self.bflb_serial_object.if_get_rate()
        oldv = bflb_utils.int_to_4bytearray_l(baudrate)
        newv = bflb_utils.int_to_4bytearray_l(newrate)
        data_bytearry = bytearray(3)
        data_bytearry[1] = cmd_len[1]
        data_bytearry[2] = cmd_len[0]
        data = cmd_id + data_bytearry + oldv + newv
        self.bflb_serial_object.if_write(data)
        stime = (11 * 10) / float(baudrate) * 2
        if stime < 0.003:
            stime = 0.003
        time.sleep(stime)
        # self.bflb_serial_object.if_close()
        self.bflb_serial_object.repeat_init(comnum, newrate, self._chip_type, self._chip_name)
        return self.bflb_serial_object.deal_ack(dmy_data=False)

    def boot_install_cmds_callback(self):
        self._bootrom_cmds.get("get_chip_id")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("get_boot_info")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_boot_header")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("808_load_boot_header")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("628_load_boot_header")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("616_load_boot_header")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("702l_load_boot_header")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("616l_load_boot_header")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("616d_load_boot_header")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_sha384_p2")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_publick_key")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_publick_key2")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_publick_key_384")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_publick_key2_384")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_signature")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_signature2")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_aes_iv")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_seg_header")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("load_seg_data")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("check_image")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("run_image")["callback"] = self.boot_process_load_cmd
        self._bootrom_cmds.get("reset")["callback"] = self.boot_process_load_cmd

    def print_issue_log(self):
        bflb_utils.printf("########################################################################")
        bflb_utils.printf("请按照以下描述排查问题：")
        if self._chip_type == "bl60x":
            bflb_utils.printf("GPIO24是否上拉到板子自身的3.3V，而不是外部的3.3V")
            bflb_utils.printf("GPIO7(RX)是否连接到USB转串口的TX引脚")
            bflb_utils.printf("GPIO14(TX)是否连接到USB转串口的RX引脚")
            bflb_utils.printf("在使用烧录软件进行烧录前，是否在GPIO24拉高的情况下，使用Reset/Chip_En复位了芯片")
        elif self._chip_type == "bl602":
            bflb_utils.printf("GPIO8是否上拉到板子自身的3.3V，而不是外部的3.3V")
            bflb_utils.printf("GPIO7(RX)是否连接到USB转串口的TX引脚")
            bflb_utils.printf("GPIO16(TX)是否连接到USB转串口的RX引脚")
            bflb_utils.printf("在使用烧录软件进行烧录前，是否在GPIO8拉高的情况下，使用Reset/Chip_En复位了芯片")
        elif self._chip_type == "bl702":
            bflb_utils.printf("GPIO28是否上拉到板子自身的3.3V，而不是外部的3.3V")
            bflb_utils.printf("GPIO15(RX)是否连接到USB转串口的TX引脚")
            bflb_utils.printf("GPIO14(TX)是否连接到USB转串口的RX引脚")
            bflb_utils.printf("在使用烧录软件进行烧录前，是否在GPIO28拉高的情况下，使用Reset/Chip_En复位了芯片")
        else:
            bflb_utils.printf("Boot pin是否上拉到板子自身的3.3V，而不是外部的3.3V")
            bflb_utils.printf("UART RX是否连接到USB转串口的TX引脚")
            bflb_utils.printf("UART TX是否连接到USB转串口的RX引脚")
            bflb_utils.printf("在使用烧录软件进行烧录前，是否在Boot pin拉高的情况下，使用Reset/Chip_En复位了芯片")
        bflb_utils.printf("烧录软件所选择的COM口，是否是连接芯片的串口")
        bflb_utils.printf("烧录软件上选择的波特率是否是USB转串口支持的波特率")
        bflb_utils.printf("3.3V供电是否正常")
        bflb_utils.printf("板子供电电流是否正常(烧录模式下，芯片耗电电流5-7mA)")
        bflb_utils.printf("########################################################################")

    def send_sync_command(self, speed):
        try:
            while True:
                if self._handshake_flag is True:
                    break
                if self._chip_type == "bl702" or self._chip_type == "bl702l":
                    self.bflb_serial_object.write(self.get_sync_bytes(int(0.003 * speed / 10)))
                else:
                    self.bflb_serial_object.write(self.get_sync_bytes(int(0.006 * speed / 10)))
        except Exception as error:
            bflb_utils.printf("Error: {}".format(error))

    def set_isp_baudrate(self, isp_baudrate):
        bflb_utils.printf("ISP mode speed: ", isp_baudrate)
        self.isp_baudrate = isp_baudrate

    def toggle_boot_or_handshake(
        self,
        run_sign,
        do_reset=False,
        reset_hold_time=100,
        shake_hand_delay=100,
        reset_revert=True,
        cutoff_time=0,
        isp_mode_sign=False,
        isp_timeout=0,
        boot_load=False,
        shake_hand_retry=2,
    ):
        """
        When run_sign is 2, it run shakehand.
        """
        device = self._device
        # speed = self._speed
        speed = self.bflb_serial_object._baudrate
        if run_sign == 2:
            pass
        elif run_sign == 1:
            shake_hand_retry = 1
        if self.bflb_serial_object:
            try:
                timeout = self.bflb_serial_object.get_timeout()
                blusbserialwriteflag = False
                if isp_mode_sign and isp_timeout > 0:
                    wait_timeout = isp_timeout
                    self.bflb_serial_object.set_timeout(0.1)
                    self._handshake_flag = False
                    # do not auto toggle DTR&RTS
                    cutoff_time = 0
                    do_reset = False
                    # set baudrate to 2000000 for shakehand with boot2
                    self.bflb_serial_object.repeat_init(device, self.isp_baudrate, self._chip_type, self._chip_name)
                    # send reboot to make sure boot2 is running
                    self.bflb_serial_object.write(b"\r\nispboot if\r\nreboot\r\n")
                    # send 5555 to boot2, boot2 jump to bootrom if mode
                    fl_thrx = None
                    fl_thrx = threading.Thread(target=self.send_sync_command, args=(speed,))
                    fl_thrx.setDaemon(True)
                    fl_thrx.start()

                    bflb_utils.printf("Please press reset key")
                    # reset low
                    # self.bflb_serial_object.set_rts(0)
                    self.bflb_serial_object.set_rts(1)
                    # RC delay is 100ms
                    time.sleep(0.2)
                    # reset high
                    # self.bflb_serial_object.set_rts(1)
                    self.bflb_serial_object.set_rts(0)

                    time_stamp = time.time()
                    ack = bytearray(0)
                    while time.time() - time_stamp < wait_timeout:
                        if self._chip_type == "bl602" or self._chip_type == "bl702":
                            self.bflb_serial_object.set_timeout(0.01)

                            # self.bflb_serial_object.clear_buf()
                            # success, ack = self.bflb_serial_object.read(3000)
                            success, data = self.bflb_serial_object.read(3000)
                            ack += data
                            if ack.find(b"Boot2 ISP Shakehand Suss") != -1:
                                self._handshake_flag = True
                                if ack.find(b"Boot2 ISP Ready") != -1:
                                    bflb_utils.printf("ISP ready")
                                    self.bflb_serial_object.write(bytearray.fromhex("a0000000"))
                                    self.bflb_serial_object.set_timeout(timeout)
                                    return "OK"
                        else:
                            success, data = self.bflb_serial_object.read(3000)
                            ack += data
                            if ack.find(b"Boot2 ISP Ready") != -1:
                                bflb_utils.printf("ISP ready")
                                self._handshake_flag = True
                        if self._handshake_flag is True:
                            self.bflb_serial_object.set_timeout(timeout)
                            val_timeout = self.bflb_serial_object.get_timeout()
                            self.bflb_serial_object.set_timeout(0.1)
                            if self._chip_type == "bl602" or self._chip_type == "bl702":
                                self.bflb_serial_object.set_timeout(0.5)
                                # read 15 byte key word
                                success, data = self.bflb_serial_object.read(15)
                                ack += data
                                # reduce timeout and read 15 byte again, make sure recv all key word
                                self.bflb_serial_object.set_timeout(0.005)
                                ack += self.bflb_serial_object.read(15)[1]
                                self.bflb_serial_object.set_timeout(val_timeout)
                                bflb_utils.printf("Read ready")
                                if ack.find(b"Boot2 ISP Ready") == -1:
                                    bflb_utils.printf("Boot2 isp is not ready")
                                    return "FL"
                                else:
                                    self.bflb_serial_object.write(bytearray.fromhex("a0000000"))
                                    time.sleep(0.002)
                                    return "OK"
                            else:
                                while True:
                                    # clear boot2 log
                                    ack = self.bflb_serial_object.raw_read()
                                    if len(ack) == 0:
                                        break
                                time.sleep(0.1)
                                while True:
                                    # clear boot2 log
                                    ack = self.bflb_serial_object.raw_read()
                                    if len(ack) == 0:
                                        break
                            self.bflb_serial_object.set_timeout(val_timeout)
                            break

                    self._handshake_flag = True
                    self.bflb_serial_object.set_timeout(timeout)
                    # set actual baudrate
                    self.bflb_serial_object.repeat_init(device, speed, self._chip_type, self._chip_name)
                    time.sleep(2.2)

                if self.bflb_serial_object._is_bouffalo_chip() and boot_load:
                    blusbserialwriteflag = True
                # cut of tx rx power and rst
                while shake_hand_retry > 0:
                    if cutoff_time != 0 and blusbserialwriteflag is not True:
                        cutoff_revert = False
                        if cutoff_time > 1000:
                            cutoff_revert = True
                            cutoff_time = cutoff_time - 1000
                        # MP_TOOL_V3 generate rising pulse to make D trigger output low
                        # reset low
                        self.bflb_serial_object.set_rts(1)  
                        # RC delay is 100ms
                        time.sleep(0.2)
                        # reset high
                        self.bflb_serial_object.set_rts(0)  
                        time.sleep(0.05)
                        # do power off
                        # reset low
                        self.bflb_serial_object.set_rts(1)  
                        if cutoff_revert:
                            # dtr high, power off
                            self.bflb_serial_object.set_dtr(0)  
                        else:
                            # dtr low, power off
                            self.bflb_serial_object.set_dtr(1)  
                        bflb_utils.printf("Power off tx and rx, press the device")
                        # bflb_utils.printf("The cutoff time is ", cutoff_time / 1000.0)
                        time.sleep(cutoff_time / 1000.0)
                        if cutoff_revert:
                            # dtr low, power on
                            self.bflb_serial_object.set_dtr(1) 
                        else:
                            # dtr high, power on
                            self.bflb_serial_object.set_dtr(0)  
                        bflb_utils.printf("Power on tx and rx ")
                        time.sleep(0.1)
                    else:
                        if run_sign == 2:
                            self.bflb_serial_object.set_dtr(0)  
                            bflb_utils.printf("Default set DTR high ")
                            time.sleep(0.1)
                    if do_reset is True and blusbserialwriteflag is not True:
                        # MP_TOOL_V3 reset high to make boot pin high
                        self.bflb_serial_object.set_rts(0)  
                        time.sleep(0.2)
                        if reset_revert:
                            # reset low for reset revert to make boot pin high when cpu rset
                            self.bflb_serial_object.set_rts(1)  
                            time.sleep(0.001)
                        reset_cnt = 2
                        if reset_hold_time > 1000:
                            reset_cnt = int(reset_hold_time // 1000)
                            reset_hold_time = reset_hold_time % 1000
                        while reset_cnt > 0:
                            if reset_revert:
                                # reset high
                                self.bflb_serial_object.set_rts(0)  
                            else:
                                # reset low
                                self.bflb_serial_object.set_rts(1)  
                            # Boot high
                            # self.bflb_serial_object.set_dtr(0)
                            time.sleep(reset_hold_time / 1000.0)
                            if reset_revert:
                                # reset low
                                self.bflb_serial_object.set_rts(1)
                            else:
                                # reset high
                                self.bflb_serial_object.set_rts(0)  
                            if shake_hand_delay > 0:
                                time.sleep(shake_hand_delay / 1000.0)
                            else:
                                time.sleep(5 / 1000.0)

                            # do reset agian to make sure boot pin is high
                            if reset_revert:
                                # reset high
                                self.bflb_serial_object.set_rts(0)  
                            else:
                                # reset low
                                self.bflb_serial_object.set_rts(1)  
                            # Boot high
                            # self.bflb_serial_object.set_dtr(0)
                            time.sleep(reset_hold_time / 1000.0)
                            if reset_revert:
                                # reset low
                                self.bflb_serial_object.set_rts(1)  
                            else:
                                # reset high
                                self.bflb_serial_object.set_rts(0)  
                            if shake_hand_delay > 0:
                                time.sleep(shake_hand_delay / 1000.0)
                            else:
                                time.sleep(5 / 1000.0)
                            reset_cnt -= 1
                        """
                        bflb_utils.printf(
                            "reset cnt: "
                            + str(reset_cnt)
                            + ", reset hold: "
                            + str(reset_hold_time / 1000.0)
                            + ", handshake delay: "
                            + str(shake_hand_delay / 1000.0)
                        )
                        """
                    if blusbserialwriteflag:
                        self.bflb_serial_object.bl_usb_serial_write(cutoff_time, reset_revert)
                    # clean buffer before start
                    bflb_utils.printf("Clean buffer")
                    self.bflb_serial_object.set_timeout(0.1)
                    self.bflb_serial_object.clear_buf()
                    # run toggle_boot
                    if run_sign == 1:
                        self.bflb_serial_object.set_timeout(timeout)
                        return "OK"
                    # handshake
                    if self._602a0_dln_fix:
                        self.bflb_serial_object.set_timeout(0.5)
                    else:
                        self.bflb_serial_object.set_timeout(0.1)
                    bflb_utils.printf("Send sync")
                    # send keep 6ms ,N*10/baudrate=0.01
                    if self._chip_type == "bl702" or self._chip_type == "bl702l":
                        self.bflb_serial_object.write(self.get_sync_bytes(int(0.003 * speed / 10)))
                    else:
                        self.bflb_serial_object.write(self.get_sync_bytes(int(0.006 * speed / 10)))
                    if self._chip_type == "bl808":
                        time.sleep(0.3)
                        self.bflb_serial_object.write(bflb_utils.hexstr_to_bytearray("5000080038F0002000000018"))
                    if self._602a0_dln_fix:
                        time.sleep(4)
                    success, ack = self.bflb_serial_object.read(1000)

                    bflb_utils.printf("The ack data is {}".format(binascii.hexlify(ack)))
                    if ack.find(b"\x4F") != -1 or ack.find(b"\x4B") != -1:
                        self.bflb_serial_object.set_timeout(timeout)
                        if self._602a0_dln_fix:
                            self.bflb_serial_object.write(bytearray(2))
                        if self.bflb_serial_object._password:
                            cmd = bflb_utils.hexstr_to_bytearray("2400")
                            cmd += bflb_utils.int_to_2bytearray_l(len(self.bflb_serial_object._password) // 2)
                            cmd += bflb_utils.hexstr_to_bytearray(self.bflb_serial_object._password)
                            self.bflb_serial_object.write(cmd)
                            success, ack = self.bflb_serial_object.read(2)
                            bflb_utils.printf(
                                "Set pswd ack is ",
                                binascii.hexlify(ack).decode("utf-8"),
                            )
                        return "OK"
                    if len(ack) != 0:
                        # peer is alive, but handshake it's not expected, do again
                        bflb_utils.printf("Retry handshake")
                        if do_reset is False:
                            bflb_utils.printf("Sleep")
                            time.sleep(3)
                    else:
                        bflb_utils.printf("Retry")
                    shake_hand_retry -= 1
                self.bflb_serial_object.set_timeout(timeout)
                return "FL"
            except Exception as error:
                bflb_utils.printf("Error: {}".format(error))
        else:
            return "FL"

    def img_get_bootinfo(
        self,
        sh_baudrate,
        wk_baudrate,
        callback=None,
        do_reset=False,
        reset_hold_time=100,
        shake_hand_delay=100,
        reset_revert=True,
        cutoff_time=0,
        shake_hand_retry=2,
        isp_mode_sign=False,
        isp_timeout=0,
        boot_load=True,
        boot_baudrate=500000,
    ):
        bflb_utils.printf("========= image get bootinfo =========")
        ret = self.img_load_handshake(
            sh_baudrate,
            wk_baudrate,
            do_reset,
            reset_hold_time,
            shake_hand_delay,
            reset_revert,
            cutoff_time,
            shake_hand_retry,
            isp_mode_sign,
            isp_timeout,
            boot_load,
        )

        if ret == "shake hand fail" or ret == "change rate fail":
            bflb_utils.printf("Handshake failed")
            self.bflb_serial_object.close()
            return False, b""

        time.sleep(0.5)
        ret, data_read = self.boot_process_one_section("get_boot_info", 0, baudrate=boot_baudrate)
        if ret.startswith("OK") is False:
            bflb_utils.printf("Get boot info failed")
            return ret, b""
        # check with image file
        data_read = binascii.hexlify(data_read)
        if self._chip_type == "bl616":
            if data_read.decode("utf-8")[:2] == "01":
                self.bl616_a0 = True
                # write memory, set bl616 a0 bootrom uart timeout to 10s
                val = bflb_utils.int_to_2bytearray_l(8)
                start_addr = bflb_utils.int_to_4bytearray_l(0x6102DF04)
                write_data = bflb_utils.int_to_4bytearray_l(0x27101200)
                cmd_id = bflb_utils.hexstr_to_bytearray(self._bootrom_cmds.get("memory_write")["cmd_id"])
                data = cmd_id + bytearray(1) + val + start_addr + write_data
                self.bflb_serial_object.write(data)
                ret, data_read_ack = self.bflb_serial_object.deal_ack(dmy_data=False)
            else:
                # 03 command to set bl616 ax bootrom uart timeout to 10s
                val = bflb_utils.int_to_2bytearray_l(4)
                timeout = bflb_utils.int_to_4bytearray_l(10000)
                cmd_id = bflb_utils.hexstr_to_bytearray(self._bootrom_cmds.get("set_timeout")["cmd_id"])
                data = cmd_id + bytearray(1) + val + timeout
                self.bflb_serial_object.write(data)
                ret, data_read_ack = self.bflb_serial_object.deal_ack(dmy_data=False)
        bflb_utils.printf("The read data is {}".format(data_read))
        return True, data_read

    def img_load_handshake(
        self,
        sh_baudrate,
        wk_baudrate,
        do_reset=False,
        reset_hold_time=100,
        shake_hand_delay=100,
        reset_revert=True,
        cutoff_time=0,
        shake_hand_retry=2,
        isp_mode_sign=False,
        isp_timeout=0,
        boot_load=True,
    ):
        self.bflb_serial_object.repeat_init(self._device, sh_baudrate, self._chip_type, self._chip_name)

        self.boot_install_cmds_callback()
        if self._chip_type == "bl602":
            self._602a0_dln_fix = False
        # shake_hand_retry = 2
        bflb_utils.printf("Start handshake")
        ret = self.toggle_boot_or_handshake(
            2,
            do_reset,
            reset_hold_time,
            shake_hand_delay,
            reset_revert,
            cutoff_time,
            isp_mode_sign,
            isp_timeout,
            boot_load,
            shake_hand_retry,
        )
        if self._chip_type == "bl602":
            self._602a0_dln_fix = False
        if ret != "OK":
            bflb_utils.printf("Handshake failed")
            self.print_issue_log()
            bflb_utils.set_error_code("0050")
            return "shake hand fail"
        if sh_baudrate != wk_baudrate:
            if self.boot_inf_change_rate(self._device, "change_rate", wk_baudrate) != "OK":
                bflb_utils.printf("Change rate failed")
                return "change rate fail"
        bflb_utils.printf("Handshake succeeded")
        return ret

    ########################main process###############################################

    def img_load_main_process(self, img_file, group, record_bootinfo=None, **kwargs):
        encrypt_blk_size = 16
        # self._imge_fp = open(img_file, 'rb')

        bflb_utils.printf("Get boot info")
        # get boot information before download
        ret, data_read = self.boot_process_one_section("get_boot_info", 0)
        if ret.startswith("OK") is False:
            bflb_utils.printf("Get boot info failed")
            return ret, None
        # check with image file
        data_read = binascii.hexlify(data_read)
        bflb_utils.printf("The read data is {}".format(data_read))
        bootinfo = data_read.decode("utf-8")
        chipid = ""
        if self._chip_type == "bl702" or self._chip_type == "bl702l":
            chipid = (
                bootinfo[32:34]
                + bootinfo[34:36]
                + bootinfo[36:38]
                + bootinfo[38:40]
                + bootinfo[40:42]
                + bootinfo[42:44]
                + bootinfo[44:46]
                + bootinfo[46:48]
            )
        else:
            chipid = (
                bootinfo[34:36]
                + bootinfo[32:34]
                + bootinfo[30:32]
                + bootinfo[28:30]
                + bootinfo[26:28]
                + bootinfo[24:26]
            )
        bflb_utils.printf("========= chip id: ", chipid, " =========")
        bflb_utils.printf("Last boot info: ", record_bootinfo)
        if record_bootinfo is not None and bootinfo[8:] == record_bootinfo[8:]:
            bflb_utils.printf("Repeated chip")
            return "repeat_burn", bootinfo
        if bootinfo[:8] == "FFFFFFFF" or bootinfo[:8] == "ffffffff":
            bflb_utils.printf("Eflash loader present")
            return "error_shakehand", bootinfo
        sign = 0
        encrypt = 0
        sign_384 = 0
        if self._chip_type == "bl60x":
            sign = int(data_read[8:10], 16) & 0x03
            encrypt = (int(data_read[8:10], 16) & 0x0C) >> 2
        elif self._chip_type == "bl602" or self._chip_type == "bl702" or self._chip_type == "bl702l":
            sign = int(data_read[8:10], 16)
            encrypt = int(data_read[10:12], 16)
        elif self._chip_type == "bl808" or self._chip_type == "bl628":
            if group == 0:
                sign = int(data_read[8:10], 16)
                encrypt = int(data_read[12:14], 16)
            else:
                sign = int(data_read[10:12], 16)
                encrypt = int(data_read[14:16], 16)
        elif self._chip_type == "bl616l":
            sign = int(data_read[8:10], 16)
            encrypt = int(data_read[10:12], 16)
            sign_384 = sign == 2
        elif self._chip_type == "bl616d":
            sign = int(data_read[8:10], 16)
            encrypt = int(data_read[10:12], 16)
            sign_384 = sign == 2
        else:
            sign = int(data_read[8:10], 16)
            encrypt = int(data_read[10:12], 16)
        bflb_utils.printf("sign is ", sign, " encrypt is ", encrypt)
        if img_file:
            eflash_loader_dir = os.path.dirname(img_file)
            eflash_loader_file = os.path.basename(img_file).split(".")[0]
            suffix = os.path.basename(img_file).split(".")[1]

        # encrypt eflash loader helper bin
        privatekey_str = None
        if "privatekey_str" in kwargs and kwargs["privatekey_str"]:
            privatekey_str = kwargs["privatekey_str"]
        if (self.encrypt_key and self.encrypt_iv) or self.private_key or privatekey_str:
            if sign and not self.private_key and not privatekey_str:
                bflb_utils.printf("Error: private key must be provided")
                return "", bootinfo
            if encrypt and (not self.encrypt_key or not self.encrypt_iv):
                bflb_utils.printf("Error: aes key and aes iv must be provided")
                return "", bootinfo
            ret, encrypted_data = bflb_img_create.encrypt_loader_bin(
                self._chip_type,
                img_file,
                sign,
                encrypt,
                self.encrypt_key,
                self.encrypt_iv,
                self.public_key,
                self.private_key,
                **kwargs,
            )
            if ret is True:
                # create new eflash loader helper bin
                filename, ext = os.path.splitext(img_file)
                file_encrypt = filename + "_encrypt" + ext
                with open(file_encrypt, "wb") as fp:
                    fp.write(encrypted_data)
                self._imge_fp = open(file_encrypt, "rb")
            else:
                img_file = os.path.join(bflb_utils.app_path, img_file)
                self._imge_fp = open(img_file, "rb")
        elif encrypt or sign:
            try:
                post_proc = kwargs.get("post_proc", False)
                if post_proc is False:
                    eflash_loader_file = eflash_loader_file + "_encrypt.bin"
                else:
                    eflash_loader_file = eflash_loader_file + "." + suffix
                img_file = os.path.join(bflb_utils.app_path, eflash_loader_dir, eflash_loader_file)
                self._imge_fp = open(img_file, "rb")
            except Exception as error:
                bflb_utils.printf(error)
                return "", bootinfo
        else:
            img_file = os.path.join(bflb_utils.app_path, img_file)
            self._imge_fp = open(img_file, "rb")
        bflb_utils.printf("Download {0}".format(img_file))
        # start to process load flow
        if self._chip_type == "bl808":
            ret, dmy = self.boot_process_one_section("808_load_boot_header", 0)
        elif self._chip_type == "bl628":
            ret, dmy = self.boot_process_one_section("628_load_boot_header", 0)
        elif self._chip_type == "bl616":
            ret, dmy = self.boot_process_one_section("616_load_boot_header", 0)
        elif self._chip_type == "bl702l":
            ret, dmy = self.boot_process_one_section("702l_load_boot_header", 0)
        elif self._chip_type == "bl616l":
            ret, dmy = self.boot_process_one_section("616l_load_boot_header", 0)
        elif self._chip_type == "bl616d":
            ret, dmy = self.boot_process_one_section("616d_load_boot_header", 0)
        else:
            ret, dmy = self.boot_process_one_section("load_boot_header", 0)
        if ret.startswith("OK") is False:
            return ret, bootinfo
        if sign_384:
            ret, dmy = self.boot_process_one_section("load_sha384_p2", 0)
            if ret.startswith("OK") is False:
                return ret, bootinfo
        if sign:
            if sign_384:
                ret, dmy = self.boot_process_one_section("load_publick_key_384", 0)
            else:
                ret, dmy = self.boot_process_one_section("load_publick_key", 0)
            if ret.startswith("OK") is False:
                return ret, bootinfo
            if self._chip_type == "bl60x" or self._chip_type == "bl808" or self._chip_type == "bl628":
                if sign_384:
                    ret, dmy = self.boot_process_one_section("load_publick_key2_384", 0)
                else:
                    ret, dmy = self.boot_process_one_section("load_publick_key2", 0)
                if ret.startswith("OK") is False:
                    return ret, bootinfo
            ret, dmy = self.boot_process_one_section("load_signature", 0)
            if ret.startswith("OK") is False:
                return ret, bootinfo
            if self._chip_type == "bl60x" or self._chip_type == "bl808" or self._chip_type == "bl628":
                ret, dmy = self.boot_process_one_section("load_signature2", 0)
                if ret.startswith("OK") is False:
                    return ret, bootinfo
        if encrypt:
            ret, dmy = self.boot_process_one_section("load_aes_iv", 0)
            if ret.startswith("OK") is False:
                return ret, bootinfo
        # process seg header and seg data
        segs = 0
        while segs < self._segcnt:
            send_len = 0
            segdata_len = 0
            ret, data_read = self.boot_process_one_section("load_seg_header", 0)
            if ret.startswith("OK") is False:
                return ret, bootinfo
            # bootrom will return decrypted seg header info
            val = bflb_utils.bytearray_reverse(data_read[4:8])
            segdata_len = bflb_utils.bytearray_to_int(val)
            bflb_utils.printf("The segdata_len is ", segdata_len)
            # for encrypted image, the segdata in segheader is the actual len of segdata
            # while the image is 16bytes aligned , so ,we the data we read for sending is also 16 bytes aligned
            if encrypt:
                if segdata_len % encrypt_blk_size != 0:
                    segdata_len = segdata_len + encrypt_blk_size - segdata_len % encrypt_blk_size
            while send_len < segdata_len:
                left = segdata_len - send_len
                if left > 4080:
                    left = 4080
                ret, dmy = self.boot_process_one_section("load_seg_data", left)
                if ret.startswith("OK") is False:
                    return ret, bootinfo
                send_len = send_len + left
                bflb_utils.printf(send_len, "/", segdata_len)
                if self._callback is not None:
                    self._callback(send_len, segdata_len, sys._getframe().f_code.co_name)
            segs = segs + 1
        ret, dmy = self.boot_process_one_section("check_image", 0)
        return ret, bootinfo

    def img_loader_reset_cpu(self):
        bflb_utils.printf("========= reset cpu =========")
        ret, data_read = self.boot_process_one_section("reset", 0)
        if ret.startswith("OK") is False:
            bflb_utils.printf("Reset cpu failed")
            return False
        return True

    def img_load_process(
        self,
        sh_baudrate,
        wk_baudrate,
        callback=None,
        do_reset=False,
        reset_hold_time=100,
        shake_hand_delay=100,
        reset_revert=True,
        cutoff_time=0,
        shake_hand_retry=2,
        isp_mode_sign=False,
        isp_timeout=0,
        boot_load=True,
        record_bootinfo=None,
        **kwargs,
    ):
        bflb_utils.printf("========= image load =========")
        success = True
        bootinfo = None
        """if temp_record_bootinfo==-1:
            record_bootinfo = self._record_bootinfo
        else:
            record_bootinfo = temp_record_bootinfo"""
        try:
            ret = self.img_load_handshake(
                sh_baudrate,
                wk_baudrate,
                do_reset,
                reset_hold_time,
                shake_hand_delay,
                reset_revert,
                cutoff_time,
                shake_hand_retry,
                isp_mode_sign,
                isp_timeout,
                boot_load,
            )
            if ret == "shake hand fail" or ret == "change rate fail":
                bflb_utils.printf("Handshake failed")
                self.bflb_serial_object.close()
                return False, bootinfo, ret
            time.sleep(0.01)
            if self._eflash_loader_file1 is not None and self._eflash_loader_file1 != "":
                res, bootinfo = self.img_load_main_process(self._eflash_loader_file1, 0, record_bootinfo, **kwargs)
                if res.startswith("OK") is False:
                    if res.startswith("repeat_burn") is True:
                        return False, bootinfo, res
                    else:
                        bflb_utils.printf("Load img failed")
                        if res.startswith("error_shakehand") is True:
                            bflb_utils.printf("Handshake with eflash loader found")
                        return False, bootinfo, res
            if self._eflash_loader_file2 is not None and self._eflash_loader_file2 != "":
                res, bootinfo = self.img_load_main_process(self._eflash_loader_file2, 1, record_bootinfo, **kwargs)
                if res.startswith("OK") is False:
                    if res.startswith("repeat_burn") is True:
                        return False, bootinfo, res
                    else:
                        bflb_utils.printf("Load img failed")
                        if res.startswith("error_shakehand") is True:
                            bflb_utils.printf("Handshake with eflash loader found")
                        return False, bootinfo, res
            bflb_utils.printf("Run img")
            self._imge_fp.close()
            res, dmy = self.boot_process_one_section("run_image", 0)
            if res.startswith("OK") is False:
                bflb_utils.printf("Run img failed")
                success = False
            else:
                bflb_utils.printf("Run img succeeded")
        except Exception as error:
            bflb_utils.printf(error)
            traceback.print_exc(limit=5, file=sys.stdout)
            return False, bootinfo, ""
        # self.bflb_serial_object.if_close()
        return success, bootinfo, ""

    @staticmethod
    def get_sync_bytes(length):
        try:
            data = bytearray(length)
            i = 0
            while i < length:
                data[i] = 0x55
                i += 1
            return data
        except Exception as error:
            bflb_utils.printf("Error: {}".format(error))


if __name__ == "__main__":
    img_load_t = BflbImgLoader()
    if len(sys.argv) == 3:
        img_load_t.img_load_process(sys.argv[1], 115200, 115200, sys.argv[2], "")
    elif len(sys.argv) == 4:
        img_load_t.img_load_process(sys.argv[1], 115200, 115200, sys.argv[2], sys.argv[3])
