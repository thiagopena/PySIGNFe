# -*- coding: utf-8 -*-


ESQUEMA_ATUAL = u'PL_009_V4'

#
# Envelopes SOAP
#
from .soap_400 import SOAPEnvio as SOAPEnvio_400
from .soap_400 import SOAPRetorno as SOAPRetorno_400

#
# Emissão de NF-e 4.00
#
from .nfe_400 import NFe as NFe_400
from .nfe_400 import NFRef as NFRef_400
from .nfe_400 import Det as Det_400
from .nfe_400 import DI as DI_400
from .nfe_400 import Adi as Adi_400
from .nfe_400 import Med as Med_400
from .nfe_400 import Arma as Arma_400
from .nfe_400 import Reboque as Reboque_400
from .nfe_400 import Vol as Vol_400
from .nfe_400 import Lacres as Lacres_400
from .nfe_400 import Dup as Dup_400
from .nfe_400 import ObsCont as ObsCont_400
from .nfe_400 import ObsFisco as ObsFisco_400
from .nfe_400 import ProcRef as ProcRef_400

#
# Envio de lote de NF-e
#
from pysignfe.nfe.manual_600 import EnviNFe_310 as EnviNFe_400
from pysignfe.nfe.manual_600 import RetEnviNFe_310 as RetEnviNFe_400

#
# Consulta do recibo do lote de NF-e
#
from pysignfe.nfe.manual_600 import ConsReciNFe_310 as ConsReciNFe_400
from pysignfe.nfe.manual_600 import RetConsReciNFe_310 as RetConsReciNFe_400
from pysignfe.nfe.manual_600 import ProtNFe_310 as ProtNFe_400
from pysignfe.nfe.manual_600 import ProcNFe_310 as ProcNFe_400

#
# Cancelamento de NF-e
#
from pysignfe.nfe.manual_600 import CancNFe_310 as CancNFe_400
from pysignfe.nfe.manual_600 import RetCancNFe_310 as RetCancNFe_400
from pysignfe.nfe.manual_600 import ProcCancNFe_310 as ProcCancNFe_400

#
# Cancelamento de NF-e por EVENTO

from pysignfe.nfe.manual_600 import EventoCancNFe_310 as EventoCancNFe_400
from pysignfe.nfe.manual_600 import EnvEventoCancNFe_310 as EnvEventoCancNFe_400
from pysignfe.nfe.manual_600 import RetEnvEventoCancNFe_310 as RetEnvEventoCancNFe_400
from pysignfe.nfe.manual_600 import ProcEventoNFeCancNFe_310 as ProcEventoNFeCancNFe_400

#
# Carta de Correção EVENTO

from pysignfe.nfe.manual_600 import EventoCCe_310 as EventoCCe_400
from pysignfe.nfe.manual_600 import EnvEventoCCe_310 as EnvEventoCCe_400
from pysignfe.nfe.manual_600 import RetEnvEventoCCe_310 as RetEnvEventoCCe_400
from pysignfe.nfe.manual_600 import ProcEventoNFeCCe_310 as ProcEventoNFeCCe_400

#
# EPEC EVENTO
#
from pysignfe.nfe.manual_600 import EventoEPEC_310 as EventoEPEC_400
from pysignfe.nfe.manual_600 import EnvEventoEPEC_310 as EnvEventoEPEC_400
from pysignfe.nfe.manual_600 import RetEnvEventoEPEC_310 as RetEnvEventoEPEC_400
from pysignfe.nfe.manual_600 import ProcEventoNFeEPEC_310 as ProcEventoNFeEPEC_400

#
# Inutilização de NF-e
#
from pysignfe.nfe.manual_600 import InutNFe_310 as InutNFe_400
from pysignfe.nfe.manual_600 import RetInutNFe_310 as RetInutNFe_400
from pysignfe.nfe.manual_600 import ProcInutNFe_310 as ProcInutNFe_400

#
# Consulta a situação de NF-e
#
from pysignfe.nfe.manual_600 import ConsSitNFe_310 as ConsSitNFe_400
from pysignfe.nfe.manual_600 import RetConsSitNFe_310 as RetConsSitNFe_400

#
# Consulta a situação do serviço
#
from pysignfe.nfe.manual_600 import ConsStatServ_310 as ConsStatServ_400
from pysignfe.nfe.manual_600 import RetConsStatServ_310 as RetConsStatServ_400

#
# Consulta cadastro

from pysignfe.nfe.manual_600 import ConsCad_310 as ConsCad_400
from pysignfe.nfe.manual_600 import RetConsCad_310 as RetConsCad_400

