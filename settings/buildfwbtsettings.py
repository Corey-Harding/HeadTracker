#!/usr/bin/python

from array import array
import csv

import set_common as s

f = open("../firmware/src/src/Bluetooth/blechars.cpp","w")
f.write("""\
/*
* This file is part of the Head Tracker distribution (https://github.com/dlktdr/headtracker)
* Copyright (c) 2022 Cliff Blackburn
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, version 3.
*
* This program is distributed in the hope that it will be useful, but
* WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
* General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

/**********************************************
 *
 *  !!! THIS FILE IS AUTOMATICALLY GENERATED, DO NOT EDIT DIRECTLY !!!
 *
 *  Modify settings.csv and execute buildsettings.py to generate this source file
 *
 ***********************************************/

/* This file contains the settings which are be adjustable via Bluetooth Web App
 */

#include "blechars.h"
#include "trackersettings.h"
#include "log.h"

""")

# Read the settings
s.readSettings()

# Data Storage Variables
for row in s.settings:
  if row[s.colbleaddr].strip() != "":
    name = row[s.colname].lower().strip()
    addr = row[s.colbleaddr].upper().strip()
    f.write(s.typeToC(row[s.coltype].strip()) + " bt_" + name + ";\n")

f.write("\n")

for row in s.settings:
  if row[s.colbleaddr].strip() != "":
    name = row[s.colname].lower().strip()
    addr = row[s.colbleaddr].upper().strip()
    f.write("struct bt_uuid_16 bt_uuid_" + name + " = BT_UUID_INIT_16(0x" + addr + ");\n")

f.write("\n")

for row in s.settings:
  if row[s.colbleaddr].strip() != "":
    name = row[s.colname].strip()
    addr = row[s.colbleaddr].upper().strip()
    f.write("""\
ssize_t btwr_{lowername}(struct bt_conn *conn, const struct bt_gatt_attr *attr, const void *buf, uint16_t len, uint16_t offset, uint8_t flags)
{{
  if(len == sizeof({ctype})) {{
    {ctype} newvalue;
    memcpy(&newvalue, buf, len);
    //LOGD("BT_Wr {name} (0x{addr})");
    trkset.set{name}(newvalue);
  }}
  return len;
}}
ssize_t btrd_{lowername}(struct bt_conn *conn, const struct bt_gatt_attr *attr, void *buf, uint16_t len, uint16_t offset)
{{
  char *value = (char *)attr->user_data;
  //LOGD("BT_Rd {name} (0x{addr})");
  bt_{lowername} = trkset.get{name}();
  return bt_gatt_attr_read(conn, attr, buf, len, offset, value, sizeof({ctype}));
}}

""".format(name = name, lowername = name.lower(), addr = addr, ctype = s.typeToC(row[s.coltype])))

f.close()

f = open("../firmware/src/src/targets/nrf52/blechars.h","w")
f.write("""\
/*
* This file is part of the Head Tracker distribution (https://github.com/dlktdr/headtracker)
* Copyright (c) 2022 Cliff Blackburn
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, version 3.
*
* This program is distributed in the hope that it will be useful, but
* WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
* General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

/**********************************************
 *
 *  !!! THIS FILE IS AUTOMATICALLY GENERATED, DO NOT EDIT DIRECTLY !!!
 *
 *  Modify /utils/settings.csv and execute buildsettings.py to generate this bluetooth header
 *
 ***********************************************/

/* This file contains the settings which are be adjustable via Bluetooth Web App
 */

#pragma once

#include <zephyr.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/conn.h>
#include <bluetooth/gatt.h>
#include <bluetooth/hci.h>
#include <bluetooth/uuid.h>

""")

# Data Storage Variables
for row in s.settings:
  if row[s.colbleaddr].strip() != "":
    name = row[s.colname].lower().strip()
    addr = row[s.colbleaddr].upper().strip()
    f.write("extern " + s.typeToC(row[s.coltype].strip()) + " bt_" + name + ";\n")

f.write("\n")

for row in s.settings:
  if row[s.colbleaddr].strip() != "":
    name = row[s.colname].lower().strip()
    addr = row[s.colbleaddr].upper().strip()
    f.write("extern struct bt_uuid_16 bt_uuid_" + name + ";\n")

f.write("\n")

for row in s.settings:
  if row[s.colbleaddr].strip() != "":
    name = row[s.colname].strip()
    addr = row[s.colbleaddr].upper().strip()
    f.write("""\
ssize_t btwr_{lowername}(struct bt_conn *conn, const struct bt_gatt_attr *attr, const void *buf, uint16_t len, uint16_t offset, uint8_t flags);
ssize_t btrd_{lowername}(struct bt_conn *conn, const struct bt_gatt_attr *attr, void *buf, uint16_t len, uint16_t offset);
""".format(name = name, lowername = name.lower(), addr = addr, ctype = s.typeToC(row[s.coltype])))

f.write("\n#define AUTOGENERATED_CHARACTERISTICS \\\n")

for row in s.settings:
  if row[s.colbleaddr].strip() != "":
    name = row[s.colname].lower().strip()
    addr = row[s.colbleaddr].upper().strip()
    f.write("""\
    ,BT_GATT_CHARACTERISTIC(&bt_uuid_{lowername}.uuid, BT_GATT_CHRC_READ | BT_GATT_CHRC_WRITE, \\
                                                   BT_GATT_PERM_READ | BT_GATT_PERM_WRITE, \\
                                                   btrd_{lowername}, btwr_{lowername}, (void*)&bt_{lowername}) \\
""".format(name = name, lowername = name.lower(), addr = addr, ctype = s.typeToC(row[s.coltype])))

f.write("\n")

f.close()


print("Gernerated Firmware Bluetooth Settings")