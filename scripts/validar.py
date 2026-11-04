#!/usr/bin/env python3
"""Valida a estrutura do repositório da skill. Uso: python3 scripts/validar.py [pasta]"""
import re
import sys
from pathlib import Path

# o console do Windows (cp1252) não imprime "≤" e quebra o script
sys.stdout.reconfigure(encoding="utf-8")

raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
ok = True


def checar(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok &= bool(cond)


skill = (raiz / "SKILL.md").read_text(encoding="utf-8")
m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", skill)
checar(m, "frontmatter válido (name + description)")
if m:
    checar(re.fullmatch(r"[a-z0-9-]{1,64}", m.group(1)), "name em minúsculas, sem acento, com hífen (≤64)")
    checar(m.group(1) == raiz.name, f"name ('{m.group(1)}') == nome da pasta ('{raiz.name}')")
    checar(len(m.group(2)) <= 1024, f"description ≤1024 ({len(m.group(2))})")

for ref in re.findall(r"`(references/[\w./-]+)`", skill):
    checar((raiz / ref).exists(), f"link existe: {ref}")

bloco = skill.split("Regras invioláveis")[1].split("## Fluxo")[0] if "Regras invioláveis" in skill else ""
for n in range(1, 6):
    checar(f"{n}. " in bloco, f"regra inviolável {n} presente")

for f in ["README.md", "LICENSE", "CHANGELOG.md", "adapters/chatgpt-instructions.md",
          "templates/lessons.md", "evals/cenarios.md"]:
    checar((raiz / f).exists(), f"existe {f}")

linhas = len(skill.splitlines())
checar(linhas < 500, f"SKILL.md curto ({linhas} linhas)")

adapter = (raiz / "adapters/chatgpt-instructions.md").read_text(encoding="utf-8")
checar(len(adapter) < 8000, f"adapter <8000 caracteres ({len(adapter)})")
for k in ["INVIOLÁVEIS", "aprovação", "≥2", "Máx. 3", "depois de entregar"]:
    checar(k in adapter, f"adapter contém '{k}' (paridade com SKILL)")

sys.exit(0 if ok else 1)
