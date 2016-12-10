# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nfs_e import nfs_e
from pysignfe.nfse.bhiss.v10.Rps import Rps as Rps_10

if __name__ == '__main__':
    mynfse = nfs_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = mynfse.extrair_certificado_a1(arquivo, "associacao")
    
    lista_rps = []
    rps = Rps_10()

    rps.InfRps.DataEmissao.valor = datetime(2016, 10, 14)
    rps.InfRps.Prestador.InscricaoMunicipal.valor = u'1733160024'
    rps.InfRps.Prestador.Cnpj.valor = u'99999999000191'
        
    rps.InfRps.IdentificacaoRps.Numero.valor = int(str(datetime.now().year) + '1'.zfill(11))
    rps.InfRps.IdentificacaoRps.Serie.valor = u'00001'
    rps.InfRps.IdentificacaoRps.Tipo.valor = 1
    rps.InfRps.Status.valor = 1
    rps.InfRps.OptanteSimplesNacional.valor = 1
    rps.InfRps.IncentivadorCultural.valor = 2
    rps.InfRps.NaturezaOperacao.valor = 1
    
    rps.InfRps.Servico.CodigoMunicipio.valor    = 3106200
    rps.InfRps.Servico.Discriminacao.valor      = u'Teste.'
    rps.InfRps.Servico.ItemListaServico.valor   = u'11.01'
    
    #Valores
    rps.InfRps.Servico.Valores.ValorServicos.valor   = u'1000.00'
    rps.InfRps.Servico.Valores.IssRetido.valor      = 1
    rps.InfRps.Servico.Valores.BaseCalculo.valor    = u'1000.00'
    
    lista_rps.append(rps)
    
    resultado = mynfse.processar_lote_rps(lista_rps=lista_rps, cert=info_certificado['cert'], key=info_certificado['key'], ambiente=2, versao=u'1.0', modelo=u'bhiss')
    
    if resultado['msg_retorno'] != u'':
        print('(Rejeitada) Alerta/Erro: ', resultado['msg_retorno'])
    else:
        ''' Retorna um dicionario com o XML de envio e de resposta '''
        for key,value in resultado.items():
            print(str(key) + " : " + str(value))