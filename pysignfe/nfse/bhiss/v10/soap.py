# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
import os
NAMESPACE_BHISS = u'http://ws.bhiss.pbh.gov.br'


DIRNAME = os.path.dirname(__file__)


class cabecalho(XMLNFe):
    def __init__(self):
        super(cabecalho, self).__init__()
        self.versao      = TagDecimal(nome=u'cabecalho', propriedade=u'versao', namespace=NAMESPACE_NFSE, valor=u'1.00', raiz=u'//cabecalho')
        self.versaoDados = TagDecimal(nome=u'versaoDados', raiz=u'//cabecalho', tamanho=[1, 4])
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/')
        self.arquivo_esquema = u'nfse.xsd'

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += self.versao.xml
        xml += self.versaoDados.xml
        xml += u'</cabecalho>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versaoDados.xml = arquivo

    xml = property(get_xml, set_xml)


class NFSeCabecMsg(XMLNFe):
    def __init__(self):
        super(NFSeCabecMsg, self).__init__()
        self.cabecalho = cabecalho()

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<nfseCabecMsg>'
        #xml += u'&lt;nfseCabecMsg&gt;'
        #xml += u'<![CDATA['
        #xml += tirar_acentos(self.cabecalho.xml).replace(u'&quot;', u'\\\'')
        xml += tirar_acentos(self.cabecalho.xml)
        #xml += self.cabecalho.xml
        #xml += u']]>'
        xml += u'</nfseCabecMsg>'
        #xml += u'&lt;/nfseCabecMsg&gt;'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.cabecalho.xml = arquivo

    xml = property(get_xml, set_xml)


class NFSeDadosMsg(XMLNFe):
    def __init__(self):
        super(NFSeDadosMsg, self).__init__()
        self.dados = None

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<nfseDadosMsg>'
        #xml += u'&lt;nfseDadosMsg&gt;'
        #xml += u'<![CDATA['
        #xml += tirar_acentos(self.dados.xml).replace(u'&quot;', u'\\\'')
        xml += tirar_acentos(self.dados.xml)
        #xml += self.dados.xml
        #xml += u']]>'
        xml += u'</nfseDadosMsg>'
        #xml += u'&lt;/nfseDadosMsg&gt;'

        return xml

    def set_xml(self, arquivo):
        pass

    xml = property(get_xml, set_xml)


class SOAPEnvio(XMLNFe):
    def __init__(self):
        super(SOAPEnvio, self).__init__()
        self.webservice = u''
        self.metodo = u''
        self.envio = None
        self.nfseCabecMsg = NFSeCabecMsg()
        self.nfseDadosMsg = NFSeDadosMsg()
        #self._header = {u'content-type': u'application/soap+xml; charset=utf-8',
        #    u'Accept': u'application/soap+xml; charset=utf-8'}
        self._header = {u'content-type': u'text/xml; charset=utf-8',
            u'Accept': u'application/soap+xml; charset=utf-8'}

    def get_xml(self):
        self.nfseDadosMsg.dados = self.envio
        self.nfseCabecMsg.cabecalho.versaoDados.valor = self.envio.versao.valor

        self._header['SOAPAction'] = self.metodo

        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">'
        xml +=     u'<S:Body>'
        xml +=         u'<ns2:' + self.metodo + u'Request xmlns:ns2="' + NAMESPACE_BHISS + u'">'
        xml += self.nfseCabecMsg.xml
        xml += self.nfseDadosMsg.xml
        xml +=         u'</ns2:' + self.metodo + u'Request>'
        xml +=     u'</S:Body>'
        xml += u'</S:Envelope>'
        return xml

    def set_xml(self):
        pass

    xml = property(get_xml, set_xml)

    def get_header(self):
        header = self._header
        return header

    header = property(get_header)


class SOAPRetorno(XMLNFe):
    def __init__(self):
        super(SOAPRetorno, self).__init__()
        self.webservice = u''
        self.metodo = u''
        self.resposta = None

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">'
        xml +=     u'<S:Body>'
        xml +=         u'<' + self.metodo + u'Response xmlns="' + NAMESPACE_BHISS + u'">'
        xml +=             u'<' + self.metodo + u'Resposta>'
        xml += self.resposta.xml
        xml +=             u'</' + self.metodo + u'Resposta>'
        xml +=         u'</' + self.metodo + u'Response>'
        xml +=     u'</S:Body>'
        xml += u'</S:Envelope>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.resposta.xml = arquivo

    xml = property(get_xml, set_xml)