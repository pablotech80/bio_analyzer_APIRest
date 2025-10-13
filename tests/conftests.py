import os

from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto, siempre, incluso en subprocesos
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOTENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(dotenv_path=DOTENV_PATH, override=True)

# Exportar manualmente para pytest (algunos runners necesitan esto)
if "OPENAI_API_KEY" in os.environ:
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    print(
        f"✅ OPENAI_API_KEY forzado en entorno (pytest): {os.environ['OPENAI_API_KEY'][:10]}..."
    )
else:
    print("🚨 Aún no se detecta OPENAI_API_KEY al inicio de pytest")

    print("🧪 Diagnóstico de entorno pytest + dotenv")
    print(f"📁 Ruta raíz: {ROOT_DIR}")
    print(f"📄 Ruta del .env: {DOTENV_PATH}")

# Forzar recarga de variables con override
if os.path.exists(DOTENV_PATH):
    success = load_dotenv(dotenv_path=DOTENV_PATH, override=True)
    print(f"✅ load_dotenv ejecutado, success={success}")
else:
    print("🚨 No se encontró el archivo .env en la ruta indicada.")

    # Mostrar todas las variables detectadas con OPENAI
    print("🔍 Variables OPENAI visibles en este entorno:")

for k, v in os.environ.items():
    if "OPENAI" in k:
        print(f"  {k}={v[:10]}...")

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print(f"✅ OPENAI_API_KEY cargada: {api_key[:10]}...")
else:
    print("🚨 OPENAI_API_KEY sigue vacía en os.environ.")
