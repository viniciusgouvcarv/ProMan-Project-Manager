from cx_Freeze import setup, Executable

base = None    

executables = [Executable("proman.py", base=base)]

packages = ["idna", "sys", "psycopg2", "datetime", "tabulate", "time"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "ProMan - Project Manager",
    options = options,
    version = "0.0.3",
    description = 'O seu Gerenciador de Projetos favorito!',
    executables = executables
)
