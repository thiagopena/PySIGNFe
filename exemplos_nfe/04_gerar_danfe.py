# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from pysignfe.nf_e import nf_e

if __name__ == '__main__':
    nova_nfe = nf_e()
    
    ##Gerar danfe a partir de uma NFe ja processada
    f = open("procNFe_exemplo.xml", encoding='utf8')
    proc_nfe = f.read()
    f.close()
    
    danfe = nova_nfe.gerar_danfe(proc_nfe, nome_sistema=u'PySIGNFe', leiaute_logo_vertical=False, versao='3.10') #logo = 'logo.bmp')
    
    with open("DANFE_retrato_exemplo.pdf", 'wb') as f:
        f.write(danfe)