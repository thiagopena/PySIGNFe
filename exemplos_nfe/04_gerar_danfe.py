# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nf_e import nf_e

if __name__ == '__main__':
    nova_nfe = nf_e()
    
    ##Gerar danfe a partir de uma NFe ja processada
    #f = open("procNFe_danfe_paisagem.xml", encoding='utf8')
    f = open("procNFe_danfe_retrato.xml", encoding='utf8')
    nfe_str = f.read()
    f.close()
    
    danfe = nova_nfe.gerar_danfe(nfe_str, nome_sistema=u'PySIGNFe', leiaute_logo_vertical=False, versao='2.00') #logo = 'logo.bmp')
    
    #with open("DANFE_paisagem_exemplo.pdf", 'wb') as f:
    with open("DANFE_retrato_exemplo.pdf", 'wb') as f:
        f.write(danfe)