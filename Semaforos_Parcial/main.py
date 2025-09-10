import tkinter as tk
from tkinter import ttk
import threading
import time

# Imports compatibles con tu estructura actual
try:
    from Back.controller import TrafficController
    from Back.config import Config
    from Back.metrics import MetricsCollector
except Exception:
    # Alternativa si estás ejecutando sin paquete "Back"
    from controller import TrafficController
    from config import Config
    from metrics import MetricsCollector

# Dibujo de la malla/intersección
# Debe existir tu módulo de render. Si se llama distinto, ajusta el import.
from grid_saso import TrafficGrid


class TrafficSimulationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulación de Semáforos Autoorganizantes - Sistemas Complejos")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)  # Tamaño mínimo de ventana

        # Estado de ejecución
        self.running = False
        self.sim_thread = None

        # Config inicial
        self.config = Config()
        self.metrics = MetricsCollector()

        # Controller principal
        self.controller = TrafficController(self.config)

        # Grid para dibujar (usa self.config para ubicaciones)
        self.grid = TrafficGrid(self.controller, self.config, self.metrics)

        # Variables de UI
        self.param_vars = {}
        self._build_gui()
        
        # Configurar el redimensionado responsive
        self.root.bind('<Configure>', self._on_window_resize)
        
        # Flag para evitar redibujado excesivo
        self._resize_pending = False
        self._resize_job = None  # Inicializar explícitamente

    # -----------------------------
    # Construcción de la interfaz
    # -----------------------------
    def _build_gui(self):
        # Frame principal con configuración de grid weights para responsive
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar pesos para el grid responsive
        main_frame.grid_rowconfigure(1, weight=1)  # Fila del contenido principal
        main_frame.grid_columnconfigure(0, weight=1)

        # ---- Panel superior de controles ----
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Frame para botones de control
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(side=tk.LEFT)

        ttk.Button(buttons_frame, text="▶ Iniciar", command=self.start).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(buttons_frame, text="⏸ Pausar", command=self.pause).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(buttons_frame, text="🔄 Reiniciar", command=self.reset).pack(side=tk.LEFT, padx=(0, 12))

        # Separador visual
        separator = ttk.Separator(control_frame, orient='vertical')
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Parámetros rápidos (ejemplo; ajusta a los tuyos)
        params_frame = ttk.LabelFrame(control_frame, text="Parámetros", padding=5)
        params_frame.pack(side=tk.LEFT, padx=(10, 0))

        # Crear grid para parámetros
        params_grid = ttk.Frame(params_frame)
        params_grid.pack()

        params = [
            ("Velocidad (ms)", "tick_ms", 30),
            ("Spawn NS (%)", "spawn_ns_pct", 35),
            ("Spawn EW (%)", "spawn_ew_pct", 35),
            ("Umbral N", "n_threshold", 4),
            ("Dist. D", "d_distance", 120),
            ("Dist. R", "r_distance", 60),
        ]

        for i, (label, key, default) in enumerate(params):
            row = i // 3
            col = (i % 3) * 2
            
            ttk.Label(params_grid, text=label + ":").grid(
                row=row, column=col, sticky=tk.W, padx=(0, 5), pady=2
            )
            var = tk.IntVar(value=getattr(self.config, key, default))
            self.param_vars[key] = var
            entry = ttk.Entry(params_grid, textvariable=var, width=8)
            entry.grid(row=row, column=col + 1, padx=(0, 10), pady=2)
            # Bind para aplicar cambios automáticamente
            entry.bind('<FocusOut>', lambda e: self._pull_params())

        # NUEVO: Frame para control de caos
        chaos_frame = ttk.LabelFrame(control_frame, text="Control de Caos", padding=5)
        chaos_frame.pack(side=tk.LEFT, padx=(10, 0))

        # Slider para factor de caos
        ttk.Label(chaos_frame, text="Factor Caos:").grid(row=0, column=0, padx=(0, 5))
        
        self.chaos_var = tk.DoubleVar(value=self.config.chaos_factor)
        chaos_scale = ttk.Scale(
            chaos_frame, 
            from_=0.0, 
            to=1.0, 
            variable=self.chaos_var, 
            orient=tk.HORIZONTAL,
            length=100,
            command=self._on_chaos_change
        )
        chaos_scale.grid(row=0, column=1, padx=(0, 5))
        
        # Etiqueta del valor actual
        self.chaos_value_label = ttk.Label(chaos_frame, text="0.10")
        self.chaos_value_label.grid(row=0, column=2)

        # Botón para aplicar caos inmediatamente
        ttk.Button(
            chaos_frame, 
            text="Aplicar Caos", 
            command=self._apply_chaos_now
        ).grid(row=1, column=0, columnspan=3, pady=(5, 0))

        # ---- Panel central: canvas + panel derecho ----
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew")
        
        # Configurar pesos del grid para responsive
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=3)  # Canvas toma más espacio
        content_frame.grid_columnconfigure(1, weight=1)  # Panel derecho menos espacio

        # Canvas (a la izquierda) - Frame del canvas
        canvas_frame = ttk.LabelFrame(content_frame, text="🚦 Simulación", padding=5)
        canvas_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Configurar canvas frame para responsive
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        # Canvas con scrollbars si es necesario
        self.canvas = tk.Canvas(
            canvas_frame, 
            background="lightgray",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars para el canvas
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Bind de eventos del canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # Panel derecho: métricas / caos / info
        right_frame = ttk.Frame(content_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Configurar pesos del panel derecho
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Título del panel derecho
        info_label = ttk.Label(right_frame, text="📊 Métricas y Estado", font=('Arial', 10, 'bold'))
        info_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Panel de estadísticas
        stats_frame = ttk.LabelFrame(right_frame, text="Estadísticas", padding=5)
        stats_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 5))
        stats_frame.grid_rowconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(0, weight=1)

        self.stats_text = tk.Text(
            stats_frame, 
            height=12, 
            width=35, 
            state=tk.DISABLED,
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.stats_text.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para stats
        stats_scroll = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_text.yview)
        stats_scroll.grid(row=0, column=1, sticky="ns")
        self.stats_text.configure(yscrollcommand=stats_scroll.set)

        # Panel de información de caos
        chaos_frame = ttk.LabelFrame(right_frame, text="Dinámica del Sistema", padding=5)
        chaos_frame.grid(row=2, column=0, sticky="nsew")
        chaos_frame.grid_rowconfigure(0, weight=1)
        chaos_frame.grid_columnconfigure(0, weight=1)

        self.chaos_info = tk.Text(
            chaos_frame, 
            height=12, 
            width=35, 
            state=tk.DISABLED,
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.chaos_info.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para chaos
        chaos_scroll = ttk.Scrollbar(chaos_frame, orient="vertical", command=self.chaos_info.yview)
        chaos_scroll.grid(row=0, column=1, sticky="ns")
        self.chaos_info.configure(yscrollcommand=chaos_scroll.set)

        # Configurar colores para los textos
        self._configure_text_styles()
        
        # Primer dibujado
        self.root.after(100, self._initial_draw)

    def _configure_text_styles(self):
        """Configura estilos para los textos de información"""
        # Configurar tags para colorear el texto
        self.stats_text.configure(state=tk.NORMAL)
        self.stats_text.tag_configure("header", foreground="blue", font=('Consolas', 9, 'bold'))
        self.stats_text.tag_configure("value", foreground="darkgreen")
        self.stats_text.tag_configure("warning", foreground="red")
        self.stats_text.configure(state=tk.DISABLED)
        
        self.chaos_info.configure(state=tk.NORMAL)
        self.chaos_info.tag_configure("header", foreground="purple", font=('Consolas', 9, 'bold'))
        self.chaos_info.tag_configure("value", foreground="darkblue")
        self.chaos_info.configure(state=tk.DISABLED)

    # -----------------------------
    # NUEVO: Métodos para control de caos
    # -----------------------------
    def _on_chaos_change(self, value):
        """Callback cuando cambia el slider de caos"""
        chaos_value = float(value)
        self.chaos_value_label.config(text=f"{chaos_value:.2f}")
        
        # Actualizar config y controller en tiempo real
        self.config.chaos_factor = chaos_value
        if hasattr(self.controller.chaos_engine, 'set_chaos_factor'):
            self.controller.chaos_engine.set_chaos_factor(chaos_value)
    
    def _apply_chaos_now(self):
        """Aplica una perturbación caótica inmediata"""
        if hasattr(self.controller.chaos_engine, 'apply_chaos'):
            self.controller.chaos_engine.apply_chaos(self.controller)
            print(f"Aplicada perturbación caótica con factor {self.chaos_var.get():.2f}")

    # -----------------------------
    # Handlers de UI mejorados
    # -----------------------------
    def start(self):
        """Inicia la simulación"""
        self._pull_params()
        if not self.running:
            self.running = True
            self.sim_thread = threading.Thread(target=self._run_loop, daemon=True)
            self.sim_thread.start()
            print("✅ Simulación iniciada")

    def pause(self):
        """Pausa la simulación"""
        self.running = False
        print("⏸ Simulación pausada")

    def reset(self):
        """Reinicia la simulación"""
        self.running = False
        if self.sim_thread and self.sim_thread.is_alive():
            self.sim_thread.join(timeout=0.5)
        
        # Reinicio: recrea controller y grid para limpiar colas/vehículos
        self.controller = TrafficController(self.config)
        self.grid = TrafficGrid(self.controller, self.config, self.metrics)
        self.metrics.reset()
        
        # Reaplica el factor de caos actual
        if hasattr(self.controller.chaos_engine, 'set_chaos_factor'):
            self.controller.chaos_engine.set_chaos_factor(self.chaos_var.get())
        
        self._force_redraw()
        print("🔄 Simulación reiniciada")

    # -----------------------------
    # Lógica de ejecución mejorada
    # -----------------------------
    def _run_loop(self):
        """Loop principal de simulación con mejor manejo de errores"""
        frame_count = 0
        while self.running:
            try:
                # Paso de simulación
                self.controller.step()
                
                # Redibujo cada pocos frames para mejor rendimiento
                if frame_count % 2 == 0:  # Dibuja cada 2 frames
                    self.root.after_idle(self._force_redraw)
                
                # Actualizar paneles cada 5 frames
                if frame_count % 5 == 0:
                    self.root.after_idle(self.update_stats_display)
                    self.root.after_idle(self.update_chaos_display)

                # Ritmo (ms/frame)
                tick = max(10, getattr(self.config, "tick_ms", 30))  # Mínimo 10ms
                time.sleep(tick / 1000.0)
                
                frame_count += 1
                
            except Exception as e:
                print(f"⚠ Error en simulación: {e}")
                self.running = False
                break

    def _force_redraw(self):
        """Fuerza el redibujado del canvas"""
        if not self._resize_pending:
            self.canvas.delete("all")
            self._update_canvas_size()
            self.grid.draw(self.canvas)

    def _initial_draw(self):
        """Dibujado inicial con tamaños correctos"""
        self._update_canvas_size()
        self._force_redraw()

    def _update_canvas_size(self):
        """Actualiza el tamaño del área de dibujo del canvas"""
        # Obtener tamaño actual del canvas
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:  # Evitar tamaños inválidos
            # Actualizar configuración
            self.config.canvas_width = max(400, canvas_width - 10)  # Margen de 10px
            self.config.canvas_height = max(300, canvas_height - 10)
            
            # Re-centrar la intersección
            self.config.intersection_x = self.config.canvas_width // 2
            self.config.intersection_y = self.config.canvas_height // 2
            
            # Configurar scroll region
            self.canvas.configure(scrollregion=(0, 0, self.config.canvas_width, self.config.canvas_height))
            
            # Notificar al controller
            if hasattr(self.controller, "update_config"):
                self.controller.update_config(self.config)

    def _pull_params(self):
        """Actualiza self.config con lo que haya en las entradas"""
        for key, var in self.param_vars.items():
            try:
                value = max(1, int(var.get()))  # Valores mínimos positivos
                setattr(self.config, key, value)
            except (ValueError, tk.TclError):
                # Si hay error, restaurar valor por defecto
                if key == "tick_ms":
                    setattr(self.config, key, 30)
                elif "pct" in key:
                    setattr(self.config, key, 35)
                else:
                    setattr(self.config, key, 4 if "threshold" in key else 60)

        # Asegurar que controller esté enterado de posibles cambios
        if hasattr(self.controller, "update_config"):
            self.controller.update_config(self.config)

    # -----------------------------
    # Eventos de canvas responsive 
    # -----------------------------
    def _on_window_resize(self, event):
        """Maneja el redimensionado de la ventana principal"""
        if event.widget == self.root:
            # Solo cancelar si el job existe y es válido
            if self._resize_job is not None:
                try:
                    self.root.after_cancel(self._resize_job)
                except (ValueError, tk.TclError):
                    # Ignora errores si el job ya no es válido
                    pass
            # Programar actualización después de que termine el redimensionado
            self._resize_job = self.root.after(100, self._handle_resize)

    def _handle_resize(self):
        """Maneja el redimensionado con debounce"""
        self._resize_pending = True
        self._resize_job = self.root.after(50, self._finish_resize)

    def _finish_resize(self):
        """Completa el proceso de redimensionado"""
        self._resize_pending = False
        self._resize_job = None  # Limpiar la referencia
        self._update_canvas_size()
        if not self.running:  # Solo redibujar si no está corriendo la simulación
            self._force_redraw()

    def _on_canvas_configure(self, event):
        """Maneja cambios en el canvas"""
        if event.widget == self.canvas:
            # Programar actualización
            self.canvas.after_idle(self._update_canvas_size)

    def _on_canvas_click(self, event):
        """Maneja clicks en el canvas (para debugging)"""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        print(f"🖱 Click en canvas: ({canvas_x:.1f}, {canvas_y:.1f})")

    # -----------------------------
    # Panel derecho: métricas/estado mejorado
    # -----------------------------
    def update_stats_display(self):
        """Actualiza el display de estadísticas con formato mejorado"""
        data = {}
        if hasattr(self.controller, "get_stats"):
            data = self.controller.get_stats()

        # Estado de los semáforos
        ns_state = "🟢" if hasattr(self.controller, "ns_light") and self.controller.ns_light.state.value == "VERDE" else "🔴"
        ew_state = "🟢" if hasattr(self.controller, "ew_light") and self.controller.ew_light.state.value == "VERDE" else "🔴"

        self.stats_text.configure(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        
        # Texto con formato
        stats_text = f"""╔══ ESTADÍSTICAS ══╗
        
Tiempo simulación: {data.get('sim_time', 0):,}
Vehículos en cola: {data.get('queue', 0)}
Throughput:
    NS: {data.get('passed_ns', 0):,} vehículos
    EW: {data.get('passed_ew', 0):,} vehículos

Estado semáforos:
   {ns_state} NS: {data.get('changes_ns', 0)} cambios
   {ew_state} EW: {data.get('changes_ew', 0)} cambios

Eficiencia:
   Total procesados: {data.get('passed_ns', 0) + data.get('passed_ew', 0):,}
   Tasa paso (veh/min): {((data.get('passed_ns', 0) + data.get('passed_ew', 0)) * 60 / max(1, data.get('sim_time', 1) / 30)):.1f}

Estado actual:
   Canvas: {self.config.canvas_width}x{self.config.canvas_height}
   Intersección: ({self.config.intersection_x}, {self.config.intersection_y})
   Simulación: {'🟢 EJECUTANDO' if self.running else '🔴 PAUSADA'}
"""
        
        self.stats_text.insert(tk.END, stats_text)
        self.stats_text.configure(state=tk.DISABLED)

    def update_chaos_display(self):
        """Actualiza el display de información de caos"""
        chaos = {}
        if hasattr(self.controller, "chaos_engine"):
            ch = self.controller.chaos_engine
            if hasattr(ch, "get_entropy"):
                chaos['entropy'] = ch.get_entropy()
            if hasattr(ch, "get_complexity_index"):
                chaos['complexity'] = ch.get_complexity_index()
            if hasattr(ch, "lorenz_x"):
                chaos['lorenz_x'] = ch.lorenz_x
                chaos['lorenz_y'] = ch.lorenz_y  
                chaos['lorenz_z'] = ch.lorenz_z
            if hasattr(ch, "chaos_factor"):
                chaos['chaos_factor'] = ch.chaos_factor

        self.chaos_info.configure(state=tk.NORMAL)
        self.chaos_info.delete("1.0", tk.END)
        
        text = f"""╔══ DINÁMICAS DEL SISTEMA ══╗

Sistema de Lorenz:
   X: {chaos.get('lorenz_x', 0):.3f}
   Y: {chaos.get('lorenz_y', 0):.3f}  
   Z: {chaos.get('lorenz_z', 0):.3f}

Métricas de Caos:
   Factor caos: {chaos.get('chaos_factor', 0):.3f}
   Entropía: {chaos.get('entropy', 0):.4f}
   Complejidad: {chaos.get('complexity', 0):.4f}
   Predictibilidad: {(1 - chaos.get('entropy', 0)):.4f}

Parámetros activos:
   Spawn NS: {self.config.spawn_ns_pct}%
   Spawn EW: {self.config.spawn_ew_pct}%
   Umbral N: {self.config.n_threshold}
   Dist. R: {self.config.r_distance}px
   Tick: {self.config.tick_ms}ms

Geometría:
   Offset parada: {getattr(self.controller, 'STOP_OFFSET', 25)}px
   Ventana frenado: {getattr(self.controller, 'BRAKE_WINDOW', 35)}px
"""
        
        self.chaos_info.insert(tk.END, text)
        self.chaos_info.configure(state=tk.DISABLED)

    # -----------------------------
    # Método principal
    # -----------------------------
    def run(self):
        """Ejecuta la aplicación"""
        print("Iniciando aplicación de semáforos inteligentes...")
        print("Redimensiona la ventana para probar el canvas responsive")
        print("Haz click en el canvas para ver coordenadas")
        print("Ajusta el factor de caos ANTES de iniciar la simulación")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Aplicación interrumpida por el usuario")
        except Exception as e:
            print(f"Error crítico: {e}")
        finally:
            self.running = False
            print("Aplicación cerrada")


if __name__ == "__main__":
    app = TrafficSimulationApp()
    app.run()