# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from .Rps import IdentificacaoRps, DadosServico, DadosConstrucaoCivil, DadosTomador, IdentificacaoPrestador, \
    Endereco, Contato, IdentificacaoIntermediarioServico
from .CancelamentoNfse import CancelamentoNfse
from .SubstituicaoNfse import SubstituicaoNfse

import os
DIRNAME = os.path.dirname(__file__)

class IdentificacaoOrgaoGerador(XMLNFe):
    def __init__(self):
        super(IdentificacaoOrgaoGerador, self).__init__()
        self.CodigoMunicipio = TagInteiro(nome=u'CodigoMunicipio', tamanho=[1,7], raiz=u'/[nfse]')
        self.Uf = TagCaracter(nome=u'Uf', tamanho=[1,2], raiz=u'/[nfse]')
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<IdentificacaoOrgaoGerador>'
        xml += self.CodigoMunicipio.xml
        xml += self.Uf.xml
        xml += u'</IdentificacaoOrgaoGerador>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CodigoMunicipio.xml    = arquivo
            self.Uf.xml  = arquivo

    xml = property(get_xml, set_xml)
        

class DadosPrestador(XMLNFe):
    def __init__(self):
        super(DadosPrestador, self).__init__()
        self.IdentificacaoPrestador = IdentificacaoPrestador()
        self.RazaoSocial = TagCaracter(nome=u'RazaoSocial', tamanho=[1, 115], raiz=u'/[nfse]')
        self.NomeFantasia = TagCaracter(nome=u'NomeFantasia', tamanho=[1, 60], raiz=u'/[nfse]')
        self.Endereco = Endereco()
        self.Contato = Contato()
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<DadosPrestador>'
        xml += self.IdentificacaoPrestador.xml
        xml += self.RazaoSocial.xml
        xml += self.NomeFantasia.xml
        xml += self.Endereco.xml
        xml += self.Contato.xml
        xml += u'</DadosPrestador>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.IdentificacaoPrestador.xml = arquivo
            self.RazaoSocial.xml = arquivo
            self.NomeFantasia.xml = arquivo
            self.Endereco.xml = arquivo
            self.Contato.xml = arquivo

    xml = property(get_xml, set_xml)
        
        
class InfNfse(XMLNFe):
    def __init__(self):
        super(InfNfse, self).__init__()
        self.Id = TagCaracter(nome=u'InfNfse', propriedade=u'Id', raiz=u'/[nfse]')
        self.Numero = TagInteiro(nome=u'Numero', tamanho=[1,15], raiz=u'/[nfse]')
        self.CodigoVerificacao = TagCaracter(nome=u'CodigoVerificacao', tamanho=[1,9], raiz=u'/[nfse]')
        self.DataEmissao = TagDataHora(nome=u'DataEmissao', raiz=u'/[nfse]')
        self.IdentificacaoRps = IdentificacaoRps()
        self.DataEmissaoRps = TagData(nome='DataEmissaoRps', raiz=u'/[nfse]')
        self.NaturezaOperacao = TagInteiro(nome=u'NaturezaOperacao', tamanho=[1,2], raiz=u'/[nfse]')
        self.RegimeEspecialTributacao = TagInteiro(nome=u'RegimeEspecialTributacao', tamanho=[1,2], raiz=u'/[nfse]')
        self.OptanteSimplesNacional = TagInteiro(nome=u'OptanteSimplesNacional', tamanho=[1,1], raiz=u'/[nfse]')
        self.IncentivadorCultural = TagInteiro(nome=u'IncentivadorCultural', tamanho=[1,1], raiz=u'/[nfse]')
        self.Competencia = TagData(nome='Competencia', raiz=u'/[nfse]')
        self.NfseSubstituida = TagInteiro(nome=u'NfseSubstituida', tamanho=[1,15], raiz=u'/[nfse]')
        self.OutrasInformacoes = TagCaracter(nome=u'OutrasInformacoes', tamanho=[1, 255], raiz=u'/[nfse]')
        self.Servico = DadosServico()
        self.ValorCredito = TagDecimal(nome=u'ValorCredito', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]')
        self.PrestadorServico = DadosPrestador()
        self.TomadorServico = DadosTomador()
        self.IntermediarioServico = IdentificacaoIntermediarioServico()
        self.OrgaoGerador = IdentificacaoOrgaoGerador()
        self.ConstrucaoCivil = DadosConstrucaoCivil()
        
    def get_xml(self):
        self.Id.valor = u'nfse:' + str(self.IdentificacaoRps.Serie.valor) + str(self.Numero.valor)
        
        xml = XMLNFe.get_xml(self)
        xml += self.Id.xml
        xml += self.Numero.xml
        xml += self.CodigoVerificacao.xml
        xml += self.DataEmissao.xml
        xml += self.IdentificacaoRps.xml
        xml += self.DataEmissaoRps.xml
        xml += self.NaturezaOperacao.xml
        xml += self.RegimeEspecialTributacao.xml
        xml += self.OptanteSimplesNacional.xml
        xml += self.IncentivadorCultural.xml
        xml += self.Competencia.xml
        xml += self.NfseSubstituida.xml
        xml += self.OutrasInformacoes.xml
        xml += self.Servico.xml
        xml += self.ValorCredito.xml
        xml += self.PrestadorServico.xml
        xml += self.TomadorServico.xml
        xml += self.IntermediarioServico.xml
        xml += self.OrgaoGerador.xml
        xml += self.ConstrucaoCivil.xml
                
        xml += u'</InfNfse>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Numero.xml = arquivo
            self.CodigoVerificacao.xml = arquivo
            self.DataEmissao.xml = arquivo
            self.IdentificacaoRps.xml = arquivo
            self.DataEmissaoRps.xml = arquivo
            self.NaturezaOperacao.xml = arquivo
            self.RegimeEspecialTributacao.xml = arquivo
            self.OptanteSimplesNacional.xml = arquivo
            self.IncentivadorCultural.xml = arquivo
            self.Competencia.xml = arquivo
            self.NfseSubstituida.xml = arquivo
            self.OutrasInformacoes.xml = arquivo
            self.Servico.xml = arquivo
            self.ValorCredito.xml = arquivo
            self.PrestadorServico.xml = arquivo
            self.TomadorServico.xml = arquivo
            self.IntermediarioServico.xml = arquivo
            self.OrgaoGerador.xml = arquivo
            self.ConstrucaoCivil.xml = arquivo
            
    xml = property(get_xml, set_xml)   
        

class NFSe(XMLNFe):
    def __init__(self):
        super(NFSe, self).__init__()
        self.InfNfse = InfNfse()
        self.Signature = Signature()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<NFSe>'
        xml += self.InfNfse.xml
        xml += self.Signature.xml
        xml += u'</NFSe>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.InfNfse.xml    = arquivo
            self.Signature.xml = self._le_noh('[nfse]//Rps/sig:Signature')

    xml = property(get_xml, set_xml) 
    
class CompNfse(XMLNFe):
    def __init__(self):
        super(CompNfse, self).__init__()
        self.Nfse = NFSe()
        self.NfseCancelamento = CancelamentoNfse()
        self.NfseSubstituicao = SubstituicaoNfse()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<CompNfse>'
        xml += self.Nfse.xml
        xml += self.NfseCancelamento.xml
        xml += self.NfseSubstituicao.xml
        xml += u'</CompNfse>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Nfse.xml    = arquivo
            self.NfseCancelamento.xml = arquivo
            self.NfseSubstituicao.xml = arquivo

    xml = property(get_xml, set_xml)