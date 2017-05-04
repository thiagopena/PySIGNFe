# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nf_e import nf_e

if __name__ == '__main__':
    nova_nfe = nf_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = nova_nfe.extrair_certificado_a1(arquivo, "associacao")
    
    ##Modificar os dados abaixo
    
    #CNPJ do destinatário da NF-e. 
    cnpj = u'99999999000191'
    '''
    Indicador de NF-e consultada:
    0=Todas as NF-e;
    1=Somente as NF-e que ainda não tiveram manifestação do destinatário (Desconhecimento da operação, Operação não Realizada ou Confirmação da Operação);
    2=Idem anterior, incluindo as NF-e que também não tiveram a Ciência da Emissão.
    '''
    indnfe = u'0'
    
    '''
    Indicador do Emissor da NF-e:
    0=Todos os Emitentes / Remetentes;
    1=Somente as NF-e emitidas por emissores/remetentes que não tenham o mesmo CNPJ-Base do destinatário (para excluir as notas fiscais de transferência entre filiais).
    '''
    indemi = u'0'
    
    '''
    Último NSU recebido.
    Caso seja informado com zero, ou com um NSU muito antigo, a consulta retornará unicamente as notas fiscais que tenham sido recepcionadas nos últimos 15 dias.
    '''
    nsu = u'0'
        
    processo = nova_nfe.consultar_nfe_destinatario(cnpj=cnpj, indnfe=indnfe, indemi=indemi, nsu=nsu, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'2.00', ambiente=2, estado=u'MG', contingencia=False)
    
    print('Status: ' + processo.resposta.cStat.valor)
    print('Motivo: ' + processo.resposta.xMotivo.valor)
    print('Razao: ' + processo.resposta.reason)
    
    #if processo.resposta.cStat.valor == '138': #Documento localizado para o destinatário
    #    for resp in processo.resposta.ret:
            #...
                
                
    