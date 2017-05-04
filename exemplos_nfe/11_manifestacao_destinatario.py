# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nf_e import nf_e

from pysignfe.nfe.manifestacao_destinatario import MD_CONFIRMACAO_OPERACAO, MD_DESCONHECIMENTO_OPERACAO, MD_OPERACAO_NAO_REALIZADA, MD_CIENCIA_OPERACAO

if __name__ == '__main__':
    nova_nfe = nf_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = nova_nfe.extrair_certificado_a1(arquivo, "associacao")
    
    cnpj = u'99999999000191'
    chave = u'35100910142785000190552000000000071946226632'
    
    '''
    Eventos manifestação do destinatário:
    - Confirmação da Operação:    MD_CONFIRMACAO_OPERACAO
    - Desconhecimento da Operação:    MD_DESCONHECIMENTO_OPERACAO
    - Operação Não Realizada:     MD_OPERACAO_NAO_REALIZADA
    - Ciência da Emissão (ou Ciência da Operação):    MD_CIENCIA_OPERACAO
    '''
    tipo_manifesto = MD_CONFIRMACAO_OPERACAO
    #tipo_manifesto = MD_DESCONHECIMENTO_OPERACAO
    #tipo_manifesto = MD_OPERACAO_NAO_REALIZADA
    #tipo_manifesto = MD_CIENCIA_OPERACAO
    
    ##Justificativa é obrigatória caso tipo_evento = MD_OPERACAO_NAO_REALIZADA
    #justificativa = u'Teste manifestacao destinatario operacao nao realizada.'
    #resultados = nova_nfe.efetuar_manifesto(cnpj=cnpj, tipo_manifesto=tipo_manifesto, chave=chave, justificativa=justificativa, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'2.00', ambiente=2, estado=u'MG', tipo_contingencia=False)
    
    #Muitos estados ainda nao implementaram Menisfestacao do destinatario,
    # caso queira enviar para o webservice do estado passe o parametro ambiente_nacional=False
    processo = nova_nfe.efetuar_manifesto(cnpj=cnpj, tipo_manifesto=tipo_manifesto, chave=chave, ambiente_nacional=True, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.10', ambiente=2, estado=u'MG', contingencia=False)
    
    print('Status do Lote: ', processo.resposta.cStat.valor)
    print('Motivo do Lote: ', processo.resposta.xMotivo.valor)    
        
    ##Resposta de cada evento enviado
    for i,ret in enumerate(processo.resposta.retEvento):
        print('Status resposta: ', ret.infEvento.cStat.valor)
        print('Numero do protocolo: ', ret.infEvento.nProt.valor)
        print('Motivo: ', ret.infEvento.xMotivo.valor)
    