from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from converter import convert, list_categories, list_units

app = FastAPI(
    title="Conversor de Unidades API",
    version="1.0.0",
    description="Converte temperaturas (C/F/K), distâncias (m/km/mi) e pesos (kg/lb).",
)

# CORS liberado para facilitar o uso no modo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConvertResponse(BaseModel):
    category: str
    from_unit: str
    to_unit: str
    input_value: float
    result: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/categories")
def categories():
    return list_categories()

@app.get("/units")
def units(category: str = Query(..., description="Categoria: temperature|distance|weight")):
    return list_units(category)

@app.get("/convert", response_model=ConvertResponse)
def convert_endpoint(
    category: str = Query(..., description="temperature | distance | weight"),
    from_unit: str = Query(..., description="Unidade de origem"),
    to_unit: str = Query(..., description="Unidade de destino"),
    value: float = Query(..., description="Valor numérico"),
):
    result, f, t = convert(category, from_unit, to_unit, value)
    return ConvertResponse(
        category=category.lower(),
        from_unit=f,
        to_unit=t,
        input_value=value,
        result=result,
    )