#!#usr/bin/python
"""
author: Alvaro Carnielo e Silva
Date: 2024-11-09
"""
tables={
    "tipo_votavel":{
        'CD_TIPO_VOTAVEL':'INT',
	    'DS_TIPO_VOTAVEL':'VARCHAR(100)',
    },
    "cargo":{
        'CD_CARGO_PERGUNTA':'INT',
	    'DS_CARGO_PERGUNTA':'VARCHAR(100)',
    },
    "municipio":{
        'SG_UF':'INT',
        'CD_MUNICIPIO':'INT',
        'NM_MUNICIPIO':'VARCHAR(100)',
    },
    "partido":{
        'NR_PARTIDO':'INT',
        'SG_PARTIDO':'VARCHAR(20)',
        'NM_PARTIDO':'VARCHAR(50)',
    },
    "zona_eleitoral_local":{
        'NR_ZONA':'INT',
        'NR_SECAO':'INT',
        'NR_LOCAL_VOTACAO':'INT',
        'CD_MUNICIPIO':'INT',
    },
    "zona_eleitoral_eleicao":{
        'ID_local_votacao':'INT',       # ID key from table "zona_eleitoral_local"
        'QT_APTOS':'INT',
        'QT_COMPARECIMENTO':'INT',
        'QT_ABSTENCOES':'INT',
        'CD_TIPO_URNA':'INT'
    },
    "urna_descricao":{
        'CD_TIPO_URNA': 'INT',
        'DS_TIPO_URNA': 'VARCHAR(50)',
    },
    "urna_descricao":{
        'DT_PLEITO': 'DATE',
        'NR_URNA_EFETIVADA': 'INT',
        'DT_ABERTURA': 'DATE',
        'DT_ENCERRAMENTO': 'DATE',
        'QT_ELEI_BIOM_SEM_HABILITACAO': 'INT',
        'DT_EMISSAO_BU': 'DATE'
    },
    "candidato":{
	    'ID_candidato':'INT',
        'CD_MUNICIPIO': 'INT',
        'NR_PARTIDO':'INT',
        'NR_VOTAVEL': 'INT',
        'NM_VOTAVEL': 'VARCHAR(150)',
    },
    "main":{
        'ANO_ELEICAO':'INT',
        'DT_PLEITO':'DATE',
        'NR_TURNO':'INT',
        'CD_MUNICIPIO':'INT',
        'ID_local_votacao':'INT',       # ID key from table "zona_eleitoral_local"
        'CD_CARGO_PERGUNTA':'INT',
        'CD_TIPO_VOTAVEL':'INT',
        'ID_candidato':'INT',           # ID Key from table "candidato"
        'QT_VOTOS':'INT',
    },
}
