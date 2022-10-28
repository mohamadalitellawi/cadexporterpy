import helpers.autocad as autocadhelper
import helpers.common as mhelper
import json

TEMP_PATH = r'C:\Users\mali\Desktop\mytemp.txt'

COLUMN_FILE_PATH = r'C:\column_output.json'
WALL_FILE_PATH = r'C:\wall_output.json'
FAMILY_REC_TYPES_PATH = r'D:\M_Concrete-Rectangular-Column.txt'
FAMILY_CIR_TYPES_PATH = r'D:\M_Concrete-Round-Column.txt'

SETTINGS = {
    'shift_xdir':0,
    'shift_ydir':0,
    'angle':0,
    'rounding_digits':-1
}

OUTPUT = {}