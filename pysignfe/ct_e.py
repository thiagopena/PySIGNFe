# -*- coding: utf-8 -*-

from .nota import NotaFiscal
from pysignfe.cte import ProcessadorCTe
from pysignfe.cte.v300 import *


'''
Serviços:
-Recepção de CT-e
-Inutilização de Numeração de CT-e
-Consulta da situação atual do CT-e
-Registro de Evento de CT-e
    *Cancelamento e Carta correção
    *Faltam eventos: EPEC, Registro do Multimodal, Serviço em desacordo e GTV
-Consulta do status do serviço
-Consulta Cadastro (especificação no MOC da NF-e) (Não feito, consultar cadastro pela mensagem de retorno do envio.)
-Recepção de CT-e Outros Serviços (Não feito por enquanto)
'''

class ct_e(NotaFiscal):

    def consultar_servidor(self, cert, key, versao=u'3.00', ambiente=2, estado=u'MG',
                           salvar_arquivos=True):
        
        p = ProcessadorCTe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao = versao
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos

        processo = p.consultar_servico()
        status = processo.resposta.cStat.valor
        processo.envio.xml
        processo.resposta.xml
        processo.resposta.reason

        return{'status': status, 'envio': processo.envio.xml, 'resposta': processo.resposta.xml,
               'reason': processo.resposta.reason}
               
    def processar_lote_cte(self, lista_cte, cert, key, versao=u'3.00', ambiente=2, estado=u'MG',
                           tipo_contingencia=False, salvar_arquivos=True, n_consultas_recibo=2, consultar_servico=True):
                           
        p = ProcessadorCTe()
        p.ambiente = ambiente
        p.estado = estado
        p.versao = versao
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.tipo_contingencia = tipo_contingencia
        p.numero_tentativas_consulta_recibo = n_consultas_recibo
        p.verificar_status_servico = consultar_servico
        
        lista = []
        if lista_cte:
            for x in lista_cte:
                c = CTe_300()
                c.infCte.xml = x
                lista.append(c)
        
        for processo in p.processar_lote_cte(lista):
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
            vals['status_resposta_'+str(nome)]  = proc.protCTe.infProt.cStat.valor
            vals['numero_protocolo_'+str(nome)] = proc.protCTe.infProt.nProt.valor
            vals['status_motivo_'+str(nome)]    = proc.protCTe.infProt.xMotivo.valor

        return vals
        
    def inutilizar_cte(self, cnpj, serie, numero, justificativa, cert, key, versao=u'3.00',
                        ambiente=2, estado=u'MG', tipo_contingencia=False, salvar_arquivos=True):
        
        p = ProcessadorCTe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.tipo_contingencia = tipo_contingencia
        p.caminho = u''
        
        processo = p.inutilizar_cte(cnpj=cnpj, serie=serie, numero_inicial=numero,
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
        
    def consultar_cte(self, chave, cert, key, versao=u'3.00', ambiente=2, estado=u'MG',
                      tipo_contingencia=False, salvar_arquivos=True):
        
        p = ProcessadorCTe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.tipo_contingencia=tipo_contingencia
        p.salvar_arquivos = salvar_arquivos
        processo = p.consultar_cte(chave_cte=chave)
        
        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'status_resposta': processo.resposta.cStat.valor,
                'status_motivo': processo.resposta.xMotivo.valor,
                'reason': processo.resposta.reason,
        }
        
        return vals
        
    def cancelar_cte(self, cnpj, chave, protocolo, justificativa, cert, key, versao=u'3.00',
                      ambiente=2, estado=u'MG', tipo_contingencia=False, salvar_arquivos=True):
        
        p = ProcessadorCTe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.tipo_contingencia = tipo_contingencia
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        
        processo = p.cancelar_cte(cnpj, chave_cte=chave, numero_protocolo=protocolo,
                                   justificativa=justificativa)
        processo.resposta.reason
        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'status_resposta': processo.resposta.infEvento.cStat.valor,
                'status_motivo': processo.resposta.infEvento.xMotivo.valor,
                'reason': processo.resposta.reason}
        if processo.resposta.infEvento.cStat.valor in ('134', '135', '136',):
            vals['proc_cancelamento'] = processo.processo_evento_cte.xml
        if processo.resposta.infEvento.cStat.valor == '135':
            vals['protocolo'] = processo.resposta.infEvento.nProt.valor

        return vals
        
    def emitir_carta_correcao(self, chave, cnpj, cert, key, correcoes=[], sequencia=None,
                              versao=u'3.00', ambiente=2, estado=u'MG', tipo_contingencia=False,
                              salvar_arquivos=True):
        
        p = ProcessadorCTe()
        p.versao = versao
        p.estado = estado
        p.ambiente = ambiente
        p.certificado.cert_str = cert
        p.certificado.key_str = key
        p.salvar_arquivos = salvar_arquivos
        p.tipo_contingencia = tipo_contingencia
                
        processo = p.corrigir_cte(chave_cte=chave, cnpj=cnpj, correcoes=correcoes,
                                   ambiente=ambiente,sequencia=sequencia)        
        processo.resposta.reason
        vals = {'envio': processo.envio.xml,
                'resposta': processo.resposta.xml,
                'status_resposta': processo.resposta.infEvento.cStat.valor,
                'status_motivo': processo.resposta.infEvento.xMotivo.valor,
                'reason': processo.resposta.reason}
                
        if processo.resposta.infEvento.cStat.valor in ('134', '135', '136',):
            vals['proc_correcao'] = processo.processo_evento_cte.xml
        if processo.resposta.infEvento.cStat.valor == '135':
            vals['protocolo'] = processo.resposta.infEvento.nProt.valor

        return vals