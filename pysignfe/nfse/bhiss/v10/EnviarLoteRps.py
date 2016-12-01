# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from .Rps import *
from .ConsultarSituacaoLoteRps import ListaMensagemRetorno

import os
DIRNAME = os.path.dirname(__file__)

            
class EnviarLoteRpsEnvio(XMLNFe):
    def __init__(self):
        super(EnviarLoteRpsEnvio, self).__init__()
        self.versao  = TagDecimal(nome=u'EnviarLoteRpsEnvio', propriedade=u'versao', namespace=NAMESPACE_NFSE, valor=u'1.00', raiz=u'/')
        self.LoteRps = LoteRps()
        self.Signature = Signature()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<EnviarLoteRpsEnvio xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.LoteRps.xml.replace(ABERTURA, u'')
        xml += self.Signature.xml
        xml += u'</EnviarLoteRpsEnvio>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.LoteRps.xml = arquivo
            self.Signature.xml = self._le_noh('//EnviarLoteRpsEnvio/sig:Signature')
            
    xml = property(get_xml, set_xml)
    

class EnviarLoteRpsResposta(XMLNFe):
    def __init__(self):
        super(EnviarLoteRpsResposta, self).__init__()
        self.NumeroLote = TagInteiro(nome=u'NumeroLote', tamanho=[1,15], raiz=u'/')
        self.DataRecebimento = TagDataHora(nome=u'DataRecebimento', raiz=u'/')
        self.Protocolo = TagCaracter(nome=u'Protocolo', tamanho=[1,50], raiz=u'/')
        self.ListaMensagemRetorno = ListaMensagemRetorno()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<EnviarLoteRpsResposta xmlns="'+ NAMESPACE_NFSE + '">'
        if len(self.ListaMensagemRetorno.MensagemRetorno) != 0:
            xml += self.ListaMensagemRetorno.xml.replace(ABERTURA, u'')
        else:
            xml += self.NumeroLote.xml
            xml += self.DataRecebimento.xml
            xml += self.Protocolo.xml
        
        xml += u'</EnviarLoteRpsResposta>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.NumeroLote.xml = arquivo
            self.DataRecebimento.xml = arquivo
            self.Protocolo.xml = arquivo
            self.ListaMensagemRetorno.xml = arquivo
            
    xml = property(get_xml, set_xml)