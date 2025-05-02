from flet import * 
import flet as ft
from io import open  # Explicitly import the built-in open function
import subprocess
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
        """
        self.name = name
        self.datas_ = datas_
        self.page = page

    def display(self):
        def main(page: ft.Page):
            # Add a monospaced text area without scrolling
            shell_output = ft.TextField(
                value=self.datas_,
                multiline=True,  # Enable multiline text
                read_only=True,  # Make the text field read-only
                expand=True,  # Expand to fill available space
                text_style=ft.TextStyle(
                    font_family="Courier New",  # Monospaced font
                    size=14,
                ),
            )
            page.add(
                ft.Text(f"{self.name}", size=20, weight="bold"),
                shell_output,
                ft.Text(f"{self.page}", size=14, italic=True),
            )
        ft.app(target=main)

class Ntps_(ScreenOpp,Dam, Dictor):
    def Ntps(data_file_creation):
       file = open(data_file_creation+'.Ntps','w')
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

class alg:
    def create(algs):  
           # Write the raw input string to the file
        with open('algorithms.Ntps', 'w') as file:
            file.write(algs)  # Write the input string as-is
        return algs  # Return the input string for verification # Store the input string for later use
class a:
    def __init__(self):
        self.a = int # Assign an integer value instead of a type

class b:
    def __init__(self):
        self.b = 0  # Assign an integer value instead of a type

class c:
    def __init__(self):
        self.c = str
class execute_alg:
    def __init__(self):
        with open('algorithms.Ntps', 'r') as file: 
            content = file.read() 

        with open('algorithms.Ntps', 'w') as file:  
            for char in content: 
                if char.isdigit():  
                    file.write('a\n')
                elif char == 0:  
                    file.write('b\n')
                elif char.isalpha(): 
                    file.write('c\n')
                elif char in ['+', '-', '*', '/']:  #
                    file.write(f'{char}\n')
class Ntps_obj:
    def __init__():
        __all__=['execution_file.py','algorithms.Ntps']
        self.algorithms = 'algorithms.Ntps'
        self.execution_file = 'execution_file.py'
        Ntps:object = '.Ntps'
        Ntps:object = type('Ntps', (object,), {})
        def __repr__():
            return Ntps(object)
        def __call__():
            __call__ = True
class shell:
    def __init__(self):
        from subprocess import Popen
        a = int
        b = str
        c = 0
        try:
            # Write to the file first
            with open('shell.py', 'w') as file:
                # Read and write contents of execution_file.py
                with open('execution_file.py', 'r') as files:
                    for data in files.read():
                        if data.isdigit():  # Check if the content is a digit
                            file.write('a')
                        elif data in ['+', '-', '*', '/']:  # Check for operators
                            file.write(f'{content}')
                    #file.write(files.read())  # Write contents of execution_file.py
                
                # Read and write contents of algorithms.Ntps
                with open('algorithms.Ntps', 'r') as filen:
                    for content in filen.read():  # Check if the content is an alphabetic character
                        if content.isdigit():  # Check if the content is a digit
                            file.write('int')
                        elif content.isalpha():
                            file.write('str')  # Check if the content is an alphabetic character
                        elif content in ['+', '-', '*', '/']:  # Check for operators
                            file.write(f'{content}')
                  # Default to 'c' for other cases


        except OSError as e:
            print('Error:', e)
    def window():
        with open('shell.py', 'r') as file:
            content = file.read()  # Read the file content once
            # Pass content to ScreenOpp with a shell-like appearance
            ScreenOpp(name="Shell Output", datas_=content, page="End of Shell").display()

