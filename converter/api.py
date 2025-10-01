

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Dict, Any
from .units import convert, normalize_unit
import os

app = FastAPI(title="Conversor de Unidades", version="1.0.0", docs_url=None, redoc_url=None, openapi_url=None)

# Montar arquivos estáticos (corrigido para 'web')
if os.path.exists("web"):
    app.mount("/static", StaticFiles(directory="web"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Exibe a interface web se disponível, senão mostra mensagem padrão."""
    try:
        with open("web/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <h1>Conversor de Unidades API</h1>
        <p>Aplicação está rodando! Acesse:</p>
        <ul>
            <li><a href="/">Interface Web</a></li>
        </ul>
        """)


# Conversão via GET (usada pela interface web)


@app.get("/convert")
async def convert_units_get(
    category: str = Query(...),
    from_unit: str = Query(...),
    to_unit: str = Query(...),
    value: float = Query(...)
):
    """Converte entre unidades (GET)"""
    try:
        from_unit_norm = normalize_unit(category, from_unit)
        to_unit_norm = normalize_unit(category, to_unit)
        result, _, _ = convert(category, from_unit_norm, to_unit_norm, float(value))
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde da API."""
    return {"status": "ok", "message": "API está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)