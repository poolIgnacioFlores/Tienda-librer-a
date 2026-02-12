# Manga Shop (Flask)

Proyecto web simple en **Python + Flask** **Git**

## 1) Requisitos
- **Python 3.10+** instalado (recomendado 3.11 o 3.12)
- Windows: usar **PowerShell**

## 2) Cómo ejecutarlo (Windows / PowerShell)

### A. Entra a la carpeta del proyecto
```powershell
cd manga_shop
```

### B. Crea un entorno virtual
```powershell
python -m venv .venv
```

### C. Activa el entorno virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell te bloquea scripts:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Luego vuelve a activar.

### D. Instala dependencias
```powershell
pip install -r requirements.txt
```

### E. Crea la BD y datos de ejemplo
```powershell
python seed.py
```

### F. Corre la web
```powershell
python run.py
```

Abre: http://127.0.0.1:5000

---

## 3) Usuario admin de prueba
- Email: **admin@pool.local**
- Password: **admin123**

---

## 4) Rutas
- Home: `/`
- Catálogo: `/catalog`
- Categoría: `/category/<slug>`
- Detalle: `/book/<id>`
- Buscar: `/search?q=...`
- Carrito: `/cart`
- Checkout (falso): `/checkout`
- About: `/about`
- Contact: `/contact`
- Auth: `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/profile`
- Admin: `/admin`, `/admin/books`, `/admin/books/new`, `/admin/books/<id>/edit`, `/admin/books/<id>/delete`

