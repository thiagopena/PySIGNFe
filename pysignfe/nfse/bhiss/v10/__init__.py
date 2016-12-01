# -*- coding: utf-8 -*-


# Envelopes SOAP
from .soap import SOAPEnvio as SOAPEnvio_10
from .soap import SOAPRetorno as SOAPRetorno_10


#Consulta situação de lote RPS
from .ConsultarSituacaoLoteRps import ConsultarSituacaoLoteRpsEnvio as ConsultarSituacaoLoteRpsEnvio_10
from .ConsultarSituacaoLoteRps import ConsultarSituacaoLoteRpsResposta as ConsultarSituacaoLoteRpsResposta_10

#Consulta lote RPS
from .ConsultarLoteRps import ConsultarLoteRpsEnvio as ConsultarLoteRpsEnvio_10
from .ConsultarLoteRps import ConsultarLoteRpsResposta as ConsultarLoteRpsResposta_10

#Consultar NFS-e por RPS
from .ConsultarNfsePorRps import ConsultarNfseRpsEnvio as ConsultarNfseRpsEnvio_10
from .ConsultarNfsePorRps import ConsultarNfseRpsResposta as ConsultarNfseRpsResposta_10

#Enviar lote de RPS
from .EnviarLoteRps import EnviarLoteRpsEnvio as EnviarLoteRpsEnvio_10
from .EnviarLoteRps import EnviarLoteRpsResposta as EnviarLoteRpsResposta_10

#Gerar Nfse
from .GerarNfse import GerarNfseEnvio as GerarNfseEnvio_10
from .GerarNfse import GerarNfseResposta as GerarNfseResposta_10

#Consultar NFS-e
from .ConsultarNfse import ConsultarNfseEnvio as ConsultarNfseEnvio_10
from .ConsultarNfse import ConsultarNfseResposta as ConsultarNfseResposta_10

#Cancelar NFS-e
from .CancelarNfse import CancelarNfseEnvio as CancelarNfseEnvio_10
from .CancelarNfse import CancelarNfseResposta as CancelarNfseResposta_10