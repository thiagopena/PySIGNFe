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
    serie = u'200'
    numero = u'7'
    justificativa = u'Teste de inutilizacao de CT-e'
    
    resultados = mycte.inutilizar_cte(cnpj=cnpj, serie=serie, numero=numero, justificativa=justificativa, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.00', ambiente=2, estado=u'SP', tipo_contingencia=False)
    print("\nResultado:\n")
    '''Retorna um dicionario'''
    for key, value in resultados.items():
        print(str(key)+" : "+str(value))