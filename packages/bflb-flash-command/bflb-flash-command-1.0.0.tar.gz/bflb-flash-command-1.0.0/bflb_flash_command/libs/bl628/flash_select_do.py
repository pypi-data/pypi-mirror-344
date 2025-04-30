# -*- coding: utf-8 -*-

import os
import csv
from re import I

from libs import bflb_utils
from libs.bflb_utils import app_path, conf_sign, cgc
from libs.bflb_configobj import BFConfigParser
from libs.bl628.bootheader_cfg_keys import bootheader_cfg_keys as flash_cfg_keys


def get_int_mask(pos, length):
    ones = "1" * 32
    zeros = "0" * 32
    mask = ones[0 : 32 - pos - length] + zeros[0:length] + ones[0:pos]
    return int(mask, 2)


def create_flashcfg_data_from_cfg(cfg_len, cfgfile):
    section = "FLASH_CFG"
    cfg = BFConfigParser()
    cfg.read(cfgfile)
    data = bytearray(cfg_len)
    min_offset = int(flash_cfg_keys.get("io_mode")["offset"], 10)

    for key in cfg.options(section):
        if flash_cfg_keys.get(key) is None:
            bflb_utils.printf("{} does not exist".format(key))
            continue
        # bflb_utils.printf(key)
        val = cfg.get(section, key)
        if val.startswith("0x"):
            val = int(val, 16)
        else:
            val = int(val, 10)
        # bflb_utils.printf(val)
        offset = int(flash_cfg_keys.get(key)["offset"], 10) - min_offset
        pos = int(flash_cfg_keys.get(key)["pos"], 10)
        bitlen = int(flash_cfg_keys.get(key)["bitlen"], 10)

        oldval = bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(data[offset : offset + 4]))
        newval = (oldval & get_int_mask(pos, bitlen)) + (val << pos)
        # bflb_utils.printf(newval,binascii.hexlify(bflb_utils.int_to_4bytearray_l(newval)))
        data[offset : offset + 4] = bflb_utils.int_to_4bytearray_l(newval)
    crcarray = bflb_utils.get_crc32_bytearray(data)
    data = bflb_utils.int_to_4bytearray_l(0x47464346) + data + crcarray
    return data


def create_flashcfg_table(start_addr):
    single_flashcfg_len = 4 + 84 + 4
    flash_table_list = bytearray(0)
    flash_table_data = bytearray(0)
    if conf_sign:
        table_file = os.path.join(app_path, "utils", "flash", "tg6210a", "flashcfg_list.csv")
    else:
        table_file = os.path.join(app_path, "utils", "flash", "bl628", "flashcfg_list.csv")
    with open(table_file, "r", encoding="utf-8-sig") as csvfile:
        table_list = []
        cfgfile_list = []
        reader = csv.DictReader(csvfile)
        cnt = 0
        for row in reader:
            row_dict = {}
            row_dict["jid"] = row.get("flashJedecID", "")
            row_dict["cfgfile"] = row.get("configFile", "")
            if row_dict["cfgfile"] not in cfgfile_list:
                cfgfile_list.append(row_dict["cfgfile"])
            table_list.append(row_dict)
            cnt += 1
        table_list_len = 4 + cnt * 8 + 4
        for cfgfile in cfgfile_list:
            if conf_sign:
                cfgfile = os.path.join(app_path, "utils", "flash", "tg6210a", cfgfile)
            else:
                cfgfile = os.path.join(app_path, "utils", "flash", "bl628", cfgfile)
            data = create_flashcfg_data_from_cfg(single_flashcfg_len - 8, cfgfile)
            flash_table_data += data
        for dict in table_list:
            flash_table_list += bflb_utils.int_to_4bytearray_b(int(dict["jid"] + "00", 16))
            i = 0
            offset = 0
            for cfgfile in cfgfile_list:
                if cfgfile == dict["cfgfile"]:
                    offset = start_addr + table_list_len + single_flashcfg_len * i
                    break
                i += 1
            flash_table_list += bflb_utils.int_to_4bytearray_l(offset)
    crcarray = bflb_utils.get_crc32_bytearray(flash_table_list)
    flash_table_list = bflb_utils.int_to_4bytearray_l(0x47544346) + flash_table_list + crcarray

    return flash_table_list, flash_table_data, len(flash_table_list)
