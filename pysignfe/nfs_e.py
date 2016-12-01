# -*- coding: utf-8 -*-

from .nota import NotaFiscal
from pysignfe.nfse.processador_bh import ProcessadorNFSeBH

class nfs_e(NotaFiscal):
    '''
    Classe de métodos para NFS-e's
    '''
    def consultar_situacao_lote_rps(self, cnpj, im, protocolo, cert, key, ambiente=2, versao=u'1.0', modelo=u'bhiss', salvar_arquivos=True):
        """
        Esse serviço efetua a consulta da situação de um Lote de RPS já enviado. 
        
        @param cnpj: string do cnpj do prestador,
        @param im: inscrição municipal do prestador,
        @param protocolo: numero do protocolo do lote,
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfse,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param modelo: modelo de NFS-e utilizada do municipio,
        @return: Dicionário com o envio, resposta, reason e uma msg_retorno caso haja rejeição.
        
        OBS: Este método apenas informa se o lote está:
          - Não processado; 
          - Processado com erros; 
          - Processado com sucesso.
        """
        
        if modelo==u'bhiss':
            p = ProcessadorNFSeBH()
            
        p.ambiente = ambiente
        p.versao   = versao
        p.certificado.cert_str = cert
        p.certificado.key_str  = key
        p.salvar_arquivos = salvar_arquivos
                
        processo = p.consultar_situacao_lote_rps(cnpj=cnpj, im=im, protocolo=protocolo)
        
        return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
                'reason': processo.resposta.reason, 'msg_retorno' : processo.msg_retorno}
        
    def consultar_lote_rps(self, cnpj, im, protocolo, cert, key, ambiente=2, versao=u'1.0', modelo=u'bhiss', salvar_arquivos=True):
        """
        Esse serviço permite ao contribuinte obter as NFS-e que foram geradas a partir
        do Lote de RPS enviado, quando o processamento ocorrer sem problemas; ou
        obter a lista de erros e/ou inconsistências encontradas nos RPS. 
        
        @param cnpj: string do cnpj do prestador,
        @param im: inscrição municipal do prestador,
        @param protocolo: numero do protocolo do lote,
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfse,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param modelo: modelo de NFS-e utilizada do municipio,
        @return: Dicionário com o envio, resposta, reason e uma msg_retorno caso haja rejeição.
        """
        if modelo==u'bhiss':
            p = ProcessadorNFSeBH()
            
        p.ambiente = ambiente
        p.versao   = versao
        p.certificado.cert_str = cert
        p.certificado.key_str  = key
        p.salvar_arquivos = salvar_arquivos
                
        processo = p.consultar_lote_rps(cnpj=cnpj, im=im, protocolo=protocolo)
        
        return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
                'reason': processo.resposta.reason, 'msg_retorno' : processo.msg_retorno}
                
    def gerar_nfse(self, lista_rps, cert, key, ambiente=2, versao=u'1.0', modelo=u'bhiss', salvar_arquivos=True, numero_lote=None, cnpj=None, im=None):
        """
        Esse serviço compreende a recepção do Lote de até 3 (três) RPS. Quando
        efetuada a recepção, o Lote será processado e serão feitas as validações
        necessárias e geração das NFS-e. 

        @param lista_rps: lista com no maximo 3 RPS's,
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfse,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param modelo: modelo de NFS-e utilizada do municipio,
        @param salvar_arquivos: salvar os arquivos caso não ocorram erros,
        @param numero_lote: caso o usuário queira definir o numero do lote enviado, se None o sistema gera um numero,
        @param cnpj: string com o cnpj do emitente, caso None o cnpj será o do primeiro RPS na lista,
        @param im: string com Inscrição municipal do emitente, cano None será o do primeiro RPS da lista,
        @return: Dicionário com o envio, resposta, reason e uma msg_retorno caso haja rejeição.
        """
        
        #Maximo de 3 RPSs!
        if len(lista_rps) > 3:
            raise ValueError(u"No maximo 3 RPS por lote enviado.")
            
        if modelo==u'bhiss':
            p = ProcessadorNFSeBH()
            
        p.ambiente = ambiente
        p.versao   = versao
        p.certificado.cert_str = cert
        p.certificado.key_str  = key
        p.salvar_arquivos = salvar_arquivos
                
        for processo in p.gerar_nfse(lista_rps=lista_rps, numero_lote=numero_lote, cnpj=cnpj, im=im):
            processo.envio.xml
            processo.resposta.xml
            processo.resposta.reason
                
        return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
                'reason': processo.resposta.reason, 'msg_retorno' : processo.msg_retorno}
        
        
    def consultar_nfse_por_rps(self, rps, cert, key, ambiente=2, versao=u'1.0', modelo=u'bhiss', salvar_arquivos=True):
        """
        Esse serviço efetua a consulta de uma NFS-e a partir do número de RPS que a gerou. 

        @param rps: RPS para consulta,
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfse,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param modelo: modelo de NFS-e utilizada do municipio,
        @return: Dicionário com o envio, resposta, reason e uma msg_retorno caso haja rejeição.
        """
        if modelo==u'bhiss':
            p = ProcessadorNFSeBH()
            
        p.ambiente = ambiente
        p.versao   = versao
        p.certificado.cert_str = cert
        p.certificado.key_str  = key
        p.salvar_arquivos = salvar_arquivos
                
        processo = p.consultar_nfse_por_rps(rps=rps)
        
        return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
                'reason': processo.resposta.reason, 'msg_retorno' : processo.msg_retorno}
                
    def consultar_nfse(self, nfse, cert, key, ambiente=2, versao=u'1.0', modelo=u'bhiss', data_inicial=None, data_final=None, salvar_arquivos=True):
        """
        Esse serviço permite a obtenção de determinada NFS-e já gerada. 

        @param nfse: NFS-e a ser consultada,
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfse,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param modelo: modelo de NFS-e utilizada do municipio,
        @param data_inicial: data inicial do periodo de emissao, formato date,
        @param data_final: data final do periodo de emissao, formato date,
        @return: Dicionário com o envio, resposta, reason e uma msg_retorno caso haja rejeição.
        """
    
        if modelo==u'bhiss':
            p = ProcessadorNFSeBH()
            
        p.ambiente = ambiente
        p.versao   = versao
        p.certificado.cert_str = cert
        p.certificado.key_str  = key
        p.salvar_arquivos = salvar_arquivos
                
        processo = p.consultar_nfse(nfse=nfse, data_inicial=data_inicial, data_final=data_final)
        
        return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
                'reason': processo.resposta.reason, 'msg_retorno' : processo.msg_retorno}
                
    def cancelar_nfse(self, codigo_cancelamento, numero_nfse, cnpj, im, cert, key, ambiente=2, versao=u'1.0', modelo=u'bhiss', codigo_ibge=None, salvar_arquivos=True):
        """
        Esse serviço permite o cancelamento direto de uma NFS-e sem substituição da mesma por outra. 

        @param codigo_cancelamento: Código de cancelamento,
        @param numero_nfse: numero da NFS-e a ser cancelada,
        @param cnpj: string com o cnpj do emitente,
        @param im: string com Inscrição municipal do emitente,
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfse,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param modelo: modelo de NFS-e utilizada do municipio,
        @param codigo_ibge: codigo IBGE do municipio, opcional,
        @return: Dicionário com o envio, resposta, reason e uma msg_retorno caso haja rejeição.
        """
        
        if modelo==u'bhiss':
            p = ProcessadorNFSeBH()
            
        p.ambiente = ambiente
        p.versao   = versao
        p.certificado.cert_str = cert
        p.certificado.key_str  = key
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.cancelar_nfse(codigo_cancelamento=codigo_cancelamento, numero_nfse=numero_nfse, cnpj=cnpj, im=im, codigo_ibge=codigo_ibge)
        
        return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
                'reason': processo.resposta.reason, 'msg_retorno' : processo.msg_retorno}
        
    def processar_lote_rps(self, lista_rps, cert, key, ambiente=2, versao=u'1.0', modelo=u'bhiss', salvar_arquivos=True, numero_lote=None, cnpj=None, im=None):
        """
        Esse serviço compreende a recepção do Lote de RPS, a resposta com o
        número do protocolo gerado para esta transação e o processamento do lote.
        Quando efetuada a recepção, o Lote entrará na fila para processamento
        posterior onde serão feitas as validações necessárias e geração das NFS-e. 

        @param lista_rps: lista as RPS's para processar,
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfse,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param modelo: modelo de NFS-e utilizada do municipio,
        @param salvar_arquivos: salvar os arquivos caso não ocorram erros,
        @param numero_lote: caso o usuário queira definir o numero do lote enviado, se None o sistema gera um numero,
        @param cnpj: string com o cnpj do emitente, caso None o cnpj será o do primeiro RPS na lista,
        @param im: string com Inscrição municipal do emitente, cano None será o do primeiro RPS da lista,
        @return: Dicionário com o envio, resposta, reason e uma msg_retorno caso haja rejeição.
        """
        
        if modelo==u'bhiss':
            p = ProcessadorNFSeBH()
        
        p.ambiente = ambiente
        p.versao=versao
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        
        for processo in p.processar_lote_rps(lista_rps=lista_rps, numero_lote=numero_lote, cnpj=cnpj, im=im):
            processo.envio.xml
            processo.resposta.xml
            processo.resposta.reason
                
        return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
                'reason': processo.resposta.reason, 'msg_retorno' : processo.msg_retorno}