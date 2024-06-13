This project (SIC_System_Software) is a commandline driven implementation of SIC System Software
(Assembler, Loader, Simulator) as described in the textbook System Software by Leland L. Beck,
3rd Edition.  Only basic SIC functionality is provided.  Implementation of SIC/XE features was
not attempted. This project was developed in PyCharm 2023.3.3 (Community Edition) using Python 3.12.
It is meant to be run inside the Pycharm IDE and has not been tested elsewhere.  Runnable files
are SIC_Assembler > sic_assembler.py for the assembler and SIC_Simulator > sic_simulator.py for
the simulator.  Examples of SIC assembly programs are provided in the Assembly Code folder.
These program examples have been taken from the book, and some have been modified for testing
purposes.  Some of these assembly programs run to completion successfully, and others fail
deliberately.  The assembly program, ReadWrite.asm, exercises the simulated peripheral devices
(both input and output).  SIC_DEFAULT_WORKING_DIRECTORY must be configured properly before running
either the assembler or the simulator.  Configuration files are found here:
SIC_Assembler > sic_configuration.py and here: SIC_Simulator > sic_configuration.py.
Extensive development notes can be found in the README folder.


ASSEMBLER RUNNABLE
==================
SIC_Assembler > sic_assembler.py

ASSEMBLER CONFIGURATION
=======================
SIC_Assembler > sic_configuration.py


SIMULATOR RUNNABLE
==================
SIC_Simulator > sic_simulator.py

SIMULATOR CONFIGURATION
=======================
SIC_Simulator > sic_configuration.py


Implementation of SIC System Software (Assembler, Loader, Simulator) as described in the textbook System Software by Leland L. Beck, 3rd Edition