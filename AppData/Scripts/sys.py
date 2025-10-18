import sys as __surely_not_even_close_to_sys

# This is a hack that allows us to overwrite the default beavhiour of the sys module.
# By hijacking the import of sys on import, we can inject custom paths without having 
# to rely on any order of init that is the big problem with any current teached approach.

def _setup_path_from_packagefolder():
    import os, re
    from sys import path

    def replace_var(match):
        var_name = match.group(1)
        if len( env_naming := var_name.split("||") ) == 2:
            return os.environ.get( env_naming[0], env_naming[1] )
        else:
            return os.environ[env_naming[0]]

    with open(".packagefolder", "a+t") as package_folder_file:
        # Lets read the .packagefolder and add specified elements. 
        # Monkeybrain uv run mb init.files will create this, otherwise it will simply be empty.
        package_folder_file.seek(0)
        for _line in reversed( package_folder_file.readlines() ):
            line = _line.strip()
            if not line: continue # skip empty lines
            if line.startswith("#"): continue # skip comments
            try:
                enved_line = re.sub(r"\$\{([^}]+)\}", replace_var, line)
            except KeyError:
                continue

            if enved_line in path: continue

            # ok, now insert.
            path.insert(0, enved_line )


_setup_path_from_packagefolder()
del _setup_path_from_packagefolder

for module_name in dir( __surely_not_even_close_to_sys ):
    # If we would just import *, we would not import all modules but only ones not preficed with _
    locals()[ module_name ] = getattr( __surely_not_even_close_to_sys, module_name )

# Some cleanup.
del __surely_not_even_close_to_sys