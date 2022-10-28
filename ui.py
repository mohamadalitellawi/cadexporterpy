from rich import print
from rich import print_json
from rich import inspect
import business as bs
from business.column import test as column_test
from business.column import get_revit_columns
from helpers.common import export_dict_to_file

from business import SETTINGS, TEMP_PATH

class App:
    def __init__(self) -> None:
        self.out_file_name = TEMP_PATH
        self.out_objects = bs.OUTPUT

    def startup(self):        
        # print the greeting at startup
        self.greeting()
        print()

    def greeting(self):
        print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-")
        print("~~~~~~ [bold yellow]Welcome to Autocad Exporter App (by Abo Akram)![/bold yellow] ~~~~~~")
        print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-")
        print("~~~~~~ 221028 ~~~~~~\n")


    def menu_header(self):
        print("--------------------------------")
        print("Please make a selection:")
        print("(R): Repeat this menu")


        print("(A): select and get columns (from polylines, circles)")
        print("(B): select and get open walls (from polylines, lines, arcs)")
        print("(C): select and get closed walls (from polylines)")
        print("(D): select and get floors (from polylines)")

        print("(O): check current objects")
        print("(P): Print objects to json file")

        print("(X): eXit program")

    def menu_error(self):
        print("That's not a valid selection. Please try again.")

    def goodbye(self):
        print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
        print(f"-~-~-~ [bold yellow]Thanks for using this App![/bold yellow] ~-~-~-~")
        print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")


    def run(self):
        # Execute the startup routine - ask for name, print greeting, etc
        self.startup()
        # Start the main program menu and run until the user exits
        self.menu()



    def menu(self):
        self.menu_header()

        # get the user's selection and act on it. This loop will
        # run until the user exits the app
        selection = ""
        while (True):
            selection = input("Selection? ")

            if len(selection) == 0:
                self.menu_error()
                continue

            selection = selection.capitalize()
            if selection[0] == 'X':
                self.goodbye()
                break
            elif selection[0] == 'R':
                self.menu_header()
                continue

            elif selection[0] == 'O':
                try:
                    #print(column_test())
                    print_json(data = bs.OUTPUT)
                except Exception as e:
                    self.menu_error()
                    raise e
                continue


            elif selection[0] == 'P':
                try:
                    print(f'current output file path is {self.out_file_name}')
                    filename = input("Enter File Name with full path <press dot(.) to use current>: ")
                    if len(filename) == 0: continue
                    if filename[0] == ".":
                        filename = self.out_file_name
                    if filename.capitalize()[0] == "X": continue
                    self.out_file_name = filename
                    print(self.out_file_name)
                    export_dict_to_file(filename, self.out_objects)
                except Exception as e:
                    self.menu_error()
                    #raise e
                continue


            elif selection[0] == 'A':
                try:
                    get_revit_columns()
                except Exception as e:
                    self.menu_error()
                    #raise e
                continue

            # elif selection[0] == 'S':
            #     try:
            #         scale = input("Enter Shape Block Scale Factor: ")
            #         if len(scale) == 0: continue
            #         if scale.capitalize()[0] == "X": continue
            #         scale = float(scale)
            #         buisness.SHAPE_SCALE_FACTOR = scale
            #     except Exception as e:
            #         self.menu_error()
            #         #raise e
            #     continue




            # elif selection[0] == 'B':
            #     try:
            #         buisness.send_selectedbars_to_excel()
            #     except Exception as e:
            #         self.menu_error()
            #         #raise e
            #     continue





if __name__ == "__main__":
    app = App()
    app.run()