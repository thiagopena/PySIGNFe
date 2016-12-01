# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from .Rps import IdentificacaoPrestador, IdentificacaoTomador, IdentificacaoIntermediario, IdentificacaoIntermediarioServico, DadosIntermediario
from .Nfse import CompNfse
from .ConsultarSituacaoLoteRps import ListaMensagemRetorno

import os
DIRNAME = os.path.dirname(__file__)
    
    
class Tomador(IdentificacaoTomador):
    def get_xml(self):
        if self.CpfCnpj.Cpf.valor==u'' and self.CpfCnpj.Cnpj.valor==u'':
            return u''
        xml = XMLNFe.get_xml(self)
        xml += u'<Tomador>'
        xml += self.CpfCnpj.xml
        xml += self.InscricaoMunicipal.xml
        xml += u'</Tomador>'
        return xml
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CpfCnpj.xml  = arquivo
            self.InscricaoMunicipal.xml  = arquivo

    xml = property(get_xml, set_xml)
    
    
class IntermediarioServico(IdentificacaoIntermediario):
    def get_xml(self):        
        xml = XMLNFe.get_xml(self)
        xml += u'<IntermediarioServico>'
        xml += self.CpfCnpj.xml
        xml += self.InscricaoMunicipal.xml
        xml += u'</IntermediarioServico>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CpfCnpj.xml = arquivo
            self.InscricaoMunicipal.xml = arquivo

    xml = property(get_xml, set_xml)
    
            
class ConsultarNfseEnvio(XMLNFe):
    def __init__(self):
        super(ConsultarNfseEnvio, self).__init__()
        self.versao  = TagDecimal(nome=u'ConsultarNfseEnvio', propriedade=u'versao', namespace=NAMESPACE_NFSE, valor=u'1.00', raiz=u'/[nfse]')
        self.Prestador = IdentificacaoPrestador()
        self.NumeroNfse = TagInteiro(nome=u'NumeroNfse', tamanho=[1,15], raiz=u'/[nfse]', obrigatorio=False)
        self.DataInicial = TagData(nome='DataInicial', raiz=u'/[nfse]', obrigatorio=False)
        self.DataFinal = TagData(nome='DataFinal', raiz=u'/[nfse]', obrigatorio=False)
        self.Tomador = Tomador()
        self.IntermediarioServico = IdentificacaoIntermediarioServico()
        
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ConsultarNfseEnvio xmlns="'+ NAMESPACE_NFSE + '">'
        xml += self.Prestador.xml.replace(ABERTURA, u'')
        xml += self.NumeroNfse.xml
        if (self.DataInicial.valor != None and self.DataFinal.valor != None):
            xml += u'<PeriodoEmissao>'
            xml += self.DataInicial.xml
            xml += self.DataFinal.xml
            xml += u'</PeriodoEmissao>'
        xml += self.Tomador.xml
        xml += self.IntermediarioServico.xml
        
        xml += u'</ConsultarNfseEnvio>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Prestador.xml = arquivo
            self.NumeroNfse.xml = arquivo
            self.DataInicial.xml = arquivo
            self.DataFinal.xml = arquivo
            self.Tomador.xml = arquivo
            self.IntermediarioServico.xml = arquivo
            
    xml = property(get_xml, set_xml)
    
    
    
class ConsultarNfseResposta(XMLNFe):
    def __init__(self):
        super(ConsultarNfseResposta, self).__init__()
        self.CompNfse = []
        self.ListaMensagemRetorno = ListaMensagemRetorno()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<ConsultarNfseResposta xmlns="'+ NAMESPACE_NFSE + '">'
        if len(self.ListaMensagemRetorno.MensagemRetorno) != 0:
            xml += self.ListaMensagemRetorno.xml.replace(ABERTURA, u'')
        else:
            xml += u'<ListaNfse>'
            for c in self.CompNfse:
                xml += tira_abertura(c.xml)
            
            xml += u'</ListaNfse>'
            
        xml += u'</ConsultarNfseResposta>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CompNfse = self.le_grupo('[nfse]//GerarNfseResposta/CompNfse', CompNfse)
            self.ListaMensagemRetorno.xml = arquivo
            
    xml = property(get_xml, set_xml)