# -*- coding: utf-8 -*-

#from OpenSSL import crypto
import socket
import ssl
from datetime import datetime
import time
import os
from uuid import uuid4

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from pysignfe.corr_unicode import *

from .webservices_flags import *
from . import webservices_2
from . import webservices_3

from pysignfe.xml_sped.certificado import Certificado

#
# Manual do Contribuinte versão 4.01
# NF-e leiaute 2.00
#
from .manual_401 import SOAPEnvio_200, SOAPRetorno_200
from .manual_401 import EnviNFe_200, RetEnviNFe_200
from .manual_401 import ConsReciNFe_200, RetConsReciNFe_200, ProtNFe_200, ProcNFe_200
from .manual_401 import CancNFe_200, RetCancNFe_200, ProcCancNFe_200, EnvEvento_200, RetEnvEvento_200, ProcEventoNFe_200
from .manual_401 import InutNFe_200, RetInutNFe_200, ProcInutNFe_200
from .manual_401 import ConsSitNFe_200, RetConsSitNFe_200, ConsCad_200, RetConsCad_200
from .manual_401 import ConsStatServ_200, RetConsStatServ_200
from .manual_401 import  EnvEventoCCe_200, RetEnvEventoCCe_200, ProcEventoNFeCCe_200

#
# Manual do Contribuinte versão 6.00
# NF-e leiaute 3.10
#
from .manual_600 import SOAPEnvio_310, SOAPRetorno_310
from .manual_600 import EnviNFe_310, RetEnviNFe_310
from .manual_600 import ConsReciNFe_310, RetConsReciNFe_310, ProtNFe_310, ProcNFe_310
from .manual_600 import CancNFe_310, RetCancNFe_310, ProcCancNFe_310, EventoCancNFe_310, EnvEventoCancNFe_310, RetEnvEventoCancNFe_310, ProcEventoNFeCancNFe_310
from .manual_600 import InutNFe_310, RetInutNFe_310, ProcInutNFe_310
from .manual_600 import ConsSitNFe_310, RetConsSitNFe_310, ConsCad_310, RetConsCad_310
from .manual_600 import ConsStatServ_310, RetConsStatServ_310
from .manual_600 import EventoCCe_310, EnvEventoCCe_310, RetEnvEventoCCe_310, ProcEventoNFeCCe_310


from .manifestacao_destinatario import EventoConfRecebimento_100, EnvEventoConfRecebimento_100, RetEnvEventoConfRecebimento_100, ProcEventoNFeConfRecebimento_100
from .manifestacao_destinatario import ConsNFeDest_101, RetConsNFeDest_101
from .manifestacao_destinatario import DownloadNFe_100, RetDownloadNFe_100
from .manifestacao_destinatario import TagChNFe

from .manifestacao_destinatario import MD_OPERACAO_NAO_REALIZADA
from .manifestacao_destinatario import MD_DESCEVENTO

#
# DANFE
#
from .danfe.danferetrato import *
from .danfe.danfepaisagem import *
from .danfe.danfce import *

from io import StringIO
import pytz
#import tempfile


class ProcessoNFe(object):
    def __init__(self, webservice=0, envio=u'', resposta=u''):
        self.webservice = webservice
        self.envio = envio
        self.resposta = resposta


class ProcessadorNFe(object):
    def __init__(self):
        self.ambiente = 2
        self.estado = u'MG'
        self.versao = u'2.00'
        self.certificado = Certificado()
        self.caminho = u''
        self.salvar_arquivos = True
        self.contingencia = False
        self.nfce = False
        self.danfe = DANFE()
        self.caminho_temporario = u''
        self.numero_tentativas_consulta_recibo = 2
        self.verificar_status_servico = True
        self.processos = []

        self._servidor     = u''
        self._url          = u''
        self._soap_envio   = None
        self._soap_retorno = None

    def _conectar_servico(self, servico, envio, resposta, ambiente=None):
        print ('  NF-e versao...', self.versao)
        print ('  Conectando ao servico SEFAZ.........')
        if ambiente is None:
            ambiente = self.ambiente

        if self.versao == u'2.00':
            self._soap_envio   = SOAPEnvio_200()
            self._soap_envio.webservice = webservices_2.METODO_WS[servico]['webservice']
            self._soap_envio.metodo     = webservices_2.METODO_WS[servico]['metodo']
            self._soap_envio.cUF        = UF_CODIGO[self.estado]
            self._soap_envio.envio      = envio

            self._soap_retorno = SOAPRetorno_200()
            self._soap_retorno.webservice = webservices_2.METODO_WS[servico]['webservice']
            self._soap_retorno.metodo     = webservices_2.METODO_WS[servico]['metodo']
            self._soap_retorno.resposta   = resposta

            if not self.contingencia:
                self._servidor = webservices_2.ESTADO_WS[self.estado][ambiente][u'servidor']
                self._url      = webservices_2.ESTADO_WS[self.estado][ambiente][servico]
            else:
                self._servidor = webservices_2.ESTADO_WS_CONTINGENCIA[self.estado][ambiente][u'servidor']
                self._url      = webservices_2.ESTADO_WS_CONTINGENCIA[self.estado][ambiente][servico]


        if self.versao == u'3.10':
            self._soap_envio   = SOAPEnvio_310()
            self._soap_envio.webservice = webservices_3.METODO_WS[servico]['webservice']
            self._soap_envio.metodo     = webservices_3.METODO_WS[servico]['metodo']
            self._soap_envio.cUF        = UF_CODIGO[self.estado]
            self._soap_envio.envio      = envio

            self._soap_retorno = SOAPRetorno_310()
            self._soap_retorno.webservice = webservices_3.METODO_WS[servico]['webservice']
            self._soap_retorno.metodo     = webservices_3.METODO_WS[servico]['metodo']
            self._soap_retorno.resposta   = resposta

            if not self.contingencia:
                self._servidor = webservices_3.ESTADO_WS[self.estado][ambiente][u'servidor']
                self._url      = webservices_3.ESTADO_WS[self.estado][ambiente][servico]
            else:
                self._servidor = webservices_3.ESTADO_WS_CONTINGENCIA[self.estado][ambiente][u'servidor']
                self._url      = webservices_3.ESTADO_WS_CONTINGENCIA[self.estado][ambiente][servico]
            
        self.certificado.prepara_certificado_arquivo_pfx()

        #
        # Salva o certificado e a chave privada para uso na conexão HTTPS
        # Salvamos como um arquivo de nome aleatório para evitar o conflito
        # de uso de vários certificados e chaves diferentes na mesma máquina
        # ao mesmo tempo
        #
        self.caminho_temporario = self.caminho_temporario or u'/tmp/'


        nome_arq_chave = self.caminho_temporario + uuid4().hex
        arq_tmp = open(nome_arq_chave, 'w')
        arq_tmp.write(self.certificado.chave)
        arq_tmp.close()

        nome_arq_certificado = self.caminho_temporario + uuid4().hex
        arq_tmp = open(nome_arq_certificado, 'w')
        arq_tmp.write(self.certificado.certificado)
        arq_tmp.close()
        
        print("  servidor: ", self._servidor)
        print("  url: ", self._url)
        from http.client import HTTPSConnection
        con = HTTPSConnection(self._servidor, key_file=nome_arq_chave, cert_file=nome_arq_certificado)
        #con = ConexaoHTTPS(self._servidor, key_file=nome_arq_chave, cert_file=nome_arq_certificado)
        con.request(u'POST', u'/' + self._url, self._soap_envio.xml.encode(u'utf-8'), self._soap_envio.header)
        resp = con.getresponse()

        #
        # Apagamos os arquivos do certificado e o da chave privada, para evitar
        # um potencial risco de segurança; muito embora o uso da chave privada
        # para assinatura exija o uso da senha, pode haver serviços que exijam
        # apenas o uso do certificado para validar a identidade, independente
        # da existência de assinatura digital
        #
        os.remove(nome_arq_chave)
        os.remove(nome_arq_certificado)

        # Dados da resposta salvos para possível debug
        self._soap_retorno.resposta.version  = resp.version
        self._soap_retorno.resposta.status   = resp.status
        #self._soap_retorno.resposta.reason   = unicode(resp.reason.decode('utf-8'))
        self._soap_retorno.resposta.reason   = unicode(resp.reason)
        self._soap_retorno.resposta.msg      = resp.msg
        self._soap_retorno.resposta.original = unicode(resp.read().decode('utf-8'))
        print ('STATUS__-', self._soap_retorno.resposta.original)
        # Tudo certo!
        if self._soap_retorno.resposta.status == 200:
            self._soap_retorno.xml = self._soap_retorno.resposta.original
            print (15*'==')
            print (self._soap_retorno.xml)
            print (15*'==')
        con.close()

    def enviar_lote(self, numero_lote=None, lista_nfes=[]):
        novos_arquivos = []

        if self.versao == u'2.00':
            envio = EnviNFe_200()
            resposta = RetEnviNFe_200()
            webservice = WS_NFE_ENVIO_LOTE
        elif self.versao == u'3.10':
            envio = EnviNFe_310()
            resposta = RetEnviNFe_310()
            webservice = WS_NFE_AUTORIZACAO

        processo = ProcessoNFe(webservice=webservice, envio=envio, resposta=resposta)

        #
        # Vamos assinar e validar todas as NF-e antes da transmissão, evitando
        # rejeição na SEFAZ por incorreção no schema dos arquivos
        #
        for nfe in lista_nfes:
            self.certificado.assina_xmlnfe(nfe)
            nfe.validar()

        envio.NFe = lista_nfes

        envio.idLote.valor = numero_lote
        envio.validar()
                
        if self.salvar_arquivos:
            for n in lista_nfes:
                n.monta_chave()
                novo_arquivo_nome = n.chave + u'-nfe.xml'
                novo_arquivo = n.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            novo_arquivo_nome = unicode(envio.idLote.valor).strip().rjust(15, u'0') + u'-env-lot.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
       
        self._conectar_servico(webservice, envio, resposta)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.idLote.valor).strip().rjust(15, u'0') + u'-rec'

            if resposta.cStat.valor == u'103':
                novo_arquivo_nome += u'.xml'
            else:
                novo_arquivo_nome += u'-rej.xml'

            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                            
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)

        return processo

    def consultar_recibo(self, ambiente=None, numero_recibo=None):
        novos_arquivos = []

        if self.versao == u'2.00':
            envio = ConsReciNFe_200()
            resposta = RetConsReciNFe_200()
            webservice = WS_NFE_CONSULTA_RECIBO
        elif self.versao == u'3.10':
            envio = ConsReciNFe_310()
            resposta = RetConsReciNFe_310()
            webservice = WS_NFE_RET_AUTORIZACAO

        processo = ProcessoNFe(webservice=webservice, envio=envio, resposta=resposta)
        
        if ambiente is None:
            ambiente = self.ambiente

        envio.tpAmb.valor = ambiente
        envio.nRec.valor  = numero_recibo

        envio.validar()
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.nRec.valor).strip().rjust(15, u'0') + u'-ped-rec.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

        self._conectar_servico(webservice, envio, resposta, ambiente)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.nRec.valor).strip().rjust(15, u'0') + u'-pro-rec'

            if resposta.cStat.valor == u'104':
                novo_arquivo_nome += u'.xml'
            else:
                novo_arquivo_nome += u'-rej.xml'

            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            if len(resposta.protNFe):
                self.caminho = self.monta_caminho_nfe(ambiente=ambiente, chave_nfe=resposta.protNFe[0].infProt.chNFe.valor, dir='Recibos')
            else:
                self.caminho = self.monta_caminho_nfe(ambiente=ambiente, dir='Recibos', data=datetime.now().strftime('%Y-%m'))
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
            
            del novos_arquivos[:]

            #
            # Salvar os resultados dos processamentos
            #
            for pn in resposta.protNFe:
                novo_arquivo_nome = unicode(pn.infProt.chNFe.valor).strip().rjust(44, u'0') + u'-pro-nfe-'
                dir = ''
                # NF-e autorizada
                if pn.infProt.cStat.valor == u'100':
                    novo_arquivo_nome += u'aut.xml'
                    dir = 'NFeAutorizada'

                # NF-e denegada
                elif pn.infProt.cStat.valor in (u'110', u'301', u'302', u'303'):
                    novo_arquivo_nome += u'den.xml'
                    dir = 'NFeDenegada'
                    
                # NF-e rejeitada
                else:
                    novo_arquivo_nome += u'rej.xml'
                    dir = 'NFeRejeitada'

                novo_arquivo = pn.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                #novos_arquivos.append(('status_resp', (pn.infProt.cStat.valor,pn.infProt.xMotivo.valor)))
                
                caminho_original = self.caminho
                self.caminho = self.monta_caminho_nfe(ambiente=ambiente, chave_nfe=pn.infProt.chNFe.valor, dir=dir)
                self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
                self.caminho = caminho_original
                
        return processo

    def consultar_notas_destinatario(self, cnpj=None, ambiente=None, indnfe=None, indemi=None, nsu='0'):
        novos_arquivos = []

        envio = ConsNFeDest_101()
        resposta = RetConsNFeDest_101()

        processo = ProcessoNFe(webservice=WS_NFE_CONSULTA_DESTINATARIO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        self.caminho = self.monta_caminho_nfe_cnpj(ambiente=ambiente, cnpj=cnpj, dir='NFeDestinada')
        
        #evento
        envio.tpAmb.valor = ambiente
        envio.CNPJ.valor = cnpj
        envio.indNFe.valor = indnfe
        envio.indEmi.valor = indemi
        envio.ultNSU.valor = nsu

        self.certificado.prepara_certificado_arquivo_pfx()

        envio.validar()
        
        nome_arq = datetime.now().strftime('%Y%m%d%H%M%S')
        
        if self.salvar_arquivos:
            novo_arquivo_nome = nome_arq + u'-env-consnfedest.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
        self._conectar_servico(WS_NFE_CONSULTA_DESTINATARIO, envio, resposta, ambiente)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = nome_arq + u'-consnfedest'
            
            #137 - Nenhum documento localizado para o destinatário
            #138 - Documento localizado para o destinatário
            if resposta.cStat.valor in (u'137', u'138'):
                novo_arquivo_nome += u'.xml'
            else:
                novo_arquivo_nome += u'-rej.xml'
            
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)

        return processo


    def download_nfes(self, cnpj=None,ambiente=None, lista_chaves=[]):
        novos_arquivos = []
        #if self.versao == u'2.00':
        envio = DownloadNFe_100()
        resposta = RetDownloadNFe_100()

        processo = ProcessoNFe(webservice=WS_NFE_DOWNLOAD_XML_DESTINATARIO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        self.caminho = self.monta_caminho_nfe_cnpj(ambiente=ambiente, cnpj=cnpj, dir='NFeDownload')
                
        #evento
        envio.tpAmb.valor = ambiente
        envio.CNPJ.valor = cnpj
        #envio.chNFe.valor = chave_nfe
        envio.chNFe = [TagChNFe(valor=ch) for ch in lista_chaves]        
        envio.xServ.valor = u'DOWNLOAD NFE'

        self.certificado.prepara_certificado_arquivo_pfx()

        envio.validar()
        
        nome_arq = datetime.now().strftime('%Y%m%d%H%M%S')
        
        #Nome do arquivo será a data e hora atual
        if self.salvar_arquivos:
            novo_arquivo_nome = nome_arq + u'-env-downloadnfe.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
        self._conectar_servico(WS_NFE_DOWNLOAD_XML_DESTINATARIO, envio, resposta, ambiente)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = nome_arq + u'-downloadnfe'
            
            #139 - Pedido de Download processado
            if resposta.cStat.valor == u'139':
                novo_arquivo_nome += u'.xml'
            else:
                novo_arquivo_nome += u'-rej.xml'
            
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)

        return processo

    def consultar_cadastro_contribuinte(self, cpf_cnpj=None, inscricao_estadual=None, ambiente=None):
        novos_arquivos = []
        if self.versao == u'2.00':
            envio = ConsCad_200()
            resposta = RetConsCad_200()
        elif self.versao == u'3.10':
            envio = ConsCad_310()
            resposta = RetConsCad_310()

        processo = ProcessoNFe(webservice=WS_NFE_CONSULTA_CADASTRO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente
            
        envio.infCons.UF.valor = self.estado

        if inscricao_estadual:
            envio.infCons.IE.valor = inscricao_estadual
            nome = 'IE_' + inscricao_estadual
        elif len(cpf_cnpj) == 11:
            envio.infCons.CPF.valor = cpf_cnpj
            nome = 'CPF_' + cpf_cnpj
        elif len(cpf_cnpj) == 14:
            envio.infCons.CNPJ.valor = cpf_cnpj
            nome = 'CNPJ_' + cpf_cnpj
        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = nome + u'-cons-cad.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

        self._conectar_servico(WS_NFE_CONSULTA_CADASTRO, envio, resposta, 1)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = nome + u'-cad.xml'
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            self.caminho = self.caminho + u'ArquivosXML/NFe/ConsultaCadastro/'
            
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
            
        return processo
        
    def enviar_lote_evento(self, tipo_evento, lista_eventos=[], numero_lote=None):
    
        novos_arquivos = []
        #
        # Determina o tipo do evento
        #
        dir = ''
        if tipo_evento == 'cce':
            classe_evento = ProcEventoNFeCCe_310
            envio = EnvEventoCCe_310()
            resposta = RetEnvEventoCCe_310()
            dir = 'Eventos/Correcao'
        elif tipo_evento == 'can':
            classe_evento = ProcEventoNFeCancNFe_310
            envio = EnvEventoCancNFe_310()
            resposta = RetEnvEventoCancNFe_310()
            dir = 'Eventos/Cancelamento'
        elif tipo_evento == 'confrec':
            classe_evento = ProcEventoNFeConfRecebimento_100
            envio = EnvEventoConfRecebimento_100()
            resposta = RetEnvEventoConfRecebimento_100()
            dir = 'Eventos/Manifestacao'
        
        processo = ProcessoNFe(webservice=WS_NFE_EVENTO, envio=envio, resposta=resposta)
        
        self.certificado.prepara_certificado_arquivo_pfx()
        #Assinar cada evento
        for evento in lista_eventos:
            self.certificado.assina_xmlnfe(evento)
        
        envio.evento = lista_eventos
        
        if numero_lote is None:
            numero_lote = datetime.now().strftime('%Y%m%d%H%M%S')

        envio.idLote.valor = numero_lote
                
        envio.validar()
        
        ambiente = lista_eventos[0].infEvento.tpAmb.valor or self.ambiente
        self.caminho = self.monta_caminho_nfe(ambiente=ambiente, chave_nfe=lista_eventos[0].infEvento.chNFe.valor, dir=dir)
        
        ##Salvar arquivo unico
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.idLote.valor).strip().rjust(15, '0') + u'-env-' + tipo_evento +'.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        
        self._conectar_servico(WS_NFE_EVENTO, envio, resposta)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.idLote.valor).strip().rjust(15, '0') + '-rec-' + tipo_evento

            if resposta.cStat.valor != '128':
                novo_arquivo_nome += u'-rej.xml'
            else:
                novo_arquivo_nome += u'.xml'

            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            self.montar_processo_lista_eventos(lista_eventos, processo.resposta.dic_retEvento, processo.resposta.dic_procEvento, classe_evento)
            
            self.salvar_processamento_eventos(processo=processo, ret_eventos=resposta.retEvento, tipo_evento=tipo_evento)
            
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            
        return processo
    
    def montar_processo_lista_eventos(self, lista_eventos, dic_retEvento, dic_procEvento, classe_procEvento):
        for evento in lista_eventos:
            chave = evento.infEvento.chNFe.valor
            if chave in dic_retEvento:
                retorno = dic_retEvento[chave]
                processo = classe_procEvento()
                processo.evento = evento
                processo.retEvento = retorno
                dic_procEvento[chave] = processo
        

    def cancelar_nota(self, ambiente=None, chave_nfe=None, numero_protocolo=None,
                      justificativa=None, data=None, numero_lote=None):
            
        evento = EventoCancNFe_310()
        evento.infEvento.tpAmb.valor = ambiente or self.ambiente
        evento.infEvento.cOrgao.valor = UF_CODIGO[self.estado]
        evento.infEvento.CNPJ.valor = chave_nfe[6:20] # Extrai o CNPJ da própria chave da NF-e
        evento.infEvento.chNFe.valor = chave_nfe
        evento.infEvento.dhEvento.valor = data or datetime.now()
        evento.infEvento.detEvento.nProt.valor = numero_protocolo
        evento.infEvento.detEvento.xJust.valor = justificativa
        
        processo = self.enviar_lote_evento(tipo_evento='can', lista_eventos=[evento], numero_lote=numero_lote)
        return processo
        
    def corrigir_nota(self, chave_nfe=None, texto_correcao=None, ambiente=None,
                      sequencia=None, data=None, numero_lote=None):
                      
        evento = EventoCCe_310()
        evento.infEvento.tpAmb.valor = ambiente or self.ambiente
        evento.infEvento.cOrgao.valor = UF_CODIGO[self.estado]
        evento.infEvento.CNPJ.valor = chave_nfe[6:20] # Extrai o CNPJ da própria chave da NF-e
        evento.infEvento.chNFe.valor = chave_nfe
        evento.infEvento.dhEvento.valor = data or datetime.now()
        evento.infEvento.detEvento.xCorrecao.valor = texto_correcao
        evento.infEvento.nSeqEvento.valor = sequencia or 1

        processo = self.enviar_lote_evento(tipo_evento='cce', lista_eventos=[evento], numero_lote=numero_lote)
        return processo
        
    def efetuar_manifesto_destinatario(self, tipo_manifesto, cnpj=None, chave_nfe=None, ambiente=None, data=None, numero_lote=None, ambiente_nacional=True, justificativa=None):
        
        evento = EventoConfRecebimento_100()
        evento.infEvento.tpAmb.valor = ambiente or self.ambiente
        if ambiente_nacional:
            evento.infEvento.cOrgao.valor = UF_CODIGO['NACIONAL']
        else:
            evento.infEvento.cOrgao.valor = UF_CODIGO[self.estado]
            
        evento.infEvento.CNPJ.valor = cnpj
        evento.infEvento.chNFe.valor = chave_nfe
        evento.infEvento.dhEvento.valor = data or datetime.now()
        evento.infEvento.tpEvento.valor = tipo_manifesto
        evento.infEvento.detEvento.descEvento.valor = MD_DESCEVENTO[tipo_manifesto]
        
        if justificativa and tipo_manifesto==MD_OPERACAO_NAO_REALIZADA:
            evento.infEvento.detEvento.xJust.valor = justificativa

        processo = self.enviar_lote_evento(tipo_evento='confrec', lista_eventos=[evento], numero_lote=numero_lote)
        return processo
        
    def inutilizar_nota(self, ambiente=None, codigo_estado=None, ano=None, cnpj=None, serie=None,
                        numero_inicial=None, numero_final=None, justificativa=None, nfce=False):
        novos_arquivos = []

        if self.versao == u'2.00':
            envio = InutNFe_200()
            resposta = RetInutNFe_200()
        elif self.versao == u'3.10':
            envio = InutNFe_310()
            resposta = RetInutNFe_310()

        processo = ProcessoNFe(webservice=WS_NFE_INUTILIZACAO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        if codigo_estado is None:
            codigo_estado = UF_CODIGO[self.estado]

        if ano is None:
            ano = datetime.now().strftime(u'%y')

        if not numero_final:
            numero_final = numero_inicial

        self.caminho = self.monta_caminho_inutilizacao(ambiente=ambiente, serie=serie,
                                    numero_inicial=numero_inicial, numero_final=numero_final)

        envio.infInut.tpAmb.valor  = ambiente
        envio.infInut.cUF.valor    = codigo_estado
        envio.infInut.ano.valor    = ano
        envio.infInut.CNPJ.valor   = cnpj
        if self.nfce:
            envio.infInut.mod.valor    = 65
        else:
            envio.infInut.mod.valor    = 55
        envio.infInut.serie.valor  = serie
        envio.infInut.nNFIni.valor = numero_inicial
        envio.infInut.nNFFin.valor = numero_final
        envio.infInut.xJust.valor  = justificativa

        envio.gera_nova_chave()
        self.certificado.prepara_certificado_arquivo_pfx()
        self.certificado.assina_xmlnfe(envio)

        envio.validar()
                
        if self.salvar_arquivos:
            nome_arq = envio.chave[0:2] + ano + cnpj + unicode(envio.infInut.mod.valor) + serie + numero_inicial + numero_final
            novo_arquivo_nome = nome_arq + u'-ped-inu.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
    
        self._conectar_servico(WS_NFE_INUTILIZACAO, envio, resposta, ambiente)

        # Se for autorizada, monta o processo de inutilização
        if resposta.infInut.cStat.valor == u'102':
            if self.versao == u'2.00':
                processo_inutilizacao_nfe = ProcInutNFe_200()

            elif self.versao == u'3.10':
                processo_inutilizacao_nfe = ProcInutNFe_310()

            processo_inutilizacao_nfe.inutNFe = envio
            processo_inutilizacao_nfe.retInutNFe = resposta

            processo_inutilizacao_nfe.validar()

            processo.processo_inutilizacao_nfe = processo_inutilizacao_nfe
            

        if self.salvar_arquivos:
            nome_arq = ano + cnpj + unicode(envio.infInut.mod.valor) + serie + numero_inicial + numero_final
            novo_arquivo_nome = nome_arq + u'-pro-inu-'

            # Inutilização autorizada
            if resposta.infInut.cStat.valor == u'102':
                novo_arquivo_nome += u'aut.xml'
            else:
                novo_arquivo_nome += u'rej.xml'

            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            # Se for autorizada, monta o processo de inutilização
            if resposta.infInut.cStat.valor == u'102':
                #novo_arquivo_nome = nome_arq + u'-proc-inu-nfe.xml'
                #novo_arquivo = processo_inutilizacao_nfe.xml.encode('utf-8')
                #novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

                novo_arquivo_nome = nome_arq + u'-inu.xml'
                novo_arquivo = processo_inutilizacao_nfe.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
    
        return processo

    def consultar_nota(self, ambiente=None, chave_nfe=None, nfe=None):
        novos_arquivos = []

        if self.versao == u'2.00':
            envio = ConsSitNFe_200()
            resposta = RetConsSitNFe_200()
        elif self.versao == u'3.10':
            envio = ConsSitNFe_310()
            resposta = RetConsSitNFe_310()

        processo = ProcessoNFe(webservice=WS_NFE_CONSULTA, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        envio.tpAmb.valor = ambiente
        envio.chNFe.valor = chave_nfe
        
        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(chave_nfe).strip().rjust(44, u'0') + u'-ped-sit.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        

        self._conectar_servico(WS_NFE_CONSULTA, envio, resposta, ambiente)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(chave_nfe).strip().rjust(44, u'0') + u'-sit.xml'
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            self.caminho = self.monta_caminho_nfe(ambiente, chave_nfe, 'NFeSituacao')
                
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
        
        return processo

    def consultar_servico(self, ambiente=None, codigo_estado=None):

        novos_arquivos = []

        if self.versao == u'2.00':
            envio = ConsStatServ_200()
            resposta = RetConsStatServ_200()
        elif self.versao == u'3.10':
            envio = ConsStatServ_310()
            resposta = RetConsStatServ_310()

        processo = ProcessoNFe(webservice=WS_NFE_SITUACAO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        if codigo_estado is None:
            codigo_estado = UF_CODIGO[self.estado]

        envio.tpAmb.valor = ambiente
        envio.cUF.valor   = codigo_estado
        envio.data        = datetime.now()

        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = envio.data.strftime(u'%Y-%m-%dT%H%M%S') + u'-ped-sta.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

        self._conectar_servico(WS_NFE_SITUACAO, envio, resposta, ambiente)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = envio.data.strftime(u'%Y-%m-%dT%H%M%S') + u'-sta.xml'
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        
            caminho_original = self.caminho
            self.caminho = self.caminho + u'ArquivosXML/NFe/ConsultaStatusServidorNFe/'
            
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
            
        return processo
        
    def gerar_xml(self, lista_nfes, numero_lote=None):
        novos_arquivos = []
        
        nfe = lista_nfes[0]
        nfe.monta_chave()
        ambiente = nfe.infNFe.ide.tpAmb.valor
        
        caminho_original = self.caminho
        self.caminho = self.monta_caminho_nfe(ambiente=nfe.infNFe.ide.tpAmb.valor, chave_nfe=nfe.chave, dir='Lotes')
        
        if self.versao == u'2.00':
            envio = EnviNFe_200()
        elif self.versao == u'3.10':
            envio = EnviNFe_310()
            
        processo = ProcessoNFe(envio=envio)
        
        self.certificado.prepara_certificado_arquivo_pfx()
        
        for nfe in lista_nfes:
            self.certificado.assina_xmlnfe(nfe)
            nfe.validar()

        envio.NFe = lista_nfes
        envio.idLote.valor = numero_lote
        envio.validar()
        
        if self.salvar_arquivos:
            for n in lista_nfes:
                n.monta_chave()
                novo_arquivo_nome = n.chave + u'-nfe.xml'
                novo_arquivo = n.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            ##Nao salva o lote, apenas NF-es
            #novo_arquivo_nome = unicode(envio.idLote.valor).strip().rjust(15, u'0') + u'-env-lot.xml'
            #novo_arquivo = envio.xml.encode('utf-8')
            #novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
        
        return processo
        
    def processar_notas(self, lista_nfes, numero_lote=None):
        #
        # Definir o caminho geral baseado na 1ª NF-e
        #
        self.processos = processos = OrderedDict()
        novos_arquivos = []

        caminho_original = self.caminho
        nfe = lista_nfes[0]
        nfe.monta_chave()
        #self.caminho = caminho_original
        ambiente = nfe.infNFe.ide.tpAmb.valor
        #self.caminho = self.monta_caminho_nfe(ambiente=nfe.infNFe.ide.tpAmb.valor, chave_nfe=nfe.chave)
        status_serv = u'107'
        if self.verificar_status_servico:
            proc_servico = self.consultar_servico(ambiente=ambiente)
            yield proc_servico
            status_serv = proc_servico.resposta.cStat.valor
        
        #Servico em operacao (status == 107)
        if status_serv == u'107':
            #
            # Verificar se as notas já não foram emitadas antes
            #
            for nfe in lista_nfes:
                nfe.monta_chave()
                self.caminho = caminho_original
                proc_consulta = self.consultar_nota(ambiente=nfe.infNFe.ide.tpAmb.valor, chave_nfe=nfe.chave)
                yield proc_consulta

                #
                # Se a nota já constar na SEFAZ
                #
                if (
                    ((self.versao == '1.10') and (proc_consulta.resposta.infProt.cStat.valor in ('217', '999',)))
                    or
                    ((self.versao in ['2.00', '3.10']) and (proc_consulta.resposta.cStat.valor in ('100', '150', '110', '301', '302')))
                ):
                    #
                    # Interrompe todo o processo
                    #
                    return

            #
            # Nenhuma das notas estava já enviada, enviá-las então
            #
            nfe = lista_nfes[0]
            nfe.monta_chave()
            self.caminho = caminho_original
            #self.caminho = self.monta_caminho_nfe(ambiente=nfe.infNFe.ide.tpAmb.valor, chave_nfe=nfe.chave)
            self.caminho = self.monta_caminho_nfe(ambiente=nfe.infNFe.ide.tpAmb.valor, chave_nfe=nfe.chave, dir='Lotes')
            proc_envio = self.enviar_lote(lista_nfes=lista_nfes, numero_lote=numero_lote)
            yield proc_envio
            self.caminho = caminho_original
            
            ret_envi_nfe = proc_envio.resposta

            #
            # Deu certo?
            #
            if ret_envi_nfe.cStat.valor == u'103':
                print(" Lote enviado com sucesso. Consultando recibo...")
                t_espera = ret_envi_nfe.infRec.tMed.valor
                #Alguns webservices exageram no tempo de espera.
                if t_espera > 10:
                    t_espera = 6
                time.sleep(t_espera * 2) # Espere o processamento antes de consultar o recibo
                proc_recibo = self.consultar_recibo(ambiente=ret_envi_nfe.tpAmb.valor, numero_recibo=ret_envi_nfe.infRec.nRec.valor)
                
                tentativa = 0
                while  proc_recibo.resposta.cStat.valor == u'105' and tentativa < self.numero_tentativas_consulta_recibo:
                    time.sleep(t_espera * 2) # Espere o processamento antes de consultar o recibo
                    proc_recibo = self.consultar_recibo(ambiente=ret_envi_nfe.tpAmb.valor, numero_recibo=ret_envi_nfe.infRec.nRec.valor)
                    tentativa += 1
                yield proc_recibo
                
                # Montar os processos das NF-es
                dic_protNFe = proc_recibo.resposta.dic_protNFe
                dic_procNFe = proc_recibo.resposta.dic_procNFe
                
                self.caminho = caminho_original
                novos_processos = self.montar_processo_lista_notas(lista_nfes, dic_protNFe, dic_procNFe)
                for i,novo_processo in enumerate(novos_processos):
                    processos['nota_%i' % i] = novo_processo
                
                return

    def montar_processo_lista_notas(self, lista_nfes, dic_protNFe, dic_procNFe):
        processos = []
        for nfe in lista_nfes:
            #if dic_protNFe.has_key(nfe.chave):
            if nfe.chave in dic_protNFe:
                protocolo = dic_protNFe[nfe.chave]
                processo = self.montar_processo_uma_nota(nfe, protnfe_recibo=protocolo)
                processos.append(processo)
                
                if processo is not None:
                    dic_procNFe[nfe.chave] = processo
        return processos
        
    def montar_processo_uma_nota(self, nfe, protnfe_recibo=None, protnfe_consulta_110=None, retcancnfe=None):
        novos_arquivos = []
       
        processo = None
        dir = ''
        
        if self.versao == u'2.00':
            processo = ProcNFe_200()
        elif self.versao == u'3.10':
            processo = ProcNFe_310()
        
        processo.NFe     = nfe
        processo.protNFe = protnfe_recibo
            
        # 100 - autorizada
        # 150 - autorizada fora do prazo
        # 110 - denegada
        # 301 - denegada por irregularidade do emitente
        # 302 - denegada por irregularidade do destinatário
        # 303 - Uso Denegado: Destinatário não habilitado a operar na UF
        if self.salvar_arquivos:
            if protnfe_recibo.infProt.cStat.valor in (u'100', u'150'):
                novo_arquivo_nome = unicode(nfe.chave).strip().rjust(44, u'0') + u'-proc-nfe.xml'
                dir = 'NFeAutorizada'
            elif protnfe_recibo.infProt.cStat.valor in (u'110', u'301', u'302', u'303'):
                novo_arquivo_nome = unicode(nfe.chave).strip().rjust(44, u'0') + u'-proc-nfe-den.xml'
                dir = 'NFeDenegada'
            else:
                novo_arquivo_nome = unicode(nfe.chave).strip().rjust(44, u'0') + u'-proc-nfe-rej.xml'
                dir = 'NFeRejeitada'
        
            caminho_original = self.caminho
            self.caminho = self.monta_caminho_nfe(ambiente=nfe.infNFe.ide.tpAmb.valor, chave_nfe=nfe.chave, dir=dir)
            novo_arquivo_nome = novo_arquivo_nome
            novo_arquivo = processo.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            
            self.caminho = caminho_original
            
        return processo

    def monta_caminho_nfe(self, ambiente, chave_nfe=None, dir='', data=None):
        caminho = self.caminho + u'ArquivosXML/NFe/'

        if ambiente == 1:
            caminho = os.path.join(caminho, 'producao/')
        else:
            caminho = os.path.join(caminho, 'homologacao/')
        
        if not data:
            data = u'20' + chave_nfe[2:4] + u'-' + chave_nfe[4:6]
            
        if dir:
            caminho = os.path.join(caminho, data + u'/' + dir + u'/')
        else:
            serie = chave_nfe[22:25]
            numero = chave_nfe[25:34]

            caminho = os.path.join(caminho, data + u'/')
            caminho = os.path.join(caminho, serie + u'-' + numero + u'/')
        
        return caminho
        
    def monta_caminho_inutilizacao(self, ambiente=None, data=None, serie=None, numero_inicial=None, numero_final=None):
        caminho = self.caminho + u'ArquivosXML/NFe/'

        if ambiente == 1:
            caminho = os.path.join(caminho, 'producao/')
        else:
            caminho = os.path.join(caminho, 'homologacao/')

        if data is None:
            data = datetime.now()

        caminho = os.path.join(caminho, data.strftime(u'%Y-%m') + u'/' + 'NFeInutilizada/')

        serie          = unicode(serie).strip().rjust(3, u'0')
        numero_inicial = unicode(numero_inicial).strip().rjust(9, u'0')
        numero_final   = unicode(numero_final).strip().rjust(9, u'0')

        caminho = os.path.join(caminho, serie + u'-' + numero_inicial + u'-' + numero_final + u'/')
        
        return caminho
        
    def monta_caminho_nfe_cnpj(self, ambiente=None, data=None, cnpj=None, dir=''):
        caminho = self.caminho + u'ArquivosXML/NFe/'

        if ambiente == 1:
            caminho = os.path.join(caminho, 'producao/')
        else:
            caminho = os.path.join(caminho, 'homologacao/')
            
        if data is None:
            data = datetime.now()
            
        caminho = os.path.join(caminho, data.strftime(u'%Y-%m') + u'/')
        if dir:
            caminho = os.path.join(caminho, dir + u'/' + cnpj + u'/')
        else:
            caminho = os.path.join(caminho, cnpj + u'/')
            
        return caminho
                
    def salvar_novos_arquivos(self, novos_arquivos):
        caminho = self.caminho
        
        try:
            os.makedirs(caminho)
        except:
            pass
    
        for arquivo in novos_arquivos:
            nome_arquivo, conteudo = arquivo
            arquivo_em_disco = open(os.path.join(caminho, nome_arquivo), 'wb')
            if hasattr(conteudo, 'getvalue'):
                arquivo_em_disco.write(conteudo.getvalue())
            else:
                arquivo_em_disco.write(conteudo)
            arquivo_em_disco.close()
    
    def salvar_processamento_eventos(self, processo, ret_eventos, tipo_evento):

        for ret in ret_eventos:
            novos_arquivos = []
            chave = ret.infEvento.chNFe.valor
            nome_arq = ret.infEvento.chNFe.valor + '-' + unicode(ret.infEvento.nSeqEvento.valor).zfill(2)
            
            #
            # O evento foi aceito e vinculado à NF-e
            #
            if ret.infEvento.cStat.valor == '135':
                novo_arquivo_nome = nome_arq + '-ret-' + tipo_evento + '.xml'
                novo_arquivo = ret.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                
                #
                # Salva o processo do evento
                #
                novo_arquivo_nome = nome_arq + '-proc-' + tipo_evento + '.xml'
                novo_arquivo = processo.resposta.dic_procEvento[chave].xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            #
            # O evento foi aceito, mas não foi vinculado à NF-e
            #
            elif ret.infEvento.cStat.valor == '136':
                novo_arquivo_nome = nome_arq + '-ret-' + tipo_evento + '-sv.xml'
                novo_arquivo = ret.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

                #
                # Salva o processo do evento
                #
                novo_arquivo_nome = nome_arq + '-proc-' + tipo_evento + '.xml'
                novo_arquivo = processo.resposta.dic_procEvento[chave].xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            #
            # O evento foi aceito e vinculado à NF-e, é um cancelamento for do prazo
            #
            elif ret.infEvento.cStat.valor == '155':
                novo_arquivo_nome = nome_arq + '-ret-' + tipo_evento + '.xml'
                novo_arquivo = ret.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

                #
                # Salva o processo do evento
                #
                novo_arquivo_nome = nome_arq + '-proc-' + tipo_evento + '.xml'
                novo_arquivo = processo.resposta.dic_procEvento[chave].xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            #
            # O evento foi rejeitado
            #
            else:
                novo_arquivo_nome = nome_arq + '-ret-' + tipo_evento + '-rej.xml'
                novo_arquivo = ret.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)


class DANFE(object):
    def __init__(self):
        self.imprime_canhoto        = True
        self.imprime_local_retirada = True
        self.imprime_local_entrega  = True
        self.imprime_fatura         = True
        self.imprime_duplicatas     = True
        self.imprime_issqn          = True
        
        #NFC-e
        self.imprime_produtos_nfce = True
        self.imprime_id_consumidor = True
        self.imprime_ender_consumidor = True

        self.caminho           = u''
        self.salvar_arquivo    = False

        self.NFe        = None
        self.protNFe    = None
        self.retCancNFe = None
        self.danfe      = None
        self.versao     = '2.00'

        self.obs_impressao    = u'DANFE gerado em %(now:%d/%m/%Y, %H:%M:%S)s'
        self.nome_sistema     = u''
        self.site             = u''
        self.logo             = u''
        self.leiaute_logo_vertical = False
        self.dados_emitente   = []

    def gerar_danfe(self):
        if self.NFe is None:
            raise ValueError(u'Não é possível gerar um DANFE sem a informação de uma NF-e')

        if self.protNFe is None:
            if self.versao == u'2.00':
                self.protNFe = ProtNFe_200()
            elif self.versao == u'3.10':
                self.protNFe = ProtNFe_310()

        if self.retCancNFe is None:
            if self.versao == u'2.00':
                self.retCancNFe = RetCancNFe_200()
            elif self.versao == u'3.10':
                self.retCancNFe = RetCancNFe_310()

        #
        # Prepara o queryset para impressão
        #
        self.NFe.monta_chave()
        self.NFe.monta_dados_contingencia_fsda()
        self.NFe.site = self.site

        for detalhe in self.NFe.infNFe.det:
            detalhe.NFe = self.NFe
            detalhe.protNFe = self.protNFe
            detalhe.retCancNFe = self.retCancNFe
        
        #
        # Prepara as bandas de impressão para cada formato
        #
        if self.NFe.infNFe.ide.tpImp.valor == 2:
            #raise ValueError(u'DANFE em formato paisagem ainda não implementado')
            self.danfe = DANFEPaisagem()
            self.danfe.queryset = self.NFe.infNFe.det
        else:
            self.danfe = DANFERetrato()
            self.danfe.queryset = self.NFe.infNFe.det
        
        if self.imprime_canhoto:
            self.danfe.band_page_header = self.danfe.canhoto
            self.danfe.band_page_header.child_bands = []
            self.danfe.band_page_header.child_bands.append(self.danfe.remetente)
        else:
            self.danfe.band_page_header = self.danfe.remetente
            self.danfe.band_page_header.child_bands = []

        # Emissão para simples conferência / sem protocolo de autorização
#        self.protNFe
 
        if not self.protNFe.infProt.nProt.valor:
            self.danfe.remetente.campo_variavel_conferencia()

        # NF-e denegada
        elif self.protNFe.infProt.cStat.valor == u'110':
            self.danfe.remetente.campo_variavel_denegacao()
            self.danfe.remetente.obs_denegacao()

        # Emissão em contingência com FS ou FSDA
        elif self.NFe.infNFe.ide.tpEmis.valor in (2, 5,):
            self.danfe.remetente.campo_variavel_contingencia_fsda()
            self.danfe.remetente.obs_contingencia_normal_scan()

        # Emissão em contingência com DPEC
        elif self.NFe.infNFe.ide.tpEmis.valor == 4:
            self.danfe.remetente.campo_variavel_contingencia_dpec()
            self.danfe.remetente.obs_contingencia_dpec()

        # Emissão normal ou contingência SCAN, SVC-AN e SVC-RS
        else:
            self.danfe.remetente.campo_variavel_normal()
            # Contingência SCAN,SVC-AN e SVC-RS
            if self.NFe.infNFe.ide.tpEmis.valor in (3, 6, 7):
                self.danfe.remetente.obs_contingencia_normal_scan()

        # A NF-e foi cancelada, no DANFE imprimir o "carimbo" de cancelamento
        if self.retCancNFe.infCanc.nProt.valor:
            self.danfe.remetente.obs_cancelamento()

        # Observação de ausência de valor fiscal
        # se não houver protocolo ou se o ambiente for de homologação
        if (not self.protNFe.infProt.nProt.valor) or self.NFe.infNFe.ide.tpAmb.valor == 2:
            self.danfe.remetente.obs_sem_valor_fiscal()

        self.danfe.band_page_header.child_bands.append(self.danfe.destinatario)

        if self.imprime_local_retirada and len(self.NFe.infNFe.retirada.xml):
            self.danfe.band_page_header.child_bands.append(self.danfe.local_retirada)

        if self.imprime_local_entrega and len(self.NFe.infNFe.entrega.xml):
            self.danfe.band_page_header.child_bands.append(self.danfe.local_entrega)

        if self.imprime_fatura:
            # Pagamento a prazo
            if (self.NFe.infNFe.ide.indPag.valor == 1) or \
                (len(self.NFe.infNFe.cobr.dup) > 1) or \
                ((len(self.NFe.infNFe.cobr.dup) == 1) and \
                (self.NFe.infNFe.cobr.dup[0].dVenc.xml > self.NFe.infNFe.ide.dhEmi.xml)):

                if self.imprime_duplicatas:
                    self.danfe.fatura_a_prazo.elements.append(self.danfe.duplicatas)

                self.danfe.band_page_header.child_bands.append(self.danfe.fatura_a_prazo)

            # Pagamento a vista
            else:
                self.danfe.band_page_header.child_bands.append(self.danfe.fatura_a_vista)

        self.danfe.band_page_header.child_bands.append(self.danfe.calculo_imposto)
        self.danfe.band_page_header.child_bands.append(self.danfe.transporte)
        self.danfe.band_page_header.child_bands.append(self.danfe.cab_produto)

#        self.danfe.band_page_footer = self.danfe.iss

        if self.imprime_issqn and len(self.NFe.infNFe.total.ISSQNTot.xml):
            self.danfe.band_page_footer = self.danfe.iss
        else:
            self.danfe.band_page_footer = self.danfe.dados_adicionais

        self.danfe.band_detail = self.danfe.det_produto

        #
        # Observação de impressão
        #
        if self.nome_sistema:
            self.danfe.ObsImpressao.expression = self.nome_sistema + u' - ' + self.obs_impressao
        else:
            self.danfe.ObsImpressao.expression = self.obs_impressao

        #
        # Quadro do emitente
        #
        # Personalizado?
        if self.dados_emitente:
            self.danfe.remetente.monta_quadro_emitente(self.dados_emitente)
        else:
            # Sem logotipo
            if not self.logo:
                self.danfe.remetente.monta_quadro_emitente(self.danfe.remetente.dados_emitente_sem_logo())

            # Logotipo na vertical
            elif self.leiaute_logo_vertical:
                self.danfe.remetente.monta_quadro_emitente(self.danfe.remetente.dados_emitente_logo_vertical(self.logo))

            # Logotipo na horizontal
            else:
                self.danfe.remetente.monta_quadro_emitente(self.danfe.remetente.dados_emitente_logo_horizontal(self.logo))

        if self.salvar_arquivo:
            self.caminho = self.monta_caminho_danfe(ambiente=self.NFe.infNFe.ide.tpAmb.valor, chave_nfe=self.NFe.chave, dir='DANFE')
            nome_arq = self.caminho + self.NFe.chave + u'.pdf'
            type(self.danfe.generate_by(PDFGenerator, filename=nome_arq))
            
    def gerar_danfce(self, via_estabelecimento=False):
        if self.NFe is None:
            raise ValueError(u'Não é possível gerar um DANFE sem a informação de uma NF-e')
            
        if self.protNFe is None:
            if self.versao == u'2.00':
                self.protNFe = ProtNFe_200()
            elif self.versao == u'3.10':
                self.protNFe = ProtNFe_310()

        if self.retCancNFe is None:
            if self.versao == u'2.00':
                self.retCancNFe = RetCancNFe_200()
            elif self.versao == u'3.10':
                self.retCancNFe = RetCancNFe_310()

        #
        # Prepara o queryset para impressão
        #
        self.NFe.monta_chave()
        #self.NFe.gera_qrcode_nfce(csc=self.NFe.infNFeSupl.csc, cidtoken=self.NFe.infNFeSupl.cidtoken, nversao=self.NFe.infNFeSupl.cidtoken)
        self.NFe.gera_qrcode_nfce()
        self.NFe.monta_dados_contingencia_fsda()
        self.NFe.site = self.site
        self.NFe.via_estabelecimento = via_estabelecimento

        for detalhe in self.NFe.infNFe.det:
            detalhe.NFe = self.NFe
            detalhe.protNFe = self.protNFe
            detalhe.retCancNFe = self.retCancNFe
        
        self.danfe = DANFCE()
        self.danfe.queryset = self.NFe.infNFe.det
                
        self.danfe.band_page_header = self.danfe.cabecalho
        
        if self.NFe.infNFe.ide.tpEmis.valor != 1:
            self.danfe.mensagem_fiscal_topo.campo_variavel_contingencia()
        elif self.NFe.infNFe.ide.tpAmb.valor == 2:
            self.danfe.mensagem_fiscal_topo.campo_variavel_homologacao()
            
        self.danfe.band_page_header.child_bands.append(self.danfe.mensagem_fiscal_topo)
        
        if self.imprime_produtos_nfce:
            lines_xprod = 0
            for d in self.NFe.infNFe.det:
                lines_xprod += len(d.prod.xProd.valor)
            self.danfe.inf_produtos.band_detail.set_band_height(lines_xprod)
            self.danfe.det_produtos.elements.append(self.danfe.inf_produtos)
            self.danfe.band_page_header.child_bands.append(self.danfe.det_produtos)
        
        ##Adicionar acrescimos se houver
        if (str(self.NFe.infNFe.total.ICMSTot.vFrete.valor) != '0.0') or \
            (str(self.NFe.infNFe.total.ICMSTot.vSeg.valor) != '0.0') or \
            (str(self.NFe.infNFe.total.ICMSTot.vOutro.valor) != '0.0'):
            
                self.danfe.descontos.band_header.set_top()
                for band in self.danfe.acrescimos.band_header.elements:
                    self.danfe.inf_totais.band_header.elements.append(band)
                
                #Adicionar a altura do band_header
                self.danfe.inf_totais.band_header.add_height()
        
        ##Adicionar descontos se houver
        if (str(self.NFe.infNFe.total.ICMSTot.vDesc.valor) != '0.0'):
            for band in self.danfe.descontos.band_header.elements:
                self.danfe.inf_totais.band_header.elements.append(band)
                
            #Adicionar a altura do band_header
            self.danfe.inf_totais.band_header.add_height()
        
        self.danfe.det_totais.elements.append(self.danfe.inf_totais)
        self.danfe.band_page_header.child_bands.append(self.danfe.det_totais)
        
        self.danfe.det_pagamento.elements.append(self.danfe.inf_pagamento)
        self.danfe.band_page_header.child_bands.append(self.danfe.det_pagamento)
        
        self.danfe.band_page_header.child_bands.append(self.danfe.consulta_chave)
        
        if self.imprime_id_consumidor:
            self.danfe.id_consumidor.consumidor_identificado()
            self.danfe.band_page_header.child_bands.append(self.danfe.id_consumidor)
            
            if self.imprime_ender_consumidor:
                self.danfe.band_page_header.child_bands.append(self.danfe.ender_consumidor)
        else:
            self.danfe.id_consumidor.consumidor_nao_identificado()
            self.danfe.band_page_header.child_bands.append(self.danfe.id_consumidor)
                    
        ##Emissão normal, imprimir numero protocolo
        if self.NFe.infNFe.ide.tpEmis.valor == 1:
            self.danfe.id_nfce.campo_variavel_protocolo()
        
        self.danfe.band_page_header.child_bands.append(self.danfe.id_nfce)
        
        if self.NFe.infNFe.ide.tpEmis.valor != 1:
            self.danfe.mensagem_fiscal_base.campo_variavel_contingencia()
        elif self.NFe.infNFe.ide.tpAmb.valor == 2:
            self.danfe.mensagem_fiscal_base.campo_variavel_homologacao()
        
        self.danfe.band_page_header.child_bands.append(self.danfe.mensagem_fiscal_base)
        
        self.danfe.qrcode_danfe.gera_img_qrcode()
        self.danfe.band_page_header.child_bands.append(self.danfe.qrcode_danfe)
        
        if self.NFe.infNFe.total.ICMSTot.vTotTrib.valor:
            self.danfe.band_page_header.child_bands.append(self.danfe.tributos_totais)
        
        ##Ajustar o tamanho da pagina
        self.danfe.set_report_height(n_produtos=len(self.NFe.infNFe.det), n_pag=len(self.NFe.infNFe.pag))
        
        if self.salvar_arquivo:
            self.caminho = self.monta_caminho_danfe(ambiente=self.NFe.infNFe.ide.tpAmb.valor, chave_nfe=self.NFe.chave, dir='DANFCE')
            nome_arq = self.caminho + self.NFe.chave + u'.pdf'
            type(self.danfe.generate_by(PDFGenerator, filename=nome_arq))
    
    def monta_caminho_danfe(self, ambiente, chave_nfe, dir=''):
        caminho = self.caminho + u'ArquivosXML/NFe/'

        if ambiente == 1:
            caminho = os.path.join(caminho, 'producao/')
        else:
            caminho = os.path.join(caminho, 'homologacao/')

        data = u'20' + chave_nfe[2:4] + u'-' + chave_nfe[4:6]
        if dir:
            caminho = os.path.join(caminho, data + u'/' + dir + u'/')
        else:
            serie = chave_nfe[22:25]
            numero = chave_nfe[25:34]

            caminho = os.path.join(caminho, data + u'/')
            caminho = os.path.join(caminho, serie + u'-' + numero + u'/')
        
        try:
            os.makedirs(caminho)
        except:
            pass
        
        return caminho
