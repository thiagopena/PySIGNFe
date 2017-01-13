# -*- coding: utf-8 -*-
import os

from pysignfe.nfe.manual_500 import consstatserv_310
from pysignfe.xml_sped import *
from pysignfe.nfe.manual_600 import ESQUEMA_ATUAL

DIRNAME = os.path.dirname(__file__)

class ConsStatServ(consstatserv_310.ConsStatServ):
    def __init__(self):
        super(ConsStatServ, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'consStatServ_v3.10.xsd'


class RetConsStatServ(consstatserv_310.RetConsStatServ):
    def __init__(self):
        super(RetConsStatServ, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retConsStatServ_v3.10.xsd'
    
