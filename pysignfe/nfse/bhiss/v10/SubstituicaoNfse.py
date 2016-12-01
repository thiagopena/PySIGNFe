# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *

class InfSubstituicaoNfse(XMLNFe):
    def __init__(self):
        super(InfSubstituicaoNfse, self).__init__()
        self.Id = TagCaracter(nome=u'InfSubstituicaoNfse', propriedade=u'Id', raiz=u'/')
        self.NfseSubstituidora = TagInteiro(nome=u'NfseSubstituidora', tamanho=[1,15], raiz=u'/')
        
    def get_xml(self):
        self.Id.valor = u'substituicao:'+str(self.NfseSubstituidora.valor)
        
        xml = XMLNFe.get_xml(self)
        xml += self.Id.xml
        xml += self.NfseSubstituidora.xml
        xml += u'</InfSubstituicaoNfse>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.NfseSubstituidora.xml    = arquivo

    xml = property(get_xml, set_xml)

class SubstituicaoNfse(XMLNFe):
    def __init__(self):
        super(SubstituicaoNfse, self).__init__()
        self.InfSubstituicaoNfse = InfSubstituicaoNfse()
        self.Signature = Signature()
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<SubstituicaoNfse>'
        xml += self.InfSubstituicaoNfse.xml
        xml += self.Signature.xml
        xml += u'</SubstituicaoNfse>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.InfSubstituicaoNfse.xml    = arquivo
            self.Signature.xml = self._le_noh('//Rps/sig:Signature')

    xml = property(get_xml, set_xml)