"""
build_derived.py — Fase Get, Etapas 0+1 da trilha (streaming + resize offline).

Lê imagens de um .zip (sem extrair tudo) OU de uma pasta já extraída,
redimensiona o LADO MENOR para ~320px (sem upscaling), regrava como JPEG q90
e organiza em data/derived/<fonte>/<classe>/. Isso reduz a Tanzânia de ~34 GB
para ~1-2 GB sem perda perceptível (a rede usa 224 mesmo).

Cada saída recebe nome ÚNICO derivado do caminho interno + extensão .jpg
(evita colisão de basename que sobrescreveria imagens silenciosamente).
Imagens aumentadas (pastas "augment*") são puladas — usamos só as originais.

Sem dependências além de Pillow. Importável:
    from build_derived import derive_zip, derive_folder
"""

import io
import os
import sys
import glob
import zipfile
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from labels import classify  # noqa: E402

from PIL import Image  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DERIVED = ROOT / "data" / "derived"
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def _save(img, out_path, short_side=320, quality=90):
    """Redimensiona o lado menor p/ short_side (nunca amplia) e grava JPEG."""
    w, h = img.size
    s = short_side / min(w, h)
    if s < 1.0:
        img = img.resize((round(w * s), round(h * s)), Image.LANCZOS)
    img.save(out_path, "JPEG", quality=quality, optimize=True)


def _out_path(source, classe, rel_name):
    """Nome de saída único (a partir do caminho interno) com extensão .jpg."""
    d = DERIVED / source / classe
    d.mkdir(parents=True, exist_ok=True)
    stem = os.path.splitext(rel_name.replace("\\", "/"))[0].replace("/", "__")
    return d / f"{stem}.jpg"


def _report(source, n_ok, n_skip, n_err):
    msg = f"[{source}] {n_ok} derivadas"
    if n_skip:
        msg += f", {n_skip} sem classe"
    if n_err:
        msg += f", {n_err} com erro"
    print(msg)


def derive_zip(zip_path, source, short_side=320, quality=90):
    """Deriva imagens de dentro de um .zip, em streaming (sem extrair tudo)."""
    n_ok = n_skip = n_err = 0
    with zipfile.ZipFile(zip_path) as zf:  # zip corrompido -> erro alto (proposital)
        for name in zf.namelist():
            if not name.lower().endswith(IMAGE_EXTS):
                continue
            classe = classify(source, name)
            if not classe:
                n_skip += 1
                continue
            try:
                img = Image.open(io.BytesIO(zf.read(name))).convert("RGB")
                _save(img, _out_path(source, classe, name), short_side, quality)
                n_ok += 1
            except Exception as e:
                n_err += 1
                if n_err <= 3:
                    print(f"  [erro] {name}: {e!r}")
    _report(source, n_ok, n_skip, n_err)
    return n_ok


def derive_folder(folder, source, short_side=320, quality=90):
    """Deriva imagens de uma pasta já extraída (ex.: download do Kaggle).

    Pula qualquer caminho de augmentation (defesa: usamos só as originais).
    """
    n_ok = n_skip = n_err = 0
    for f in glob.glob(f"{folder}/**/*.*", recursive=True):
        low = f.lower()
        if "augment" in low:        # pula AugmentedSet (evita vazamento treino/teste)
            continue
        if not low.endswith(IMAGE_EXTS) or not os.path.isfile(f):
            continue
        classe = classify(source, f)
        if not classe:
            n_skip += 1
            continue
        try:
            img = Image.open(f).convert("RGB")
            rel = os.path.relpath(f, folder)
            _save(img, _out_path(source, classe, rel), short_side, quality)
            n_ok += 1
        except Exception as e:
            n_err += 1
            if n_err <= 3:
                print(f"  [erro] {f}: {e!r}")
    _report(source, n_ok, n_skip, n_err)
    return n_ok
