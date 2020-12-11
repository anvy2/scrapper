import pandas as pd
import sys
import threading
import Yahoo
import TOI

argumentList = sys.argv
root_dir = argumentList[1]
source_list = argumentList[2]
root_dir = root_dir.split('=')
source_list = source_list.split('=')
root_dir[0] = root_dir[0][2:]
source_list[0] = source_list[0][2:]
if len(root_dir) != 2 or len(source_list) != 2:
    sys.exit('Malformed arguments')
print(root_dir, source_list)
comm = {
    root_dir[0]: root_dir[1],
    source_list[0]: source_list[1]
}

try:
    document = pd.read_pickle('symbols.pickle')
    destination = comm['root_dir']
    # Yahoo.init(document, 'symbol')
    # TOI.init(document, 'company')

    x = threading.Thread(target=Yahoo.init, args=(document, 'symbol',))
    y = threading.Thread(target=TOI.init, args=(document, 'company',))
    x.start()
    y.start()
except:
    sys.exit('Malformed arguments')
