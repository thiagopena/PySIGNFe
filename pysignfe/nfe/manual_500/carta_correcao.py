# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from pysignfe.nfe.manual_500 import ESQUEMA_ATUAL
from .evento_base import DetEvento, InfEventoEnviado, Evento, EnvEvento, InfEventoRecebido, RetEvento, RetEnvEvento, ProcEventoNFe

import os

DIRNAME = os.path.dirname(__file__)

CONDICAO_USO = u'A Carta de Correcao e disciplinada pelo paragrafo 1o-A do art. 7o do Convenio S/N, de 15 de dezembro de 1970 e pode ser utilizada para regularizacao de erro ocorrido na emissao de documento fiscal, desde que o erro nao esteja relacionado com: I - as variaveis que determinam o valor do imposto tais como: base de calculo, aliquota, diferenca de preco, quantidade, valor da operacao ou da prestacao; II - a correcao de dados cadastrais que implique mudanca do remetente ou do destinatario; III - a data de emissao ou de saida.'

class DetEventoCCe(DetEvento):
    def __init__(self):
        super(DetEventoCCe, self).__init__()
        self.versao     = TagDecimal(nome=u'detEvento'  , codigo=u'HP18', propriedade=u'versao', valor=u'1.00', raiz=u'/')
        self.descEvento = TagCaracter(nome=u'descEvento', codigo=u'HP19', tamanho=[ 5,  60, 5], raiz=u'//infEvento/detEvento',valor=u'Carta de Correcao')
        self.xCorrecao = TagCaracter(nome=u'xCorrecao', codigo=u'HP20', tamanho=[15, 1000, 15], raiz=u'//infEvento/detEvento')
        self.xCondUso = TagCaracter(nome=u'xCondUso', codigo=u'HP20a', raiz=u'//detEvento', valor=CONDICAO_USO)

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.versao.xml
        xml += self.descEvento.xml
        xml += self.xCorrecao.xml
        xml += self.xCondUso.xml
        xml += '</detEvento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo
            self.descEvento.xml = arquivo
            self.xCorrecao.xml = arquivo
            self.xCondUso.xml = arquivo

    xml = property(get_xml, set_xml)
    

class InfEventoEnviadoCCe(InfEventoEnviado):
    def __init__(self):
        super(InfEventoEnviadoCCe, self).__init__()
        self.detEvento = DetEventoCCe()
        self.tpEvento.valor = '110110'

    
class EventoCCe(Evento):
    def __init__(self):
        super(EventoCCe, self).__init__()
        self.infEvento = InfEventoEnviado()
        self.caminho_esquema = os.path.join(DIRNAME, 'schema/', ESQUEMA_ATUAL + '/')
        self.arquivo_esquema = 'CCe_v1.00.xsd'


class EnvEventoCCe(EnvEvento):
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


class InfEventoRecebidoCCe(InfEventoRecebido):
    def __init__(self):
        super(InfEventoRecebidoCCe, self).__init__()
       

class RetEventoCCe(RetEvento):
    def __init__(self):
        super(RetEventoCCe, self).__init__()
    
    
class RetEnvEventoCCe(RetEnvEvento):
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
    

class ProcEventoNFeCCe(ProcEventoNFe):
    def __init__(self):
        super(ProcEventoNFeCCe, self).__init__()
        self.evento = EventoCCe()
        self.retEvento = RetEventoCCe()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'procCCeNFe_v1.00.xsd'

