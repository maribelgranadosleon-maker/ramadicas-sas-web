RAMADICAS S.A.S. — ENCUESTAS Y DASHBOARD (PROYECTO DEMOSTRATIVO SENA)

REQUISITOS
- Python 3.10 o superior
- Visual Studio Code recomendado
- Internet para cargar Chart.js y las fuentes visuales. La aplicación y la base SQLite funcionan localmente.

PASOS EN WINDOWS
1. Descomprime la carpeta ramadicas_sas_web en una ubicación fácil de encontrar.
2. Abre Visual Studio Code > Archivo > Abrir carpeta... > selecciona ramadicas_sas_web.
3. Abre Terminal > Nueva terminal.
4. Crea un entorno virtual:
   py -m venv .venv
5. Actívalo en PowerShell:
   .venv\\Scripts\\Activate.ps1
   Si PowerShell bloquea la activación, prueba en CMD:
   .venv\\Scripts\\activate.bat
6. Instala Flask:
   py -m pip install -r requirements.txt
7. Ejecuta:
   py app.py
8. Abre en tu navegador:
   http://127.0.0.1:5000
9. Llena el formulario y pulsa “Guardar respuesta”. La página recargará y actualizará las gráficas.
10. Para detener el servidor, vuelve a la terminal y pulsa Ctrl+C.

BASE DE DATOS
- Al iniciar por primera vez, se crea ramadicas.db en esta misma carpeta.
- SQLite guarda las respuestas en el computador; no necesitas instalar un servidor de base de datos.
- No borres ramadicas.db si quieres conservar los registros.
- Haz una copia de seguridad con la aplicación detenida.

IMPORTANTE
- Este proyecto es una plantilla académica/demostrativa; no es un sistema oficial ni está conectado a los sistemas de Ramadicas S.A.S.
- Antes de usar datos reales, pide autorización a la empresa, informa a los participantes del propósito y limita el acceso a la información. Para una demostración, usa nombres ficticios/códigos.
- No publiques el servidor de desarrollo de Flask directamente en internet. Para desplegarlo públicamente hay que configurar un hosting WSGI, variables de entorno, seguridad, HTTPS, permisos y una base de datos/almacenamiento adecuados.
- Cambia app.secret_key antes de cualquier despliegue y desactiva debug=True en producción.
- Los gráficos utilizan Chart.js desde un CDN, por eso requieren internet para dibujarse.
