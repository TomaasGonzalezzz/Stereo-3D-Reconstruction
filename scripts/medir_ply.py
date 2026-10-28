"""Comprueba y mide el PLY entregado sin ejecutar modelos, pickles ni Open3D."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def read_submission_ply(path):
    """Lee el formato binario XYZ double + RGB uchar usado en esta entrega."""
    with path.open("rb") as stream:
        header = []
        for _ in range(100):
            line = stream.readline().decode("ascii").strip()
            header.append(line)
            if line == "end_header":
                break
        else:
            raise ValueError("Cabecera PLY inválida")
        if "format binary_little_endian 1.0" not in header:
            raise ValueError("Este lector solo comprueba el formato de ferrari.ply")
        properties = [line for line in header if line.startswith("property ")]
        expected = ["property double x", "property double y", "property double z",
                    "property uchar red", "property uchar green", "property uchar blue"]
        if properties != expected:
            raise ValueError("Propiedades distintas del PLY original")
        count = int(next(line.split()[-1] for line in header if line.startswith("element vertex ")))
        dtype = np.dtype([("x", "<f8"), ("y", "<f8"), ("z", "<f8"),
                          ("red", "u1"), ("green", "u1"), ("blue", "u1")])
        payload = stream.read()
        if len(payload) != count * dtype.itemsize:
            raise ValueError("Tamaño binario distinto de la cantidad de vértices declarada")
        vertices = np.frombuffer(payload, dtype=dtype, count=count)
    points = np.column_stack([vertices[axis] for axis in ["x", "y", "z"]])
    if not np.isfinite(points).all():
        raise ValueError("Coordenadas no finitas")
    return points


def measure(points, trim):
    # Mismo criterio del notebook: PCA en XY y percentiles, tablero Z=0.
    _, _, axes = np.linalg.svd(points[:, :2] - points[:, :2].mean(axis=0), full_matrices=False)
    uv = (points[:, :2] - points[:, :2].mean(axis=0)) @ axes.T
    low, high = np.percentile(uv, [trim, 100 - trim], axis=0)
    return [*(high - low), -np.percentile(points[:, 2], trim)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ply", type=Path, default=ROOT / "ferrari.ply")
    parser.add_argument("--output", type=Path, default=ROOT / "resultados/medicion_ply.json")
    parser.add_argument("--trim", type=float, default=0.1)
    args = parser.parse_args()
    if not 0 <= args.trim < 50:
        parser.error("trim debe estar entre 0 y 50 (excluido)")
    points = read_submission_ply(args.ply)
    sizes = measure(points, args.trim)
    real = {"largo": 290.0, "ancho": 120.0, "alto": 80.0}
    result = {
        "source": "ferrari.ply entregado; no se vuelve a ejecutar la reconstrucción",
        "vertices": len(points), "trim_percent": args.trim,
        "measured_mm": dict(zip(real, sizes)), "reference_mm": real,
        "relative_error_percent": {k: 100 * (v - real[k]) / real[k] for k, v in zip(real, sizes)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
