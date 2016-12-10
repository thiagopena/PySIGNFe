# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

from pysignfe.ct_e import ct_e

if __name__ == '__main__':
    mycte = ct_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = mycte.extrair_certificado_a1(arquivo, "associacao")
       
    ##Modificar os dados abaixo
    cnpj = u'99999999000191'
    chave = u'31161002740755000158571010000000271138052109'
    protocolo = u'135100026181256'
    justificativa = u'Teste de cancelamento de CT-e'
    
    resultados = mycte.cancelar_cte(cnpj=cnpj, chave=chave, protocolo=protocolo, justificativa=justificativa, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.00', ambiente=2, estado=u'MG', tipo_contingencia=False)
    print("\nResultado:\n")
    '''Retorna um dicionario'''
    for key, value in resultados.items():
        print(str(key)+" : "+str(value))