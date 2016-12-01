# -*- coding: utf-8 -*-

from .webservices_flags import *

METODO_WS = {
    WS_NFSE_CONSULTAR_SIT_LOTE_RPS:{
        u'webservice': u'nfse',
        u'metodo'    : u'ConsultarSituacaoLoteRps',
    },
    WS_NFSE_CONSULTAR_NFSE_POR_RPS:{
        u'webservice': u'nfse',
        u'metodo'    : u'ConsultarNfsePorRps',
    },
    WS_NFSE_RECEPCIONAR_LOTE_RPS:{
        u'webservice': u'nfse',
        u'metodo'    : u'RecepcionarLoteRps',
    },
    WS_NFSE_CONSULTAR_LOTE_RPS:{
        u'webservice': u'nfse',
        u'metodo'    : u'ConsultarLoteRps',
    },
    WS_NFSE_GERAR_NFSE:{
        u'webservice': u'nfse',
        u'metodo'    : u'GerarNfse',
    },
    WS_NFSE_CONSULTAR_NFSE:{
        u'webservice': u'nfse',
        u'metodo'    : u'ConsultarNfse',
    },
    WS_NFSE_CANCELAR_NFSE:{
        u'webservice': u'nfse',
        u'metodo'    : u'CancelarNfse',
    },
}

WEBSERVICES_BH = {
    NFSE_AMBIENTE_PRODUCAO: {
        u'servidor': u'bhissdigital.pbh.gov.br/bhiss-ws',
        u'url': u'nfse?wsdl',
    },
    NFSE_AMBIENTE_HOMOLOGACAO: {
        u'servidor': u'bhisshomologa.pbh.gov.br',
        u'url': u'bhiss-ws/nfse?wsdl',
    },
}