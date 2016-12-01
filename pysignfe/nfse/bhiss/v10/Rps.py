# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
import os
DIRNAME = os.path.dirname(__file__)

class Contato(XMLNFe):
    def __init__(self):
        super(Contato, self).__init__()
        self.Telefone = TagCaracter(nome=u'Telefone', tamanho=[1, 11], raiz=u'/[nfse]', obrigatorio=False)
        self.Email = TagCaracter(nome=u'Email', tamanho=[1, 80], raiz=u'/[nfse]', obrigatorio=False)
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<Contato>'
        xml += self.Telefone.xml
        xml += self.Email.xml
        
        xml += u'</Contato>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Telefone.xml = arquivo
            self.Email.xml = arquivo
            
    xml = property(get_xml, set_xml)

class Endereco(XMLNFe):
    def __init__(self):
        super(Endereco, self).__init__()
        self.Endereco = TagCaracter(nome=u'Endereco', tamanho=[1, 125], raiz=u'/[nfse]', obrigatorio=False)
        self.Numero = TagCaracter(nome=u'Numero', tamanho=[1, 10], raiz=u'/[nfse]', obrigatorio=False)
        self.Complemento = TagCaracter(nome=u'Complemento', tamanho=[1, 60], raiz=u'/[nfse]', obrigatorio=False)
        self.Bairro = TagCaracter(nome=u'Bairro', tamanho=[1, 60], raiz=u'/[nfse]', obrigatorio=False)
        self.CodigoMunicipio = TagInteiro(nome=u'CodigoMunicipio', tamanho=[1, 7], raiz=u'/[nfse]', obrigatorio=False)
        self.Uf = TagCaracter(nome=u'Uf', tamanho=[1, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.Cep = TagInteiro(nome=u'Cep', tamanho=[1, 8], raiz=u'/[nfse]', obrigatorio=False)
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<Endereco>'
        xml += self.Endereco.xml
        xml += self.Numero.xml
        xml += self.Complemento.xml
        xml += self.Bairro.xml
        xml += self.CodigoMunicipio.xml
        xml += self.Uf.xml
        xml += self.Cep.xml
        
        xml += u'</Endereco>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Endereco.xml = arquivo
            self.Numero.xml = arquivo
            self.Complemento.xml = arquivo
            self.Bairro.xml = arquivo
            self.CodigoMunicipio.xml = arquivo
            self.Uf.xml = arquivo
            self.Cep.xml = arquivo

    xml = property(get_xml, set_xml)

class CpfCnpj(XMLNFe):
    def __init__(self):
        super(CpfCnpj, self).__init__()
        self.Cpf = TagCaracter(nome=u'Cpf'   , tamanho=[1, 11], raiz=u'/[nfse]')
        self.Cnpj = TagCaracter(nome=u'Cnpj'   , tamanho=[1, 14], raiz=u'/[nfse]')
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<CpfCnpj>'
        if self.Cnpj.valor != u'':
            xml += self.Cnpj.xml
        else:
            xml += self.Cpf.xml
        
        xml += u'</CpfCnpj>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Cpf.xml  = arquivo
            self.Cnpj.xml  = arquivo

    xml = property(get_xml, set_xml)
        

class IdentificacaoTomador(XMLNFe):
    def __init__(self):
        super(IdentificacaoTomador, self).__init__()
        self.CpfCnpj = CpfCnpj()
        self.InscricaoMunicipal = TagCaracter(nome=u'InscricaoMunicipal', tamanho=[1, 15], raiz=u'/[nfse]', obrigatorio=False)
    def get_xml(self):
        if self.CpfCnpj.Cpf.valor==u'' and self.CpfCnpj.Cnpj.valor==u'':
            return u''
        xml = XMLNFe.get_xml(self)
        xml += u'<IdentificacaoTomador>'
        xml += self.CpfCnpj.xml
        xml += self.InscricaoMunicipal.xml
        
        xml += u'</IdentificacaoTomador>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CpfCnpj.xml  = arquivo
            self.InscricaoMunicipal.xml  = arquivo

    xml = property(get_xml, set_xml)

class DadosTomador(XMLNFe):
    def __init__(self):
        super(DadosTomador, self).__init__()
        self.IdentificacaoTomador = IdentificacaoTomador()
        self.RazaoSocial = TagCaracter(nome=u'RazaoSocial', tamanho=[1, 115], raiz=u'/[nfse]', obrigatorio=False)
        self.Endereco = Endereco()
        self.Contato = Contato()
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<DadosTomador>'
        xml += self.IdentificacaoTomador.xml
        xml += self.RazaoSocial.xml
        xml += self.Endereco.xml
        xml += self.Contato.xml
        
        xml += u'</DadosTomador>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.IdentificacaoTomador.xml   = arquivo
            self.RazaoSocial.xml   = arquivo
            self.Endereco.xml   = arquivo
            self.Contato.xml   = arquivo

    xml = property(get_xml, set_xml)
    
class Tomador(DadosTomador):
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<Tomador>'
        xml += self.IdentificacaoTomador.xml
        xml += self.RazaoSocial.xml
        xml += self.Endereco.xml
        xml += self.Contato.xml
        
        xml += u'</Tomador>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.IdentificacaoTomador.xml   = arquivo
            self.RazaoSocial.xml   = arquivo
            self.Endereco.xml   = arquivo
            self.Contato.xml   = arquivo

    xml = property(get_xml, set_xml)    
    
        

class Valores(XMLNFe):
    def __init__(self):
        super(Valores, self).__init__()
        self.ValorServicos = TagDecimal(nome=u'ValorServicos', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]')
        self.ValorDeducoes = TagDecimal(nome=u'ValorDeducoes', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.ValorPis = TagDecimal(nome=u'ValorPis', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.ValorCofins = TagDecimal(nome=u'ValorCofins', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.ValorInss = TagDecimal(nome=u'ValorInss', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.ValorIr = TagDecimal(nome=u'ValorIr', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.ValorCsll = TagDecimal(nome=u'ValorCsll', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.IssRetido = TagInteiro(nome=u'IssRetido', tamanho=[1,1], raiz=u'/[nfse]')
        self.ValorIss = TagDecimal(nome=u'ValorIss', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.OutrasRetencoes = TagDecimal(nome=u'OutrasRetencoes', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.BaseCalculo = TagDecimal(nome=u'BaseCalculo', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]')
        self.Aliquota = TagDecimal(nome=u'Aliquota', tamanho=[1, 5], decimais=[0, 4], raiz=u'/[nfse]', obrigatorio=False)
        self.ValorLiquidoNfse = TagDecimal(nome=u'ValorLiquidoNfse', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.ValorIssRetido = TagDecimal(nome=u'ValorIssRetido', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.DescontoCondicionado = TagDecimal(nome=u'DescontoCondicionado', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
        self.DescontoIncondicionado = TagDecimal(nome=u'DescontoIncondicionado', tamanho=[1, 15], decimais=[0, 2], raiz=u'/[nfse]', obrigatorio=False)
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<Valores>'
        xml += self.ValorServicos.xml
        xml += self.ValorDeducoes.xml
        xml += self.ValorPis.xml
        xml += self.ValorCofins.xml
        xml += self.ValorInss.xml
        xml += self.ValorIr.xml
        xml += self.ValorCsll.xml
        xml += self.IssRetido.xml
        xml += self.ValorIss.xml
        xml += self.OutrasRetencoes.xml
        xml += self.BaseCalculo.xml
        xml += self.Aliquota.xml
        xml += self.ValorLiquidoNfse.xml
        xml += self.ValorIssRetido.xml
        xml += self.DescontoCondicionado.xml
        xml += self.DescontoIncondicionado.xml
        
        xml += u'</Valores>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.ValorServicos.xml = arquivo
            self.ValorDeducoes.xml = arquivo
            self.ValorPis.xml = arquivo
            self.ValorCofins.xml = arquivo
            self.ValorInss.xml = arquivo
            self.ValorIr.xml = arquivo
            self.ValorCsll.xml = arquivo
            self.IssRetido.xml = arquivo
            self.ValorIss.xml = arquivo
            self.OutrasRetencoes.xml = arquivo
            self.BaseCalculo.xml = arquivo
            self.Aliquota.xml = arquivo
            self.ValorLiquidoNfse.xml = arquivo
            self.ValorIssRetido.xml = arquivo
            self.DescontoCondicionado.xml = arquivo
            self.DescontoIncondicionado.xml = arquivo

    xml = property(get_xml, set_xml)    
    

class DadosServico(XMLNFe):
    def __init__(self):
        super(DadosServico, self).__init__()
        self.Valores = Valores()
        self.ItemListaServico = TagCaracter(nome=u'ItemListaServico', tamanho=[1, 5], raiz=u'/[nfse]')
        self.CodigoCnae = TagInteiro(nome=u'CodigoCnae', tamanho=[1,7], raiz=u'/[nfse]', obrigatorio=False)
        self.CodigoTributacaoMunicipio = TagCaracter(nome=u'CodigoTributacaoMunicipio', tamanho=[1, 20], raiz=u'/[nfse]', obrigatorio=False)
        self.Discriminacao = TagCaracter(nome=u'Discriminacao', tamanho=[1, 2000], raiz=u'/[nfse]')
        self.CodigoMunicipio = TagInteiro(nome=u'CodigoMunicipio', tamanho=[1, 7], raiz=u'/[nfse]')
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<Servico>'
        xml += self.Valores.xml
        xml += self.ItemListaServico.xml
        xml += self.CodigoCnae.xml
        xml += self.CodigoTributacaoMunicipio.xml
        xml += self.Discriminacao.xml
        xml += self.CodigoMunicipio.xml
        
        xml += u'</Servico>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Valores.xml   = arquivo
            self.ItemListaServico.xml   = arquivo
            self.CodigoCnae.xml   = arquivo
            self.CodigoTributacaoMunicipio.xml   = arquivo
            self.Discriminacao.xml   = arquivo
            self.CodigoMunicipio.xml   = arquivo

    xml = property(get_xml, set_xml)

    
class IdentificacaoRps(XMLNFe):
    def __init__(self):
        super(IdentificacaoRps, self).__init__()
        self.Numero = TagInteiro(nome=u'Numero', tamanho=[1,15], raiz=u'/[nfse]')
        self.Serie = TagCaracter(nome=u'Serie', tamanho=[1, 5], raiz=u'/[nfse]')
        self.Tipo = TagInteiro(nome=u'Tipo', tamanho=[1,1], raiz=u'/[nfse]')
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<IdentificacaoRps>'
        xml += self.Numero.xml
        xml += self.Serie.xml
        xml += self.Tipo.xml
        
        xml += u'</IdentificacaoRps>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Numero.xml   = arquivo
            self.Serie.xml   = arquivo
            self.Tipo.xml   = arquivo

    xml = property(get_xml, set_xml)
    
class RpsSubstituido(IdentificacaoRps):
    def get_xml(self):
        if not (self.Numero.valor or self.Serie.valor or self.Tipo.valor):
            return u''
        xml = XMLNFe.get_xml(self)
        xml += u'<RpsSubstituido>'
        xml += self.Numero.xml
        xml += self.Serie.xml
        xml += self.Tipo.xml
        
        xml += u'</RpsSubstituido>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Numero.xml   = arquivo
            self.Serie.xml   = arquivo
            self.Tipo.xml   = arquivo

    xml = property(get_xml, set_xml)    

    

class IdentificacaoPrestador(XMLNFe):
    def __init__(self):
        super(IdentificacaoPrestador, self).__init__()
        self.Cnpj = TagCaracter(nome=u'Cnpj'   , tamanho=[1, 14], raiz=u'/[nfse]')
        self.InscricaoMunicipal = TagCaracter(nome=u'InscricaoMunicipal'   , tamanho=[1, 15], raiz=u'/[nfse]', obrigatorio=False)
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<Prestador>'
        xml += self.Cnpj.xml
        xml += self.InscricaoMunicipal.xml
        
        xml += u'</Prestador>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Cnpj.xml   = arquivo
            self.InscricaoMunicipal.xml   = arquivo

    xml = property(get_xml, set_xml)
    
#ABRASF
class IdentificacaoIntermediario(XMLNFe):
    def __init__(self):
        super(IdentificacaoIntermediario, self).__init__()
        self.CpfCnpj = CpfCnpj()
        self.InscricaoMunicipal = TagCaracter(nome=u'InscricaoMunicipal'   , tamanho=[1, 15], raiz=u'/[nfse]')
    def get_xml(self):        
        xml = XMLNFe.get_xml(self)
        xml += u'<IdentificacaoIntermediario>'
        xml += self.CpfCnpj.xml
        xml += self.InscricaoMunicipal.xml
        xml += u'</IdentificacaoIntermediario>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CpfCnpj.xml = arquivo
            self.InscricaoMunicipal.xml = arquivo

    xml = property(get_xml, set_xml)
    

#ABRASF
class DadosIntermediario(XMLNFe):
    def __init__(self):
        super(DadosIntermediario, self).__init__()
        self.IdentificacaoIntermediario = IdentificacaoIntermediario()
        self.RazaoSocial = TagCaracter(nome=u'RazaoSocial', tamanho=[1, 150], raiz=u'/[nfse]')
        #self.CodigoMunicipio =  TagInteiro(nome=u'CodigoMunicipio', tamanho=[1, 7], raiz=u'/')
    def get_xml(self):
        if not self.RazaoSocial.valor:
            return u''
        xml = XMLNFe.get_xml(self)
        xml += u'<IntermediarioServico>'
        xml += self.IdentificacaoIntermediario.xml
        xml += self.RazaoSocial.xml
        #xml += self.CodigoMunicipio.xml
        xml += u'</IntermediarioServico>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.IdentificacaoIntermediario.xml = arquivo
            self.RazaoSocial.xml = arquivo
            #self.CodigoMunicipio.xml = arquivo

    xml = property(get_xml, set_xml)
    

class IdentificacaoIntermediarioServico(XMLNFe):
    def __init__(self):
        super(IdentificacaoIntermediarioServico, self).__init__()
        self.RazaoSocial = TagCaracter(nome=u'RazaoSocial', tamanho=[1, 115], raiz=u'/[nfse]')
        self.CpfCnpj = CpfCnpj()
        self.InscricaoMunicipal = TagCaracter(nome=u'InscricaoMunicipal'   , tamanho=[1, 15], raiz=u'/[nfse]')
    def get_xml(self):        
        xml = XMLNFe.get_xml(self)
        xml += u'<IntermediarioServico>'
        xml += self.RazaoSocial.xml
        xml += self.CpfCnpj.xml
        xml += self.InscricaoMunicipal.xml
        xml += u'</IntermediarioServico>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.RazaoSocial.xml = arquivo
            self.CpfCnpj.xml = arquivo
            self.InscricaoMunicipal.xml = arquivo

    xml = property(get_xml, set_xml)

        
class DadosConstrucaoCivil(XMLNFe):
    def __init__(self):
        super(DadosConstrucaoCivil, self).__init__()
        self.CodigoObra = TagCaracter(nome=u'CodigoObra', tamanho=[1, 15], raiz=u'/[nfse]')
        self.Art = TagCaracter(nome=u'Art', tamanho=[1, 15], raiz=u'/[nfse]')
    def get_xml(self):
        if not (self.CodigoObra.valor or self.Art.valor):
            return u''
            
        xml = XMLNFe.get_xml(self)
        xml += u'<ConstrucaoCivil>'
        xml += self.CodigoObra.xml
        xml += self.Art.xml
        xml += u'</ConstrucaoCivil>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CodigoObra.xml = arquivo
            self.Art.xml = arquivo

    xml = property(get_xml, set_xml)

class InfRps(XMLNFe):
    def __init__(self):
        super(InfRps, self).__init__()
        self.Id = TagCaracter(nome=u'InfRps', propriedade=u'Id', raiz=u'/[nfse]')
        self.IdentificacaoRps = IdentificacaoRps()
        self.DataEmissao = TagDataHora(nome=u'DataEmissao', raiz=u'/[nfse]')
        self.NaturezaOperacao = TagInteiro(nome=u'NaturezaOperacao', tamanho=[1,2], raiz=u'/[nfse]')
        self.RegimeEspecialTributacao = TagInteiro(nome=u'RegimeEspecialTributacao', tamanho=[1,2], raiz=u'/[nfse]', obrigatorio=False)
        self.OptanteSimplesNacional = TagInteiro(nome=u'OptanteSimplesNacional', tamanho=[1,1], raiz=u'/[nfse]')
        self.IncentivadorCultural = TagInteiro(nome=u'IncentivadorCultural', tamanho=[1,1], raiz=u'/[nfse]')
        self.Status = TagInteiro(nome=u'Status', tamanho=[1,1], raiz=u'/[nfse]')
        self.RpsSubstituido = RpsSubstituido()
        self.Servico = DadosServico()
        self.Prestador = IdentificacaoPrestador()
        self.Tomador = Tomador()
        #self.IntermediarioServico = IdentificacaoIntermediarioServico()
        self.IntermediarioServico = DadosIntermediario()
        self.ConstrucaoCivil = DadosConstrucaoCivil()
        
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
        
    def get_xml(self):
        self.Id.valor = u'rps:'+str(self.IdentificacaoRps.Numero.valor) + str(self.IdentificacaoRps.Serie.valor)
        
        xml = XMLNFe.get_xml(self)
        xml += self.Id.xml
        xml += self.IdentificacaoRps.xml
        xml += self.DataEmissao.xml
        xml += self.NaturezaOperacao.xml
        xml += self.RegimeEspecialTributacao.xml
        xml += self.OptanteSimplesNacional.xml
        xml += self.IncentivadorCultural.xml
        xml += self.Status.xml
        xml += self.RpsSubstituido.xml
        xml += self.Servico.xml
        xml += self.Prestador.xml.replace(ABERTURA, u'')
        xml += self.Tomador.xml
        xml += self.IntermediarioServico.xml
        xml += self.ConstrucaoCivil.xml
        
        xml += u'</InfRps>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.IdentificacaoRps.xml = arquivo
            self.DataEmissao.xml = arquivo
            self.NaturezaOperacao.xml = arquivo
            self.RegimeEspecialTributacao.xml = arquivo
            self.OptanteSimplesNacional.xml = arquivo
            self.IncentivadorCultural.xml = arquivo
            self.Status.xml = arquivo
            self.RpsSubstituido.xml = arquivo
            self.Servico.xml = arquivo
            self.Prestador.xml = arquivo
            self.Tomador.xml = arquivo
            self.IntermediarioServico.xml = arquivo
            self.ConstrucaoCivil.xml = arquivo

    xml = property(get_xml, set_xml)    
        
        

class Rps(XMLNFe):
    def __init__(self):
        super(Rps, self).__init__()
        self.InfRps = InfRps()
        self.Signature = Signature()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<Rps>'
        xml += self.InfRps.xml
        xml += self.Signature.xml
        xml += u'</Rps>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.InfRps.xml    = arquivo
            self.Signature.xml = self._le_noh('[nfse]//Rps/sig:Signature')

    xml = property(get_xml, set_xml)
    
    
class LoteRps(XMLNFe):
    def __init__(self):
        super(LoteRps, self).__init__()
        self.versao = TagDecimal(nome=u'LoteRps' , propriedade=u'versao', raiz=u'/', valor=u'1.00')
        self.Id = TagCaracter(nome=u'LoteRps', propriedade=u'Id', raiz=u'/')
        self.NumeroLote = TagInteiro(nome=u'NumeroLote', tamanho=[1,15], raiz=u'/')
        self.Cnpj = TagCaracter(nome=u'Cnpj'   , tamanho=[1, 14], raiz=u'/')
        self.InscricaoMunicipal = TagCaracter(nome=u'InscricaoMunicipal'   , tamanho=[1, 15], raiz=u'/')
        self.QuantidadeRps = TagInteiro(nome=u'QuantidadeRps', tamanho=[1,4], raiz=u'/')
        self.Rps = []
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'
        
    def get_xml(self):
        #self.Id.valor = u'lote:'+ str(self.Cnpj.valor) +str(self.NumeroLote.valor)
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<LoteRps versao="' + str(self.versao.valor) + u'" Id="' + self.Id.valor + u'">'
        xml += self.NumeroLote.xml
        xml += self.Cnpj.xml
        xml += self.InscricaoMunicipal.xml
        xml += self.QuantidadeRps.xml
        xml += u'<ListaRps>'
        
        for r in self.Rps:
            xml += tira_abertura(r.xml)
            
        xml += u'</ListaRps>'
        xml += u'</LoteRps>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.NumeroLote.xml = arquivo
            self.Cnpj.xml = arquivo
            self.InscricaoMunicipal.xml = arquivo
            self.QuantidadeRps.xml = arquivo
            self.Rps = self.le_grupo('[nfse]//LoteRps/Rps', Rps)

    xml = property(get_xml, set_xml)