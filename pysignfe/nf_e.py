# -*- coding: utf-8 -*-

from .nota import NotaFiscal
from pysignfe.corr_unicode import *

from pysignfe.nfe import ProcessadorNFe, DANFE
from pysignfe.nfe.manual_401 import *
#from pysignfe.nfe.manual_500 import *
from pysignfe.nfe.manual_600 import *

from os.path import abspath, dirname
from OpenSSL import crypto
import io
from xml.dom import minidom
from datetime import datetime

from pysignfe.nfe.danfe.danferetrato import *
from pysignfe.nfe.webservices_2 import ESTADO_WS, SVAN, SVRS, UFRS, NFE_AMBIENTE_PRODUCAO
from pysignfe.nfe.webservices_3 import ESTADO_WS as ESTADO_WS3
from pysignfe.nfe.webservices_3 import ESTADO_SVC_CONTINGENCIA
from pysignfe.nfe.webservices_3 import SVAN as SVAN3
from pysignfe.nfe.webservices_3 import AN
from pysignfe.nfe.webservices_3 import SVRS as SVRS3
from pysignfe.nfe.webservices_3 import UFRS as UFRS3
from pysignfe.nfe.webservices_flags import WS_NFE_CONSULTA_CADASTRO, WS_NFE_EVENTO, UF_CODIGO

FILE_DIR = abspath(dirname(__file__))


class nf_e(NotaFiscal):

    def consultar_servidor(self, cert, key, versao=u'3.10', ambiente=2, estado=u'MG',
                           contingencia=False, salvar_arquivos=True, caminho=u''):
        """
        Este método verifica se o servidor está em operação
        @param cert: string do certificado digital A1,
        @param key: chave privada do certificado digital,
        @param versao: versão da nfe,
        @param ambiente: ambiente da consulta, pode ser 1 para o ambiente de produção e 2 para homologação,
        @param estado: estado em que realizará a consulta do servidor,
        @param contingencia : habilita a contigência.
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
        p.contingencia = contingencia
        p.caminho = caminho
        
        processo = p.consultar_servico()
        processo.envio.xml
        processo.resposta.xml
        processo.resposta.reason

        return processo
        
    def gerar_xml(self, xml_nfe, cert, key, versao=u'3.10', consumidor=False, ambiente=2, estado=u'MG', salvar_arquivos=True, numero_lote=None, caminho=u''):
        p = ProcessadorNFe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao = versao
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.caminho = caminho
        
        if numero_lote is None:
            numero_lote = datetime.now().strftime('%Y%m%d%H%M%S')
        
        if versao == '3.10':
            n = NFe_310()
        else:
            n = NFe_200()
        n.infNFe.xml = xml_nfe
                
        n.auto_preencher_campos(ambiente=ambiente, estado=estado)
        
        if consumidor:
            n.preencher_campos_nfce()
        else:
            n.preencher_campos_nfe()
            
        processo =  p.gerar_xml([n], numero_lote=numero_lote)

        return processo
        
    def processar_nota(self, xml_nfe, cert, key, versao=u'3.10', consumidor=False, ambiente=2, estado=u'MG',
                      contingencia=False, salvar_arquivos=True, n_consultas_recibo=2, consultar_servico=True, numero_lote=None, caminho=u''):
        """
        Este método realiza o processamento de validação, assinatura e transmissão da nfe.
        @param xml_nfe: xml da nfe (string)
        @param consultar_servico: consulta o status do webservice antes de enviar
        @param consumidor: True caso NFC-e
        @param n_consultas_recibo: numero de tentativas de consultar o recibo
        @return: Dicionário com a chave_nfe, protocolo, envio, numero_lote, resposta, status_resposta,status_motivo e reason.
        """
        p = ProcessadorNFe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao = versao
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.contingencia = contingencia
        p.caminho = caminho
        p.numero_tentativas_consulta_recibo = n_consultas_recibo
        p.verificar_status_servico = consultar_servico
        
        if numero_lote is None:
            numero_lote = datetime.now().strftime('%Y%m%d%H%M%S')
        
        if versao == '3.10':
            n = NFe_310()
        else:
            n = NFe_200()
        n.infNFe.xml = xml_nfe
                
        n.auto_preencher_campos(ambiente=ambiente, estado=estado, contingencia=contingencia, consumidor=consumidor)
        
        if consumidor:
            n.preencher_campos_nfce()
        else:
            n.preencher_campos_nfe()
        
        for processo in p.processar_notas([n], numero_lote=numero_lote):
            processo.envio.xml
            processo.resposta.xml
            processo.resposta.reason
        
        processos = {}
        processos['numero_lote'] = numero_lote
        processos['lote'] = processo
        processos['notas'] = []
        
        for nome, proc in p.processos.items():
            processos['notas'].append(proc)
        
        return processos
        
    def processar_lote(self, lista_xml_nfe, cert, key, versao=u'3.10', consumidor=False, ambiente=2, estado=u'MG',
                       contingencia=False, salvar_arquivos=True, n_consultas_recibo=2, consultar_servico=True, numero_lote=None, caminho=u''):
        """
        Este método realiza o processamento de validação, assinatura e transmissão da nfe.
        @param lista_xml_nfe:lista nfe(strings ou objetos NFe)
        @param consumidor: True caso NFC-e
        @param consultar_servico: consulta o status do webservice antes de enviar
        @param n_consultas_recibo: numero de tentativas de consultar o recibo
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao=versao
        p.contingencia = contingencia
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.caminho = caminho
        p.numero_tentativas_consulta_recibo = n_consultas_recibo
        p.verificar_status_servico = consultar_servico
        
        if numero_lote is None:
            numero_lote = datetime.now().strftime('%Y%m%d%H%M%S')
        
        if isinstance(lista_xml_nfe[0], basestring) and lista_xml_nfe:
            lista_nfe = []
            for x in lista_xml_nfe:
                if versao == '3.10':
                    n = NFe_310()
                else:
                    n = NFe_200()
                n.infNFe.xml = x
                
                n.auto_preencher_campos(ambiente=ambiente, estado=estado, contingencia=contingencia, consumidor=consumidor)
                
                if consumidor:
                    n.preencher_campos_nfce()
                else:
                    n.preencher_campos_nfe()
                    
                lista_nfe.append(n)
        else:
            lista_nfe = lista_xml_nfe
        
        for processo in p.processar_notas(lista_nfe, numero_lote=numero_lote):
            processo.envio.xml
            processo.resposta.xml
            processo.resposta.reason
        
        processos = {}
        processos['numero_lote'] = numero_lote
        processos['lote'] = processo
        processos['notas'] = []
        
        for nome, proc in p.processos.items():
            processos['notas'].append(proc)

        return processos
        
    def consultar_recibo(self, numero_recibo, cert, key, versao=u'2.00', ambiente=2, estado=u'MG',
                       salvar_arquivos=True, n_tentativas=2, caminho=u''):
                       
        """
        Este método retorna o resultado do processamento do lote enviado.
        @param numero_recibo: numero do recibo do lote enviado.
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
        p.caminho = caminho
        
        tentativa = 0
        processo = p.consultar_recibo(ambiente=ambiente, numero_recibo=numero_recibo)
        
        while processo.resposta.cStat.valor == '105' and tentativa < n_tentativas:
            processo = p.consultar_recibo(ambiente=ambiente, numero_recibo=numero_recibo)
            tentativa += 1
            
        #return {'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
        #        'reason': processo.resposta.reason}
        
        return processo


    def cancelar_nota(self, chave, protocolo, justificativa, cert, key, data=None, versao=u'3.10',
                      ambiente=2, estado=u'MG', contingencia=False, salvar_arquivos=True, numero_lote=None, caminho=u''):
        """
        Realiza o cancelamento da nfe.
        @param chave:chave da nfe
        @param protocolo: protocolo do processamento da nfe
        @param justificativa: justificativa do cancelamento 
        @param numero_lote: usuario pode definir o numero do lote, caso contrario sera a ANO+MES+DIA+HORA+MIN+SEG
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.contingencia = contingencia
        p.caminho = caminho
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.cancelar_nota(chave_nfe=chave, numero_protocolo=protocolo,
                                   justificativa=justificativa, data=data, numero_lote=numero_lote)
        processo.resposta.reason
        
        return processo
                
    def emitir_carta_correcao(self, chave, texto_correcao, cert, key, sequencia=None, data=None, numero_lote=None,
                              versao=u'3.10', ambiente=2, estado=u'MG', contingencia=False,
                              salvar_arquivos=True, caminho=u''):
        """
        @param chave:chave da nfe
        @param texto_correcao: correção a ser considerada, texto livre
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.caminho = caminho
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.contingencia = contingencia
                
        processo = p.corrigir_nota(chave_nfe=chave, texto_correcao=texto_correcao,
                                   ambiente=ambiente,sequencia=sequencia, data=data, numero_lote=numero_lote)
        processo.resposta.reason

        return processo
        
    def efetuar_manifesto(self, cnpj, tipo_manifesto, chave,  cert, key, ambiente_nacional=True, versao=u'3.10', ambiente=2,
                          estado=u'MG', contingencia=False, justificativa=None, salvar_arquivos=True, caminho=u''):
        """
        Realiza o manifesto do destinatário
        @param tipo_manifesto: Confirmação da Operação, Desconhecimento da Operação, Operação Não Realizada ou Ciência da Emissão
        @param ambiente_nacional: usa o webservice do ambiente nacional (Recomendado manter True)
        @param justificativa: justificativa porque a operação não foi realizada, este campo deve ser informado somente no evento de Operação não Realizada.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.caminho = caminho

        if ambiente_nacional:
            if versao == '3.10':
                ESTADO_WS3[estado] = SVAN3
            else:
                ESTADO_WS[estado] = SVAN
            
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.contingencia = contingencia
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.efetuar_manifesto_destinatario(cnpj=cnpj, tipo_manifesto=tipo_manifesto, chave_nfe=chave, justificativa=justificativa, ambiente_nacional=ambiente_nacional)

        return processo
        
    def enviar_lote_evento(self, lista_eventos, tipo, cert, key, versao=u'3.10',
                      ambiente=2, estado=u'MG', contingencia=False, numero_lote=None, salvar_arquivos=True,
                      ambiente_nacional=False, caminho=u''):
        """
        Envia um lote de eventos (cancelamento, correcao, manifestacao ou epec)
        @param lista_eventos: lista com eventos (todos os eventos devem ser do mesmo tipo)
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.caminho = caminho
        p.ambiente = ambiente
        p.contingencia = contingencia
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        
        for ev in lista_eventos:
            ev.infEvento.tpAmb.valor = ambiente
            if ambiente_nacional:
                ev.infEvento.cOrgao.valor = UF_CODIGO['NACIONAL']
            else:
                ev.infEvento.cOrgao.valor = UF_CODIGO[estado]
                
            ev.infEvento.CNPJ.valor = ev.infEvento.CNPJ.valor or ev.infEvento.chNFe.valor[6:20] # Extrai o CNPJ da própria chave da NF-e
            ev.infEvento.dhEvento.valor = ev.infEvento.dhEvento.valor or datetime.now()
            
        processo = p.enviar_lote_evento(tipo_evento=tipo, lista_eventos=lista_eventos, numero_lote=numero_lote)
        
        return processo    

    def inutilizar_nota(self, cnpj, serie, numero, justificativa, cert, key, nfce=False, versao=u'3.10',
                        ambiente=2, estado=u'MG', contingencia=False, salvar_arquivos=True, caminho=u''):
        """
        Realiza a inutilização do número de uma nota fiscal
        @param cnpj:cnpj do emitente
        @param serie: serie da nfe
        @param nfce: True se inutilizando numeração de NFC-e
        @param numero: número da nota que deseja inutilizar
        @param justificativa: justificativa da inutilização 
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.contingencia = contingencia
        p.caminho = caminho
        p.nfce = nfce
        
        processo = p.inutilizar_nota(cnpj=cnpj, serie=serie, numero_inicial=numero,
                                     justificativa=justificativa)
        processo.envio.xml
        processo.resposta.xml
        processo.resposta.reason
        
        return processo
                

    def inutilizar_faixa_numeracao(self, cnpj, serie, numero_inicial, numero_final, justificativa,
                                   cert, key, nfce=False, versao=u'2.00', ambiente=2, estado=u'MG',
                                   contingencia=False, salvar_arquivos=True, caminho=u''):
        """
        Realiza a inutilização de faixa de numeração de nota fiscal
        @param cnpj:cnpj do emitente
        @param serie: série da nfe
        @param numero_inicial: faixa inicial da nota que deseja inutilizar
        @param numero_final: faixa final da nota que deseja inutilizar
        @param justificativa: justificativa da inutilização 
        @param nfce: True se inutilizando numeração de NFC-e
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.contingencia = contingencia
        p.caminho = caminho
        p.nfce = nfce
        
        processo = p.inutilizar_nota(cnpj=cnpj, serie=serie, numero_inicial=numero_inicial,
                                     numero_final=numero_final, justificativa=justificativa)
        processo.envio.xml
        processo.resposta.xml
        processo.resposta.reason
        
        return processo
        
    def gerar_danfe(self, proc_nfe, retcan_nfe=None, site_emitente=u'', logo=u'',
                    nome_sistema=u'', leiaute_logo_vertical=False, versao='3.10', salvar_arquivo=False):
        """
        Geração do DANFE
        @param nfe: string da NF-e processada ou objeto ProcNFe_310
        @param site_emitente: Endereço do site do emitente
        @param logo: O caminho para a imagem ou  Instância da imagem.
        @param leiaute_logo_vertical: possibilita que a logomarca tenha a orientação vertical
        @return: String
        """
        d = DANFE()
        if isinstance(proc_nfe, basestring):
            if versao == '3.10':
                proc = ProcNFe_310()
            else:
                proc = ProcNFe_200()
                
            proc.xml = proc_nfe
            
        else:
            proc = proc_nfe
            
        d.NFe = proc.NFe
        d.protNFe = proc.protNFe
        d.versao = versao
        d.salvar_arquivo = salvar_arquivo
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
    
    def gerar_danfce(self, proc_nfce, csc='', imprime_produtos=True, imprime_id_consumidor=True, imprime_ender_consumidor=True, via_estabelecimento=False, 
                    cidtoken='000001', nversao='100', versao='3.10', salvar_arquivo=False):
        '''
        Gerar DANFCE
        @param nfce: string da NFC-e processada ou objeto ProcNFe_310
        @param csc: Codigo de Segurança do Contribuinte
        @param imprime_produtos: imprime os produtos e seus dados na DANFE
        @param imprime_id_consumidor: imprime dados do consumidor na DANFE
        @param imprime_ender_consumidor: imprime o endereço do consumidor na DANFE
        @param via_estabelecimento: via do estabelecimento ou do consumidor
        @param cidtoken: identificador do csc
        '''
        d = DANFE()
        if isinstance(proc_nfce, basestring):
            if versao == '3.10':
                proc = ProcNFe_310()
            else:
                raise ValueError("Geracao de DANFCE apenas valido com versao 3.10")
                
            proc.xml = proc_nfce
            proc.NFe.infNFeSupl.csc = csc
            proc.NFe.infNFeSupl.cidtoken = cidtoken
            proc.NFe.infNFeSupl.nversao = nversao
            
        else:
            proc = proc_nfce
            
        if not proc.NFe.infNFeSupl.csc:
            raise ValueError("Informar Código de Segurança do Contribuinte (CSC)")
        
        d.NFe = proc.NFe
        d.protNFe = proc.protNFe
        d.versao = versao
        d.salvar_arquivo = False
        d.imprime_produtos_nfce = imprime_produtos
        d.imprime_id_consumidor = imprime_id_consumidor
        d.imprime_ender_consumidor = imprime_ender_consumidor
        d.obs_impressao = u'DANFCE gerado em %(now:%d/%m/%Y, %H:%M:%S)s'
        d.gerar_danfce(via_estabelecimento=via_estabelecimento)
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

    def consultar_nfe(self, chave, cert, key, versao=u'3.10', ambiente=2, estado=u'MG',
                      contingencia=False, salvar_arquivos=True, caminho=u''):
        """
        Consultar a situaçao da NF-e
        @param chave:chave da nfe
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.caminho = caminho
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.contingencia=contingencia
        p.salvar_arquivos = salvar_arquivos
        processo = p.consultar_nota(chave_nfe=chave)
        
        return processo

    def consultar_cadastro(self, cert, key, cpf_cnpj=None, inscricao_estadual=None, versao=u'2.00',
                           ambiente=2, estado=u'MG', contingencia=False, salvar_arquivos=True, caminho=u''):
        """
        Consulta cadastro do contribuinte
        @param cpf_cnpj: CPF ou CNPJ do contribuinte
        @param inscricao_estadual: IE do contribuinte
        @return: Dicionário com o envio,resposta e reason.
        """
        if cpf_cnpj is None and inscricao_estadual is None:
            raise ValueError("Deve-se informar o CNPJ ou CPF ou IE.")
        
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.caminho = caminho
        
        if estado in ('AC', 'AL', 'AP', 'DF', 'ES', 'PB', 'RJ', 'RN', 'RO', 'RR', 'SC',
                  'SE', 'TO'):
            #SVRS[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'svp-ws.sefazvirtual.rs.gov.br'
            if versao == '3.10':
                SVRS3[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'cad.svrs.rs.gov.br'
            else:
                SVRS[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'cad.svrs.rs.gov.br'
        if estado == 'RS':
            #UFRS[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'sef.sefaz.rs.gov.br'
            if versao == '3.10':
                UFRS3[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'cad.sefazrs.rs.gov.br'
            else:
                UFRS[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'cad.sefazrs.rs.gov.br'
        if estado == 'MA':
            if versao == '3.10':
                SVAN3[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'sistemas.sefaz.ma.gov.br'
                SVAN3[NFE_AMBIENTE_PRODUCAO][WS_NFE_CONSULTA_CADASTRO] = u'wscadastro/CadConsultaCadastro2'
            else:
                SVAN[NFE_AMBIENTE_PRODUCAO][u'servidor'] = u'sistemas.sefaz.ma.gov.br'
                SVAN[NFE_AMBIENTE_PRODUCAO][WS_NFE_CONSULTA_CADASTRO] = u'wscadastro/CadConsultaCadastro2'
        
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.contingencia = contingencia
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.consultar_cadastro_contribuinte(cpf_cnpj=cpf_cnpj,
                                                     inscricao_estadual=inscricao_estadual,
                                                     ambiente=ambiente)
                                                     
        return processo

    def consultar_nfe_destinatario(self, cnpj, indnfe, indemi, cert, key, nsu='0', versao=u'3.10',
                                   ambiente=2, estado=u'MG', contingencia=False, salvar_arquivos=True, caminho=u''):
        """
        Realiza  a consulta do manifesto do destinatário
        @return: Dicionário com o envio,resposta e reason.
        """
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.caminho = caminho
        #Provisoriamente apontado para um estado que usa o webservice de ambiente nacional, pois em MG ainda
        # não existe suporte ao Manifesto do Destinatário
        if versao == '3.10':
            ESTADO_WS3[estado] = AN
        else:
            ESTADO_WS[estado] = AN
        #ESTADO_WS[estado] = SVAN
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.contingencia = contingencia
        p.salvar_arquivos = salvar_arquivos
        processo = p.consultar_notas_destinatario(cnpj=cnpj, indnfe=indnfe, indemi=indemi, nsu=nsu)
        
        return processo
        

    def download_notas(self, cnpj, lista_chaves,  cert, key, ambiente_nacional=True, versao=u'2.00', ambiente=2, estado=u'MG',
                     contingencia=False, salvar_arquivos=True, caminho=u''):
        """
        Realiza download de NFe para uma determinada chave de acesso, para NF-e confirmada pelo destinatario.
        @param lista_chaves: lista de até 10 chaves
        @return: Dicionário com o envio,resposta e reason.
        """
        if len(lista_chaves)>10:
            raise ValueError(u'Maximo de 10 Chaves de Acesso por lote.')
            
        p = ProcessadorNFe()
        p.versao = versao
        p.estado = estado
        p.caminho = caminho
        if ambiente_nacional:
            if versao == '3.10':
                #ESTADO_WS3[estado] = SVAN3
                ESTADO_WS3[estado] = AN
            else:
                #ESTADO_WS[estado] = SVAN
                ESTADO_WS[estado] = AN
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.contingencia = contingencia
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.download_nfes(cnpj, ambiente, lista_chaves=lista_chaves)
        
        return processo
