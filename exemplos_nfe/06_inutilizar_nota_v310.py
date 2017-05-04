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
    cnpj = u'99999999000191'
    serie = u'101'
    numero = u'27'
    justificativa = u'Teste de inutilizacao de NF-e'
    
    processo = nova_nfe.inutilizar_nota(cnpj=cnpj, serie=serie, numero=numero, justificativa=justificativa, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.10', ambiente=2, estado=u'MG', contingencia=False)
    
    print('Status: ' + processo.resposta.infInut.cStat.valor)
    print('Motivo: ' + processo.resposta.infInut.xMotivo.valor)
    print('Razao: ' + processo.resposta.reason)