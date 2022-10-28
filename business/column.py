
from business import SETTINGS, TEMP_PATH
from helpers.common import get_equivelant_rectangle, get_polygon_area,get_polygon_centroid
import helpers.autocad as cad


def test():
    return cad.select_polylines_get_coordinates2d()

def export_rec_columns_family_types(columns, file_path = TEMP_PATH):
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



def export_cir_columns_family_types(columns, file_path = TEMP_PATH):
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