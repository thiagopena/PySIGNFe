# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nf_e import nf_e

if __name__ == '__main__':
    nova_nfe = nf_e()
    
    ##Gerar danfe a partir de uma NFCe ja processada
    f = open("NFCe_proc_danfe_exemplo.xml", encoding='utf8')
    nfce_str = f.read()
    f.close()
    
    ##CSC: 36 caracteres
    danfe = nova_nfe.gerar_danfe_consumidor(nfce_str, csc='111111111111111111111111111111111111', cidtoken='000001', versao='3.10')
    
    ##Arquivo de saida
    with open("DANFE_NFCe.pdf", 'wb') as f:
        f.write(danfe)