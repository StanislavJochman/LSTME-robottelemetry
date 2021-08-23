from cx_Freeze import setup, Executable

executables = [Executable("main.py",icon="../img/LSTME_logo.png")]

setup(
    name="JozefBot Telemetry",
    version = "1.0.0",
    description = 'Telemetry program for JozefBot',
    author = 'Stanislav Jochman',
    options={"build_exe": {"packages":["serial","PyQt5","time","sys","serial.tools.list_ports","time","ui"],
                           "include_files":["../img/gyro.png",
                                            "../img/robot.png",
                                            "../img/LSTME_logo.png"
                                            ]}},
    executables = executables
    )

