### Clonar el repositorio
```bash
git clone https://github.com/MartinezRobledo/AgenteIACAP.git
cd AgenteIACAP
```

### Crear entorno para la Azure Function
```bash
py -3.10 -m venv .venv
.venv\Scripts\Activate
```

### Instalar Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Instalar dependencias
```bash
poetry install
```

### Ejecutar Function
```bash
func start
```
