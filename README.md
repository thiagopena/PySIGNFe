PySIGNFe
============

Biblioteca de interface com o webservice de Nota Fiscal Eletronica da SEFAZ, oficializada pelo Ministerio da Fazendo do Governo do Brasil.

Desenvolvida em Python 3 no Windows, testada em Python 3 e 2 no GNU/Linux e Windows.

Implementações
----------
* Geração do XML, assinatura, emissão e armazenamento de NF-e, NFC-e, NFS-e e CT-e.
* Impressão de DANFE (Retrato e Paisagem)
* Geração de DANFE NFC-e

Avisos
----------
* Este projeto NÃO foi homologado para todos os estados.
* Antes de começar, faça uma leitura atenta dos manuais divulgados pelo [SEFAZ](http://www.nfe.fazenda.gov.br/portal/principal.aspx)
* O módulo de NFS-e foi implementado apenas para o Município de Belo Horizonte, pretendo implementar em breve os formatos BETHA e GINFES.
* Por enquanto só podem ser utilizados certificados no formato A1.
* **TESTE ANTES DE EMITIR QUALQUER NOTA EM AMBIENTE DE PRODUÇÃO**

Dependências
------------
* OpenSSL
* pytz
* lxml
* signxml
* cryptography
* reportlab
* six
* [geraldo](https://github.com/thiagopena/geraldo)
    * Utilizar o fork do geraldo para gerar DANFE.

Instalação:
-----------
```bash
python setup.py install
pip install -r requirements.txt
```

Créditos
----------
Esta biblioteca foi baseada nos projetos: 
* [Recursos-NFE-em-Python](https://github.com/marcydoty/Recursos-NFE-em-Python)
* [PySPED](https://github.com/aricaldeira/PySPED)


License LGPLv2.1
-------

> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU Lesser General Public License as published by
> the Free Software Foundation, either version 2.1 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU Lesser General Public
> License along with this library; if not, write to the Free Software
> Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.