# -*- coding:utf-8 -*-

import os
import sys
import hashlib
import binascii
import codecs

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature

from libs import bflb_utils
from libs.bflb_utils import img_create_sha256_data, img_create_encrypt_data
from libs.bflb_configobj import BFConfigParser
from libs.bl808.flash_select_do import create_flashcfg_table
from libs.bl808.bootheader_cfg_keys import (
    flashcfg_table_start_pos as flashcfg_table_start,
)
from libs.bl808.bootheader_cfg_keys import bootcpucfg_start_pos as bootcpucfg_start
from libs.bl808.bootheader_cfg_keys import bootcpucfg_len as bootcpucfg_length
from libs.bl808.bootheader_cfg_keys import (
    bootcpucfg_m0_index as bootcpucfg_m0_index_number,
)
from libs.bl808.bootheader_cfg_keys import (
    bootcpucfg_d0_index as bootcpucfg_d0_index_number,
)
from libs.bl808.bootheader_cfg_keys import (
    bootcpucfg_lp_index as bootcpucfg_lp_index_number,
)
from libs.bl808.bootheader_cfg_keys import bootcfg_start_pos as bootcfg_start
from libs.bl808.bootheader_cfg_keys import bootheader_len as header_len

keyslot0 = 28
keyslot1 = keyslot0 + 16
keyslot2 = keyslot1 + 16
keyslot3 = keyslot2 + 16
keyslot3_end = keyslot3 + 16
keyslot4 = 128
keyslot5 = keyslot4 + 16
keyslot6 = keyslot5 + 16
keyslot7 = keyslot6 + 16
keyslot8 = keyslot7 + 16
keyslot9 = keyslot8 + 16
keyslot10 = keyslot9 + 16
keyslot10_end = keyslot10 + 16
keyslot11 = keyslot3_end + 16
keyslot11_end = keyslot11 + 16

wr_lock_boot_mode = 14
wr_lock_dbg_pwd = 15
wr_lock_wifi_mac = 16
wr_lock_key_slot_0 = 17
wr_lock_key_slot_1 = 18
wr_lock_key_slot_2 = 19
wr_lock_key_slot_3 = 20
wr_lock_sw_usage_0 = 21
wr_lock_sw_usage_1 = 22
wr_lock_sw_usage_2 = 23
wr_lock_sw_usage_3 = 24
wr_lock_key_slot_11 = 25
rd_lock_dbg_pwd = 26
rd_lock_key_slot_0 = 27
rd_lock_key_slot_1 = 28
rd_lock_key_slot_2 = 29
rd_lock_key_slot_3 = 30
rd_lock_key_slot_11 = 31

wr_lock_key_slot_4 = 15
wr_lock_key_slot_5 = 16
wr_lock_key_slot_6 = 17
wr_lock_key_slot_7 = 18
wr_lock_key_slot_8 = 19
wr_lock_key_slot_9 = 20
wr_lock_key_slot_10 = 21
rd_lock_key_slot_4 = 25
rd_lock_key_slot_5 = 26
rd_lock_key_slot_6 = 27
rd_lock_key_slot_7 = 28
rd_lock_key_slot_8 = 29
rd_lock_key_slot_9 = 30
rd_lock_key_slot_10 = 31


def bytearray_data_merge(data1, data2, len):
    for i in range(len):
        data1[i] |= data2[i]
    return data1


# update efuse info
def img_update_efuse_group0(
    cfg,
    sign,
    pk_hash,
    flash_encryp_type,
    flash_key,
    sec_eng_key_sel,
    sec_eng_key,
    security=False,
):
    with open(cfg.get("Img_Group0_Cfg", "efuse_file"), "rb") as fp:
        efuse_data = bytearray(fp.read()) + bytearray(0)
    with open(cfg.get("Img_Group0_Cfg", "efuse_mask_file"), "rb") as fp:
        efuse_mask_data = bytearray(fp.read()) + bytearray(0)

    mask_4bytes = bytearray.fromhex("FFFFFFFF")

    # Set ef_sf_aes_mode
    if flash_encryp_type >= 3:
        efuse_data[0] |= 3
    else:
        efuse_data[0] |= flash_encryp_type
    # Set ef_sw_usage_0 --> sign_cfg
    if sign > 0:
        efuse_data[93] |= sign
        efuse_mask_data[93] |= 0xFF
    # Set ef_sboot_en
    if flash_encryp_type > 0:
        efuse_data[0] |= 0x30
    efuse_mask_data[0] |= 0xFF
    rw_lock0 = 0
    rw_lock1 = 0
    if pk_hash is not None:
        efuse_data[keyslot0:keyslot2] = pk_hash
        efuse_mask_data[keyslot0:keyslot2] = mask_4bytes * 8
        rw_lock0 |= 1 << wr_lock_key_slot_0
        rw_lock0 |= 1 << wr_lock_key_slot_1
    if flash_key is not None:
        if flash_encryp_type == 1:
            # aes 128
            efuse_data[keyslot2:keyslot3] = flash_key[0:16]
            efuse_mask_data[keyslot2:keyslot3] = mask_4bytes * 4
        elif flash_encryp_type == 2:
            # aes 192
            efuse_data[keyslot2:keyslot3_end] = flash_key
            efuse_mask_data[keyslot2:keyslot3_end] = mask_4bytes * 8
            rw_lock0 |= 1 << wr_lock_key_slot_3
            rw_lock0 |= 1 << rd_lock_key_slot_3
        elif flash_encryp_type == 3:
            # aes 256
            efuse_data[keyslot2:keyslot3_end] = flash_key
            efuse_mask_data[keyslot2:keyslot3_end] = mask_4bytes * 8
            rw_lock0 |= 1 << wr_lock_key_slot_3
            rw_lock0 |= 1 << rd_lock_key_slot_3
        elif flash_encryp_type == 4 or flash_encryp_type == 5 or flash_encryp_type == 6:
            # aes xts 128/192/256
            efuse_data[keyslot2:keyslot3_end] = flash_key
            efuse_mask_data[keyslot2:keyslot3_end] = mask_4bytes * 8
            rw_lock0 |= 1 << wr_lock_key_slot_3
            rw_lock0 |= 1 << rd_lock_key_slot_3

        rw_lock0 |= 1 << wr_lock_key_slot_2
        rw_lock0 |= 1 << rd_lock_key_slot_2

    if sec_eng_key is not None:
        if flash_encryp_type == 0:
            if sec_eng_key_sel == 0:
                efuse_data[keyslot2:keyslot3] = sec_eng_key[16:32]
                efuse_data[keyslot3:keyslot3_end] = sec_eng_key[0:16]
                efuse_mask_data[keyslot2:keyslot3_end] = mask_4bytes * 8
                rw_lock0 |= 1 << wr_lock_key_slot_2
                rw_lock0 |= 1 << wr_lock_key_slot_3
                rw_lock0 |= 1 << rd_lock_key_slot_2
                rw_lock0 |= 1 << rd_lock_key_slot_3
            if sec_eng_key_sel == 1:
                efuse_data[keyslot3:keyslot3_end] = sec_eng_key[16:32]
                efuse_data[keyslot4:keyslot5] = sec_eng_key[0:16]
                efuse_mask_data[keyslot3:keyslot3_end] = mask_4bytes * 4
                efuse_mask_data[keyslot4:keyslot5] = mask_4bytes * 4
                rw_lock0 |= 1 << wr_lock_key_slot_3
                rw_lock1 |= 1 << wr_lock_key_slot_4
                rw_lock0 |= 1 << rd_lock_key_slot_3
                rw_lock1 |= 1 << rd_lock_key_slot_4
            if sec_eng_key_sel == 2:
                efuse_data[keyslot4:keyslot5] = sec_eng_key[16:32]
                efuse_data[keyslot2:keyslot3] = sec_eng_key[0:16]
                efuse_mask_data[keyslot3:keyslot5] = mask_4bytes * 8
                rw_lock1 |= 1 << wr_lock_key_slot_4
                rw_lock0 |= 1 << wr_lock_key_slot_2
                rw_lock1 |= 1 << rd_lock_key_slot_4
                rw_lock0 |= 1 << rd_lock_key_slot_2
            if sec_eng_key_sel == 3:
                efuse_data[keyslot4:keyslot5] = sec_eng_key[16:32]
                efuse_data[keyslot2:keyslot3] = sec_eng_key[0:16]
                efuse_mask_data[keyslot3:keyslot5] = mask_4bytes * 8
                rw_lock1 |= 1 << wr_lock_key_slot_4
                rw_lock0 |= 1 << wr_lock_key_slot_2
                rw_lock1 |= 1 << rd_lock_key_slot_4
                rw_lock0 |= 1 << rd_lock_key_slot_2
        if flash_encryp_type == 1:
            if sec_eng_key_sel == 0:
                efuse_data[keyslot5:keyslot6] = sec_eng_key[0:16]
                efuse_mask_data[keyslot5:keyslot6] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_5
                rw_lock1 |= 1 << rd_lock_key_slot_5
            if sec_eng_key_sel == 1:
                efuse_data[keyslot4:keyslot5] = sec_eng_key[0:16]
                efuse_mask_data[keyslot4:keyslot5] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_4
                rw_lock1 |= 1 << rd_lock_key_slot_4
            if sec_eng_key_sel == 2:
                if flash_key is not None:
                    # Sec eng use xip key
                    pass
                else:
                    efuse_data[keyslot3:keyslot3_end] = sec_eng_key[0:16]
                    efuse_mask_data[keyslot3:keyslot3_end] = mask_4bytes * 4
                    rw_lock0 |= 1 << wr_lock_key_slot_3
                    rw_lock0 |= 1 << rd_lock_key_slot_3
            if sec_eng_key_sel == 3:
                if flash_key is not None:
                    # Sec eng use xip key
                    pass
                else:
                    efuse_data[keyslot2:keyslot3] = sec_eng_key[0:16]
                    efuse_mask_data[keyslot2:keyslot3] = mask_4bytes * 4
                    rw_lock0 |= 1 << wr_lock_key_slot_2
                    rw_lock0 |= 1 << rd_lock_key_slot_2
        if (
            flash_encryp_type == 2
            or flash_encryp_type == 3
            or flash_encryp_type == 4
            or flash_encryp_type == 5
            or flash_encryp_type == 6
        ):
            if sec_eng_key_sel == 0:
                efuse_data[keyslot6:keyslot7] = sec_eng_key[16:32]
                efuse_data[keyslot10:keyslot10_end] = sec_eng_key[0:16]
                efuse_mask_data[keyslot6:keyslot7] = mask_4bytes * 4
                efuse_mask_data[keyslot10:keyslot10_end] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_6
                rw_lock1 |= 1 << wr_lock_key_slot_10
                rw_lock1 |= 1 << rd_lock_key_slot_6
                rw_lock1 |= 1 << rd_lock_key_slot_10
            if sec_eng_key_sel == 1:
                efuse_data[keyslot10:keyslot10_end] = sec_eng_key[16:32]
                efuse_data[keyslot6:keyslot7] = sec_eng_key[0:16]
                efuse_mask_data[keyslot6:keyslot7] = mask_4bytes * 4
                efuse_mask_data[keyslot10:keyslot10_end] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_6
                rw_lock1 |= 1 << wr_lock_key_slot_10
                rw_lock1 |= 1 << rd_lock_key_slot_6
                rw_lock1 |= 1 << rd_lock_key_slot_10
            if sec_eng_key_sel == 2:
                if flash_key is not None:
                    # Sec eng use xip key
                    pass
                else:
                    efuse_data[keyslot2:keyslot3] = sec_eng_key[16:32]
                    efuse_data[keyslot3:keyslot3_end] = sec_eng_key[0:16]
                    efuse_mask_data[keyslot2:keyslot3_end] = mask_4bytes * 8
                    rw_lock0 |= 1 << wr_lock_key_slot_2
                    rw_lock0 |= 1 << rd_lock_key_slot_2
                    rw_lock0 |= 1 << wr_lock_key_slot_3
                    rw_lock0 |= 1 << rd_lock_key_slot_3
            if sec_eng_key_sel == 3:
                if flash_key is not None:
                    # Sec eng use xip key
                    pass
                else:
                    efuse_data[keyslot2:keyslot3_end] = sec_eng_key
                    efuse_mask_data[keyslot2:keyslot3_end] = mask_4bytes * 8
                    rw_lock0 |= 1 << wr_lock_key_slot_2
                    rw_lock0 |= 1 << rd_lock_key_slot_2
                    rw_lock0 |= 1 << wr_lock_key_slot_3
                    rw_lock0 |= 1 << rd_lock_key_slot_3
    # set read write lock key
    efuse_data[124:128] = bytearray_data_merge(efuse_data[124:128], bflb_utils.int_to_4bytearray_l(rw_lock0), 4)
    efuse_mask_data[124:128] = bytearray_data_merge(
        efuse_mask_data[124:128], bflb_utils.int_to_4bytearray_l(rw_lock0), 4
    )
    efuse_data[252:256] = bytearray_data_merge(efuse_data[252:256], bflb_utils.int_to_4bytearray_l(rw_lock1), 4)
    efuse_mask_data[252:256] = bytearray_data_merge(
        efuse_mask_data[252:256], bflb_utils.int_to_4bytearray_l(rw_lock1), 4
    )

    if security is True:
        bflb_utils.printf("Encrypt efuse data")
        security_key, security_iv = bflb_utils.get_security_key()
        efuse_data = img_create_encrypt_data(efuse_data, security_key, security_iv, 0)
        efuse_data = bytearray(4096) + efuse_data
    with open(cfg.get("Img_Group0_Cfg", "efuse_file"), "wb+") as fp:
        fp.write(efuse_data)
    with open(cfg.get("Img_Group0_Cfg", "efuse_mask_file"), "wb+") as fp:
        fp.write(efuse_mask_data)


def img_update_efuse_group1(
    cfg,
    sign,
    pk_hash,
    flash_encryp_type,
    flash_key,
    sec_eng_key_sel,
    sec_eng_key,
    security=False,
):
    with open(cfg.get("Img_Group1_Cfg", "efuse_file"), "rb") as fp:
        efuse_data = bytearray(fp.read()) + bytearray(0)
    with open(cfg.get("Img_Group1_Cfg", "efuse_mask_file"), "rb") as fp:
        efuse_mask_data = bytearray(fp.read()) + bytearray(0)

    mask_4bytes = bytearray.fromhex("FFFFFFFF")

    # Set ef_sf_aes_mode
    if flash_encryp_type >= 3:
        efuse_data[0] |= 3
    else:
        efuse_data[0] |= flash_encryp_type
    # Set ef_sw_usage_0 --> sign_cfg
    if sign > 0:
        efuse_data[93] |= sign
        efuse_mask_data[93] |= 0xFF
    # Set ef_sboot_en
    if flash_encryp_type > 0:
        efuse_data[0] |= 0x30
    efuse_mask_data[0] |= 0xFF
    rw_lock0 = 0
    rw_lock1 = 0
    if pk_hash is not None:
        efuse_data[keyslot8:keyslot10] = pk_hash
        efuse_mask_data[keyslot8:keyslot10] = mask_4bytes * 8
        rw_lock1 |= 1 << wr_lock_key_slot_8
        rw_lock1 |= 1 << wr_lock_key_slot_9
    if flash_key is not None:
        if flash_encryp_type == 1:
            # aes 128
            efuse_data[keyslot3:keyslot3_end] = flash_key[0:16]
            efuse_mask_data[keyslot3:keyslot3_end] = mask_4bytes * 4
            rw_lock0 |= 1 << wr_lock_key_slot_3
            rw_lock0 |= 1 << rd_lock_key_slot_3
        elif flash_encryp_type == 2:
            # aes 192
            efuse_data[keyslot4:keyslot6] = flash_key
            efuse_mask_data[keyslot4:keyslot6] = mask_4bytes * 8
            rw_lock1 |= 1 << wr_lock_key_slot_4
            rw_lock1 |= 1 << wr_lock_key_slot_5
            rw_lock1 |= 1 << rd_lock_key_slot_4
            rw_lock1 |= 1 << rd_lock_key_slot_5
        elif flash_encryp_type == 3:
            # aes 256
            efuse_data[keyslot4:keyslot6] = flash_key
            efuse_mask_data[keyslot4:keyslot6] = mask_4bytes * 8
            rw_lock1 |= 1 << wr_lock_key_slot_4
            rw_lock1 |= 1 << wr_lock_key_slot_5
            rw_lock1 |= 1 << rd_lock_key_slot_4
            rw_lock1 |= 1 << rd_lock_key_slot_5
        elif flash_encryp_type == 4 or flash_encryp_type == 5 or flash_encryp_type == 6:
            # aes xts 128/192/256
            efuse_data[keyslot4:keyslot6] = flash_key
            efuse_mask_data[keyslot4:keyslot6] = mask_4bytes * 8
            rw_lock1 |= 1 << wr_lock_key_slot_4
            rw_lock1 |= 1 << wr_lock_key_slot_5
            rw_lock1 |= 1 << rd_lock_key_slot_4
            rw_lock1 |= 1 << rd_lock_key_slot_5

    if sec_eng_key is not None:
        if flash_encryp_type == 0:
            if sec_eng_key_sel == 0:
                efuse_data[keyslot5:keyslot6] = sec_eng_key[16:32]
                efuse_data[keyslot6:keyslot7] = sec_eng_key[0:16]
                efuse_mask_data[keyslot5:keyslot7] = mask_4bytes * 8
                rw_lock1 |= 1 << wr_lock_key_slot_5
                rw_lock1 |= 1 << wr_lock_key_slot_6
                rw_lock1 |= 1 << rd_lock_key_slot_5
                rw_lock1 |= 1 << rd_lock_key_slot_6
            if sec_eng_key_sel == 1:
                efuse_data[keyslot6:keyslot7] = sec_eng_key[16:32]
                efuse_data[keyslot7:keyslot8] = sec_eng_key[0:16]
                efuse_mask_data[keyslot6:keyslot8] = mask_4bytes * 8
                rw_lock1 |= 1 << wr_lock_key_slot_6
                rw_lock1 |= 1 << wr_lock_key_slot_7
                rw_lock1 |= 1 << rd_lock_key_slot_6
                rw_lock1 |= 1 << rd_lock_key_slot_7
            if sec_eng_key_sel == 2:
                efuse_data[keyslot7:keyslot8] = sec_eng_key[16:32]
                efuse_data[keyslot5:keyslot6] = sec_eng_key[0:16]
                efuse_mask_data[keyslot7:keyslot8] = mask_4bytes * 4
                efuse_mask_data[keyslot5:keyslot6] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_7
                rw_lock1 |= 1 << wr_lock_key_slot_5
                rw_lock1 |= 1 << rd_lock_key_slot_7
                rw_lock1 |= 1 << rd_lock_key_slot_5
            if sec_eng_key_sel == 3:
                efuse_data[keyslot7:keyslot8] = sec_eng_key[16:32]
                efuse_data[keyslot5:keyslot6] = sec_eng_key[0:16]
                efuse_mask_data[keyslot7:keyslot8] = mask_4bytes * 4
                efuse_mask_data[keyslot5:keyslot6] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_7
                rw_lock1 |= 1 << wr_lock_key_slot_5
                rw_lock1 |= 1 << rd_lock_key_slot_7
                rw_lock1 |= 1 << rd_lock_key_slot_5
        if flash_encryp_type == 1:
            if sec_eng_key_sel == 0:
                efuse_data[keyslot7:keyslot8] = sec_eng_key[0:16]
                efuse_mask_data[keyslot7:keyslot8] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_7
                rw_lock1 |= 1 << rd_lock_key_slot_7
            if sec_eng_key_sel == 1:
                efuse_data[keyslot6:keyslot7] = sec_eng_key[0:16]
                efuse_mask_data[keyslot6:keyslot7] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_6
                rw_lock1 |= 1 << rd_lock_key_slot_6
            if sec_eng_key_sel == 2:
                if flash_key is not None:
                    # Sec eng use xip key
                    pass
                else:
                    efuse_data[keyslot3:keyslot3_end] = sec_eng_key[0:16]
                    efuse_mask_data[keyslot3:keyslot3_end] = mask_4bytes * 4
                    rw_lock0 |= 1 << wr_lock_key_slot_3
                    rw_lock0 |= 1 << rd_lock_key_slot_3
            if sec_eng_key_sel == 3:
                if flash_key is not None:
                    # Sec eng use xip key
                    pass
                else:
                    efuse_data[keyslot2:keyslot3] = sec_eng_key[0:16]
                    efuse_mask_data[keyslot2:keyslot3] = mask_4bytes * 4
                    rw_lock0 |= 1 << wr_lock_key_slot_2
                    rw_lock0 |= 1 << rd_lock_key_slot_2
        if (
            flash_encryp_type == 2
            or flash_encryp_type == 3
            or flash_encryp_type == 4
            or flash_encryp_type == 5
            or flash_encryp_type == 6
        ):
            if sec_eng_key_sel == 0:
                efuse_data[keyslot7:keyslot8] = sec_eng_key[16:32]
                efuse_data[keyslot11:keyslot11_end] = sec_eng_key[0:16]
                efuse_mask_data[keyslot7:keyslot8] = mask_4bytes * 4
                efuse_mask_data[keyslot11:keyslot11_end] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_7
                rw_lock0 |= 1 << rd_lock_key_slot_11
                rw_lock1 |= 1 << wr_lock_key_slot_7
                rw_lock0 |= 1 << rd_lock_key_slot_11
            if sec_eng_key_sel == 1:
                efuse_data[keyslot11:keyslot11_end] = sec_eng_key[16:32]
                efuse_data[keyslot7:keyslot8] = sec_eng_key[0:16]
                efuse_mask_data[keyslot7:keyslot8] = mask_4bytes * 4
                efuse_mask_data[keyslot11:keyslot11_end] = mask_4bytes * 4
                rw_lock1 |= 1 << wr_lock_key_slot_7
                rw_lock0 |= 1 << rd_lock_key_slot_11
                rw_lock1 |= 1 << wr_lock_key_slot_7
                rw_lock0 |= 1 << rd_lock_key_slot_11
            if sec_eng_key_sel == 2:
                if flash_key is not None:
                    # Sec eng use xip key
                    pass
                else:
                    efuse_data[keyslot4:keyslot5] = sec_eng_key[16:32]
                    efuse_data[keyslot5:keyslot6] = sec_eng_key[0:16]
                    efuse_mask_data[keyslot4:keyslot6] = mask_4bytes * 8
                    rw_lock1 |= 1 << wr_lock_key_slot_4
                    rw_lock1 |= 1 << wr_lock_key_slot_5
                    rw_lock1 |= 1 << rd_lock_key_slot_4
                    rw_lock1 |= 1 << rd_lock_key_slot_5
            if sec_eng_key_sel == 3:
                if flash_key is not None:
                    # Sec eng use xip key
                    pass
                else:
                    efuse_data[keyslot4:keyslot6] = sec_eng_key
                    efuse_mask_data[keyslot4:keyslot6] = mask_4bytes * 8
                    rw_lock1 |= 1 << wr_lock_key_slot_4
                    rw_lock1 |= 1 << wr_lock_key_slot_5
                    rw_lock1 |= 1 << rd_lock_key_slot_4
                    rw_lock1 |= 1 << rd_lock_key_slot_5
    # set read write lock key
    efuse_data[124:128] = bytearray_data_merge(efuse_data[124:128], bflb_utils.int_to_4bytearray_l(rw_lock0), 4)
    efuse_mask_data[124:128] = bytearray_data_merge(
        efuse_mask_data[124:128], bflb_utils.int_to_4bytearray_l(rw_lock0), 4
    )
    efuse_data[252:256] = bytearray_data_merge(efuse_data[252:256], bflb_utils.int_to_4bytearray_l(rw_lock1), 4)
    efuse_mask_data[252:256] = bytearray_data_merge(
        efuse_mask_data[252:256], bflb_utils.int_to_4bytearray_l(rw_lock1), 4
    )

    if security is True:
        bflb_utils.printf("Encrypt efuse data")
        security_key, security_iv = bflb_utils.get_security_key()
        efuse_data = img_create_encrypt_data(efuse_data, security_key, security_iv, 0)
        efuse_data = bytearray(4096) + efuse_data
    with open(cfg.get("Img_Group1_Cfg", "efuse_file"), "wb+") as fp:
        fp.write(efuse_data)
    with open(cfg.get("Img_Group1_Cfg", "efuse_mask_file"), "wb+") as fp:
        fp.write(efuse_mask_data)


# get sign and encrypt info
def img_create_get_sign_encrypt_info(bootheader_data):
    sign = bootheader_data[bootcfg_start] & 0x3
    encrypt = (bootheader_data[bootcfg_start] >> 2) & 0x3
    key_sel = (bootheader_data[bootcfg_start] >> 4) & 0x3
    xts_mode = (bootheader_data[bootcfg_start] >> 6) & 0x1
    return sign, encrypt, key_sel, xts_mode


# get img start addr
def img_create_get_img_start_addr(bootheader_data):
    bootentry = []
    bootentry.append(
        bflb_utils.bytearray_to_int(
            bflb_utils.bytearray_reverse(
                bootheader_data[
                    bootcpucfg_start
                    + bootcpucfg_length * bootcpucfg_m0_index_number
                    + 16 : bootcpucfg_start
                    + bootcpucfg_length * bootcpucfg_m0_index_number
                    + 16
                    + 4
                ]
            )
        )
    )
    bootentry.append(
        bflb_utils.bytearray_to_int(
            bflb_utils.bytearray_reverse(
                bootheader_data[
                    bootcpucfg_start
                    + bootcpucfg_length * bootcpucfg_d0_index_number
                    + 16 : bootcpucfg_start
                    + bootcpucfg_length * bootcpucfg_d0_index_number
                    + 16
                    + 4
                ]
            )
        )
    )
    bootentry.append(
        bflb_utils.bytearray_to_int(
            bflb_utils.bytearray_reverse(
                bootheader_data[
                    bootcpucfg_start
                    + bootcpucfg_length * bootcpucfg_lp_index_number
                    + 16 : bootcpucfg_start
                    + bootcpucfg_length * bootcpucfg_lp_index_number
                    + 16
                    + 4
                ]
            )
        )
    )
    return bootentry


# get whole group img data
def img_create_flash_default_data(length):
    datas = bytearray(length)
    for i in range(length):
        datas[i] = 0xFF
    return datas


def img_get_file_data(files):
    datas = []
    for file in files:
        if file == "UNUSED":
            datas.append(bytearray(0))
            continue
        with open(file, "rb") as fp:
            data = fp.read()
        datas.append(data)
    return datas


def img_get_largest_addr(addrs, files):
    min = 0x3FFFFFF
    maxlen = 0
    datalen = 0
    for i in range(len(addrs)):
        if files[i] == "UNUSED":
            continue
        addr = addrs[i] & 0x3FFFFFF
        if addr >= maxlen:
            maxlen = addr
            datalen = os.path.getsize(files[i])
        if addr <= min:
            min = addr
    if maxlen == 0 and datalen == 0:
        return 0, 0
    return maxlen + datalen - min, min


def img_get_one_group_img(d_addrs, d_files):
    # bflb_utils.printf(d_files)
    # bflb_utils.printf(d_addrs)
    whole_img_len, min = img_get_largest_addr(d_addrs, d_files)
    whole_img_len &= 0x3FFFFFF
    # bflb_utils.printf(whole_img_len)
    whole_img_data = img_create_flash_default_data(whole_img_len)
    filedatas = img_get_file_data(d_files)
    # create_whole_image_flash
    for i in range(len(d_addrs)):
        if d_files[i] == "UNUSED":
            continue
        start_addr = d_addrs[i]
        start_addr &= 0x3FFFFFF
        start_addr -= min
        whole_img_data[start_addr : start_addr + len(filedatas[i])] = filedatas[i]
    return whole_img_data


# get hash ignore ignore
def img_create_get_hash_ignore(bootheader_data):
    return (bootheader_data[bootcfg_start + 2] >> 1) & 0x1


# get crc ignore ignore
def img_create_get_crc_ignore(bootheader_data):
    return bootheader_data[bootcfg_start + 2] & 0x1


def img_create_update_bootheader_if(bootheader_data, hash, seg_cnt):
    # update segment count
    bootheader_data[bootcfg_start + 12 : bootcfg_start + 12 + 4] = bflb_utils.int_to_4bytearray_l(seg_cnt)

    # update hash
    sign = bootheader_data[bootcfg_start] & 0x3
    encrypt = (bootheader_data[bootcfg_start] >> 2) & 0x3
    key_sel = (bootheader_data[bootcfg_start] >> 4) & 0x3
    xts_mode = (bootheader_data[bootcfg_start] >> 6) & 0x1

    if ((bootheader_data[bootcfg_start + 2] >> 1) & 0x1) == 1 and sign == 0:
        # do nothing
        bflb_utils.printf("Hash ignored")
    else:
        bootheader_data[bootcfg_start + 16 : bootcfg_start + 16 + 32] = hash

    # update header crc
    if (bootheader_data[bootcfg_start + 2] & 0x1) == 1:
        # do nothing
        bflb_utils.printf("Header crc ignored")
    else:
        hd_crcarray = bflb_utils.get_crc32_bytearray(bootheader_data[0 : header_len - 4])
        bootheader_data[header_len - 4 : header_len] = hd_crcarray
        bflb_utils.printf("Header crc: ", binascii.hexlify(hd_crcarray))
    return bootheader_data


# update boot header info
def img_create_update_bootheader(bootheader_data, hash, seg_cnt, flashcfg_table_addr, flashcfg_table_len):
    # update flashcfg table value
    bootheader_data[flashcfg_table_start : flashcfg_table_start + 4] = bflb_utils.int_to_4bytearray_l(
        flashcfg_table_addr
    )
    bootheader_data[flashcfg_table_start + 4 : flashcfg_table_start + 8] = bflb_utils.int_to_4bytearray_l(
        flashcfg_table_len
    )

    # update segment count
    bootheader_data[bootcfg_start + 12 : bootcfg_start + 12 + 4] = bflb_utils.int_to_4bytearray_l(seg_cnt)

    # update hash
    sign, encrypt, key_sel, xts_mode = img_create_get_sign_encrypt_info(bootheader_data)
    if img_create_get_hash_ignore(bootheader_data) == 1 and sign == 0:
        # do nothing
        bflb_utils.printf("Hash ignored")
    else:
        bootheader_data[bootcfg_start + 16 : bootcfg_start + 16 + 32] = hash

    # update header crc
    if img_create_get_crc_ignore(bootheader_data) == 1:
        # do nothing
        bflb_utils.printf("Header crc ignored")
    else:
        hd_crcarray = bflb_utils.get_crc32_bytearray(bootheader_data[0 : header_len - 4])
        bootheader_data[header_len - 4 : header_len] = hd_crcarray
        bflb_utils.printf("Header crc: ", binascii.hexlify(hd_crcarray))

    return bootheader_data[0:header_len]


# update segment header according segdata
def img_create_update_segheader(segheader, segdatalen, segdatacrc):
    segheader[4:8] = segdatalen
    segheader[8:12] = segdatacrc
    return segheader


def reverse_str_data_unit_number(str_data_unit_number):
    """
    high position low data
    data unit number:00000280
    storage format:  80020000
    """
    reverse_str = ""
    if len(str_data_unit_number) == 8:
        str_part1 = str_data_unit_number[0:2]
        str_part2 = str_data_unit_number[2:4]
        str_part3 = str_data_unit_number[4:6]
        str_part4 = str_data_unit_number[6:8]
        reverse_str = str_part4 + str_part3 + str_part2 + str_part1
    return reverse_str


def reverse_iv(need_reverse_iv_bytearray):
    temp_reverse_iv_bytearray = binascii.hexlify(need_reverse_iv_bytearray).decode()
    if temp_reverse_iv_bytearray[24:32] != "00000000":
        bflb_utils.printf(
            "The lower 4 bytes of IV should be set 0, if set IV is less than 16 bytes, make up 0 for the low 4 bytes of IV "
        )
        sys.exit()
    reverse_iv_bytearray = "00000000" + temp_reverse_iv_bytearray[0:24]
    return reverse_iv_bytearray


# sign image(hash code)
def img_create_sign_data(data_bytearray, privatekey_file_uecc, publickey_file, flag=0):
    try:
        if flag:
            n = 64
            list_sk = [privatekey_file_uecc[i : i + n] for i in range(0, len(privatekey_file_uecc), n)]
            str_sk = "-----BEGIN EC PRIVATE KEY-----\n"
            for item in list_sk:
                str_sk = str_sk + item + "\n"
            str_sk = str_sk + "-----END EC PRIVATE KEY-----\n"
            sk = serialization.load_pem_private_key(str_sk.encode("utf-8"), password=None)
            if publickey_file:
                list_pk = [publickey_file[i : i + n] for i in range(0, len(publickey_file), n)]
                str_pk = "-----BEGIN PUBLIC KEY-----\n"
                for item in list_pk:
                    str_pk = str_pk + item + "\n"
                str_pk = str_pk + "-----END PUBLIC KEY-----\n"
                vk = serialization.load_pem_public_key(str_pk.encode("utf-8"), backend=default_backend())
            else:
                vk = sk.public_key()
        else:
            with open(privatekey_file_uecc, "rb") as fp:
                key = fp.read()
            sk = serialization.load_pem_private_key(key, password=None)
            if publickey_file:
                with open(publickey_file, "rb") as fp:
                    key = fp.read()
                vk = serialization.load_pem_public_key(key, backend=default_backend())
            else:
                vk = sk.public_key()
        public_numbers = vk.public_numbers()
        x = public_numbers.x
        y = public_numbers.y
        x_bytes = x.to_bytes(32, "big")
        y_bytes = y.to_bytes(32, "big")
        pk_data = x_bytes + y_bytes
        bflb_utils.printf("Public key: ", binascii.hexlify(pk_data))
        pk_hash = img_create_sha256_data(pk_data)
        bflb_utils.printf("Public key hash=", binascii.hexlify(pk_hash))
        signature = sk.sign(data_bytearray, ec.ECDSA(hashes.SHA256()))
        r, s = decode_dss_signature(signature)
        signature = r.to_bytes(32, "big") + s.to_bytes(32, "big")
        bflb_utils.printf("Signature=", binascii.hexlify(signature))
        # return len+signature+crc
        len_array = bflb_utils.int_to_4bytearray_l(len(signature))
        sig_field = len_array + signature
        crcarray = bflb_utils.get_crc32_bytearray(sig_field)
        return pk_data, pk_hash, sig_field + crcarray
    except Exception as e:
        bflb_utils.printf(e)
        sys.exit()


# read one file and append crc if needed
def img_create_read_file_append_crc(file, crc):
    with open(file, "rb") as fp:
        read_data = bytearray(fp.read())
        crcarray = bytearray(0)
        if crc:
            crcarray = bflb_utils.get_crc32_bytearray(read_data)
    return read_data + crcarray


def encrypt_loader_bin_do(
    file,
    sign,
    encrypt,
    temp_encrypt_key,
    temp_encrypt_iv,
    publickey_file,
    privatekey_file,
):
    if encrypt or sign:
        encrypt_key = bytearray(0)
        encrypt_iv = bytearray(0)
        load_helper_bin_header = bytearray(0)
        load_helper_bin_body = bytearray(0)

        # get header & body
        offset = bootcfg_start
        sign_pos = 0
        encrypt_type_pos = 2
        pk_data = bytearray(0)
        signature = bytearray(0)
        aesiv_data = bytearray(0)
        data_tohash = bytearray(0)

        with open(file, "rb") as fp:
            load_helper_bin = fp.read()
            load_helper_bin_header = load_helper_bin[0:header_len]
            load_helper_bin_body = load_helper_bin[header_len:]

        if load_helper_bin_header != bytearray(0) and load_helper_bin_body != bytearray(0):
            # encrypt body
            load_helper_bin_body = bflb_utils.fill_to_16(load_helper_bin_body)
            if encrypt:
                encrypt_key = bflb_utils.hexstr_to_bytearray(temp_encrypt_key)
                encrypt_iv = bflb_utils.hexstr_to_bytearray(temp_encrypt_iv)
                iv_crcarray = bflb_utils.get_crc32_bytearray(encrypt_iv)
                aesiv_data = encrypt_iv + iv_crcarray
                data_tohash = data_tohash + aesiv_data
                load_helper_bin_body_encrypt = bflb_utils.img_create_encrypt_data(
                    load_helper_bin_body, encrypt_key, encrypt_iv, 0
                )
            else:
                load_helper_bin_body_encrypt = load_helper_bin_body
            # update header
            data = bytearray(load_helper_bin_header)
            oldval = bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(data[offset : offset + 4]))
            newval = oldval
            if encrypt:
                newval = newval | (1 << encrypt_type_pos)
            if sign:
                newval = newval | (1 << sign_pos)
                data_tohash += load_helper_bin_body_encrypt
                pk_data, pk_hash, signature = img_create_sign_data(data_tohash, privatekey_file, publickey_file)
                pk_data = pk_data + bflb_utils.get_crc32_bytearray(pk_data)
            data[offset : offset + 4] = bflb_utils.int_to_4bytearray_l(newval)
            load_helper_bin_header = data
            load_helper_bin_encrypt = (
                load_helper_bin_header + pk_data + signature + aesiv_data + load_helper_bin_body_encrypt
            )
            # calculate hash
            hashfun = hashlib.sha256()
            hashfun.update(load_helper_bin_body_encrypt)
            hash = bflb_utils.hexstr_to_bytearray(hashfun.hexdigest())
            # update hash & crc
            load_helper_bin_data = bytearray(load_helper_bin_encrypt)
            load_helper_bin_encrypt = img_create_update_bootheader_if(load_helper_bin_data, hash, 1)
        return True, load_helper_bin_encrypt
    return False, None


def img_creat_process(group_type, flash_img, cfg, security=False, **kwargs):
    encrypt_blk_size = 16
    padding = bytearray(encrypt_blk_size)
    data_tohash = bytearray(0)
    cfg_section = ""
    if group_type == "group0":
        img_update_efuse_fun = img_update_efuse_group0
        cfg_section = "Img_Group0_Cfg"
    elif group_type == "group1":
        img_update_efuse_fun = img_update_efuse_group1
        cfg_section = "Img_Group1_Cfg"
    else:
        bflb_utils.printf("group type is incorrect")
        return "FAIL", data_tohash
    # get segdata to deal with
    segheader_file = []
    if flash_img == 0:
        for files in cfg.get(cfg_section, "segheader_file").split(" "):
            segheader_file.append(str(files))
    segdata_file = []
    for files in cfg.get(cfg_section, "segdata_file").split("|"):
        if files:
            segdata_file.append(str(files))
    # get bootheader
    boot_header_file = cfg.get(cfg_section, "boot_header_file")
    bootheader_data = img_create_read_file_append_crc(boot_header_file, 0)
    # decide encrypt and sign
    encrypt = 0
    sign, encrypt, key_sel, xts_mode = img_create_get_sign_encrypt_info(bootheader_data)
    boot_entry = img_create_get_img_start_addr(bootheader_data)
    aesiv_data = bytearray(0)
    pk_data = bytearray(0)
    publickey_file = ""
    privatekey_file_uecc = ""
    if sign:
        bflb_utils.printf("Image need sign")
        publickey_file = cfg.get(cfg_section, "publickey_file")
        privatekey_file_uecc = cfg.get(cfg_section, "privatekey_file_uecc")
    if encrypt:
        bflb_utils.printf("Image need encrypt ", encrypt)
        if xts_mode == 1:
            bflb_utils.printf("Enable xts mode")
        encrypt_key_org = bflb_utils.hexstr_to_bytearray(cfg.get(cfg_section, "aes_key_org"))
        if encrypt == 1:
            if xts_mode == 1:
                encrypt_key = encrypt_key_org[0:32]
            else:
                encrypt_key = encrypt_key_org[0:16]
        elif encrypt == 2:
            if xts_mode == 1:
                encrypt_key = encrypt_key_org[0:32]
            else:
                encrypt_key = encrypt_key_org[0:32]
        elif encrypt == 3:
            if xts_mode == 1:
                encrypt_key = encrypt_key_org[0:24]
            else:
                encrypt_key = encrypt_key_org[0:24]
        # bflb_utils.printf("Key= ", binascii.hexlify(encrypt_key))
        iv_value = cfg.get(cfg_section, "aes_iv")
        if xts_mode == 1:
            iv_value = iv_value[24:32] + iv_value[:24]
        encrypt_iv = bflb_utils.hexstr_to_bytearray(iv_value)
        iv_crcarray = bflb_utils.get_crc32_bytearray(encrypt_iv)
        aesiv_data = encrypt_iv + iv_crcarray
        data_tohash = data_tohash + aesiv_data
    # decide seg_cnt values
    seg_cnt = len(segheader_file)
    segdata_cnt = len(segdata_file)
    if flash_img == 0 and seg_cnt != segdata_cnt:
        bflb_utils.printf("Segheader count and segdata count do not match")
        return "FAIL", data_tohash
    data_toencrypt = bytearray(0)
    if flash_img == 0:
        i = 0
        seg_header_list = []
        seg_data_list = []
        while i < seg_cnt:
            # read seg data and calculate crcdata
            seg_data = bytearray(0)
            if segdata_file[i] != "UNUSED":
                seg_data = img_create_read_file_append_crc(segdata_file[i], 0)
            padding_size = 0
            if len(seg_data) % encrypt_blk_size != 0:
                padding_size = encrypt_blk_size - len(seg_data) % encrypt_blk_size
                seg_data += padding[0:padding_size]
            segdata_crcarray = bflb_utils.get_crc32_bytearray(seg_data)
            seg_data_list.append(seg_data)
            # read seg header and replace segdata's CRC
            seg_header = img_create_read_file_append_crc(segheader_file[i], 0)
            seg_header = img_create_update_segheader(
                seg_header,
                bflb_utils.int_to_4bytearray_l(len(seg_data)),
                segdata_crcarray,
            )
            segheader_crcarray = bflb_utils.get_crc32_bytearray(seg_header)
            seg_header = seg_header + segheader_crcarray
            seg_header_list.append(seg_header)
            i = i + 1
        # get all data to encrypt
        i = 0
        cnt = 0
        while i < seg_cnt:
            # ,now changed to encrypted since download tool's segdata len is from bootrom
            if seg_header_list[i][4:8] != bytearray(4):
                data_toencrypt += seg_header_list[i]
                data_toencrypt += seg_data_list[i]
                cnt += 1
            i += 1
        seg_cnt = cnt
    else:
        seg_data = img_get_one_group_img(boot_entry, segdata_file)
        padding_size = 0
        if len(seg_data) % encrypt_blk_size != 0:
            padding_size = encrypt_blk_size - len(seg_data) % encrypt_blk_size
            seg_data += padding[0:padding_size]
        data_toencrypt += seg_data
        seg_cnt = len(data_toencrypt)
    # do encrypt
    if encrypt:
        unencrypt_mfg_data = bytearray(0)
        if seg_cnt >= 0x2000:
            if data_toencrypt[0x1000:0x1004] == bytearray("0mfg".encode("utf-8")):
                unencrypt_mfg_data = data_toencrypt[0x1000:0x2000]
        if xts_mode:
            return "FAIL", data_tohash
            # encrypt_iv = codecs.decode(reverse_iv(encrypt_iv), 'hex')
            # data_toencrypt = img_create_encrypt_data_xts(data_toencrypt, encrypt_key, encrypt_iv, encrypt)
        else:
            data_toencrypt = img_create_encrypt_data(data_toencrypt, encrypt_key, encrypt_iv, flash_img)
        if unencrypt_mfg_data != bytearray(0):
            data_toencrypt = data_toencrypt[0:0x1000] + unencrypt_mfg_data + data_toencrypt[0x2000:]
    # get fw data
    fw_data = bytearray(0)
    data_tohash += data_toencrypt
    fw_data = data_toencrypt
    # hash fw img
    hash = img_create_sha256_data(data_tohash)
    bflb_utils.printf("Image hash is ", binascii.hexlify(hash))
    # add signautre
    signature = bytearray(0)
    pk_hash = None
    if sign == 1:
        if "privatekey_str" in kwargs and "publickey_str" in kwargs and kwargs["privatekey_str"]:
            pk_data, pk_hash, signature = img_create_sign_data(
                data_tohash, kwargs["privatekey_str"], kwargs["publickey_str"], 1
            )
        else:
            pk_data, pk_hash, signature = img_create_sign_data(data_tohash, privatekey_file_uecc, publickey_file)
        pk_data = pk_data + bflb_utils.get_crc32_bytearray(pk_data)

    flash_cfg_addr = len(bootheader_data + pk_data + pk_data + signature + signature + aesiv_data)
    flash_cfg_list_len = 0
    flash_cfg_list = bytearray(0)
    flash_cfg_table = bytearray(0)
    if flash_img == 1:
        # only flash boot need flashcfg table
        # if flash mid != 0xff, create flashcfg table list
        if bootheader_data[25:26] == b"\xff":
            flash_cfg_list, flash_cfg_table, flash_cfg_list_len = create_flashcfg_table(flash_cfg_addr)

    # update boot header and recalculate crc
    bootheader_data = img_create_update_bootheader(bootheader_data, hash, seg_cnt, flash_cfg_addr, flash_cfg_list_len)

    # write whole image
    if flash_img == 1:
        bflb_utils.printf("Write flash img")
        bootinfo_file_name = cfg.get(cfg_section, "bootinfo_file")
        with open(bootinfo_file_name, "wb+") as fp:
            bootinfo = (
                bootheader_data
                + pk_data
                + pk_data
                + signature
                + signature
                + aesiv_data
                + flash_cfg_list
                + flash_cfg_table
            )
            fp.write(bootinfo)
        fw_file_name = cfg.get(cfg_section, "img_file")
        with open(fw_file_name, "wb+") as fp:
            fp.write(fw_data)
        # add create fw with hash
        fw_data_hash = img_create_sha256_data(fw_data)
        with open(fw_file_name.replace(".bin", "_withhash.bin"), "wb+") as fp:
            fp.write(fw_data + fw_data_hash)
        # update efuse
        if encrypt:
            flash_encrypt_type = 0
            if encrypt == 1:
                # AES 128
                flash_encrypt_type = 1
            if encrypt == 2:
                # AES 256
                flash_encrypt_type = 3
            if encrypt == 3:
                # AES 192
                flash_encrypt_type = 2
            if xts_mode == 1:
                # AES XTS mode
                flash_encrypt_type += 3
            img_update_efuse_fun(
                cfg,
                sign,
                pk_hash,
                flash_encrypt_type,
                encrypt_key + bytearray(32 - len(encrypt_key)),
                key_sel,
                None,
                security,
            )
        else:
            img_update_efuse_fun(cfg, sign, pk_hash, encrypt, None, key_sel, None, security)
    else:
        bflb_utils.printf("Write if img")
        whole_img_file_name = cfg.get(cfg_section, "whole_img_file")
        with open(whole_img_file_name, "wb+") as fp:
            img_data = bootheader_data + pk_data + pk_data + signature + signature + aesiv_data + fw_data
            fp.write(img_data)
        # update efuse
        if encrypt:
            if_encrypt_type = 0
            if encrypt == 1:
                # AES 128
                if_encrypt_type = 1
            if encrypt == 2:
                # AES 256
                if_encrypt_type = 3
            if encrypt == 3:
                # AES 192
                if_encrypt_type = 2
            if xts_mode == 1:
                # AES XTS mode
                if_encrypt_type += 3
            img_update_efuse_fun(
                cfg,
                sign,
                pk_hash,
                if_encrypt_type,
                None,
                key_sel,
                encrypt_key + bytearray(32 - len(encrypt_key)),
                security,
            )
        else:
            img_update_efuse_fun(cfg, sign, pk_hash, 0, None, key_sel, bytearray(32), security)
    return "OK", data_tohash


def img_create_do(args, img_dir_path=None, config_file=None, **kwargs):
    bflb_utils.printf("Image create path: ", img_dir_path)
    if config_file is None:
        config_file = img_dir_path + "/img_create_cfg.ini"
    bflb_utils.printf("Config file: ", config_file)
    cfg = BFConfigParser()
    cfg.read(config_file)
    group_type = "all"
    img_type = "media"
    signer = "none"
    security = False
    data_tohash = bytearray(0)
    try:
        if args.image:
            img_type = args.image
        if args.group:
            group_type = args.group
        if args.signer:
            signer = args.signer
        if args.security:
            security = args.security == "efuse"
    except Exception as error:
        # bflb_utils.printf(help information and exit:)
        # will  something like "option -a not recognized")
        bflb_utils.printf(error)
    if img_type == "media":
        flash_img = 1
    else:
        flash_img = 0

    # deal image creation
    ret0 = ret1 = "OK"
    if group_type == "group0":
        ret0, data_tohash0 = img_creat_process("group0", flash_img, cfg, security, **kwargs)
    elif group_type == "group1":
        ret1, data_tohash1 = img_creat_process("group1", flash_img, cfg, security, **kwargs)
    elif group_type == "all":
        ret0, data_tohash0 = img_creat_process("group0", flash_img, cfg, False, **kwargs)
        ret1, data_tohash1 = img_creat_process("group1", flash_img, cfg, security, **kwargs)
    else:
        img_creat_process("", flash_img, cfg, security)

    if ret0 != "OK":
        bflb_utils.printf("Fail to create group0 images!")
        return
    if ret1 != "OK":
        bflb_utils.printf("Fail to create group1 images!")


def create_sp_media_image(config, cpu_type=None, security=False):
    bflb_utils.printf("========= sp image create =========")
    cfg = BFConfigParser()
    cfg.read(config)
    if cpu_type == "Group1":
        img_creat_process("group1", 1, cfg, security)
    else:
        img_creat_process("group0", 1, cfg, security)


