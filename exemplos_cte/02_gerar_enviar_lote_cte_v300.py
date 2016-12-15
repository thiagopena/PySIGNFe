# -*- coding: utf-8 -*-

import os, sys
import copy
from datetime import datetime
sys.path.insert(0, os.path.abspath(".."))

from pysignfe.ct_e import ct_e

from pysignfe.cte.v300 import CTe_300, InfQ_300, InfNFe_300, InfNF_300, InfOutros_300
from pysignfe.cte.v300.modais_300 import Multimodal, Duto, Ferrov, Aquav, Aereo, Rodo
from pysignfe.nfe.webservices_flags import UF_CODIGO

if __name__ == '__main__':
    mycte = ct_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = mycte.extrair_certificado_a1(arquivo, "associacao")
    
    ##Montar nota fiscal
    cte  = CTe_300()
    
    #Identificação:
    cte.infCte.ide.cUF.valor        = UF_CODIGO['MG']
    cte.infCte.ide.CFOP.valor       = '6353'
    cte.infCte.ide.natOp.valor      = 'Servico de transporte'
    cte.infCte.ide.mod.valor        = '57'
    cte.infCte.ide.serie.valor      = 101
    cte.infCte.ide.nCT.valor        = 27
    cte.infCte.ide.dhEmi.valor      = datetime(2016, 10, 14)
    #cte.infCte.ide.dhEmi.valor      = datetime.now()
    cte.infCte.ide.tpImp.valor      = 1
    cte.infCte.ide.tpEmis.valor     = 1
    cte.infCte.ide.tpAmb.valor      = 2
    cte.infCte.ide.tpCTe.valor      = 0
    cte.infCte.ide.procEmi.valor    = 0
    cte.infCte.ide.verProc.valor    = 'PySIGNFe'
    cte.infCte.ide.cMunEnv.valor    = '3106200'
    cte.infCte.ide.xMunEnv.valor    = 'Belo Horizonte'
    cte.infCte.ide.UFEnv.valor      = 'MG'
    cte.infCte.ide.modal.valor      = '01'
    cte.infCte.ide.tpServ.valor     = '0'
    cte.infCte.ide.cMunIni.valor    = '3106200'
    cte.infCte.ide.xMunIni.valor    = 'Belo Horizonte'
    cte.infCte.ide.UFIni.valor      = 'MG'
    cte.infCte.ide.cMunFim.valor    = '3543402'
    cte.infCte.ide.xMunFim.valor    = 'Ribeirao Preto'
    cte.infCte.ide.UFFim.valor      = 'SP'
    cte.infCte.ide.retira.valor     = 1
    cte.infCte.ide.indIEToma.valor  = 1
    cte.infCte.ide.tomador.toma.valor  = 0
    
    #Identificação do emitente
    cte.infCte.emit.CNPJ.valor              = '99999999999999'
    cte.infCte.emit.xNome.valor             = 'RAZAO SOCIAL'        
    cte.infCte.emit.xFant.valor             = 'Nome Fantasia'
    cte.infCte.emit.IE.valor                = '111111111111'
    #Endereco emitente
    cte.infCte.emit.enderEmit.xLgr.valor    = 'LOGRADOURO (RUA, PRACA, AVENIDA)'
    cte.infCte.emit.enderEmit.nro.valor     = '140'
    cte.infCte.emit.enderEmit.xCpl.valor    = ''                        
    cte.infCte.emit.enderEmit.xBairro.valor = 'PILAR'
    cte.infCte.emit.enderEmit.cMun.valor    = '3106200'
    cte.infCte.emit.enderEmit.xMun.valor    = 'BELO HORIONTE'
    cte.infCte.emit.enderEmit.UF.valor      = 'MG'
    cte.infCte.emit.enderEmit.CEP.valor     = '30390350'
    cte.infCte.emit.enderEmit.fone.valor    = '3133333333'
    
    #Identificação do remetente
    cte.infCte.rem.CNPJ.valor  = '99999999000191'
    cte.infCte.rem.IE.valor  = '111111111111'
    cte.infCte.rem.xNome.valor = 'CT-E EMITIDO EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL'     #Para homologacao
    #Endereco remetente
    cte.infCte.rem.enderReme.xLgr.valor    = 'RUA DOIS'
    cte.infCte.rem.enderReme.nro.valor     = '140'
    cte.infCte.rem.enderReme.xCpl.valor    = ''
    cte.infCte.rem.enderReme.xBairro.valor = 'BARRO PRETO'
    cte.infCte.rem.enderReme.cMun.valor    = '3106200'
    cte.infCte.rem.enderReme.xMun.valor    = 'BELO HORIZONTE'
    cte.infCte.rem.enderReme.UF.valor      = 'MG'
    cte.infCte.rem.enderReme.CEP.valor     = '30190110'
    cte.infCte.rem.enderReme.cPais.valor   = '1058'
    cte.infCte.rem.enderReme.xPais.valor   = 'Brasil'
    
    #Identificação do destinatario
    cte.infCte.dest.CNPJ.valor  = '99999999000191'
    cte.infCte.dest.IE.valor  = '111111111111'
    cte.infCte.dest.xNome.valor = 'CT-E EMITIDO EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL'     #Para homologacao
    #Endereco remetente
    cte.infCte.dest.enderDest.xLgr.valor    = 'RUA DOIS'
    cte.infCte.dest.enderDest.nro.valor     = '140'
    cte.infCte.dest.enderDest.xCpl.valor    = ''
    cte.infCte.dest.enderDest.xBairro.valor = 'BARRO PRETO'
    cte.infCte.dest.enderDest.cMun.valor    = '3106200'
    cte.infCte.dest.enderDest.xMun.valor    = 'BELO HORIZONTE'
    cte.infCte.dest.enderDest.UF.valor      = 'MG'
    cte.infCte.dest.enderDest.CEP.valor     = '30190110'
    cte.infCte.dest.enderDest.cPais.valor   = '1058'
    cte.infCte.dest.enderDest.xPais.valor   = 'Brasil'
    
    #valores prestação de serviço:
    cte.infCte.vPrest.vTPrest.valor = '3000.00'
    cte.infCte.vPrest.vRec.valor = '3000.00'
    
    #Impostos
    cte.infCte.imp.ICMS.CST.valor = '00'
    cte.infCte.imp.ICMS.vBC.valor = '3000.00'
    cte.infCte.imp.ICMS.pICMS.valor = '12.00'
    cte.infCte.imp.ICMS.vICMS.valor = '360.00'
    
    #informacoes do CTe Normal:
    cte.infCte.infCTeNorm.infCarga.proPred.valor = 'Descricao produto predominante'
    cte.infCte.infCTeNorm.infCarga.vCargaAverb.valor = '169762.10'
    cte.infCte.infCTeNorm.infCarga.vCarga.valor = '169762.10'
    
    #informações dos documentos transportados
    infnf = InfNF_300()
    infnf.mod.valor     = '01'
    infnf.serie.valor   = '1'
    infnf.nDoc.valor    = '29667'
    infnf.dEmi.valor    = datetime(2016, 12, 14)
    infnf.vBC.valor     = '0.00'
    infnf.vICMS.valor   = '0.00'
    infnf.vBCST.valor   = '0.00'
    infnf.vST.valor     = '0.00'
    infnf.vProd.valor   = '7755.23'
    infnf.vNF.valor     = '8918.51'
    infnf.nCFOP.valor   = '6101'
    infnf.nPeso.valor   = '335.200'
    
    cte.infCte.infCTeNorm.infDoc.infNF.append(infnf)
    
    #Informações de quantidades da Carga do CT-e 
    infq = InfQ_300()
    infq.cUnid.valor    = '03'
    infq.tpMed.valor    = 'UNIDADE'
    infq.qCarga.valor   = '10592.0000'
    
    cte.infCte.infCTeNorm.infCarga.infQ.append(infq)
    
    #Informações do modal:
    ##Escolher entre as classes de modais: Duto, Ferrov, Aquav, Aereo, Rodo
    cte.infCte.infCTeNorm.infModal.modal = Rodo()
    cte.infCte.infCTeNorm.infModal.modal.RNTRC.valor = '99999999'
    
    cte.gera_nova_chave()
    
    lista_cte = []
    lista_cte.append(cte.xml)
    
    resultados = mycte.processar_lote_cte(lista_cte=lista_cte, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.00', ambiente=2, estado=u'MG', tipo_contingencia=False, salvar_arquivos=False, consultar_servico=False)
    print("\nResultado:\n")
    '''Retorna um dicionario'''
    for key, value in resultados.items():
        print(str(key)+" : "+str(value))