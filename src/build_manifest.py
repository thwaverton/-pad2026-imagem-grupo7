"""
build_manifest.py — Fase Get: monta o "banco" data/manifest.csv.

Varre data/derived/<fonte>/<classe>/ (já harmonizado e redimensionado pelo
build_derived.py) e grava uma linha por imagem com a coluna `source` (chave
do LODO). Faz DEDUPLICAÇÃO EXATA por SHA-256 dos bytes (Etapa 5 da trilha),
mas de forma ciente de fonte/rótulo:

- duplicata na MESMA fonte e MESMO rótulo  -> `dup_of` aponta p/ a 1ª cópia
  (o split descarta as marcadas, evitando vazamento treino/teste);
- duplicata entre FONTES diferentes        -> marcada `note=cross_source`,
  NÃO colapsada (colapsar vazaria conteúdo no LODO);
- duplicata com RÓTULOS diferentes          -> `note=label_conflict`, NÃO
  colapsada e listada em data/dup_conflicts.csv (erro de rotulagem a revisar).

Uso:
    python src/build_manifest.py
"""

import sys
import csv
import hashlib
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from labels import CANONICAL, SOURCES  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DERIVED = ROOT / "data" / "derived"
MANIFEST = ROOT / "data" / "manifest.csv"
CONFLICTS = ROOT / "data" / "dup_conflicts.csv"
FIELDS = ["image_id", "source", "country", "label", "sha256", "dup_of", "note", "filepath"]


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def main():
    if not DERIVED.exists():
        print(f"[!] Pasta nao encontrada: {DERIVED}")
        print("    Rode o notebook (build_derived) antes para gerar o derivado.")
        sys.exit(1)

    rows = []
    for source, cfg in SOURCES.items():
        if not (DERIVED / source).exists():
            print(f"[aviso] fonte '{source}' declarada mas sem pasta em data/derived/ "
                  f"-> ignorada (0 imagens).")
            continue
        for classe in CANONICAL:
            for img in sorted((DERIVED / source / classe).glob("*")):
                if not img.is_file():
                    continue
                rows.append({
                    "image_id": str(img.relative_to(ROOT)),
                    "source": source,
                    "country": cfg["country"],
                    "label": classe,
                    "sha256": sha256(img),
                    "dup_of": "",
                    "note": "",
                    "filepath": str(img),
                })

    if not rows:
        print("\n[!] Nenhuma imagem em data/derived/. Rode o notebook (Get) antes.")
        sys.exit(1)

    # --- dedup ciente de fonte/rotulo ---
    by_hash = {}
    for r in rows:
        by_hash.setdefault(r["sha256"], []).append(r)
    n_dup = n_cross = 0
    conflitos = []
    for grupo in by_hash.values():
        if len(grupo) == 1:
            continue
        labels = {r["label"] for r in grupo}
        sources = {r["source"] for r in grupo}
        if len(labels) > 1:                       # mesmo byte, rotulo diferente
            for r in grupo:
                r["note"] = "label_conflict"
            conflitos.extend(grupo)
            continue
        if len(sources) > 1:                      # mesmo byte em fontes diferentes
            for r in grupo:
                r["note"] = "cross_source"
            n_cross += len(grupo)
            continue
        grupo.sort(key=lambda r: r["image_id"])   # dup segura (mesma fonte+classe)
        keep = grupo[0]["image_id"]
        for r in grupo[1:]:
            r["dup_of"] = keep
            n_dup += 1

    rows.sort(key=lambda r: (r["source"], r["label"], r["image_id"]))
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    if conflitos:
        with open(CONFLICTS, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(conflitos)

    # --- resumo ---
    uniq = [r for r in rows if not r["dup_of"] and r["note"] != "label_conflict"]
    print(f"[OK] manifest.csv: {len(rows)} imagens "
          f"({len(uniq)} usaveis, {n_dup} duplicatas, {n_cross} cross-source) -> {MANIFEST}")

    cont = {}
    for r in uniq:
        cont[(r["source"], r["label"])] = cont.get((r["source"], r["label"]), 0) + 1
    print("\nDistribuicao usavel (fonte x classe):")
    print(f"{'fonte':<18}{'classe':<16}{'n':>6}")
    for k in sorted(cont):
        print(f"{k[0]:<18}{k[1]:<16}{cont[k]:>6}")
    print("\nTotal por classe:")
    for c in CANONICAL:
        print(f"  {c:<16}{sum(v for k, v in cont.items() if k[1] == c):>6}")

    # --- avisos de avaliacao (LODO) ---
    fontes_por_classe = {}
    for (src, lab), n in cont.items():
        if n:
            fontes_por_classe.setdefault(lab, set()).add(src)
    single = [c for c in CANONICAL if len(fontes_por_classe.get(c, set())) <= 1]
    if single:
        print("\n[AVISO LODO] classes em uma UNICA fonte "
              "(F1=0/indefinido no fold que deixa essa fonte de fora):")
        for c in single:
            fontes = ", ".join(sorted(fontes_por_classe.get(c, []))) or "(nenhuma)"
            print(f"  - {c}: somente {fontes}")
        print("  -> defina a politica de F1-macro do LODO para essas classes (fase Model).")
    if conflitos:
        print(f"\n[AVISO] {len(conflitos)} imagens com bytes identicos e ROTULOS "
              f"diferentes -> revise data/dup_conflicts.csv (erro de rotulagem).")


if __name__ == "__main__":
    main()
