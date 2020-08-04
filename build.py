import os
import nsist

cfg_file= './installer.cfg'
dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(dir)
nsist.main([cfg_file])