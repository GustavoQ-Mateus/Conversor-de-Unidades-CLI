## Recursos principais
- Uso via Interface Web (servida pela própria API mínima).
- Categorias suportadas: temperatura (C/F/K), distância (m/km/mi) e peso (kg/lb).
- Normalização de sinônimos (ex.: "quilo" → kg, "celsius" → c, "milha" → mi).
- Conversão realizada por um único endpoint interno (`GET /convert`), retornando `{ "result": <número> }`.
- Código simples e didático, ideal para estudo e reuso.

## Estrutura do projeto
```
.
├─ converter/
│  ├─ api.py          # API FastAPI + serve a Interface Web
│  ├─ units.py        # Lógica de conversão e sinônimos
│  └─ __init__.py     # Exporta funções principais
├─ web/
│  ├─ index.html      # Interface Web
│  ├─ app.js          # Lógica do frontend
│  └─ style.css       # Estilos
├─ requirements.txt   # Dependências Python
└─ README.md
```

## Como executar
1) Configurar ambiente (Windows PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2) Iniciar API + Web (recomendado):
```powershell
python -m converter.api
```
Acesse:
- Interface Web: http://localhost:8000/
	(Abra sempre pela raiz "/" e não por "/static/index.html".)

## Como utilizar
### Via Interface Web
- Abra http://localhost:8000/
- Escolha a categoria, unidades e informe o valor
- Clique em Converter para ver o resultado

## Personalização rápida
- Adicionar unidades/sinônimos: edite `converter/units.py` em `CATEGORIES` e `SYNONYMS` e ajuste as funções de conversão quando necessário.
- Alterar rótulos do frontend: edite `web/app.js` em `UNIT_OPTIONS`.
- Mudar porta/host (desenvolvimento):
	```powershell
	uvicorn converter.api:app --reload --port 8000 --host 0.0.0.0
	```
- A documentação pública da API está desativada (sem `/docs`).
- Evite abrir a UI por `/static/index.html`; use sempre `http://localhost:8000/`.

## Interface
Adicione aqui um print/screenshot da interface (o autor fará a captura).

## Autor
GustavoQ-Mateus

Projeto desenvolvido para aprendizado e prática em desenvolvimento web. Este projeto é fornecido tal como está, sem garantias. Adapte livremente conforme sua necessidade.

