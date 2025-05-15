import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from utils.file_loader import load_processes
from gui.gantt_view import draw_gantt_chart
import copy

def iniciar_comparacion_algoritmos(root, nombres, funciones_dict, volver_callback):
    for widget in root.winfo_children():
        widget.destroy()

    archivo_procesos = tk.StringVar()
    frames_algoritmos = []  # Lista para almacenar los frames de ambos algoritmos
    quantums = {}  # Diccionario para guardar quantums si es necesario

    # === Preguntar por quantum antes si está Round Robin
    if "Round Robin" in nombres:
        quantum = simpledialog.askinteger("Quantum", "Ingrese quantum para Round Robin:", minvalue=1, maxvalue=100)
        if quantum is None:
            volver_callback()
            return
        quantums["Round Robin"] = quantum

    # === Frame izquierdo con scroll
    frame_izq = tk.Frame(root, width=580)
    frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_menu = tk.Frame(frame_izq)
    frame_menu.pack(side=tk.TOP, fill=tk.X)

    canvas = tk.Canvas(frame_izq, width=1000)
    scroll_y = tk.Scrollbar(frame_izq, orient="vertical", command=canvas.yview)
    scroll_x = tk.Scrollbar(frame_izq, orient="horizontal", command=canvas.xview)

    frame_vista = tk.Frame(canvas)

    frame_vista.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=frame_vista, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    # === Panel derecho
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
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if not archivo:
            return
        archivo_procesos.set(archivo)
        label_nombre_archivo.config(text=archivo.split("/")[-1])
        mostrar_contenido_archivo(archivo)
        ejecutar_algoritmos()

    def reset_global():
        confirmacion = messagebox.askyesno("Confirmación", "¿Deseas resetear ambas simulaciones y eliminar el archivo cargado?")
        if not confirmacion:
            return

        archivo_procesos.set("")
        label_nombre_archivo.config(text="(ninguno)")
        vista_archivo.config(state=tk.NORMAL)
        vista_archivo.delete(1.0, tk.END)
        vista_archivo.config(state=tk.DISABLED)

        for frame in frames_algoritmos:
            for w in frame.winfo_children():
                w.destroy()
            tk.Label(frame, text="⏹️ Esperando simulación...", font=("Arial", 10, "italic"), fg="gray").pack(pady=20)

    def rerun_global():
        for widget in frame_vista.winfo_children():
            widget.destroy()
        ejecutar_algoritmos()

    def ejecutar_algoritmos():
        for widget in frame_vista.winfo_children():
            widget.destroy()
        frames_algoritmos.clear()

        try:
            procesos = load_processes(archivo_procesos.get())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
            return

        if len(nombres) == 2:
            for nombre in nombres:
                frame_alg = tk.Frame(frame_vista, borderwidth=1, relief="ridge", width=550, height=400)
                frame_alg.pack_propagate(False)
                frame_alg.pack(side=tk.LEFT, padx=6, pady=6)
                frames_algoritmos.append(frame_alg)

                tk.Label(frame_alg, text=f"📊 {nombre}", font=("Arial", 12, "bold")).pack(pady=5)
                ejecutar_individual(nombre, frame_alg, procesos)

        else:
            nombre = nombres[0]
            frame_alg = tk.Frame(frame_vista, borderwidth=1, relief="ridge", width=1500, height=800)
            frame_alg.pack_propagate(False)
            frame_alg.pack(side=tk.LEFT, padx=30, pady=30)
            frames_algoritmos.append(frame_alg)

            tk.Label(frame_alg, text=f"📊 {nombre}", font=("Arial", 12, "bold")).pack(pady=5)
            ejecutar_individual(nombre, frame_alg, procesos)

    def ejecutar_individual(nombre, frame_alg, procesos=None):
        try:
            if not procesos:
                procesos = load_processes(archivo_procesos.get())
            procesos_copia = copy.deepcopy(procesos)
            quantum = quantums.get(nombre) if nombre == "Round Robin" else None
            resultado = funciones_dict[nombre](procesos_copia, quantum) if nombre == "Round Robin" else funciones_dict[nombre](procesos_copia)
            procesos_finales, gantt, avg_wt = resultado
            draw_gantt_chart(frame_alg, gantt, procesos_finales, avg_wt, True)
        except Exception as e:
            for w in frame_alg.winfo_children():
                w.destroy()
            mensaje_error = f"      ❌ Error en {nombre}:\n{e}"
            if nombre == "Round Robin":
                mensaje_error += "\n        Nota: normalmente en Round Robin los procesos no llegan todos al mismo tiempo(<AT>). \nIntenta cambiar el quantum también."
            tk.Label(frame_alg, text=mensaje_error, fg="red", font=("Arial", 9), justify="left").pack(pady=10)

    # === Menú de control superior
    tk.Label(frame_menu, text="📊 Comparador de algoritmos", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(frame_menu, text="📂 Cargar archivo de procesos", font=("Arial", 12), command=seleccionar_archivo).pack(pady=5)
    tk.Button(frame_menu, text="🔁 RERUN GLOBAL", bg="#ccf5ff", font=("Arial", 11), command=rerun_global).pack(pady=5)
    tk.Button(frame_menu, text="⚠️ RESET GLOBAL", bg="#ffdddd", font=("Arial", 11), command=reset_global).pack(pady=5)
    tk.Button(frame_menu, text="🔙 Volver a algoritmos", font=("Arial", 10), command=volver_callback).pack(pady=10)