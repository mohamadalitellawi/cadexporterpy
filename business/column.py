

from business import OUTPUT, SETTINGS, TEMP_PATH, FAMILY_REC_TYPES_PATH, FAMILY_CIR_TYPES_PATH
from helpers.common import get_equivelant_rectangle, get_polygon_area,get_polygon_centroid
import helpers.autocad as cad


def test():
    return cad.select_get_multiple_objects()


def get_revit_columns(export_types = True):
    '''
    Returns the tuple of rec and circle columns from selected objects in autocad (polylines, circles).

        Parameters:
                export_types (bool): True for export family type files

        Returns:
                success (bool) : True if all is ok
    '''

    try:
        selected_cad_objects = cad.select_get_multiple_objects()
        rec_columns = circle_columns = []
        rec_columns = get_rectangular_columns(selected_cad_objects['polylines'])
        circle_columns = get_circular_columns(selected_cad_objects['circles'])
        if len(rec_columns) > 0:
            OUTPUT['columns'] = rec_columns
        if len(circle_columns) > 0:
            OUTPUT['circular_columns'] = circle_columns
        if export_types:
            export_rec_columns_family_types(rec_columns)
            export_cir_columns_family_types(circle_columns)
        return True
    except:
        print("Error in revit columns")


def export_rec_columns_family_types(columns, file_path = FAMILY_REC_TYPES_PATH):
    header = ',b##LENGTH##MILLIMETERS,h##LENGTH##MILLIMETERS,Structural Material##OTHER##\n'
    shapes = []
    for column in columns:
        shapes.append(column['shape'][3])
    shapes = set(shapes)
    with open(file_path, 'w') as file:
        file.write(header)
        for column in shapes:
            b = column.split('*')[1]
            h = column.split('*')[0][1:]
            row = f'{column},{b},{h},"Concrete, Cast-in-Place gray"\n'
            file.write(row)

def get_rectangular_columns(selected_polylines_coordinates):
    shifted_coordinates = []
    columns = []
    for pl in selected_polylines_coordinates:
        shifted_polyline = []
        for pnt in pl:
            x,y = pnt
            x += SETTINGS['shift_xdir']
            y += SETTINGS['shift_ydir']
            shifted_polyline.append((x,y))
        shifted_coordinates.append(shifted_polyline)

    for pl in shifted_coordinates:
        area = get_polygon_area(pl)
        center = get_polygon_centroid(pl)
        center = center[0]
        col = get_equivelant_rectangle(pl,area,rounding=SETTINGS['rounding_digits'])
        columns.append({'shape':col, 'center':center, 'coordinates':pl})
    return columns



def export_cir_columns_family_types(columns, file_path = FAMILY_CIR_TYPES_PATH):
    header = ',b##LENGTH##MILLIMETERS,Structural Material##OTHER##\n'
    shapes = []
    for column in columns:
        shapes.append(column['shape'][1])
    shapes = set(shapes)
    with open(file_path, 'w') as file:
        file.write(header)
        for column in shapes:
            b = column[1:]
            row = f'{column},{b},"Concrete, Cast-in-Place gray"\n'
            file.write(row)



def get_circular_columns(selected_circles):
    columns = []
    for circle in selected_circles:
        diameter = circle[0]
        x,y,z = circle[1]
        x += SETTINGS['shift_xdir']
        y += SETTINGS['shift_ydir']
        diameter = round(diameter,SETTINGS['rounding_digits'])

        label = f'C{int(diameter)}'
        col = (diameter, label)
        columns.append({'shape':col, 'center':(x,y)})
    return columns