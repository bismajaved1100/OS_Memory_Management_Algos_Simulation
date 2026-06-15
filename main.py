import tkinter as tk
from tkinter import messagebox, ttk
from algorithms import first_fit, best_fit, worst_fit, next_fit

class MemorySimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 6: Memory Management Simulator")
        self.root.geometry("800x600")

        # Data storage
        self.history = []
        self.current_step = 0
        self.process_sizes = []

        self.setup_ui()

    def setup_ui(self):
        # Input Section
        input_frame = tk.Frame(self.root, pady=20)
        input_frame.pack()

        tk.Label(input_frame, text="Block Sizes (comma separated):").grid(row=0, column=0)
        self.block_entry = tk.Entry(input_frame, width=30)
        self.block_entry.insert(0, "100, 500, 200, 300, 600")
        self.block_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Process Sizes (comma separated):").grid(row=1, column=0)
        self.proc_entry = tk.Entry(input_frame, width=30)
        self.proc_entry.insert(0, "212, 417, 112, 426")
        self.proc_entry.grid(row=1, column=1)

        # Algorithm Selection
        tk.Label(input_frame, text="Select Algorithm:").grid(row=2, column=0)
        self.algo_var = tk.StringVar(value="First Fit")
        self.algo_menu = ttk.Combobox(input_frame, textvariable=self.algo_var, 
                                     values=["First Fit", "Best Fit", "Worst Fit", "Next Fit"])
        self.algo_menu.grid(row=2, column=1)

        # Controls
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Start Simulation", command=self.start_sim, bg="green", fg="white").pack(side="left", padx=5)
        self.next_btn = tk.Button(btn_frame, text="Next Step >>", command=self.show_next, state="disabled")
        self.next_btn.pack(side="left")

        # Visualization Area
        self.canvas = tk.Canvas(self.root, width=700, height=300, bg="white", highlightbackground="black")
        self.canvas.pack(pady=20)
        
        self.status_label = tk.Label(self.root, text="Enter data and press Start", font=("Arial", 12, "bold"))
        self.status_label.pack()

    def start_sim(self):
        try:
            blocks = [int(x.strip()) for x in self.block_entry.get().split(",")]
            self.process_sizes = [int(x.strip()) for x in self.proc_entry.get().split(",")]
            algo = self.algo_var.get()

            # Map selection to function
            mapping = {"First Fit": first_fit, "Best Fit": best_fit, 
                       "Worst Fit": worst_fit, "Next Fit": next_fit}
            
            self.history, _ = mapping[algo](blocks, self.process_sizes)
            self.current_step = 0
            self.next_btn.config(state="normal")
            self.draw_memory(self.history[0])
            self.update_status(0)
        except Exception as e:
            messagebox.showerror("Input Error", "Please check your numbers and try again.")

    def update_status(self, step):
        p_size = self.process_sizes[step]
        self.status_label.config(text=f"Step {step+1}: Allocating Process of {p_size} KB")

    def draw_memory(self, blocks):
        self.canvas.delete("all")
        
        x_start = 50
        y_bottom = 250
        width = 100
        
        process_colors = {
            "P1": "#e74c3c", "P2": "#2ecc71", "P3": "#f1c40f",
            "P4": "#9b59b6", "P5": "#e67e22", "P6": "#1abc9c",
            "P7": "#34495e", "P8": "#e84393"
        }
        
        max_block_val = max(b['size'] for b in blocks)
        
        for b in blocks:
            # 1. Block ki total unchayi (Height)
            full_h = (b['size'] / max_block_val) * 180 + 20 
            
            # 2. Pehle poora khali White rectangle banayen
            self.canvas.create_rectangle(x_start, y_bottom - full_h, x_start + width, y_bottom, outline="black", width=2, fill="#ffffff")
            
            # 3. Block ke andar ki processes ko "Stack" (teh dar teh) draw karna
            current_y_offset = 0
            
            # Agar algorithms ne p_list bheji hai to usay loop mein chalayen
            if "p_list" in b:
                for proc in b["p_list"]:
                    # Har process ki unchayi uske size ke mutabiq
                    proc_h = (proc['size'] / b['size']) * full_h
                    
                    # Process ka color nikaalna
                    p_name = proc['name']
                    color = process_colors.get(p_name, "#3498db") # Agar P9 ho to default blue
                    
                    # SEGMENT DRAW KARNA (Har process ka apna rectangle)
                    self.canvas.create_rectangle(
                        x_start + 1, 
                        y_bottom - current_y_offset - proc_h, 
                        x_start + width - 1, 
                        y_bottom - current_y_offset - 1, 
                        fill=color, outline="white" # White outline taake processes alag dikhen
                    )
                    
                    # Process ka Naam uske apne segment ke beech mein
                    self.canvas.create_text(
                        x_start + width/2, 
                        y_bottom - current_y_offset - (proc_h/2), 
                        text=f"{p_name}\n({proc['size']}K)", 
                        fill="white", font=("Arial", 8, "bold")
                    )
                    
                    # Agle process ko iske upar rakhne ke liye offset barha den
                    current_y_offset += proc_h

            # LABELS
            self.canvas.create_text(x_start + width / 2, y_bottom + 15, text=f"Block {b['id']}", font=("Arial", 9, "bold"))
            self.canvas.create_text(x_start + width / 2, y_bottom - full_h - 10, text=f"{b['remaining']} KB left", font=("Arial", 9, "italic"), fill="#16a085")
            
            x_start += 130

    def show_next(self):
        self.current_step += 1
        if self.current_step < len(self.history):
            self.draw_memory(self.history[self.current_step])
            self.update_status(self.current_step)
        else:
            self.next_btn.config(state="disabled")
            self.status_label.config(text="Simulation Complete!")
            messagebox.showinfo("Done", "All processes have been processed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemorySimApp(root)
    root.mainloop()