# -*- coding: utf-8 -*-

import os

from pysignfe.nfe.manual_500 import soap_310
from pysignfe.xml_sped import *

DIRNAME = os.path.dirname(__file__)

class NFeCabecMsg(soap_310.NFeCabecMsg):
    def __init__(self):
        super(NFeCabecMsg, self).__init__()


class NFeDadosMsg(soap_310.NFeDadosMsg):
    def __init__(self):
        super(NFeDadosMsg, self).__init__()


class SOAPEnvio(soap_310.SOAPEnvio):
    def __init__(self):
        super(SOAPEnvio, self).__init__()


class SOAPRetorno(soap_310.SOAPRetorno):
    def __init__(self):
        super(SOAPRetorno, self).__init__()

