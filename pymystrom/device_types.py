"""
Device types.

See https://api.mystrom.ch/#f37a4be7-0233-4d93-915e-c6f92656f129
"""

DEVICE_MAPPING_NUMERIC = {
    101: "Switch CH v1",
    102: "Bulb",
    103: "Button+",
    104: "Button",
    105: "LED Strip",
    106: "Switch CH v2",
    107: "Switch EU",
    110: "Motion Sensor",
    113: "modulo® STECCO / CUBO",
    118: "Button Plus 2nd",
    120: "Switch Zero",
}

DEVICE_MAPPING_LITERAL = {
    "WSW": DEVICE_MAPPING_NUMERIC[101],
    "WRB": DEVICE_MAPPING_NUMERIC[102],
    "WBP": DEVICE_MAPPING_NUMERIC[103],
    "WBS": DEVICE_MAPPING_NUMERIC[104],
    "WRS": DEVICE_MAPPING_NUMERIC[105],
    "WS2": DEVICE_MAPPING_NUMERIC[106],
    "WSE": DEVICE_MAPPING_NUMERIC[107],
    "WMS": DEVICE_MAPPING_NUMERIC[110],
    "WLL": DEVICE_MAPPING_NUMERIC[113],
    "BP2": DEVICE_MAPPING_NUMERIC[118],
    "LCS": DEVICE_MAPPING_NUMERIC[120],
}
