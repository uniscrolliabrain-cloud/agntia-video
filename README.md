# Agntia-video

Un estudio de podcast en tu navegador: importa cámara, avatares, audios y B-roll; conversa sobre el briefing; revisa el montaje y exporta el episodio y sus clips verticales.

**Versión 0.2 (MVP), para Windows y servidores Linux.** Funciona sin claves para cargar archivos, editar cortes, previsualizar y exportar. DeepSeek y Gemini son opcionales y se configuran después. No incluye claves ni créditos. Incluye un pequeño modelo RNNoise para limpiar voz localmente, sin API.

## Qué puedes hacer

- Crear proyectos persistentes y subir archivos desde el navegador, arrastrarlos o importar la carpeta `inbox/` del equipo que ejecuta el servidor.
- Clasificar material como diálogo, avatar, audio o B-roll.
- Elegir imagen y audio independientes en cada corte, con tiempos separados; reordenar y recortar segmentos.
- Conversar con DeepSeek para construir el briefing y proponer o modificar el plan de edición.
- Analizar vídeo y audio con Gemini en bloques de 3 minutos. Se envían proxies reducidos, se guardan transcripciones y momentos destacados, y se reutiliza la caché por contenido/modelo/idioma.
- Elegir idioma del material (automático, español, inglés, francés) y subtítulos (sin, original o traducción a uno de esos idiomas).
- Previsualizar el podcast y cada clip antes de exportar. MP4/H.264, podcast 1920×1080, clips 1080×1920. Subtítulos incrustados y SRT descargable cuando se activan.
- Normalizar el audio del montaje, conservar la imagen completa con bandas o recortar al centro.
- Mejorar la voz con IA local RNNoise o limpieza clásica, con intensidad ajustable.
- Añadir música MP3/WAV/M4A, ajustar volumen e inicio, repetirla y bajar su nivel automáticamente cuando habla alguien.
- Detectar golpes musicales, visualizar marcadores y acercar las transiciones existentes a beats cercanos, con margen elegible y opción de deshacer.
- Descargar el plan de edición en JSON. Los originales se conservan; cada render crea archivos nuevos.

## Arranque en Windows

Requisitos: **Python 3.11+**, **Git** y **FFmpeg con ffprobe en el PATH**. Puedes instalar FFmpeg con `winget install --id Gyan.FFmpeg -e` y volver a abrir PowerShell. Comprueba `ffmpeg -version` y `ffprobe -version`.

Clona este repositorio desde su botón **Code** y abre PowerShell en esa carpeta:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn agntia.app:app --host 127.0.0.1 --port 8000
```

Abre **http://127.0.0.1:8000**. No hace falta activar la venv ni cambiar la política de ejecución de PowerShell.

1. Crea un proyecto y añade tus grabaciones. Para importar una carpeta, coloca los archivos directamente en `inbox/` junto al código y pulsa **Importar carpeta**. En un servidor, esa carpeta pertenece al servidor, no a tu PC; usa **Añadir archivos** para subirlos desde Windows.
2. Asigna los tipos de material. Pulsa **Añadir corte** y elige sus tiempos. Si usas B-roll con diálogo, selecciona la imagen del B-roll y la pista de audio del diálogo, indicando dónde empieza cada una.
3. Escribe tu briefing. Con claves configuradas puedes analizar con Gemini y conversar con el agente para obtener propuestas de cortes.
4. Añade los clips: sus tiempos corresponden al episodio **resultante**, después de los cortes, no a los archivos originales.
5. Guarda, genera previsualización, revisa los resultados en **Entregas**, pide cambios o ajusta los cortes y exporta.

## Voz, MP3 y edición al ritmo de los beats

En el panel **Sonido**:

1. En **Mejora de voz**, elige **Mejora con IA · RNNoise local**, ajusta la intensidad y genera una previsualización. Usa la biblioteca para escuchar el original y el reproductor para comparar el resultado. Se reduce ruido con una red neuronal; se añade claridad y compresión suave. No es el motor de CapCut y no reconstruye voz saturada ni garantiza eliminar reverberación. La limpieza clásica usa filtros de señal, sin IA.
2. Pulsa **Añadir MP3 / audio**. La pista se clasifica como música y se selecciona automáticamente; puedes cambiarla por cualquier archivo con audio de la biblioteca. Ajusta volumen, inicio dentro de la canción, repetición y fundido. **Bajar música cuando hay voz** aplica compresión sidechain. Hay una sola banda sonora independiente, además del audio del diálogo.
3. Pulsa **Detectar beats**. El análisis es local y no necesita claves. Muestra golpes percutivos estimados y BPM aproximados; no todos los golpes coinciden con el pulso musical. El detector funciona mejor con percusión clara y acepta canciones de hasta dos horas.
4. Prepara al menos dos cortes y pulsa **Ajustar cortes a beats**. Se mueven sus finales a golpes cercanos dentro de 0,12/0,20/0,40 s (según el margen elegido), sin cambiar los puntos de inicio de las fuentes, la duración total del episodio ni los tiempos de los clips. Se omiten movimientos que excedan el material o dejen cortes demasiado breves. No se añaden cortes nuevos dentro de frases. Puedes **Deshacer ajuste** mientras el montaje siga siendo el mismo.
5. Genera una previsualización, revisa que ninguna frase haya quedado cortada y exporta. Los clips conservan la posición musical que les corresponde dentro del episodio; si la canción termina sin repetición, el diálogo continúa. Los fundidos se aplican al principio y al final de cada entrega.

La IA se ejecuta con el filtro **arnndn** de FFmpeg y el modelo incluido. Si tu FFmpeg no lo ofrece, la interfaz desactiva esa opción; instala una compilación completa con `arnndn` o usa la limpieza clásica. No requiere GPU, DeepSeek ni Gemini. El audio y los originales no se suben a proveedores para estas funciones. La música se decodifica temporalmente a PCM para evitar desfases de repetición por el padding del MP3; reserva espacio para esos temporales.

El ajuste al beat cambia el contenido de los cortes: se orienta a recursos, intros y montajes con margen. Revisa el diálogo. La precisión visual está limitada por los 25 fotogramas por segundo del render. Los marcadores muestran la canción completa, y el ajuste respeta su inicio y repetición configurados.

## Claves para más adelante

Edita `.env` localmente (nunca lo subas a GitHub) y reinicia el servidor:

```dotenv
DEEPSEEK_API_KEY=tu_clave
DEEPSEEK_MODEL=deepseek-chat
GEMINI_API_KEY=tu_clave
GEMINI_MODEL=gemini-2.5-flash
```

Los nombres de modelo son configurables: elige modelos disponibles en tus cuentas. La aplicación no verifica precios ni garantiza una tarifa concreta. No llama a las APIs al arrancar: analizar, conversar o traducir requiere una acción explícita. **Analizar envía vídeo/audio reducido a Google; el agente y las traducciones envían texto a DeepSeek.** No hay telemetría propia. Las cachés guardan texto de los proyectos en `data/` y no caducan automáticamente.

Sin claves no se simulan decisiones de IA: puedes trabajar manualmente y los botones correspondientes explican cómo configurar el proveedor. Los subtítulos necesitan transcripción de Gemini; la traducción usa DeepSeek. Para clips con conversación en un audio separado, analiza también ese audio.

## Servidor Linux

Instala Python 3.11+, FFmpeg y ffprobe con el gestor de tu sistema. Desde el repositorio:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
cp .env.example .env
# Configura AGNTIA_ACCESS_TOKEN con un secreto largo en .env antes de acceso remoto.
.venv/bin/python -m uvicorn agntia.app:app --host 0.0.0.0 --port 8000 --workers 1
```

Para uso remoto configura **AGNTIA_ACCESS_TOKEN**, HTTPS en el proxy inverso y límites de subida adecuados. El navegador pide ese token y lo guarda en cookie HttpOnly. Sin token, el backend rechaza clientes remotos. No expongas el puerto sin HTTPS; el estudio está pensado para un propietario de confianza, no para alojar usuarios independientes. Detrás de un proxy, configura correctamente la confianza en sus cabeceras y conserva el host original para la comprobación de origen. No añadas `--workers` mayor que 1: la cola de trabajo es de un proceso.

Alternativa con Docker Compose (Docker Desktop en Windows o Docker Engine en Linux):

```bash
cp .env.example .env
# Añade AGNTIA_ACCESS_TOKEN a .env: Docker llega al backend desde una IP no local.
docker compose up --build -d
```

El puerto se publica solo en `127.0.0.1:8000`. Para un servidor remoto usa un túnel SSH (`ssh -L 8000:127.0.0.1:8000 usuario@servidor`) o tu proxy HTTPS. No requiere GPU. Se necesitan CPU, espacio para originales y renders, y conexión para las APIs. Haz copia de seguridad de `data/` y `.env` por separado del repositorio.

## Carpetas y datos

```text
agntia/             Backend, proveedores y aplicación web
data/              Proyectos, originales, análisis, cachés y entregas (ignorado por Git)
inbox/             Carpeta de entrada en el equipo servidor (ignorada por Git)
tests/             Pruebas de API, contratos de IA y render real con FFmpeg
docs/              Arquitectura, decisiones y referencias
```

`AGNTIA_DATA_DIR` y `AGNTIA_INBOX_DIR` permiten cambiar rutas. La importación copia archivos del nivel superior, ignora enlaces simbólicos y formatos no admitidos, y evita duplicados por SHA-256 dentro del proyecto. El límite por archivo se configura con `AGNTIA_MAX_UPLOAD_GB` (10 por defecto). También necesitas suficiente espacio temporal para las subidas multipart y los renders. Los archivos no se borran automáticamente y la cola se procesa de uno en uno. Un trabajo interrumpido al reiniciar queda marcado para que lo vuelvas a lanzar.

**GitHub contiene el código; la aplicación recibe las grabaciones.** Por tamaño y privacidad, vídeos, audios, claves, proyectos y cachés quedan excluidos del historial público. Comparte grabaciones mediante el almacenamiento del servidor si lo necesitas.

## Límites de esta versión

- La sincronización entre pistas es manual, mediante inicios de imagen/audio. No mezcla varias voces simultáneas, no hace multicámara simultáneo ni detecta automáticamente qué cámara corresponde a cada voz.
- El B-roll sustituye la imagen de un corte mientras mantiene el audio elegido; no hay capas visuales, transiciones, doblaje ni generación de avatares. Sí admite una pista musical mezclada con el diálogo.
- Los tiempos de Gemini son aproximados a nivel de frase. Revisa la transcripción, los recortes y los subtítulos. No hay alineación fonética ni subtítulos karaoke. Si recortas parte de una frase, su texto sigue siendo el de la frase original: ajusta el corte al límite de frase para evitar inconsistencias.
- La elección de momentos depende del análisis y del briefing. Sin análisis, el agente debe explicarlo y no atribuir calidad al material que no ha visto. Los planes de IA se validan antes de guardarse; el agente modifica el plan, pero nunca renderiza sin pulsar un botón.
- Encuadre fijo (imagen completa o centro), sin seguimiento de caras. Las previsualizaciones se renderizan a baja resolución; no es un editor de arrastrar clips sobre una pista gráfica en tiempo real.
- Diseñado para un único servidor y propietario. No hay cuentas multiusuario, cuotas por usuario, reanudación de subidas, facturación ni almacenamiento S3 incluido.

## Desarrollo y pruebas

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
```

FFmpeg/ffprobe se requieren para las pruebas de integración. Las APIs de pago se prueban con respuestas controladas, sin gastar créditos. Para pruebas de navegador: `python -m playwright install chromium` y `python tests/browser_smoke.py`. El test arranca y detiene su propio servidor HTTP en un puerto local y usa datos temporales; no necesitas arrancar el estudio manualmente. Puedes usar un navegador existente con `AGNTIA_BROWSER_EXECUTABLE`. En GitHub Actions se ejecutan las pruebas y se guardan capturas de escritorio y móvil como artefactos.

## Referencias

Estudiamos [auto-editor](https://github.com/WyattBlue/auto-editor), [WhisperX](https://github.com/m-bain/whisperX) y [FunClip](https://github.com/modelscope/FunClip). Esta primera versión implementa su propio flujo sobre FFmpeg; no incorpora su código ni instala sus modelos. Consulta las [decisiones y referencias](docs/architecture.md). El código propio se publica bajo MIT. El modelo RNNoise tiene licencia BSD: consulta [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Los proveedores, FFmpeg y los medios tienen sus propias condiciones.
