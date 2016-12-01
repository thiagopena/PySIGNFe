# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from .CancelamentoNfse import PedidoCancelamento, CancelamentoNfse
from .ConsultarSituacaoLoteRps import ListaMensagemRetorno

import os
DIRNAME = os.path.dirname(__file__)

class CancelarNfseEnvio(XMLNFe):
    def __init__(self):
        super(CancelarNfseEnvio, self).__init__()
        self.versao  = TagDecimal(nome=u'CancelarNfseEnvio', propriedade=u'versao', namespace=NAMESPACE_NFSE, valor=u'1.00', raiz=u'/[nfse]')
        self.Pedido = PedidoCancelamento()
        
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<CancelarNfseEnvio xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.Pedido.xml.replace(ABERTURA, u'')
        
        xml += u'</CancelarNfseEnvio>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Pedido.xml = arquivo
            
    xml = property(get_xml, set_xml)
    
    
    
class CancelarNfseResposta(XMLNFe):
    def __init__(self):
        super(CancelarNfseResposta, self).__init__()
        self.Cancelamento = CancelamentoNfse()
        self.ListaMensagemRetorno = ListaMensagemRetorno()
        
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<CancelarNfseResposta xmlns="'+ NAMESPACE_NFSE + '">'
        if len(self.ListaMensagemRetorno.MensagemRetorno) != 0:
            xml += self.ListaMensagemRetorno.xml.replace(ABERTURA, u'')
        else:
            xml += self.Cancelamento.xml
            
        xml += u'</CancelarNfseResposta>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Cancelamento.xml = arquivo
            self.ListaMensagemRetorno.xml = arquivo
            
    xml = property(get_xml, set_xml)