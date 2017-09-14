# -*- coding: utf-8 -*-

import os

from pysignfe.nfe.manual_600 import soap_310
from pysignfe.xml_sped import *

DIRNAME = os.path.dirname(__file__)

class NFeDadosMsg(soap_310.NFeDadosMsg):
    def __init__(self):
        super(NFeDadosMsg, self).__init__()


class SOAPEnvio(XMLNFe):
    def __init__(self):
        super(SOAPEnvio, self).__init__()
        self.webservice = u''
        self.metodo = u''
        self.cUF    = None
        self.envio  = None
        self.nfeDadosMsg = NFeDadosMsg()
        self._header = {u'content-type': u'application/soap+xml; charset=utf-8'}

    def get_xml(self):
        self.nfeDadosMsg.webservice = self.webservice
        self.nfeDadosMsg.dados = self.envio

        self._header[u'content-type'] = u'application/soap+xml; charset=utf-8; action="http://www.portalfiscal.inf.br/nfe/wsdl/' + self.webservice + u'"'

        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'
        xml +=     u'<soap:Body>'
        xml +=             self.nfeDadosMsg.xml
        xml +=     u'</soap:Body>'
        xml += u'</soap:Envelope>'
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
        xml += u'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'
        xml +=     u'<soap:Body>'
        xml +=         u'<' + self.metodo + u'Result xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/' + self.webservice + u'">'
        xml +=             self.resposta.xml
        xml +=         u'</' + self.metodo + u'Result>'
        xml +=     u'</soap:Body>'
        xml += u'</soap:Envelope>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.resposta.xml = arquivo

    xml = property(get_xml, set_xml)

