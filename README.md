# Stereo 3D Reconstruction
### Reconstrucción y medición de un Ferrari de LEGO

A partir de fotografías estéreo tomadas desde distintas posiciones, reconstruimos una nube 3D y medimos el objeto en milímetros. El trabajo recorre calibración, disparidad, estimación de pose, fusión de vistas y filtrado de puntos.

**García, González y Turkie** · Visión Artificial, UdeSA · octubre de 2026.

![Reconstrucción del Ferrari y caja de medición](figures/measurement.png)

[Informe](docs/informe.pdf) · [Notebook liviano](main_sin_salidas.ipynb) · [Nube final](ferrari.ply)

## Reconstrucción

Utilizamos 25 pares de calibración y 15 vistas estéreo del objeto. Comparamos **StereoBM, SGBM y CREStereo**; la pose se obtiene con ChArUco y solvePnP. La nube se procesa con Open3D mediante recorte, vóxeles, filtrado de outliers y DBSCAN, y se estudia el efecto de ICP.

La nube entregada tiene **299.841 puntos**. Estas medidas se obtuvieron del PLY con PCA en XY y recorte del 0,1 % en cada extremo:

| Dimensión | Medida | Referencia del trabajo | Error |
| --- | ---: | ---: | ---: |
| Largo | 291,5 mm | 290,0 mm | +0,53 % |
| Ancho | 129,0 mm | 120,0 mm | +7,49 % |
| Alto | 79,9 mm | 80,0 mm | −0,10 % |

La medición verifica el archivo entregado; no constituye una validación física independiente. El mayor error aparece en el ancho.

## Revisar el resultado

La nube se puede medir sin cámara ni modelos:

~~~sh
uv run --no-project --python 3.11.18 --with numpy==1.26.4 python scripts/medir_ply.py
~~~

Para ejecutar la reconstrucción completa, consultar el [entorno y los pasos del notebook](DOCUMENTACION.md). Requiere un entorno separado con OpenCV, Open3D y ONNX Runtime; CREStereo descarga modelos y algunas visualizaciones necesitan contexto gráfico.

Las figuras y el [notebook original](main.ipynb) conservan los resultados del equipo. Las bibliotecas, redes preentrenadas y ejemplos de la cátedra se identifican en la documentación.
