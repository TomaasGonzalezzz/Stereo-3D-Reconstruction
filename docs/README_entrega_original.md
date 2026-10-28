# TP2 - Reconstruccion 3D

Reconstruccion 3D de un Ferrari de Lego con la camara estereo + medicion en mm.

Todo esta en `main.ipynb`, se corre de arriba a abajo.

## Dependencias

Lo corrimos con Python 3.9.6 y:

```
pip install numpy==1.26.4 opencv-python==4.11.0.86 open3d==0.18.0 onnxruntime==1.19.2 matplotlib==3.9.4
```

Ojo: open3d 0.18 no anda con numpy 2, y opencv 4.12 no anda con numpy < 2, por eso las versiones.

El modelo de CREStereo se baja solo la primera vez (queda en `~/.cache/stereodemo/models`).

## Datos

- `i308-calib/data/`: calibracion (`stereo_calibration.pkl`, `stereo_maps.pkl`), pares de calibracion y capturas del auto sobre el ChArUco
- `code_examples/stereodemo_disp_example/`: codigo de la catedra para CREStereo

## Salida

- `ferrari.ply`: nube final (binario)
- `figures/`: figuras del informe (las genera el notebook)

Medida del auto: 291.5 x 129.0 x 79.9 mm (largo x ancho x alto). Las oficiales son 290 x 120 x 80 mm.
