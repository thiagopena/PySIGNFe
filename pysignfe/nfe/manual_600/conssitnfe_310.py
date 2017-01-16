# -*- coding: utf-8 -*-
import os
from pysignfe.xml_sped.base import etree
          
from pysignfe.nfe.manual_500 import conssitnfe_310
from pysignfe.xml_sped import *
from pysignfe.nfe.manual_600 import ESQUEMA_ATUAL, ProtNFe_310, RetCancNFe_310
from .cancnfe_evento import ProcEventoNFeCancNFe
from .carta_correcao import ProcEventoNFeCCe
from .epec_evento import ProcEventoNFeEPEC
from pysignfe.nfe.manifestacao_destinatario import ProcEventoNFeConfRecebimento_100

DIRNAME = os.path.dirname(__file__)

class ConsSitNFe(conssitnfe_310.ConsSitNFe):
    def __init__(self):
        super(ConsSitNFe, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'consSitNFe_v3.10.xsd'


class RetConsSitNFe(conssitnfe_310.RetConsSitNFe):
    def __init__(self):
        super(RetConsSitNFe, self).__init__()
        self.versao     = TagDecimal(nome=u'retConsSitNFe', codigo=u'ER01', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'3.10', raiz=u'/')
        self.dhRecbto   = TagDataHoraUTC(nome=u'dhRecbto' , codigo=u'ER07a', raiz=u'//retConsSitNFe')
        self.protNFe        = None
        self.retCancNFe     = None
        self.procEventoNFe  = []
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retConsSitNFe_v3.10.xsd'

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += self.versao.xml
        xml += self.tpAmb.xml
        xml += self.verAplic.xml
        xml += self.cStat.xml
        xml += self.xMotivo.xml
        xml += self.cUF.xml
        xml += self.dhRecbto.xml
        xml += self.chNFe.xml

        if self.protNFe is not None:
            xml += self.protNFe.xml

        if self.retCancNFe is not None:
            xml += tira_abertura(self.retCancNFe.xml)
        
        #if self.procEventoNFe is not None:
        if len(self.procEventoNFe):
            for ev in self.procEventoNFe:
                xml += tira_abertura(ev.xml)

        xml += u'</retConsSitNFe>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml    = arquivo
            self.tpAmb.xml     = arquivo
            self.verAplic.xml  = arquivo
            self.cStat.xml     = arquivo
            self.xMotivo.xml   = arquivo
            self.cUF.xml       = arquivo
            self.dhRecbto.xml  = arquivo
            self.chNFe.xml     = arquivo

            if self._le_noh(u'//retConsSitNFe/protNFe') is not None:
                self.protNFe = ProtNFe_310()
                self.protNFe.xml = arquivo

            if self._le_noh(u'//retConsSitNFe/retCancNFe') is not None:
                self.retCancNFe = RetCancNFe_310()
                self.retCancNFe.xml = arquivo
                
            #if self._le_nohs('//retConsSitNFe/procEventoNFe') is not None:
            #    self.procEventoNFe = self.le_grupo('//retConsSitNFe/procEventoNFe', procEventoNFe)
            
            if self._le_nohs('//retConsSitNFe/procEventoNFe') is not None:
                for p in self._le_nohs('//retConsSitNFe/procEventoNFe'):
                    desc = p.xpath('//nfe:detEvento/nfe:descEvento/text()', namespaces={'nfe':NAMESPACE_NFE})
                    pev = None
                    if 'Cancelamento' in desc:
                        pev = ProcEventoNFeCancNFe()
                        #pev.xml = etree.tostring(p).decode('utf-8').strip('\n')
                        pev.xml = etree.tounicode(p)
                    elif 'Correcao' in desc or 'Correção' in desc:
                        pev = ProcEventoNFeCCe()
                        pev.xml = etree.tounicode(p)
                    elif 'Operacao' in desc:
                        pev = ProcEventoNFeConfRecebimento_100()
                        pev.xml = etree.tounicode(p)
                    elif 'EPEC' in desc:
                        pev = ProcEventoNFeEPEC()
                        pev.xml = etree.tounicode(p)
                    
                    if pev:
                        self.procEventoNFe.append(pev)
                
                
    xml = property(get_xml, set_xml)
