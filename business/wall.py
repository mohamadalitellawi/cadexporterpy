
import helpers.autocad as cad
from business import OUTPUT, SETTINGS, get_walls_labels
from helpers.common import get_distance_2d
from rich import print

def get_revit_walls_open(update_existing = False):
    '''
    Returns the tuple of walls from selected objects in autocad (polylines).

        Parameters:
                update_existing (bool) : option to add new selected data to existing data (walls only)

        Returns:
                success (bool) : True if all is ok
    '''

    try:
        selected_cad_objects = cad.select_get_multiple_objects()
        walls = []
        walls = get_open_wall_by_polyline(selected_cad_objects['polylines'])
        if update_existing:
            existing_walls = OUTPUT['walls']
            if len(existing_walls) > 0 :
                walls = existing_walls + walls

        if len(walls) > 0:
            OUTPUT['walls'] = walls
        print(get_walls_labels())
        return True
    except:
        print("Error in revit open walls")
        raise


def get_revit_walls_by_centerline(thickness = SETTINGS['wall_thk']):
    '''
    Returns the tuple of walls from selected objects in autocad (polylines, lines,arcs).

        Parameters:
                None

        Returns:
                success (bool) : True if all is ok
    '''

    try:
        selected_cad_objects = cad.select_get_multiple_objects()
        walls = walls_polyline = walls_line = walls_arc = walls_circle = []
        walls_polyline = get_wall_by_polyline(selected_cad_objects['polylines'],thickness)
        walls_line = get_wall_by_line(selected_cad_objects['lines'],thickness)
        walls_arc = get_wall_by_arc(selected_cad_objects['arcs'],thickness)
        walls_circle = get_wall_by_circle(selected_cad_objects['circles'],thickness)

        walls = walls_polyline + walls_line
        if len(walls) > 0:
            OUTPUT['walls'] = walls
        if len(walls_arc) > 0:
            OUTPUT['walls_arc'] = walls_arc
        if len(walls_circle) > 0:
            OUTPUT['walls_circle'] = walls_circle
        print(get_walls_labels())
        return True
    except:
        print("Error in revit walls")
        raise





















def get_wall_by_polyline(selected_polylines_coordinates, thickness = SETTINGS['wall_thk'] , rounding=SETTINGS['rounding_digits']):
    walls = []
    thickness = int(thickness)
    label = f'HSC_Wall_{thickness}_RC-40Mpa'

    #print( selected_polylines_coordinates)
    for polyline in selected_polylines_coordinates:
        points_list = []
        for pnt in polyline:
            x,y = pnt
            x += SETTINGS['shift_xdir']
            y += SETTINGS['shift_ydir']
            points_list.append((x,y))
        walls.append({'shape':(thickness, label), 'coordinates':points_list})
    return walls


def get_wall_by_line(selected_lines_coordinates, thickness = SETTINGS['wall_thk'] , rounding=SETTINGS['rounding_digits']):
    walls = []
    thickness = int(thickness)
    label = f'HSC_Wall_{thickness}_RC-40Mpa'
    
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
    label = f'HSC_Wall_{thickness}_RC-40Mpa'
    #(diameter, (center_point,start_point,end_point))
    for arc in selected_arcs_coordinates:
        points_list = []
        diameter = arc[0]
        for pnt in arc[1]:
            x,y,z = pnt
            x += float(SETTINGS['shift_xdir'])
            y += float(SETTINGS['shift_ydir'])
            points_list.append((x,y))
        walls.append({'shape':(thickness, label, diameter), 'coordinates':points_list })
    return walls


def get_wall_by_circle(selected_circles_coordinates, thickness = SETTINGS['wall_thk'] , rounding=SETTINGS['rounding_digits']):
    walls = []
    thickness = int(thickness)
    label = f'HSC_Wall_{thickness}_RC-40Mpa'
    #(diameter, (center_point))
    for circle in selected_circles_coordinates:
        diameter = circle[0]
        x,y,z = circle[1]
        x += float(SETTINGS['shift_xdir'])
        y += float(SETTINGS['shift_ydir'])
        walls.append({'shape':(thickness, label, diameter), 'coordinates':[(x,y)]})
    return walls







def get_open_wall_by_polyline(selected_polylines_coordinates, rounding=SETTINGS['rounding_digits']):
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
        label = f'HSC_Wall_{thickness}_RC-40Mpa'
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


