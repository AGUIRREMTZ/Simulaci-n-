import tkinter as tk
from tkinter import ttk, messagebox
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

class AnalizadorGastos:
    def __init__(self, archivo="gastos.csv"):
        self.archivo = archivo
        self.gastos = self.cargar()

    def cargar(self):
        gastos = []
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    gastos.append(fila)
        except FileNotFoundError:
            messagebox.showwarning("Archivo no encontrado", "⚠️ No se encontró el archivo 'gastos.csv'.")
        return gastos

    def total_por_categoria(self):
        totales = defaultdict(float)
        for g in self.gastos:
            try:
                totales[g["categoria"]] += float(g["monto"])
            except (KeyError, ValueError):
                pass
        return dict(totales)

    def total_general(self):
        return sum(float(g["monto"]) for g in self.gastos if "monto" in g and g["monto"].replace('.', '', 1).isdigit())


class AppAnalizador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📊 Analizador de Gastos")
        self.geometry("500x400")
        self.resizable(False, False)

        self.analizador = AnalizadorGastos()

        ttk.Label(self, text="ANALIZADOR DE GASTOS", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Button(self, text="Mostrar Totales por Categoría", command=self.mostrar_totales).pack(pady=10)
        ttk.Button(self, text="Ver Gráfica de Gastos", command=self.graficar_gastos).pack(pady=10)
        ttk.Button(self, text="Actualizar Datos", command=self.actualizar_datos).pack(pady=10)
        ttk.Button(self, text="Salir", command=self.destroy).pack(pady=10)

        self.resultado = tk.Text(self, height=10, width=55, wrap="word", state="disabled")
        self.resultado.pack(pady=10)

    def mostrar_totales(self):
        totales = self.analizador.total_por_categoria()
        total_general = self.analizador.total_general()

        if not totales:
            messagebox.showinfo("Sin datos", "No hay datos disponibles.")
            return

        texto = "\n".join([f"💼 {cat}: ${monto:.2f}" for cat, monto in totales.items()])
        texto += f"\n\n💰 Total general: ${total_general:.2f}"

        self.resultado.config(state="normal")
        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(tk.END, texto)
        self.resultado.config(state="disabled")

    def graficar_gastos(self):
        totales = self.analizador.total_por_categoria()
        if not totales:
            messagebox.showinfo("Sin datos", "No hay gastos para graficar.")
            return

        categorias = list(totales.keys())
        montos = list(totales.values())

        plt.figure(figsize=(8, 5))
        plt.bar(categorias, montos)
        plt.title("Gastos por Categoría")
        plt.xlabel("Categorías")
        plt.ylabel("Monto ($)")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

    def actualizar_datos(self):
        self.analizador = AnalizadorGastos()
        messagebox.showinfo("Actualizado", "🔄 Los datos se han actualizado correctamente.")
        self.mostrar_totales()


if __name__ == "__main__":
    app = AppAnalizador()
    app.mainloop()
      
