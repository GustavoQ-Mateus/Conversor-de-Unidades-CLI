import sys
from typing import Optional

from converter import convert, list_categories, list_units, normalize_unit

BANNER = r"""
===============================
 Conversor de Unidades (CLI)
===============================
Categorias:
1) Temperatura (C/F/K)
2) Distância (m/km/mi)
3) Peso (kg/lb)
Q) Sair
"""

CAT_MAP = {
    "1": "temperature",
    "2": "distance",
    "3": "weight",
}

def prompt(msg: str) -> str:
    try:
        return input(msg)
    except EOFError:
        print("\nSaindo...")
        sys.exit(0)

def choose_category() -> Optional[str]:
    print(BANNER)
    choice = prompt("Escolha uma opção: ").strip().lower()
    if choice in ("q", "quit", "sair", "exit"):
        return None
    if choice in CAT_MAP:
        return CAT_MAP[choice]
    print("Opção inválida. Tente novamente.")
    return choose_category()

def ask_unit(category: str, kind: str) -> str:
    units = list_units(category)
    pretty = ", ".join(units)
    raw = prompt(f"Informe a unidade de {kind} ({pretty} ou sinônimos): ").strip()
    try:
        return normalize_unit(category, raw)
    except Exception as e:
        print(f"Unidade inválida: {e}")
        return ask_unit(category, kind)

def ask_value(category: str, from_unit: str) -> float:
    raw = prompt(f"Informe o valor em {from_unit}: ").strip()
    try:
        value = float(raw.replace(",", "."))
        return value
    except ValueError:
        print("Valor inválido. Use números. Ex: 12.34")
        return ask_value(category, from_unit)

def main():
    print("Bem-vindo(a)!")
    while True:
        category = choose_category()
        if category is None:
            break

        from_unit = ask_unit(category, "origem")
        to_unit = ask_unit(category, "destino")
        value = ask_value(category, from_unit)

        try:
            result, f, t = convert(category, from_unit, to_unit, value)
            print(f"\nResultado: {value} {f} = {result:.6g} {t}\n")
        except Exception as e:
            print(f"Erro na conversão: {e}\n")

        again = prompt("Deseja fazer outra conversão? [s/N]: ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            break

    print("Até logo!")

if __name__ == "__main__":
    main()

