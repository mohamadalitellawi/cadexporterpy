import sys
from pyautocad import Autocad, APoint
from rich import print

ACAD = None
ROUNDING = 3

def main():
    pass

def get_autocad(create_if_not_exists=True, acad = ACAD):
    try:
        if acad is None:
            acad = Autocad(create_if_not_exists)
        return acad
    except:
        print("Unexpected error")
        raise


def get_block_insertion_point():
    try:
        acad = get_autocad(create_if_not_exists=True)
        acad.prompt("Hello, Autocad from Python\n")
        print (acad.doc.Name)
        result = []

        sset = acad.get_selection("Selecet Blocks:\n")
        
        for indx,obj in enumerate(sset):
            #if ("insert" in str(acad.best_interface(obj)).lower()):
            result.append((*obj.InsertionPoint,))
        
        return result

    except:
        print("Unexpected error")
        raise
    finally:
        acad = None

def get_text_value_coordinate():
    try:
        acad = get_autocad(create_if_not_exists=True)

        acad.prompt("Hello, Autocad from Python\n")
        print (acad.doc.Name)
        result = []

        sset = acad.get_selection("Selecet Texts:\n")
        
        for indx,obj in enumerate(sset):
            if ("text" in str(acad.best_interface(obj)).lower()):
                result.append( (obj.TextString, *obj.TextAlignmentPoint))
        
        return result
    except:
        print("Unexpected error")
        raise
    finally:
        acad = None

def test1():
    try:
        acad = Autocad(create_if_not_exists=True)

        acad.prompt("Hello, Autocad from Python\n")
        print (acad.doc.Name)
        p1 = APoint(0, 0)
        p2 = APoint(50, 25)
        for i in range(5):
            text = acad.model.AddText(u'Hi %s!' % i, p1, 2.5)
            acad.model.AddLine(p1, p2)
            acad.model.AddCircle(p1, 10)
            p1.y += 10

        for obj in acad.iter_objects():
            print (obj.ObjectName)
        
        '''Object name can be partial and case insensitive, e.g. acad.iter_objects('tex') will return AcDbText and AcDbMText objects'''
        for text in acad.iter_objects('Text'):
            print (text.TextString, text.InsertionPoint)
        
        for obj in acad.iter_objects(['Text', 'Line']):
            print (obj.ObjectName)

        for layout in acad.iter_layouts(skip_model=False):
            print(layout.Name)

    except:
        print("Unexpected error")
        raise
    finally:
        acad = None


def select_get_multiple_objects(clean_duplicate= True,rounding_digits = ROUNDING): 
    '''
    Returns the list of selected objects in autocad (lines, polylines, circles).

        Parameters:
                clean_duplicate (bool): True for removing duplicated (points and polylines)
                rounding_digits (int): use to round the coordinates

        Returns:
                multiple objects dictionary (dict of list of tuples of tuples): [(start_coordinate3d, end_coordinate3d)]
                results = {"lines":lines_coordinates, "polylines":polylines_coordinates,"circles":circles_coordinates}
    '''


    try:
        acad = get_autocad(create_if_not_exists=True)
        acad.prompt("Hello, Autocad from Python\n")
        print (acad.doc.Name)
        
        sset = acad.get_selection("Selece Polyline-line-circle:\n")
        
        polylines_coordinates = []
        lines_coordinates = []
        circles_coordinates = []
        for indx,obj in enumerate(sset):
            if ("polyline" in str(acad.best_interface(obj)).lower()):
                polyline = _get_polyline_coordinates2d(obj,clean_duplicate,rounding_digits)
                if clean_duplicate:
                    if polyline in polylines_coordinates:
                        continue
                polylines_coordinates.append(polyline)
            elif ("acadline" in str(acad.best_interface(obj)).lower()):
                line = _get_line_coordinates(obj,rounding_digits)
                if clean_duplicate:
                    if line in lines_coordinates:
                        continue
                lines_coordinates.append(line)
            elif ("acadcircle" in str(acad.best_interface(obj)).lower()):
                circle = _get_circle_diameter_coordinates(obj, rounding_digits)
                if clean_duplicate:
                    if circle in circles_coordinates:
                        continue
                circles_coordinates.append(circle)
        results = {"lines":lines_coordinates, "polylines":polylines_coordinates,"circles":circles_coordinates}
        return results
        
    except:
        print("Unexpected error", sys.exc_info()[0])
        raise
    finally:
        acad = None



def _get_polyline_coordinates2d(cadObj, clean_duplicate:'bool' = True, rounding_digits:'int' = ROUNDING):
    polyline = []
    #print (type(obj.Coordinates))
    coordinates = cadObj.Coordinates
    for i in range(0,len(coordinates),2):
        point = (round(coordinates[i],rounding_digits),round(coordinates[i+1],rounding_digits))
        if clean_duplicate:
            if point in polyline:
                continue
        polyline.append(point)

    polyline = tuple(polyline)
    return polyline

def select_polylines_get_coordinates2d(clean_duplicate:'bool' = True,rounding_digits:'int' = ROUNDING)-> 'list[list[tuple(float,float,float)]]' : 
    '''
    Returns the list of selected polylines in autocad.

        Parameters:
                clean_duplicate (bool): True for removing duplicated (points and polylines)
                rounding_digits (int): use to round the coordinates

        Returns:
                polylines (list of tuples of tuples): [((coordinates 2d))]
    '''


    try:
        acad = get_autocad(create_if_not_exists=True)

        acad.prompt("Hello, Autocad from Python\n")
        print (acad.doc.Name)
        
        sset = acad.get_selection("Selece Polyline:\n")
        
        polylines_coordinates = []
        for indx,obj in enumerate(sset):
            if ("polyline" in str(acad.best_interface(obj)).lower()):
                polyline = _get_polyline_coordinates2d(obj,clean_duplicate,rounding_digits)
                if clean_duplicate:
                    if polyline in polylines_coordinates:
                        continue
                polylines_coordinates.append(polyline)
        return polylines_coordinates
        
    except:
        print("Unexpected error", sys.exc_info()[0])
        raise
    finally:
        acad = None


def _get_line_coordinates(cadObj, rounding_digits:'int' = ROUNDING):
    start_point = list(cadObj.StartPoint)
    end_point = list(cadObj.EndPoint)
    start_point = tuple(round(x,rounding_digits) for x in start_point)
    end_point = tuple(round(x,rounding_digits) for x in end_point)
    line = (start_point, end_point)
    return line

def select_lines_get_coordinates3d(clean_duplicate:'bool' = True,rounding_digits:'int' = ROUNDING)-> 'list[tuple(tuple(float,float,float))]' : 
    '''
    Returns the list of selected lines in autocad.

        Parameters:
                clean_duplicate (bool): True for removing duplicated
                rounding_digits (int): use to round the coordinates

        Returns:
                lines (list of tuples): [(start_coordinate3d, end_coordinate3d)]
    '''


    try:
        acad = get_autocad(create_if_not_exists=True)

        acad.prompt("Hello, Autocad from Python\n")
        print (acad.doc.Name)
        
        sset = acad.get_selection("Selece lines:\n")
        
        lines_coordinates = []
        for indx,obj in enumerate(sset):
            if ("acadline" in str(acad.best_interface(obj)).lower()):
                line = _get_line_coordinates(obj,rounding_digits)
                if clean_duplicate:
                    if line in lines_coordinates:
                        continue
                lines_coordinates.append(line)
        return lines_coordinates
        
    except:
        print("Unexpected error", sys.exc_info()[0])
        raise
    finally:
        acad = None


def _get_circle_diameter_coordinates(cadObj, rounding_digits:'int' = ROUNDING):
    center_point = list(cadObj.Center)
    center_point = tuple(round(x,rounding_digits) for x in center_point)
    radius = float(cadObj.Radius)
    circle = (round(2*radius , rounding_digits), center_point)
    return circle

def select_circles_get_coordinates3d(clean_duplicate:'bool' = True,rounding_digits:'int' = ROUNDING) : 
    '''
    Returns the list of selected circles in autocad.

        Parameters:
                clean_duplicate (bool): True for removing duplicated
                rounding_digits (int): use to round the coordinates and diameter

        Returns:
                circles (list of tuples): [(Diameter, coordinate3d)]
    '''


    try:
        acad = get_autocad(create_if_not_exists=True)

        acad.prompt("Hello, Autocad from Python\n")
        print (acad.doc.Name)
        
        sset = acad.get_selection("Selece Circles:\n")
        
        circles_coordinates = []
        for indx,obj in enumerate(sset):
            if ("acadcircle" in str(acad.best_interface(obj)).lower()):
                circle = _get_circle_diameter_coordinates(obj, rounding_digits)
                if clean_duplicate:
                    if circle in circles_coordinates:
                        continue
                circles_coordinates.append(circle)
        return circles_coordinates
        
    except:
        print("Unexpected error", sys.exc_info()[0])
        raise
    finally:
        acad = None


if __name__ == "__main__":
    main()

