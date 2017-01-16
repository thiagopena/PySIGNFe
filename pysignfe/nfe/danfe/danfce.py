# -*- coding: utf-8 -*-


from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from geraldo import Report, ReportBand, SubReport, ReportGroup
from geraldo import Line, Rect, Image
from geraldo.barcodes import BarCode

from pysignfe.relato_sped import *


class DANFCE(Report):
    def __init__(self, *args, **kargs):
        super(DANFCE, self).__init__(*args, **kargs)
        self.title = 'Documento Auxiliar da Nota Fiscal de Consumidor Eletrônica'
        self.print_if_empty = True
        self.additional_fonts = FONTES_ADICIONAIS

        self.page_size = (8*cm, 15.0*cm)
        self.margin_top = 0.2*cm
        self.margin_bottom = 0.2*cm
        self.margin_left = 0.2*cm
        self.margin_right = 0.2*cm
        
        # Bandas e observações
        self.cabecalho      = Cabecalho()
        self.mensagem_fiscal_topo = MensagemFiscalTopo()
        self.det_totais     = DetTotais()
        self.det_produtos   = DetProdutos()
        self.det_pagamento  = DetPagamento()
        self.consulta_chave = ConsultaChave()
        self.id_consumidor  = IdConsumidor()
        self.ender_consumidor = EnderecoConsumidor()
        self.id_nfce        = IdNFCe()
        self.mensagem_fiscal_base = MensagemFiscalBase()
        self.qrcode_danfe   = QRCodeDanfe()
        self.tributos_totais = TributosTotais()
        
        self.inf_produtos   = InfoProdutos()
        self.inf_totais     = InfoTotais()
        self.inf_pagamento  = InfoPagamento()
        
        self.acrescimos = Acrescimos()
        self.descontos  = Descontos()
        
    def format_date(self, data, formato):
        return  data.strftime(formato)
        
    def do_on_new_page(self, page, page_number, generator):
        pass
    
    ##Adaptar tamanha pagina com o conteudo
    def set_report_height(self, n_produtos, n_pag):
        #Cabecalho
        fit_height = self.band_page_header.height
        #band_page_header.child_bands (MensagemFiscalTopo, MensagemFiscalBase, DetProdutos(0), DetTotais(0), DetPagamento(0), 
        #                              ConsultaChave, IdConsumidor, EnderecoConsumidor, IdNFCe, QRCodeDanfe, TributosTotais )
        for i in self.band_page_header.child_bands:
            fit_height += i.height
        
        ##Somar produtos: band_header + band_detail * (n_produtos)
        for el in self.det_produtos.elements:
            fit_height += el.band_detail.height * n_produtos
            fit_height += el.band_header.height
        
        ##Somar totais: band_header + band_footer
        for el in self.det_totais.elements:
            fit_height += el.band_header.height
            fit_height += el.band_footer.height
        
        ##Somar pagamentos: band_header + (band_detail * (n_pag)) + band_footer
        for el in self.det_pagamento.elements:
            fit_height += el.band_header.height
            fit_height += el.band_detail.height * n_pag
            fit_height += el.band_footer.height
        
        #Somar margens
        fit_height += self.margin_top + self.margin_bottom + 10
        self.page_size = (8*cm, fit_height)
        
class Cabecalho(BandaDANFE):
    def __init__(self):
        super(Cabecalho, self).__init__()
        self.elements = []
        
        fld = self.inclui_campo_sem_borda(nome='razao_social', conteudo=u'NFe.razao_social_formatado', top=0*cm, left=0.3*cm, width=7.6*cm, height=0.5*cm)
        fld.style = {'fontName': FONTE_NFCE_NEGRITO, 'fontSize': FONTE_TAMANHO_9}
        
        fld = self.inclui_campo_sem_borda(nome='emitente', conteudo=u'NFe.cnpj_com_label_formatado', top=0.5*cm, left=0.3*cm, width=7.6*cm, height=0.5*cm)
        fld.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7}
        
        fld = self.inclui_campo_sem_borda(nome='endereco_emitente', conteudo=u'NFe.endereco_emitente_nfce_formatado', top=1*cm, left=0.3*cm, width=7.6*cm, height=0.5*cm)
        fld.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
        
        txt = self.inclui_texto_sem_borda(nome='danfe_ext', texto=u'Documento Auxiliar da Nota Fiscal de Consumidor Eletrônica', top=1.6*cm, left=0*cm, width=7.6*cm, height=1*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_9, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_9}
        
        self.height = 2.6*cm
        
        
class DetProdutos(BandaDANFE):
    def __init__(self):
        super(DetProdutos, self).__init__()
        self.elements = []

        self.height = 0*cm
        #self.auto_expand_height = True
        
              
class InfoProdutos(SubReport):
    def __init__(self):
        super(InfoProdutos, self).__init__()
        self.get_queryset = lambda self, parent_object: parent_object.NFe.infNFe.det or []

    class band_header(BandaDANFE):
        def __init__(self):
            super(InfoProdutos.band_header, self).__init__()
            self.elements = []
            
            txt = self.inclui_texto_sem_borda(nome='', texto='Código', top=0*cm, left=0*cm, width=1.9*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_texto_sem_borda(nome='', texto='Descrição', top=0*cm, left=1.9*cm, width=2.1*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_texto_sem_borda(nome='', texto='Qtde', top=0*cm, left=4*cm, width=1*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_texto_sem_borda(nome='', texto='UN', top=0*cm, left=5*cm, width=0.7*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_texto_sem_borda(nome='', texto='V Un.', top=0*cm, left=5.7*cm, width=0.95*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_texto_sem_borda(nome='', texto='Total', top=0*cm, left=6.65*cm, width=0.95*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            
            self.elements.append(Line(top=0.1*cm, bottom=0.1*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
            self.elements.append(Line(top=0.51*cm, bottom=0.51*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))

            self.height = 0.51*cm
            
    class band_detail(BandaDANFE):
        def __init__(self):
            super(InfoProdutos.band_detail, self).__init__()
            self.elements = []
            self.display_inline = True
            self.width = 7.6*cm
            
            txt = self.inclui_campo_sem_borda(nome=u'prod_codigo', conteudo=u'prod.cProd.valor', top=0*cm, left=0*cm, width=1.9*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'leading': FONTE_TAMANHO_5}
            txt = self.inclui_campo_sem_borda(nome=u'prod_descricaco', conteudo=u'prod.xProd.valor', top=0*cm, left=1.9*cm, width=2.1*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'leading': FONTE_TAMANHO_5}
            txt = self.inclui_campo_sem_borda(nome='prod_quantidade', conteudo=u'prod.qCom.formato_danfe_nfce', top=0*cm, left=4*cm, width=1*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'leading': FONTE_TAMANHO_5}
            txt = self.inclui_campo_sem_borda(nome=u'prod_unidade', conteudo=u'prod.uCom.valor', top=0*cm, left=5*cm, width=0.7*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'leading': FONTE_TAMANHO_5}
            txt = self.inclui_campo_sem_borda(nome='vr_unitario', conteudo=u'prod.vUnCom.formato_danfe_nfce', top=0*cm, left=5.7*cm, width=0.95*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'leading': FONTE_TAMANHO_5}
            txt = self.inclui_campo_sem_borda(nome='', conteudo='prod.vProd.formato_danfe', top=0*cm, left=6.65*cm, width=0.95*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'leading': FONTE_TAMANHO_5}

            #self.auto_expand_height = True
            self.height = 0.5*cm
        
        def set_band_height(self, field_size):
            ##14 caracteres por linha
            n_lines = field_size/14
            ##0.22*cm por linha
            self.height = 0.2*cm*(n_lines+1)
            
                        
class DetTotais(BandaDANFE):
    def __init__(self):
        super(DetTotais, self).__init__()
        self.elements = []

        self.height = 0*cm
        
                        
class InfoTotais(SubReport):
    def __init__(self):
        super(InfoTotais, self).__init__()
        self.get_queryset = lambda self, parent_object: parent_object.NFe.infNFe.det or []

    class band_header(BandaDANFE):
        def __init__(self):
            super(InfoTotais.band_header, self).__init__()
            self.elements = []
            
            self.elements.append(Line(top=0.1*cm, bottom=0.1*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
            
            txt = self.inclui_texto_sem_borda(nome='', texto='Qtde. Total de Itens', top=0.1*cm, left=0*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_campo_sem_borda(nome=u'qtd_itens', conteudo=u'NFe.quantidade_itens', top=0.1*cm, left=3.8*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7, 'alignment': TA_RIGHT}
            
            txt = self.inclui_texto_sem_borda(nome='', texto='Valor Total R$', top=0.6*cm, left=0*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_campo_sem_borda(nome=u'valor_total', conteudo=u'NFe.valor_total_nota', top=0.6*cm, left=3.8*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7, 'alignment': TA_RIGHT}
            
            #self.auto_expand_height = True
            self.height = 1.1*cm
            
        def add_height(self):
            self.height += 0.5*cm

    class band_detail(BandaDANFE):
        def __init__(self):
            super(InfoTotais.band_detail, self).__init__()
            self.elements = []
            
            self.height = 0*cm
    
    class band_footer(BandaDANFE):
        def __init__(self):
            super(InfoTotais.band_footer, self).__init__()
            self.elements = []
            
            txt = self.inclui_texto_sem_borda(nome='', texto='Valor a Pagar R$', top=0*cm, left=0*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_campo_sem_borda(nome=u'qtd_itens', conteudo=u'NFe.valor_a_pagar_formatado', top=0*cm, left=3.8*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7, 'alignment': TA_RIGHT}
            
            self.height = 0.5*cm
            
            
class Acrescimos(SubReport):
    def __init__(self):
        super(Acrescimos, self).__init__()
        self.get_queryset = lambda self, parent_object: parent_object.NFe.infNFe.det or []

    class band_header(BandaDANFE):
        def __init__(self):
            super(Acrescimos.band_header, self).__init__()
            self.elements = []
            
            txt = self.inclui_texto_sem_borda(nome='', texto='Acréscimo R$', top=1.1*cm, left=0*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_campo_sem_borda(nome=u'total_acrescimos', conteudo=u'NFe.total_acrescimos', top=1.1*cm, left=3.8*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7, 'alignment': TA_RIGHT}
            
            self.height = 0.5*cm
            
            
class Descontos(SubReport):
    def __init__(self):
        super(Descontos, self).__init__()
        self.get_queryset = lambda self, parent_object: parent_object.NFe.infNFe.det or []

    class band_header(BandaDANFE):
        def __init__(self):
            super(Descontos.band_header, self).__init__()
            self.elements = []
            
            txt = self.inclui_texto_sem_borda(nome='', texto='Desconto R$', top=1.1*cm, left=0*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_campo_sem_borda(nome=u'total_desconto', conteudo=u'NFe.total_desconto', top=1.1*cm, left=3.8*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7, 'alignment': TA_RIGHT}
            
            self.height = 0.5*cm
        
        def set_top(self):
            for el in self.elements:
                el.top = 1.6*cm
            
class DetPagamento(BandaDANFE):
    def __init__(self):
        super(DetPagamento, self).__init__()
        self.elements = []
        
        self.height = 0*cm
        #self.auto_expand_height = True
            
            
class InfoPagamento(SubReport):
    def __init__(self):
        super(InfoPagamento, self).__init__()
        self.get_queryset = lambda self, parent_object: parent_object.NFe.infNFe.pag or []

    class band_header(BandaDANFE):
        def __init__(self):
            super(InfoPagamento.band_header, self).__init__()
            self.elements = []
            
            txt = self.inclui_texto_sem_borda(nome='', texto='FORMA DE PAGAMENTO', top=0*cm, left=0*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE_NEGRITO, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            
            txt = self.inclui_texto_sem_borda(nome='', texto='VALOR PAGO', top=0*cm, left=3.8*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE_NEGRITO, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7, 'alignment': TA_RIGHT}
            
            self.height = 0.5*cm
            

    class band_detail(BandaDANFE):
        def __init__(self):
            super(InfoPagamento.band_detail, self).__init__()
            self.elements = []
            
            txt = self.inclui_campo_sem_borda(nome=u'forma_pagamento', conteudo=u'forma_pagamento_danfe', top=0*cm, left=0*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7, 'alignment': TA_LEFT}
            txt = self.inclui_campo_sem_borda(nome=u'valor_pagamento', conteudo=u'valor_pagamento_danfe', top=0*cm, left=3.8*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7, 'alignment': TA_RIGHT}
            
            #self.auto_expand_height = True
            self.height = 0.5*cm
            
    class band_footer(BandaDANFE):
        def __init__(self):
            super(InfoPagamento.band_footer, self).__init__()
            self.elements = []
            
            txt = self.inclui_texto_sem_borda(nome='', texto='Troco', top=0*cm, left=0*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading': FONTE_TAMANHO_7}
            txt = self.inclui_campo_sem_borda(nome=u'troco', conteudo=u'NFe.troco_danfe', top=0*cm, left=3.8*cm, width=3.8*cm)
            txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'leading':FONTE_TAMANHO_7, 'alignment': TA_RIGHT}
            
            self.height = 0.5*cm
            
            
class ConsultaChave(BandaDANFE):
    def __init__(self):
        super(ConsultaChave, self).__init__()
        self.elements = []
        
        self.elements.append(Line(top=0.1*cm, bottom=0.1*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
        
        txt = self.inclui_texto_sem_borda(nome='consulta_chave_texto', texto=u'Consulte pela Chave de Acesso em', top=0.1*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE_NEGRITO, 'fontSize': FONTE_TAMANHO_6, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_6}
        
        txt = self.inclui_campo_sem_borda(nome='endereco_consulta_chave', conteudo=u'NFe.endereco_consulta_chave_nfce', top=0.5*cm, left=0*cm, width=7.6*cm, height=0.4*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_5, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_5}
        
        txt = self.inclui_campo_sem_borda(nome='chave_formatada', conteudo=u'NFe.chave_formatada', top=1*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_6}
        
        self.height = 1.5*cm
        

class IdConsumidor(BandaDANFE):
    def __init__(self):
        super(IdConsumidor, self).__init__()
        self.elements = []
        
        self.elements.append(Line(top=0.1*cm, bottom=0.1*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
        
    def consumidor_identificado(self):
        txt = self.inclui_campo_sem_borda(nome='id_consumidor', conteudo=u'NFe.id_consumidor', top=0.1*cm, left=0*cm, width=7.6*cm, height=0.4*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        
        self.height = 0.5*cm
    
    def consumidor_nao_identificado(self):
        txt = self.inclui_texto_sem_borda(nome='consumidor_ni', texto=u'CONSUMIDOR NÃO IDENTIFICADO', top=0.1*cm, left=0*cm, width=7.6*cm, height=0.4*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        
        self.height = 0.5*cm
        
class EnderecoConsumidor(BandaDANFE):
    def __init__(self):
        super(EnderecoConsumidor, self).__init__()
        self.elements = []
        
        txt = self.inclui_campo_sem_borda(nome='ender_consumidor', conteudo=u'NFe.ender_consumidor', top=0*cm, left=0*cm, width=7.6*cm, height=0.4*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_6}
        
        self.height = 0.4*cm
        
class IdNFCe(BandaDANFE):
    def __init__(self):
        super(IdNFCe, self).__init__()
        self.elements = []
        
        self.elements.append(Line(top=0.1*cm, bottom=0.1*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
        
        txt = self.inclui_campo_sem_borda(nome='id_nfce', conteudo=u'NFe.id_nfce', top=0.1*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE_NEGRITO, 'fontSize': FONTE_TAMANHO_7, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        
        txt = self.inclui_campo_sem_borda(nome='id_nfce', conteudo=u'NFe.data_emissao_danfe_nfce', top=0.5*cm, left=0*cm, width=7.6*cm, height=0.4*cm)
        txt.style = {'fontName': FONTE_NFCE_NEGRITO, 'fontSize': FONTE_TAMANHO_6, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_6}
        
        self.height = 0.9*cm
    
    def campo_variavel_protocolo(self):
        txt = self.inclui_campo_sem_borda(nome='prot_aut', conteudo=u'protNFe.protocolo_formatado_nfce', top=1*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE_NEGRITO, 'fontSize': FONTE_TAMANHO_7, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        
        txt = self.inclui_campo_sem_borda(nome='data_aut', conteudo=u'protNFe.data_autorizacao_nfce', top=1.5*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE_NEGRITO, 'fontSize': FONTE_TAMANHO_7, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        
        self.height = 2*cm
        
class MensagemFiscalTopo(BandaDANFE):
    def __init__(self):
        super(MensagemFiscalTopo, self).__init__()
        self.elements = []
        
        self.height = 0*cm
    
    def campo_variavel_contingencia(self):
        self.elements.append(Line(top=0.1*cm, bottom=0.1*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
        
        txt = self.inclui_texto_sem_borda(nome='msg_contingencia', texto=u'EMITIDA EM CONTINGÊNCIA', top=0*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_8, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_8}
        
        txt = self.inclui_texto_sem_borda(nome='msg_contingencia', texto=u'Pendente de autorização', top=0.4*cm, left=0*cm, width=7.6*cm, height=0.4*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        
        #for l in [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]:
        for l in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            self.elements.append(Line(top=l*cm, bottom=l*cm, left=0*cm, right=1.7*cm, stroke_width=0.1))
            self.elements.append(Line(top=l*cm, bottom=l*cm, left=5.9*cm, right=7.6*cm, stroke_width=0.1))
        
        self.height = 0.9*cm
        
    def campo_variavel_homologacao(self):
        self.elements.append(Line(top=0.1*cm, bottom=0.1*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
        txt = self.inclui_texto_sem_borda(nome='amb_2', texto=u'EMITIDA EM AMBIENTE DE HOMOLOGAÇÃO – SEM VALOR FISCAL', top=0*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_8, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        txt.padding_top = 0.3*cm
        
        self.height = 1*cm
        
        
class MensagemFiscalBase(BandaDANFE):
    def __init__(self):
        super(MensagemFiscalBase, self).__init__()
        self.elements = []
        
        self.height = 0*cm
    
    def campo_variavel_contingencia(self):
        
        txt = self.inclui_texto_sem_borda(nome='msg_contingencia', texto=u'EMITIDA EM CONTINGÊNCIA', top=0.1*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_8, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_8}
        
        txt = self.inclui_texto_sem_borda(nome='msg_contingencia', texto=u'Pendente de autorização', top=0.5*cm, left=0*cm, width=7.6*cm, height=0.4*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_7, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        
        self.height = 0.9*cm
        
    def campo_variavel_homologacao(self):
        
        txt = self.inclui_texto_sem_borda(nome='amb_2', texto=u'EMITIDA EM AMBIENTE DE HOMOLOGAÇÃO – SEM VALOR FISCAL', top=0.1*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_8, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_7}
        txt.padding_top = 0.25*cm
        self.height = 1*cm
        
        
class QRCodeDanfe(BandaDANFE):
    def __init__(self):
        super(QRCodeDanfe, self).__init__()
        self.elements = []
        
        self.height = 0*cm
    
    def gera_img_qrcode(self):
        
        ##Aprox. 37mmx37mm
        self.elements.append(BarCode(type=u'QR', attribute_name=u'NFe.infNFeSupl.qrCode.valor', top=0.1*cm, left=1.3*cm, width=5*cm, height=5*cm, border=0.5*cm, qr_level='M'))
        
        self.height = 5.2*cm
        
class TributosTotais(BandaDANFE):
    def __init__(self):
        super(TributosTotais, self).__init__()
        self.elements = []
        
        self.elements.append(Line(top=0.1*cm, bottom=0.1*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
        
        txt = self.inclui_campo_sem_borda(nome='trib_tot', conteudo=u'NFe.tributos_totais_nfce', top=0*cm, left=0*cm, width=7.6*cm, height=0.5*cm)
        txt.style = {'fontName': FONTE_NFCE, 'fontSize': FONTE_TAMANHO_6, 'alignment': TA_CENTER, 'leading': FONTE_TAMANHO_6}
        
        self.elements.append(Line(top=0.6*cm, bottom=0.6*cm, left=0*cm, right=7.6*cm, stroke_width=0.3, dash=(1,1)))
        
        self.height = 0.6*cm
    