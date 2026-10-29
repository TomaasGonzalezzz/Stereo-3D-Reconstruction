# TP2 - Reconstrucción 3D estéreo multivista

Trabajo grupal de **I308 - Visión Artificial**, Universidad de San Andrés.
**Autores: García, González y Turkie.** Informe original fechado el 24 de octubre de 2026.

Reconstrucción y medición de un Ferrari de LEGO a partir de fotografías estéreo: calibración,
rectificación, disparidad, pose mediante ChArUco, fusión de nubes y limpieza con Open3D.

[Consigna](docs/consigna.pdf) · [Informe](docs/informe.pdf) ·
[Notebook liviano](main_sin_salidas.ipynb) · [Notebook original con resultados](main.ipynb) ·
[Descargar nube final](https://github.com/TomaasGonzalezzz/i308-tp2-reconstruccion-3d/raw/refs/heads/main/ferrari.ply)

![Reconstrucción final y caja de medición, figura original del notebook](figures/measurement.png)

## Qué contiene la resolución

- Calibración con **25 pares** de checkerboard y capturas del objeto desde **15 vistas estéreo**.
- Comparación de **StereoBM, SGBM y CREStereo**.
- Transformación de disparidad a nube local; pose del tablero con ChArUco/solvePnP y marco global.
- Corrección de disparidad basada en el tablero, filtro de bordes y evaluación de su efecto.
- Recorte, reducción por vóxeles, filtrado de outliers, DBSCAN y evaluación de ICP.
- Medición robusta en milímetros mediante PCA y percentiles; nube final `ferrari.ply`.

![Comparación de métodos de disparidad, figura original del notebook](figures/disparity_methods.png)

## Resultado entregado

La nube final contiene **299.841 puntos**. La tabla se comprobó leyendo el PLY original con el
mismo criterio de medición del notebook (PCA en XY y recorte del 0,1% en cada extremo).
Los tamaños de referencia son los usados por el equipo para el LEGO Ferrari FXX K, set 42212.

| Dimensión | Medida en el PLY | Referencia del trabajo | Error relativo |
|---|---|---|---|
| Largo | 291.5 mm | 290.0 mm | +0.53% |
| Ancho | 129.0 mm | 120.0 mm | +7.49% |
| Alto | 79.9 mm | 80.0 mm | -0.10% |

Esta comprobación verifica la medición del archivo entregado; **no vuelve a ejecutar CREStereo
ni toda la reconstrucción**, ni constituye una validación física independiente. El informe y
el notebook conservan las observaciones, ablaciones y limitaciones originales.

## Archivos

```text
main.ipynb                          Resolución original con salidas
main_sin_salidas.ipynb              Mismas celdas, copia liviana para GitHub
ferrari.ply                         Nube final binaria, descarga directa
i308-calib/data/calib/              25 pares de calibración del equipo
i308-calib/data/captures/           15 pares de capturas del Ferrari
i308-calib/data/*.pkl               Calibración y mapas de rectificación originales
code_examples/                     Adaptadores de disparidad incluidos en la entrega
material_catedra/                   Datasets y ejemplos originales de la consigna
docs/consigna.pdf                   Enunciado
docs/informe.pdf                    Informe del equipo
docs/calib-tool.md                  Guía de uso de la herramienta de calibración
docs/README_entrega_original.md     Instrucciones originales del equipo
docs/origen_archivos.json           Archivos de origen y hashes SHA-256
docs/figuras_notebook.json          Procedencia de las figuras extraídas
figures/                           12 figuras guardadas en el notebook original
scripts/medir_ply.py                Verificación de estructura y medición del PLY
resultados/medicion_ply.json         Resultado de esa comprobación
```

Las figuras se recuperaron de las salidas existentes del notebook, sin regenerar ni cambiar
sus resultados. Los ejemplos de cátedra están separados para evitar sobrescribir las versiones
incluidas con la resolución. Ambos notebooks deben abrirse desde la raíz del repo para que
las rutas relativas a datos y `code_examples/` funcionen.

## Verificar la nube sin modelos ni cámara

Con [uv](https://docs.astral.sh/uv/), desde la raíz:

```bash
git clone https://github.com/TomaasGonzalezzz/i308-tp2-reconstruccion-3d.git
cd i308-tp2-reconstruccion-3d
uv run --no-project --python 3.11.18 --with numpy==1.26.4 python scripts/medir_ply.py
```

El script valida la cabecera y tamaño del PLY, comprueba coordenadas finitas y guarda medidas
en JSON. Solo acepta el formato XYZ double/RGB uchar del archivo entregado. No carga pickles,
no descarga pesos y no abre ventanas 3D.

## Ejecutar el notebook original

El equipo declaró **Python 3.9.6** y estas dependencias:

```text
numpy==1.26.4
opencv-python==4.11.0.86
open3d==0.18.0
onnxruntime==1.19.2
matplotlib==3.9.4
```

Preparar un entorno separado; `requirements.txt` conserva esas versiones y agrega Jupyter:

```bash
uv venv --python 3.9 --seed
uv pip install -r requirements.txt
uv run --no-project jupyter lab
```

Abrir `main.ipynb` y ejecutar de arriba abajo. La versión de Python instalada con `--python 3.9`
puede ser un parche posterior a 3.9.6. La publicación no certifica la reejecución integral en
todos los sistemas: Open3D requiere contexto gráfico para las vistas y CREStereo descarga
modelos la primera vez a `~/.cache/stereodemo/models`. Ver instrucciones originales en
[README de la entrega](docs/README_entrega_original.md).

Usar los requirements de la raíz para el notebook, no los requirements genéricos de cada
carpeta de ejemplos, que declaran otras versiones de OpenCV. No instalar este entorno encima
del de VisionX o el TP1. Para nuevas capturas, consultar [calib-tool.md](docs/calib-tool.md).

## Créditos y procedencia

Trabajo original de **García, González y Turkie**; publicación de Tomás González.
Consigna, datasets de Buda y ejemplos: material de la cátedra I308, UdeSA.
Herramienta de calibración: [udesa-vision/i308-calib](https://github.com/udesa-vision/i308-calib).
Los adaptadores de disparidad incluidos utilizan modelos y código de
[stereodemo](https://github.com/nburrus/stereodemo); se conserva su contenido y referencia.

Se preservan sin cambios los archivos de ambos ZIP y la guía recibida. Solo se reorganizaron
PDF/README de la entrega para distinguir consigna y resolución. La copia liviana del notebook,
las figuras extraídas, este README y el script de medición se agregaron para facilitar lectura
y consulta. No se atribuye al equipo la implementación de las redes preentrenadas ni de las
bibliotecas utilizadas, ni se atribuye todo el TP a quien publica este repositorio.
