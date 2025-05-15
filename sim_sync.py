import tkinter as tk
from tkinter import filedialog, messagebox
from utils.sync_loader import load_processes_sync, load_resources, load_actions
from sync.sync_engine import run_sync_simulation
from gui.sync_view import draw_sync_timeline

def iniciar_simulador_sincronizacion(root, volver_callback):
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
        archivo = filedialog.askopenfilename(
            title=f"Cargar archivo de {tipo.lower()}",
            filetypes=[("Archivos de texto", "*.txt")]
        )
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
        confirmacion = messagebox.askyesno(
            "Confirmación",
            "¿Estás seguro de que deseas resetear la simulación?\nSe perderán los archivos cargados y el Gantt actual."
        )
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
    tk.Button(frame_parametros, text="📂 Cargar archivo de procesos",
              command=lambda: seleccionar_archivo(procesos_file, "Procesos")).pack(pady=2)
    tk.Button(frame_parametros, text="📂 Cargar archivo de recursos",
              command=lambda: seleccionar_archivo(recursos_file, "Recursos")).pack(pady=2)
    tk.Button(frame_parametros, text="📂 Cargar archivo de acciones",
              command=lambda: seleccionar_archivo(acciones_file, "Acciones")).pack(pady=2)

    # === Columna: Entradas ===
    tk.Label(frame_entradas, text="🧪 Control de ejecución", font=("Arial", 11, "bold")).pack(pady=5)
    tk.Button(frame_entradas, text="▶ Ejecutar simulación", font=("Arial", 11), command=ejecutar_simulacion).pack(pady=5)
    tk.Button(frame_entradas, text="🔁 RERUN", bg="#ccf5ff", width=20, command=rerun_simulacion).pack(pady=2)
    tk.Button(frame_entradas, text="⚠️ RESET", bg="#ffdddd", width=20, command=reset_simulacion).pack(pady=2)
    tk.Button(frame_entradas, text="🔙 Volver al menú principal", command=volver_callback).pack(pady=10)
