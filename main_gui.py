import tkinter as tk
from tkinter import messagebox 
from sim_cal import iniciar_simulador_con_algoritmo
from sim_com import iniciar_comparacion_algoritmos
from sim_sync import iniciar_simulador_sincronizacion
from scheduling.fifo import fifo_scheduling
from scheduling.sjf import sjf_scheduling
from scheduling.srt import srt_scheduling
from scheduling.round_robin import round_robin_scheduling
from scheduling.priority import priority_scheduling

def mostrar_menu_principal():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="🖥️ Simulador de Sistemas Operativos", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Button(root, text="🧠 Simulador de Calendarización", font=("Arial", 12),
              command=mostrar_submenu_algoritmos).pack(pady=10)
    tk.Button(root, text="🔒 Simulador de Sincronización", font=("Arial", 12),
              command=lambda: iniciar_simulador_sincronizacion(root, mostrar_menu_principal)).pack(pady=10)
    tk.Button(root, text="❌ Salir", font=("Arial", 12), command=root.quit).pack(pady=30)

def mostrar_submenu_algoritmos():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="🧠 Selecciona el tipo de simulación", font=("Arial", 13, "bold")).pack(pady=20)

    tk.Button(root, text="▶ Ejecución de algoritmo", font=("Arial", 12),
              command=mostrar_seleccion_algoritmo_individual).pack(pady=10)

    tk.Button(root, text="📊 Comparación de algoritmos", font=("Arial", 12),
              command=mostrar_seleccion_comparacion).pack(pady=10)

    tk.Button(root, text="🔙 Volver al menú principal", font=("Arial", 11),
              command=mostrar_menu_principal).pack(pady=30)
def mostrar_seleccion_algoritmo_individual():
    for widget in root.winfo_children():
        widget.destroy()

    algoritmos = {
        "FIFO": fifo_scheduling,
        "SJF": sjf_scheduling,
        "SRT": srt_scheduling,
        "Round Robin": round_robin_scheduling,
        "Priority": priority_scheduling
    }

    selected = tk.StringVar(value="")

    tk.Label(root, text="🧠 Selecciona un algoritmo para ejecutar", font=("Arial", 13, "bold")).pack(pady=10)
    frame_radio = tk.Frame(root)
    frame_radio.pack(pady=10)

    for nombre in algoritmos:
        tk.Radiobutton(frame_radio, text=nombre, variable=selected, value=nombre, font=("Arial", 11)).pack(anchor="w")

    def ejecutar():
        algoritmo = selected.get()
        if not algoritmo:
            messagebox.showerror("Error", "Debes seleccionar un algoritmo.")
            return
        iniciar_simulador_con_algoritmo(root, algoritmo, algoritmos[algoritmo], algoritmo == "Round Robin", mostrar_submenu_algoritmos)

    tk.Button(root, text="▶ Ejecutar", font=("Arial", 12), command=ejecutar).pack(pady=10)
    tk.Button(root, text="🔙 Volver", font=("Arial", 10), command=mostrar_submenu_algoritmos).pack(pady=10)
def mostrar_seleccion_comparacion():
    for widget in root.winfo_children():
        widget.destroy()

    algoritmos = {
        "FIFO": fifo_scheduling,
        "SJF": sjf_scheduling,
        "SRT": srt_scheduling,
        "Round Robin": round_robin_scheduling,
        "Priority": priority_scheduling
    }

    seleccionados = {nombre: tk.BooleanVar() for nombre in algoritmos}

    tk.Label(root, text="📊 Selecciona dos algoritmos para comparar", font=("Arial", 13, "bold")).pack(pady=10)
    frame_checks = tk.Frame(root)
    frame_checks.pack(pady=10)

    for nombre in algoritmos:
        tk.Checkbutton(frame_checks, text=nombre, variable=seleccionados[nombre], font=("Arial", 11)).pack(anchor="w")

    def ejecutar():
        seleccion = [n for n, var in seleccionados.items() if var.get()]
        if len(seleccion) != 2:
            messagebox.showerror("Error", "Debes seleccionar exactamente dos algoritmos.")
            return
        iniciar_comparacion_algoritmos(root, seleccion, algoritmos, mostrar_submenu_algoritmos)

    tk.Button(root, text="▶ Comparar", font=("Arial", 12), command=ejecutar).pack(pady=10)
    tk.Button(root, text="🔙 Volver", font=("Arial", 10), command=mostrar_submenu_algoritmos).pack(pady=10)

# Iniciar ventana principal
root = tk.Tk()
root.title("Simulador de Sistemas Operativos")
root.geometry("600x500")
mostrar_menu_principal()
root.mainloop()
