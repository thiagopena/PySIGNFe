# -*- coding: utf-8 -*-

from http.client import HTTPSConnection, HTTPResponse
from uuid import uuid4
import ssl
import os
from datetime import datetime
import time
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from pysignfe.xml_sped.certificado import Certificado
from pysignfe.xml_sped import *

#Versao 1.0
from .bhiss.v10 import SOAPEnvio_10, SOAPRetorno_10
from .bhiss.v10 import ConsultarSituacaoLoteRpsEnvio_10, ConsultarSituacaoLoteRpsResposta_10
from .bhiss.v10 import ConsultarNfseRpsEnvio_10, ConsultarNfseRpsResposta_10
from .bhiss.v10 import EnviarLoteRpsEnvio_10, EnviarLoteRpsResposta_10
from .bhiss.v10 import ConsultarLoteRpsEnvio_10, ConsultarLoteRpsResposta_10
from .bhiss.v10 import GerarNfseEnvio_10, GerarNfseResposta_10
from .bhiss.v10 import ConsultarNfseEnvio_10, ConsultarNfseResposta_10
from .bhiss.v10 import CancelarNfseEnvio_10, CancelarNfseResposta_10

from pysignfe.corr_unicode import *
from .webservices_flags import *
from . import webservices


class ProcessoNFSe(object):
    def __init__(self, webservice=0, envio=u'', resposta=u''):
        self.webservice = webservice
        self.envio = envio
        self.resposta = resposta
        self.msg_retorno = u''


class ProcessadorNFSeBH(object):
    def __init__(self):
        self.ambiente = 2
        self.versao = u'1.0'
        self.n_rps = 1
        self.certificado = Certificado()
        self.caminho = u''
        self.salvar_arquivos = True
        self.caminho_temporario = u''
        self.processos = []

        self._servidor     = u''
        self._url          = u''
        self._soap_envio   = None
        self._soap_retorno = None
    
    def _conectar_servico(self, servico, envio, resposta, ambiente=None):
        print("Conectando servico...")
        if ambiente is None:
            ambiente = self.ambiente
                
        if self.versao == u'1.0':
            self._soap_envio        = SOAPEnvio_10()
            self._soap_envio.metodo = webservices.METODO_WS[servico]['metodo']
            self._soap_envio.envio  = envio
            
            self._soap_retorno = SOAPRetorno_10()
            self._soap_retorno.metodo     = webservices.METODO_WS[servico]['metodo']
            self._soap_retorno.resposta   = resposta
            
            self._servidor = webservices.WEBSERVICES_BH[ambiente]['servidor']
            self._url      = webservices.WEBSERVICES_BH[ambiente]['url']
            
        
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
        
        print("servidor: ",self._servidor)
        print("url: ", self._url)
        
        fpath =  os.path.dirname(os.path.abspath(__file__))
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1)
        context.load_verify_locations(capath=fpath + "certificados/bhisscert64.cer")
                
        con = HTTPSConnection(self._servidor, key_file=nome_arq_chave, cert_file=nome_arq_certificado, context=context)
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
        
        #Dados da resposta salvos para possível debug
        self._soap_retorno.resposta.version  = resp.version
        self._soap_retorno.resposta.status   = resp.status
        #self._soap_retorno.resposta.reason   = unicode(resp.reason.decode('utf-8'))
        self._soap_retorno.resposta.reason   = unicode(resp.reason)
        self._soap_retorno.resposta.msg      = resp.msg
        self._soap_retorno.resposta.original = unicode(resp.read().decode('utf-8'))
        # Tudo certo!
        if self._soap_retorno.resposta.status == 200:
            self._soap_retorno.xml = self._soap_retorno.resposta.original

        con.close()
    
    def consultar_situacao_lote_rps(self, numero_lote=None, cnpj=None, im=None, protocolo=None):
        novos_arquivos = []
                
        if self.versao == u'1.0':
            envio = ConsultarSituacaoLoteRpsEnvio_10()
            resposta = ConsultarSituacaoLoteRpsResposta_10()
        else:
            raise ValueError(u"Versao invalida.")
            
        processo = ProcessoNFSe(webservice=WS_NFSE_CONSULTAR_SIT_LOTE_RPS, envio=envio, resposta=resposta)

        envio.Prestador.Cnpj.valor = cnpj
        envio.Prestador.InscricaoMunicipal.valor = im
        envio.Protocolo.valor = protocolo
        
        envio.validar()
                
        self._conectar_servico(WS_NFSE_CONSULTAR_SIT_LOTE_RPS, envio, resposta)
        
        if len(processo.resposta.ListaMensagemRetorno.MensagemRetorno) != 0:
            for err in processo.resposta.ListaMensagemRetorno.MensagemRetorno:
                processo.msg_retorno += err.Codigo.valor + " : " + err.Mensagem.valor + "\n"
        
        if self.salvar_arquivos:
            n_lote = numero_lote or str(resposta.NumeroLote.valor).strip().rjust(15, u'0')
            novo_arquivo_nome = n_lote + u'-sit-env.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            novo_arquivo_nome = n_lote + u'-sit'
            if processo.msg_retorno != u'':
                novo_arquivo_nome += u'-rej.xml'
            else:
                novo_arquivo_nome += u'.xml' 
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            self.caminho = self.monta_caminho_nfse(identificacao=n_lote)
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
        
        return processo
        
    def consultar_lote_rps(self, cnpj=None, im=None, protocolo=None):
        novos_arquivos = []
                
        if self.versao == u'1.0':
            envio = ConsultarLoteRpsEnvio_10()
            resposta = ConsultarLoteRpsResposta_10()
        else:
            raise ValueError(u"Versao invalida.")
            
        processo = ProcessoNFSe(webservice=WS_NFSE_CONSULTAR_LOTE_RPS, envio=envio, resposta=resposta)

        envio.Prestador.Cnpj.valor = cnpj
        envio.Prestador.InscricaoMunicipal.valor = im
        envio.Protocolo.valor = protocolo
        
        envio.validar()
                
        self._conectar_servico(WS_NFSE_CONSULTAR_LOTE_RPS, envio, resposta)
        
        if len(processo.resposta.ListaMensagemRetorno.MensagemRetorno) != 0:
            #Arquivos nao serao salvas caso retorne erro
            self.salvar_arquivos = False
            for err in processo.resposta.ListaMensagemRetorno.MensagemRetorno:
                processo.msg_retorno += err.Codigo.valor + " : " + err.Mensagem.valor + "\n"
        
        if self.salvar_arquivos:
            #identificar pelo Numero da primeira CompNfse retornada
            n_nfse = str(resposta.CompNfse[0].Nfse.InfNfse.Numero.valor).strip().rjust(15, u'0')
            novo_arquivo_nome = n_nfse + u'-cons-lot-rps-env.xml'
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            novo_arquivo_nome = n_nfse + u'-cons-lot-rps-ret'
            if processo.msg_retorno != u'':
                novo_arquivo_nome += u'-rej.xml'
            else:
                novo_arquivo_nome += u'.xml' 
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            self.caminho = self.monta_caminho_nfse(identificacao=n_nfse)
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
        
        return processo
         
    def consultar_nfse_por_rps(self, rps, ident=None):
        novos_arquivos = []
        
        if self.versao == u'1.0':
            envio = ConsultarNfseRpsEnvio_10()
            resposta = ConsultarNfseRpsResposta_10()
        else:
            raise ValueError(u"Versao invalida.")
        
        processo = ProcessoNFSe(webservice=WS_NFSE_CONSULTAR_NFSE_POR_RPS, envio=envio, resposta=resposta)
        
        envio.IdentificacaoRps = rps.InfRps.IdentificacaoRps
        envio.Prestador = rps.InfRps.Prestador
        
        envio.validar()
                
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.IdentificacaoRps.Numero.valor).replace(":","_").strip().rjust(15, u'0') + u'-comp-nfse-env.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        
        self._conectar_servico(WS_NFSE_CONSULTAR_NFSE_POR_RPS, envio, resposta)
        
        if len(processo.resposta.ListaMensagemRetorno.MensagemRetorno) != 0:
            for err in processo.resposta.ListaMensagemRetorno.MensagemRetorno:
                processo.msg_retorno += err.Codigo.valor + " : " + err.Mensagem.valor + "\n"
        
        if self.salvar_arquivos:
            novo_arquivo_nome = unicode(envio.IdentificacaoRps.Numero.valor).replace(":","_").strip().rjust(15, u'0') + u'-comp-nfse'
            if processo.msg_retorno != u'':
                novo_arquivo_nome += u'-rej.xml'
            else:
                novo_arquivo_nome += u'.xml'
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            #ident = ident or unicode(rps.InfRps.Id.valor).replace(":","_").strip().rjust(15, u'0')
            ident = ident or (unicode(envio.IdentificacaoRps.Numero.valor) + unicode(envio.IdentificacaoRps.Serie.valor))
            self.caminho = self.monta_caminho_nfse(identificacao=ident)
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
            
        return processo
        
    def enviar_lote_rps(self, numero_lote=None, lista_rps=[], cnpj=None, im=None, webservice=None):
        print("## Enviando lote de RPS... ##")
        novos_arquivos = []
        self.certificado.prepara_certificado_arquivo_pfx()
        
        if webservice == WS_NFSE_RECEPCIONAR_LOTE_RPS:
            if self.versao == u'1.0':
                envio = EnviarLoteRpsEnvio_10()
                resposta = EnviarLoteRpsResposta_10()
            else:
                raise ValueError(u"Versao invalida.")
        elif webservice == WS_NFSE_GERAR_NFSE:
            if self.versao == u'1.0':
                envio = GerarNfseEnvio_10()
                resposta = GerarNfseResposta_10()
            else:
                raise ValueError(u"Versao invalida.")
        else:
            raise ValueError("Webservice incorreto para envio de lote.")
        
        processo = ProcessoNFSe(webservice=webservice, envio=envio, resposta=resposta)
        
        #Assinar as RPS
        for rps in lista_rps:
            self.certificado.assina_xmlnfe(rps)

        envio.LoteRps.Rps = lista_rps
        
        #Escolhe CNPJ e IM da primeira RPS
        if cnpj is None:
            envio.LoteRps.Cnpj.valor = lista_rps[0].InfRps.Prestador.Cnpj.valor
        if im is None:
            envio.LoteRps.InscricaoMunicipal.valor = lista_rps[0].InfRps.Prestador.InscricaoMunicipal.valor
        
        envio.LoteRps.QuantidadeRps.valor = len(lista_rps)
        
        envio.LoteRps.NumeroLote.valor = numero_lote
        envio.LoteRps.Id.valor = u'lote:'+str(numero_lote)
        
        #Assinar o lote
        self.certificado.assina_xmlnfe(envio)
        envio.validar()
        '''
        Salvar RPSs individualmente
        for r in lista_rps:
            novo_arquivo_nome = r.InfRps.Id.valor + u'-rps.xml'
            novo_arquivo = r.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        '''
        if self.salvar_arquivos:
            novo_arquivo_nome = str(envio.LoteRps.Id.valor).strip().replace(":","_").rjust(15, u'0')
            if webservice == WS_NFSE_GERAR_NFSE:
                novo_arquivo_nome += u'-gerar-nfse-env.xml'
            else:
                novo_arquivo_nome += u'-lot-rps-env.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        
        self._conectar_servico(webservice, envio, resposta)
                
        if webservice == WS_NFSE_GERAR_NFSE:
            if len(processo.resposta.ListaMensagemRetornoLote.MensagemRetornoLote) != 0:
                for lote_err in processo.resposta.ListaMensagemRetornoLote.MensagemRetornoLote:
                    processo.msg_retorno += lote_err.Codigo.valor + " : " + lote_err.Mensagem.valor + "\n"
        
        if len(processo.resposta.ListaMensagemRetorno.MensagemRetorno) != 0:
            for err in processo.resposta.ListaMensagemRetorno.MensagemRetorno:
                processo.msg_retorno += err.Codigo.valor + " : " + err.Mensagem.valor + "\n"
            
        if self.salvar_arquivos:
            novo_arquivo_nome = str(envio.LoteRps.Id.valor).strip().replace(":","_").rjust(15, u'0')
            if webservice == WS_NFSE_GERAR_NFSE:
                novo_arquivo_nome += u'-gerar-nfse-ret'
            else:
                novo_arquivo_nome += u'-lot-rps-ret'
                
            if processo.msg_retorno != u'':
                novo_arquivo_nome += u'-rej.xml'
            else:
                novo_arquivo_nome += u'.xml'
                
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            self.caminho = self.monta_caminho_nfse(identificacao=str(numero_lote))
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
            
        return processo
        
        
    def gerar_nfse(self, lista_rps, numero_lote=None, cnpj=None, im=None):
        self.processos = processos = OrderedDict()
        novos_arquivos = []
        
        #Se o numero do lote nao foi definido pelo usuario, ele será a data atual + um valor incremental
        if numero_lote is None:
            numero_lote = datetime.now().strftime('%Y%m%d%H%M%S') + str(self.n_rps)
            self.n_rps = self.n_rps + 1
        
        proc_envio = self.enviar_lote_rps(numero_lote=numero_lote, lista_rps=lista_rps, cnpj=cnpj, im=im, webservice=WS_NFSE_GERAR_NFSE)
        yield proc_envio
            
    def processar_lote_rps(self, lista_rps, numero_lote=None, cnpj=None, im=None):
        self.processos = processos = OrderedDict()
        novos_arquivos = []
        
        #Se o numero do lote nao foi definido pelo usuario, ele será a data atual + um valor incremental
        if numero_lote is None:
            numero_lote = datetime.now().strftime('%Y%m%d%H%M%S') + str(self.n_rps)
            self.n_rps = self.n_rps + 1
        
        for rps in lista_rps:
            #Verificar se alguma RPS ja foi enviada
            proc_consulta = self.consultar_nfse_por_rps(rps=rps, ident=numero_lote)
            yield proc_consulta
            
            if len(proc_consulta.resposta.ListaMensagemRetorno.MensagemRetorno) == 0:
                #Sem erros, então RPS já foi enviada.
                return
        
        proc_envio = self.enviar_lote_rps(numero_lote=numero_lote, lista_rps=lista_rps, cnpj=cnpj, im=im, webservice=WS_NFSE_RECEPCIONAR_LOTE_RPS)
        yield proc_envio
        
        if len(proc_envio.resposta.ListaMensagemRetorno.MensagemRetorno) == 0:
            print("Lote enviado com sucesso, consultando situacao do lote em 4 segundos...")
            time.sleep(4)
            proc_situacao = self.consultar_situacao_lote_rps(numero_lote=numero_lote, cnpj=proc_envio.envio.LoteRps.Cnpj.valor, im=proc_envio.envio.LoteRps.InscricaoMunicipal.valor, protocolo=proc_envio.resposta.Protocolo.valor)
            yield proc_situacao
        
                
    def consultar_nfse(self, nfse, data_inicial=None, data_final=None):
        novos_arquivos = []
                
        if self.versao == u'1.0':
            envio = ConsultarNfseEnvio_10()
            resposta = ConsultarNfseResposta_10()
        else:
            raise ValueError(u"Versao invalida.")
            
        processo = ProcessoNFSe(webservice=WS_NFSE_CONSULTAR_NFSE, envio=envio, resposta=resposta)
                
        envio.Prestador.Cnpj.valor = nfse.InfNfse.PrestadorServico.IdentificacaoPrestador.Cnpj.valor
        envio.Prestador.InscricaoMunicipal.valor = nfse.InfNfse.PrestadorServico.IdentificacaoPrestador.InscricaoMunicipal.valor
        
        envio.NumeroNfse.valor = nfse.InfNfse.Numero.valor
        
        envio.Tomador.CpfCnpj.Cnpj.valor = nfse.InfNfse.TomadorServico.IdentificacaoTomador.CpfCnpj.Cnpj.valor
        envio.Tomador.InscricaoMunicipal.valor = nfse.InfNfse.TomadorServico.IdentificacaoTomador.InscricaoMunicipal.valor
        
        envio.IntermediarioServico.RazaoSocial.valor = nfse.InfNfse.IntermediarioServico.RazaoSocial.valor
        envio.IntermediarioServico.CpfCnpj.Cnpj.valor = nfse.InfNfse.IntermediarioServico.CpfCnpj.Cnpj.valor
        envio.IntermediarioServico.InscricaoMunicipal.valor = nfse.InfNfse.IntermediarioServico.InscricaoMunicipal.valor
        
        if data_inicial is not None:
            envio.DataInicial.valor = data_inicial
        if data_final is not None:
            envio.DataFinal.valor = data_final
            
        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = str(envio.NumeroNfse.valor).strip().rjust(15, u'0') + u'-comp-nfse-env.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
        
        self._conectar_servico(WS_NFSE_CONSULTAR_NFSE, envio, resposta)
        
        if len(processo.resposta.ListaMensagemRetorno.MensagemRetorno) != 0:
            for err in processo.resposta.ListaMensagemRetorno.MensagemRetorno:
                processo.msg_retorno += err.Codigo.valor + " : " + err.Mensagem.valor + "\n"
        
        if self.salvar_arquivos:
            novo_arquivo_nome = str(envio.NumeroNfse.valor).strip().rjust(15, u'0') + u'-comp-nfse'
            if processo.msg_retorno != u'':
                novo_arquivo_nome += u'-rej.xml'
            else:
                novo_arquivo_nome += u'.xml'
            
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            ident = str(envio.NumeroNfse.valor).strip().rjust(15, u'0')
            self.caminho = self.monta_caminho_nfse(identificacao=ident)
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
        
        return processo
        
    def cancelar_nfse(self, codigo_cancelamento=None, numero_nfse=None, cnpj=None, im=None, codigo_ibge=None):
        novos_arquivos = []
        self.certificado.prepara_certificado_arquivo_pfx()
        
        if self.versao == u'1.0':
            envio = CancelarNfseEnvio_10()
            resposta = CancelarNfseResposta_10()
        else:
            raise ValueError(u"Versao invalida.")
            
        processo = ProcessoNFSe(webservice=WS_NFSE_CANCELAR_NFSE, envio=envio, resposta=resposta)
        
        envio.Pedido.InfPedidoCancelamento.CodigoCancelamento.valor = codigo_cancelamento
        envio.Pedido.InfPedidoCancelamento.IdentificacaoNfse.Numero.valor = numero_nfse
        envio.Pedido.InfPedidoCancelamento.IdentificacaoNfse.Cnpj.valor = cnpj
        envio.Pedido.InfPedidoCancelamento.IdentificacaoNfse.InscricaoMunicipal.valor = im
        envio.Pedido.InfPedidoCancelamento.IdentificacaoNfse.CodigoMunicipio.valor = codigo_ibge
                        
        self.certificado.assina_xmlnfe(envio.Pedido)
        envio.validar()
        
        if self.salvar_arquivos:
            novo_arquivo_nome = str(envio.Pedido.InfPedidoCancelamento.IdentificacaoNfse.Numero.valor).strip().rjust(15, u'0') + u'-ped-can-env.xml'
            novo_arquivo = envio.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
                
        self._conectar_servico(WS_NFSE_CANCELAR_NFSE, envio, resposta)
        
        if len(processo.resposta.ListaMensagemRetorno.MensagemRetorno) != 0:
            for err in processo.resposta.ListaMensagemRetorno.MensagemRetorno:
                processo.msg_retorno += err.Codigo.valor + " : " + err.Mensagem.valor + "\n"
        
        if self.salvar_arquivos:
            n_nfse = str(envio.Pedido.InfPedidoCancelamento.IdentificacaoNfse.Numero.valor).strip().rjust(15, u'0')
            novo_arquivo_nome = n_nfse + u'-can-ret'
            if processo.msg_retorno != u'':
                novo_arquivo_nome += u'-rej.xml'
            else:
                novo_arquivo_nome += u'.xml'
            novo_arquivo = resposta.xml.encode('utf-8')
            novos_arquivos.append((novo_arquivo_nome, novo_arquivo))
            
            caminho_original = self.caminho
            self.caminho = self.monta_caminho_nfse(identificacao=n_nfse)
            self.salvar_novos_arquivos(novos_arquivos=novos_arquivos)
            self.caminho = caminho_original
        
        return processo
                                
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
            
    def monta_caminho_nfse(self, identificacao, ambiente=None):
        caminho = self.caminho + u'ArquivosXML/NFSe/'
        
        ambiente = ambiente or self.ambiente
        
        if ambiente == 1:
            caminho = os.path.join(caminho, 'producao/')
        else:
            caminho = os.path.join(caminho, 'homologacao/')

        data = datetime.now()
        
        caminho = os.path.join(caminho, data.strftime(u'%Y-%m') + u'/')
        caminho = os.path.join(caminho, identificacao + u'/')
        
        return caminho