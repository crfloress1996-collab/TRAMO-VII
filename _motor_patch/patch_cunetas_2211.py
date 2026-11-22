"""Parche 22/11 (i) — Cunetas, 'Avance por sector': el sector se escribe en romanos (XIII, XIV, XV) y no 'Xiii'."""
O = "nombre=f\"Sector {o['nombre']}\""
N = "nombre=f\"Sector {str(o['nombre']).upper()}\""


def aplicar(motor):
    from pathlib import Path
    f = Path(motor) / 'dash_data.py'
    s = f.read_text(encoding='utf8')
    if N in s or O not in s:
        return []
    f.write_text(s.replace(O, N, 1), encoding='utf8')
    return ['dash_data.py']
