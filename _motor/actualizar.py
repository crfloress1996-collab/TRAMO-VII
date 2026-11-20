"""Actualiza el Tablero Tramo VII desde la PC (lo llama ACTUALIZAR_TABLERO.bat).

1. Lee los Excel de cada frente (carpeta 01 CONTROL DE PRODUCCIÓN (Last Planner)) con dash_data.py.
2. Junta las restricciones nuevas de los Excel con las que ya están en el tablero (rx_vivas.json).
3. Arma la página (index.html) y la copia a 00 TABLET\\WEB TABLERO.
4. Si hay Git, la sube a GitHub (https://crfloress1996-collab.github.io/TRAMO-VII/).
0. Antes de todo, si hay Git, baja de GitHub las mejoras del motor (carpeta _motor_patch del repositorio) y las aplica
   a tablero.html y dash_data.py. Así los cambios que hace Claude llegan solos a la PC con el .bat.
La página de Claude se actualiza aparte (pedírselo a Claude: usa el data.json que deja este script).
uso: python actualizar.py [carpeta_last_planner]
"""
import os, sys, json, shutil, subprocess, datetime as dt, time
from pathlib import Path

MOTOR = Path(__file__).resolve().parent
WEB = MOTOR.parent                      # 00 TABLET\WEB TABLERO
ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else WEB.parent.parent   # 01 CONTROL DE PRODUCCIÓN (Last Planner)
REPO_URL = 'https://github.com/crfloress1996-collab/TRAMO-VII.git'
REPO = MOTOR / 'repo_github'
ENV = {**os.environ, 'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8'}


def paso(n, t):
    print(f'\n[{n}/4] {t}', flush=True)


def correr(cmd, cwd=None, mostrar=True):
    r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if mostrar and r.stdout.strip():
        print('   ' + r.stdout.strip().replace('\n', '\n   '))
    return r


def mejoras_del_motor():
    """Paso 0: git pull del repositorio y aplica los parches de _motor_patch (cada uno tiene aplicar(motor); no repiten si ya están)."""
    if shutil.which('git') is None:
        return
    if not (REPO / '.git').exists():
        correr(['git', 'clone', '--depth', '1', REPO_URL, str(REPO)], mostrar=False)
    if not (REPO / '.git').exists():
        return
    correr(['git', 'checkout', '--', '.'], cwd=REPO, mostrar=False)
    correr(['git', 'pull', '-q', '--rebase'], cwd=REPO, mostrar=False)
    # este mismo archivo: si en GitHub hay una versión nueva, queda lista para la próxima vez
    nuevo = REPO / '_motor' / 'actualizar.py'
    if nuevo.exists() and nuevo.read_bytes() != Path(__file__).read_bytes():
        shutil.copy(nuevo, Path(__file__))
    pdir = REPO / '_motor_patch'
    if not pdir.exists():
        return
    import importlib.util
    hechos = []
    for f in sorted(pdir.glob('*.py')):
        try:
            spec = importlib.util.spec_from_file_location(f.stem, f)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            if hasattr(m, 'aplicar'):
                r = m.aplicar(MOTOR)
                if r:
                    hechos.append(f"{f.stem} ({', '.join(r)})")
        except Exception as e:
            print(f'   Aviso: la mejora {f.name} no se pudo aplicar: {e}')
    if hechos:
        print('   Mejoras aplicadas: ' + ' · '.join(hechos))


def main():
    t0 = time.time()
    print('=' * 64)
    print(' TABLERO TRAMO VII - actualizacion desde los Excel de los frentes')
    print('=' * 64)
    print(' Carpeta de los Excel:', ROOT)
    if not (ROOT / '09 Control por frentes').exists():
        print('\n ERROR: no encuentro la carpeta "09 Control por frentes" dentro de', ROOT)
        return 1

    print('\n[0/4] Buscando mejoras del tablero en GitHub...', flush=True)
    try:
        mejoras_del_motor()
    except Exception as e:
        print('   Aviso: no se pudieron revisar las mejoras:', e)

    paso(1, 'Leyendo los partes de cada frente (tarda 1 a 2 minutos)...')
    data = MOTOR / 'data.json'
    r = correr([sys.executable, str(MOTOR / 'dash_data.py'), str(ROOT), str(data)])
    if r.returncode != 0 or not data.exists():
        print('\n ERROR al leer los Excel. Revisa que esten guardados y que no tengan errores.')
        print('   ' + (r.stderr or '')[-1500:].replace('\n', '\n   '))
        return 1
    d = json.load(open(data, encoding='utf-8'))
    est = d['estado']
    print(f"   Semana {est.get('semana')} · ultimo parte {est.get('prod', {}).get('corte')}")

    paso(2, 'Juntando restricciones...')
    viv_p = MOTOR / 'rx_vivas.json'
    vivas = json.load(open(viv_p, encoding='utf-8')) if viv_p.exists() else []
    por_id = {x['id']: x for x in vivas}
    excel = {x['id']: x for x in d.get('restricciones', [])}
    nuevas = [x for k, x in excel.items() if k not in por_id]
    vivas += nuevas
    levantadas = 0
    hoy = dt.date.today().isoformat()
    for x in vivas:
        if x['id'] not in excel and x.get('origen') == 'Excel del frente' and x.get('estado') != 'Levantada':
            x['estado'] = 'Levantada'
            x.setdefault('levantada', hoy)
            levantadas += 1
    json.dump(vivas, open(viv_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'   {len(nuevas)} nuevas · {levantadas} ya no estan en los Excel (pasan a Levantada) · {len(vivas)} en total')

    paso(3, 'Armando la pagina...')
    idx = MOTOR / 'index.html'
    r = correr([sys.executable, str(MOTOR / 'gen_web.py'), str(MOTOR / 'tablero.html'), str(data), str(idx), str(viv_p)], mostrar=False)
    if r.returncode != 0:
        print('\n ERROR al armar la pagina:\n   ' + (r.stderr or '')[-1500:])
        return 1
    shutil.copy(idx, WEB / 'index.html')
    print('   Listo:', WEB / 'index.html')

    paso(4, 'Subiendo a GitHub...')
    if shutil.which('git') is None:
        print('   Git no esta instalado: la pagina de GitHub NO se actualizo.')
        print('   (Instalar una vez desde https://git-scm.com/download/win y volver a correr este archivo.)')
    else:
        if not (REPO / '.git').exists():
            print('   Primera vez: descargando el repositorio...')
            r = correr(['git', 'clone', '--depth', '1', REPO_URL, str(REPO)])
            if r.returncode != 0:
                print('   No se pudo descargar el repositorio:\n   ' + r.stderr[-800:])
        if (REPO / '.git').exists():
            correr(['git', 'pull', '-q', '--rebase'], cwd=REPO, mostrar=False)
            shutil.copy(idx, REPO / 'index.html')
            correr(['git', 'add', 'index.html'], cwd=REPO, mostrar=False)
            msg = f"Tablero: partes al {est.get('prod', {}).get('corte')} (actualizado desde la PC)"
            r = correr(['git', '-c', 'user.name=crfloress1996-collab', '-c', 'user.email=crfloress1996@gmail.com', 'commit', '-q', '-m', msg], cwd=REPO, mostrar=False)
            if r.returncode != 0 and 'nothing to commit' in (r.stdout + r.stderr):
                print('   Sin cambios: GitHub ya tenia esta version.')
            else:
                r = correr(['git', 'push', '-q'], cwd=REPO, mostrar=False)
                if r.returncode == 0:
                    print('   Subido. En 1 a 2 minutos se ve en https://crfloress1996-collab.github.io/TRAMO-VII/')
                else:
                    print('   No se pudo subir (la primera vez pide iniciar sesion en GitHub):\n   ' + r.stderr[-800:])
    print(f'\n Terminado en {time.time() - t0:.0f} s.')
    print(' La pagina de Claude se actualiza aparte: pidele a Claude "actualiza el tablero".')
    return 0


if __name__ == '__main__':
    sys.exit(main())
