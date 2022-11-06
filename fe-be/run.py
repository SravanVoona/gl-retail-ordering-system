from ecommerce import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
