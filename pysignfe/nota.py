# -*- coding: utf-8 -*-

from OpenSSL import crypto
from pysignfe.xml_sped.certificado import Certificado

#Classe definida para metodos e parametros de NFS-e's e NF-e's

class NotaFiscal(object):
    
    def extrair_certificado_a1(self, arquivo, senha):
        '''
        Extrai o conteúdo do certificado A1
        @param arquivo:arquivo binário do certificado
        @param senha: senha do certificado.
        @return: dicionário com a string do certificado, chave privada, emissor, proprietario, data_inicio_validade e
        data_final_validade.
        '''
        
        conteudo_pkcs12 = crypto.load_pkcs12(arquivo, senha)
        key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, conteudo_pkcs12.get_privatekey())
        cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, conteudo_pkcs12.get_certificate())
        
        certificado = Certificado()
        certificado.prepara_certificado_txt(cert_str.decode('utf-8'))
        
        vals = {'cert': cert_str.decode('utf-8'),
                'key': key_str.decode('utf-8'),
                'emissor': certificado.emissor.get('OU'),
                'proprietario': certificado.proprietario.get('CN'),
                'data_inicio_validade': certificado.data_inicio_validade,
                'data_final_validade': certificado.data_fim_validade,
        }
        return vals