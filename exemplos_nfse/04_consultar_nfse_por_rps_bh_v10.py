
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
    
    rps = Rps_10()
    
    #Identificação da RPS
    rps.InfRps.IdentificacaoRps.Numero.valor = int(str(datetime.now().year) + '1'.zfill(11))
    rps.InfRps.IdentificacaoRps.Serie.valor = u'00001'
    rps.InfRps.IdentificacaoRps.Tipo.valor = 1
    
    #Identificação do Prestador
    rps.InfRps.Prestador.InscricaoMunicipal.valor = u'1733160024'
    rps.InfRps.Prestador.Cnpj.valor = u'99999999000191'
    
    resultado = mynfse.consultar_nfse_por_rps(rps=rps, cert=info_certificado['cert'], key=info_certificado['key'], ambiente=2, versao=u'1.0', modelo=u'bhiss')
    
    if resultado['msg_retorno'] != u'':
        print('(Rejeitada) Alerta/Erro: ', resultado['msg_retorno'])
    else:
        ''' Retorna um dicionario com o XML de envio e de resposta '''
        for key,value in resultado.items():
            print(str(key) + " : " + str(value))