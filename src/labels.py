"""
labels.py — Fonte única da taxonomia do projeto (fase Get).

Define as classes finais e o mapa de harmonização (nome de pasta de cada
fonte -> classe comum). Usado pelo build_derived.py e pelo build_manifest.py.

NOTA METODOLÓGICA (sigatoka): a classe canônica `sigatoka` agrega
**Black Sigatoka** (só Tanzânia) com Sigatoka não-especificada (BananaLSD /
Bangladesh-424). Como a Tanzânia é a única fonte de Black Sigatoka E a única
de `fusarium_wilt`, há correlação classe↔fonte: interprete o F1 de sigatoka
no fold LODO em que a Tanzânia é o hold-out à luz dessa mistura.
"""

import os

# Taxonomia comum do projeto (ordem fixa)
CANONICAL = ["healthy", "sigatoka", "cordana", "pestalotiopsis", "fusarium_wilt"]

# Para cada fonte: país + mapa (trecho do nome da pasta -> classe comum).
# O casamento é por SUBTRECHO em minúsculo, então "FUSARIUM WILT-1" casa com
# "fusarium" e "Black Sigatoka" casa com "sigatoka". Chaves mais longas têm
# prioridade (ver classify()).
SOURCES = {
    "tanzania_zenodo": {
        "country": "Tanzania",
        "map": {
            "fusarium": "fusarium_wilt",
            "healthy": "healthy",
            "sigatoka": "sigatoka",  # "Black Sigatoka"
        },
    },
    "bananalsd": {
        "country": "Bangladesh",
        "map": {
            "healthy": "healthy",
            "sigatoka": "sigatoka",
            "cordana": "cordana",
            "pestalotiopsis": "pestalotiopsis",
        },
    },
    "bangladesh424": {
        "country": "Bangladesh",
        "map": {
            "healthy": "healthy",
            "fresh": "healthy",
            "sigatoka": "sigatoka",
            "cordana": "cordana",
            "pestalotiopsis": "pestalotiopsis",
        },
    },
}


def classify(source, path):
    """Descobre a classe comum de uma imagem pelo nome das PASTAS do caminho.

    `path` pode ser o caminho no disco ou o nome interno do zip. Casa a classe
    só contra os componentes de DIRETÓRIO (ignora o nome do arquivo), do mais
    profundo para o mais raso, para não rotular errado por causa do basename
    (ex.: uma foto "healthy_compare.jpg" dentro de .../cordana/). A chave mais
    longa vence. Retorna a classe comum ou None se nada casar.
    """
    mapa = SOURCES[source]["map"]
    chaves = sorted(mapa, key=len, reverse=True)
    partes = path.replace("\\", "/").split("/")
    dirs = [d.lower() for d in partes[:-1]]  # exclui o nome do arquivo
    for d in reversed(dirs):                  # pasta mais profunda primeiro
        for chave in chaves:
            if chave in d:
                return mapa[chave]
    return None
