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
    #cnpj = u'99999999000191'
    chave = u'31170102740755000158551010000000381017738769'
    protocolo = u'131170127492528'
    justificativa = u'Teste de cancelamento de NF-e'
    
    processo = nova_nfe.cancelar_nota(chave=chave, protocolo=protocolo, justificativa=justificativa, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.10', ambiente=2, estado=u'MG', contingencia=False)
    
    print('Status do Lote: ', processo.resposta.cStat.valor)
    print('Motivo do Lote: ', processo.resposta.xMotivo.valor)    
        
    ##Resposta de cada evento enviado
    for i,ret in enumerate(processo.resposta.retEvento):
        print('Status resposta: ', ret.infEvento.cStat.valor)
        print('Numero do protocolo: ', ret.infEvento.nProt.valor)
        print('Motivo: ', ret.infEvento.xMotivo.valor)
    