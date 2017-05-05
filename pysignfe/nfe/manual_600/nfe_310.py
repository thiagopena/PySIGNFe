# -*- coding: utf-8 -*-

from pysignfe.corr_unicode import *
import os
import locale
import hashlib

from pysignfe.xml_sped import *
from pysignfe.nfe.manual_500 import nfe_310
from pysignfe.nfe.manual_600 import ESQUEMA_ATUAL
from pysignfe.nfe.webservices_3 import CONSULTA_CHAVE_NFCE, CONSULTA_QRCODE_NFCE, ESTADO_SVC_CONTINGENCIA
from pysignfe.nfe.webservices_flags import UF_CODIGO
from pysignfe import __version__

DIRNAME = os.path.dirname(__file__)

class Deduc(nfe_310.Deduc):
    def __init__(self):
        super(Deduc, self).__init__()


class ForDia(nfe_310.ForDia):
    def __init__(self):
        super(ForDia, self).__init__()


class Cana(nfe_310.Cana):
    def __init__(self):
        super(Cana, self).__init__()
        

class IPIDevol(XMLNFe):
    def __init__(self):
        super(IPIDevol, self).__init__()
        self.vIPIDevol = TagDecimal(nome='vIPIDevol', codigo='I50', tamanho=[1,  15, 1], decimais=[0, 2, 2], raiz='//det/impostoDevol/IPI')

    def get_xml(self):
        xml = XMLNFe.get_xml(self)

        if self.vIPIDevol.valor:
            xml += '<IPI>'
            xml += self.vIPIDevol.xml
            xml += '</IPI>'

        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.vIPIDevol.xml = arquivo

    xml = property(get_xml, set_xml)

        
class ImpostoDevol(XMLNFe):
    def __init__(self):
        super(ImpostoDevol, self).__init__()
        self.pDevol = TagDecimal(nome='pDevol', codigo='I50', tamanho=[1,  5, 1], decimais=[0, 2, 2], raiz='//det/impostoDevol')
        self.IPI    = IPIDevol()

    def get_xml(self):
        xml = XMLNFe.get_xml(self)

        if self.pDevol.valor:
            xml += '<impostoDevol>'
            xml += self.pDevol.xml
            xml += self.IPI.xml
            xml += '</impostoDevol>'

        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.pDevol.xml = arquivo

    xml = property(get_xml, set_xml)


class ISSQN(nfe_310.ISSQN):
    def __init__(self):
        super(ISSQN, self).__init__()
        self.vAliq     = TagDecimal(nome='vAliq'    , codigo='U03', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='//det/imposto/ISSQN')
        self.cListServ = TagCaracter(nome='cListServ', codigo='U06', tamanho=[5,  5],                     raiz='//det/imposto/ISSQN')
        #
        # Campos novos da versão 3.10
        #
        self.vDeducao = TagDecimal(nome='vDeducao', codigo='U04', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.vOutro = TagDecimal(nome='vOutro', codigo='U04', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.vDescIncond = TagDecimal(nome='vDescIncond', codigo='U04', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.vDescCond = TagDecimal(nome='vDescCond', codigo='U04', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.vISSRet = TagDecimal(nome='vISSRet', codigo='U04', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.indISS  = TagCaracter(nome='indISS', codigo='U07', tamanho=[1,  1], raiz='//det/imposto/ISSQN')
        self.cServico = TagCaracter(nome='cServico', codigo='U06', tamanho=[1, 20], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.cMun     = TagInteiro(nome='cMun'   , codigo='U05', tamanho=[7, 7, 7], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.cPais    = TagInteiro(nome='cPais'  , codigo='U05', tamanho=[4, 4, 4], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.nProcesso = TagCaracter(nome='indISS', codigo='U07', tamanho=[1, 30], raiz='//det/imposto/ISSQN', obrigatorio=False)
        self.indIncentivo = TagCaracter(nome='indIncentivo', codigo='U07', tamanho=[1, 1], raiz='//det/imposto/ISSQN', valor='2')

    def get_xml(self):
        if not (self.indISS.valor):
            return ''

        xml = XMLNFe.get_xml(self)
        xml += '<ISSQN>'
        xml += self.vBC.xml
        xml += self.vAliq.xml
        xml += self.vISSQN.xml
        xml += self.cMunFG.xml
        xml += self.cListServ.xml
        xml += self.vDeducao.xml
        xml += self.vOutro.xml
        xml += self.vDescIncond.xml
        xml += self.vDescCond.xml
        xml += self.vISSRet.xml
        xml += self.indISS.xml
        xml += self.cServico.xml
        xml += self.cMun.xml
        xml += self.cPais.xml
        xml += self.nProcesso.xml
        xml += self.indIncentivo.xml
        xml += '</ISSQN>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.vBC.xml       = arquivo
            self.vAliq.xml     = arquivo
            self.vISSQN.xml    = arquivo
            self.cMunFG.xml    = arquivo
            self.cListServ.xml = arquivo
            self.vDeducao.xml  = arquivo
            self.vOutro.xml  = arquivo
            self.vDescIncond.xml  = arquivo
            self.vDescCond.xml  = arquivo
            self.vISSRet.xml  = arquivo
            self.indISS.xml  = arquivo
            self.cServico.xml  = arquivo
            self.cMun.xml  = arquivo
            self.cPais.xml  = arquivo
            self.nProcesso.xml  = arquivo
            self.indIncentivo.xml  = arquivo

    xml = property(get_xml, set_xml)

##NT 2015/003
class ICMSUFDest(XMLNFe):
    def __init__(self):
        super(ICMSUFDest, self).__init__()
        self.vBCUFDest = TagDecimal(nome='vBCUFDest', codigo='NA03', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ICMSUFDest')
        self.pFCPUFDest = TagDecimal(nome='pFCPUFDest', codigo='NA05', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='//det/imposto/ICMSUFDest')
        self.pICMSUFDest = TagDecimal(nome='pICMSUFDest', codigo='NA07', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='//det/imposto/ICMSUFDest')
        self.pICMSInter = TagDecimal(nome='pICMSInter', codigo='NA09', tamanho=[1,  5, 1], decimais=[0, 2, 2], raiz='//det/imposto/ICMSUFDest')
        self.pICMSInterPart = TagDecimal(nome='pICMSInterPart', codigo='NA11', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='//det/imposto/ICMSUFDest', valor=40)
        
        self.vFCPUFDest = TagDecimal(nome='vFCPUFDest', codigo='NA13', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ICMSUFDest')
        self.vICMSUFDest = TagDecimal(nome='vICMSUFDest', codigo='N15', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ICMSUFDest')
        self.vICMSUFRemet = TagDecimal(nome='vICMSUFRemet', codigo='N15', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//det/imposto/ICMSUFDest')
        
    def get_xml(self):
        if not (self.vBCUFDest.valor):
            return ''

        xml = XMLNFe.get_xml(self)
        xml += '<ICMSUFDest>'
        xml += self.vBCUFDest.xml
        xml += self.pFCPUFDest.xml
        xml += self.pICMSUFDest.xml
        xml += self.pICMSInter.xml
        xml += self.pICMSInterPart.xml
        xml += self.vFCPUFDest.xml
        xml += self.vICMSUFDest.xml
        xml += self.vICMSUFRemet.xml
        xml += '</ICMSUFDest>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.vBCUFDest.xml       = arquivo
            self.pFCPUFDest.xml       = arquivo
            self.pICMSUFDest.xml       = arquivo
            self.pICMSInter.xml       = arquivo
            self.pICMSInterPart.xml       = arquivo
            self.vFCPUFDest.xml       = arquivo
            self.vICMSUFDest.xml       = arquivo
            self.vICMSUFRemet.xml       = arquivo

    xml = property(get_xml, set_xml)    


class COFINSST(nfe_310.COFINSST):
    def __init__(self):
        super(COFINSST, self).__init__()


class TagCSTCOFINS(nfe_310.TagCSTCOFINS):
    def __init__(self, *args, **kwargs):
        super(TagCSTCOFINS, self).__init__(*args, **kwargs)


class COFINS(nfe_310.COFINS):
    def __init__(self):
        super(COFINS, self).__init__()
        self.pCOFINS = TagDecimal(nome='pCOFINS', codigo='S08', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='')


class PISST(nfe_310.PISST):
    def __init__(self):
        super(PISST, self).__init__()


class TagCSTPIS(nfe_310.TagCSTPIS):
    def __init__(self, *args, **kwargs):
        super(TagCSTPIS, self).__init__(*args, **kwargs)


class PIS(nfe_310.PIS):
    def __init__(self):
        super(PIS, self).__init__()
        self.pPIS = TagDecimal(nome='pPIS', codigo='Q08', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='')

class II(nfe_310.II):
    def __init__(self):
        super(II, self).__init__()


class TagCSTIPI(nfe_310.TagCSTIPI):
    def __init__(self, *args, **kwargs):
        super(TagCSTIPI, self).__init__(*args, **kwargs)


class IPI(nfe_310.IPI):
    def __init__(self):
        super(IPI, self).__init__()
        self.pIPI     = TagDecimal(nome=u'pIPI', codigo=u'O13', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz=u'')

class TagCSOSN(nfe_310.TagCSOSN):
    def __init__(self, *args, **kwargs):
        super(TagCSOSN, self).__init__(*args, **kwargs)


class TagCSTICMS(nfe_310.TagCSTICMS):
    def __init__(self, *args, **kwargs):
        super(TagCSTICMS, self).__init__(*args, **kwargs)
    
    def set_valor(self, novo_valor):
        super(TagCSTICMS, self).set_valor(novo_valor)

        if not self.grupo_icms:
            return None

        #
        # Definimos todas as tags como não obrigatórias
        #
        self.grupo_icms.vICMSDeson.obrigatorio = False
        self.grupo_icms.vICMSOp.obrigatorio = False
        self.grupo_icms.pDif.obrigatorio = False
        self.grupo_icms.vICMSDif.obrigatorio = False

        #
        # Por segurança, zeramos os valores das tags do
        # grupo ICMS ao redefinirmos o código da situação
        # tributária
        #
        self.grupo_icms.vICMSDeson.valor = '0.00'
        self.grupo_icms.vICMSOp.valor = '0.00'
        self.grupo_icms.pDif.valor = '0.00'
        self.grupo_icms.vICMSDif.valor = '0.00'

        #
        # Redefine a raiz para todas as tags do grupo ICMS
        #
        self.grupo_icms.vICMSDeson.raiz  = self.grupo_icms.raiz_tag
        self.grupo_icms.vICMSOp.raiz     = self.grupo_icms.raiz_tag
        self.grupo_icms.pDif.raiz        = self.grupo_icms.raiz_tag
        self.grupo_icms.vICMSDif.raiz    = self.grupo_icms.raiz_tag

    def get_valor(self):
        return self._valor_string

    valor = property(get_valor, set_valor)


class ICMS(nfe_310.ICMS):
    def __init__(self):
        super(ICMS, self).__init__()
        self.CST = TagCSTICMS()
        ##Modifica casas decimais
        self.pRedBC   = TagDecimal(nome='pRedBC'  , codigo='N14', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='')
        self.pICMS    = TagDecimal(nome='pICMS'   , codigo='N16', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='')
        self.pMVAST   = TagDecimal(nome='pMVAST'  , codigo='N19', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='')
        self.pRedBCST = TagDecimal(nome='pRedBCST', codigo='N20', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='')
        self.pICMSST  = TagDecimal(nome='pICMSST' , codigo='N22', tamanho=[1,  5, 1], decimais=[0, 4, 4], raiz='')
        self.pCredSN  = TagDecimal(nome='pCredSN' , codigo='N29', tamanho=[1, 15, 1], decimais=[0, 4, 4], raiz='')
        ##Novas tags
        self.vICMSDeson = TagDecimal(nome='vICMSDeson', codigo='N27a', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='', obrigatorio=False)
        self.vICMSOp    = TagDecimal(nome='vICMSOp', codigo='P16a', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='', obrigatorio=False)
        self.pDif       = TagDecimal(nome='pDif', codigo='P16b', tamanho=[1, 7, 1], decimais=[0, 2, 4], raiz='', obrigatorio=False)
        self.vICMSDif   = TagDecimal(nome='vICMSDif', codigo='P16b', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='', obrigatorio=False)
        #
        # Situação tributária do Simples Nacional
        #
        self.CSOSN = TagCSOSN()
        self.CSOSN.grupo_icms = self
        self.CSOSN.valor = '400'

        #
        # Situação tributária tradicional
        #
        self.CST = TagCSTICMS()
        self.CST.grupo_icms = self
        self.CST.valor = '41'
        
    def get_xml(self):
        #
        # Define as tags baseado no código da situação tributária
        #
        xml = XMLNFe.get_xml(self)
        xml += u'<ICMS><' + self.nome_tag + u'>'
        xml += self.orig.xml

        #
        # Se for regime tradicional (não Simples Nacional)
        #
        if self.regime_tributario != 1:
            xml += self.CST.xml

            if self.CST.valor == u'00':
                xml += self.modBC.xml
                xml += self.vBC.xml
                xml += self.pICMS.xml
                xml += self.vICMS.xml
            elif self.CST.valor == u'10':
                if not self.partilha:
                    xml += self.modBC.xml
                    xml += self.vBC.xml
                    #xml += self.pRedBC.xml
                    xml += self.pICMS.xml
                    xml += self.vICMS.xml
                    xml += self.modBCST.xml

                    # Somente quando for marge de valor agregado
                    if self.modBCST.valor == 4:
                        xml += self.pMVAST.xml

                    xml += self.pRedBCST.xml
                    xml += self.vBCST.xml
                    xml += self.pICMSST.xml
                    xml += self.vICMSST.xml
                else:
                    xml += self.modBC.xml
                    xml += self.vBC.xml
                    xml += self.pRedBC.xml
                    xml += self.pICMS.xml
                    xml += self.vICMS.xml
                    xml += self.modBCST.xml

                    # Somente quando for marge de valor agregado
                    if self.modBCST.valor == 4:
                        xml += self.pMVAST.xml

                    xml += self.pRedBCST.xml
                    xml += self.vBCST.xml
                    xml += self.pICMSST.xml
                    xml += self.vICMSST.xml
                    xml += self.pBCOp.xml
                    xml += self.UFST.xml

            elif self.CST.valor == u'20':
                xml += self.modBC.xml
                xml += self.pRedBC.xml
                xml += self.vBC.xml
                xml += self.pICMS.xml
                xml += self.vICMS.xml
                xml += self.vICMSDeson.xml
                xml += self.motDesICMS.xml

            elif self.CST.valor == u'30':
                xml += self.modBCST.xml

                # Somente quando for marge de valor agregado
                if self.modBCST.valor == 4:
                    xml += self.pMVAST.xml

                xml += self.pRedBCST.xml
                xml += self.vBCST.xml
                xml += self.pICMSST.xml
                xml += self.vICMSST.xml
                xml += self.vICMSDeson.xml
                xml += self.motDesICMS.xml

            elif self.CST.valor in (u'40', u'41', u'50'):
                if self.repasse and self.CST.valor == u'41':
                    xml += self.vBCSTRet.xml
                    xml += self.vICMSSTRet.xml
                    xml += self.vBCSTDest.xml
                    xml += self.vICMSSTDest.xml

                elif self.motDesICMS.valor:
                    xml += self.vICMSDeson.xml
                    xml += self.motDesICMS.xml

            elif self.CST.valor == u'51':
                xml += self.modBC.xml
                xml += self.pRedBC.xml
                xml += self.vBC.xml
                xml += self.pICMS.xml
                xml += self.vICMSOp.xml
                xml += self.pDif.xml
                xml += self.vICMSDif.xml
                xml += self.vICMS.xml

            elif self.CST.valor == u'60':
                xml += self.vBCSTRet.xml
                xml += self.vICMSSTRet.xml

            elif self.CST.valor == u'70':
                xml += self.modBC.xml
                xml += self.pRedBC.xml
                xml += self.vBC.xml
                xml += self.pICMS.xml
                xml += self.vICMS.xml
                xml += self.modBCST.xml

                # Somente quando for marge de valor agregado
                if self.modBCST.valor == 4:
                    xml += self.pMVAST.xml

                xml += self.pRedBCST.xml
                xml += self.vBCST.xml
                xml += self.pICMSST.xml
                xml += self.vICMSST.xml
                xml += self.vICMSDeson.xml
                xml += self.motDesICMS.xml

            elif self.CST.valor == u'90':
                xml += self.modBC.xml
                xml += self.vBC.xml
                xml += self.pRedBC.xml
                xml += self.pICMS.xml
                xml += self.vICMS.xml
                xml += self.modBCST.xml

                # Somente quando for marge de valor agregado
                if self.modBCST.valor == 4:
                    xml += self.pMVAST.xml

                xml += self.pRedBCST.xml
                xml += self.vBCST.xml
                xml += self.pICMSST.xml
                xml += self.vICMSST.xml
                if not self.partilha:
                    xml += self.vICMSDeson.xml
                    xml += self.motDesICMS.xml
                else:
                    xml += self.pBCOp.xml
                    xml += self.UFST.xml

        #
        # O regime tributário é o Simples Nacional
        #
        else:
            xml += self.CSOSN.xml

            if self.CSOSN.valor == u'101':
                xml += self.pCredSN.xml
                xml += self.vCredICMSSN.xml

            elif self.CSOSN.valor in (u'102', u'103', u'300', u'400'):
                pass

            elif self.CSOSN.valor == u'201':
                xml += self.modBCST.xml

                # Somente quando for marge de valor agregado
                if self.modBCST.valor == 4:
                    xml += self.pMVAST.xml

                xml += self.pRedBCST.xml
                xml += self.vBCST.xml
                xml += self.pICMSST.xml
                xml += self.vICMSST.xml
                xml += self.pCredSN.xml
                xml += self.vCredICMSSN.xml

            elif self.CSOSN.valor in (u'202', u'203'):
                xml += self.modBCST.xml

                # Somente quando for marge de valor agregado
                if self.modBCST.valor == 4:
                    xml += self.pMVAST.xml

                xml += self.pRedBCST.xml
                xml += self.vBCST.xml
                xml += self.pICMSST.xml
                xml += self.vICMSST.xml

            elif self.CSOSN.valor == u'500':
                xml += self.vBCSTRet.xml
                xml += self.vICMSSTRet.xml

            elif self.CSOSN.valor == u'900':
                xml += self.modBC.xml
                xml += self.vBC.xml
                xml += self.pRedBC.xml
                xml += self.pICMS.xml
                xml += self.vICMS.xml
                xml += self.modBCST.xml

                # Somente quando for marge de valor agregado
                if self.modBCST.valor == 4:
                    xml += self.pMVAST.xml

                xml += self.pRedBCST.xml
                xml += self.vBCST.xml
                xml += self.pICMSST.xml
                xml += self.vICMSST.xml
                xml += self.pCredSN.xml
                xml += self.vCredICMSSN.xml

        xml += u'</' + self.nome_tag + u'></ICMS>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            #
            # Para ler corretamente o ICMS, primeiro temos que descobrir em
            # qual grupo de situação tributária ele está
            #
            self.partilha = False
            self.repasse  = False
            if self._le_noh(u'//det/imposto/ICMS/ICMS00') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'00'
            elif self._le_noh(u'//det/imposto/ICMS/ICMS10') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'10'
            elif self._le_noh(u'//det/imposto/ICMS/ICMS20') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'20'
            elif self._le_noh(u'//det/imposto/ICMS/ICMS30') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'30'
            elif self._le_noh(u'//det/imposto/ICMS/ICMS40') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'40'
            elif self._le_noh(u'//det/imposto/ICMS/ICMS51') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'51'
            elif self._le_noh(u'//det/imposto/ICMS/ICMS60') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'60'
            elif self._le_noh(u'//det/imposto/ICMS/ICMS70') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'70'
            elif self._le_noh(u'//det/imposto/ICMS/ICMS90') is not None:
                self.regime_tributario = 3
                self.CST.valor = u'90'
            elif self._le_noh(u'//det/imposto/ICMS/ICMSPart') is not None:
                self.regime_tributario = 3
                self.partilha = True
                self.CST.valor = u'10'
            elif self._le_noh(u'//det/imposto/ICMS/ICMSST') is not None:
                self.regime_tributario = 3
                self.repasse = True
                self.CST.valor = u'41'
            elif self._le_noh(u'//det/imposto/ICMS/ICMSSN101') is not None:
                self.regime_tributario = 1
                self.CSOSN.valor = u'101'
            elif self._le_noh(u'//det/imposto/ICMS/ICMSSN102') is not None:
                self.regime_tributario = 1
                self.CSOSN.valor = u'102'
            elif self._le_noh(u'//det/imposto/ICMS/ICMSSN201') is not None:
                self.regime_tributario = 1
                self.CSOSN.valor = u'201'
            elif self._le_noh(u'//det/imposto/ICMS/ICMSSN202') is not None:
                self.regime_tributario = 1
                self.CSOSN.valor = u'202'
            elif self._le_noh(u'//det/imposto/ICMS/ICMSSN500') is not None:
                self.regime_tributario = 1
                self.CSOSN.valor = u'500'
            elif self._le_noh(u'//det/imposto/ICMS/ICMSSN900') is not None:
                self.regime_tributario = 1
                self.CSOSN.valor = u'900'

            #
            # Agora podemos ler os valores tranquilamente...
            #
            self.orig.xml       = arquivo

            if self.regime_tributario == 1:
                self.CSOSN.xml       = arquivo
            else:
                self.CST.xml        = arquivo

            self.modBC.xml      = arquivo
            self.vBC.xml        = arquivo
            self.pRedBC.xml     = arquivo
            self.pICMS.xml      = arquivo
            self.vICMS.xml      = arquivo
            self.modBCST.xml    = arquivo
            self.pMVAST.xml     = arquivo
            self.pRedBCST.xml   = arquivo
            self.vBCST.xml      = arquivo
            self.pICMSST.xml    = arquivo
            self.vICMSST.xml    = arquivo
            self.vBCSTRet.xml   = arquivo
            self.vICMSSTRet.xml = arquivo
            self.vICMSDeson.xml = arquivo
            self.vICMSOp.xml    = arquivo
            self.pDif.xml       = arquivo
            self.vICMSDif.xml   = arquivo

            if self.regime_tributario == 1:
                self.pCredSN.xml     = arquivo
                self.vCredICMSSN.xml = arquivo
            else:
                self.UFST.xml        = arquivo
                self.pBCOp.xml       = arquivo
                self.motDesICMS.xml  = arquivo
                self.vBCSTDest.xml   = arquivo
                self.vICMSSTDest.xml = arquivo
                
    xml = property(get_xml, set_xml)


class Imposto(nfe_310.Imposto):
    def __init__(self):
        super(Imposto, self).__init__()
        self.ICMS     = ICMS()
        self.IPI      = IPI()
        self.PIS      = PIS()
        self.COFINS   = COFINS()
        self.ISSQN    = ISSQN()
        self.ICMSUFDest = ICMSUFDest()
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += '<imposto>'
        xml += self.vTotTrib.xml

        # Enviar ICMS, IPI e II somente quando não for serviço
        if not self.ISSQN.cSitTrib.valor:
            xml += self.ICMS.xml
            xml += self.IPI.xml
            xml += self.II.xml

        xml += self.PIS.xml
        xml += self.PISST.xml
        xml += self.COFINS.xml
        xml += self.COFINSST.xml
        xml += self.ICMSUFDest.xml

        if self.ISSQN.cSitTrib.valor:
            xml += self.ISSQN.xml

        xml += '</imposto>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.vTotTrib.xml = arquivo
            self.ICMS.xml     = arquivo
            self.IPI.xml      = arquivo
            self.II.xml       = arquivo
            self.PIS.xml      = arquivo
            self.PISST.xml    = arquivo
            self.COFINS.xml   = arquivo
            self.COFINSST.xml = arquivo
            self.ICMSUFDest.xml = arquivo
            self.ISSQN.xml    = arquivo

    xml = property(get_xml, set_xml)


class CIDE(nfe_310.CIDE):
    def __init__(self):
        super(CIDE, self).__init__()


class Comb(nfe_310.Comb):
    def __init__(self):
        super(Comb, self).__init__()
        
class Arma(nfe_310.Arma):
    def __init__(self):
        super(Arma, self).__init__()


class Med(nfe_310.Med):
    def __init__(self):
        super(Med, self).__init__()


class VeicProd(nfe_310.VeicProd):
    def __init__(self):
        super(VeicProd, self).__init__()


class Adi(nfe_310.Adi):
    def __init__(self):
        super(Adi, self).__init__()
        self.nDraw =  TagInteiro(nome='nDraw', codigo='I29a', tamanho=[1,  11], raiz='//adi', obrigatorio=False)
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<adi>'
        xml += self.nAdicao.xml
        xml += self.nSeqAdic.xml
        xml += self.cFabricante.xml
        xml += self.vDescDI.xml
        xml += self.nDraw.xml
        xml += u'</adi>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.nAdicao.xml  = arquivo
            self.nSeqAdic.xml = arquivo
            self.cFabricante  = arquivo
            self.vDescDI      = arquivo
            self.nDraw.xml     = arquivo

    xml = property(get_xml, set_xml)
    

class DI(nfe_310.DI):
    def __init__(self):
        super(DI, self).__init__()
        
    def get_xml(self):
        if not self.nDI:
            return ''

        xml = XMLNFe.get_xml(self)
        xml += '<DI>'
        xml += self.nDI.xml
        xml += self.dDI.xml
        xml += self.xLocDesemb.xml
        xml += self.UFDesemb.xml
        xml += self.dDesemb.xml
        xml += self.tpViaTransp.xml
        xml += self.vAFRMM.xml
        xml += self.tpIntermedio.xml
        xml += self.CNPJ.xml
        xml += self.UFTerceiro.xml
        xml += self.cExportador.xml

        for a in self.adi:
            xml += a.xml

        xml += '</DI>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.nDI.xml         = arquivo
            self.dDI.xml         = arquivo
            self.xLocDesemb.xml  = arquivo
            self.UFDesemb.xml    = arquivo
            self.dDesemb.xml     = arquivo
            self.tpViaTransp.xml = arquivo
            self.vAFRMM.xml = arquivo
            self.tpIntermedio.xml = arquivo
            self.CNPJ.xml = arquivo
            self.UFTerceiro.xml = arquivo
            self.cExportador.xml = arquivo

            #
            # Técnica para leitura de tags múltiplas
            # As classes dessas tags, e suas filhas, devem ser
            # "reenraizadas" (propriedade raiz) para poderem ser
            # lidas corretamente
            #
            adis = self._le_nohs('//DI/adi')
            self.adi = []
            if adis is not None:
                self.adi = [Adi() for a in adis]
                for i in range(len(adis)):
                    self.adi[i].xml = adis[i]

    xml = property(get_xml, set_xml)


class ExportInd(nfe_310.ExportInd):
    def __init__(self):
        super(ExportInd, self).__init__()


class DetExport(nfe_310.DetExport):
    def __init__(self):
        super(DetExport, self).__init__()


class Prod(nfe_310.Prod):
    def __init__(self):
        super(Prod, self).__init__()
        self.CEST = TagCaracter(nome='CEST', codigo='I05c', tamanho=[7, 7], raiz='//det/prod', obrigatorio=False)
        self.detExport = []
        self.veicProd = VeicProd()
        self.comb     = Comb()
        self.nRECOPI  = TagCaracter(nome='nRECOPI', codigo='LB01', tamanho=[20, 20, 20], raiz='//det/prod', obrigatorio=False)
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += '<prod>'
        xml += self.cProd.xml
        xml += self.cEAN.xml
        xml += self.xProd.xml
        xml += self.NCM.xml
        xml += self.NVE.xml
        xml += self.CEST.xml
        xml += self.EXTIPI.xml
        #xml += self.genero.xml
        xml += self.CFOP.xml
        xml += self.uCom.xml
        xml += self.qCom.xml
        xml += self.vUnCom.xml
        xml += self.vProd.xml
        xml += self.cEANTrib.xml
        xml += self.uTrib.xml
        xml += self.qTrib.xml
        xml += self.vUnTrib.xml
        xml += self.vFrete.xml
        xml += self.vSeg.xml
        xml += self.vDesc.xml
        xml += self.vOutro.xml
        xml += self.indTot.xml

        for d in self.DI:
            xml += d.xml
        
        for de in self.detExport:
            xml += de.xml

        xml += self.xPed.xml
        xml += self.nItemPed.xml
        xml += self.nFCI.xml
        xml += self.veicProd.xml

        for m in self.med:
            xml += m.xml

        for a in self.arma:
            xml += a.xml

        xml += self.comb.xml
        xml += self.nRECOPI.xml
        xml += '</prod>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.cProd.xml    = arquivo
            self.cEAN.xml     = arquivo
            self.xProd.xml    = arquivo
            self.NCM.xml      = arquivo
            self.NVE.xml      = arquivo
            self.CEST.xml     = arquivo
            self.EXTIPI.xml   = arquivo
            #self.genero.xml   = arquivo
            self.CFOP.xml     = arquivo
            self.uCom.xml     = arquivo
            self.qCom.xml     = arquivo
            self.vUnCom.xml   = arquivo
            self.vProd.xml    = arquivo
            self.cEANTrib.xml = arquivo
            self.uTrib.xml    = arquivo
            self.qTrib.xml    = arquivo
            self.vUnTrib.xml  = arquivo
            self.vFrete.xml   = arquivo
            self.vSeg.xml     = arquivo
            self.vDesc.xml    = arquivo
            self.vOutro.xml   = arquivo
            self.indTot.xml   = arquivo

            #
            # Técnica para leitura de tags múltiplas
            # As classes dessas tags, e suas filhas, devem ser
            # "reenraizadas" (propriedade raiz) para poderem ser
            # lidas corretamente
            #
            self.DI = self.le_grupo('//det/prod/DI', DI)
            self.detExport = self.le_grupo('//det/prod/detExport', DetExport)
            
            self.xPed.xml      = arquivo
            self.nItemPed.xml  = arquivo
            self.nFCI.xml      = arquivo
            self.veicProd.xml  = arquivo

            #
            # Técnica para leitura de tags múltiplas
            # As classes dessas tags, e suas filhas, devem ser
            # "reenraizadas" (propriedade raiz) para poderem ser
            # lidas corretamente
            #
            self.med = self.le_grupo('//det/prod/med', Med)
            self.arma = self.le_grupo('//det/prod/arma', Arma)

            self.comb.xml = arquivo
            self.nRECOPI.xml = arquivo

    xml = property(get_xml, set_xml)

class Det(nfe_310.Det):
    def __init__(self):
        super(Det, self).__init__()
        self.prod       = Prod()
        self.imposto   = Imposto()
        self.impostoDevol = ImpostoDevol()
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.nItem.xml
        xml += self.prod.xml
        xml += self.imposto.xml
        xml += self.impostoDevol.xml
        xml += self.infAdProd.xml
        xml += '</det>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.nItem.xml     = arquivo
            self.prod.xml      = arquivo
            self.imposto.xml   = arquivo
            self.impostoDevol.xml = arquivo
            self.infAdProd.xml = arquivo

    xml = property(get_xml, set_xml)
    

class Compra(nfe_310.Compra):
    def __init__(self):
        super(Compra, self).__init__()
        self.xNEmp = TagCaracter(nome=u'xNEmp', codigo=u'ZB02', tamanho=[1, 22], raiz=u'//NFe/infNFe/compra', obrigatorio=False)


class Exporta(nfe_310.Exporta):
    def __init__(self):
        super(Exporta, self).__init__()
        self.UFSaidaPais   = TagCaracter(nome=u'UFSaidaPais'  , codigo=u'ZA02', tamanho=[2,  2], raiz=u'//NFe/infNFe/exporta', obrigatorio=False)
        self.xLocExporta = TagCaracter(nome=u'xLocExporta', codigo=u'ZA03', tamanho=[1, 60], raiz=u'//NFe/infNFe/exporta', obrigatorio=False)
        self.xLocDespacho = TagCaracter(nome=u'xLocDespacho', codigo=u'ZA04', tamanho=[1, 60], raiz=u'//NFe/infNFe/exporta', obrigatorio=False)
    
    def get_xml(self):
        if not (self.UFSaidaPais.valor or self.xLocExporta.valor):
            return u''

        xml = XMLNFe.get_xml(self)
        xml += u'<exporta>'
        xml += self.UFSaidaPais.xml
        xml += self.xLocExporta.xml
        xml += self.xLocDespacho.xml
        xml += u'</exporta>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.UFSaidaPais.xml   = arquivo
            self.xLocExporta.xml = arquivo
            self.xLocDespacho.xml = arquivo

    xml = property(get_xml, set_xml)
        

class ProcRef(nfe_310.ProcRef):
    def __init__(self):
        super(ProcRef, self).__init__()


class ObsFisco(nfe_310.ObsFisco):
    def __init__(self):
        super(ObsFisco, self).__init__()


class ObsCont(nfe_310.ObsCont):
    def __init__(self):
        super(ObsCont, self).__init__()


class InfAdic(nfe_310.InfAdic):
    def __init__(self):
        super(InfAdic, self).__init__()
        

class Card(nfe_310.Card):
    # Cartoes de credito = NFC-e.
    def __init__(self):
        super(Card, self).__init__()
        

class Pag(nfe_310.Pag):
     # Formas de pagamento NFC-e.
    def __init__(self):
        super(Pag, self).__init__()
        
        
class Dup(nfe_310.Dup):
    def __init__(self):
        super(Dup, self).__init__()


class Fat(nfe_310.Fat):
    def __init__(self):
        super(Fat, self).__init__()
        
        
class Cobr(nfe_310.Cobr):
    def __init__(self):
        super(Cobr, self).__init__()

class Lacres(nfe_310.Lacres):
    def __init__(self):
        super(Lacres, self).__init__()


class Vol(nfe_310.Vol):
    def __init__(self, xml=None):
        super(Vol, self).__init__()


class Reboque(nfe_310.Reboque):
    def __init__(self):
        super(Reboque, self).__init__()


class VeicTransp(nfe_310.VeicTransp):
    def __init__(self):
        super(VeicTransp, self).__init__()


class RetTransp(nfe_310.RetTransp):
    def __init__(self):
        super(RetTransp, self).__init__()
        self.pICMSRet = TagDecimal(nome='vICMSRet', codigo='X14', tamanho=[1, 15, 1], decimais=[0, 4, 4], raiz='//NFe/infNFe/transp/retTransp')


class Transporta(nfe_310.Transporta):
    def __init__(self):
        super(Transporta, self).__init__()


class Transp(nfe_310.Transp):
    def __init__(self):
        super(Transp, self).__init__()
        self.retTransp  = RetTransp()
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<transp>'
        xml += self.modFrete.xml
        xml += self.transporta.xml
        xml += self.retTransp.xml
        xml += self.veicTransp.xml

        if self.balsa.valor:
            xml += self.balsa.xml
        elif self.vagao.valor:
            xml += self.vagao.xml

        for r in self.reboque:
            xml += r.xml

        for v in self.vol:
            xml += v.xml

        xml += u'</transp>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.modFrete.xml   = arquivo
            self.transporta.xml = arquivo
            self.retTransp.xml  = arquivo
            self.veicTransp.xml = arquivo

            #
            # Técnica para leitura de tags múltiplas
            # As classes dessas tags, e suas filhas, devem ser
            # "reenraizadas" (propriedade raiz) para poderem ser
            # lidas corretamente
            #
            self.reboque = self.le_grupo('//NFe/infNFe/transp/reboque', Reboque)

            self.vagao.xml = arquivo
            self.balsa.xml = arquivo

            self.vol = self.le_grupo('//NFe/infNFe/transp/vol', Vol)


    xml = property(get_xml, set_xml)


class RetTrib(nfe_310.RetTrib):
    def __init__(self):
        super(RetTrib, self).__init__()


class ISSQNTot(nfe_310.ISSQNTot):
    def __init__(self):
        super(ISSQNTot, self).__init__()


class ICMSTot(nfe_310.ICMSTot):
    def __init__(self):
        super(ICMSTot, self).__init__()
        ##NT 2015/003
        self.vICMSDeson = TagDecimal(nome='vICMSDeson', codigo='W04a', tamanho=[1, 15, 1], decimais=[1,  2,  2], raiz='//NFe/infNFe/total/ICMSTot')
        self.vFCPUFDest = TagDecimal(nome='vFCPUFDest', codigo='NA13', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//NFe/infNFe/total/ICMSTot', obrigatorio=False)
        self.vICMSUFDest = TagDecimal(nome='vICMSUFDest', codigo='N15', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//NFe/infNFe/total/ICMSTot', obrigatorio=False)
        self.vICMSUFRemet = TagDecimal(nome='vICMSUFRemet', codigo='N15', tamanho=[1, 15, 1], decimais=[0, 2, 2], raiz='//NFe/infNFe/total/ICMSTot', obrigatorio=False)
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += '<ICMSTot>'
        xml += self.vBC.xml
        xml += self.vICMS.xml
        xml += self.vICMSDeson.xml
        xml += self.vFCPUFDest.xml
        xml += self.vICMSUFDest.xml
        xml += self.vICMSUFRemet.xml
        xml += self.vBCST.xml
        xml += self.vST.xml
        xml += self.vProd.xml
        xml += self.vFrete.xml
        xml += self.vSeg.xml
        xml += self.vDesc.xml
        xml += self.vII.xml
        xml += self.vIPI.xml
        xml += self.vPIS.xml
        xml += self.vCOFINS.xml
        xml += self.vOutro.xml
        xml += self.vNF.xml
        xml += self.vTotTrib.xml
        xml += '</ICMSTot>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.vBC.xml     = arquivo
            self.vICMS.xml   = arquivo
            self.vICMSDeson.xml = arquivo
            self.vBCST.xml   = arquivo
            self.vST.xml     = arquivo
            self.vProd.xml   = arquivo
            self.vFrete.xml  = arquivo
            self.vSeg.xml    = arquivo
            self.vDesc.xml   = arquivo
            self.vII.xml     = arquivo
            self.vIPI.xml    = arquivo
            self.vPIS.xml    = arquivo
            self.vCOFINS.xml = arquivo
            self.vOutro.xml  = arquivo
            self.vNF.xml     = arquivo
            self.vTotTrib.xml = arquivo

    xml = property(get_xml, set_xml)


class Total(nfe_310.Total):
    def __init__(self):
        super(Total, self).__init__()
        

class Entrega(nfe_310.Entrega):
    def __init__(self):
        super(Entrega, self).__init__()


class Retirada(nfe_310.Retirada):
    def __init__(self):
        super(Retirada, self).__init__()


class autXML(nfe_310.autXML):
    def __init__(self):
        super(autXML, self).__init__()
        

class EnderDest(nfe_310.EnderDest):
    def __init__(self):
        super(EnderDest, self).__init__()

class Dest(nfe_310.Dest):
    def __init__(self):
        super(Dest, self).__init__()
        self.enderDest = EnderDest()


class Avulsa(nfe_310.Avulsa):
    def __init__(self):
        super(Avulsa, self).__init__()


class EnderEmit(nfe_310.EnderEmit):
    def __init__(self):
        super(EnderEmit, self).__init__()


class Emit(nfe_310.Emit):
    def __init__(self):
        super(Emit, self).__init__()


class RefECF(nfe_310.RefECF):
    def __init__(self):
        super(RefECF, self).__init__()


class RefNFP(nfe_310.RefNFP):
    def __init__(self):
        super(RefNFP, self).__init__()


class RefNF(nfe_310.RefNF):
    def __init__(self):
        super(RefNF, self).__init__()


class NFRef(nfe_310.NFRef):
    def __init__(self):
        super(NFRef, self).__init__()


class Ide(nfe_310.Ide):
    def __init__(self):
        super(Ide, self).__init__()
    

class InfNFe(nfe_310.InfNFe):
    def __init__(self):
        super(InfNFe, self).__init__()
        self.versao   = TagDecimal(nome='infNFe' , codigo='A01', propriedade='versao', raiz='//NFe', namespace=NAMESPACE_NFE, valor='3.10')
        self.ide      = Ide()
        self.emit     = Emit()
        self.avulsa   = Avulsa()
        self.dest     = Dest()
        self.retirada = Retirada()
        self.entrega  = Entrega()
        self.autXML   = []
        self.det      = []
        self.total    = Total()
        self.transp   = Transp()
        self.cobr     = Cobr()
        self.pag = []
        self.infAdic  = InfAdic()
        self.exporta  = Exporta()
        self.compra   = Compra()
        self.cana     = Cana()
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<infNFe versao="' + unicode(self.versao.valor) + u'" Id="' + self.Id.valor + u'">'
        xml += self.ide.xml
        xml += self.emit.xml
        xml += self.avulsa.xml
        xml += self.dest.xml
        xml += self.retirada.xml
        xml += self.entrega.xml

        for aut in self.autXML:
            xml += aut.xml

        for d in self.det:
            xml += d.xml
            
        if self.ide.mod.valor == '65':
            for p in self.pag:
                xml += p.xml

        xml += self.total.xml
        xml += self.transp.xml
        xml += self.cobr.xml
        xml += self.infAdic.xml
        xml += self.exporta.xml
        xml += self.compra.xml
        xml += self.cana.xml
        xml += u'</infNFe>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml   = arquivo
            self.Id.xml       = arquivo
            self.ide.xml      = arquivo
            self.emit.xml     = arquivo
            self.avulsa.xml   = arquivo
            self.dest.xml     = arquivo
            self.retirada.xml = arquivo
            self.entrega.xml  = arquivo

            #
            # Técnica para leitura de tags múltiplas
            # As classes dessas tags, e suas filhas, devem ser
            # "reenraizadas" (propriedade raiz) para poderem ser
            # lidas corretamente
            #
            self.autXML = self.le_grupo('//NFe/infNFe/autXML',autXML)

            self.det = self.le_grupo('//NFe/infNFe/det', Det)
            
            self.pag = self.le_grupo('//NFe/infNFe/pag', Pag)

            self.total.xml    = arquivo
            self.transp.xml   = arquivo
            self.cobr.xml     = arquivo
            self.infAdic.xml  = arquivo
            self.exporta.xml  = arquivo
            self.compra.xml   = arquivo
            self.cana.xml     = arquivo

    xml = property(get_xml, set_xml)
    

#Informacao suplementar, apenas para NFC-e
class InfNFeSupl(XMLNFe):
    def __init__(self):
        super(InfNFeSupl, self).__init__()
        self.qrCode     = TagCaracter(nome=u'qrCode', codigo=u'ZX02', tamanho=[100, 600], raiz=u'//NFe/infNFeSupl')
        self.csc        = ''
        self.cidtoken   = '000001'
        self.nversao    = '100'

    def get_xml(self):
        if not self.qrCode.valor:
            return ''
        xml = XMLNFe.get_xml(self)
        xml += u'<infNFeSupl><![CDATA['
        xml += self.qrCode.xml
        xml += u']]></infNFeSupl>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.qrCode.xml     = arquivo

    xml = property(get_xml, set_xml)
    
    
class NFe(nfe_310.NFe):
    def __init__(self):
        super(NFe, self).__init__()
        self.infNFe = InfNFe()
        
        ##NFC-e
        self.infNFeSupl = InfNFeSupl()
                
        self.Signature = Signature()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'nfe_v3.10.xsd'
    
    def endereco_consulta_chave_nfce(self):
        url_consulta = CONSULTA_CHAVE_NFCE[self.infNFe.emit.enderEmit.UF.valor]
        if url_consulta == '':
            raise ValueError('UF não habilitado para NFC-e')
        return url_consulta
        
    def gera_qrcode_nfce(self):
        
        url_consulta_qrcode = CONSULTA_QRCODE_NFCE[self.infNFe.emit.enderEmit.UF.valor]
        if url_consulta_qrcode == '':
            raise ValueError('UF não habilitado para NFC-e')
        
        ##Montando parametros:
        params_qrcode = u'chNFe=' + unicode(self.chave) + u'&'
        params_qrcode += u'nVersao=' + unicode(self.infNFeSupl.nversao) + u'&'
        params_qrcode += u'tpAmp=' + unicode(self.infNFe.ide.tpAmb.valor) + u'&'
        if (self.infNFe.dest.CPF.valor or self.infNFe.dest.CNPJ.valor or self.infNFe.dest.idEstrangeiro.valor):
            params_qrcode += u'cDest=' + unicode(self.infNFe.dest.CPF.valor or self.infNFe.dest.CNPJ.valor or self.infNFe.dest.idEstrangeiro.valor) + u'&'
        
        ##Converter dhEmi e o digest para Hex:
        dhemi_hex = "".join("{:02x}".format(ord(c)) for c in self.infNFe.ide.dhEmi.valor.isoformat())
        digval_hex = "".join("{:02x}".format(ord(c)) for c in self.Signature.DigestValue)
        
        params_qrcode += u'dhEmi=' + unicode(dhemi_hex) + u'&'
        params_qrcode += u'vNF=' + unicode(self.infNFe.total.ICMSTot.vNF.valor) + u'&'
        params_qrcode += u'vICMS=' + unicode(self.infNFe.total.ICMSTot.vICMS.valor) + u'&'
        params_qrcode += u'digVal=' + unicode(digval_hex) + u'&'
        params_qrcode += u'cIdToken=' + unicode(self.infNFeSupl.cidtoken.zfill(6)) + u'&'
        
        ##Calcular cHashQRCode
        hash_string = params_qrcode + self.infNFeSupl.csc
        hash_object = hashlib.sha1(hash_string.encode('utf-8'))
        chash_qrcode = hash_object.hexdigest()
        
        params_qrcode += u'cHashQRCode=' + unicode(chash_qrcode)
        
        params_qrcode = url_consulta_qrcode + params_qrcode
                
        self.infNFeSupl.qrCode.valor = params_qrcode
    
    def preencher_campos_nfce(self):
        self.infNFe.ide.mod.valor = '65'
        #self.infNFe.ide.indFinal.valor = '1'
        #self.infNFe.dest.indIEDest.valor = '9'
    
    def preencher_campos_nfe(self):
        self.infNFe.ide.mod.valor = '55'
        #self.infNFe.ide.indFinal.valor = '0'

