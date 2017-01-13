# -*- coding: utf-8 -*-

import os
from pysignfe.xml_sped import *
from pysignfe.nfe.manual_500 import inutnfe_310
from pysignfe.nfe.manual_600 import ESQUEMA_ATUAL

DIRNAME = os.path.dirname(__file__)

class InfInutEnviado(inutnfe_310.InfInutEnviado):
    def __init__(self):
        super(InfInutEnviado, self).__init__()


class InutNFe(inutnfe_310.InutNFe):
    def __init__(self):
        super(InutNFe, self).__init__()
        self.infInut = InfInutEnviado()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'inutNFe_v3.10.xsd'
        

class InfInutRecebido(inutnfe_310.InfInutRecebido):
    def __init__(self):
        super(InfInutRecebido, self).__init__()



class RetInutNFe(inutnfe_310.RetInutNFe):
    def __init__(self):
        super(RetInutNFe, self).__init__()
        self.versao = TagDecimal(nome=u'retInutNFe', codigo=u'DR01', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'3.10', raiz=u'/')
        self.infInut = InfInutRecebido()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retInutNFe_v3.10.xsd'



class ProcInutNFe(inutnfe_310.ProcInutNFe):
    def __init__(self):
        super(ProcInutNFe, self).__init__()
        #
        # Atenção --- a tag ProcInutNFe tem que começar com letra maiúscula, para
        # poder validar no XSD. Os outros arquivos proc, procCancNFe, e procNFe
        # começam com minúscula mesmo
        #
        self.versao = TagDecimal(nome=u'ProcInutNFe', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'3.10', raiz=u'/')
        self.inutNFe = InutNFe()
        self.retInutNFe = RetInutNFe()

        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'procInutNFe_v3.10.xsd'

