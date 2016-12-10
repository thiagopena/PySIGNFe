# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nfs_e import nfs_e

if __name__ == '__main__':
    mynfse = nfs_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = mynfse.extrair_certificado_a1(arquivo, "associacao")
    
    cnpj = u'99999999000191'
    im = u'1733160024'
    protocolo = u'Ak0591217L2009q000000006'
    
    resultado = mynfse.consultar_situacao_lote_rps(cnpj=cnpj, im=im, protocolo=protocolo, cert=info_certificado['cert'], key=info_certificado['key'], ambiente=2, versao=u'1.0', modelo=u'bhiss', salvar_arquivos=True)
    
    if resultado['msg_retorno'] != u'':
        print('(Rejeitada) Alerta/Erro: ', resultado['msg_retorno'])
    else:
        ''' Retorna um dicionario com o XML de envio e de resposta '''
        for key,value in resultado.items():
            print(str(key) + " : " + str(value))