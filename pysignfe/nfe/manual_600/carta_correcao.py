# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from pysignfe.nfe.manual_600 import ESQUEMA_ATUAL
from pysignfe.nfe.manual_500 import carta_correcao

import os

DIRNAME = os.path.dirname(__file__)


class DetEventoCCe(carta_correcao.DetEventoCCe):
    def __init__(self):
        super(DetEventoCCe, self).__init__()


class InfEventoEnviadoCCe(carta_correcao.InfEventoEnviadoCCe):
    def __init__(self):
        super(InfEventoEnviadoCCe, self).__init__()
        self.detEvento = DetEventoCCe()
        
class EventoCCe(carta_correcao.EventoCCe):
    def __init__(self):
        super(EventoCCe, self).__init__()
        self.versao    = TagDecimal(nome=u'evento', codigo=u'HP05', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'1.00', raiz=u'/')
        self.infEvento = InfEventoEnviadoCCe()


class EnvEventoCCe(carta_correcao.EnvEventoCCe):
    def __init__(self):
        super(EnvEventoCCe, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'envCCe_v1.00.xsd'
    
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
            self.evento = self.le_grupo('//envEvento/evento', EventoCCe)
            
    xml = property(get_xml, set_xml)


class InfEventoRecebidoCCe(carta_correcao.InfEventoRecebidoCCe):
    def __init__(self):
        super(InfEventoRecebidoCCe, self).__init__()
        

class RetEventoCCe(carta_correcao.RetEventoCCe):
    def __init__(self):
        super(RetEventoCCe, self).__init__()
        self.infEvento = InfEventoRecebidoCCe()
        

class RetEnvEventoCCe(carta_correcao.RetEnvEventoCCe):
    def __init__(self):
        super(RetEnvEventoCCe, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retEnvCCe_v1.00.xsd'
    
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
            self.retEvento = self.le_grupo('//retEnvEvento/retEvento', RetEventoCCe)
            
            # Monta o dicionário dos retornos
            for ret in self.retEvento:
                self.dic_retEvento[ret.infEvento.chNFe.valor] = ret

    xml = property(get_xml, set_xml)
    

class ProcEventoNFeCCe(carta_correcao.ProcEventoNFeCCe):
    def __init__(self):
        super(ProcEventoNFeCCe, self).__init__()
        self.evento = EventoCCe()
        self.retEvento = RetEventoCCe()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'procCCeNFe_v1.00.xsd'
