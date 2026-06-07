# 📦 Dados — Fase **Get** (AGEMC)

> As **imagens não ficam no Git** (são pesadas). Este arquivo explica **como obter**
> os dados e **como reconstruir** o manifesto. O pipeline da fase Get está no
> notebook [`notebooks/01_get.ipynb`](../notebooks/01_get.ipynb): ele baixa, **reduz
> para 320px**, organiza em `data/derived/<fonte>/<classe>/` e gera o manifesto.

## 🧭 Pipeline (caminho recomendado da trilha)

1. **Stream** dos zips (não extrai 34 GB) → `src/build_derived.py`;
2. **Resize** do lado menor p/ 320px + JPEG q90 (a rede usa 224 mesmo) → `data/derived/`;
3. **Manifesto** + **dedup SHA-256** (antes do split, evita vazamento) → `src/build_manifest.py`;
4. **Drive** guarda o derivado (~1–2 GB) pronto p/ as fases Explore/Model.

Arquivos-fonte da lógica: [`src/labels.py`](../src/labels.py) (taxonomia + harmonização),
[`src/build_derived.py`](../src/build_derived.py) (resize/stream),
[`src/build_manifest.py`](../src/build_manifest.py) (manifesto/dedup).

## 🎯 Taxonomia comum (após harmonização)

`healthy` · `sigatoka` · `cordana` · `pestalotiopsis` · `fusarium_wilt`

## 🌍 Fontes (multi-fonte = a originalidade do projeto)

| Fonte (pasta) | Origem | Classes que cobre | Licença | Link |
|---|---|---|---|---|
| `bananalsd` | Bangladesh | healthy, sigatoka, cordana, pestalotiopsis | CC BY 4.0 | [Mendeley](https://data.mendeley.com/datasets/9tb7k297ff/1) · [Kaggle](https://www.kaggle.com/datasets/shifatearman/bananalsd) |
| `tanzania_zenodo` | Tanzânia (NM-AIST / IITA) | healthy, sigatoka (Black Sigatoka), **fusarium_wilt** | CC BY 4.0 | [Scientific Data](https://www.nature.com/articles/s41597-025-04456-4) / Zenodo |
| `bangladesh424` | Bangladesh (Noakhali/Rangamati/Bandarban) | healthy, sigatoka, cordana, pestalotiopsis | CC BY 4.0 | [Mendeley](https://data.mendeley.com/datasets/wfzpdmc5vx/1) |

> ⚠️ **Atenção LODO:** hoje a classe **`fusarium_wilt` só aparece na fonte Tanzânia**.
> Isso é esperado e até interessante de discutir no relatório: ao "deixar a Tanzânia de
> fora" (leave-one-dataset-out), o modelo fica sem exemplos de fusário no treino.
> Se acharem uma 4ª fonte com fusário, melhor ainda — é só adicionar em `SOURCES`.

## ⬇️ Como baixar (resumo por fonte)

| Fonte | Como o notebook baixa | Login? |
|---|---|---|
| `tanzania_zenodo` | `wget` direto do Zenodo (1 zip por classe, ~9 GB) | não |
| `bananalsd` | `kaggle datasets download -d shifatearman/bananalsd` | sim (kaggle.json) |
| `bangladesh424` | manual: **Download All** no Mendeley → arrastar p/ a pasta | — |

> Os nomes das **subpastas** variam conforme o download. A harmonização casa por trecho
> (ex.: `FUSARIUM WILT-1` → `fusarium_wilt`); se algo não for reconhecido, ajuste o
> mapa da fonte em [`src/labels.py`](../src/labels.py).

## 🗃️ O "banco": `data/manifest.csv`

| coluna | descrição |
|---|---|
| `image_id` | identificador estável (caminho relativo da imagem) |
| `source` | fonte/dataset de origem (**chave do LODO**) |
| `country` | país de coleta |
| `label` | classe harmonizada (taxonomia comum) |
| `sha256` | hash dos bytes (para deduplicação) |
| `dup_of` | vazio se única; senão, `image_id` da 1ª cópia idêntica |
| `note` | `cross_source` (cópia entre fontes) ou `label_conflict` (mesma imagem, rótulos diferentes) |
| `filepath` | caminho do arquivo |

> Conflitos de rótulo (mesma imagem, classes diferentes) vão também para
> `data/dup_conflicts.csv` para revisão manual. O `build_manifest.py` avisa no
> resumo quando uma classe só existe em uma fonte (impacta o LODO).

O `manifest.csv` **é versionado** (é leve e é a prova do trabalho de Get).
As imagens em `data/raw/` e `data/derived/` **não** são versionadas (ver `.gitignore`).
