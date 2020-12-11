def get_map(symbol, column):
    keys = list(symbol[column])
    value = list(symbol['symbol'])
    symbols = {}
    for i in range(len(keys)):
        symbols[keys[i]] = value[i]
    return symbols
