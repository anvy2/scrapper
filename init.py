import pandas as pd

import Yahoo
import TOI

document = pd.read_pickle('symbols.pickle')

Yahoo.init(document, 'symbol')
TOI.init(document, 'company')
