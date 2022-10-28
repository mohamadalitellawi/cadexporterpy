import math
from shapely.geometry import Polygon


ROUNDING_3 = 3

def get_polygon_centroid(polyline2D):
    polygon = Polygon(polyline2D)
    return list(polygon.centroid.coords)

def get_polygon_area(polyline2D):
    polygon = Polygon(polyline2D)
    return polygon.area

def flatten_3d_polylines(polylines, level = 0):
    new_polylines = []
    z = level
    for polyline in polylines:
        new_polyline = []
        for point in polyline:
            x = point[0]
            y = point[1]
            new_polyline.append((x,y,z))
        new_polylines.append(new_polyline)
    return new_polylines


def get_equivelant_rectangle(polyline2D,area,rounding = ROUNDING_3) :
    '''return length, width, angle from x direction in degree, label'''

    max_length = -1.0
    
    polyline = polyline2D.copy()
    #print(polyline)
    # add last point to the end to close the polyline
    polyline.append(polyline[0])
    for i,pnt in enumerate(polyline):
        if i == 0:
            continue
        prev_pnt = polyline2D[i-1]
        length  = get_distance_2d(pnt,prev_pnt,rounding)
        if length <= max_length:
            continue
        # continue only if we found larger length
        max_length = length
        if (pnt[0] - prev_pnt[0]) == 0:
            slope = 90
        else:
            slope = (pnt[1] - prev_pnt[1])/(pnt[0] - prev_pnt[0])

        angle_in_radians = math.atan(slope)
        angle_in_degrees = math.degrees(angle_in_radians)
        angle_in_degrees = round(angle_in_degrees,rounding)

        width = round(area / length, rounding)
        label = f'R{int(length)}*{int(width)}'
        result = (length, width, angle_in_degrees,label)
    
    return result



def shift_2d_coordinates(coordinates, x_dir_shift,y_dir_shift):
    new_coordinates = []
    # if shifting values are 0,0 no need to update coordinates
    if float(x_dir_shift) == 0 and float(y_dir_shift) == 0:
        return coordinates

    for p in coordinates:
        new_x = p[0] + float(x_dir_shift)
        new_y = p[1] + float(y_dir_shift)
        new_coordinates.append((new_x,new_y))
    return new_coordinates

def get_distance_2d(p0,p1,rounding = ROUNDING_3):
    return round(((p1[0]-p0[0])**2+(p1[1]-p0[1])**2)**0.5,rounding)

def get_polyline_segments_length_2d(polyline_coordinates,rounding = ROUNDING_3):
    start_point = polyline_coordinates[0]

    polyline_segments_length = [0]
    for indx,p in enumerate(polyline_coordinates):
        if indx == 0 : continue
        polyline_segments_length.append(
            get_distance_2d(polyline_coordinates[indx-1], p, rounding)
        )
    total_length = sum(polyline_segments_length)

    polyline_segments_length[0] = total_length # store total length in first element instead of zero
    return polyline_segments_length

def main():
    pass

if __name__ == "__main__":
    main()