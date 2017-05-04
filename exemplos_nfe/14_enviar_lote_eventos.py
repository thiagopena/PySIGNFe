# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nf_e import nf_e
#Eventos: Cancelamento, Carta Correcao, EPEC, Manifestacao destinatario
from pysignfe.nfe.manual_600 import EventoCancNFe_310, EventoCCe_310, EventoEPEC_310


if __name__ == '__main__':
    nova_nfe = nf_e()
    
    #Associacao.pfx nao e valido, utilize um certificado valido
    caminho_certificado = "certificado/Associacao.pfx"
    with open(caminho_certificado, 'rb') as f:
        arquivo = f.read()
    
    info_certificado = nova_nfe.extrair_certificado_a1(arquivo, "associacao")
    
    #Exemplo para evento cancelamento
    lista_eventos = []
    ev1 = EventoCancNFe_310()
    ev1.infEvento.chNFe.valor = u'35100910142785000190552000000000071946226632'
    ev1.infEvento.dhEvento.valor = datetime.now()
    ev1.infEvento.detEvento.nProt.valor = '111111111111111'
    ev1.infEvento.detEvento.xJust.valor = 'Teste evento Cancelamento 1'
    
    lista_eventos.append(ev1)
    
    ev2 = EventoCancNFe_310()
    ev2.infEvento.chNFe.valor = u'42110403452234000145550010000000281765232806'
    ev2.infEvento.dhEvento.valor = datetime.now()
    ev2.infEvento.detEvento.nProt.valor = '111111111111111'
    ev2.infEvento.detEvento.xJust.valor = 'Teste evento Cancelamento 2'
    
    lista_eventos.append(ev2)
    
    #tipo = 'confrec'    ##Manifestacao destinatario
    #tipo = 'epec'       ##EPEC
    #tipo = 'cce'        ##Carta Correcao
    tipo = 'can'        ##Cancelamento
    
    processo = nova_nfe.enviar_lote_evento(lista_eventos=lista_eventos, tipo=tipo, cert=info_certificado['cert'], key=info_certificado['key'], versao=u'3.10', ambiente=2, estado=u'MG', contingencia=False)
    
    print('Status do Lote: ', processo.resposta.cStat.valor)
    print('Motivo do Lote: ', processo.resposta.xMotivo.valor)
        
    ##Resposta de cada evento enviado
    for i,ret in enumerate(processo.resposta.retEvento):
        print('Status resposta: ', ret.infEvento.cStat.valor)
        print('Numero do protocolo: ', ret.infEvento.nProt.valor)
        print('Motivo: ', ret.infEvento.xMotivo.valor)
    