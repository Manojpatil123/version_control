

from version import get_version
import os
import flask
app = Flask(__name__)
PASS=os.environ['PASS']


@app.route('/')
def version():

   print(PASS)
    
if __name__ == '__main__':
    app.run(port=80,debug=True)

