# -*- coding: utf-8 -*-

import os

from pysignfe.xml_sped import *
from pysignfe.nfe.manual_500 import conscad_310
from pysignfe.nfe.manual_600 import ESQUEMA_ATUAL

DIRNAME = os.path.dirname(__file__)

class InfConsEnviado(conscad_310.InfConsEnviado):
    def __init__(self):
        super(InfConsEnviado, self).__init__()


class ConsCad(conscad_310.ConsCad):
    def __init__(self):
        super(ConsCad, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'consCad_v2.00.xsd'


class Ender(conscad_310.Ender):
    def __init__(self):
        super(Ender, self).__init__()


class InfCadRecebido(conscad_310.InfCadRecebido):
    def __init__(self):
        super(InfCadRecebido, self).__init__()
        self.ender = Ender()


class InfConsRecebido(conscad_310.InfConsRecebido):
    def __init__(self):
        super(InfConsRecebido, self).__init__()

    def get_xml(self):
        return super(InfConsRecebido, self).get_xml()

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.verAplic.xml = arquivo
            self.cStat.xml = arquivo
            self.xMotivo.xml = arquivo
            self.UF.xml = arquivo
            self.IE.xml = arquivo
            self.CNPJ.xml = arquivo
            self.CPF.xml = arquivo
            self.dhCons.xml = arquivo
            self.cUF.xml = arquivo

            self.infCad = self.le_grupo('//retConsCad/infCons/infCad', InfCadRecebido)

    xml = property(get_xml, set_xml)


class RetConsCad(conscad_310.RetConsCad):
    def __init__(self):
        super(RetConsCad, self).__init__()
        self.versao = TagDecimal(nome=u'retConsCad', codigo=u'GR01', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'2.00', raiz=u'/')
        self.infCons = InfConsRecebido()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retConsCad_v2.00.xsd'
