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

from .confrecebto import MD_CONFIRMACAO_OPERACAO, MD_DESCONHECIMENTO_OPERACAO, MD_OPERACAO_NAO_REALIZADA, MD_CIENCIA_OPERACAO, MD_DESCEVENTO

from .confrecebto import EventoConfRecebimento as EventoConfRecebimento_100
from .confrecebto import EnvEventoConfRecebimento as EnvEventoConfRecebimento_100
from .confrecebto import RetEnvEventoConfRecebimento as RetEnvEventoConfRecebimento_100
from .confrecebto import ProcEventoNFeConfRecebimento as ProcEventoNFeConfRecebimento_100

from .consnfedest import ConsNFeDest as ConsNFeDest_101
from .consnfedest import RetConsNFeDest as RetConsNFeDest_101

from .downloadNFe import DownloadNFe as DownloadNFe_100
from .downloadNFe import RetDownloadNFe as RetDownloadNFe_100

from .downloadNFe import TagChNFe