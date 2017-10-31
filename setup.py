from distutils.core import setup
import py2exe

#setup(windows=["Attendance.py"])  # without icon

setup(
    windows = [
        {
            "script": "MailingClient.py"
        }
    ],

    options = {"py2exe": {"compressed": 1,
                       "optimize": 2,
                       "packages": ["email",
                                    ],
                       "excludes": ["MySQLdb", "Tkconstants", "Tkinter", 
"tcl",
                                    "orm.adapters.pgsql", 
"orm.adapters.mysql"
                       ],
                       "dll_excludes": ["tcl84.dll", "tk84.dll", 
"wxmsw26uh_vc.dll"]
                       }
           },
)
