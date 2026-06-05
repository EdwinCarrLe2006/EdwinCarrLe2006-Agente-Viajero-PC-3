"""
Gráficos para artículo TSP (IEEE) – diseño limpio con tipografía estilo LaTeX.
- Figuras individuales: solo puntos, líneas finas, color azul.
- Figura comparativa: colores y estilos de línea variados, puntos.
- Solo PNG.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── Configuración global con tipografía estilo LaTeX ─────────────────────────
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "TeX Gyre Termes", "Times New Roman", "DejaVu Serif"],
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "axes.grid": True,
    "grid.linestyle": ":",
    "grid.alpha": 0.3,
    "lines.linewidth": 1.0,
    "lines.markersize": 4,
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "mathtext.fontset": "stix",  # Para que las fórmulas matemáticas tengan aspecto LaTeX
})

# Ruta de salida
OUTPUT = r"C:\Users\Edwin CL\Desktop\ING SISTEMAS\CICLO[5]\IO\PC3\GRAF"
os.makedirs(OUTPUT, exist_ok=True)

# ── Datos (sin cambios) ──────────────────────────────────────────────────────
data = {
    "MTZ Clásico": {
        "cities": [5, 10, 12, 15, 20, 25, 30, 35, 43, 49],
        "time": [0.0301, 0.4723, 0.7049, 0.2208, 0.5671,
                 4.5949, 4.3927, 4.7061, 23.0412, 79.8385],
        "label": "Modelo 1: MTZ Clásico",
        "fname": "fig_mtz_clasico",
        "color": "#1b9e77",
        "linestyle": "-",
    },
    "Moustapha Diaby": {
        "cities": [5, 10, 12, 15, 20, 25, 30],
        "time": [0.3954, 1.508, 6.0029, 3.9622, 24.9708, 573.9782, 2492.0219],
        "label": "Modelo 2: Moustapha Diaby",
        "fname": "fig_moustapha",
        "color": "#d95f02",
        "linestyle": "--",
    },
    "Gavish & Graves": {
        "cities": [5, 10, 12, 15, 20, 25, 30, 35, 43, 49],
        "time": [0.0266, 0.5177, 0.5931, 0.2960, 0.6029,
                 4.2218, 1.4995, 4.7742, 14.06, 10.1731],
        "label": "Modelo 3: Gavish & Graves",
        "fname": "fig_gavish",
        "color": "#7570b3",
        "linestyle": "-.",
    },
    "Finke Claus & Gunn": {
        "cities": [5, 10, 12, 15, 20, 25, 30, 35, 43, 49],
        "time": [0.0332, 0.0968, 0.1369, 0.0704, 0.1354,
                 1.9467, 2.0104, 2.4695, 8.3471, 15.3705],
        "label": "Modelo 4: Finke, Claus & Gunn",
        "fname": "fig_finke",
        "color": "#e7298a",
        "linestyle": ":",
    },
    "MTZ con Lifting": {
        "cities": [5, 10, 12, 15, 20, 25, 30, 35, 43, 49],
        "time": [0.0285, 0.0706, 0.1256, 0.0526, 0.0762,
                 0.7107, 0.8686, 0.7080, 3.4802, 1.8783],
        "label": "Modelo 5: MTZ con Lifting Robustecido",
        "fname": "fig_mtz_lifting",
        "color": "#66a61e",
        "linestyle": (0, (3, 1, 1, 1)),  # trazo-punto
    },
}

# ── Figura individual (azul, solo puntos, línea fina) ────────────────────────
def plot_modelo(nombre, info):
    fig, ax = plt.subplots(figsize=(3.5, 2.6))

    ax.plot(info["cities"], info["time"],
            color="#1f77b4",  # azul único
            marker="o",
            linestyle="-",
            linewidth=1.0,
            markersize=4,
            clip_on=False,
            zorder=3)

    ax.set_xlabel("Número de ciudades ($n$)")
    ax.set_ylabel("Tiempo de ejecución (s)")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:g}"))
    ax.set_xticks(info["cities"])
    ax.tick_params(axis="x", rotation=45)
    ax.set_xlim(min(info["cities"]) - 0.5, max(info["cities"]) + 0.5)

    ymin = min(info["time"]) * 0.8
    ymax = max(info["time"]) * 1.2
    ax.set_ylim(ymin, ymax)

    ax.grid(True, linestyle=":", alpha=0.3)
    ax.set_title(info["label"], pad=6, fontsize=10, fontweight="normal")

    fig.tight_layout(pad=0.8)
    ruta_png = os.path.join(OUTPUT, info["fname"] + ".png")
    fig.savefig(ruta_png, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓  {ruta_png}")

# ── Generar figuras individuales ──────────────────────────────────────────────
print("Generando figuras individuales (estilo unificado azul)...")
for nombre, info in data.items():
    plot_modelo(nombre, info)

# ── Figura comparativa (colores variados, estilos de línea, puntos) ──────────
print("Generando figura comparativa...")

modelos_comp = ["MTZ Clásico", "Gavish & Graves", "Finke Claus & Gunn", "MTZ con Lifting"]

fig, ax = plt.subplots(figsize=(3.5, 2.8))

for nombre in modelos_comp:
    info = data[nombre]
    short = {
        "MTZ Clásico": "MTZ Clásico",
        "Gavish & Graves": "Gavish & Graves",
        "Finke Claus & Gunn": "Finke et al.",
        "MTZ con Lifting": "MTZ Lifting",
    }[nombre]
    ax.plot(info["cities"], info["time"],
            color=info["color"],
            marker="o",
            linestyle=info["linestyle"],
            linewidth=1.0,
            markersize=4,
            label=short,
            zorder=3)

# Moustapha Diaby
m = data["Moustapha Diaby"]
ax.plot(m["cities"], m["time"],
        color=m["color"],
        marker="o",
        linestyle=m["linestyle"],
        linewidth=1.0,
        markersize=4,
        label="Moustapha Diaby*",
        zorder=3)

ax.set_xlabel("Número de ciudades ($n$)")
ax.set_ylabel("Tiempo de ejecución (s)")
ax.set_yscale("log")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:g}"))
ax.set_title("Comparación de tiempo de ejecución\npor formulación MILP", pad=4, fontsize=10)
ax.legend(loc="upper left", framealpha=0.9, edgecolor="gray",
          fontsize=8, handlelength=2.0, ncol=1)
ax.annotate("* datos hasta $n=30$", xy=(0.98, 0.03),
            xycoords="axes fraction", ha="right", va="bottom",
            fontsize=7, style="italic", color="gray")

ax.set_xlim(4, 50)
ax.grid(True, linestyle=":", alpha=0.3)

fig.tight_layout(pad=0.8)
ruta_png = os.path.join(OUTPUT, "fig_comparativa.png")
fig.savefig(ruta_png, format="png", dpi=300, bbox_inches="tight")
print(f"  ✓  {ruta_png}")

print("\n¡Todos los gráficos generados correctamente!")