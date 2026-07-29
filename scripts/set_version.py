"""Pre-render do Quarto: grava o numero de versao (baseado no historico git)
na capa de todas as aulas, via aulas/_metadata.yml.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META_PATH = ROOT / "aulas" / "_metadata.yml"


def get_version() -> str:
    # Baseado apenas na contagem de commits (numero de "versoes" salvas no
    # git). Nao verifica se ha alteracoes nao commitadas: como este proprio
    # script reescreve aulas/_metadata.yml a cada render, um check de "sujo"
    # baseado nesse arquivo entraria em loop (alterna limpo/sujo a cada
    # execucao). Se quiser saber se ha mudancas pendentes, use `git status`.
    try:
        count = subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return f"v{count}"
    except Exception:
        return "v0"


def main() -> None:
    text = META_PATH.read_text(encoding="utf-8")

    base_match = re.search(r'^institute_base:\s*"(.*)"\s*$', text, flags=re.M)
    base = base_match.group(1) if base_match else ""

    version = get_version()
    institute_line = f'institute: "{base} · {version}"'

    if re.search(r"^institute:.*$", text, flags=re.M):
        text = re.sub(r"^institute:.*$", institute_line, text, flags=re.M)
    else:
        text = text.rstrip("\n") + f"\n{institute_line}\n"

    META_PATH.write_text(text, encoding="utf-8")
    print(f"[set_version] versao da capa atualizada para {version}")


if __name__ == "__main__":
    main()
