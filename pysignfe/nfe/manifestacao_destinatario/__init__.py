# -*- coding: utf-8 -*-

ESQUEMA_ATUAL = u'pl'


#
# Envelopes SOAP
#
#from manual_401 import SOAPEnvio as SOAPEnvio_200
#from manual_401.soap_200 import SOAPRetorno as SOAPRetorno_200
#
#from soap_200 import SOAPEnvio as SOAPEnvio_200
#from soap_200 import SOAPRetorno as SOAPRetorno_200

MD_CONFIRMACAO_OPERACAO     = u'210200'
MD_DESCONHECIMENTO_OPERACAO = u'210220'
MD_OPERACAO_NAO_REALIZADA   = u'210240'
MD_CIENCIA_OPERACAO         = u'210210'

MD_DESCEVENTO = {
    MD_CONFIRMACAO_OPERACAO: 'Confirmacao da Operacao',
    MD_CIENCIA_OPERACAO: 'Ciencia da Operacao',
    MD_DESCONHECIMENTO_OPERACAO: 'Desconhecimento da Operacao',
    MD_OPERACAO_NAO_REALIZADA: 'Operacao nao Realizada',
}

from .confrecebto import EnvConfRecebto as EnvConfRecebto_200
from .confrecebto import RetEnvConfRecebto as RetEnvConfRecebto_200
from .confrecebto import ProcEventoNFe as ProcEventoNFeRecebto_200

from .consnfedest import ConsNFeDest as ConsNFeDest_200
from .consnfedest import RetConsNFeDest as RetConsNFeDest_200

from .downloadNFe import DownloadNFe as DownloadNFe_200
from .downloadNFe import RetDownloadNFe as RetDownloadNFe_200

from .downloadNFe import TagChNFe