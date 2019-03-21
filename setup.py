
#!/usr/bin/env python3

import os

if os.name == 'nt':
    os.system('pip install pymediainfo')
    os.system('pause')
else:
    os.system('pip3 install pymediainfo')

