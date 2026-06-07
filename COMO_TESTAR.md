# 🧪 Como testar a fase Get

Guia para qualquer integrante rodar e validar o pipeline de dados (fase **Get** do AGEMC).

---

## 🧠 O que o Get faz (em 1 minuto)

O pipeline pega fotos **reais** de folha de banana de vários datasets, **encolhe** cada uma
e **organiza** tudo num formato pronto para treinar. Em 3 movimentos:

1. **Baixa** os datasets (Tanzânia via Zenodo + BananaLSD via Kaggle);
2. **Reduz** cada imagem para 320 px e organiza em `data/derived/<fonte>/<classe>/`;
3. **Monta** o `manifest.csv` (1 linha por imagem, marcando de qual fonte veio) e salva tudo
   no seu Google Drive.

---

## 🔑 Antes de começar — credencial do Kaggle (só 1 vez)

1. Entre em [kaggle.com](https://www.kaggle.com) (crie conta se não tiver).
2. Clique na sua foto → **Settings**.
3. Seção **API** → botão **Create New Token** → baixa o arquivo **`kaggle.json`**. Guarde-o.

---

## 📋 Passo a passo (no Google Colab)

| Passo | O que fazer | O que esperar |
|------:|-------------|---------------|
| **1** | Abra o repo no GitHub e clique no botão **"Open in Colab"** (topo do README) | Abre o `notebooks/01_get.ipynb` no Colab |
| **2** | Menu **Ambiente de execução → Alterar o tipo → GPU** | (bom hábito; o Get nem exige GPU) |
| **3** | Rode a **célula 1** (montar o Drive) | Pede para autorizar sua conta Google → autorize |
| **4** | Rode as **células 2 e 3** (clonar + entrar na pasta) | Aparece `/content/repo` |
| **5** | Rode a **célula 4** (importar os scripts) | Sem erro = ok |
| **6** | Rode a **célula 5** (baixar + derivar a Tanzânia, ~9 GB) | ⏳ **demora alguns minutos**. Imprime `[tanzania_zenodo] N derivadas` por zip |
| **7** | Rode a **célula 6** (instalar o Kaggle) | instala rápido |
| **8** | Rode a **célula 7** → **"Escolher arquivos"** → envie o **`kaggle.json`** | mostra o nome do arquivo enviado |
| **9** | Rode a **célula 8** (configurar credencial) | sem erro |
| **10** | Rode as **células 9 e 10** (baixar + derivar o BananaLSD) | imprime `[bananalsd] N derivadas` |
| **11** | Rode a **célula 11** (montar o manifesto) | resumo de contagens |
| **12** | Rode a **célula 12** (conferir) ⭐ | planilha de contagem por fonte × classe |
| **13** | Rode a **célula 13** (amostra visual) | mostra 1 folha real de cada classe |
| **14** | Rode a **célula 14** (salvar no Drive) | copia tudo para o seu Drive |

---

## ✅ O que conferir (checkpoints)

**1. Célula 10 (BananaLSD) — o teste mais importante**
- Deve dar **centenas** por classe (~900 no total), **não milhares**.
- Se vier ~2.500, o `AugmentedSet` escapou → avise a equipe.

**2. Célula 12 (contagens) — deve fazer sentido**
- `fusarium_wilt` só em **tanzania_zenodo**;
- `cordana` e `pestalotiopsis` só em **bananalsd**;
- `healthy` e `sigatoka` nas **duas** fontes;
- Vai aparecer um **`[AVISO LODO]`** listando as classes de fonte única — **isso é
  esperado** (não é erro), é um lembrete para a fase Model.

**3. Célula 13 (visual)**
- Devem aparecer **folhas de banana reais**, todas no mesmo tamanho (320×320).

**4. No seu Google Drive**
- Deve surgir a pasta `banana_pad/derived/` com as imagens e o `manifest.csv`.

---

## 🎯 Sinal de que deu tudo certo

Sem erros vermelhos, as contagens fazem sentido, aparecem folhas reais na amostra e o dataset
fica salvo no Drive. **Aí o Get está validado com os dados reais.**

> 💡 **Teste rápido:** para ver funcionando sem esperar os 9 GB, edite a célula 5 e deixe
> **só um zip** na lista (ex.: `['FUSARIUM WILT-1.zip']`). Roda em ~2 min e já prova o fluxo.
> Depois volte os três para valer.

---

## ❓ Deu erro? Onde olhar

| Sintoma | Provável causa | O que fazer |
|---|---|---|
| `kaggle: command not found` / erro 401 | `kaggle.json` não enviado/configurado | refaça as células 7 e 8 |
| `download corrompido` na Tanzânia | queda no download | rode a célula 5 de novo (ela retoma) |
| BananaLSD com milhares de imagens | `AugmentedSet` entrou | confira na célula 12 e avise a equipe |
| Sessão caiu e perdi os dados | disco do Colab é temporário | rode a célula 1 + **célula 16** (recarrega do Drive, sem rebaixar) |

---

📂 Arquivos relacionados: [`notebooks/01_get.ipynb`](notebooks/01_get.ipynb) ·
[`data/README.md`](data/README.md) · [`data/SOURCES.md`](data/SOURCES.md)
