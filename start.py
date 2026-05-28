import os
import sys
import socket
import threading
import time
import datetime
from pathlib import Path

# Corrige erro Unicode no Agendador do Windows
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"

sys.path.insert(0, str(BACKEND_DIR))

# Debug simples
with open(BASE_DIR / "start_debug.txt", "a", encoding="utf-8") as f:
    f.write(f"{datetime.datetime.now()} - start.py executado\n")

# Credenciais
os.environ["HEMO_LOGIN"] = "rlc"
os.environ["HEMO_SENHA"] = "hemo2016"
os.environ["CLINUX_LOGIN"] = "Dicomvix"
os.environ["CLINUX_SENHA"] = "imagem"


def porta_em_uso(porta=5055):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", porta))
            return False
        except OSError:
            return True


if porta_em_uso():
    print("Porta 5055 já ocupada. Monitor já está rodando.", flush=True)
    sys.exit(0)


try:
    from app import app
    print("App carregado com sucesso!", flush=True)
except Exception as e:
    print(f"Erro ao importar app: {repr(e)}", flush=True)
    sys.exit(1)


def iniciar_robo():
    time.sleep(5)
    try:
        print("Iniciando robo...", flush=True)

        from scheduler import iniciar_scheduler, ciclo_exames

        iniciar_scheduler()

        print("Robo/Scheduler iniciado com sucesso.", flush=True)

        time.sleep(60)
        print("Forcando primeiro ciclo de exames...", flush=True)
        ciclo_exames()

        while True:
            time.sleep(60)

    except Exception as e:
        print(f"Erro ao iniciar robo/scheduler: {repr(e)}", flush=True)

robo_thread = threading.Thread(target=iniciar_robo)
robo_thread.start()


if __name__ == "__main__":
    print("Servidor iniciando...", flush=True)
    print("Dashboard: http://127.0.0.1:5055", flush=True)
    print("=" * 60, flush=True)

    app.run(
        host="127.0.0.1",
        port=5055,
        debug=False,
        use_reloader=False
    )
