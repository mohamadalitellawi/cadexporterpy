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

def select_polylines_get_coordinates2d(clean_duplicate:'bool' = True,rounding_digits:'int' = ROUNDING)-> 'list[list[tuple(float,float,float)]]' : 
    '''
    Returns the list of selected polylines in autocad.

        Parameters:
                clean_duplicate (bool): True for removing duplicated (points and polylines)
                rounding_digits (int): use to round the coordinates

        Returns:
                polylines (list of tuples): [(start_coordinate3d, end_coordinate3d)]
    '''


    try:
        acad = get_autocad(create_if_not_exists=True)

        acad.prompt("Hello, Autocad from Python\n")
        print (acad.doc.Name)
        
        sset = acad.get_selection("Selece Polyline:\n")
        
        polylines_coordinates = []
        for indx,obj in enumerate(sset):
            if ("polyline" in str(acad.best_interface(obj)).lower()):
                polyline = []
                #print (type(obj.Coordinates))
                coordinates = obj.Coordinates
                for i in range(0,len(coordinates),2):
                    point = (round(coordinates[i],rounding_digits),round(coordinates[i+1],rounding_digits))
                    if clean_duplicate:
                        if point in polyline:
                            continue
                    polyline.append(point)

                polyline = tuple(polyline)
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
                print(obj.Handle)
                start_point = list(obj.StartPoint)
                end_point = list(obj.EndPoint)
                start_point = tuple(round(x,rounding_digits) for x in start_point)
                end_point = tuple(round(x,rounding_digits) for x in end_point)
                line = (start_point, end_point)
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
                center_point = list(obj.Center)
                center_point = tuple(round(x,rounding_digits) for x in center_point)
                radius = float(obj.Radius)
                circle = (round(2*radius , rounding_digits), center_point)
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

