import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Viewer and Predictor")
        self.root.geometry("900x600")

        self.df = None

        # Buttons
        tk.Button(root, text="Load Data", command=self.load_data).pack(pady=5)
        tk.Button(root, text="Predict", command=self.predict).pack(pady=5)

        # Prediction Label
        self.prediction_label = tk.Label(root, text="Prediction will appear here", fg="blue")
        self.prediction_label.pack(pady=5)

        # Data display
        self.text_area = tk.Text(root, height=15)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10)

        # Log area
        self.log_label = tk.Label(root, text="Status: Waiting for action")
        self.log_label.pack(pady=5)

        # Plot area
        self.figure = plt.Figure(figsize=(6,3))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack()

    def load_data(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            self.df = pd.read_csv(file_path)

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, self.df.to_string())

            self.plot_data()
            self.log_label.config(text="Status: Data loaded successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_data(self):
        self.ax.clear()
        self.ax.plot(self.df["sensor_value"])
        self.ax.set_title("Sensor Value Over Time")
        self.ax.set_ylabel("Sensor Value")
        self.canvas.draw()

    def predict(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first")
            return

        avg_value = self.df["sensor_value"].mean()

        if avg_value > 50:
            result = "Prediction: System requires calibration"
        else:
            result = "Prediction: System functioning normally"

        self.prediction_label.config(text=result)
        self.log_label.config(text=f"Status: Prediction calculated (Avg = {avg_value:.2f})")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataViewerApp(root)
    root.mainloop()
