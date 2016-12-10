# -*- coding: utf-8 -*-

import os, sys

sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nfs_e import nfs_e

if __name__ == '__main__':
    mynfse = nfs_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = mynfse.extrair_certificado_a1(arquivo, "associacao")
    
    '''
    Codigo cancelamento:
    1 – Erro na emissão
    2 – Serviço não prestado
    3 – Erro de assinatura
    4 – Duplicidade da nota
    5 – Erro de processamento
    Importante: Os códigos 3 (Erro de assinatura) e 5 (Erro de processamento) são de uso restrito da Administração Tributária Municipal
    '''
    
    resultado = mynfse.cancelar_nfse(codigo_cancelamento='2', numero_nfse=u'000000000000001', cnpj=u'99999999000191', im=u'1733160024', codigo_ibge=3106200, cert=info_certificado['cert'], key=info_certificado['key'], ambiente=2, versao=u'1.0', modelo=u'bhiss')
    
    if resultado['msg_retorno'] != u'':
        print('(Rejeitada) Alerta/Erro: ', resultado['msg_retorno'])
    else:
        ''' Retorna um dicionario com o XML de envio e de resposta '''
        for key,value in resultado.items():
            print(str(key) + " : " + str(value))