# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *
from pysignfe.nfe.manual_600 import ESQUEMA_ATUAL
from pysignfe.nfe.manual_500.evento_base import DetEvento, InfEventoEnviado, Evento, EnvEvento, InfEventoRecebido, RetEvento, RetEnvEvento, ProcEventoNFe

import os

DIRNAME = os.path.dirname(__file__)


class Dest(XMLNFe):
    def __init__(self):
        super(DetEvento, self).__init__()
        self.UF        = TagCaracter(nome=u'UF'   , codigo=u'P27', tamanho=[ 2,  2], raiz=u'//dest')
        self.CNPJ      = TagCaracter(nome=u'CNPJ' , codigo=u'P28', tamanho=[0 , 14]   , raiz=u'//dest', obrigatorio=False)
        self.CPF       = TagCaracter(nome=u'CPF'  , codigo=u'P29', tamanho=[11, 11]   , raiz=u'//dest', obrigatorio=False)
        self.IE        = TagCaracter(nome=u'IE'   , codigo=u'P31', tamanho=[ 2, 14]   , raiz=u'//dest', obrigatorio=False)
        self.idEstrangeiro = TagCaracter(nome=u'idEstrangeiro', codigo=u'P30', tamanho=[ 5, 20]   , raiz=u'//dest',obrigatorio=False)

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += '<dest>'
        xml += self.UF.xml
        xml += self.CNPJ.xml
        xml += self.CPF.xml
        xml += self.IE.xml
        xml += self.idEstrangeiro.xml
        
        xml += '</dest>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.UF.xml = arquivo
            self.CNPJ.xml = arquivo
            self.CPF.xml = arquivo
            self.IE.xml = arquivo
            self.idEstrangeiro.xml = arquivo
            
    xml = property(get_xml, set_xml)


class DetEventoEPEC(DetEvento):
    def __init__(self):
        super(DetEventoEPEC, self).__init__()
        self.versao      = TagDecimal(nome=u'detEvento'  , codigo=u'P18', propriedade=u'versao', valor=u'1.00', raiz=u'/')
        self.descEvento  = TagCaracter(nome=u'descEvento', codigo=u'P19', tamanho=[ 5,  60, 5], raiz=u'//infEvento/detEvento',valor=u'EPEC')
        self.cOrgaoAutor = TagInteiro(nome=u'cOrgaoAutor', codigo=u'P20', tamanho=[2, 2, 2], raiz=u'//infEvento/detEvento')
        self.tpAutor     = TagInteiro(nome=u'tpAutor', codigo=u'P21', tamanho=[1, 1, 1], raiz=u'//infEvento/detEvento')
        self.verAplic    = TagCaracter(nome=u'verAplic', codigo=u'P22' , tamanho=[1, 20]     , raiz=u'//infEvento/detEvento')
        self.dhEmi       = TagDataHoraUTC(nome=u'dhEmi', codigo=u'P23',raiz=u'//infEvento/detEvento')
        self.tpNF        = TagInteiro(nome=u'tpNF', codigo=u'P24', tamanho=[1, 1, 1], raiz=u'//infEvento/detEvento')
        self.IE          = TagCaracter(nome=u'IE', codigo=u'P25', tamanho=[ 2, 14]   , raiz=u'//infEvento/detEvento')
        self.dest        = Dest()
        self.nNF         = TagDecimal(nome=u'vNF', codigo=u'P32', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz=u'//infEvento/detEvento')
        self.vICMS       = TagDecimal(nome=u'vICMS', codigo=u'P33', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz=u'//infEvento/detEvento')
        self.vST         = TagDecimal(nome=u'vST', codigo=u'P34', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz=u'//infEvento/detEvento')

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.versao.xml
        xml += self.descEvento.xml
        xml += self.cOrgaoAutor.xml
        xml += self.tpAutor.xml
        xml += self.verAplic.xml
        xml += self.dhEmi.xml
        xml += self.tpNF.xml
        xml += self.IE.xml
        xml += self.dest.xml
        xml += self.vNF.xml
        xml += self.vICMS.xml
        xml += self.vST.xml

        xml += '</detEvento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo
            self.descEvento.xml = arquivo
            self.cOrgaoAutor.xml = arquivo
            self.tpAutor.xml = arquivo
            self.verAplic.xml = arquivo
            self.dhEmi.xml = arquivo
            self.tpNF.xml = arquivo
            self.IE.xml = arquivo
            self.dest.xml = arquivo
            self.vNF.xml = arquivo
            self.vICMS.xml = arquivo
            self.vST.xml = arquivo
            
    xml = property(get_xml, set_xml)
    

class InfEventoEnviadoEPEC(InfEventoEnviado):
    def __init__(self):
        super(InfEventoEnviadoEPEC, self).__init__()
        self.detEvento = DetEventoEPEC()
    
    
class EventoEPEC(Evento):
    def __init__(self):
        super(EventoEPEC, self).__init__()
        self.infEvento = InfEventoEnviadoEPEC()
    

class EnvEventoEPEC(EnvEvento):
    def __init__(self):
        super(EnvEventoEPEC, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'envEPEC_v1.00.xsd'

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += self.versao.xml
        xml += self.idLote.xml
        
        for ev in self.evento:
            xml += tira_abertura(ev.xml)
            
        xml += u'</envEvento>'

        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml    = arquivo
            self.idLote.xml    = arquivo
            self.evento = self.le_grupo('//envEvento/evento', EventoEPEC)
            
    xml = property(get_xml, set_xml)


class TagChNFePend(TagCaracter):
    def __init__(self, *args, **kwargs):
        super(TagChNFePend, self).__init__(*args, **kwargs)
        self.nome = 'chNFePend'
        self.codigo = 'R25',
        self.tamanho = [44, 44]
        self.raiz = '//infEvento'

class InfEventoRecebidoEPEC(InfEventoRecebido):
    def __init__(self):
        super(InfEventoRecebidoEPEC, self).__init__()
        self.tpEvento = TagCaracter(nome=u'tpEvento'   , codigo=u'HR19', tamanho=[6, 6, 6], raiz=u'//retEnvEvento/retEvento/infEvento',valor=u'110140',obrigatorio=False)
        self.cOrgaoAutor = TagInteiro(nome=u'cOrgaoAutor', codigo=u'R22', tamanho=[2, 2, 2], raiz=u'//retEnvEvento/retEvento/infEvento')
        self.chNFePend = []

    def get_xml(self):
        xml = XMLNFe.get_xml(self)

        if self.Id.xml:
            xml += self.Id.xml
        else:
            xml += u'<infEvento>'
        xml += self.tpAmb.xml
        xml += self.verAplic.xml
        xml += self.cOrgao.xml
        xml += self.cStat.xml
        xml += self.xMotivo.xml
        xml += self.chNFe.xml
        xml += self.tpEvento.xml
        xml += self.xEvento.xml
        xml += self.nSeqEvento.xml
        xml += self.cOrgaoAutor.xml
        xml += self.dhRegEvento.xml
        xml += self.nProt.xml
        
        for c in self.chNFePend:
            xml += c.xml
        
        xml += u'</infEvento>'
        return xml


    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Id.xml = arquivo
            self.tpAmb.xml = arquivo
            self.verAplic.xml = arquivo
            self.cOrgao.xml = arquivo
            self.cStat.xml = arquivo
            self.xMotivo.xml = arquivo
            self.chNFe.xml = arquivo
            self.tpEvento.xml = arquivo
            self.xEvento.xml = arquivo
            self.nSeqEvento.xml = arquivo
            self.cOrgaoAutor.xml = arquivo
            self.dhRegEvento.xml = arquivo
            self.nProt.xml = arquivo
            self.chNFePend = self.le_grupo('//retEnvEvento/retEvento/infEvento/chNFePend', TagChNFePend)

    xml = property(get_xml, set_xml)


class RetEventoEPEC(RetEvento):
    def __init__(self):
        super(RetEventoEPEC, self).__init__()
        self.infEvento = InfEventoRecebidoEPEC()
    
    
class RetEnvEventoEPEC(RetEnvEvento):
    def __init__(self):
        super(RetEnvEventoEPEC, self).__init__()        
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retEnvEPEC_v1.00.xsd'

    def get_xml(self):
        xml = XMLNFe.get_xml(self)

        xml += ABERTURA
        xml += self.versao.xml
        xml += self.idLote.xml
        xml += self.tpAmb.xml
        xml += self.verAplic.xml
        xml += self.cOrgao.xml
        xml += self.cStat.xml
        xml += self.xMotivo.xml

        for r in self.retEvento:
            xml += tira_abertura(r.xml)
            
        xml += u'</retEnvEvento>'

        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo
            self.idLote.xml = arquivo
            self.tpAmb.xml = arquivo
            self.verAplic.xml = arquivo
            self.cOrgao.xml = arquivo
            self.cStat.xml = arquivo
            self.xMotivo.xml = arquivo
            self.retEvento = self.le_grupo('//retEnvEvento/retEvento', RetEventoEPEC)
            
            # Monta o dicionário dos retornos
            for ret in self.retEvento:
                self.dic_retEvento[ret.infEvento.chNFe.valor] = ret

    xml = property(get_xml, set_xml)
    

class ProcEventoNFeEPEC(ProcEventoNFe):
    def __init__(self):
        super(ProcEventoNFeEPEC, self).__init__()
        self.evento = EventoEPEC()
        self.retEvento = RetEventoEPEC()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'procEPEC_v1.00.xsd'
