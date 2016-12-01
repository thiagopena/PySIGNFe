# -*- coding: utf-8 -*-

try:
    unicode = unicode
except NameError:
    # Se 'unicode', utilizando versao Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' esta definido, deve ser Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring