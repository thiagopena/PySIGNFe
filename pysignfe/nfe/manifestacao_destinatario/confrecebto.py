# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from pysignfe.nfe.manifestacao_destinatario import ESQUEMA_ATUAL

#from pysignfe.nfe.manual_401 import cancnfe_evento as Evento
from pysignfe.nfe.manual_500.evento_base import DetEvento, InfEventoEnviado, Evento, EnvEvento, InfEventoRecebido, RetEvento, RetEnvEvento, ProcEventoNFe

import os
DIRNAME = os.path.dirname(__file__)


MD_CONFIRMACAO_OPERACAO     = u'210200'
MD_DESCONHECIMENTO_OPERACAO = u'210220'
MD_OPERACAO_NAO_REALIZADA   = u'210240'
MD_CIENCIA_OPERACAO         = u'210210'

MD_DESCEVENTO = {
    MD_CONFIRMACAO_OPERACAO: 'Confirmacao da Operacao',
    MD_CIENCIA_OPERACAO: 'Ciencia da Operacao',
    MD_DESCONHECIMENTO_OPERACAO: 'Desconhecimento da Operacao',
    MD_OPERACAO_NAO_REALIZADA: 'Operacao nao Realizada',
}


class DetEventoConfRecebimento(DetEvento):
    def __init__(self):
        super(DetEventoConfRecebimento, self).__init__()
        self.versao     = TagDecimal(nome=u'detEvento'  , codigo=u'HP18', propriedade=u'versao', valor=u'1.00', raiz=u'/')
        self.descEvento = TagCaracter(nome=u'descEvento', codigo=u'HP19', tamanho=[ 5,  60, 5], raiz=u'//infEvento/detEvento')
        self.xJust = TagCaracter(nome='xJust'  , codigo='HP20', tamanho=[15, 255]   , raiz='//detEvento', obrigatorio=False)

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.versao.xml
        xml += self.descEvento.xml

        #
        # A justificativa só deve ser enviada no evento MD_OPERACAO_NAO_REALIZADA
        #
        if self.descEvento.valor == MD_DESCEVENTO[MD_OPERACAO_NAO_REALIZADA]:
            xml += self.xJust.xml

        xml += '</detEvento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo
            self.descEvento.xml = arquivo
            self.xJust.xml = arquivo

    xml = property(get_xml, set_xml)
    

class InfEventoEnviadoConfRecebimento(InfEventoEnviado):
    def __init__(self):
        super(InfEventoEnviadoConfRecebimento, self).__init__()
        self.detEvento  = DetEventoConfRecebimento()
    
    
class EventoConfRecebimento(Evento):
    def __init__(self):
        super(EventoConfRecebimento, self).__init__()
        self.infEvento = InfEventoEnviadoConfRecebimento()
        self.caminho_esquema = os.path.join(DIRNAME, 'schema/', ESQUEMA_ATUAL + '/')
        self.arquivo_esquema = 'confRecebto_v1.00.xsd'
    

class  EnvEventoConfRecebimento(EnvEvento):
    def __init__(self):
        super(EnvEventoConfRecebimento, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'envConfRecebto_v1.00.xsd'

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
            self.versao.xml = arquivo
            self.idLote.xml = arquivo
            self.evento     = self.le_grupo('//envEvento/evento', EventoConfRecebimento)
            
    xml = property(get_xml, set_xml)


class InfEventoRecebidoConfRecebimento(InfEventoRecebido):
    def __init__(self):
        super(InfEventoRecebidoConfRecebimento, self).__init__()
        

class RetEventoConfRecebimento(RetEvento):
    def __init__(self):
        super(RetEventoConfRecebimento, self).__init__()
        self.infEvento = InfEventoRecebidoConfRecebimento()

    
class RetEnvEventoConfRecebimento(RetEnvEvento):
    def __init__(self):
        super(RetEnvEventoConfRecebimento, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, 'schema/', ESQUEMA_ATUAL + '/')
        self.arquivo_esquema = 'retEnvConfRecebto_v1.00.xsd'
    
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
            self.retEvento = self.le_grupo('//retEnvEvento/retEvento', RetEventoConfRecebimento)
            
            # Monta o dicion?rio dos retornos
            for ret in self.retEvento:
                self.dic_retEvento[ret.infEvento.chNFe.valor] = ret
            
    xml = property(get_xml, set_xml)


class ProcEventoNFeConfRecebimento(ProcEventoNFe):
    def __init__(self):
        super(ProcEventoNFeConfRecebimento, self).__init__()
        self.evento = EventoConfRecebimento()
        self.retEvento = RetEventoConfRecebimento()
        self.caminho_esquema = os.path.join(DIRNAME, 'schema', ESQUEMA_ATUAL + '/')
        self.arquivo_esquema = 'procConfRecebtoNFe_v1.00.xsd'
