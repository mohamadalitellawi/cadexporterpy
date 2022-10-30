import helpers.autocad as autocadhelper
import helpers.common as mhelper
import json


TEMP_PATH = r'.\out.json'

COLUMN_FILE_PATH = r'.\column_output.json'
WALL_FILE_PATH = r'.\wall_output.json'
FLOOR_FILE_PATH = r'.\floor_output.json'
# FAMILY_REC_TYPES_PATH = r'.\M_Concrete-Rectangular-Column.txt'
# FAMILY_CIR_TYPES_PATH = r'.\M_Concrete-Round-Column.txt'
COLUMN_FAMILY_REC = 'Structural-Column_Rectangular_NA'
COLUMN_FAMILY_CIR = 'Structural-Column_Round_NA'
FAMILY_REC_TYPES_PATH = r'.\Structural-Column_Rectangular_NA.txt'
FAMILY_CIR_TYPES_PATH = r'.\Structural-Column_Round_NA.txt'


SETTINGS = {
    'shift_xdir':0,
    'shift_ydir':0,
    'angle':0,
    'rounding_digits':-1,
    'wall_thk':200,
    'floot_thk':200
}

OUTPUT = {'settings':SETTINGS, 'columns':[],'columns_circle':[], 'walls':[], 'walls_arc':[], 'walls_circle':[],'floors' : [], 'floors_circle' :[]}




def get_columns_labels():
    labels = []
    for k,v in OUTPUT.items():
        if k.startswith('columns'):
            for column in v:
                shape = column['shape'][-1]
                labels.append(shape)
    if len(labels) > 0:
        return set(labels)


def get_walls_labels():
    labels = []
    for k,v in OUTPUT.items():
        if k.startswith('walls'):
            for wall in v:
                shape = wall['shape'][1]
                labels.append(shape)
    if len(labels) > 0:
        return set(labels)



def get_floors_labels():
    labels = []
    for k,v in OUTPUT.items():
        if k.startswith('floors'):
            for floor in v:
                shape = floor['shape'][1]
                labels.append(shape)
    if len(labels) > 0:
        return set(labels)



def extract_all_current_types():
    result = {
        'columns':get_columns_labels(),
        'walls':get_walls_labels(),
        'floors': get_floors_labels()
    }
    return result



def reset_default_settings():
    SETTINGS = {
    'shift_xdir':0.0,
    'shift_ydir':0.0,
    'angle':0.0,
    'rounding_digits':-1,
    'wall_thk':200,
    'floot_thk':200
}
    return SETTINGS

def update_settings_from_console():
    try:
        prev_shift_xdir = SETTINGS['shift_xdir']
        prev_shift_ydir = SETTINGS['shift_ydir']
        prev_angle = SETTINGS['angle']
        prev_rounding_digits = SETTINGS['rounding_digits']
        prev_wall_thk = SETTINGS['wall_thk']
        prev_floot_thk = SETTINGS['floot_thk']

        shift_xdir = input(f'shift_xdir [{prev_shift_xdir}]: ')
        shift_ydir = input(f'shift_ydir [{prev_shift_ydir}]: ')
        angle = input(f'angle [{prev_angle}]: ')
        rounding_digits = input(f'rounding_digits [{prev_rounding_digits}]: ')
        wall_thk = input(f'wall_thk [{prev_wall_thk}]: ')
        floot_thk = input(f'floot_thk [{prev_floot_thk}]: ')

        SETTINGS['shift_xdir'] = float(shift_xdir) if len(shift_xdir) > 0 else prev_shift_xdir
        SETTINGS['shift_ydir']=float(shift_ydir) if len(shift_ydir) > 0 else prev_shift_ydir
        SETTINGS['angle']=float(angle) if len(angle) > 0 else prev_angle
        SETTINGS['rounding_digits']=int(rounding_digits) if len(rounding_digits) > 0 else prev_rounding_digits
        SETTINGS['wall_thk']=int(wall_thk) if len(wall_thk) > 0 else prev_wall_thk
        SETTINGS['floot_thk']=int(floot_thk) if len(floot_thk) > 0 else prev_floot_thk
    except:
        print("Error happend during update settings!\nwe will reset")
        reset_default_settings()
    finally:
        return SETTINGS

