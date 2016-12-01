# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from .Rps import LoteRps
from .ConsultarSituacaoLoteRps import ListaMensagemRetorno, ListaMensagemRetornoLote
from .Nfse import CompNfse

import os
DIRNAME = os.path.dirname(__file__)           
            
class GerarNfseEnvio(XMLNFe):
    def __init__(self):
        super(GerarNfseEnvio, self).__init__()
        self.versao  = TagDecimal(nome=u'GerarNfseEnvio', propriedade=u'versao', namespace=NAMESPACE_NFSE, valor=u'1.00', raiz=u'/')
        self.LoteRps = LoteRps()
        self.Signature = Signature()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<GerarNfseEnvio xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.LoteRps.xml.replace(ABERTURA, u'')
        xml += self.Signature.xml
        
        xml += u'</GerarNfseEnvio>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.LoteRps.xml = arquivo
            self.Signature.xml = self._le_noh('//GerarNfseEnvio/sig:Signature')
            
    xml = property(get_xml, set_xml)
    
    
    
class GerarNfseResposta(XMLNFe):
    def __init__(self):
        super(GerarNfseResposta, self).__init__()
        self.NumeroLote = TagInteiro(nome=u'NumeroLote', tamanho=[1, 15], raiz=u'/')
        self.DataRecebimento = TagDataHora(nome=u'DataRecebimento', raiz=u'/')
        self.Protocolo = TagCaracter(nome=u'Protocolo', tamanho=[1,50], raiz=u'/')
       
        self.ListaMensagemRetorno = ListaMensagemRetorno()
        self.ListaMensagemRetornoLote = ListaMensagemRetornoLote()
        self.CompNfse = []
        
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<GerarNfseResposta xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.NumeroLote.xml
        xml += self.DataRecebimento.xml
        xml += self.Protocolo.xml
        
        if len(self.ListaMensagemRetorno.MensagemRetorno) != 0:
            xml += self.ListaMensagemRetorno.xml.replace(ABERTURA, u'')
        elif len(self.ListaMensagemRetornoLote.MensagemRetornoLote) != 0:
            xml += self.ListaMensagemRetornoLote.xml.replace(ABERTURA, u'')
        else:
            xml += u'<ListaNfse>'
            for c in self.CompNfse:
                xml += tira_abertura(c.xml)
            xml += u'</ListaNfse>'
        
        xml += u'</GerarNfseResposta>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.NumeroLote.xml = arquivo
            self.DataRecebimento.xml = arquivo
            self.Protocolo.xml = arquivo
            self.ListaMensagemRetorno.xml = arquivo
            self.ListaMensagemRetornoLote.xml = arquivo
            self.CompNfse = self.le_grupo('[nfse]//GerarNfseResposta/CompNfse', CompNfse)
            
    xml = property(get_xml, set_xml)