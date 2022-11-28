

from version import get_version
import os
import flask



def version():
   PASS=os.environ.get('PASSWORD')

   print(PASS)
    
if __name__ == '__main__':
    version()

