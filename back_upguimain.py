# === IMPORTACIONES ===
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling
from scheduling.sjf import sjf_scheduling
from scheduling.srt import srt_scheduling
from scheduling.round_robin import round_robin_scheduling
from scheduling.priority import priority_scheduling

from sync.sync_engine import run_sync_simulation
from gui.gantt_view import draw_gantt_chart
from gui.sync_view import draw_sync_timeline
from utils.sync_loader import load_processes_sync, load_resources, load_actions


# === MENÚ PRINCIPAL ===
def mostrar_menu_principal():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="🖥️ Simulador de Sistemas Operativos", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Button(root, text="🧠 Simulador de Calendarización", font=("Arial", 12),
              command=iniciar_simulador_calendarizacion).pack(pady=10)
    tk.Button(root, text="🔒 Simulador de Sincronización", font=("Arial", 12),
              command=iniciar_simulador_sincronizacion).pack(pady=10)
    tk.Button(root, text="❌ Salir", font=("Arial", 12), command=root.quit).pack(pady=30)


# === SIMULADOR CALENDARIZACIÓN ===
def iniciar_simulador_calendarizacion():
    mostrar_submenu_algoritmos()


def mostrar_submenu_algoritmos():
    for widget in root.winfo_children():
        widget.destroy()

    algoritmos_disponibles = {
        "FIFO": fifo_scheduling,
        "SJF": sjf_scheduling,
        "SRT": srt_scheduling,
        "Round Robin": round_robin_scheduling,
        "Priority": priority_scheduling
    }

    seleccionados = {nombre: tk.BooleanVar() for nombre in algoritmos_disponibles}

    tk.Label(root, text="🧠 Selecciona uno o dos algoritmos para comparar", font=("Arial", 13, "bold")).pack(pady=10)
    check_frame = tk.Frame(root)
    check_frame.pack(pady=10)

    for nombre in seleccionados:
        tk.Checkbutton(check_frame, text=nombre, variable=seleccionados[nombre], font=("Arial", 11)).pack(anchor="w")

    def ejecutar_comparacion():
        seleccion = [nombre for nombre, var in seleccionados.items() if var.get()]
        if len(seleccion) == 0 or len(seleccion) > 2:
            messagebox.showerror("Error", "Debes seleccionar 1 o 2 algoritmos.")
            return
        iniciar_comparacion_algoritmos(seleccion, algoritmos_disponibles)

    tk.Button(root, text="▶ Comparar algoritmos", font=("Arial", 12), command=ejecutar_comparacion).pack(pady=10)
    tk.Button(root, text="🔙 Volver al menú principal", command=mostrar_menu_principal).pack(pady=20)


def iniciar_simulador_con_algoritmo(nombre_algoritmo, funcion_algoritmo, requiere_quantum=False):
    for widget in root.winfo_children():
        widget.destroy()

    archivo_procesos = tk.StringVar()
    quantum = None

    frame_izq = tk.Frame(root)
    frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_der = tk.Frame(root, width=300, bg="#f0f0f0")
    frame_der.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(frame_der, text="📄 Archivo cargado", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=5)
    label_nombre_archivo = tk.Label(frame_der, text="(ninguno)", font=("Arial", 10), bg="#f0f0f0", wraplength=280)
    label_nombre_archivo.pack(padx=10)

    vista_archivo = tk.Text(frame_der, height=30, width=40, bg="#f7f7f7", font=("Courier", 9))
    vista_archivo.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    vista_archivo.config(state=tk.DISABLED)

    def mostrar_contenido_archivo(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as e:
            contenido = f"Error al leer el archivo:\n{e}"
        vista_archivo.config(state=tk.NORMAL)
        vista_archivo.delete(1.0, tk.END)
        vista_archivo.insert(tk.END, contenido)
        vista_archivo.config(state=tk.DISABLED)

    def seleccionar_archivo():
        archivo = filedialog.askopenfilename(title="Seleccionar archivo de procesos",
                                             filetypes=[("Archivos de texto", "*.txt")])
        if not archivo:
            return
        archivo_procesos.set(archivo)
        label_nombre_archivo.config(text=archivo.split("/")[-1])
        mostrar_contenido_archivo(archivo)
        if not requiere_quantum or (requiere_quantum and quantum is not None):
            ejecutar_simulacion()

    def ejecutar_simulacion():
        try:
            procesos = load_processes(archivo_procesos.get())
            resultado = funcion_algoritmo(procesos, quantum) if requiere_quantum else funcion_algoritmo(procesos)
            procesos_finales, gantt, avg_wt = resultado

            for widget in frame_izq.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.destroy()
            draw_gantt_chart(frame_izq, gantt, procesos_finales, avg_wt)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar la simulación:\n{e}")

    def volver():
        mostrar_submenu_algoritmos()

    tk.Label(frame_izq, text=f"📊 Simulador - {nombre_algoritmo}", font=("Arial", 14, "bold")).pack(pady=10)

    if requiere_quantum:
        quantum = simpledialog.askinteger("Quantum", "Ingrese el quantum:", minvalue=1, maxvalue=100)
        if quantum is None:
            volver()
            return

        # === Botones de control ===
    tk.Button(frame_izq, text="📂 Cargar archivo de procesos", font=("Arial", 12),
              command=seleccionar_archivo).pack(pady=10)
    tk.Button(frame_izq, text="▶ Ejecutar de nuevo", font=("Arial", 11),
              command=ejecutar_simulacion).pack(pady=5)

    def rerun_simulacion():
        for widget in frame_izq.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        ejecutar_simulacion()

    def reset_simulacion():
        confirmacion = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas resetear la simulación?")
        if not confirmacion:
            return
        archivo_procesos.set("")
        label_nombre_archivo.config(text="(ninguno)")
        vista_archivo.config(state=tk.NORMAL)
        vista_archivo.delete(1.0, tk.END)
        vista_archivo.config(state=tk.DISABLED)
        for widget in frame_izq.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

    tk.Button(frame_izq, text="🔁 RERUN", bg="#ccf5ff", width=20,
              command=rerun_simulacion).pack(pady=20)
    tk.Button(frame_izq, text="⚠️ RESET", bg="#ffdddd", width=20,
              command=reset_simulacion).pack(pady=20)

    tk.Button(frame_izq, text="🔙 Volver a algoritmos", font=("Arial", 10),
              command=volver).pack(pady=20)



def iniciar_comparacion_algoritmos(nombres, funciones_dict):
    for widget in root.winfo_children():
        widget.destroy()

    archivo_procesos = tk.StringVar()

    frame_izq = tk.Frame(root)
    frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_der = tk.Frame(root, width=300, bg="#f0f0f0")
    frame_der.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(frame_der, text="📄 Archivo cargado", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=5)
    label_nombre_archivo = tk.Label(frame_der, text="(ninguno)", font=("Arial", 10), bg="#f0f0f0", wraplength=280)
    label_nombre_archivo.pack(padx=10)

    vista_archivo = tk.Text(frame_der, height=30, width=40, bg="#f7f7f7", font=("Courier", 9))
    vista_archivo.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    vista_archivo.config(state=tk.DISABLED)

    def mostrar_contenido_archivo(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as e:
            contenido = f"Error al leer el archivo:\n{e}"
        vista_archivo.config(state=tk.NORMAL)
        vista_archivo.delete(1.0, tk.END)
        vista_archivo.insert(tk.END, contenido)
        vista_archivo.config(state=tk.DISABLED)

    def seleccionar_archivo():
        archivo = filedialog.askopenfilename(title="Seleccionar archivo de procesos",
                                             filetypes=[("Archivos de texto", "*.txt")])
        if not archivo:
            return
        archivo_procesos.set(archivo)
        label_nombre_archivo.config(text=archivo.split("/")[-1])
        mostrar_contenido_archivo(archivo)
        ejecutar_algoritmos()

    def ejecutar_algoritmos():
        try:
            procesos = load_processes(archivo_procesos.get())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
            return

        if len(nombres) == 2:
            frame_comparacion = tk.Frame(frame_izq)
            frame_comparacion.pack(fill=tk.BOTH, expand=True)
            for nombre in nombres:
                frame_alg = tk.Frame(frame_comparacion, borderwidth=2, relief="groove")
                frame_alg.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
                try:
                    if nombre == "Round Robin":
                        quantum = simpledialog.askinteger("Quantum", f"Ingrese el quantum para {nombre}:",
                                                          minvalue=1, maxvalue=100)
                        if quantum is None:
                            return
                        procesos_finales, gantt, avg_wt = funciones_dict[nombre](procesos, quantum)
                    else:
                        procesos_finales, gantt, avg_wt = funciones_dict[nombre](procesos)
                    tk.Label(frame_alg, text=f"📊 {nombre}", font=("Arial", 11, "bold")).pack(pady=5)
                    draw_gantt_chart(frame_alg, gantt, procesos_finales, avg_wt)
                except Exception as e:
                    tk.Label(frame_alg, text=f"❌ Error en {nombre}: {e}", fg="red").pack()
        else:
            nombre = nombres[0]
            frame_alg = tk.Frame(frame_izq, borderwidth=2, relief="groove")
            frame_alg.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            try:
                if nombre == "Round Robin":
                    quantum = simpledialog.askinteger("Quantum", f"Ingrese el quantum para {nombre}:",
                                                      minvalue=1, maxvalue=100)
                    if quantum is None:
                        return
                    procesos_finales, gantt, avg_wt = funciones_dict[nombre](procesos, quantum)
                else:
                    procesos_finales, gantt, avg_wt = funciones_dict[nombre](procesos)
                tk.Label(frame_alg, text=f"📊 {nombre}", font=("Arial", 11, "bold")).pack(pady=5)
                draw_gantt_chart(frame_alg, gantt, procesos_finales, avg_wt)
            except Exception as e:
                tk.Label(frame_alg, text=f"❌ Error en {nombre}: {e}", fg="red").pack()

    tk.Label(frame_izq, text="📊 Comparador de algoritmos", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(frame_izq, text="📂 Cargar archivo de procesos", font=("Arial", 12),
              command=seleccionar_archivo).pack(pady=10)
    tk.Button(frame_izq, text="🔙 Volver a algoritmos", font=("Arial", 10),
              command=mostrar_submenu_algoritmos).pack(pady=10)


# === SIMULADOR SINCRONIZACIÓN ===
def iniciar_simulador_sincronizacion():
    for widget in root.winfo_children():
        widget.destroy()

    modo_var = tk.StringVar(value="mutex")
    procesos_file = tk.StringVar()
    recursos_file = tk.StringVar()
    acciones_file = tk.StringVar()
    velocidad_var = tk.IntVar(value=100)

    archivos_dict = {
        "Procesos": procesos_file,
        "Recursos": recursos_file,
        "Acciones": acciones_file
    }

    # === Layout general ===
    frame_izq = tk.Frame(root)
    frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_menu = tk.Frame(frame_izq)
    frame_menu.pack(side=tk.TOP, fill=tk.X)

    frame_vista = tk.Frame(frame_izq)
    frame_vista.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    frame_der = tk.Frame(root, width=300, bg="#f0f0f0")
    frame_der.pack(side=tk.RIGHT, fill=tk.Y)

    # === Panel derecho ===
    tk.Label(frame_der, text="📋 Archivos cargados", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=5)
    lista_archivos = tk.Listbox(frame_der, height=5)
    lista_archivos.pack(padx=10, pady=5, fill=tk.X)

    vista_archivo = tk.Text(frame_der, height=25, width=40, bg="#f7f7f7", font=("Courier", 9))
    vista_archivo.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    vista_archivo.config(state=tk.DISABLED)

    # === FUNCIONES ===

    def actualizar_lista_archivos():
        lista_archivos.delete(0, tk.END)
        for nombre, var in archivos_dict.items():
            ruta = var.get()
            if ruta:
                lista_archivos.insert(tk.END, f"{nombre}: {ruta.split('/')[-1]}")

    def mostrar_contenido_archivo(event):
        seleccion = lista_archivos.curselection()
        if not seleccion:
            return
        item = lista_archivos.get(seleccion[0])
        tipo = item.split(":")[0]
        ruta = archivos_dict[tipo].get()
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as e:
            contenido = f"Error al leer el archivo:\n{e}"
        vista_archivo.config(state=tk.NORMAL)
        vista_archivo.delete(1.0, tk.END)
        vista_archivo.insert(tk.END, contenido)
        vista_archivo.config(state=tk.DISABLED)

    lista_archivos.bind("<<ListboxSelect>>", mostrar_contenido_archivo)

    def seleccionar_archivo(var, tipo):
        archivo = filedialog.askopenfilename(title=f"Cargar archivo de {tipo.lower()}", filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            var.set(archivo)
            actualizar_lista_archivos()

    def ejecutar_simulacion():
        try:
            procesos = load_processes_sync(procesos_file.get())
            recursos = load_resources(recursos_file.get())
            acciones = load_actions(acciones_file.get())
            modo = modo_var.get()

            for widget in frame_vista.winfo_children():
                widget.destroy()

            gantt_sync = run_sync_simulation(procesos, recursos, acciones, modo)
            draw_sync_timeline(frame_vista, gantt_sync, velocidad=velocidad_var.get())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar la simulación:\n{e}")

    def reset_simulacion():
        confirmacion = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas resetear la simulación?\nSe perderán los archivos cargados y el Gantt actual.")
        if not confirmacion:
            return
        procesos_file.set("")
        recursos_file.set("")
        acciones_file.set("")
        lista_archivos.delete(0, tk.END)
        vista_archivo.config(state=tk.NORMAL)
        vista_archivo.delete(1.0, tk.END)
        vista_archivo.config(state=tk.DISABLED)
        for widget in frame_vista.winfo_children():
            widget.destroy()

    def rerun_simulacion():
        for widget in frame_vista.winfo_children():
            widget.destroy()
        ejecutar_simulacion()

    # === Subcolumnas dentro de frame_menu ===
    frame_parametros = tk.Frame(frame_menu)
    frame_parametros.pack(side=tk.LEFT, padx=20, pady=5, anchor="n")

    frame_entradas = tk.Frame(frame_menu)
    frame_entradas.pack(side=tk.RIGHT, padx=20, pady=5, anchor="n")

    # === Columna: Parámetros ===
    tk.Label(frame_parametros, text="⚙️ Parámetros", font=("Arial", 11, "bold")).pack(pady=5)
    tk.Label(frame_parametros, text="Modo:", font=("Arial", 10)).pack()
    tk.Radiobutton(frame_parametros, text="Mutex", variable=modo_var, value="mutex").pack(anchor="w")
    tk.Radiobutton(frame_parametros, text="Semáforo", variable=modo_var, value="semaforo").pack(anchor="w")

    tk.Label(frame_parametros, text="Velocidad de animación (ms):", font=("Arial", 10)).pack(pady=5)
    tk.Scale(frame_parametros, from_=10, to=1000, orient="horizontal", variable=velocidad_var).pack()

    tk.Label(frame_parametros, text="Archivos de entrada:", font=("Arial", 10, "italic")).pack(pady=5)
    tk.Button(frame_parametros, text="📂 Cargar archivo de procesos", command=lambda: seleccionar_archivo(procesos_file, "Procesos")).pack(pady=2)
    tk.Button(frame_parametros, text="📂 Cargar archivo de recursos", command=lambda: seleccionar_archivo(recursos_file, "Recursos")).pack(pady=2)
    tk.Button(frame_parametros, text="📂 Cargar archivo de acciones", command=lambda: seleccionar_archivo(acciones_file, "Acciones")).pack(pady=2)

    # === Columna: Entradas ===
    tk.Label(frame_entradas, text="🧪 Control de ejecución", font=("Arial", 11, "bold")).pack(pady=5)
    tk.Button(frame_entradas, text="▶ Ejecutar simulación", font=("Arial", 11), command=ejecutar_simulacion).pack(pady=5)
    tk.Button(frame_entradas, text="🔁 RERUN", bg="#ccf5ff", width=20, command=rerun_simulacion).pack(pady=2)
    tk.Button(frame_entradas, text="⚠️ RESET", bg="#ffdddd", width=20, command=reset_simulacion).pack(pady=2)
    tk.Button(frame_entradas, text="🔙 Volver al menú principal", command=mostrar_menu_principal).pack(pady=10)



# (ya incluido por completo en tu mensaje y sin cambios necesarios, si deseas que lo ordene también dímelo)

# === INICIALIZACIÓN ===
root = tk.Tk()
root.title("Simulador de Sistemas Operativos")
root.geometry("600x500")
mostrar_menu_principal()
root.mainloop()
