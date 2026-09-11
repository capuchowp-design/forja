#!/usr/bin/env python3
"""
Gera exercicios/ (arquivos renomeados) + gifs.js para o app FORJA.

Uso:
    python3 gerar_manifest.py /caminho/para/pasta/com/webp

Faz:
  1. Normaliza nomes de arquivo (minusculo, sem acento, sem espaço) -> evita
     problemas de case-sensitivity no GitHub Pages (Linux).
  2. Casa cada exercicio do FORJA (lista EX abaixo, extraida do app) com o
     arquivo .webp cujo nome mais se parece.
  3. Gera gifs.js só com os 64 ids que casaram.
  4. Gera nao-casados.txt com a lista dos demais arquivos (os outros ~647),
     para você revisar / me mandar e eu expandir o banco de exercicios.
"""
import sys, os, re, shutil, unicodedata, json, difflib

EX = ["Supino Reto com Barra","Supino Inclinado com Halteres","Supino Declinado","Crucifixo com Halteres","Crucifixo no Cabo","Flexão de Braço","Peck Deck (Voador)","Pullover com Halter","Puxada Frontal (Lat Pulldown)","Puxada Atrás da Cabeça","Remada Curvada com Barra","Remada Unilateral (Serrote)","Remada Baixa no Cabo","Remada na Máquina","Levantamento Terra","Pull-up (Barra Fixa)","Chin-up (Pegada Supinada)","Face Pull","Agachamento Livre (Back Squat)","Agachamento Frontal","Leg Press 45°","Afundo (Lunge)","Cadeira Extensora","Mesa Flexora","Stiff (Terra Romeno)","Elevação de Panturrilha em Pé","Elevação de Panturrilha Sentado","Agachamento Búlgaro","Hack Squat","Terra Sumô","Desenvolvimento Militar com Barra","Desenvolvimento com Halteres","Elevação Lateral","Elevação Frontal","Crucifixo Inverso (Rear Delt)","Encolhimento (Shrugs)","Arnold Press","Push Press","Rosca Direta com Barra","Rosca Alternada com Halteres","Rosca Martelo","Rosca no Cabo (W)","Rosca Scott (Máquina)","Tríceps Testa (French Press)","Tríceps no Cabo (Corda)","Tríceps Francês","Mergulho nas Paralelas (Dips)","Extensão de Tríceps Unilateral","Prancha Abdominal","Prancha Lateral","Crunch Abdominal","Elevação de Pernas","Abdominal na Polia Alta","Russian Twist","Dead Bug","Mountain Climbers","Elevação de Joelhos na Barra","Corrida","Bike Ergométrica","Pular Corda","Burpee","Remo Ergométrico","Stairmaster","Caminhada Inclinada"]

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower()
    s = re.sub(r"[_\s]+", "-", s)
    s = re.sub(r"[^a-z0-9\-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 gerar_manifest.py /caminho/para/pasta"); sys.exit(1)
    src = sys.argv[1]
    out_dir = "exercicios"
    os.makedirs(out_dir, exist_ok=True)

    files = []
    for root, _, names in os.walk(src):
        for n in names:
            if n.lower().endswith((".webp", ".gif")):
                files.append(os.path.join(root, n))

    # normaliza e copia todos os arquivos (flat) para exercicios/
    renamed = {}  # slug_sem_ext -> nome_final
    for f in files:
        base, ext = os.path.splitext(os.path.basename(f))
        new_name = slug(base) + ext.lower()
        # evita colisão de nomes
        i = 1
        final = new_name
        while final in renamed.values():
            final = f"{slug(base)}-{i}{ext.lower()}"
            i += 1
        renamed[f] = final
        shutil.copy2(f, os.path.join(out_dir, final))

    # casa exercicios <-> arquivos por similaridade de slug
    file_slugs = {f: slug(os.path.splitext(v)[0]) for f, v in renamed.items()}
    used = set()
    gifs = {}
    unmatched_ex = []
    for idx, name in enumerate(EX):
        target = slug(name)
        target_tokens = set(target.split("-"))
        best, best_score = None, 0.0
        for f, fs in file_slugs.items():
            if f in used:
                continue
            f_tokens = set(fs.split("-"))
            overlap = len(target_tokens & f_tokens) / max(1, len(target_tokens))
            ratio = difflib.SequenceMatcher(None, target, fs).ratio()
            score = 0.6 * overlap + 0.4 * ratio
            if score > best_score:
                best_score, best = score, f
        if best is not None and best_score >= 0.55:
            gifs[str(idx)] = renamed[best]
            used.add(best)
        else:
            unmatched_ex.append(name)

    with open("gifs.js", "w", encoding="utf-8") as fh:
        fh.write("window.GIFS = ")
        fh.write(json.dumps(gifs, ensure_ascii=False, indent=2))
        fh.write(";\n")

    leftover = sorted(v for f, v in renamed.items() if f not in used)
    with open("nao-casados.txt", "w", encoding="utf-8") as fh:
        fh.write(f"{len(leftover)} arquivos que NÃO foram vinculados a nenhum exercício existente:\n\n")
        fh.write("\n".join(leftover))

    print(f"OK: {len(gifs)}/{len(EX)} exercícios vinculados automaticamente.")
    if unmatched_ex:
        print("Exercícios do app sem GIF encontrado:")
        for n in unmatched_ex:
            print("  -", n)
    print(f"{len(leftover)} arquivos sobraram (ver nao-casados.txt) — me envie essa lista para eu expandir o banco de exercícios.")

if __name__ == "__main__":
    main()
