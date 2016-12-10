# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

from pysignfe.ct_e import ct_e
from pysignfe.cte.v300 import InfCorrecao_300

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
    sequencia = 1
    
    ##Correcoes:
    correcoes = []
    corr1 = InfCorrecao_300()
    corr1.grupoAlterado.valor = u'ide'
    corr1.campoAlterado.valor = u'mod'
    corr1.valorAlterado.valor = u'57'
    
    correcoes.append(corr1)
    
    corr2 = InfCorrecao_300()
    corr2.grupoAlterado.valor = u'rem'
    corr2.campoAlterado.valor = u'CNPJ'
    corr2.valorAlterado.valor = u'99999999000191'
    
    correcoes.append(corr2)
    
    resultados = mycte.emitir_carta_correcao(chave=chave, cnpj=cnpj, correcoes=correcoes, sequencia=sequencia, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.00', ambiente=2, estado=u'MG', tipo_contingencia=False)
    
    print("\nResultado:\n")
    '''Retorna um dicionario'''
    for key, value in resultados.items():
        print(str(key)+" : "+str(value))