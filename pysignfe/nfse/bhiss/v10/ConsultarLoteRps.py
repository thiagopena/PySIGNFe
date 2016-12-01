# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from .ConsultarSituacaoLoteRps import ListaMensagemRetorno
from .Rps import IdentificacaoPrestador, IdentificacaoRps
from .Nfse import CompNfse

import os
DIRNAME = os.path.dirname(__file__)
            
            
class ConsultarLoteRpsEnvio(XMLNFe):
    def __init__(self):
        super(ConsultarLoteRpsEnvio, self).__init__()
        self.versao  = TagDecimal(nome=u'ConsultarLoteRpsEnvio', propriedade=u'versao', namespace=NAMESPACE_NFSE, valor=u'1.00', raiz=u'/')
        self.Prestador = IdentificacaoPrestador()
        self.Protocolo = TagCaracter(nome=u'Protocolo', tamanho=[ 1,  50], raiz=u'/')
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ConsultarLoteRpsEnvio xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.Prestador.xml.replace(ABERTURA, u'')
        xml += self.Protocolo.xml
        
        xml += u'</ConsultarLoteRpsEnvio>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Prestador.xml = arquivo
            self.Protocolo.xml = arquivo
            
    xml = property(get_xml, set_xml)
    
    
    
class ConsultarLoteRpsResposta(XMLNFe):
    def __init__(self):
        super(ConsultarLoteRpsResposta, self).__init__()
        self.CompNfse = []
        self.ListaMensagemRetorno = ListaMensagemRetorno()
        
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ConsultarLoteRpsResposta xmlns="'+ NAMESPACE_NFSE + '">'
        if len(self.ListaMensagemRetorno.MensagemRetorno) != 0:
            xml += self.ListaMensagemRetorno.xml.replace(ABERTURA, u'')
        else:
            xml += u'<ListaNfse>'
            for c in self.CompNfse:
                xml += tira_abertura(c.xml)
            xml += u'</ListaNfse>'
        
        xml += u'</ConsultarLoteRpsResposta>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CompNfse = self.le_grupo('[nfse]//ConsultarLoteRpsResposta/CompNfse', CompNfse)
            self.ListaMensagemRetorno.xml = arquivo
            
    xml = property(get_xml, set_xml)