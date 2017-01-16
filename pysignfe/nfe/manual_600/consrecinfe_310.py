# -*- coding: utf-8 -*-
import os

from pysignfe.nfe.manual_500 import consrecinfe_310
from pysignfe.nfe.manual_600 import ESQUEMA_ATUAL
from pysignfe.xml_sped import *
from pysignfe.nfe.manual_600.nfe_310 import NFe

DIRNAME = os.path.dirname(__file__)

class ConsReciNFe(consrecinfe_310.ConsReciNFe):
    def __init__(self):
        super(ConsReciNFe, self).__init__()
        self.versao  = TagDecimal(nome=u'consReciNFe', codigo=u'BP02', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'3.10', raiz=u'/')
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'consReciNFe_v3.10.xsd'


class InfProt(consrecinfe_310.InfProt):
    def __init__(self):
        super(InfProt, self).__init__()
        
    def get_xml(self):
        if not (self.tpAmb.valor or self.chNFe.valor or self.dhRecbto.valor):
            return ''
            
        xml = XMLNFe.get_xml(self)

        if self.Id.valor:
            xml += self.Id.xml
        else:
            xml += u'<infProt>'

        xml += self.tpAmb.xml
        xml += self.verAplic.xml
        xml += self.chNFe.xml
        xml += self.dhRecbto.xml
        xml += self.nProt.xml
        xml += self.digVal.xml
        xml += self.cStat.xml
        xml += self.xMotivo.xml
        xml += u'</infProt>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Id.xml        = arquivo
            self.tpAmb.xml     = arquivo
            self.verAplic.xml  = arquivo
            self.chNFe.xml     = arquivo
            self.dhRecbto.xml  = arquivo
            self.nProt.xml     = arquivo
            self.digVal.xml    = arquivo
            self.cStat.xml     = arquivo
            self.xMotivo.xml   = arquivo

    xml = property(get_xml, set_xml)
    

class ProtNFe(consrecinfe_310.ProtNFe):
    def __init__(self):
        super(ProtNFe, self).__init__()
        self.versao  = TagDecimal(nome=u'protNFe', codigo=u'PR02' , propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'3.10', raiz=u'/')
        self.infProt = InfProt()
        
    def get_xml(self):
        if not self.infProt.xml:
            return ''
            
        xml = XMLNFe.get_xml(self)
        xml += self.versao.xml
        xml += self.infProt.xml

        if len(self.Signature.URI) and (self.Signature.URI.strip() != u'#'):
            xml += self.Signature.xml

        xml += u'</protNFe>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml  = arquivo
            self.infProt.xml = self._le_noh(u'//protNFe/infProt')
            self.Signature.xml = self._le_noh(u'//protNFe/sig:Signature')

    xml = property(get_xml, set_xml)
    
    def protocolo_formatado_nfce(self):
        if not self.infProt.nProt.valor:
            return u''
        return u'Protocolo de autorização: '+ self.infProt.nProt.valor
        
    def data_autorizacao_nfce(self):
        if not self.infProt.nProt.valor:
            return u''
        return u'Data de autorização: '+ self.infProt.dhRecbto.formato_danfe()
        

class RetConsReciNFe(consrecinfe_310.RetConsReciNFe):
    def __init__(self):
        super(RetConsReciNFe, self).__init__()
        self.versao   = TagDecimal(nome=u'retConsReciNFe', codigo=u'BR02' , propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'3.10', raiz=u'/')
        self.dhRecbto = TagDataHoraUTC(nome=u'dhRecbto' , codigo=u'BR06a1', raiz=u'//retConsReciNFe')
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retConsReciNFe_v3.10.xsd'
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.versao.xml
        xml += self.tpAmb.xml
        xml += self.verAplic.xml
        xml += self.nRec.xml
        xml += self.cStat.xml
        xml += self.xMotivo.xml
        xml += self.cUF.xml
        xml += self.dhRecbto.xml
        xml += self.cMsg.xml
        xml += self.xMsg.xml
        
        for pn in self.protNFe:
            xml += pn.xml
            
        xml += u'</retConsReciNFe>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml   = arquivo
            self.tpAmb.xml    = arquivo
            self.verAplic.xml = arquivo
            self.nRec.xml     = arquivo
            self.cStat.xml    = arquivo
            self.xMotivo.xml  = arquivo
            self.cUF.xml      = arquivo
            self.dhRecbto.xml = arquivo
            self.cMsg.xml     = arquivo
            self.xMsg.xml     = arquivo
            self.protNFe      = self.le_grupo('//retConsReciNFe/protNFe', ProtNFe)

            #
            # Monta o dicionário dos protocolos
            #
            for pn in self.protNFe:
                self.dic_protNFe[pn.infProt.chNFe.valor] = pn
       
    xml = property(get_xml, set_xml)

    
class ProcNFe(consrecinfe_310.ProcNFe):
    def __init__(self):
        super(ProcNFe, self).__init__()
        self.versao  = TagDecimal(nome=u'nfeProc', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'3.10', raiz=u'/')
        self.NFe     = NFe()
        self.protNFe = ProtNFe()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'procNFe_v3.10.xsd'
