# -*- coding: utf-8 -*-

import os, sys

sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nf_e import nf_e

if __name__ == '__main__':
    nova_nfe = nf_e()
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = nova_nfe.extrair_certificado_a1(arquivo, "associacao")
    
    cnpj = '11111111111111'
    #ie   = '1111111111111'
    
    ##CPF ou CNPJ ou IE
    processo = nova_nfe.consultar_cadastro(cert=info_certificado['cert'], key=info_certificado['key'], cpf_cnpj=cnpj, versao=u'3.10', ambiente=2, estado=u'MG', contingencia=False, salvar_arquivos=True)
    print('Status: ' + processo.resposta.infCons.cStat.valor)
    print('Motivo: ' + processo.resposta.infCons.xMotivo.valor)
    print('Razao: ' + processo.resposta.reason)