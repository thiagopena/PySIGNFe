# -*- coding: utf-8 -*-


ESQUEMA_ATUAL = u'PL_CTe_300'

#Envelopes SOAP
from .soap_300 import SOAPEnvio as SOAPEnvio_300
from .soap_300 import SOAPRetorno as SOAPRetorno_300

# Emissão de CT-e 3.00
from .CTe_300 import CTe as CTe_300
from .CTe_300 import InfQ as InfQ_300
from .CTe_300 import InfNF as InfNF_300
from .CTe_300 import InfNFe as InfNFe_300
from .CTe_300 import InfOutros as InfOutros_300
from .CTe_300 import VeicNovos as VeicNovos_300
from .CTe_300 import Comp as Comp_300
from .CTe_300 import Pass as Pass_300
from .CTe_300 import ObsCont as ObsCont_300
from .CTe_300 import ObsFisco as ObsFisco_300
from .CTe_300 import AutXML as AutXML_300
from .CTe_300 import InfCTeMultimodal as InfCTeMultimodal_300
from .CTe_300 import Dup as Dup_300
from .CTe_300 import IdDocAnt as IdDocAnt_300
from .CTe_300 import IdDocAntPap as IdDocAntPap_300
from .CTe_300 import IdDocAntEle as IdDocAntEle_300
from .CTe_300 import EmitDocAnt as EmitDocAnt_300
from .CTe_300 import InfUnidCarga as InfUnidCarga_300
from .CTe_300 import InfUnidTransp as InfUnidTransp_300
from .CTe_300 import LacUnidTransp as LacUnidTransp_300
from .CTe_300 import LacUnidCarga as LacUnidCarga_300

# Envio e retorno Eventos
from .procEventoCTe_300 import EventoCTe as EventoCTe_300
from .procEventoCTe_300 import RetEventoCTe as RetEventoCTe_300
from .procEventoCTe_300 import ProcEventoCTe as ProcEventoCTe_300

# Eventos
from .eventosCTe_300 import EvCancCTe as EvCancCTe_300
from .eventosCTe_300 import EvEPECCTe as EvEPECCTe_300
from .eventosCTe_300 import EvRegMultimodal as EvRegMultimodal_300
from .eventosCTe_300 import EvCCeCTe as EvCCeCTe_300
from .eventosCTe_300 import InfCorrecao as InfCorrecao_300
from .eventosCTe_300 import EvPrestDesacordo as EvPrestDesacordo_300
from .eventosCTe_300 import EvGTV as EvGTV_300

# Consulta Status Servico
from .consStatServCte_300 import ConsStatServCTe    as ConsStatServCTe_300
from .consStatServCte_300 import RetConsStatServCTe as RetConsStatServCTe_300

# Consulta a situação de CT-e
from .consSitCTe_300 import ConsSitCTe as ConsSitCTe_300
from .consSitCTe_300 import RetConsSitCTe as RetConsSitCTe_300


# Envio de lote de CT-e
from .enviCTe_300 import EnviCTe as EnviCTe_300
from .enviCTe_300 import RetEnviCTe as RetEnviCTe_300

# Consulta do recibo do lote de CT-e
from .consReciCTe_300 import ConsReciCTe as ConsReciCTe_300
from .consReciCTe_300 import RetConsReciCTe as RetConsReciCTe_300
from .consReciCTe_300 import ProtCTe as ProtCTe_300
from .consReciCTe_300 import ProcCTe as ProcCTe_300

# Inutilização de CT-e
from .inutCTe_300 import InutCTe as InutCTe_300
from .inutCTe_300 import RetInutCTe as RetInutCTe_300
from .inutCTe_300 import ProcInutCTe as ProcInutCTe_300
