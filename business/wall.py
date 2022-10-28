
import helpers.autocad as cad
from business import OUTPUT, SETTINGS
from helpers.common import get_distance_2d
from rich import print

def get_revit_walls_open(thickness = SETTINGS['wall_thk']):
    '''
    Returns the tuple of walls from selected objects in autocad (polylines, lines,arcs).

        Parameters:
                None

        Returns:
                success (bool) : True if all is ok
    '''

    try:
        selected_cad_objects = cad.select_get_multiple_objects()
        walls = walls_polyline = walls_line = walls_arc = []
        walls_polyline = get_wall_by_center_line(selected_cad_objects['polylines'])
        walls_line = get_wall_by_line(selected_cad_objects['lines'])
        walls_arc = get_wall_by_arc(selected_cad_objects['arcs'])
        walls = walls_polyline + walls_line
        if len(walls) > 0:
            OUTPUT['walls'] = walls
        if len(walls_arc) > 0:
            OUTPUT['arc_walls'] = walls_arc

        return True
    except:
        print("Error in revit columns")


def get_wall_by_line(selected_lines_coordinates, thickness = SETTINGS['wall_thk'] , rounding=SETTINGS['rounding_digits']):
    walls = []
    thickness = int(thickness)
    label = f'W{thickness}'
    
    #print( selected_polylines_coordinates)
    for line in selected_lines_coordinates:
        points_list = []
        for pnt in line:
            x,y,z = pnt
            x += SETTINGS['shift_xdir']
            y += SETTINGS['shift_ydir']
            points_list.append((x,y))
        walls.append({'shape':(thickness, label), 'coordinates':points_list})
    return walls


def get_wall_by_arc(selected_arcs_coordinates, thickness = SETTINGS['wall_thk'] , rounding=SETTINGS['rounding_digits']):
    walls = []
    thickness = int(thickness)
    label = f'W{thickness}'
    #(diameter, (center_point,start_point,end_point))
    for arc in selected_arcs_coordinates:
        points_list = []
        for pnt in arc[1]:
            x,y,z = pnt
            x += float(SETTINGS['shift_xdir'])
            y += float(SETTINGS['shift_ydir'])
            points_list.append((x,y))
        walls.append({'shape':(thickness, label), 'coordinates':points_list})
    return walls


def get_wall_by_center_line(selected_polylines_coordinates, rounding=SETTINGS['rounding_digits']):
    walls = []
    #print( selected_polylines_coordinates)
    for pl in selected_polylines_coordinates:
        points = {}
        thicknessess = []
        for p in pl:
            points[p] = {'taken':False, 'near_point':None}
        points_list = list(points.keys())

        for p in points_list:
            if points[p]['taken']:
                continue
            else:
                points[p]['taken'] = True
                near_points = [k for k,v in points.items() if v['taken'] == False]
                near_point, thickness = _get_nearest_point(p,near_points,rounding)
                if near_point is not None:
                    points[near_point]['taken'] = True
                    points[p]['near_point'] = near_point
                    thicknessess.append(thickness)
        #print(points)
        mid_points = []
        for k,v in points.items():
            if v['near_point'] is not None:
                x = round((k[0] + v['near_point'][0])/2 + SETTINGS['shift_xdir'], rounding)
                y = round((k[1] + v['near_point'][1])/2 + SETTINGS['shift_ydir'], rounding)
                mid_points.append((x,y))
        #print(mid_points, thickness)
        thickness = min(thicknessess)
        thickness = round(thickness, rounding)
        thickness = int(thickness)
        label = f'W{thickness}'
        walls.append({'shape':(thickness, label), 'coordinates':mid_points})
    return walls


def _get_nearest_point(point1, point_list,rounding=SETTINGS['rounding_digits']):
    min_distance = 100000
    nearest_point = ()
    for point in point_list:
        distance = get_distance_2d(point1, point,rounding)
        if distance == 0 :
            continue
        if distance <= min_distance:
            min_distance = distance
            nearest_point = point
    return nearest_point,min_distance


