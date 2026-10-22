"""Extrae las figuras reales del cuaderno ejecutado y crea una comparación de RMSE.

Se ejecuta después del notebook, no genera datos sintéticos ni reentrena modelos.
"""
from __future__ import annotations

import base64
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "stock_forecasting_executed.ipynb"
FIGURES = ROOT / "notebooks" / "reports" / "figuras"
REPORTS = ROOT / "notebooks" / "reports"

# Mismo orden que las gráficas mostradas en el cuaderno.
FIGURE_NAMES = [
    "01_precio_y_particiones.png",
    "02_velas_recientes.png",
    "03_medias_moviles.png",
    "04_perdida_entrenamiento_validacion.png",
    "05_rmse_por_epoca.png",
    "06_cierre_real_y_estimado.png",
    "07_dispersion_de_errores.png",
    "08_residuos_en_el_tiempo.png",
    "09_histograma_de_residuos.png",
    "10_autocorrelacion_de_residuos.png",
    "11_validacion_temporal.png",
]


def extract_notebook_figures() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    images = []
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        for output in cell.get("outputs", []):
            encoded = output.get("data", {}).get("image/png")
            if encoded:
                images.append(
                    base64.b64decode(
                        "".join(encoded) if isinstance(encoded, list) else encoded
                    )
                )

    if len(images) != len(FIGURE_NAMES):
        raise ValueError(
            f"Se esperaban {len(FIGURE_NAMES)} gráficas; "
            f"el cuaderno generó {len(images)}. Revisar el orden antes de publicar."
        )
    FIGURES.mkdir(parents=True, exist_ok=True)
    for filename, image_data in zip(FIGURE_NAMES, images):
        (FIGURES / filename).write_bytes(image_data)
        print(f"Figura guardada: {filename}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def plot_rmse_comparison() -> None:
    models = read_csv(REPORTS / "model_metrics.csv")
    baselines = read_csv(REPORTS / "baseline_metrics.csv")

    # Se reproduce el mismo criterio utilizado en el notebook: menor RMSE de validación.
    selected = min(models, key=lambda row: float(row["validacion_RMSE"]))
    labels = [
        "Último cierre",
        "Media móvil (20)",
        "Red seleccionada",
    ]
    values = [
        float(next(row["RMSE"] for row in baselines
                   if row["modelo"] == "Último cierre observado")),
        float(next(row["RMSE"] for row in baselines
                   if row["modelo"] == "Media móvil de 20 días")),
        float(selected["prueba_RMSE"]),
    ]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    bars = ax.bar(labels, values)
    ax.bar_label(bars, fmt="%.2f", padding=4)
    ax.set_title("Error de predicción sobre los datos de prueba")
    ax.set_ylabel("RMSE (USD; menor es mejor)")
    ax.set_ylim(0, max(values) * 1.2)
    ax.text(
        0.5, -0.17,
        f"Red elegida por validación: {selected['modelo']} "
        "· mismos datos de prueba para los tres métodos",
        ha="center", transform=ax.transAxes, fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "00_comparacion_rmse.png", dpi=160)
    plt.close(fig)
    print("Figura guardada: 00_comparacion_rmse.png")


if __name__ == "__main__":
    extract_notebook_figures()
    plot_rmse_comparison()
