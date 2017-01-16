# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nf_e import nf_e

if __name__ == '__main__':
    nova_nfe = nf_e()
    
    ##Gerar danfce a partir de uma NFCe ja processada
    f = open("procNFCe_exemplo.xml", encoding='utf8')
    proc_nfce = f.read()
    f.close()
    
    ##Código de Segurança do Contribuinte(CSC): 36 caracteres
    danfe = nova_nfe.gerar_danfce(proc_nfce, csc='111111111111111111111111111111111111', cidtoken='000001', versao='3.10')
    
    ##Arquivo de saida
    with open("DANFCE.pdf", 'wb') as f:
        f.write(danfe)