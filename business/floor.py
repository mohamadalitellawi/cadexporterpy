import helpers.autocad as cad
from business import OUTPUT, SETTINGS
from helpers.common import get_distance_2d
from rich import print


def get_revit_floors_by_edge_polyline(thickness = SETTINGS['floot_thk']):
    '''
    Returns the tuple of floors from selected objects in autocad (polylines, circles).

        Parameters:
                None

        Returns:
                success (bool) : True if all is ok
    '''

    try:
        selected_cad_objects = cad.select_get_multiple_objects()
        floors = floors_circle =  []
        floors = get_floor_by_polyline(selected_cad_objects['polylines'],thickness)
        floors_circle = get_floor_by_circle(selected_cad_objects['circles'],thickness)

        if len(floors) > 0:
            OUTPUT['floors'] = floors

        if len(floors_circle) > 0:
            OUTPUT['floors_circle'] = floors_circle

        return True
    except:
        print("Error in revit floors")
        raise

def get_floor_by_polyline(selected_polylines_coordinates, thickness = SETTINGS['floot_thk'] , rounding=SETTINGS['rounding_digits']):
    floors = []
    thickness = int(thickness)
    label = f'T{thickness}'

    #print( selected_polylines_coordinates)
    for polyline in selected_polylines_coordinates:
        points_list = []
        for pnt in polyline:
            x,y = pnt
            x += SETTINGS['shift_xdir']
            y += SETTINGS['shift_ydir']
            points_list.append((x,y))
        floors.append({'shape':(thickness, label), 'coordinates':points_list})
    return floors

def get_floor_by_circle(selected_circles_coordinates, thickness = SETTINGS['floot_thk'] , rounding=SETTINGS['rounding_digits']):
    floors = []
    thickness = int(thickness)
    label = f'T{thickness}'
    #(diameter, (center_point))
    for circle in selected_circles_coordinates:
        diameter = circle[0]
        x,y,z = circle[1]
        x += float(SETTINGS['shift_xdir'])
        y += float(SETTINGS['shift_ydir'])
        floors.append({'shape':(thickness, label, diameter), 'coordinates':[(x,y)]})
    return floors