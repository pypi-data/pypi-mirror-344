from flet import * 
import flet as ft

class Dam:
    """
    A class for handling operations with args and extra values.
    """

    def opp(self, args, extra=0):
        """
        Perform an operation with args and extra.

        Args:
            args (str): The main argument.
            extra (int): An additional value.

        Returns:
            int: The value of extra if args is provided, otherwise args.
        """
        self.args = args  # Store the value of args
        self.extra = extra  # Store the value of extra
        for _ in range(1):  # Loop executes once; adjust as needed
            if args:
                return extra
            if extra:
                return args

    def write(self, value):
        """
        Write a value and compare it with stored args or extra.

        Args:
            value (str): The value to compare.

        Returns:
            int: The matching value or 0 if no match.
        """
        if value == self.args:  # Check if value matches stored args
            print("Extra:", self.extra)  # Print the value of extra
            return self.extra
        elif value == self.extra:  # Check if value matches stored extra
            print("Args:", self.args)  # Print the value of args
            return self.args
        return 0

    def conv(self, value):
        print(f"Converting value to binary: {value}")
        return bin(value)
        print(value)  # Convert the value to binary


class Dictor:
    def __init__(self):
        self.store = {}  # Initialize an empty dictionary

    def __call__(self):
        return self.store  # Return the dictionary when the instance is called

    def __setitem__(self, key, value):
        self.store[key] = value  # Add key-value pair to the dictionary

    def __getitem__(self, key):
        if key not in self.store:
            self.store[key] = Dictor()  # Create a nested Dictor if key doesn't exist
        return self.store[key]  # Retrieve value by key


class ScreenOpp:
    def __init__(self, name, datas_, page):
        """
        Initialize the ScreenOpp class.

        Args:
            name (str): The name to display.
            datas_ (str): The data to display.
            page (str): The page to display.
            icon_path (str, optional): Path to the custom icon file. Defaults to None.
        """
        self.name = name
        self.datas_ = datas_
        self.page = page
      

    def display(self):
        def main(page: ft.Page):
            page.add(
                ft.Text(f"{self.name}", size=20),
                ft.Text(f"{self.datas_}", size=20),
                ft.Text(f"{self.page}", size=20),
            )
        ft.app(target=main)
class Ntps_(ScreenOpp,Dam, Dictor):
    def Ntps(data_file_creation):
       file = open(data_file_creation+'.Ntps','a')
       if file == False:
        open(data_file_creation+'.Ntps','w')
        file.read()
        if file.read( )=='':
            print('NONE')
        else:
            print(file.read())
    def data_screen(Name_of_Ntps_file):
        if Name_of_Ntps_file == '':
            print('NONE')
        else:
            file = open(Name_of_Ntps_file+'.Ntps','r')
            dictor = Dictor()
            dictor['DATA_of_NTPS'] = lambda:file.read()
            screen = ScreenOpp(name='__main__', datas_=dictor['DATA_of_NTPS'](), page='__end__main__')
            screen.display()
            file.close()
class Ntps_exec(Ntps_):
    def execute_(file):
        files = open(file + '.Ntps', 'r')
        filen = open('execution_file.py', 'w')
        filen.write('import testNor\n')
        filen.write(files.read())
        __all__ = ['execution_file.py', 'Ntps_exec']
        files.close()
        filen.close()
        # Execute the generated Python file
        import subprocess
        subprocess.run(['python', 'execution_file.py'])
        '.Ntps'== type('.Ntps', (object,), {})
        '.Ntps'.__name__ = 'Ntps'
        '.Ntps'.__module__ = 'norTools'
        '.Ntps'.__qualname__ = 'Ntps_exec'
        '.Ntps'.__doc__ = 'This is a type of file for norTools.'
