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
    
    resultado = nova_nfe.consultar_cadastro(uf='MG', cert=info_certificado['cert'], key=info_certificado['key'], cpf_cnpj='11111111111111', inscricao_estadual='1111111111111', versao=u'3.10', ambiente=2, estado=u'MG', tipo_contingencia=False, salvar_arquivos=True)
    print('Status: '+str(resultado['status_resposta']))
    print('Motivo: '+str(resultado['status_motivo']))
    print('Razao: '+str(resultado['reason']))