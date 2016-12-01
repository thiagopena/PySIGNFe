# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from .Rps import IdentificacaoPrestador, IdentificacaoRps
from .Nfse import CompNfse
from .ConsultarSituacaoLoteRps import ListaMensagemRetorno

import os
DIRNAME = os.path.dirname(__file__)
    
            
class ConsultarNfseRpsEnvio(XMLNFe):
    def __init__(self):
        super(ConsultarNfseRpsEnvio, self).__init__()
        self.versao  = TagDecimal(nome=u'ConsultarNfseRpsEnvio', propriedade=u'versao', namespace=NAMESPACE_NFSE, valor=u'1.00', raiz=u'/')
        self.IdentificacaoRps = IdentificacaoRps()
        self.Prestador = IdentificacaoPrestador()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ConsultarNfseRpsEnvio xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.IdentificacaoRps.xml.replace(ABERTURA, u'')
        xml += self.Prestador.xml.replace(ABERTURA, u'')
        
        xml += u'</ConsultarNfseRpsEnvio>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.IdentificacaoRps.xml = arquivo
            self.Prestador.xml = arquivo
            
    xml = property(get_xml, set_xml)
    
    
    
class ConsultarNfseRpsResposta(XMLNFe):
    def __init__(self):
        super(ConsultarNfseRpsResposta, self).__init__()
        self.CompNfse = CompNfse()
        self.ListaMensagemRetorno = ListaMensagemRetorno()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ConsultarNfseRpsResposta xmlns="'+ NAMESPACE_NFSE + '">'
        if len(self.ListaMensagemRetorno.MensagemRetorno) != 0:
            xml += self.ListaMensagemRetorno.xml.replace(ABERTURA, u'')
        else:
            xml += self.CompNfse.xml
        
        xml += u'</ConsultarNfseRpsResposta>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CompNfse.xml = arquivo
            self.ListaMensagemRetorno.xml = arquivo
            
    xml = property(get_xml, set_xml)