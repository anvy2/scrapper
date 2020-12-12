import pandas as pd
import sys
import threading
import Yahoo
import TOI
import os

import sys

argumentList = sys.argv
root_dir = argumentList[1]
source_list = argumentList[2]
root_dir = root_dir.split('=')
source_list = source_list.split('=')
root_dir[0] = root_dir[0][2:]
source_list[0] = source_list[0][2:]
if len(root_dir) != 2 or len(source_list) != 2:
    sys.exit('Malformed arguments')


Comm = {
    root_dir[0]: root_dir[1],
    source_list[0]: source_list[1]
}
location = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(location, 'symbols.pickle')
print(filepath)
try:
    try:
        document = pd.read_pickle(filepath)
    except:
        sys.exit("error reading in pickle file")
    destination = Comm['root_dir']
    x = threading.Thread(target=Yahoo.init, args=(
        document, 'symbol', destination,))
    y = threading.Thread(target=TOI.init, args=(
        document, 'company', destination,))
    x.start()
    y.start()
except:
    sys.exit('Malformed arguments!')
