# -*- coding: utf-8 -*-

from .nota import NotaFiscal

from pysignfe.nfe import ProcessadorNFe, DANFE
from pysignfe.nfe.manual_401 import *
from pysignfe.nfe.manual_500 import *

from os.path import abspath, dirname
from OpenSSL import crypto
import io
from xml.dom import minidom

from pysignfe.nfe.danfe.danferetrato import *
from pysignfe.xml_sped.certificado import Certificado
from pysignfe.nfe.webservices_2 import ESTADO_WS, SVAN, SVRS, UFRS, NFE_AMBIENTE_PRODUCAO
from pysignfe.nfe.webservices_3 import ESTADO_WS as ESTADO_WS3
from pysignfe.nfe.webservices_3 import SVAN as SVAN3
from pysignfe.nfe.webservices_3 import SVRS as SVRS3
from pysignfe.nfe.webservices_3 import UFRS as UFRS3
from pysignfe.nfe.webservices_flags import WS_NFE_CONSULTA_CADASTRO, WS_NFE_EVENTO

FILE_DIR = abspath(dirname(__file__))

class nf_e(NotaFiscal):
    """
    Especialização da biblioteca pysped.
    @author: Marcilene Ribeiro
    Modificada por thiagopena
    """
    
    def consultar_servidor(self, cert, key, versao=u'2.00', ambiente=2, estado=u'MG',
                           tipo_contingencia=False, salvar_arquivos=True):
        """
        Este método verifica se o servidor está em operação
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfe,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param estado: estado em que realizará a consulta do servidor,
        @param tipo_contingencia : habilita a contigência.
        @param salvar_arquivos: salvar ou nao os arquivos XML gerados.
        @return: Dicionário com o status,envio,resposta e reason.
        """

        p = ProcessadorNFe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao = versao
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.tipo_contingencia = tipo_contingencia
        p.caminho = u''
        processo = p.consultar_servico()
        status = processo.resposta.cStat.valor
        processo.envio.xml
        processo.resposta.xml
        processo.resposta.reason

        return{'status': status, 'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
               'reason': processo.resposta.reason}


    def processar_nfe(self, xml_nfe, cert, key, versao=u'2.00', ambiente=2, estado=u'MG',
                      tipo_contingencia=False, salvar_arquivos=True, n_consultas_recibo=2):
        """
        Este método realiza o processamento de validação, assinatura e transmissão da nfe.
        @param xml_nfe:xml da nfe (string)
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfe,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param estado: estado em que realizará o processamento,
        @param tipo_contingencia: habilita a contigência .
        @return: Dicionário com a chave_nfe, protocolo, envio, numero_lote, resposta, status_resposta,status_motivo e reason.
        """
        p = ProcessadorNFe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao = versao
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.tipo_contingencia = tipo_contingencia
        p.caminho = u''
        p.numero_tentativas_consulta_recibo = n_consultas_recibo
        
        if versao == '3.10':
            n = NFe_310()
        else:
            n = NFe_200()
        n.infNFe.xml = xml_nfe
        
        for processo in p.processar_notas([n]):
            processo.envio.xml
            processo.resposta.xml
            processo.resposta.reason
            
        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'chave_nfe': n.chave,
                'status_resposta_lote': processo.resposta.cStat.valor,
                'status_motivo_lote': processo.resposta.xMotivo.valor,
                'reason': processo.resposta.reason
        }
        try:
            if processo.resposta.infProt.nProt.valor == '':
                vals['protocolo'] = processo.resposta.protNFe.infProt.nProt.valor
        except:
            pass

        for nome, proc in p.processos.items():
            vals['status_resposta_'+str(nome)]  = proc.protNFe.infProt.cStat.valor
            vals['numero_protocolo_'+str(nome)] = proc.protNFe.infProt.nProt.valor
            vals['status_motivo_'+str(nome)]    = proc.protNFe.infProt.xMotivo.valor
            '''
            for arquivo in proc[1]:
                if arquivo[0] == 'numero_lote':
                    vals['numero_lote'] = arquivo[1]
                if arquivo[0] == 'numero_protocolo':
                    vals['protocolo'] = arquivo[1]
                    vals['resposta'] = proc[1][1][1]
                if arquivo[0] == 'status_resp':
                    vals['status_resposta'] = arquivo[1][0]
                    vals['status_motivo'] = arquivo[1][1]
            '''
        return vals


    def processar_lote(self, lista_xml_nfe, cert, key, versao=u'2.00', ambiente=2, estado=u'MG',
                       tipo_contingencia=False, salvar_arquivos=True, n_consultas_recibo=2):
        """
        Este método realiza o processamento de validação, assinatura e transmissão da nfe.
        @param lista_xml_nfe:lista nfe(strings)
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfe,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param estado: estado em que realizará o processamento,
        @param tipo_contingencia: habilita a contigência .
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao=versao
        p.tipo_contingencia = tipo_contingencia
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.caminho = u''
        p.numero_tentativas_consulta_recibo = n_consultas_recibo
        '''
        if versao == '3.10':
            n = NFe_310()
        else:
            n = NFe_200()
        '''
        lista = []
        if lista_xml_nfe:
            for x in lista_xml_nfe:
                if versao == '3.10':
                    n = NFe_310()
                else:
                    n = NFe_200()
                n.infNFe.xml = x
                lista.append(n)
        
        for processo in p.processar_notas(lista):
            processo.envio.xml
            processo.resposta.xml
            processo.resposta.reason
            
        vals = {
            'envio': processo.envio.xml, 
            'resposta': processo.resposta.xml,
            'status_resposta_lote': processo.resposta.cStat.valor,
            'status_motivo_lote': processo.resposta.xMotivo.valor,
            'reason': processo.resposta.reason
        }
            
        for nome, proc in p.processos.items():
            vals['status_resposta_'+str(nome)]  = proc.protNFe.infProt.cStat.valor
            vals['numero_protocolo_'+str(nome)] = proc.protNFe.infProt.nProt.valor
            vals['status_motivo_'+str(nome)]    = proc.protNFe.infProt.xMotivo.valor

        return vals
                
    def consultar_recibo(self, numero_recibo, cert, key, versao=u'2.00', ambiente=2, estado=u'MG',
                       salvar_arquivos=True, n_tentativas=2):
                       
        """
        Este método retorna o resultado do processamento do lote enviado.
        @param numero_recibo: numero do recibo do lote enviado.
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfe,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param estado: estado em que realizará o processamento,
        @param n_tentativas: numero de tentativas de envio.
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao=versao
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.caminho = u''
        
        tentativa = 0
        processo = p.consultar_recibo(ambiente=ambiente, numero_recibo=numero_recibo)
        
        while processo.resposta.cStat.valor == '105' and tentativa < n_tentativas:
            processo = p.consultar_recibo(ambiente=ambiente, numero_recibo=numero_recibo)
            tentativa += 1
            
        return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
                'reason': processo.resposta.reason}


    def cancelar_nota(self, cnpj, chave, protocolo, justificativa, cert, key, versao=u'2.00',
                      ambiente=2, estado=u'MG', tipo_contingencia=False, salvar_arquivos=True):
        """
        Realiza o cancelamento da nfe.
        @param chave:chave da nfe
        @param protocolo: protocolo do processamento da nfe
        @param justificativa: justificativa do cancelamento 
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfe,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param estado: estado em que realizará o processamento,
        @param tipo_contingencia: habilita a contigência .
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.tipo_contingencia = tipo_contingencia
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.cancelar_nota(cnpj, chave_nfe=chave, numero_protocolo=protocolo,
                                   justificativa=justificativa)
        processo.resposta.reason
        vals = {'envio': processo.envio.xml,
                'resposta': processo.processo_cancelamento_nfe.xml,
                'status_resposta': processo.resposta.infEvento.cStat.valor,
                'status_motivo': processo.resposta.infEvento.xMotivo.valor,
                'reason': processo.resposta.reason}
        if processo.resposta.infEvento.cStat.valor == '135':
            vals['protocolo'] = processo.resposta.infEvento.nProt.valor

        return vals


    def inutilizar_nota(self, cnpj, serie, numero, justificativa, cert, key, versao=u'2.00',
                        ambiente=2, estado=u'MG', tipo_contingencia=False, salvar_arquivos=True):
        """
        Realiza a inutilização do número de uma nota fiscal
        @param cnpj:cnpj do emitente
        @param serie: serie da nfe
        @param numero: número da nota que deseja inutilizar
        @param justificativa: justificativa da inutilização 
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfe,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param estado: estado em que realizará o processamento,
        @param tipo_contingencia: habilita a contigência .
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.tipo_contingencia = tipo_contingencia
        p.caminho = u''
        
        processo = p.inutilizar_nota(cnpj=cnpj, serie=serie, numero_inicial=numero,
                                     justificativa=justificativa)
        processo.envio.xml
        processo.resposta.xml
        processo.resposta.reason
        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'status_resposta': processo.resposta.infInut.cStat.valor,
                'status_motivo': processo.resposta.infInut.xMotivo.valor,
                'reason': processo.resposta.reason}
        return vals

    def inutilizar_faixa_numeracao(self, cnpj, serie, numero_inicial, numero_final, justificativa,
                                   cert, key, versao=u'2.00', ambiente=2, estado=u'MG',
                                   tipo_contingencia=False, salvar_arquivos=True):
        """
        Realiza a inutilização de faixa de numeração de nota fiscal
        @param cnpj:cnpj do emitente
        @param serie: série da nfe
        @param numero_inicial: faixa inicial da nota que deseja inutilizar
        @param numero_final: faixa final da nota que deseja inutilizar
        @param justificativa: justificativa da inutilização 
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfe,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param estado: estado em que realizará o processamento,
        @param tipo_contingencia: habilita a contigência .
        @return: Dicionário com o envio,resposta e reason.
        """

        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.tipo_contingencia = tipo_contingencia
        p.caminho = u''
        
        processo = p.inutilizar_nota(cnpj=cnpj, serie=serie, numero_inicial=numero_inicial,
                                     numero_final=numero_final, justificativa=justificativa)
        processo.envio.xml
        processo.resposta.xml
        processo.resposta.reason
        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'status_resposta': processo.resposta.infInut.cStat.valor,
                'status_motivo': processo.resposta.infInut.xMotivo.valor,
                'reason': processo.resposta.reason}
        if processo.resposta.infInut.cStat.valor == '102':
            vals['protocolo'] = processo.resposta.infInut.nProt.valor

        return vals

    def gerar_danfe(self, nfe, retcan_nfe=None, site_emitente=u'', logo=u'',
                    nome_sistema=u'', leiaute_logo_vertical=False, versao='2.00'):
        """
        Geração do DANFE
        @param nfe:string do xml da NF-e
        @param site_emitente: Endereço do site do emitente
        @param logo:O caminho para a imagem ou  Instância da imagem.
        @param leiaute_logo_vertical: possibilita que a logomarca tenha a orientação vertical
        @return: String
        """
        d = DANFE()
        if versao == '3.10':
            nota = NFe_310()
            protNFe = ProtNFe_310()
            proc = ProcNFe_310()
        else:
            nota = NFe_200()
            protNFe = ProtNFe_200()
            proc = ProcNFe_200()
        nota.xml = nfe
        resp = minidom.parseString(nfe.encode('utf-8'))
        resp = resp.getElementsByTagName("protNFe")[0]
        resposta = resp.toxml()
        protNFe.xml = resposta
        proc.protNFe = protNFe

        d.NFe = nota
        d.protNFe = protNFe
        d.versao = versao
        d.salvar_arquivo = False
        d.obs_impressao = u'DANFE gerado em %(now:%d/%m/%Y, %H:%M:%S)s'
        d.nome_sistema = nome_sistema
        d.site = site_emitente
        d.logo = logo
        d.leiaute_logo_vertical = leiaute_logo_vertical
        d.gerar_danfe()
        danfe_pdf = io.BytesIO()
        d.danfe.generate_by(PDFGenerator, filename=danfe_pdf)
        d.danfe = danfe_pdf.getvalue()
        danfe_pdf.close()

        return d.danfe

    def validar_chave_nfe(self, chave, uf, data_emissao, cnpj, modelo, serie, numero_nf):
        """
        Verifica consistência da chave de NF-e informada
        @param chave:Chave da NF-e
        @param uf:
        @param data_emissao:
        @param cnpj
        @param modelo
        @param serie
        @param numero_nf
        @return: Dicionário
        """
        msg = ''
        res = {'valida': True, msg: ''}
        if len(chave) == 44:
            if chave[:2] != uf:
                msg += '* Estado informado inválido.\n'
            data_emissao = data_emissao[2:4] + data_emissao[5:7]
            if chave[2:6] != data_emissao:
                msg += '* Data de emissão inválida. \n'
            cnpj = cnpj.replace('.', '').replace('-', '').replace('/', '')
            if chave[6:20] != cnpj:
                msg += '* CNPJ do emitente inválido. \n'
            if chave[20:22] != modelo:
                msg += '* Modelo da Nota Fiscal inválido.\n'
            if chave[22:25] != ('%003d' % int(serie)):
                msg += '* Série da Nota Fiscal inválida.\n'
            if chave[25:34] != '%009d' % int(numero_nf):
                msg += '* Número da Nota Fiscal inválido. \n'
            nf = NFe_200()
            digito_verificador = nf._calcula_dv(chave[:43])
            if digito_verificador != int(chave[43:]):
                msg += '* Dígito verificador inválido. \n'
            if msg:
                res['msg'] = 'Chave de acesso inválida: \n' + msg
                res['valida'] = False
        else:
            res['msg'] = 'Chave inválida.'
            res['valida'] = False
        return res

    def consultar_nfe(self, chave, cert, key, versao=u'2.00', ambiente=2, estado=u'MG',
                      tipo_contingencia=False, salvar_arquivos=True):
        """
            @param chave:chave da nfe
            @param cert: string do certificado digital A1,
            @param key: chave privada do certificado digital,
            @param versao: versão da nfe,
            @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
            @param estado: estado em que realizará o processamento,
            @param tipo_contingencia: habilita a contigência.
            @param salvar_arquivos: salvar ou nao os arquivos XML gerados.
            @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.tipo_contingencia=tipo_contingencia
        p.salvar_arquivos = salvar_arquivos
        processo = p.consultar_nota(chave_nfe=chave)
        
        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'status_resposta': processo.resposta.cStat.valor,
                'status_motivo': processo.resposta.xMotivo.valor,
                'reason': processo.resposta.reason,
        }
        
        return vals


    def consultar_cadastro(self, uf, cert, key, cpf_cnpj=None, inscricao_estadual=None, versao=u'2.00',
                           ambiente=2, estado=u'MG', tipo_contingencia=False, salvar_arquivos=True):
        """
            @param chave:chave da nfe
            @param cert: string do certificado digital A1,
            @param key: chave privada do certificado digital,
            @param versao: versão da nfe,
            @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
            @param estado: estado em que realizará o processamento,
            @param tipo_contingencia: habilita a contigência .
            @return: Dicionário com o envio,resposta e reason.
             """
        if cpf_cnpj is None and inscricao_estadual is None:
            raise ValueError("Deve-se informar o CNPJ ou CPF ou IE.")
        
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        if uf in ('AC', 'AL', 'AP', 'DF', 'ES', 'PB', 'RJ', 'RN', 'RO', 'RR', 'SC',
                  'SE', 'TO'):
            #SVRS[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'svp-ws.sefazvirtual.rs.gov.br'
            if versao == '3.10':
                SVRS3[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'cad.svrs.rs.gov.br'
            else:
                SVRS[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'cad.svrs.rs.gov.br'
        if uf == 'RS':
            #UFRS[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'sef.sefaz.rs.gov.br'
            if versao == '3.10':
                UFRS3[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'cad.sefazrs.rs.gov.br'
            else:
                UFRS[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'cad.sefazrs.rs.gov.br'
        if uf == 'MA':
            if versao == '3.10':
                SVAN3[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'sistemas.sefaz.ma.gov.br'
                SVAN3[NFE_AMBIENTE_PRODUCAO][WS_NFE_CONSULTA_CADASTRO] = u'wscadastro/CadConsultaCadastro2'
            else:
                SVAN[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'sistemas.sefaz.ma.gov.br'
                SVAN[NFE_AMBIENTE_PRODUCAO][WS_NFE_CONSULTA_CADASTRO] = u'wscadastro/CadConsultaCadastro2'
        
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.tipo_contingencia = tipo_contingencia
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.consultar_cadastro_contribuinte(cpf_cnpj=cpf_cnpj,
                                                     inscricao_estadual=inscricao_estadual, uf=uf,
                                                     ambiente=ambiente)
        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'status_resposta': processo.resposta.infCons.cStat.valor,
                'status_motivo': processo.resposta.infCons.xMotivo.valor,
                'reason': processo.resposta.reason}
        return vals

    #MANIFESTAÇÃO DO DESTINATÁRIO

    def efetuar_manifesto(self, cnpj, tipo_evento, chave,  cert, key, ambiente_nacional=True, versao=u'2.00', ambiente=2,
                          estado=u'MG', tipo_contingencia=False, justificativa=None, salvar_arquivos=True):
        """
            Realiza o manifesto do destinatário
            @param chave:chave da nfe
            @param cert: string do certificado digital A1,
            @param key: chave privada do certificado digital,
            @param versao: versão da nfe,
            @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
            @param estado: estado em que realizará o processamento,
            @param tipo_contingencia: habilita a contigência .
            @return: Dicionário com o envio,resposta e reason.
            """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado

        if ambiente_nacional:
            if versao == '3.10':
                ESTADO_WS3[estado] = SVAN3
            else:
                ESTADO_WS[estado] = SVAN
            
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.tipo_contingencia = tipo_contingencia
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.consultar_manifesto_destinatario(cnpj, tipo_evento=tipo_evento, chave_nfe=chave, justificativa=justificativa, ambiente_nacional=ambiente_nacional)

        vals = {'envio': processo.envio.xml,
                #'resposta': processo.processo_evento_nfe.xml,
                'status_resposta': processo.resposta.infEvento.cStat.valor,
                'status_motivo': processo.resposta.infEvento.xMotivo.valor,
                'reason': processo.resposta.reason}
        
        if processo.resposta.infEvento.cStat.valor == '135':
            vals['protocolo'] = processo.resposta.infEvento.nProt.valor
        if processo.resposta.cStat.valor == u'128':
            vals['resposta'] = processo.processo_evento_nfe.xml
        else:
            vals['resposta'] = processo.resposta.xml
            vals['status_resposta'] = processo.resposta.cStat.valor
            vals['status_motivo'] = processo.resposta.xMotivo.valor

        return vals


    def consultar_nfe_destinatario(self, cnpj, indnfe, indemi, cert, key, nsu='0', versao=u'2.00',
                                   ambiente=2, estado=u'MG', tipo_contingencia=False, salvar_arquivos=True):
        """
            Realiza  a consulta do manifesto do destinatário
            @param cert: string do certificado digital A1,
            @param key: chave privada do certificado digital,
            @param versao: versão da nfe,
            @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
            @param estado: estado em que realizará o processamento,
            @param tipo_contingencia: habilita a contigência .
            @return: Dicionário com o envio,resposta e reason.
            """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        #Provisoriamente apontado para um estado que usa o webservice de ambiente nacional, pois em MG ainda
        # não existe suporte ao Manifesto do Destinatário
        ESTADO_WS[estado] = SVAN
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.tipo_contingencia = tipo_contingencia
        p.salvar_arquivos = salvar_arquivos
        processo = p.consultar_notas_destinatario(cnpj=cnpj, indnfe=indnfe, indemi=indemi, nsu=nsu)
        resp = processo.resposta
        lista_notas = []
        if resp.cStat.valor == '138':#Documento localizado para o destinatário
            for resp in resp.ret:
                if resp.resNFe.xml:
                    dict_resnfe = {
                        'NSU': resp.resNFe.NSU.valor,
                        'chNFe': resp.resNFe.chNFe.valor,
                        'CNPJ': resp.resNFe.CNPJ.valor,
                        'CPF': resp.resNFe.CPF.valor,
                        'xNome': resp.resNFe.xNome.valor,
                        'IE': resp.resNFe.IE.valor,
                        'dEmi': resp.resNFe.dEmi.valor,
                        'tpNF': resp.resNFe.tpNF.valor,
                        'vNF': resp.resNFe.vNF.valor,
                        'digVal': resp.resNFe.digVal.valor,
                        'dhRecbto': resp.resNFe.dhRecbto.valor,
                        'cSitNFe': resp.resNFe.cSitNFe.valor,
                        'cSitConf': resp.resNFe.cSitConf.valor
                    }
                    lista_notas.append({'resNFe': dict_resnfe})
                if resp.resCanc.xml:
                    dict_rescanc = {
                        'NSU': resp.resCanc.NSU.valor,
                        'chNFe': resp.resCanc.chNFe.valor,
                        'CNPJ': resp.resCanc.CNPJ.valor,
                        'CPF': resp.resCanc.CPF.valor,
                        'xNome': resp.resCanc.xNome.valor,
                        'IE': resp.resCanc.IE.valor,
                        'dEmi': resp.resCanc.dEmi.valor,
                        'tpNF': resp.resCanc.tpNF.valor,
                        'vNF': resp.resCanc.vNF.valor,
                        'digVal': resp.resCanc.digVal.valor,
                        'dhRecbto': resp.resCanc.dhRecbto.valor,
                        'cSitNFe': resp.resCanc.cSitNFe.valor,
                        'cSitConf': resp.resCanc.cSitConf.valor
                    }
                    lista_notas.append({'resCanc': dict_rescanc})
                if resp.resCCe.xml:
                    dict_rescce = {
                        'NSU': resp.resCCe.NSU.valor,
                        'chNFe': resp.resCCe.chNFe.valor,
                        'dhEvento': resp.resCCe.dhEvento.valor,
                        'tpEvento': resp.resCCe.tpEvento.valor,
                        'nSeqEvento': resp.resCCe.nSeqEvento.valor,
                        'descEvento': resp.resCCe.descEvento.valor,
                        'xCorrecao': resp.resCCe.xCorrecao.valor,
                        'tpNF': resp.resCCe.tpNF.valor,
                        'dhRecbto': resp.resCCe.dhRecbto.valor
                    }
                    lista_notas.append({'resCCe': dict_rescce})


        vals = {'envio':processo.envio.xml,
                'resposta': processo.resposta.xml,
                'status_resposta': processo.resposta.cStat.valor,
                'status_motivo': processo.resposta.xMotivo.valor,
                'lista_notas': lista_notas,
                'reason': processo.resposta.reason}

        return vals

    def download_notas(self, cnpj, lista_chaves,  cert, key, ambiente_nacional=True, versao=u'2.00', ambiente=2, estado=u'MG',
                     tipo_contingencia=False, salvar_arquivos=True):
        """
            Realiza download de NFe para uma determinada chave de acesso, para NF-e confirmada pelo destinatario.
            @param lista_chaves: lista de até 10 chaves
            @param cert: string do certificado digital A1,
            @param key: chave privada do certificado digital,
            @param versao: versão da nfe,
            @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
            @param estado: estado em que realizará o processamento,
            @param tipo_contingencia: habilita a contigência .
            @return: Dicionário com o envio,resposta e reason.
            """
        if len(lista_chaves)>10:
            raise ValueError(u'Maximo de 10 Chaves de Acesso por lote.')
            
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        if ambiente_nacional:
            if versao == '3.10':
                ESTADO_WS3[estado] = SVAN3
            else:
                ESTADO_WS[estado] = SVAN
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.tipo_contingencia = tipo_contingencia
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.download_nfes(cnpj, ambiente, lista_chaves=lista_chaves)

        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'proc_xml':processo.resposta.original,
                'status_resposta': processo.resposta.retNFe.cStat.valor,
                'status_motivo': processo.resposta.retNFe.xMotivo.valor,
                'reason': processo.resposta.reason}


        return vals

    #CARTA DE CORRECAO
    def emitir_carta_correcao(self, chave, cnpj, texto_correcao, cert, key, sequencia=None,
                              versao=u'2.00', ambiente=2, estado=u'MG', tipo_contingencia=False,
                              salvar_arquivos=True):
        """
            @param chave:chave da nfe
            @param cert: string do certificado digital A1,
            @param key: chave privada do certificado digital,
            @param versao: versão da nfe,
            @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
            @param estado: estado em que realizará o processamento,
            @param tipo_contingencia: habilita a contigência .
            @return: Dicionário com o envio,resposta e reason.
            """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.tipo_contingencia = tipo_contingencia
                
        processo = p.corrigir_nota(chave_nfe=chave, cnpj=cnpj, texto_correcao=texto_correcao,
                                   ambiente=ambiente,sequencia=sequencia)        
        processo.resposta.reason
        vals = {'envio': processo.envio.xml,
                'resposta': processo.processo_correcao_nfe.xml,
                'status_resposta': processo.resposta.infEvento.cStat.valor,
                'status_motivo': processo.resposta.infEvento.xMotivo.valor,
                'reason': processo.resposta.reason}
        if processo.resposta.infEvento.cStat.valor == '135':
            vals['protocolo'] = processo.resposta.infEvento.nProt.valor

        return vals







