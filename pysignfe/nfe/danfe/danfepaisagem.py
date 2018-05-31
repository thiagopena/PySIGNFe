# -*- coding: utf-8 -*-


from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import HexColor

from geraldo import Report, ReportBand, SubReport
from geraldo import ObjectValue, SystemField, Label, Line, Rect, Image
from geraldo.barcodes import BarCode
from geraldo.generators import PDFGenerator

import os
cur_dir = os.path.dirname(os.path.abspath(__file__))

from pysignfe.relato_sped import *
from pysignfe.nfe.manual_401 import Vol_200

EMIT_DADOS_PAISAGEM     = {'fontName': FONTE_NEGRITO, 'fontSize': FONTE_TAMANHO_8, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_8}
EMIT_NOME_PAISAGEM      = {'fontName': FONTE_NEGRITO, 'fontSize': FONTE_TAMANHO_11, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_9}
DADO_VARIAVEL_PAISAGEM  = {'fontName': FONTE_NORMAL, 'fontSize': FONTE_TAMANHO_8, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_9}

class DANFEPaisagem(Report):
    def __init__(self, *args, **kargs):
        super(DANFEPaisagem, self).__init__(*args, **kargs)
        self.title = 'DANFE - Documento Auxiliar da Nota Fiscal Eletrônica'
        self.print_if_empty = True
        self.additional_fonts = FONTES_ADICIONAIS
        
        self.page_size = PAISAGEM
        '''
        self.margin_top = MARGEM_SUPERIOR
        self.margin_bottom = MARGEM_INFERIOR
        self.margin_left = MARGEM_ESQUERDA
        self.margin_right = MARGEM_DIREITA
        '''
        self.margin_top = 0*cm
        self.margin_bottom = 0.5*cm
        self.margin_left = 0*cm
        self.margin_right = 0*cm
        
        # Bandas e observações
        self.canhoto          = CanhotoPaisagem()
        self.remetente        = RemetentePaisagem()
        self.destinatario     = DestinatarioPaisagem()
        self.local_retirada   = LocalRetiradaPaisagem()
        self.local_entrega    = LocalEntregaPaisagem()
        self.fatura_a_vista   = FaturaAVistaPaisagem()
        self.fatura_a_prazo   = FaturaAPrazoPaisagem()
        self.duplicatas       = DuplicatasPaisagem()
        self.calculo_imposto  = CalculoImpostoPaisagem()
        self.transporte       = TransportePaisagem()
        self.cab_produto      = CabProdutoPaisagem()
        self.det_produto      = DetProdutoPaisagem()
        self.iss              = ISSPaisagem()
        self.dados_adicionais = DadosAdicionaisPaisagem()
        self.rodape_final     = RodapeFinalPaisagem()
    
    def do_on_new_page(self, page, page_number, generator):
        if generator._current_page_number != 1:
            self.band_page_footer = self.rodape_final
            self.band_page_header.child_bands.append(self.remetente)
            self.band_page_header.child_bands = []
            self.band_page_header.child_bands.append(self.cab_produto)

    def format_date(self, data, formato):
        #return  data.strftime(formato.encode('utf-8')).decode('utf-8')
        return  data.strftime(formato)
        
        
    class ObsImpressao(SystemField):
        expression = u'DANFE gerado em %(now:%d/%m/%Y, %H:%M:%S)s'

        def __init__(self):
            self.name = 'obs_impressao'
            self.top = 0*cm
            self.left = 2.6*cm
            self.width = 26.8*cm
            self.height = 0.15*cm
            self.style = DADO_PRODUTO = {'fontName': FONTE_NORMAL, 'fontSize': FONTE_TAMANHO_5, 'leading': FONTE_TAMANHO_8}
            #self.borders = {'bottom': 1.0}    
    
    
class CanhotoPaisagem(BandaDANFE):
    def __init__(self):
        super(CanhotoPaisagem, self).__init__()
        self.elements = []
        lbl, txt = self.inclui_texto(nome='', titulo='', texto=u'', top=4.2*cm, left=0.15*cm, width=0.9*cm, height=16.5*cm)
        fld = self.inclui_campo_sem_borda(nome='canhoto_recebemos_vertical', conteudo=u'NFe.canhoto_formatado', top=20.2*cm, left=0.15*cm, width=16.5*cm)
        fld.style = {'fontName': FONTE_NEGRITO, 'fontSize': FONTE_TAMANHO_6}
        
        self.inclui_texto(nome='', titulo=u'', texto='', top=15.7*cm, left=1.05*cm, height=5*cm, width=1*cm)
        fld = self.inclui_texto_sem_borda(nome='canhoto_data_vertical', texto=u'DATA DE RECEBIMENTO', top=20.2*cm, left=1.05*cm, height=1.02*cm, width=5*cm)
        fld.style = {'fontName': FONTE_NEGRITO, 'fontSize': FONTE_TAMANHO_6}
        self.inclui_texto(nome='', titulo=u'', texto='', top=4.2*cm, left=1.05*cm, height=11.5*cm, width=1*cm)
        fld = self.inclui_texto_sem_borda(nome='canhoto_assinatura_vertical', texto=u'IDENTIFICAÇÃO E ASSINATURA DO RECEBEDOR', top=15.2*cm, left=1.05*cm, height=1.02*cm, width=5*cm)
        fld.style = {'fontName': FONTE_NEGRITO, 'fontSize': FONTE_TAMANHO_6}
        
        self.inclui_texto(nome='', titulo=u'', texto='', top=0.3*cm, left=0.15*cm, height=3.9*cm, width=1.9*cm)
        fld = self.inclui_texto_sem_borda(nome='canhoto_nfe_vertical', texto=u'NF-e', top=2.4*cm, left=0.2*cm, height=3.4*cm, width=1.4*cm)
        fld.style = {'fontName': FONTE_NEGRITO, 'fontSize': FONTE_TAMANHO_11}
        fld = self.inclui_campo_sem_borda(nome='canhoto_numero_vertical', conteudo=u'NFe.numero_formatado', top=3.3*cm, left=0.7*cm, width=3.4*cm, height=0.5*cm)
        fld.style = {'fontName': FONTE_NEGRITO, 'fontSize': FONTE_TAMANHO_12}
        fld = self.inclui_campo_sem_borda(nome='canhoto_serie_vertical', conteudo=u'NFe.serie_formatada', top=3*cm, left=1.3*cm, width=3.4*cm, height=0.5*cm)
        fld.style = {'fontName': FONTE_NEGRITO, 'fontSize': FONTE_TAMANHO_12}
        
        self.elements.append(Line(top=0.3*cm, bottom=20.7*cm, left=2.3*cm, right=2.3*cm, stroke_width=0.1))
        self.height = 0*cm
        
        
class RemetentePaisagem(BandaDANFE):
    def __init__(self):
        super(RemetentePaisagem, self).__init__()
        self.elements = []

        # Quadro do emitente
        lbl, txt = self.inclui_texto(nome='quadro_emitente', titulo='', texto='', top=0.3*cm, left=2.6*cm, width=11*cm, height=3.1*cm)
        
        #
        # Área central - Dados do DANFE
        #
        lbl, txt = self.inclui_texto(nome='danfe', titulo='', texto=u'DANFE', top=0.3*cm, left=13.6*cm, width=3.1*cm, height=3.1*cm)
        txt.padding_top = 0*cm
        txt.style = DESCRITIVO_DANFE
        
        txt = self.inclui_texto_sem_borda(nome='danfe_ext', texto=u'DOCUMENTO AUXILIAR DA NOTA FISCAL ELETRÔNICA', top=0.67*cm, left=13.6*cm, width=3.1*cm, height=3.1*cm)
        txt.style = DESCRITIVO_DANFE_GERAL
        
        txt = self.inclui_texto_sem_borda(nome='danfe_entrada', texto=u'0 - ENTRADA', top=1.4*cm, left=13.7*cm, width=3.1*cm, height=3.1*cm)
        txt.style = DESCRITIVO_DANFE_ES
        
        txt = self.inclui_texto_sem_borda(nome='danfe_saida', texto=u'1 - SAÍDA', top=1.65*cm, left=13.7*cm, width=3.1*cm, height=3.1*cm)
        txt.style = DESCRITIVO_DANFE_ES
        
        fld = self.inclui_campo_sem_borda(nome='danfe_entrada_saida', conteudo=u'NFe.infNFe.ide.tpNF.valor', top=1.5*cm, left=15.7*cm, width=0.6*cm, height=0.6*cm)
        fld.style = DESCRITIVO_NUMERO
        fld.borders = {'top': 1.0, 'right': 1.0, 'bottom': 1.0, 'left': 1.0}
        fld.padding_bottom = 1.0*cm
        
        fld = self.inclui_campo_sem_borda(nome='danfe_numero', conteudo=u'NFe.numero_formatado', top=2.1*cm, left=13.4*cm, width=3.4*cm, height=0.5*cm)
        fld.style = DESCRITIVO_NUMERO

        fld = self.inclui_campo_sem_borda(nome='danfe_serie', conteudo=u'NFe.serie_formatada', top=2.45*cm, left=13.4*cm, width=3.4*cm, height=0.5*cm)
        fld.style = DESCRITIVO_NUMERO
        
        fld = SystemField(name='fld_danfe_folha', expression=u'FOLHA %(page_number)02d/%(page_count)02d', top=2.9*cm, left=13.4*cm, width=3.4*cm, height=0.5*cm)
        fld.style = DESCRITIVO_NUMERO
        self.elements.append(fld)
        
        #
        # No caso dos códigos de barra, altura (height) e largura (width) se referem às barras, não à imagem
        #
        lbl, txt = self.inclui_texto(nome='', titulo='', texto=u'', top=0.3*cm, left=16.7*cm, width=12.7*cm, height=1.2*cm)
        self.elements.append(BarCode(type=u'Code128', attribute_name=u'NFe.chave_para_codigo_barras', top=0.5*cm, left=18.8*cm, width=0.025*cm, height=0.8*cm))
        
        lbl, fld = self.inclui_campo(nome='remetente_chave', titulo=u'CHAVE DE ACESSO', conteudo=u'NFe.chave_formatada', top=1.5*cm, left=16.7*cm, width=12.7*cm, margem_direita=True)
        fld.style = DADO_CHAVE
        
        self.inclui_campo(nome='remetente_natureza', titulo=u'NATUREZA DA OPERAÇÃO', conteudo=u'NFe.infNFe.ide.natOp.valor', top=3.4*cm, left=2.6*cm, width=14.1*cm, height=0.7*cm)

        self.inclui_campo(nome='remetente_ie', titulo=u'INSCRIÇÃO ESTADUAL', conteudo=u'NFe.infNFe.emit.IE.valor', top=4.1*cm, left=2.6*cm, width=9*cm)
        self.inclui_campo(nome='remetente_iest', titulo=u'INSCRIÇÃO ESTADUAL DO SUBSTITUTO TRIBUTÁRIO', conteudo=u'NFe.infNFe.emit.IEST.valor', top=4.1*cm, left=11.6*cm, width=9*cm)
        self.inclui_campo(nome='remetente_cnpj', titulo=u'CNPJ', conteudo=u'NFe.cnpj_emitente_formatado', top=4.1*cm, left=20.6*cm, width=8.8*cm, margem_direita=True)
        
        self.height = 4.8*cm
        
    def campo_variavel_conferencia(self):
        txt = self.inclui_texto_sem_borda(nome='remetente_var1', texto=u'<font color="red"><b>Impresso para simples conferência<br />Informações ainda não transmitidas a nenhuma SEFAZ autorizadora, nem ao SCAN<br />Sem valor fiscal</b></font>', top=2.2*cm, left=16.7*cm, width=12.7*cm, height=0.9*cm)
        txt.padding_top = 0.1*cm
        txt.style = DADO_VARIAVEL_PAISAGEM
        
        self.elements.append(Line(top=2.2*cm, bottom=3.6*cm, left=29.4*cm, right=29.4*cm, stroke_width=1))

        lbl, lbl = self.inclui_campo(nome='remetente_var2', titulo=u'PROTOCOLO DE AUTORIZAÇÃO DE USO', conteudo=u'protNFe.protocolo_formatado', top=3.4*cm, left=16.7*cm, width=12.7*cm, margem_direita=True)
        lbl.style = DADO_VARIAVEL

    def campo_variavel_normal(self):
        txt = self.inclui_texto_sem_borda(nome='remetente_var1', texto=u'Consulta de autenticidade no portal nacional da NF-e<br /><a href="http://www.nfe.fazenda.gov.br/portal"><u>www.nfe.fazenda.gov.br/portal</u></a><br /> ou no site da SEFAZ autorizadora', top=2.2*cm, left=16.7*cm, width=12.7*cm, height=0.9*cm)
        txt.padding_top = 0.1*cm
        txt.style = DADO_VARIAVEL_PAISAGEM
        
        self.elements.append(Line(top=2.2*cm, bottom=3.6*cm, left=29.4*cm, right=29.4*cm, stroke_width=1))
        
        lbl, lbl = self.inclui_campo(nome='remetente_var2', titulo=u'PROTOCOLO DE AUTORIZAÇÃO DE USO', conteudo=u'protNFe.protocolo_formatado', top=3.4*cm, left=16.7*cm, width=12.7*cm, margem_direita=True)
        lbl.style = DADO_VARIAVEL

    def campo_variavel_denegacao(self):
        txt = self.inclui_texto_sem_borda(nome='remetente_var1', texto=u'A circulação da mercadoria foi <font color="red"><b>PROIBIDA</b></font> pela SEFAZ<br />autorizadora, devido a irregularidades fiscais.', top=2.2*cm, left=16.7*cm, width=12.7*cm, height=0.9*cm)
        txt.padding_top = 0.2*cm
        txt.style = DADO_VARIAVEL_PAISAGEM
        
        self.elements.append(Line(top=2.2*cm, bottom=3.6*cm, left=29.4*cm, right=29.4*cm, stroke_width=1))

        lbl, lbl = self.inclui_campo(nome='remetente_var2', titulo=u'PROTOCOLO DE DENEGAÇÃO DE USO', conteudo=u'protNFe.protocolo_formatado', top=3.4*cm, left=16.7*cm, width=12.7*cm, margem_direita=True)
        lbl.style = DADO_VARIAVEL

    def campo_variavel_contingencia_fsda(self):
        #
        # No caso dos códigos de barra, altura (height) e largura (width) se referem às barras, não à imagem
        #
        self.elements.append(BarCode(type=u'Code128', attribute_name=u'NFe.dados_contingencia_fsda_para_codigo_barras', top=2.4*cm, left=19.4*cm, width=0.025*cm, height=0.8*cm))
        
        self.elements.append(Line(top=2.2*cm, bottom=3.6*cm, left=29.4*cm, right=29.4*cm, stroke_width=1))
        
        lbl, fld = self.inclui_campo(nome='remetente_var2', titulo=u'DADOS DA NF-e', conteudo=u'NFe.dados_contingencia_fsda_formatados', top=3.4*cm, left=16.7*cm, width=12.7*cm, margem_direita=True)
        fld.style = DADO_CHAVE

    def campo_variavel_contingencia_dpec(self):
        txt = self.inclui_texto_sem_borda(nome='remetente_var1', texto=u'Consulta de autenticidade no portal nacional da NF-e<br /><a href="http://www.nfe.fazenda.gov.br/portal"><u>www.nfe.fazenda.gov.br/portal</u></a>', top=2.2*cm, left=16.7*cm, width=12.7*cm, height=0.9*cm)
        txt.padding_top = 0.2*cm
        txt.style = DADO_VARIAVEL_PAISAGEM
        
        self.elements.append(Line(top=2.2*cm, bottom=3.6*cm, left=29.4*cm, right=29.4*cm, stroke_width=1))
        
        lbl, txt = self.inclui_texto(nome='remetente_var2', titulo=u'NÚMERO DE REGISTRO DPEC', texto=u'123456789012345 99/99/9999 99:99:99', top=3.4*cm, left=16.7*cm, width=12.7*cm, margem_direita=True)
        txt.style = DADO_VARIAVEL

    def obs_cancelamento(self):
        txt = Texto()
        txt.name   = 'txt_obs_cancelamento'
        txt.text   = u'cancelada'
        txt.top    = 3*cm
        txt.left   = 9.85*cm
        txt.width  = 10*cm
        txt.height = 2*cm
        txt.padding_top = 0.1*cm
        txt.style  = OBS_CANCELAMENTO
        self.elements.insert(0, txt)

        lbl = LabelMargemEsquerda()
        lbl.borders = {'top': 1.0, 'right': 1.0, 'bottom': 1.0, 'left': 1.0}
        lbl.name = 'lbl_prot_cancelamento'
        lbl.text = u'PROTOCOLO<br />DE CANCELAMENTO'
        lbl.top = 4.85*cm
        lbl.left = 11*cm
        lbl.width = 1.75*cm
        lbl.style = DESCRITIVO_CAMPO_CANCELAMENTO
        self.elements.append(lbl)

        fld = Campo()
        fld.name = 'fld_prot_cancelamento'
        fld.attribute_name = u'retCancNFe.protocolo_formatado'
        fld.top  = 4.65*cm
        fld.left = 12.35*cm
        fld.width = 6.3*cm
        fld.padding_top = 0.25*cm
        fld.style = DADO_VARIAVEL_CANCELAMENTO

        self.elements.insert(2, fld)

    def obs_denegacao(self):
        txt = Texto()
        txt.name   = 'txt_obs_denegacao'
        txt.text   = u'denegada'
        txt.top    = 3*cm
        txt.left   = 9.85*cm
        txt.width  = 10*cm
        txt.height = 2*cm
        txt.padding_top = 0.1*cm
        txt.style  = OBS_CANCELAMENTO
        self.elements.insert(0, txt)

        lbl = LabelMargemEsquerda()
        lbl.borders = {'top': 1.0, 'right': 1.0, 'bottom': 1.0, 'left': 1.0}
        lbl.name = 'lbl_prot_denegacao'
        lbl.text = u'PROTOCOLO<br />DE DENEGAÇÃO'
        lbl.top = 4.85*cm
        lbl.left = 11*cm
        lbl.width = 1.75*cm
        lbl.style = DESCRITIVO_CAMPO_CANCELAMENTO
        self.elements.append(lbl)

        fld = Campo()
        fld.name = 'fld_prot_denegacao'
        fld.attribute_name = u'protNFe.protocolo_formatado'
        fld.top  = 4.65*cm
        fld.left = 12.35*cm
        fld.width = 6.3*cm
        fld.padding_top = 0.25*cm
        fld.style = DADO_VARIAVEL_CANCELAMENTO

        self.elements.insert(2, fld)

    def obs_contingencia_normal_scan(self):
        lbl = Texto()
        lbl.name  = 'txt_obs_contingencia'
        lbl.text  = u'DANFE em contingência<br /><br />impresso em decorrência de problemas técnicos'
        lbl.top   = 5.4*cm
        lbl.left  = 6*cm
        lbl.width = 19.4*cm
        lbl.padding_top = 0.1*cm
        lbl.style = OBS_CONTINGENCIA
        self.elements.insert(0, lbl)

    def obs_contingencia_dpec(self):
        lbl = Texto()
        lbl.name  = 'txt_obs_contingencia'
        lbl.text  = u'DANFE em contingência<br /><br />DPEC regularmente recebida pela Receita Federal do Brasil'
        lbl.top   = 5.4*cm
        lbl.left  = 6*cm
        lbl.width = 19.4*cm
        lbl.padding_top = 0.1*cm
        lbl.style = OBS_CONTINGENCIA
        self.elements.insert(0, lbl)

    def obs_sem_valor_fiscal(self):
        lbl = Texto()
        lbl.name  = 'txt_obs_homologacao'
        lbl.text  = u'Sem valor fiscal'
        lbl.top   = 9*cm
        lbl.left  = 6*cm
        lbl.width = 19.4*cm
        lbl.padding_top = 0.1*cm
        lbl.style = OBS_HOMOLOGACAO
        self.elements.append(lbl)

    def monta_quadro_emitente(self, dados_emitente=[]):
        for de in dados_emitente:
            self.elements.append(de)

    def dados_emitente_sem_logo(self):
        elements = []

        #
        # Dados do remetente
        #
        fld = Campo()
        fld.nome  = 'fld_rem_nome'
        fld.attribute_name = u'NFe.infNFe.emit.xNome.valor'
        fld.top   = 0.4*cm
        fld.left = 4.1*cm
        fld.width = 8*cm
        fld.height = 0.7*cm
        fld.style = EMIT_NOME_PAISAGEM
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_1'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_1'
        fld.top   = 1.1*cm
        fld.left = 4.1*cm
        fld.width = 8*cm
        fld.height = 0.7*cm
        fld.style = EMIT_DADOS_PAISAGEM
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_2'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_2'
        fld.top   = 1.8*cm
        fld.left = 4.1*cm
        fld.width = 8*cm
        fld.height = 0.7*cm
        fld.style = EMIT_DADOS_PAISAGEM
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_3'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_3'
        fld.top   = 2.5*cm
        fld.left = 4.1*cm
        fld.width = 8*cm
        fld.height = 0.45*cm
        fld.style = EMIT_DADOS_PAISAGEM
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_4'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_4'
        fld.top   = 2.9*cm
        fld.left = 4.1*cm
        fld.width = 8*cm
        fld.height = 0.45*cm
        fld.style = EMIT_DADOS_PAISAGEM
        elements.append(fld)

        return elements

    def dados_emitente_logo_vertical(self, arquivo_imagem):
        elements = []

        #
        # Dados do remetente
        #
        img = Image()


        img.top = 0.4*cm
        img.left = 3.6*cm
        #
        # Tamanhos equilaventes, em centímetros, a 2,5 x 3,8, em 128 dpi
        # estranhamente, colocar os tamanhos em centímetros encolhe a imagem
        #
        img.width  = 2*cm/(0.02*cm)     #geraldo retorna a altura e comprimento das imagens multiplicada por 0.02*cm por algum motivo
        img.height = 2.9*cm/(0.02*cm)
        img.filename = arquivo_imagem
        elements.append(img)

        fld = Campo()
        fld.nome  = 'fld_rem_nome'
        fld.attribute_name = u'NFe.infNFe.emit.xNome.valor'
        fld.top   = 0.4*cm
        fld.left  = 6.5*cm
        fld.width = 5.4*cm
        fld.height = 0.7*cm
        fld.style = EMIT_NOME
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_1'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_1'
        fld.top   = 1.1*cm
        fld.left  = 6.5*cm
        fld.width = 5.4*cm
        fld.height = 0.7*cm
        fld.style = EMIT_DADOS
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_2'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_2'
        fld.top   = 1.8*cm
        fld.left  = 6.5*cm
        fld.width = 5.4*cm
        fld.height = 0.7*cm
        fld.style = EMIT_DADOS
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_3'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_3'
        fld.top   = 2.5*cm
        fld.left  = 6.5*cm
        fld.width = 5.4*cm
        fld.height = 0.45*cm
        fld.style = EMIT_DADOS
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_4'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_4'
        fld.top   = 3*cm
        fld.left  = 6.5*cm
        fld.width = 5.4*cm
        fld.height = 0.45*cm
        fld.style = EMIT_DADOS
        elements.append(fld)

        return elements

    def dados_emitente_logo_horizontal(self, arquivo_imagem):
        elements = []

        #
        # Dados do remetente
        #
        img = Image()

        img.top = 0.6*cm
        img.left = 3.1*cm
        #
        # Tamanhos equilaventes, em centímetros, a 3,8 x 2,5, em 128 dpi
        # estranhamente, colocar os tamanhos em centímetros encolhe a imagem
        #
        img.width  = 4*cm/(0.02*cm)     #geraldo retorna a altura e comprimento das imagens multiplicada por 0.02*cm por algum motivo
        img.height = 2.5*cm/(0.02*cm)
        img.filename = arquivo_imagem

        elements.append(img)

        fld = Campo()
        fld.nome  = 'fld_rem_nome'
        fld.attribute_name = u'NFe.infNFe.emit.xNome.valor'
        fld.top   = 0.4*cm
        fld.left  = 7.5*cm
        fld.width = 5.4*cm
        fld.height = 0.7*cm
        fld.style = EMIT_NOME
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_3'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_3'
        fld.top   = 2.5*cm
        fld.left  = 7.5*cm
        fld.width = 5.4*cm
        fld.height = 0.45*cm
        fld.style = EMIT_DADOS
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_4'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_4'
        fld.top   = 3*cm
        fld.left  = 7.5*cm
        fld.width = 5.4*cm
        fld.height = 0.45*cm
        fld.style = EMIT_DADOS
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_1'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_1'
        fld.top   = 1.1*cm
        fld.left  = 7.5*cm
        fld.width = 5.4*cm
        fld.height = 0.7*cm
        fld.style = EMIT_DADOS
        elements.append(fld)

        fld = Campo()
        fld.nome  = 'fld_rem_endereco_2'
        fld.attribute_name = u'NFe.endereco_emitente_formatado_linha_2'
        fld.top   = 1.8*cm
        fld.left  = 7.5*cm
        fld.width = 5.4*cm
        fld.height = 0.7*cm
        fld.style = EMIT_DADOS
        elements.append(fld)

        return elements


class DestinatarioPaisagem(BandaDANFE):
    def __init__(self):
        super(DestinatarioPaisagem, self).__init__()
        self.elements = []
        lbl = self.inclui_descritivo(nome='remetente', titulo=u'DESTINATÁRIO/REMETENTE', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)
        
        # 1ª linha
        lbl, fld = self.inclui_campo(nome='remetente_nome', titulo=u'NOME/RAZÃO SOCIAL', conteudo=u'NFe.nome_destinatario_formatado', top=0.4*cm, left=2.6*cm, width=17*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='remetente_cnpj', titulo=u'CNPJ/CPF', conteudo=u'NFe.cnpj_destinatario_formatado', top=0.4*cm, left=19.6*cm, width=6*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        fld.style = DADO_CAMPO_NEGRITO
        lbl, fld = self.inclui_campo(nome='remetente_data_emissao', titulo=u'DATA DA EMISSÃO', conteudo=u'NFe.infNFe.ide.dEmi.formato_danfe', top=0.4*cm, left=25.6*cm, width=3.8*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        fld.style = DADO_CAMPO_NEGRITO
        
        # 2ª linha
        lbl, fld = self.inclui_campo(nome='remetente_nome', titulo=u'ENDEREÇO', conteudo=u'NFe.endereco_destinatario_formatado', top=1*cm, left=2.6*cm, width=13*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='remetente_bairro', titulo=u'BAIRRO/DISTRITO', conteudo=u'NFe.infNFe.dest.enderDest.xBairro.valor', top=1*cm, left=15.6*cm, width=6*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='remetente_cep', titulo=u'CEP', conteudo=u'NFe.cep_destinatario_formatado', top=1*cm, left=21.6*cm, width=4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='remetente_data_entradasaida', titulo=u'DATA DA ENTRADA/SAÍDA', conteudo=u'NFe.infNFe.ide.dSaiEnt.formato_danfe', top=1*cm, left=25.6*cm, width=3.8*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        fld.style = DADO_CAMPO_NEGRITO
        
        ## 3ª linha
        lbl, fld = self.inclui_campo(nome='remetente_municipio', titulo=u'MUNICÍPIO', conteudo=u'NFe.infNFe.dest.enderDest.xMun.valor', top=1.6*cm, left=2.6*cm, width=10.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='remetente_fone', titulo=u'FONE', conteudo=u'NFe.fone_destinatario_formatado', top=1.6*cm, left=13*cm, width=5*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='remetente_uf', titulo=u'UF', conteudo='NFe.infNFe.dest.enderDest.UF.valor', top=1.6*cm, left=18*cm, width=1.5*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='remetente_ie', titulo=u'INSCRIÇÃO ESTADUAL', conteudo=u'NFe.infNFe.dest.IE.valor', top=1.6*cm, left=19.5*cm, width=6.1*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='remetente_hora_entradasaida', titulo=u'HORA DA ENTRADA/SAÍDA', conteudo=u'NFe.infNFe.ide.hSaiEnt.formato_danfe', top=1.6*cm, left=25.6*cm, width=3.8*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        fld.style = DADO_CAMPO_NEGRITO
        
        self.height = 2.2*cm

class LocalRetiradaPaisagem(BandaDANFE):
    def __init__(self):
        super(LocalRetiradaPaisagem, self).__init__()
        self.elements = []
        self.inclui_descritivo(nome='locret', titulo=u'LOCAL DE RETIRADA', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)

        # 1ª linha
        lbl, fld = self.inclui_campo(nome='locret_cnpj', titulo=u'CNPJ/CPF', conteudo=u'NFe.cnpj_retirada_formatado', top=0.4*cm, left=2.6*cm, width=8*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='locret_endereco', titulo=u'ENDEREÇO', conteudo=u'NFe.endereco_retirada_formatado', top=0.4*cm, left=10.6*cm, width=18.8*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        
        self.height = 1*cm
        


class LocalEntregaPaisagem(BandaDANFE):
    def __init__(self):
        super(LocalEntregaPaisagem, self).__init__()
        self.elements = []
        self.inclui_descritivo(nome='locent', titulo=u'LOCAL DE ENTREGA', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)

        # 1ª linha
        lbl, fld = self.inclui_campo(nome='locent_cnpj', titulo=u'CNPJ/CPF', conteudo=u'NFe.cnpj_entrega_formatado', top=0.4*cm, left=2.6*cm, width=8*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='locent_endereco', titulo=u'ENDEREÇO', conteudo=u'NFe.endereco_entrega_formatado', top=0.4*cm, left=10.6*cm, width=18.8*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        
        self.height = 1*cm
        


class FaturaAVistaPaisagem(BandaDANFE):
    def __init__(self):
        super(FaturaAVistaPaisagem, self).__init__()
        self.elements = []
        self.inclui_descritivo(nome='fat', titulo=u'FATURA', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)

        # 1ª linha
        lbl, txt = self.inclui_texto(nome='fat_texto', titulo='', texto=u'PAGAMENTO À VISTA', top=0.4*cm, left=2.6*cm, width=10*cm, height=0.6*cm)
        txt.padding_top = 0.1*cm
        lbl, fld = self.inclui_campo(nome='fat_numero', titulo=u'NÚMERO DA FATURA', conteudo=u'NFe.infNFe.cobr.fat.nFat.valor', top=0.4*cm, left=12.6*cm, width=9*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='fat_vorig', titulo=u'VALOR LÍQUIDO', conteudo=u'NFe.infNFe.cobr.fat.vLiq.formato_danfe', top=0.4*cm, left=21.6*cm, width=7.8*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        
        self.height = 1*cm
        

class FaturaAPrazoPaisagem(BandaDANFE):
    def __init__(self):
        super(FaturaAPrazoPaisagem, self).__init__()
        self.elements = []
        self.inclui_descritivo(nome='fat', titulo=u'FATURA', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)

        # 1ª linha
        lbl, txt = self.inclui_texto(nome='fat_texto', titulo='', texto=u'PAGAMENTO A PRAZO', top=0.4*cm, left=2.6*cm, width=10*cm, height=0.6*cm)
        txt.padding_top = 0.1*cm
        lbl.borders['right'] = {'top': 1.0, 'right': 1.0, 'bottom': 1.0, 'left': 1.0}

        lbl, fld = self.inclui_campo(nome='fat_numero', titulo=u'NÚMERO DA FATURA', conteudo=u'NFe.infNFe.cobr.fat.nFat.valor', top=0.4*cm, left=12.6*cm, width=9*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='fat_vorig', titulo=u'VALOR LÍQUIDO', conteudo=u'NFe.infNFe.cobr.fat.vLiq.formato_danfe', top=0.4*cm, left=21.6*cm, width=7.8*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        
        self.height = 1*cm
        

class DuplicatasPaisagem(SubReport):
    def __init__(self):
        super(DuplicatasPaisagem, self).__init__()
        self.get_queryset = lambda self, parent_object: parent_object.NFe.infNFe.cobr.dup or []

    class band_header(BandaDANFE):
        def __init__(self):
            super(DuplicatasPaisagem.band_header, self).__init__()
            self.elements = []
            self.inclui_descritivo(nome='dup', titulo=u'DUPLICATAS', top=1*cm, left=2.6*cm, width=6.4*cm, height=0.4*cm)
            self.height = 0.4*cm
    class band_detail(BandaDANFE):
        def __init__(self):
            super(DuplicatasPaisagem.band_detail, self).__init__()
            self.width = 6.4*cm
            self.display_inline = True
            self.margin_right = 0.08*cm
            self.margin_top = 0.08*cm

            self.elements = []
            lbl, fld = self.inclui_campo(nome='dup_numero', titulo=u'NÚMERO', conteudo=u'nDup.valor', top=1*cm, left=2.6*cm, width=2.8*cm, height=0.6*cm)
            fld.padding_top = 0.18*cm
            lbl, fld = self.inclui_campo(nome='dup_venc'  , titulo=u'VENCIMENTO', conteudo=u'dVenc.formato_danfe', top=1*cm, left=5.4*cm, width=1.9*cm, height=0.6*cm)
            fld.padding_top = 0.18*cm
            lbl, fld = self.inclui_campo_numerico(nome='dup_valor', titulo=u'VALOR', conteudo=u'vDup.formato_danfe', top=1*cm, left=7.3*cm, width=1.7*cm, height=0.6*cm, margem_direita=True)
            fld.padding_top = 0.18*cm
            
            self.height = fld.height


class CalculoImpostoPaisagem(BandaDANFE):
    def __init__(self):
        super(CalculoImpostoPaisagem, self).__init__()
        self.elements = []
        self.inclui_descritivo(nome='clc', titulo=u'CÁLCULO DO IMPOSTO', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)

        # 1ª linha
        lbl, fld = self.inclui_campo_numerico(nome='clc_bip', titulo=u'BASE DE CÁLCULO DO ICMS', conteudo=u'NFe.infNFe.total.ICMSTot.vBC.formato_danfe', top=0.4*cm, left=2.6*cm, width=5.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='clc_vip', titulo=u'VALOR DO ICMS', conteudo=u'NFe.infNFe.total.ICMSTot.vICMS.formato_danfe', top=0.4*cm, left=8*cm, width=5.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='clc_bis', titulo=u'BASE DE CÁLCULO DO ICMS ST', conteudo=u'NFe.infNFe.total.ICMSTot.vBCST.formato_danfe', top=0.4*cm, left=13.4*cm, width=5.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='clc_vis', titulo=u'VALOR DO ICMS ST', conteudo=u'NFe.infNFe.total.ICMSTot.vST.formato_danfe', top=0.4*cm, left=18.8*cm, width=5.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='clc_vpn', titulo=u'VALOR TOTAL DOS PRODUTOS', conteudo=u'NFe.infNFe.total.ICMSTot.vProd.formato_danfe', top=0.4*cm, left=24.2*cm, width=5.2*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        #fld.style = DADO_CAMPO_NUMERICO_NEGRITO

        # 2ª linha
        lbl, fld = self.inclui_campo_numerico(nome='clc_vfrete', titulo=u'VALOR DO FRETE', conteudo=u'NFe.infNFe.total.ICMSTot.vFrete.formato_danfe', top=1*cm, left=2.6*cm, width=4.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='clc_vseguro', titulo=u'VALOR DO SEGURO', conteudo=u'NFe.infNFe.total.ICMSTot.vSeg.formato_danfe', top=1*cm, left=7*cm, width=4.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='clc_vdesconto', titulo=u'DESCONTO', conteudo=u'NFe.infNFe.total.ICMSTot.vDesc.formato_danfe', top=1*cm, left=11.4*cm, width=4.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='clc_voutras', titulo=u'OUTRAS DESPESAS ACESSÓRIAS', conteudo=u'NFe.infNFe.total.ICMSTot.vOutro.formato_danfe', top=1*cm, left=15.8*cm, width=4.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='clc_vipi', titulo=u'VALOR TOTAL DO IPI', conteudo=u'NFe.infNFe.total.ICMSTot.vIPI.formato_danfe', top=1*cm, left=20.2*cm, width=4.4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        
        # Fundo destacado do total da NF
        self.elements.append(Rect(top=1*cm, left=24.6*cm, height=0.6*cm, width=4.8*cm, stroke=False, stroke_width=0, fill=True, fill_color=HexColor(0xd0d0d0)))
        lbl, fld = self.inclui_campo_numerico(nome='clc_vnf', titulo=u'VALOR TOTAL DA NOTA', conteudo=u'NFe.infNFe.total.ICMSTot.vNF.formato_danfe', top=1*cm, left=24.6*cm, width=4.8*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        lbl.style = DESCRITIVO_CAMPO_NEGRITO
        fld.style = DADO_CAMPO_NUMERICO_NEGRITO

        self.height = 1.6*cm


class TransportePaisagem(BandaDANFE):
    def __init__(self):
        super(TransportePaisagem, self).__init__()
        self.elements = []
        self.inclui_descritivo(nome='clc', titulo=u'TRANSPORTADOR/VOLUMES TRANSPORTADOS', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)

        # 1ª linha
        lbl, fld = self.inclui_campo(nome='trn_nome', titulo=u'NOME/RAZÃO SOCIAL', conteudo='NFe.infNFe.transp.transporta.xNome.valor', top=0.4*cm, left=2.6*cm, width=11.5*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='trn_frete', titulo=u'FRETE POR CONTA', conteudo='NFe.frete_formatado', top=0.4*cm, left=14.1*cm, width=2.8*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='trn_antt', titulo=u'CÓDIGO ANTT', conteudo='NFe.infNFe.transp.veicTransp.RNTC.valor', top=0.4*cm, left=16.9*cm, width=3*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='trn_placa', titulo=u'PLACA DO VEÍCULO', conteudo=u'NFe.placa_veiculo_formatada', top=0.4*cm, left=19.9*cm, width=4*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='trn_vei_uf', titulo=u'UF', conteudo='NFe.infNFe.transp.veicTransp.UF.valor', top=0.4*cm, left=23.9*cm, width=1*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='trn_cnpj', titulo=u'CNPJ/CPF', conteudo=u'NFe.cnpj_transportadora_formatado', top=0.4*cm, left=24.9*cm, width=4.5*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        
        # 2ª linha
        lbl, fld = self.inclui_campo(nome='trn_end', titulo=u'ENDEREÇO', conteudo='NFe.infNFe.transp.transporta.xEnder.valor', top=1*cm, left=2.6*cm, width=11.5*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='trn_mun', titulo=u'MUNICÍPIO', conteudo='NFe.infNFe.transp.transporta.xMun.valor', top=1*cm, left=14.1*cm, width=9.8*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='trn_uf', titulo=u'UF', conteudo='NFe.infNFe.transp.transporta.UF.valor', top=1*cm, left=23.9*cm, width=1*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo(nome='trn_ie', titulo=u'INSCRIÇÃO ESTADUAL', conteudo=u'NFe.infNFe.transp.transporta.IE.valor', top=1*cm, left=24.9*cm, width=4.5*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        
        # 3ª linha
        self.elements.append(VolumesPaisagem())

        #self.height = (2.52*cm) - fld.height
        self.height = 1.6*cm
        


class VolumesPaisagem(SubReport):
    def __init__(self):
        super(VolumesPaisagem, self).__init__()
        self.get_queryset = lambda self, parent_object: parent_object.NFe.infNFe.transp.vol or [Vol_200()]

    class band_detail(BandaDANFE):
        def __init__(self):
            super(VolumesPaisagem.band_detail, self).__init__()
            self.elements = []
            lbl, fld = self.inclui_campo_numerico(nome='vol_qtd', titulo=u'QUANTIDADE', conteudo=u'qVol.formato_danfe', top=1.6*cm, left=2.6*cm, width=4*cm, height=0.6*cm)
            fld.padding_top = 0.18*cm
            lbl, fld = self.inclui_campo(nome='vol_esp', titulo=u'ESPÉCIE', conteudo=u'esp.valor', top=1.6*cm, left=6.6*cm, width=4*cm, height=0.6*cm)
            fld.padding_top = 0.18*cm
            lbl, fld = self.inclui_campo(nome='vol_marca', titulo=u'MARCA', conteudo=u'marca.valor', top=1.6*cm, left=10.6*cm, width=4*cm, height=0.6*cm)
            fld.padding_top = 0.18*cm
            lbl, fld = self.inclui_campo(nome='vol_numero', titulo=u'NÚMERO', conteudo=u'nVol.valor', top=1.6*cm, left=14.6*cm, width=5*cm, height=0.6*cm)
            fld.padding_top = 0.18*cm
            lbl, fld = self.inclui_campo_numerico(nome='vol_peso_bruto', titulo=u'PESO BRUTO', conteudo=u'pesoB.formato_danfe', top=1.6*cm, left=19.6*cm, width=5*cm, height=0.6*cm)
            fld.padding_top = 0.18*cm
            lbl, fld = self.inclui_campo_numerico(nome='vol_peso_liquido', titulo=u'PESO LÍQUIDO', conteudo=u'pesoL.formato_danfe', top=1.6*cm, left=24.6*cm, width=4.8*cm, height=0.6*cm, margem_direita=True)
            fld.padding_top = 0.18*cm
            
            self.height = fld.height


class CabProdutoPaisagem(BandaDANFE):
    def __init__(self):
        super(CabProdutoPaisagem, self).__init__()
        self.elements = []
        self.inclui_descritivo(nome='cabprod', titulo=u'DADOS DOS PRODUTOS/SERVIÇOS', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)

        lbl = self.inclui_descritivo_produto(nome='', titulo='CÓDIGO DO PRODUTO', top=0.4*cm, left=2.6*cm, width=3.4*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='DESCRIÇÃO DO PRODUTO/SERVIÇO', top=0.4*cm, left=6*cm, width=5.4*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='CÓDIGO DE BARRAS', top=0.4*cm, left=11.4*cm, width=2.5*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='NCM/SH', top=0.4*cm, left=13.9*cm, width=1.5*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='CST', top=0.4*cm, left=15.4*cm, width=1.2*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='CFOP', top=0.4*cm, left=16.6*cm, width=1.2*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='UNIDADE', top=0.4*cm, left=17.8*cm, width=2*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='QUANTIDADE', top=0.4*cm, left=19.8*cm, width=1.5*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='VALOR UNITÁRIO', top=0.4*cm, left=21.3*cm, width=1.5*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='VALOR TOTAL', top=0.4*cm, left=22.8*cm, width=1.5*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='BASE CÁLC. DO ICMS', top=0.4*cm, left=24.3*cm, width=1.3*cm)
        lbl = self.inclui_descritivo_produto(nome='', titulo='VALOR DO ICMS', top=0.4*cm, left=25.6*cm, width=1.2*cm)
        lbl = self.inclui_descritivo_produto(nome='', titulo='VALOR DO IPI', top=0.4*cm, left=26.8*cm, width=1.2*cm)
        lbl.padding_top = 0.15*cm
        lbl = self.inclui_descritivo_produto(nome='', titulo='ALÍQUOTAS', top=0.4*cm, left=28*cm, width=1.4*cm, height=0.26*cm, margem_direita=True)
        lbl = self.inclui_descritivo_produto(nome='', titulo='ICMS', top=0.66*cm, left=28*cm, width=0.7*cm, height=0.26*cm)
        lbl = self.inclui_descritivo_produto(nome='', titulo='IPI', top=0.66*cm, left=28.7*cm, width=0.7*cm, height=0.26*cm, margem_direita=True)

        self.height = 0.94*cm
        

class DetProdutoPaisagem(BandaDANFE):
    def __init__(self):
        super(DetProdutoPaisagem, self).__init__()
        self.elements = []

        #
        # Modelagem do tamanho dos campos
        #
        txt = self.inclui_campo_produto(nome=u'prod_codigo', conteudo=u'prod.cProd.valor', top=0*cm, left=2.6*cm, width=3.4*cm)
        txt = self.inclui_campo_produto(nome=u'prod_descricaco', conteudo=u'descricao_produto_formatada', top=0*cm, left=6*cm, width=5.4*cm)
        txt = self.inclui_campo_centralizado_produto(nome=u'prod_cean', conteudo=u'prod.cEAN.valor', top=0*cm, left=11.4*cm, width=2.5*cm)
        txt = self.inclui_campo_centralizado_produto(nome=u'prod_ncm', conteudo=u'prod.NCM.valor', top=0*cm, left=13.9*cm, width=1.5*cm)
        txt = self.inclui_campo_centralizado_produto(nome='prod_cst', conteudo='cst_formatado', top=0*cm, left=15.4*cm, width=1.2*cm)
        txt = self.inclui_campo_centralizado_produto(nome=u'prod_cfop', conteudo=u'prod.CFOP.valor', top=0*cm, left=16.6*cm, width=1.2*cm)
        txt = self.inclui_campo_centralizado_produto(nome=u'prod_unidade', conteudo=u'prod.uCom.valor', top=0*cm, left=17.8*cm, width=2*cm)
        txt = self.inclui_campo_numerico_produto(nome='prod_quantidade', conteudo=u'prod.qCom.formato_danfe', top=0*cm, left=19.8*cm, width=1.5*cm)
        txt = self.inclui_campo_numerico_produto(nome='vr_unitario', conteudo=u'prod.vUnCom.formato_danfe', top=0*cm, left=21.3*cm, width=1.5*cm)
        txt = self.inclui_campo_numerico_produto(nome='', conteudo='prod.vProd.formato_danfe', top=0*cm, left=22.8*cm, width=1.5*cm)
        txt = self.inclui_campo_numerico_produto(nome='', conteudo='imposto.ICMS.vBC.formato_danfe', top=0*cm, left=24.3*cm, width=1.3*cm)
        txt = self.inclui_campo_numerico_produto(nome='', conteudo='imposto.ICMS.vICMS.formato_danfe', top=0*cm, left=25.6*cm, width=1.2*cm)
        txt = self.inclui_campo_numerico_produto(nome='', conteudo='imposto.IPI.vIPI.formato_danfe', top=0*cm, left=26.8*cm, width=1.2*cm)
        txt = self.inclui_campo_numerico_produto(nome='', conteudo='imposto.ICMS.pICMS.formato_danfe', top=0*cm, left=28*cm, width=0.7*cm)
        txt = self.inclui_campo_numerico_produto(nome='', conteudo='imposto.IPI.pIPI.formato_danfe', top=0*cm, left=28.7*cm, width=0.7*cm, margem_direita=True)

        self.auto_expand_height = True


class ISSPaisagem(BandaDANFE):
    def __init__(self):
        super(ISSPaisagem, self).__init__()
        self.elements = []

        # Cálculo do ISS
        self.inclui_descritivo(nome='iss', titulo=u'CÁLCULO DO ISSQN', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)
        
        lbl, fld = self.inclui_campo(nome='iss_im', titulo=u'INSCRIÇÃO MUNICIPAL', conteudo=u'NFe.infNFe.ide.cMunFG.valor', top=0.4*cm, left=2.6*cm, width=6.7*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='iss_vr_servico', titulo=u'VALOR TOTAL DOS SERVIÇOS', conteudo=u'NFe.infNFe.total.ISSQNTot.vServ.formato_danfe', top=0.4*cm, left=9.3*cm, width=6.7*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='iss_bc', titulo=u'BASE DE CÁLCULO DO ISSQN', conteudo=u'NFe.infNFe.total.ISSQNTot.vBC.formato_danfe', top=0.4*cm, left=16*cm, width=6.7*cm, height=0.6*cm)
        fld.padding_top = 0.18*cm
        lbl, fld = self.inclui_campo_numerico(nome='iss_vr_iss', titulo=u'VALOR DO ISSQN', conteudo=u'NFe.infNFe.total.ISSQNTot.vISS.formato_danfe', top=0.4*cm, left=22.7*cm, width=6.7*cm, height=0.6*cm, margem_direita=True)
        fld.padding_top = 0.18*cm
        
        # Dados adicionais
        self.inclui_descritivo(nome='clc', titulo=u'DADOS ADICIONAIS', top=1*cm, left=2.6*cm, width=26.8*cm)
        
        lbl, txt = self.inclui_campo(nome='', titulo='INFORMAÇÕES COMPLEMENTARES', conteudo='NFe.dados_adicionais', top=1.42*cm, left=2.6*cm, width=19.1*cm, height=2.8*cm)
        txt.style = DADO_COMPLEMENTAR
        self.inclui_texto(nome='', titulo='RESERVADO AO FISCO', texto='', top=1.42*cm, left=21.7*cm, width=7.7*cm, height=2.8*cm, margem_direita=True)

        fld = DANFEPaisagem.ObsImpressao()
        fld.top = 4.2*cm
        self.elements.append(fld)

        self.height = 4.2*cm


class DadosAdicionaisPaisagem(BandaDANFE):
    def __init__(self):
        super(DadosAdicionaisPaisagem, self).__init__()
        self.elements = []
        self.inclui_descritivo(nome='clc', titulo=u'DADOS ADICIONAIS', top=0*cm, left=2.6*cm, width=26.8*cm, height=0.4*cm)

        lbl, txt = self.inclui_campo(nome='', titulo='INFORMAÇÕES COMPLEMENTARES', conteudo='NFe.dados_adicionais', top=0.4*cm, left=2.6*cm, width=19.1*cm, height=3.2*cm)
        txt.style = DADO_COMPLEMENTAR
        self.inclui_texto(nome='', titulo='RESERVADO AO FISCO', texto='', top=0.4*cm, left=21.7*cm, width=7.7*cm, height=3.2*cm, margem_direita=True)

        fld = DANFEPaisagem.ObsImpressao()
        fld.top = 3.6*cm
        self.elements.append(fld)

        self.height = 3.6*cm
        

class RodapeFinalPaisagem(BandaDANFE):
    def __init__(self):
        super(RodapeFinalPaisagem, self).__init__()
        self.elements = []
        self.height = 1.0*cm

        # Obs de impressão
        fld = DANFEPaisagem.ObsImpressao()
        fld.top = 1.0*cm
        self.elements.append(fld)
