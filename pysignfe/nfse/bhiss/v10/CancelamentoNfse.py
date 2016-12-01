# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *

class IdentificacaoNfse(XMLNFe):
    def __init__(self):
        super(IdentificacaoNfse, self).__init__()
        self.Numero = TagInteiro(nome=u'Numero', tamanho=[1,15], raiz=u'/[nfse]')
        self.Cnpj = TagCaracter(nome=u'Cnpj'   , tamanho=[1, 14], raiz=u'/[nfse]')
        self.InscricaoMunicipal = TagCaracter(nome=u'InscricaoMunicipal'   , tamanho=[1, 15], raiz=u'/[nfse]', obrigatorio=False)
        self.CodigoMunicipio = TagInteiro(nome=u'CodigoMunicipio', tamanho=[1, 7], raiz=u'/[nfse]', obrigatorio=False)
    def get_xml(self):    
        xml = XMLNFe.get_xml(self)
        xml += u'<IdentificacaoNfse>'
        xml += self.Numero.xml
        xml += self.Cnpj.xml
        xml += self.InscricaoMunicipal.xml
        xml += self.CodigoMunicipio.xml
        xml += u'</IdentificacaoNfse>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Numero.xml    = arquivo
            self.Cnpj.xml = arquivo
            self.InscricaoMunicipal.xml = arquivo
            self.CodigoMunicipio.xml = arquivo

    xml = property(get_xml, set_xml)
    

class InfPedidoCancelamento(XMLNFe):
    def __init__(self):
        super(InfPedidoCancelamento, self).__init__()
        self.Id = TagCaracter(nome=u'InfPedidoCancelamento', propriedade=u'Id', raiz=u'/[nfse]')
        self.IdentificacaoNfse = IdentificacaoNfse()
        self.CodigoCancelamento = TagCaracter(nome=u'CodigoCancelamento', tamanho=[1, 4], raiz=u'/[nfse]')
    def get_xml(self):
        self.Id.valor = u'cancelamento:' + str(self.IdentificacaoNfse.Cnpj.valor) + str(self.IdentificacaoNfse.Numero.valor)
    
        xml = XMLNFe.get_xml(self)
        xml += self.Id.xml
        xml += self.IdentificacaoNfse.xml
        xml += self.CodigoCancelamento.xml
        xml += u'</InfPedidoCancelamento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.IdentificacaoNfse.xml    = arquivo
            self.CodigoCancelamento.xml = arquivo

    xml = property(get_xml, set_xml)          
    

class PedidoCancelamento(XMLNFe):
    def __init__(self):
        super(PedidoCancelamento, self).__init__()
        self.InfPedidoCancelamento = InfPedidoCancelamento()
        self.Signature = Signature()

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<Pedido xmlns="'+ NAMESPACE_NFSE + '">'
        #xml += u'<PedidoCancelamento>'
        xml += self.InfPedidoCancelamento.xml
        xml += self.Signature.xml
        xml += u'</Pedido>'
        #xml += u'</PedidoCancelamento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.InfPedidoCancelamento.xml    = arquivo
            self.Signature.xml = self._le_noh('[nfse]//Rps/sig:Signature')

    xml = property(get_xml, set_xml)      

class ConfirmacaoCancelamento(XMLNFe):
    def __init__(self):
        super(ConfirmacaoCancelamento, self).__init__()
        self.Id = TagCaracter(nome=u'ConfirmacaoCancelamento', propriedade=u'Id', raiz=u'/[nfse]')
        self.Pedido = PedidoCancelamento()
        self.DataHora = TagDataHora(nome=u'DataHora', raiz=u'/')
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.Id.xml
        xml += self.Pedido.xml
        xml += self.DataHora.xml
        xml += u'</ConfirmacaoCancelamento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Id.xml    = arquivo
            self.Pedido.xml = arquivo
            self.DataHora.xml = arquivo

    xml = property(get_xml, set_xml)  
    

class CancelamentoNfse(XMLNFe):
    def __init__(self):
        super(CancelamentoNfse, self).__init__()
        self.ConfirmacaoCancelamento = ConfirmacaoCancelamento()
        self.Signature = Signature()
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<CancelamentoNfse>'
        xml += self.ConfirmacaoCancelamento.xml
        xml += self.Signature.xml
        xml += u'</CancelamentoNfse>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.ConfirmacaoCancelamento.xml    = arquivo
            self.Signature.xml = self._le_noh('//Rps/sig:Signature')

    xml = property(get_xml, set_xml)    