import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/pc/projects/Intelligent-mutli-Model-Robot-agent/install/wheel-control'
