# -*- coding: utf-8 -*-

from OpenSSL import crypto
from datetime import datetime
from pysignfe.xml_sped import *
import lxml


class Certificado(object):
    def __init__(self):
        self.arquivo    = u''
        self.senha      = u''
        self.chave      = u''
        self.certificado = u''
        self.emissor     = {}
        self.proprietario = {}
        self.data_inicio_validade = None
        self.data_fim_validade    = None
        self._doc_xml    = None
        self.cert_str=''
        self.key_str=''
        
    def prepara_certificado_arquivo_pfx(self):
        self.chave=self.key_str
        self.prepara_certificado_txt(self.cert_str)    
    
    def prepara_certificado_txt(self, cert_txt):
        #
        # Para dar certo a leitura pelo xmlsec, temos que separar o certificado
        # em linhas de 64 caracteres de extensão...
        #
        cert_txt = cert_txt.replace(u'\n', u'')
        cert_txt = cert_txt.replace(u'-----BEGIN CERTIFICATE-----', u'')
        cert_txt = cert_txt.replace(u'-----END CERTIFICATE-----', u'')

        linhas_certificado = [u'-----BEGIN CERTIFICATE-----\n']
        for i in range(0, len(cert_txt), 64):
            linhas_certificado.append(cert_txt[i:i+64] + '\n')
        linhas_certificado.append(u'-----END CERTIFICATE-----\n')

        self.certificado = u''.join(linhas_certificado)

        cert_openssl = crypto.load_certificate(crypto.FILETYPE_PEM, self.certificado)

        self.emissor = dict(cert_openssl.get_issuer().get_components())
        self.proprietario = dict(cert_openssl.get_subject().get_components())

        self.data_inicio_validade = datetime.strptime(cert_openssl.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
        self.data_fim_validade    = datetime.strptime(cert_openssl.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
    
    def assina_xmlnfe(self, doc):
        if not isinstance(doc, XMLNFe):
            raise ValueError('O documento nao e do tipo esperado: XMLNFe')

        # Realiza a assinatura
        xml = self.assina_xml(doc.xml)

        # Devolve os valores para a instância doc
        doc.Signature.xml = xml
        
    def assina_arquivo(self, doc):
        xml = open(doc, 'r').read()
        xml = self.assina_xml(xml)
        return xml
        
    def _prepara_doc_xml(self, xml):
        #
        # Importantíssimo colocar o encode, pois do contário não é possível
        # assinar caso o xml tenha letras acentuadas
        #
        xml = tira_abertura(xml)
        xml = ABERTURA + xml
        #
        # Remove todos os \n
        #
        xml = xml.replace(u'\n', u'')
        
        return xml
        
    def _finaliza_xml(self, xml):
        
        xml = xml.replace(u'\n', u'')
        #xml = xml.replace(u'ds:',u'').replace(u':ds',u'')
        return xml
        
    def _ler_chave_acesso(self, xml):
        #Le a chave de acesso para a assinatura e retira a TAG Signature do documento
        chave_de_acesso = None
        
        #CTe
        if NAMESPACE_CTE in str(xml):
            for child in xml.iter():
                if u'infCte' in child.tag:
                    chave_de_acesso = child.get('Id')
                elif u'infInut' in child.tag:
                    chave_de_acesso = child.get('Id')
                elif u'infEvento' in child.tag:
                    chave_de_acesso = child.get('Id')
        #NFe/NFSe
        else:
            for child in xml.iter():
                #NFe
                if "infNFe" in child.tag:
                    chave_de_acesso = child.get('Id')
                elif u'infCanc' in child.tag:
                    chave_de_acesso = child.get('Id')
                elif u'infEvento' in child.tag:
                    chave_de_acesso = child.get('Id')
                elif u'infInut' in child.tag:
                    chave_de_acesso = child.get('Id')
                #NFSe
                elif u'LoteRps' in child.tag:
                    chave_de_acesso = child.get('Id')
                elif u'InfRps' in child.tag:
                    chave_de_acesso = child.get('Id')
                elif u'InfPedidoCancelamento' in child.tag:
                    chave_de_acesso = child.get('Id')
                #if "Signature" in child.tag:
                    #Remover TAG Signature, se tiver
                    #xml.remove(child)
                #    pass
        
        return chave_de_acesso
        
    def assina_xml(self, xml):
        ##Modificado para utilizar o signxml ao inves do libxml2 e xmlsec
        from signxml import XMLSigner
        from signxml import methods

        xml = self._prepara_doc_xml(xml)
        doc_xml = lxml.etree.fromstring(xml.encode('utf-8'))
        
        #buscando chave de acesso no documento e retiranto TAG Signature
        chave_de_acesso = self._ler_chave_acesso(doc_xml)
        if chave_de_acesso is None:
            raise ValueError('Nao foi possivel encontrar a Tag para a assinatura.')
        
        #String para bytes para a leitura no signxml
        chave = self.chave.encode('utf-8')
        certificado = self.certificado.encode('utf-8')
        
        signer = XMLSigner(method=methods.enveloped, signature_algorithm='rsa-sha1', digest_algorithm='sha1', c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315')
        
        #Retirar os prefixos ds: da assinatura
        ns = {}
        ns[None] = signer.namespaces['ds']
        signer.namespaces = ns
        
        #Assina o documento
        signed_doc = signer.sign(doc_xml, key=chave, cert=certificado, reference_uri='#{0}'.format(chave_de_acesso))
        
        #Selecionar apenas a tag Signature do documento.
        signature_tag = None
        for child in signed_doc:
            if 'Signature' in child.tag:
                signature_tag = child
        if signature_tag is None:
            raise("Assinatura nao encontrada.")
            
        signature_tag = lxml.etree.tostring(signature_tag).decode('utf-8')
                
        signature_tag = self._finaliza_xml(signature_tag)
                
        return signature_tag

    def verifica_assinatura_xmlnfe(self, doc):
        if not isinstance(doc, XMLNFe):
            raise ValueError('O documento nao e do tipo esperado: XMLNFe')

        return self.verifica_assinatura_xml(doc.xml)

    def verifica_assinatura_arquivo(self, doc):
        xml = open(doc, 'r').read()
        return self.verifica_assinatura_xml(xml)

    def verifica_assinatura_xml(self, xml):
        pass
        
