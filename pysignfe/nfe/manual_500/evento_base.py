# -*- coding: utf-8 -*-

from pysignfe.xml_sped import *

import os

DIRNAME = os.path.dirname(__file__)

class DetEvento(XMLNFe):
    def __init__(self):
        super(DetEvento, self).__init__()
        self.versao     = TagDecimal(nome=u'detEvento'  , codigo=u'HP18', propriedade=u'versao', valor=u'1.00', raiz=u'/')

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.versao.xml
        
        xml += '</detEvento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo

    xml = property(get_xml, set_xml)
    

class InfEventoEnviado(XMLNFe):
    def __init__(self):
        super(InfEventoEnviado, self).__init__()
        self.Id    = TagCaracter(nome=u'infEvento', codigo=u'HP06', tamanho=[54, 54]    , raiz=u'//envEvento', propriedade=u'Id')
        self.cOrgao  = TagInteiro(nome=u'cOrgao'      , codigo=u'HP08', tamanho=[2, 2,2]   , raiz=u'//envEvento/infEvento', valor=91)
        self.tpAmb = TagInteiro(nome=u'tpAmb'   , codigo=u'HP09', tamanho=[ 1,  1, 1] , raiz=u'//envEvento/infEvento', valor=2)
        self.CNPJ    = TagCaracter(nome=u'CNPJ'   , codigo=u'HP10' , tamanho=[ 0, 14]   , raiz=u'//envEvento/infEvento')
        self.CPF     = TagCaracter(nome=u'CPF'    , codigo=u'HP11', tamanho=[11, 11]   , raiz=u'//envEvento/infEvento')
        self.chNFe = TagCaracter(nome=u'chNFe'   , codigo=u'HP12', tamanho=[44, 44, 44], raiz=u'//envEvento/infEvento')
        self.dhEvento = TagDataHoraUTC(nome=u'dhEvento', codigo=u'HP13' , raiz=u'//envEvento/infEvento')
        self.tpEvento = TagCaracter(nome=u'tpEvento'   , codigo=u'HP14', tamanho=[6, 6, 6], raiz=u'//envEvento/infEvento')
        self.nSeqEvento = TagInteiro(nome=u'nSeqEvento'   , codigo=u'HP15', tamanho=[1,2], raiz=u'//envEvento/infEvento', valor=1)
        self.verEvento = TagDecimal(nome=u'verEvento'   , codigo=u'HP16', raiz=u'//envEvento/infEvento', valor=u'1.00')
        self.detEvento = DetEvento()

    def get_xml(self):

        xml = XMLNFe.get_xml(self)

        self.Id.valor = u'ID' + self.tpEvento.valor + self.chNFe.valor +  ("%02d" % self.nSeqEvento.valor)

        xml += self.Id.xml
        xml += self.cOrgao.xml
        xml += self.tpAmb.xml
        if self.CNPJ.valor:
            xml += self.CNPJ.xml
        else:
            xml += self.CPF.xml
        xml += self.chNFe.xml
        xml += self.dhEvento.xml
        xml += self.tpEvento.xml
        xml += self.nSeqEvento.xml
        xml += self.verEvento.xml
        xml += self.detEvento.xml
        xml += u'</infEvento>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Id.xml = arquivo
            self.cOrgao.xml = arquivo
            self.tpAmb.xml = arquivo
            self.CNPJ.xml = arquivo
            self.CPF.xml = arquivo
            self.chNFe.xml = arquivo
            self.dhEvento.xml = arquivo
            self.tpEvento.xml = arquivo
            self.nSeqEvento.xml = arquivo
            self.verEvento.xml = arquivo
            self.detEvento.xml = arquivo

    xml = property(get_xml, set_xml)
    
    
class Evento(XMLNFe):
    def __init__(self):
        super(Evento, self).__init__()
        self.versao    = TagDecimal(nome=u'evento', codigo=u'HP05', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'1.00', raiz=u'/')
        self.infEvento = InfEventoEnviado()
        self.Signature = Signature()

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += self.versao.xml
        xml += self.infEvento.xml
        #
        # Define a URI a ser assinada
        #
        self.Signature.URI = u'#' + self.infEvento.Id.valor

        xml += self.Signature.xml
        xml += u'</evento>'

        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml    = arquivo
            self.infEvento.xml = arquivo
            self.Signature.xml = self._le_noh('//evento/sig:Signature')
            
    xml = property(get_xml, set_xml)


class EnvEvento(XMLNFe):
    def __init__(self):
        super(EnvEvento, self).__init__()
        self.versao    = TagDecimal(nome=u'envEvento', codigo=u'HP01', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'1.00', raiz=u'/')
        self.idLote    = TagInteiro(nome=u'idLote', codigo=u'HP03', tamanho=[1, 15]    , raiz=u'//envEvento', valor=1)
        self.evento    = []
        
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
            self.evento = self.le_grupo('//envEvento/evento', Evento)
            
    xml = property(get_xml, set_xml)


class InfEventoRecebido(XMLNFe):
    def __init__(self):
        super(InfEventoRecebido, self).__init__()
        self.Id    = TagCaracter(nome=u'infEvento', codigo=u'HR11', tamanho=[17, 17]    , raiz=u'//retEvento', propriedade=u'Id',obrigatorio=False)
        self.tpAmb = TagInteiro(nome=u'tpAmb'   , codigo=u'HR13', tamanho=[ 1,  1, 1] , raiz=u'//retEvento/infEvento')
        self.verAplic = TagCaracter(nome=u'verAplic', codigo=u'HR14' , tamanho=[1, 20]     , raiz=u'//retEvento/infEvento')
        self.cOrgao  = TagInteiro(nome=u'cOrgao'      , codigo=u'HR15', tamanho=[2, 2,2]   , raiz=u'//retEvento/infEvento' )
        self.cStat    = TagCaracter(nome=u'cStat'    , codigo=u'HR16' , tamanho=[3, 3, 3]   , raiz=u'//retEvento/infEvento')
        self.xMotivo  = TagCaracter(nome=u'xMotivo' , codigo=u'HR17' , tamanho=[1, 255]    , raiz=u'//retEvento/infEvento')
        self.chNFe = TagCaracter(nome=u'chNFe'   , codigo=u'HR18', tamanho=[44, 44, 44], raiz=u'//retEvento/infEvento',obrigatorio=False)
        self.tpEvento = TagCaracter(nome=u'tpEvento'   , codigo=u'HR19', tamanho=[6, 6, 6], raiz=u'//retEvento/infEvento', obrigatorio=False)
        self.xEvento  = TagCaracter(nome=u'xEvento'   , codigo=u'HR20' , tamanho=[ 5, 60]   , raiz=u'//retEvento/infEvento', obrigatorio=False)
        self.nSeqEvento = TagInteiro(nome=u'nSeqEvento'   , codigo=u'HR21', tamanho=[2,2], raiz=u'//retEvento/infEvento',obrigatorio=False, valor=1)
        self.CNPJDest  = TagCaracter(nome=u'CNPJDest'   , codigo=u'HR22' , tamanho=[ 0, 14]   , raiz=u'//retEvento/infEvento',obrigatorio=False)
        self.CPFDest  = TagCaracter(nome=u'CPFDest'    , codigo=u'HR23', tamanho=[11, 11]   , raiz=u'//retEvento/infEvento',obrigatorio=False)
        self.emailDest = TagCaracter(nome=u'emailDest'   , codigo=u'HR24' , tamanho=[ 1, 60]   , raiz=u'//retEvento/infEvento',obrigatorio=False)
        self.dhRegEvento = TagDataHoraUTC(nome=u'dhRegEvento', codigo=u'HR25' ,  tamanho=[ 0, 30],raiz=u'//retEvento/infEvento')
        self.nProt    = TagCaracter(nome=u'nProt'    , codigo=u'HR26' , tamanho=[15, 15, 15], raiz=u'//retEvento/infEvento',obrigatorio=False)

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
        
        if self.CNPJDest.valor:
            xml += self.CNPJDest.xml
        elif self.CPFDest.valor:
            xml += self.CPFDest.xml
            
        xml += self.emailDest.xml
        xml += self.dhRegEvento.xml
        xml += self.nProt.xml
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
            self.CNPJDest.xml = arquivo
            self.CPFDest.xml = arquivo
            self.emailDest.xml = arquivo
            self.dhRegEvento.xml = arquivo
            self.nProt.xml = arquivo

    xml = property(get_xml, set_xml)


class RetEvento(XMLNFe):
    def __init__(self):
        super(RetEvento, self).__init__()
        self.versao    = TagDecimal(nome=u'retEvento',propriedade=u'versao', codigo=u'HR10',  namespace=NAMESPACE_NFE, valor=u'1.00', raiz=u'/')
        self.infEvento = InfEventoRecebido()
        self.Signature = Signature()

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += self.versao.xml
        xml += self.infEvento.xml
        
        if len(self.Signature.URI) and (self.Signature.URI.strip() != u'#'):
            xml += self.Signature.xml

        xml += u'</retEvento>'

        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo
            self.infEvento.xml = arquivo
            self.Signature.xml = self._le_noh('//retEvento/sig:Signature')

    xml = property(get_xml, set_xml)
    
    
class RetEnvEvento(XMLNFe):
    def __init__(self):
        super(RetEnvEvento, self).__init__()
        self.versao    = TagDecimal(nome=u'retEnvEvento',propriedade=u'versao', codigo=u'HR01',  namespace=NAMESPACE_NFE, valor=u'1.00', raiz=u'/')
        self.idLote    = TagInteiro(nome=u'idLote', codigo=u'HR03', tamanho=[1, 15]    , raiz=u'//retEnvEvento', valor=1)
        self.tpAmb = TagInteiro(nome=u'tpAmb'   , codigo=u'HR04', tamanho=[ 1,  1, 1] , raiz=u'//retEnvEvento', valor=2)
        self.verAplic = TagCaracter(nome=u'verAplic', codigo=u'HR05' , tamanho=[1, 20]     , raiz=u'//retEnvEvento')
        self.cOrgao  = TagInteiro(nome=u'cOrgao'      , codigo=u'HR06', tamanho=[2, 2, 2]   , raiz=u'//retEnvEvento' )
        self.cStat    = TagCaracter(nome=u'cStat'    , codigo=u'HR07' , tamanho=[3, 3, 3]   , raiz=u'//retEnvEvento')
        self.xMotivo  = TagCaracter(nome=u'xMotivo' , codigo=u'HR08' , tamanho=[1, 255]    , raiz=u'//retEnvEvento')
        #self.ret_evento_versao = TagDecimal(nome=u'retEvento', codigo=u'HR09', raiz=u'//retEnvEvento', valor=u'1.00',  propriedade=u'versao')
        self.retEvento = []
        
        #
        # Dicionário dos retornos, com a chave sendo a chave da NF-e
        #
        self.dic_retEvento = {}
        #
        # Dicionário dos processos (evento + retorno), com a chave sendo a chave da NF-e
        #
        self.dic_procEvento = {}
        
        #self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        #self.arquivo_esquema = u'retEnvEventoCancNFe_v1.00.xsd'

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
            self.retEvento = self.le_grupo('//retEnvEvento/retEvento', RetEvento)
            
            # Monta o dicionário dos retornos
            for ret in self.retEvento:
                self.dic_retEvento[ret.infEvento.chNFe.valor] = ret

    xml = property(get_xml, set_xml)
    

class ProcEventoNFe(XMLNFe):
    def __init__(self):
        super(ProcEventoNFe, self).__init__()
        #
        # Atenção --- a tag procEventoNFe tem que começar com letra minúscula, para
        # poder validar no XSD.
        #
        self.versao = TagDecimal(nome=u'procEventoNFe', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'1.00', raiz=u'/')
        self.evento = Evento()
        self.retEvento = RetEvento()
        #self.caminho_esquema = os.path.join(DIRNAME, u'schema', ESQUEMA_ATUAL + u'/')
        #self.arquivo_esquema = u'procEventoCancNFe_v1.00.xsd'

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += self.versao.xml
        xml += self.evento.xml.replace(ABERTURA, '')
        xml += self.retEvento.xml.replace(ABERTURA, '')
        xml += '</procEventoNFe>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.evento.xml = arquivo
            self.retEvento.xml = arquivo

    xml = property(get_xml, set_xml)
