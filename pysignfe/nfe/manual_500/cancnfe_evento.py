# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from pysignfe.nfe.manual_500 import ESQUEMA_ATUAL
from .evento_base import DetEvento, InfEventoEnviado, Evento, EnvEvento, InfEventoRecebido, RetEvento, RetEnvEvento, ProcEventoNFe

import os

DIRNAME = os.path.dirname(__file__)


class DetEventoCancNFe(DetEvento):
    def __init__(self):
        super(DetEventoCancNFe, self).__init__()
        self.versao     = TagDecimal(nome=u'detEvento'  , codigo=u'HP18', propriedade=u'versao', valor=u'1.00', raiz=u'/')
        self.descEvento = TagCaracter(nome=u'descEvento', codigo=u'HP19', tamanho=[ 5,  60, 5], raiz=u'//infEvento/detEvento',valor=u'Cancelamento')
        self.nProt = TagCaracter(nome='nProt'   , codigo='CP08', tamanho=[15, 15, 15], raiz='//detEvento')
        self.xJust = TagCaracter(nome='xJust'  , codigo='CP09', tamanho=[15, 255]   , raiz='//detEvento')

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.versao.xml
        xml += self.descEvento.xml
        xml += self.nProt.xml
        xml += self.xJust.xml
        xml += '</detEvento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo
            self.descEvento.xml = arquivo
            self.nProt.xml = arquivo
            self.xJust.xml = arquivo

    xml = property(get_xml, set_xml)
    

class InfEventoEnviadoCancNFe(InfEventoEnviado):
    def __init__(self):
        super(InfEventoEnviadoCancNFe, self).__init__()
        self.detEvento = DetEventoCancNFe()
        self.tpEvento.valor = '110111'

    
class EventoCancNFe(Evento):
    def __init__(self):
        super(EventoCancNFe, self).__init__()
        self.versao    = TagDecimal(nome=u'evento', codigo=u'HP05', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'1.00', raiz=u'/')
        self.infEvento = InfEventoEnviadoCancNFe()
        self.Signature = Signature()
        self.caminho_esquema = os.path.join(DIRNAME, 'schema/', ESQUEMA_ATUAL + '/')
        self.arquivo_esquema = 'eventoCancNFe_v1.00.xsd'


class EnvEventoCancNFe(EnvEvento):
    def __init__(self):
        super(EnvEventoCancNFe, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'envEventoCancNFe_v1.00.xsd'

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += self.versao.xml
        xml += self.idLote.xml
        
        for ev in self.evento:
            xml += tira_abertura(ev.xml)
            
        xml += u'</envEvento>'

        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml    = arquivo
            self.idLote.xml    = arquivo
            self.evento = self.le_grupo('//envEvento/evento', EventoCancNFe)
            
    xml = property(get_xml, set_xml)


class InfEventoRecebidoCancNFe(InfEventoRecebido):
    def __init__(self):
        super(InfEventoRecebidoCancNFe, self).__init__()


class RetEventoCancNFe(RetEvento):
    def __init__(self):
        super(RetEventoCancNFe, self).__init__()
        self.versao    = TagDecimal(nome=u'retEvento',propriedade=u'versao', codigo=u'HR10',  namespace=NAMESPACE_NFE, valor=u'1.00', raiz=u'/')
        self.infEvento = InfEventoRecebidoCancNFe()
        self.Signature = Signature()
    
    
class RetEnvEventoCancNFe(RetEnvEvento):
    def __init__(self):
        super(RetEnvEventoCancNFe, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retEnvEventoCancNFe_v1.00.xsd'

    def get_xml(self):
        xml = XMLNFe.get_xml(self)

        xml += ABERTURA
        xml += self.versao.xml
        xml += self.idLote.xml
        xml += self.tpAmb.xml
        xml += self.verAplic.xml
        xml += self.cOrgao.xml
        xml += self.cStat.xml
        xml += self.xMotivo.xml

        for r in self.retEvento:
            xml += tira_abertura(r.xml)
            
        xml += u'</retEnvEvento>'

        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo
            self.idLote.xml = arquivo
            self.tpAmb.xml = arquivo
            self.verAplic.xml = arquivo
            self.cOrgao.xml = arquivo
            self.cStat.xml = arquivo
            self.xMotivo.xml = arquivo
            self.retEvento = self.le_grupo('//retEnvEvento/retEvento', RetEventoCancNFe)
            
            # Monta o dicionário dos retornos
            for ret in self.retEvento:
                self.dic_retEvento[ret.infEvento.chNFe.valor] = ret

    xml = property(get_xml, set_xml)
    

class ProcEventoNFeCancNFe(ProcEventoNFe):
    def __init__(self):
        super(ProcEventoNFeCancNFe, self).__init__()
        self.evento = EventoCancNFe()
        self.retEvento = RetEventoCancNFe()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'procEventoCancNFe_v1.00.xsd'
