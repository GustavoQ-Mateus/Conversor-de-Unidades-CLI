from typing import Dict, Tuple

# Canonical units por categoria
CATEGORIES = {
    "temperature": ["c", "f", "k"],  # Celsius, Fahrenheit, Kelvin
    "distance": ["m", "km", "mi"],   # Metro, Quilômetro, Milha
    "weight": ["kg", "lb"],          # Quilograma, Libra
}

# Mapeamento de sinônimos -> canonical
SYNONYMS: Dict[str, Dict[str, str]] = {
    "temperature": {
        "c": "c", "cel": "c", "celsius": "c", "°c": "c",
        "f": "f", "fah": "f", "fahrenheit": "f", "°f": "f",
        "k": "k", "kelvin": "k",
    },
    "distance": {
        "m": "m", "metro": "m", "metros": "m",
        "km": "km", "kilometro": "km", "quilometro": "km", "quilômetro": "km",
        "kilometros": "km", "quilometros": "km", "quilômetros": "km",
        "mi": "mi", "mile": "mi", "miles": "mi", "milha": "mi", "milhas": "mi",
    },
    "weight": {
        "kg": "kg", "kilogram": "kg", "kilograma": "kg", "quilograma": "kg", "quilo": "kg",
        "lb": "lb", "lbs": "lb", "pound": "lb", "pounds": "lb", "libra": "lb", "libras": "lb",
    },
}

def list_categories() -> Dict[str, list]:
    return CATEGORIES.copy()

def list_units(category: str) -> list:
    category = category.lower()
    if category not in CATEGORIES:
        raise ValueError(f"Categoria inválida: {category}")
    return CATEGORIES[category]

def normalize_unit(category: str, unit: str) -> str:
    category = category.lower().strip()
    unit = unit.lower().strip()
    if category not in CATEGORIES:
        raise ValueError(f"Categoria inválida: {category}")
    if unit in CATEGORIES[category]:
        return unit
    norm_map = SYNONYMS.get(category, {})
    if unit in norm_map:
        return norm_map[unit]
    raise ValueError(f"Unidade inválida para {category}: {unit}")

# ---- Temperature conversions ----
def _to_celsius(value: float, from_unit: str) -> float:
    if from_unit == "c":
        return value
    if from_unit == "f":
        return (value - 32.0) * 5.0 / 9.0
    if from_unit == "k":
        return value - 273.15
    raise ValueError(f"Unidade de origem inválida para temperatura: {from_unit}")

def _from_celsius(value_c: float, to_unit: str) -> float:
    if to_unit == "c":
        return value_c
    if to_unit == "f":
        return value_c * 9.0 / 5.0 + 32.0
    if to_unit == "k":
        return value_c + 273.15
    raise ValueError(f"Unidade de destino inválida para temperatura: {to_unit}")

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    # Valida Kelvin não negativo na entrada
    if from_unit == "k" and value < 0:
        raise ValueError("Temperatura em Kelvin não pode ser negativa.")
    if from_unit == to_unit:
        return float(value)
    c = _to_celsius(float(value), from_unit)
    k = _from_celsius(c, "k")
    if k < 0:
        # Conversão resultou em Kelvin negativo => fisicamente inválido
        raise ValueError("Resultado inválido: temperatura abaixo de 0 K.")
    return _from_celsius(c, to_unit)

# ---- Distance conversions (via metro como base) ----
METER_FACTORS = {
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
}

def convert_distance(value: float, from_unit: str, to_unit: str) -> float:
    if value < 0:
        raise ValueError("Distância não pode ser negativa.")
    if from_unit == to_unit:
        return float(value)
    meters = float(value) * METER_FACTORS[from_unit]
    return meters / METER_FACTORS[to_unit]

# ---- Weight conversions (via kg como base) ----
KG_FACTORS = {
    "kg": 1.0,
    "lb": 2.2046226218487757,  # 1 kg = 2.2046226218 lb
}

def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    if value < 0:
        raise ValueError("Peso não pode ser negativo.")
    if from_unit == to_unit:
        return float(value)
    kg = float(value) / (KG_FACTORS[from_unit] if from_unit != "kg" else 1.0)
    if to_unit == "kg":
        return kg
    return kg * KG_FACTORS[to_unit]

def convert(category: str, from_unit: str, to_unit: str, value: float) -> Tuple[float, str, str]:
    """
    Converte um valor entre unidades.

    Retorna (resultado, from_canonical, to_canonical)
    """
    cat = category.lower().strip()
    if cat not in CATEGORIES:
        raise ValueError(f"Categoria inválida: {category}")

    f = normalize_unit(cat, from_unit)
    t = normalize_unit(cat, to_unit)

    if cat == "temperature":
        result = convert_temperature(value, f, t)
    elif cat == "distance":
        result = convert_distance(value, f, t)
    elif cat == "weight":
        result = convert_weight(value, f, t)
    else:
        raise ValueError(f"Categoria não suportada: {category}")

    return float(result), f, t