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
import shutil
import zipfile
import traceback

from libs import bflb_utils
from libs.bflb_utils import app_path, chip_path, set_error_code, convert_path
from libs.bflb_configobj import BFConfigParser


def bootheader_update_flash_pll_crc(bootheader_data, chiptype):
    flash_cfg_start = 8
    flash_cfg_len = 4 + 84 + 4
    # magic+......+CRC32
    flash_cfg = bootheader_data[flash_cfg_start + 4 : flash_cfg_start + flash_cfg_len - 4]
    crcarray = bflb_utils.get_crc32_bytearray(flash_cfg)
    bootheader_data[flash_cfg_start + flash_cfg_len - 4 : flash_cfg_start + flash_cfg_len] = crcarray
    pll_cfg_start = flash_cfg_start + flash_cfg_len
    pll_cfg_len = 4 + 8 + 4
    if chiptype == "bl808":
        pll_cfg_len = 4 + 20 + 4
    elif chiptype == "bl628":
        pll_cfg_len = 4 + 16 + 4
    elif chiptype == "bl616":
        pll_cfg_len = 4 + 12 + 4
    # magic+......+CRC32
    pll_cfg = bootheader_data[pll_cfg_start + 4 : pll_cfg_start + pll_cfg_len - 4]
    crcarray = bflb_utils.get_crc32_bytearray(pll_cfg)
    bootheader_data[pll_cfg_start + pll_cfg_len - 4 : pll_cfg_start + pll_cfg_len] = crcarray
    return bootheader_data


def get_int_mask(pos, length):
    ones = "1" * 32
    zeros = "0" * 32
    mask = ones[0 : 32 - pos - length] + zeros[0:length] + ones[0:pos]
    return int(mask, 2)


def update_data_from_cfg(config_keys, config_file, section):
    bflb_utils.printf("Updating data according to <" + config_file + "[" + section + "]>")
    cfg = BFConfigParser()
    cfg.read(config_file)
    # get finally data len
    filelen = 0
    for key in config_keys:
        offset = int(config_keys.get(key)["offset"], 10)
        if offset > filelen:
            filelen = offset
    filelen += 4
    bflb_utils.printf("Created file len:" + str(filelen))
    data = bytearray(filelen)
    data_mask = bytearray(filelen)
    # bflb_utils.printf(binascii.hexlify(data))
    for key in cfg.options(section):
        if config_keys.get(key) is None:
            bflb_utils.printf("{} does not exist".format(key))
            continue
        # bflb_utils.printf(key)
        val = cfg.get(section, key)
        if val.startswith("0x"):
            val = int(val, 16)
        else:
            val = int(val, 10)
        # bflb_utils.printf(val)
        offset = int(config_keys.get(key)["offset"], 10)
        pos = int(config_keys.get(key)["pos"], 10)
        bitlen = int(config_keys.get(key)["bitlen"], 10)

        oldval = bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(data[offset : offset + 4]))
        oldval_mask = bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(data_mask[offset : offset + 4]))
        newval = (oldval & get_int_mask(pos, bitlen)) + (val << pos)
        if val != 0:
            newval_mask = oldval_mask | (~get_int_mask(pos, bitlen))
        else:
            newval_mask = oldval_mask
        # bflb_utils.printf(newval,binascii.hexlify(bflb_utils.int_to_4bytearray_l(newval)))
        data[offset : offset + 4] = bflb_utils.int_to_4bytearray_l(newval)
        data_mask[offset : offset + 4] = bflb_utils.int_to_4bytearray_l(newval_mask)
    # bflb_utils.printf(binascii.hexlify(data))
    return data, data_mask


def bootheader_create_do(chipname, chiptype, config_file, section, output_file=None, if_img=False):
    efuse_bootheader_path = os.path.join(chip_path, chipname, "efuse_bootheader")
    try:
        bflb_utils.printf("Create bootheader using ", config_file)
        sub_module = __import__("libs." + chiptype, fromlist=[chiptype])
        bh_data, _ = update_data_from_cfg(sub_module.bootheader_cfg_keys.bootheader_cfg_keys, config_file, section)
        bh_data = bootheader_update_flash_pll_crc(bh_data, chiptype)
        if output_file is None:
            fp = open(
                efuse_bootheader_path + "/" + section.lower().replace("_cfg", ".bin"),
                "wb+",
            )
        else:
            fp = open(output_file, "wb+")
        if section == "BOOTHEADER_CFG" and chiptype == "bl60x":
            final_data = bytearray(8 * 1024)
            # add sp core feature
            # halt
            bh_data[118] = bh_data[118] | (1 << 2)
            final_data[0:176] = bh_data
            final_data[4096 + 0 : 4096 + 176] = bh_data
            # change magic
            final_data[4096 + 2] = 65
            # change waydis to 0xf
            final_data[117] = final_data[117] | (15 << 4)
            # change crc and hash ignore
            final_data[4096 + 118] = final_data[4096 + 118] | 0x03
            bh_data = final_data
        if if_img is True:
            # clear flash magic
            bh_data[8:12] = bytearray(4)
            # clear clock magic
            bh_data[100:104] = bytearray(4)
            if chiptype == "bl808":
                fp.write(bh_data[0:384])
            elif chiptype == "bl628":
                fp.write(bh_data[0:256])
            elif chiptype == "bl616":
                fp.write(bh_data[0:256])
            elif chiptype == "bl702l":
                fp.write(bh_data[0:240])
            else:
                fp.write(bh_data[0:176])
        else:
            fp.write(bh_data)
        fp.close()

        if chiptype == "bl808":
            if section == "BOOTHEADER_GROUP0_CFG":
                with open(efuse_bootheader_path + "/clock_para.bin", "wb+") as fp:
                    fp.write(bh_data[100 : 100 + 28])
                with open(efuse_bootheader_path + "/flash_para.bin", "wb+") as fp:
                    fp.write(bh_data[12 : 12 + 84])
        elif chiptype == "bl628":
            if section == "BOOTHEADER_GROUP0_CFG":
                with open(efuse_bootheader_path + "/clock_para.bin", "wb+") as fp:
                    fp.write(bh_data[100 : 100 + 24])
                with open(efuse_bootheader_path + "/flash_para.bin", "wb+") as fp:
                    fp.write(bh_data[12 : 12 + 84])
        elif chiptype == "bl616":
            if section == "BOOTHEADER_GROUP0_CFG":
                with open(efuse_bootheader_path + "/clock_para.bin", "wb+") as fp:
                    fp.write(bh_data[100 : 100 + 20])
                with open(efuse_bootheader_path + "/flash_para.bin", "wb+") as fp:
                    fp.write(bh_data[12 : 12 + 84])
        elif chiptype == "bl702l":
            if section == "BOOTHEADER_CFG":
                with open(efuse_bootheader_path + "/clock_para.bin", "wb+") as fp:
                    fp.write(bh_data[100 : 100 + 16])
                with open(efuse_bootheader_path + "/flash_para.bin", "wb+") as fp:
                    fp.write(bh_data[12 : 12 + 84])
        else:
            with open(efuse_bootheader_path + "/flash_para.bin", "wb+") as fp:
                fp.write(bh_data[12 : 12 + 84])
    except Exception as error:
        bflb_utils.printf("bootheader_create_do fail!!")
        bflb_utils.printf(error)
        traceback.print_exc(limit=5, file=sys.stdout)


def bootheader_create_process(chipname, chiptype, config_file, output_file1=None, output_file2=None, if_img=False):
    with open(config_file, "r") as fp:
        data = fp.read()
    if "BOOTHEADER_CFG" in data:
        bootheader_create_do(chipname, chiptype, config_file, "BOOTHEADER_CFG", output_file1, if_img)
    if "BOOTHEADER_CPU0_CFG" in data:
        bootheader_create_do(chipname, chiptype, config_file, "BOOTHEADER_CPU0_CFG", output_file1, if_img)
    if "BOOTHEADER_CPU1_CFG" in data:
        bootheader_create_do(chipname, chiptype, config_file, "BOOTHEADER_CPU1_CFG", output_file2, if_img)
    if "BOOTHEADER_GROUP0_CFG" in data:
        bootheader_create_do(
            chipname,
            chiptype,
            config_file,
            "BOOTHEADER_GROUP0_CFG",
            output_file1,
            if_img,
        )
    if "BOOTHEADER_GROUP1_CFG" in data:
        bootheader_create_do(
            chipname,
            chiptype,
            config_file,
            "BOOTHEADER_GROUP1_CFG",
            output_file2,
            if_img,
        )


def efuse_create_process(chipname, chiptype, config_file, output_file=None):
    efuse_bootheader_path = os.path.join(chip_path, chipname, "efuse_bootheader")
    eflash_loader_path = os.path.join(chip_path, chipname, "eflash_loader")
    filedir = ""
    bflb_utils.printf("Create efuse using ", config_file)
    cfg_file = eflash_loader_path + "/eflash_loader_cfg.ini"
    if os.path.isfile(cfg_file) is False:
        shutil.copyfile(eflash_loader_path + "/eflash_loader_cfg.conf", cfg_file)
    cfg = BFConfigParser()
    cfg.read(cfg_file)
    sub_module = __import__("libs." + chiptype, fromlist=[chiptype])
    efuse_data, mask = update_data_from_cfg(sub_module.efuse_cfg_keys.efuse_cfg_keys, config_file, "EFUSE_CFG")
    if output_file is None:
        filedir = efuse_bootheader_path + "/efusedata.bin"
    else:
        filedir = output_file
    with open(filedir, "wb+") as fp:
        fp.write(efuse_data)
    bflb_utils.update_cfg(cfg, "EFUSE_CFG", "file", convert_path(os.path.relpath(filedir, app_path)))
    if output_file is None:
        filedir = efuse_bootheader_path + "/efusedata_mask.bin"
    else:
        filedir = output_file.replace(".bin", "_mask.bin")
    with open(filedir, "wb+") as fp:
        fp.write(mask)
    bflb_utils.update_cfg(cfg, "EFUSE_CFG", "maskfile", convert_path(os.path.relpath(filedir, app_path)))
    cfg.write(cfg_file, "w+")


def take_second(elem):
    return elem[1]


def factory_mode_set(file, value):
    cfg = BFConfigParser()
    cfg.read(file)
    if cfg.has_option("EFUSE_CFG", "factory_mode"):
        cfg.set("EFUSE_CFG", "factory_mode", value)
        cfg.write(file, "w")


def check_pt_file(file, addr):
    if len(file) > 0:
        i = 0
        L = []
        while i < len(file):
            L.append([convert_path(file[i]), int(addr[i], 16)])
            i += 1
        L.sort(key=take_second)
        i = 0
        try:
            while i < len(L) - 1:
                address = L[i][1]
                address_next = L[i + 1][1]
                file_size = os.path.getsize(os.path.join(app_path, L[i][0]))
                if address_next < address + file_size:
                    bflb_utils.printf(
                        "pt check fail, %s is overlayed with %s in flash layout, please check your partition table to fix this issue"
                        % (L[i][0], L[i + 1][0])
                    )
                    return False
                i += 1
        except Exception as error:
            bflb_utils.printf(error)
            return False
    return True


def compress_dir(
    chipname,
    zippath,
    efuse_load=False,
    address=None,
    flash_file=None,
    efuse_file=None,
    efuse_mask_file=None,
):
    zip_file = os.path.join(chip_path, chipname, zippath, "whole_img.pack")
    dir_path = os.path.join(chip_path, chipname, chipname)
    cfg_file = os.path.join(chip_path, chipname, "eflash_loader/eflash_loader_cfg.ini")
    cfg = BFConfigParser()
    cfg.read(cfg_file)
    if not address:
        address = []
    if not flash_file:
        flash_file = []

    if check_pt_file(flash_file, address) is not True:
        bflb_utils.printf("PT Check Fail")
        set_error_code("0082")
        return False
    # factory_mode_set(os.path.join(chip_path, chipname, "eflash_loader/eflash_loader_cfg.ini"), "false")
    flash_file.append(os.path.join(chip_path, chipname, "eflash_loader/eflash_loader_cfg.ini"))
    temp_path = os.path.join(chip_path, chipname, "efuse_bootheader")

    for name in os.listdir(temp_path):
        temp_new_path = os.path.join(temp_path, name)
        flash_file.append(temp_new_path)
    if efuse_load:
        # flash_file.append(cfg.get("EFUSE_CFG", "file"))
        # flash_file.append(cfg.get("EFUSE_CFG", "maskfile"))
        if efuse_file:
            flash_file.append(efuse_file)
        if efuse_mask_file:
            flash_file.append(efuse_mask_file)
    if len(flash_file) > 0:
        i = 0
        try:
            while i < len(flash_file):
                file_dir = convert_path(flash_file[i])
                file_name = os.path.basename(file_dir)
                suffix = file_dir.split(".")[-1]
                if (suffix == "bin" or suffix == "dtb") and file_name not in [
                    "flash_para.bin",
                    "efusedata.bin",
                    "efusedata_mask.bin",
                ]:
                    dirname = os.path.join(chip_path, chipname, chipname, "img_create", file_name)
                else:
                    relpath = os.path.relpath(os.path.join(app_path, file_dir), chip_path)
                    dirname = os.path.join(chip_path, chipname, relpath)
                if os.path.isdir(os.path.dirname(dirname)) is False:
                    os.makedirs(os.path.dirname(dirname))
                shutil.copyfile(os.path.join(app_path, file_dir), dirname)

                i += 1
            ver_file = os.path.join(chip_path, chipname, chipname, "version.txt")
            with open(ver_file, mode="w") as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        except Exception as error:
            bflb_utils.printf(error)
            # factory_mode_set(os.path.join(chipname, "eflash_loader/eflash_loader_cfg.ini"), "false")
            return False

    try:
        z = zipfile.ZipFile(zip_file, "w")
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for file in filenames:
                # z.write(os.path.relpath(os.path.join(dirpath, file), os.path.join(app_path, chipname)))
                z.write(
                    os.path.join(dirpath, file),
                    os.path.relpath(os.path.join(dirpath, file), os.path.join(chip_path, chipname)),
                )
        z.close()
        shutil.rmtree(dir_path)
    except Exception as error:
        bflb_utils.printf(error)
        # factory_mode_set(os.path.join(chipname, "eflash_loader/eflash_loader_cfg.ini"), "false")
        return False
    # factory_mode_set(os.path.join(chipname, "eflash_loader/eflash_loader_cfg.ini"), "false")
    return True


def img_create(args, chipname="bl60x", chiptype="bl60x", img_dir=None, config_file=None, **kwargs):
    sub_module = __import__("libs." + chiptype, fromlist=[chiptype])
    img_dir_path = os.path.join(chip_path, chipname, "img_create")
    if img_dir is None:
        res = sub_module.img_create_do.img_create_do(args, img_dir_path, config_file, **kwargs)
    else:
        res = sub_module.img_create_do.img_create_do(args, img_dir, config_file, **kwargs)
    return res


def create_sp_media_image_file(config, chiptype="bl60x", cpu_type=None, security=False, **kwargs):
    sub_module = __import__("libs." + chiptype, fromlist=[chiptype])
    sub_module.img_create_do.create_sp_media_image(config, cpu_type, security, **kwargs)


def get_img_offset(chiptype="bl60x", bootheader_data=None):
    sub_module = __import__("libs." + chiptype, fromlist=[chiptype])
    return sub_module.img_create_do.img_create_get_img_offset(bootheader_data)


def encrypt_loader_bin(
    chiptype,
    file,
    sign,
    encrypt,
    encrypt_key,
    encrypt_iv,
    publickey_file,
    privatekey_file,
    **kwargs,
):
    sub_module = __import__("libs." + chiptype, fromlist=[chiptype])
    return sub_module.img_create_do.encrypt_loader_bin_do(
        file, sign, encrypt, encrypt_key, encrypt_iv, publickey_file, privatekey_file, **kwargs
    )


def run():
    parser_image = bflb_utils.image_create_parser_init()
    args = parser_image.parse_args()
    # args = parser_image.parse_args("--image=media", "--signer=none")
    bflb_utils.printf("Chipname: %s" % args.chipname)
    if args.chipname:
        chip_dict = {
            "bl56x": "bl60x",
            "bl60x": "bl60x",
            "bl562": "bl602",
            "bl602": "bl602",
            "bl702": "bl702",
            "bl702l": "bl702l",
            "bl808": "bl808",
            "bl606p": "bl808",
            "bl616": "bl616",
        }
        chipname = args.chipname
        chiptype = chip_dict[chipname]
        img_create_path = os.path.join(chip_path, chipname, "img_create_mcu")
        img_create_cfg = os.path.join(chip_path, chipname, "img_create_mcu") + "/img_create_cfg.ini"
        bh_cfg_file = img_create_path + "/efuse_bootheader_cfg.ini"
        bh_file = img_create_path + "/bootheader.bin"
        if args.imgfile:
            imgbin = args.imgfile
            cfg = BFConfigParser()
            cfg.read(img_create_cfg)
            cfg.set("Img_Cfg", "segdata_file", imgbin)
            cfg.write(img_create_cfg, "w")
        bootheader_create_process(
            chipname,
            chiptype,
            bh_cfg_file,
            bh_file,
            img_create_path + "/bootheader_dummy.bin",
        )
        img_create(args, chipname, chiptype, img_create_path, img_create_cfg)
    else:
        bflb_utils.printf("Please set chipname config, exit")


if __name__ == "__main__":
    run()
