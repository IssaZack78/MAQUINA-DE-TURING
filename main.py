import tkinter as tk
from tkinter import messagebox, filedialog
from turing_machine import TuringMachine
from utils import save_machine, load_machine
import time
import threading

class TuringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")

        # Campos de entrada
        tk.Label(root, text="Estados (separados por coma):").pack()
        self.entry_states = tk.Entry(root, width=50)
        self.entry_states.pack()

        tk.Label(root, text="Estado inicial:").pack()
        self.entry_initial = tk.Entry(root, width=20)
        self.entry_initial.pack()

        tk.Label(root, text="Estados de aceptación (coma):").pack()
        self.entry_accept = tk.Entry(root, width=50)
        self.entry_accept.pack()

        tk.Label(root, text="Alfabeto de cinta (coma):").pack()
        self.entry_tape = tk.Entry(root, width=50)
        self.entry_tape.pack()

        tk.Label(root, text="Transiciones (ejemplo: q0,0=q1,1,R):").pack()
        self.entry_transitions = tk.Text(root, height=5, width=60)
        self.entry_transitions.pack()

        tk.Label(root, text="Cadena de entrada:").pack()
        self.entry_input = tk.Entry(root, width=50)
        self.entry_input.pack()

        # Botones
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Cargar Máquina", command=self.load_machine).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="Ejecutar Paso", command=self.run_step).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="Ejecutar Completa", command=self.run_full).grid(row=0, column=2, padx=5)
        tk.Button(frame_buttons, text="Reiniciar", command=self.reset_machine).grid(row=0, column=3, padx=5)
        tk.Button(frame_buttons, text="Guardar Config.", command=self.save_config).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_buttons, text="Cargar Config.", command=self.load_config).grid(row=1, column=1, padx=5, pady=5)

        # Visualización
        self.label_output = tk.Label(root, text="", font=("Courier", 14))
        self.label_output.pack(pady=10)

        self.tm = None

    def parse_machine_data(self):
        states = [s.strip() for s in self.entry_states.get().split(",")]
        initial = self.entry_initial.get().strip()
        accept = [s.strip() for s in self.entry_accept.get().split(",")]
        tape_alphabet = [s.strip() for s in self.entry_tape.get().split(",")]

        transitions_text = self.entry_transitions.get("1.0", tk.END).strip().split("\n")
        transitions = {}
        for line in transitions_text:
            if not line:
                continue
            left, right = line.split("=")
            state, symbol = left.split(",")
            new_state, write, move = right.split(",")
            transitions[(state.strip(), symbol.strip())] = (new_state.strip(), write.strip(), move.strip())

        tape_input = self.entry_input.get().strip()
        return states, initial, accept, tape_alphabet, transitions, tape_input

    def load_machine(self):
        try:
            states, initial, accept, tape_alphabet, transitions, tape_input = self.parse_machine_data()
            self.tm = TuringMachine(states, [], tape_alphabet, transitions, initial, accept, tape_input)
            self.label_output.config(text="Máquina cargada correctamente ✅")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la máquina: {e}")

    def run_step(self):
        if not self.tm:
            messagebox.showwarning("Advertencia", "Primero carga una máquina.")
            return
        result = self.tm.step()
        self.label_output.config(text=result)

    def run_full(self):
        if not self.tm:
            messagebox.showwarning("Advertencia", "Primero carga una máquina.")
            return

        def run():
            while not self.tm.halted:
                result = self.tm.step()
                self.label_output.config(text=result)
                time.sleep(0.8)
            messagebox.showinfo("Resultado", f"Ejecución terminada: {result}")

        thread = threading.Thread(target=run)
        thread.start()

    def reset_machine(self):
        if self.tm:
            self.tm.reset(self.entry_input.get().strip())
            self.label_output.config(text="Máquina reiniciada 🔄")

    def save_config(self):
        try:
            states, initial, accept, tape_alphabet, transitions, tape_input = self.parse_machine_data()
            data = {
                "states": states,
                "initial": initial,
                "accept": accept,
                "tape_alphabet": tape_alphabet,
                "transitions": {f"{k[0]},{k[1]}": v for k, v in transitions.items()},
                "tape_input": tape_input
            }
            filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filename:
                save_machine(filename, data)
                messagebox.showinfo("Guardar", "Configuración guardada correctamente ✅")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def load_config(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if not filename:
                return
            data = load_machine(filename)
            self.entry_states.delete(0, tk.END)
            self.entry_states.insert(0, ",".join(data["states"]))
            self.entry_initial.delete(0, tk.END)
            self.entry_initial.insert(0, data["initial"])
            self.entry_accept.delete(0, tk.END)
            self.entry_accept.insert(0, ",".join(data["accept"]))
            self.entry_tape.delete(0, tk.END)
            self.entry_tape.insert(0, ",".join(data["tape_alphabet"]))
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, data["tape_input"])

            self.entry_transitions.delete("1.0", tk.END)
            for key, value in data["transitions"].items():
                self.entry_transitions.insert(tk.END, f"{key}={','.join(value)}\n")

            messagebox.showinfo("Cargar", "Configuración cargada correctamente ✅")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringApp(root)
    root.mainloop()