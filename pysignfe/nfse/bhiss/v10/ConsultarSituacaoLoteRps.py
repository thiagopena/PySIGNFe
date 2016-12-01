# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from .Rps import IdentificacaoPrestador, IdentificacaoRps

import os
DIRNAME = os.path.dirname(__file__)

class MensagemRetorno(XMLNFe):
    def __init__(self):
        super(MensagemRetorno, self).__init__()
        self.Codigo = TagCaracter(nome=u'Codigo', tamanho=[1, 4], raiz=u'/[nfse]')
        self.Mensagem = TagCaracter(nome=u'Mensagem', tamanho=[1, 200], raiz=u'/[nfse]')
        self.Correcao = TagCaracter(nome=u'Correcao', tamanho=[0, 200], raiz=u'/[nfse]')
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<MensagemRetorno>'
        xml += self.Codigo.xml
        xml += self.Mensagem.xml
        xml += self.Correcao.xml
        
        xml += u'</MensagemRetorno>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Codigo.xml   = arquivo
            self.Mensagem.xml   = arquivo
            self.Correcao.xml   = arquivo

    xml = property(get_xml, set_xml)
    
    
class MensagemRetornoLote(XMLNFe):
    def __init__(self):
        super(MensagemRetornoLote, self).__init__()
        self.IdentificacaoRps = IdentificacaoRps()
        self.Codigo = TagCaracter(nome=u'Codigo', tamanho=[1, 4], raiz=u'/[nfse]')
        self.Mensagem = TagCaracter(nome=u'Mensagem', tamanho=[1, 200], raiz=u'/[nfse]')
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<MensagemRetornoLote>'
        xml += self.IdentificacaoRps.xml
        xml += self.Codigo.xml
        xml += self.Mensagem.xml
        
        xml += u'</MensagemRetornoLote>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.IdentificacaoRps.xml = arquivo
            self.Codigo.xml   = arquivo
            self.Mensagem.xml   = arquivo

    xml = property(get_xml, set_xml)   
    
    
class ListaMensagemRetornoLote(XMLNFe):
    def __init__(self):
        super(ListaMensagemRetornoLote, self).__init__()
        self.MensagemRetornoLote = []
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ListaMensagemRetornoLote>'
        
        for m in self.MensagemRetornoLote:
            xml += tira_abertura(m.xml)
        
        xml += u'</ListaMensagemRetornoLote>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.MensagemRetornoLote   = self.le_grupo('[nfse]//ListaMensagemRetornoLote/MensagemRetornoLote', MensagemRetornoLote)

    xml = property(get_xml, set_xml)

class ListaMensagemRetorno(XMLNFe):
    def __init__(self):
        super(ListaMensagemRetorno, self).__init__()
        self.MensagemRetorno = []
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ListaMensagemRetorno>'
        
        for m in self.MensagemRetorno:
            xml += tira_abertura(m.xml)
        
        xml += u'</ListaMensagemRetorno>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.MensagemRetorno   = self.le_grupo('[nfse]//ListaMensagemRetorno/MensagemRetorno', MensagemRetorno)

    xml = property(get_xml, set_xml)
            
            
class ConsultarSituacaoLoteRpsEnvio(XMLNFe):
    def __init__(self):
        super(ConsultarSituacaoLoteRpsEnvio, self).__init__()
        self.versao  = TagDecimal(nome=u'ConsultarSituacaoLoteRpsEnvio', propriedade=u'versao', namespace=NAMESPACE_NFSE, valor=u'1.00', raiz=u'/')
        self.Prestador = IdentificacaoPrestador()
        self.Protocolo = TagCaracter(nome=u'Protocolo', tamanho=[ 1,  50], raiz=u'/')
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ConsultarSituacaoLoteRpsEnvio xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.Prestador.xml.replace(ABERTURA, u'')
        xml += self.Protocolo.xml
        
        xml += u'</ConsultarSituacaoLoteRpsEnvio>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Prestador.xml = arquivo
            self.Protocolo.xml = arquivo
            
    xml = property(get_xml, set_xml)
    
    
    
class ConsultarSituacaoLoteRpsResposta(XMLNFe):
    def __init__(self):
        super(ConsultarSituacaoLoteRpsResposta, self).__init__()
        self.NumeroLote = TagInteiro(nome=u'NumeroLote', tamanho=[1, 15], raiz=u'/')
        self.Situacao = TagInteiro(nome=u'Situacao', tamanho=[1, 1], raiz=u'/')
        self.ListaMensagemRetorno = ListaMensagemRetorno()
        
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ConsultarSituacaoLoteRpsResposta xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.NumeroLote.xml
        xml += self.Situacao.xml
        xml += self.ListaMensagemRetorno.xml.replace(ABERTURA, u'')
        
        xml += u'</ConsultarSituacaoLoteRpsResposta>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.NumeroLote.xml = arquivo
            self.Situacao.xml   = arquivo
            self.ListaMensagemRetorno.xml = arquivo
            
    xml = property(get_xml, set_xml)