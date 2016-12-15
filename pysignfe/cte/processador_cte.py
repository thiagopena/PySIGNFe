# -*- coding: utf-8 -*-

from http.client import HTTPSConnection, HTTPResponse
from datetime import datetime
import time
from uuid import uuid4
import os
import pytz

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from pysignfe.corr_unicode import *

from pysignfe.xml_sped import *

from pysignfe.nfe.webservices_flags import CODIGO_UF, UF_CODIGO
from .webservices_flags import *
from . import webservices

from pysignfe.xml_sped.certificado import Certificado

#Versão 3.00
from .v300 import ConsStatServCTe_300, RetConsStatServCTe_300
from .v300 import SOAPEnvio_300, SOAPRetorno_300
from .v300 import ConsSitCTe_300, RetConsSitCTe_300
from .v300 import EnviCTe_300, RetEnviCTe_300
from .v300 import ConsReciCTe_300, RetConsReciCTe_300, ProcCTe_300, ProtCTe_300
from .v300 import InutCTe_300, RetInutCTe_300, ProcInutCTe_300
from .v300 import EventoCTe_300, RetEventoCTe_300, ProcEventoCTe_300
#Eventos
from .v300 import EvCancCTe_300, EvEPECCTe_300, EvRegMultimodal_300, EvCCeCTe_300, EvPrestDesacordo_300, EvGTV_300


class ProcessoCTe(object):
    def __init__(self, webservice=0, envio=u'', resposta=u''):
        self.webservice = webservice
        self.envio = envio
        self.resposta = resposta

class ProcessadorCTe(object):
    def __init__(self):
        self.ambiente = 2
        self.estado = u'MG'
        self.versao = u'2.00'
        self.certificado = Certificado()
        self.caminho = u''
        self.salvar_arquivos = True
        self.tipo_contingencia = False
        self.caminho_temporario = u''
        self.numero_tentativas_consulta_recibo = 2
        self.verificar_status_servico = True
        self.processos = []

        self._servidor     = u''
        self._url          = u''
        self._soap_envio   = None
        self._soap_retorno = None
    
    def _conectar_servico(self, servico, envio, resposta, ambiente=None):
        print ('  CT-e versao...', self.versao)
        print ('  Conectando ao webservice.........')
        if ambiente is None:
            ambiente = self.ambiente

        if self.versao == u'3.00':
            self._soap_envio   = SOAPEnvio_300()
            self._soap_envio.webservice = webservices.METODO_WS[servico]['webservice']
            self._soap_envio.metodo     = webservices.METODO_WS[servico]['metodo']
            self._soap_envio.cUF        = UF_CODIGO[self.estado]
            self._soap_envio.envio      = envio

            self._soap_retorno = SOAPRetorno_300()
            self._soap_retorno.webservice = webservices.METODO_WS[servico]['webservice']
            self._soap_retorno.metodo     = webservices.METODO_WS[servico]['metodo']
            self._soap_retorno.resposta   = resposta

            self._servidor = webservices.ESTADO_WS[self.estado][ambiente][u'servidor']
            self._url      = webservices.ESTADO_WS[self.estado][ambiente][servico]
            

        #try:
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
        # Tudo certo!
        #print ('servidor:', self._servidor)
        #print('url: ', self._url)
        #print ('STATUS__-', self._soap_retorno.resposta.original)
        if self._soap_retorno.resposta.status == 200:
            self._soap_retorno.xml = self._soap_retorno.resposta.original
            
        con.close()
        
    def consultar_servico(self, ambiente=None):
        print("## Consultando status do servidor... ##")
        novos_arquivos = []

        if self.versao == u'3.00':
            envio = ConsStatServCTe_300()
            resposta = RetConsStatServCTe_300()
        else:
            raise ValueError(u"Versao invalida.")

        processo = ProcessoCTe(webservice=WS_CTE_STATUS_SERVICO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        envio.tpAmb.valor = ambiente
        envio.data        = datetime.now()

        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = envio.data.strftime(u'%Y-%m-%dT%H%M%S') + u'-ped-sta.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

        self._conectar_servico(WS_CTE_STATUS_SERVICO, envio, resposta, ambiente)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = envio.data.strftime(u'%Y-%m-%dT%H%M%S') + u'-sta.xml'
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        
            caminho_original = self.caminho
            self.caminho = self.caminho + u'ArquivosXML/ConsultaStatusServidorCTe/'
            
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
            
        return processo
        
    def consultar_recibo(self, ambiente=None, numero_recibo=None):
        print('## Consultando o recibo... ##')
        novos_arquivos = []

        if self.versao == u'3.00':
            envio = ConsReciCTe_300()
            resposta = RetConsReciCTe_300()
            webservice = WS_CTE_RET_RECEPCAO
        else:
            raise ValueError(u"Versao invalida.")

        processo = ProcessoCTe(webservice=webservice, envio=envio, resposta=resposta)
        
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

            #
            # Salvar os resultados dos processamentos
            #
            for pc in resposta.protCTe:
                novo_arquivo_nome = unicode(pc.infProt.chCTe.valor).strip().rjust(44, u'0') + u'-pro-cte'

                # CT-e autorizada
                if pc.infProt.cStat.valor == u'100':
                    novo_arquivo_nome += u'.xml'

                # CT-e denegada
                elif pc.infProt.cStat.valor in (u'110', u'301', u'302'):
                    novo_arquivo_nome += u'-den.xml'

                # CT-e rejeitada
                else:
                    novo_arquivo_nome += u'-rej.xml'

                novo_arquivo = pc.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                caminho_original = self.caminho
                self.caminho = self.monta_caminho_cte(ambiente=ambiente, chave_cte=pc.infProt.chCTe.valor)
                self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
                self.caminho = caminho_original
                
        return processo
        
    def enviar_lote(self, numero_lote=None, lista_cte=[]):
        print("## Enviando lote... ##")
        novos_arquivos = []

        if self.versao == u'3.00':
            envio = EnviCTe_300()
            resposta = RetEnviCTe_300()
            webservice = WS_CTE_RECEPCAO
        else:
            raise ValueError(u"Versao invalida.")
            
        processo = ProcessoCTe(webservice=webservice, envio=envio, resposta=resposta)

        #
        # Vamos assinar e validar todas as CT-e antes da transmissão, evitando
        # rejeição na SEFAZ por incorreção no schema dos arquivos
        #
        for cte in lista_cte:
            self.certificado.assina_xmlnfe(cte)
            cte.validar()

        envio.CTe = lista_cte

        if numero_lote is None:
            numero_lote = datetime.now().strftime('%Y%m%d%H%M%S')

        envio.idLote.valor = numero_lote        
        envio.validar()
        
        if self.salvar_arquivos:
            for c in lista_cte:
                c.monta_chave()
                novo_arquivo_nome = c.chave + u'-cte.xml'
                novo_arquivo = c.xml.encode('utf-8')
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
    
        
    def consultar_cte(self, ambiente=None, chave_cte=None, cte=None):
        novos_arquivos = []

        if self.versao == u'3.00':
            envio = ConsSitCTe_300()
            resposta = RetConsSitCTe_300()
        else:
            raise ValueError(u"Versao invalida.")

        processo = ProcessoCTe(webservice=WS_CTE_CONSULTA, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        envio.tpAmb.valor = ambiente
        envio.chCTe.valor = chave_cte
        
        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(chave_cte).strip().rjust(44, u'0') + u'-ped-sit.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        

        self._conectar_servico(WS_CTE_CONSULTA, envio, resposta, ambiente)
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(chave_cte).strip().rjust(44, u'0') + u'-sit.xml'
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            self.caminho = self.monta_caminho_cte(ambiente, chave_cte)
                
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
        
        return processo
        
    def inutilizar_cte(self, ambiente=None, codigo_estado=None, ano=None, cnpj=None, serie=None,
                        numero_inicial=None, numero_final=None, justificativa=None):
        novos_arquivos = []

        if self.versao == u'3.00':
            envio = InutCTe_300()
            resposta = RetInutCTe_300()
        else:
            raise ValueError(u"Versao invalida.")

        processo = ProcessoCTe(webservice=WS_CTE_INUTILIZACAO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        if codigo_estado is None:
            codigo_estado = UF_CODIGO[self.estado]

        if ano is None:
            ano = datetime.now().strftime(u'%y')

        if numero_final is None:
            numero_final = numero_inicial

        self.caminho = self.monta_caminho_inutilizacao(ambiente=ambiente, serie=serie,
                                    numero_inicial=numero_inicial, numero_final=numero_final)

        envio.infInut.tpAmb.valor  = ambiente
        envio.infInut.cUF.valor    = codigo_estado
        envio.infInut.ano.valor    = ano
        envio.infInut.CNPJ.valor   = cnpj
        envio.infInut.mod.valor    = 57
        envio.infInut.serie.valor  = serie
        envio.infInut.nCTIni.valor = numero_inicial
        envio.infInut.nCTFin.valor = numero_final
        envio.infInut.xJust.valor  = justificativa

        envio.gera_nova_chave()
        self.certificado.prepara_certificado_arquivo_pfx()
        self.certificado.assina_xmlnfe(envio)

        envio.validar()
        
        if self.salvar_arquivos:
            nome_arq = unicode(envio.infInut.cUF.valor) + unicode(envio.infInut.ano.valor) + unicode(envio.infInut.CNPJ.valor) + unicode(envio.infInut.mod.valor) + unicode(envio.infInut.serie.valor)\
                + unicode(envio.infInut.nCTIni.valor) + unicode(envio.infInut.nCTFin.valor)
            novo_arquivo_nome = nome_arq + u'-ped-inu.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
    
        self._conectar_servico(WS_CTE_INUTILIZACAO, envio, resposta, ambiente)

        # Se for autorizada, monta o processo de inutilização
        if resposta.infInut.cStat.valor == u'102':
            
            processo_inutilizacao_cte = ProcInutCTe_300()

            processo_inutilizacao_cte.inutCTe = envio
            processo_inutilizacao_cte.retInutCTe = resposta

            processo_inutilizacao_cte.validar()

            processo.processo_inutilizacao_cte = processo_inutilizacao_cte
            

        if self.salvar_arquivos:
            nome_arq = unicode(envio.infInut.ano.valor) + unicode(envio.infInut.CNPJ.valor) + unicode(envio.infInut.mod.valor) + unicode(envio.infInut.serie.valor)\
                + unicode(envio.infInut.nCTIni.valor) + unicode(envio.infInut.nCTFin.valor)
            novo_arquivo_nome = nome_arq + u'-inu'

            # Inutilização autorizada
            if resposta.infInut.cStat.valor == u'102':
                novo_arquivo_nome += u'.xml'
            else:
                novo_arquivo_nome += u'-rej.xml'

            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            # Se for autorizada, monta o processo de inutilização
            if resposta.infInut.cStat.valor == u'102':
                nome_arq = unicode(resposta.nProt.valor) + '_v' + unicode(self.versao).zfill(5)
                novo_arquivo_nome = nome_arq + u'-procInutCTe.xml'
                novo_arquivo = processo_inutilizacao_cte.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
    
        return processo
        
    def monta_caminho_inutilizacao(self, ambiente=None, data=None, serie=None, numero_inicial=None, numero_final=None):
        caminho = self.caminho + u'ArquivosXML/CTe/'

        if ambiente == 1:
            caminho = os.path.join(caminho, 'producao/')
        else:
            caminho = os.path.join(caminho, 'homologacao/')

        if data is None:
            data = datetime.now()

        caminho = os.path.join(caminho, data.strftime(u'%Y-%m') + u'/')

        serie          = unicode(serie).strip().rjust(3, u'0')
        numero_inicial = unicode(numero_inicial).strip().rjust(9, u'0')
        numero_final   = unicode(numero_final).strip().rjust(9, u'0')

        caminho = os.path.join(caminho, serie + u'-' + numero_inicial + u'-' + numero_final + u'/')
        
        return caminho
        
    def processar_lote_cte(self, lista_cte):
    
        self.processos = processos = OrderedDict()
        novos_arquivos = []

        caminho_original = self.caminho
        cte = lista_cte[0]
        cte.monta_chave()
        ambiente = cte.infCte.ide.tpAmb.valor
        status_serv = u'107'
        if self.verificar_status_servico:
            proc_servico = self.consultar_servico(ambiente=ambiente)
            yield proc_servico
            status_serv = proc_servico.resposta.cStat.valor
            print (' resposta status servico: ', status_serv)
        
        #Servico em operacao (status == 107)
        if status_serv == u'107' or 107:
            #
            # Verificar se as notas já não foram emitadas antes
            #
            print("Verificando se CTes ja foram enviadas...")
            for cte in lista_cte:
                cte.monta_chave()
                self.caminho = caminho_original
                proc_consulta = self.consultar_cte(ambiente=ambiente, chave_cte=cte.chave)
                yield proc_consulta

                #
                # Se a nota já constar na SEFAZ
                #
                if not (
                    (self.versao == u'3.00') and (proc_consulta.resposta.cStat.valor in (u'217', u'999',))
                ):
                    #
                    # Interrompe todo o processo
                    #
                    print(" !!Nota ja enviada ou com erro | Status: "+ proc_consulta.resposta.cStat.valor +". Encerrando processo...")
                    return
            #
            # Nenhuma das notas estava já enviada, enviá-las então
            #
            cte = lista_cte[0]
            cte.monta_chave()
            self.caminho = caminho_original
            self.caminho = self.monta_caminho_cte(ambiente=cte.infCte.ide.tpAmb.valor, chave_cte=cte.chave)
            proc_envio = self.enviar_lote(lista_cte=lista_cte)
            yield proc_envio
            self.caminho = caminho_original
            
            ret_envi_cte = proc_envio.resposta
            
            #
            # Deu certo?
            #
            if ret_envi_cte.cStat.valor == u'103':
                print(" Lote enviado com sucesso.")
                t_espera = ret_envi_cte.infRec.tMed.valor
                #Alguns webservices exageram no tempo de espera.
                if t_espera > 10:
                    t_espera = 6
                time.sleep(t_espera * 2) # Espere o processamento antes de consultar o recibo
                proc_recibo = self.consultar_recibo(ambiente=ret_envi_cte.tpAmb.valor, numero_recibo=ret_envi_cte.infRec.nRec.valor)
                
                tentativa = 0
                while  proc_recibo.resposta.cStat.valor == u'105' and tentativa < self.numero_tentativas_consulta_recibo:
                    time.sleep(t_espera * 2) # Espere o processamento antes de consultar o recibo
                    proc_recibo = self.consultar_recibo(ambiente=ret_envi_cte.tpAmb.valor, numero_recibo=ret_envi_cte.infRec.nRec.valor)
                    tentativa += 1
                yield proc_recibo
                
                # Montar os processos das CT-es
                dic_protCTe = proc_recibo.resposta.dic_protCTe
                dic_procCTe = proc_recibo.resposta.dic_procCTe
                
                self.caminho = caminho_original
                novos_processos = self.montar_processo_lista_notas(lista_cte, dic_protCTe, dic_procCTe)
                for i,novo_processo in enumerate(novos_processos):
                    processos['cte_%i' % i] = novo_processo
                
                return
                
    def montar_processo_lista_notas(self, lista_cte, dic_protCTe, dic_procCTe):
        processos = []
        for cte in lista_cte:
            if cte.chave in dic_protCTe:
                protocolo = dic_protCTe[cte.chave]
                processo = self.montar_processo_uma_nota(cte, protcte_recibo=protocolo)
                processos.append(processo)
                
                if processo is not None:
                    dic_procCTe[cte.chave] = processo
        return processos
        
    def montar_processo_uma_nota(self, cte, protcte_recibo=None):
        novos_arquivos = []
        
        caminho_original = self.caminho
        self.caminho = self.monta_caminho_cte(ambiente=cte.infCte.ide.tpAmb.valor, chave_cte=cte.chave)

        processo = None
        # Se nota foi autorizada ou denegada
        if protcte_recibo.infProt.cStat.valor in (u'100', u'150', u'110', u'301', u'302'):

            if self.versao == u'3.00':
                processo = ProcCTe_300()
            else:
                raise ValueError(u"Versao invalida.")

            processo.CTe     = cte
            processo.protCTe = protcte_recibo
            #novos_arquivos.append(('numero_protocolo', protcte_recibo.infProt.nProt.valor))
                        
            if self.salvar_arquivos:
                nome_arq = unicode(processo.protCTe.infProt.nProt.valor) + unicode(self.versao).zfill(5)
                novo_arquivo_nome = nome_arq + u'-procCTe.xml'
                novo_arquivo = processo.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                
                # Estranhamente, o nome desse arquivo, pelo manual, deve ser chave-cte.xml ou chave-den.xml
                # para notas denegadas
                if protcte_recibo.infProt.cStat.valor == u'100':
                    novo_arquivo_nome = unicode(cte.chave).strip().rjust(44, u'0') + u'-cte.xml'
                else:
                    novo_arquivo_nome = unicode(cte.chave).strip().rjust(44, u'0') + u'-den.xml'

                novo_arquivo_nome = novo_arquivo_nome
                novo_arquivo = processo.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
        # Se houve erro no lote, para buscar codigo e mensagem de erro
        else:
            processo         = ProcCTe_300()
            processo.CTe     = cte
            processo.protCTe = protcte_recibo
                
        self.caminho = caminho_original
        return processo
        
    def cancelar_cte(self, cnpj=None, ambiente=None, chave_cte=None, numero_protocolo=None,
                      justificativa=None, sequencia=None):
        novos_arquivos = []

        if self.versao == u'3.00':
            envio = EventoCTe_300()
            resposta = RetEventoCTe_300()
        else:
            raise ValueError(u"Versao invalida.")

        processo = ProcessoCTe(webservice=WS_CTE_EVENTO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        self.caminho = self.monta_caminho_cte(ambiente=ambiente, chave_cte=chave_cte)

        #evento
        envio.infEvento.cOrgao.valor = UF_CODIGO[self.estado]
        envio.infEvento.tpAmb.valor = ambiente
        envio.infEvento.CNPJ.valor = cnpj
        envio.infEvento.chCTe.valor = chave_cte
        
        dt = datetime.now()
        dt = dt.replace(tzinfo=pytz.utc)
        data_hora_tz = datetime.astimezone(dt, pytz.timezone("Brazil/East"))
        data_evento = datetime.strftime(data_hora_tz, u'%Y-%m-%dT%H:%M:%S')+str(data_hora_tz)[-6:]
        envio.infEvento.dhEvento.valor = data_evento
        envio.infEvento.tpEvento.valor = '110111' #codigo evento cancelamento
        envio.infEvento.nSeqEvento.valor = sequencia or 1
        
        envio.infEvento.detEvento.evento = EvCancCTe_300()
        envio.infEvento.detEvento.evento.nProt.valor = numero_protocolo
        envio.infEvento.detEvento.evento.xJust.valor = justificativa
        
        self.certificado.prepara_certificado_arquivo_pfx()
        self.certificado.assina_xmlnfe(envio)

        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.infEvento.chCTe.valor).strip().rjust(44, u'0') + u'-ped-eve.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

        self._conectar_servico(WS_CTE_EVENTO, envio, resposta, ambiente)

        # Caso evento foi homologado, montar processo de cancelamento
        if resposta.infEvento.cStat.valor in ('134', '135', '136',):
        
            processo_evento_cte = ProcEventoCTe_300()
            
            processo_evento_cte.eventoCTe = envio
            processo_evento_cte.retEventoCTe = resposta

            processo_evento_cte.validar()

            processo.processo_evento_cte = processo_evento_cte

        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.infEvento.chCTe.valor).strip().rjust(44, u'0') + u'-eve'

            # Cancelamento autorizado
            if resposta.infEvento.cStat.valor in (u'135'):
                novo_arquivo_nome += u'.xml'
            else:
                novo_arquivo_nome += u'-rej.xml'

            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            # Se for autorizado, monta o processo de cancelamento
            if resposta.infEvento.cStat.valor == u'135':
                # Estranhamente, o nome desse arquivo, pelo manual, deve ser chave-can.xml
                #novo_arquivo_nome = unicode(envio.infEvento.chCTe.valor).strip().rjust(44, u'0') + u'-can.xml'
                nome_arq = unicode(resposta.infEvento.nProt.valor) + u'_v' + unicode(self.versao).zfill(5)
                novo_arquivo_nome = nome_arq + u'-eventoCTe.xml'
                novo_arquivo = processo_evento_cte.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)

        return processo
        
    def corrigir_cte(self, correcoes=[], chave_cte=None, cnpj=None, ambiente=None,
                      sequencia=None):
        novos_arquivos = []
        if self.versao == u'3.00':
            envio = EventoCTe_300()
            resposta = RetEventoCTe_300()
        else:
            raise ValueError(u"Versao invalida.")

        processo = ProcessoCTe(webservice=WS_CTE_EVENTO, envio=envio, resposta=resposta)

        if ambiente is None:
            ambiente = self.ambiente

        self.caminho = self.monta_caminho_cte(ambiente=ambiente, chave_cte=chave_cte)

        #evento
        envio.infEvento.cOrgao.valor = UF_CODIGO[self.estado]
        envio.infEvento.tpAmb.valor = ambiente
        envio.infEvento.CNPJ.valor = cnpj
        envio.infEvento.chCTe.valor = chave_cte
        
        dt = datetime.now()
        dt = dt.replace(tzinfo=pytz.utc)
        data_hora_tz = datetime.astimezone(dt, pytz.timezone("Brazil/East"))
        data_evento = datetime.strftime(data_hora_tz, u'%Y-%m-%dT%H:%M:%S')+str(data_hora_tz)[-6:]
        envio.infEvento.dhEvento.valor = data_evento
        envio.infEvento.tpEvento.valor = '110110' #codigo evento carta correcao
        envio.infEvento.nSeqEvento.valor = sequencia or 1
        
        envio.infEvento.detEvento.evento = EvCCeCTe_300()
        envio.infEvento.detEvento.evento.infCorrecao = correcoes
        
        self.certificado.prepara_certificado_arquivo_pfx()
        self.certificado.assina_xmlnfe(envio)

        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.infEvento.chCTe.valor).strip().rjust(44, u'0') + u'-ped-eve.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

        self._conectar_servico(WS_CTE_EVENTO, envio, resposta, ambiente)

        # Caso evento foi homologado, montar processo de cancelamento
        if resposta.infEvento.cStat.valor in ('134', '135', '136',):
        
            processo_evento_cte = ProcEventoCTe_300()
            
            processo_evento_cte.eventoCTe = envio
            processo_evento_cte.retEventoCTe = resposta

            processo_evento_cte.validar()

            processo.processo_evento_cte = processo_evento_cte

        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.infEvento.chCTe.valor).strip().rjust(44, u'0') + u'-eve'

            # Cancelamento autorizado
            if resposta.infEvento.cStat.valor in (u'135'):
                novo_arquivo_nome += u'.xml'
            else:
                novo_arquivo_nome += u'-rej.xml'

            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))

            # Se for autorizado, monta o processo de cancelamento
            if resposta.infEvento.cStat.valor == u'135':
                # Estranhamente, o nome desse arquivo, pelo manual, deve ser chave-can.xml
                #novo_arquivo_nome = unicode(envio.infEvento.chCTe.valor).strip().rjust(44, u'0') + u'-can.xml'
                nome_arq = unicode(resposta.infEvento.nProt.valor) + u'_v' + unicode(self.versao).zfill(5)
                novo_arquivo_nome = nome_arq + u'-eventoCTe.xml'
                novo_arquivo = processo_evento_cte.xml.encode('utf-8')
                novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)

        return processo
    
                    
    def monta_caminho_cte(self, ambiente, chave_cte):
        caminho = self.caminho + u'ArquivosXML/CTe/'

        if ambiente == 1:
            caminho = os.path.join(caminho, 'producao/')
        else:
            caminho = os.path.join(caminho, 'homologacao/')

        data = u'20' + chave_cte[2:4] + u'-' + chave_cte[4:6]
        serie = chave_cte[22:25]
        numero = chave_cte[25:34]

        caminho = os.path.join(caminho, data + u'/')
        caminho = os.path.join(caminho, serie + u'-' + numero + u'/')

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