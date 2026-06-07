# 🖼️ Projeto 7 — Classificação de Imagens com *Transfer Learning*

> Projeto da disciplina **PAD 2026 — Projetos** (Prof. Federson / UFG)
> Área de Conhecimento: **Ciência de Dados** · Tipo de problema: **7. Imagem**

---

## 👥 Equipe

| Integrante | Papel | GitHub |
|------------|-------|--------|
| João Gabriel | Líder | [@jgds007]( |
| Thwaverton OLiveira Martins | integrante | [@thwaverton] |
| Vitor Severino França | integrante| [@] |
| Gustavo Henrique Alves dos Santos |integrante| [@Henrique-codes] |

---

## 🎯 Sobre o projeto

Este é um projeto **ORIGINAL** baseado em um **Projeto FMF de referência**, no qual aplicamos o processo de Ciência de Dados (**AGEMC** — *Ask, Get, Explore, Model, Communicate*) a um problema de **classificação de imagens** usando *transfer learning* em PyTorch.

- **Projeto FMF de referência:** *Image classification tutorials in pytorch — transfer learning* (Sanchit Tanwar)
  https://medium.com/swlh/image-classification-tutorials-in-pytorch-transfer-learning-19ebc329e200

### Pergunta-problema
> *(a definir na Semana A — ex.: "Dada uma imagem de X, conseguimos classificar automaticamente entre as classes A, B e C?")*

### Nossa originalidade (o que nos diferencia do FMF)
> *(a definir — ex.: dataset com contexto local + explicabilidade com Grad-CAM + mini-app de demonstração)*

---

## 🚀 Como rodar a fase Get (coleta dos dados)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thwaverton/-pad2026-imagem-grupo7/blob/main/notebooks/01_get.ipynb)

Todo o pipeline de dados roda no **Google Colab**, célula por célula (cada uma explicada):

1. **Abra** o notebook [`notebooks/01_get.ipynb`](notebooks/01_get.ipynb) no Colab (botão acima).
2. **Pré-requisitos:** uma conta Google (para o Drive) e uma conta Kaggle — baixe seu
   `kaggle.json` em *Kaggle → Settings → Create New Token*.
3. **Rode as células de cima para baixo.** Elas baixam os datasets (Zenodo + Kaggle),
   reduzem cada imagem para 320 px, organizam em `data/derived/<fonte>/<classe>/`, montam o
   `data/manifest.csv` (com a coluna `source`, que viabiliza o teste **LODO**) e salvam tudo
   no seu Google Drive.
4. **Resultado:** dataset limpo (~1–2 GB) + `manifest.csv`. Nas próximas sessões é só
   remontar o Drive — sem rebaixar nada.

> As imagens **não** ficam no Git (são pesadas). Detalhes de fontes, licenças e do pipeline
> em [`data/README.md`](data/README.md) e [`data/SOURCES.md`](data/SOURCES.md).

---

## 🗓️ Cronograma (AGEMC)

| Fase | Etapa | Prazo |
|------|-------|-------|
| **A** — Ask | Pergunta, classes e métrica de sucesso | até **01/jun** |
| **G** — Get | Coleta e organização dos dados | até **07/jun** ✅ |
| **E** — Explore | Análise exploratória (EDA) | até **14/jun** |
| **M** — Model | Treino e validação do modelo | até **21/jun** |
| **C** — Communicate | Resultados, demo e slides | até **28/jun** |
| 🎤 | **Apresentação final** (~15 min) | **02/jul** |

O repositório é atualizado **semana a semana** (commits acompanham o processo, não só o resultado final).

---

## 📁 Estrutura do repositório

```
.
├── README.md
├── requirements.txt
├── data/
│   ├── README.md          # como obter/reconstruir os dados
│   ├── SOURCES.md         # fontes, licenças e links
│   └── raw/ , derived/    # imagens (NÃO versionadas — ficam no Drive/Colab)
├── notebooks/
│   └── 01_get.ipynb       # ✅ fase Get (download, resize, manifesto) — roda no Colab
├── src/
│   ├── labels.py          # taxonomia e harmonização de rótulos por fonte
│   ├── build_derived.py   # stream dos zips + resize 320px (JPEG q90)
│   └── build_manifest.py  # manifesto multi-fonte + dedup SHA-256
├── models/                # modelo treinado (.pth) — fases futuras
└── reports/               # gráficos, matriz de confusão, slides
```

---

## 🛠️ Tecnologias previstas

- Python · PyTorch · torchvision
- scikit-learn (métricas) · matplotlib (visualização)
- Google Colab (treino com GPU)

---

## 📌 Status

🚧 **Semana 1 (Ask)** — grupo formado, projeto escolhido e repositório criado. Desenvolvimento em andamento.

❓ Após uma breve reunião o Grupo decidiu a seguite pergunta: **Analisando a foto de uma plantação de bananeiras em conjunto com imagens de folhas pré-selecionadas, é possível identificar se as plantas estão saudáveis ou doentes? Em caso positivo, é possível determinar a extensão aproximada da área afetada?**

O processo para a criação da pergunta surgiu após um dos nossos menbros comentar sobre a familia possuir uma plantação de Bananas e como era o dia a dia deles, após isso ele nos mostrou os problemas que a plantação sofre, pragas e bananeiras doentes. Nos inicialmente decidimos abordar a pergunta para apenas classificar se uma bananeira estaria doente ou não, mas depois de dialogar por mais um tempo decidimos ir além de so classificar as bananeiras, mas sim dizer qual o tamanho da aréa da plantação afetada e qual pode ser o possivel aumento da area afetada durante o tratamento da area atual.

🗂️ Possiveis datasets que utilizaremos:
| Apelido | Dataset | País | Classes | Tamanho | Onde pegar |
|---------|---------|------|---------|---------|------------|
| lsd | BananaLSD | Bangladesh | healthy, sigatoka, cordana, pestalotiopsis | ~937 + aumentado | Kaggle: shifatearman/bananalsd |

| rec | Banana Disease Recognition | campo real | ~7 classes (várias doenças + saudável) | ~408 | Kaggle: sujaykapadnis/banana-disease-recognition-dataset |

| tz | Banana Leaves Imagery | Tanzânia | healthy, black sigatoka, fusarium wilt | 11.767 | Zenodo/Harvard ("Banana Leaves Imagery Dataset") |

| psfd | PSFD-Musa | Índia (Assam) | variedades + 7 doenças (Sigatoka preta/amarela, Panamá...) | 8.000+ | Mendeley DOI 10.17632/4wyymrcpyz |

| br | Coleta da equipe | 🇧🇷 Brasil | (a definir) | 30–60 fotos | celular da equipe |

lsd— BananaLSD (Bangladesh)

Kaggle (mais fácil no Colab): https://www.kaggle.com/datasets/shifatearman/bananalsd
Mendeley (oficial): https://data.mendeley.com/datasets/9tb7k297ff/1
Artigo: https://www.sciencedirect.com/science/article/pii/S2352340923006959

rec — Banana Disease Recognition (imagens de campo)

Kaggle: https://www.kaggle.com/datasets/sujaykapadnis/banana-disease-recognition-dataset
Espelho no Roboflow: https://universe.roboflow.com/bananadisease/banana-disease-recognition
Espelho no Hugging Face: https://huggingface.co/datasets/as-cle-bert/banana-disease-classification

tz — Banana Leaves Imagery (Tanzânia) — esta é a fonte que eu precisava confirmar:

Zenodo (a versão de 11.767 imagens, 3 classes): https://doi.org/10.5281/zenodo.7670326 — "Banana imagery dataset – Tanzania", de Mduma & Elinisa (2023), com a raiz organizada em 9 zips: 3 de Fusarium Wilt, 3 de Black Sigatoka e 3 de Healthy. Google Tradutor
Artigo (Nature Scientific Data): https://www.nature.com/articles/s41597-025-04456-4
💡 Existe uma versão maior (16.092 imagens, folhas + caule ) no Harvard Dataverse, caso queiram mais dados: DOI 10.7910/DVN/LQUWXW → https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LQUWXW NIH

psfd — PSFD-Musa (Índia/Assam)

Mendeley (DOI 10.17632/4wyymrcpyz.1): https://data.mendeley.com/datasets/4wyymrcpyz/1
Artigo: https://www.sciencedirect.com/science/article/pii/S2352340922006242

br — Coleta da equipe (🇧🇷 Brasil): sem fonte externa —.

🎲 **Semana 2** — Datasets escolhidos, filtrar quais dados são relevantes e pequena exploração dos dados —

  Ao longo da semana a equipe se dedicou a encontrar datasets que possuam dados que iremos processar para a nossa pergunta (fotos de bananal, folhas saudaveis e doentes) agora o grupo ira se reunir hoje para nossa comunicar os datasets encontrados e visualisalos e filtralos para descobrir quais dados são mais relevantes e condizentes com o nosso objetivo.
