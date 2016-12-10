# -*- coding: utf-8 -*-

import os, sys

sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nfs_e import nfs_e
from pysignfe.nfse.bhiss.v10.Nfse import NFSe as NFSe_10

if __name__ == '__main__':
    mynfse = nfs_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = mynfse.extrair_certificado_a1(arquivo, "associacao")
    
    nfse = NFSe_10()
    
    nfse.InfNfse.PrestadorServico.IdentificacaoPrestador.Cnpj.valor = u'99999999000191'
    nfse.InfNfse.PrestadorServico.IdentificacaoPrestador.InscricaoMunicipal.valor = u'1733160024'
    nfse.InfNfse.Numero.valor = u'000000000000001'
    
    nfse.InfNfse.TomadorServico.IdentificacaoTomador.CpfCnpj.Cnpj.valor = u'99999999000191'
    nfse.InfNfse.TomadorServico.IdentificacaoTomador.InscricaoMunicipal.valor = u'1733160032'
    
    nfse.InfNfse.IntermediarioServico.RazaoSocial.valor = u'Razao Social Teste'
    nfse.InfNfse.IntermediarioServico.CpfCnpj.Cnpj.valor = u'99999999000191'
    nfse.InfNfse.IntermediarioServico.InscricaoMunicipal.valor = u'1733160032'
    
    resultado = mynfse.consultar_nfse(nfse=nfse, cert=info_certificado['cert'], key=info_certificado['key'], ambiente=2, versao=u'1.0', modelo=u'bhiss')
    
    if resultado['msg_retorno'] != u'':
        print('(Rejeitada) Alerta/Erro: ', resultado['msg_retorno'])
    else:
        ''' Retorna um dicionario com o XML de envio e de resposta '''
        for key,value in resultado.items():
            print(str(key) + " : " + str(value))