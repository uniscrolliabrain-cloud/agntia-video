# Componentes de terceros

## Modelo RNNoise

`agntia/resources/rnnoise.rnnn` contiene el modelo estándar de Xiph RNNoise, convertido al formato del filtro FFmpeg `arnndn` y distribuido en [richardpl/arnndn-models](https://github.com/richardpl/arnndn-models).

- Archivo fuente: `std.rnnn`.
- Git blob fijado: `2c940d14b54486e50cdd188232a3f1cb75ec6af7`.
- [Contenido de esa versión](https://api.github.com/repos/richardpl/arnndn-models/git/blobs/2c940d14b54486e50cdd188232a3f1cb75ec6af7).
- El README del distribuidor identifica `std.rnnn` como el modelo originalmente incluido con Xiph RNNoise.
- Proyecto original: [xiph/rnnoise](https://github.com/xiph/rnnoise).
- Licencia BSD con tres condiciones: se conserva el aviso completo en [RNNOISE-LICENSE.txt](agntia/resources/RNNOISE-LICENSE.txt).

El modelo tiene su propia licencia y no queda relicenciado como MIT. El código original de Agntia-video sigue bajo MIT. El modelo se usa para reducir ruido de voz localmente; no genera voces ni envía grabaciones a una API.

## FFmpeg

Se utiliza como ejecutable externo. Su licencia y las de los códecs dependen de la compilación instalada. El Dockerfile instala el paquete FFmpeg de la distribución base. No se incorpora su código al paquete Python.
