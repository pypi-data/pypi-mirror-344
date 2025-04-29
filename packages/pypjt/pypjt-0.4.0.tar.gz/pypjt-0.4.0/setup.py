from pathlib import Path

from setuptools import setup

PROJECT_DIR = Path(__file__).resolve().parent


def get_requires() -> dict[str, list[str]]:
    requirements_dir = PROJECT_DIR / 'requirements'
    base = ((requirements_dir / "base.txt").read_text(encoding="utf-8").split("\n"))
    base = [item for item in base if item]
    prod = ((requirements_dir / "prod.txt").read_text(encoding="utf-8").split("\n"))[1:]
    prod = [item for item in prod if item and item not in base]
    dev = ((requirements_dir / "dev.txt").read_text(encoding="utf-8").split("\n"))[1:]
    dev = list(set(prod + [item for item in dev if item and item not in base]))

    return {'base': base, 'prod': prod, 'dev': dev}


requires = get_requires()

setup(
    install_requires=requires["base"],
    extras_require={
        "dev": requires["dev"],
        "prod": requires["prod"],
    },
)
