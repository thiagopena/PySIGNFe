from setuptools import setup, find_packages
import os

setup(
    name="PySIGNFe",
    version="0.1.0",
    description=("Biblioteca para implementacao de notas fiscais eletronicas"),
    license="LGPL",
    keywords="NF-e NFS-e CT-e",
    classifiers=["Development Status :: 1 - Planning",
                 "Topic :: Office/Business :: Financial",
                 "Programming Language :: Python",
                 "License :: LGPL",
                 "Operating System :: OS Independent",],
    packages=[package for package in find_packages() if package.startswith('pysignfe')],
    package_data={'pysignfe': ['nfe/danfe/fonts/*', 'nfe/manifestacao_destinatario/schema/pl/*', 'relato_sped/fonts/*'],
                  'pysignfe.nfe.manual_401':  [os.path.join('schema', 'pl_006j', '*'),
                                               os.path.join('schema', 'pl_006r', '*'),
                                               os.path.join('schema', 'pl_006s', '*')],
                  'pysignfe.nfe.manual_500':  [os.path.join('schema', 'pl_008e', '*')],
                  'pysignfe.nfe.manual_600':  [os.path.join('schema', 'pl_008i2', '*')],
                  'pysignfe.xml_sped':  [os.path.join('schema', '*')],
                  'pysignfe.nfse': ['certificados/*'],
                  'pysignfe.nfse.bhiss': [os.path.join('v10', 'schema', '*')]
    }
)