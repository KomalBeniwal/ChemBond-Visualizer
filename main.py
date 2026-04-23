import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='vpython')

import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import turtle
import math
from vpython import sphere, vector, color, canvas as vp_canvas, cylinder, rate
import time

# ---------- MySQL Database Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="your_password",   # 🔑 Replace with your MySQL password
        database="ip_project"
    )

# ---------- Valency Chart ----------
def plot_valencies(compound):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT element_symbol, valency FROM compound_data WHERE compound = %s", (compound,))
    data = cur.fetchall()
    conn.close()

    if not data:
        messagebox.showerror("Error", f"No data found for compound {compound}")
        return None

    symbols, valencies = zip(*data)
    fig, ax = plt.subplots()
    ax.bar(symbols, valencies, color='#3498db')
    ax.set_title(f"Valency Chart for {compound}", fontsize=14, fontweight="bold")
    ax.set_ylabel("Valency")
    ax.set_xlabel("Elements")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig

# ---------- Table Details ----------
def show_compound_details(compound):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT element_name, element_symbol, valency, compound, compound_name, structure, bond_type FROM compound_data WHERE compound = %s", (compound,))
    records = cur.fetchall()
    conn.close()

    if not records:
        messagebox.showerror("Error", f"No details found for compound {compound}")
        return

    top = tk.Toplevel()
    top.title("Compound Details")
    top.geometry("1000x300")

    container = ttk.Frame(top)
    container.pack(fill="both", expand=True)

    tree = ttk.Treeview(container, columns=["Element Name", "Symbol", "Valency", "Compound", "Compound Name", "Structure", "Bond Type"], show='headings')

    for col in ["Element Name", "Symbol", "Valency", "Compound", "Compound Name", "Structure", "Bond Type"]:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    for row in records:
        tree.insert("", "end", values=row)

    tree.grid(row=0, column=0, sticky="nsew")

    ysb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    ysb.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=ysb.set)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)


# ---------- Lewis Structure ----------
def draw_structure(compound):
    try:
        turtle.bye()
        time.sleep(0.5)
    except:
        pass

    turtle.TurtleScreen._RUNNING = True
    wn = turtle.Screen()
    wn.title(f"Lewis Dot Structure: {compound}")
    wn.bgcolor("white")
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()

    valencies = {
        "H": 1,
        "O": 6,
        "N": 5,
        "C": 4,
        "Cl": 7}

    elements = {
        "H2O": [('O', 0, 0), ('H', -100, 100), ('H', 100, 100)],
        "CO2": [('O', -150, 0), ('C', 0, 0), ('O', 150, 0)],
        "CH4": [('C', 0, 0), ('H', -100, 100), ('H', 100, 100), ('H', -100, -100), ('H', 100, -100)],
        "NH3": [('N', 0, 0), ('H', -100, 100), ('H', 100, 100), ('H', 0, -100)],
        "HCl": [('H', -100, 0), ('Cl', 100, 0)],
        "C2H6": [('C', -50, 0), ('C', 50, 0), ('H', -100, 50), ('H', -100, -50), ('H', 0, 50), ('H', 0, -50), ('H', 100, 50), ('H', 100, -50)]}

    coords = elements.get(compound, [])

    for symbol, x, y in coords:
        t.goto(x, y)
        t.write(symbol, align="center", font=("Courier", 16, "bold"))
        if symbol != 'H':
            for i in range(valencies[symbol]):
                angle = i * (360 / valencies[symbol])
                t.goto(x + 30 * math.cos(math.radians(angle)), y + 30 * math.sin(math.radians(angle)))
                t.dot(6, "blue")
                time.sleep(0.05)

    t.pensize(2)
    t.pencolor("black")
    for i in range(1, len(coords)):
        t.penup()
        t.goto(coords[0][1], coords[0][2])
        t.pendown()
        t.goto(coords[i][1], coords[i][2])

    t.penup()
    t.goto(0, -200)
    t.write(f"Lewis Structure of {compound}", align="center", font=("Arial", 14, "bold"))


# ---------- 3D Molecular Viewer ----------
canvas_3d_instance = None

def show_3d(compound):
    global canvas_3d_instance

    compounds = {
        "H2O": [("O", vector(0, 0, 0), color.red), ("H", vector(1, 1, 0), color.white), ("H", vector(-1, 1, 0), color.white)],
        "CO2": [("O", vector(-2, 0, 0), color.red), ("C", vector(0, 0, 0), color.black), ("O", vector(2, 0, 0), color.red)],
        "CH4": [("C", vector(0, 0, 0), color.black), ("H", vector(1, 1, 1), color.white), ("H", vector(-1, -1, 1), color.white), ("H", vector(-1, 1, -1), color.white), ("H", vector(1, -1, -1), color.white)],
        "NH3": [("N", vector(0, 0, 0), color.blue), ("H", vector(1, 1, 0), color.white), ("H", vector(-1, 1, 0), color.white), ("H", vector(0, -1, 0), color.white)],
        "HCl": [("H", vector(-1, 0, 0), color.white), ("Cl", vector(1, 0, 0), color.green)],
        "C2H6": [("C", vector(-1, 0, 0), color.black), ("C", vector(1, 0, 0), color.black), ("H", vector(-2, 1, 0), color.white), ("H", vector(-2, -1, 0), color.white), ("H", vector(0, 1, 1), color.white), ("H", vector(0, -1, 1), color.white), ("H", vector(2, 1, 0), color.white), ("H", vector(2, -1, 0), color.white)]
    }

    atoms = compounds.get(compound)

    if not atoms:
        messagebox.showerror("Error", f"3D data for {compound} not found.")
        return

    if canvas_3d_instance:
        canvas_3d_instance.visible = False

    canvas_3d_instance = vp_canvas(
        title=f"3D Structure: {compound}",
        width=600,
        height=400,
        background=color.white
    )

    spheres = []

    for name, pos, col in atoms:
        s = sphere(pos=pos, radius=0.3, color=col, make_trail=True)
        spheres.append(s)

    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            pi, pj = atoms[i][1], atoms[j][1]
            if (pi - pj).mag < 2.5:
                cylinder(pos=pi, axis=(pj - pi), radius=0.05, color=color.gray(0.5))

    for _ in range(200):
        rate(60)
        for s in spheres:
            s.rotate(angle=0.01, axis=vector(0, 1, 0))



# ---------- Start Program ----------
def start_program():
    compound = combo.get()

    if compound == "Random":
        compound = random.choice(["H2O", "CO2", "CH4", "NH3", "HCl", "C2H6"])
        combo.set(compound)

    for widget in output_frame.winfo_children():
        widget.destroy()

    fig = plot_valencies(compound)
    if fig:
        canvas = FigureCanvasTkAgg(fig, master=output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    tk.Button(output_frame, text="Show Lewis Structure", command=lambda: draw_structure(compound), bg="#1abc9c", fg="white").pack(pady=2)

    tk.Button(output_frame, text="Show 3D Structure", command=lambda: show_3d(compound), bg="#2980b9", fg="white").pack(pady=2)

    tk.Button(output_frame, text="Show Table Info", command=lambda: show_compound_details(compound), bg="#f39c12", fg="white").pack(pady=2)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT bond_type FROM compound_data WHERE compound = %s", (compound,))
    bond = cur.fetchone()
    conn.close()

  if bond:
    tk.Label(
        output_frame,
        text=f"Bond Type: {bond[0]}",
        font=("Arial", 12, "bold"),
        fg="#2c3e50",
        bg="#ecf0f1"
    ).pack(pady=2)



# ---------- GUI Initialization ----------
root = tk.Tk()
root.title("Chemical Bonding Visualizer")
root.geometry("1000x750")
root.configure(bg="#ecf0f1")

header = tk.Label(
    root,
    text="Chemical Bonding Visualizer",
    font=("Helvetica", 22, "bold"),
    fg="#2c3e50",
    bg="#ecf0f1"
)
header.pack(pady=15)

select_frame = tk.Frame(root, bg="#ecf0f1")
select_frame.pack(pady=5)

tk.Label(select_frame, text="Choose Compound: ", font=("Arial", 12), bg="#ecf0f1").pack(side="left")

combo = ttk.Combobox(
    select_frame,
    values=["H2O", "CO2", "NH3", "CH4", "HCl", "C2H6", "Random"],
    state="readonly",
    width=15
)
combo.set("Random")
combo.pack(side="left", padx=5)

visualize_btn = tk.Button(
    select_frame,
    text="Visualize",
    command=start_program,
    bg="#34495e",
    fg="white",
    font=("Arial", 11)
)
visualize_btn.pack(side="left", padx=5)

output_container = tk.Frame(root, bg="#ecf0f1")
output_container.pack(fill="both", expand=True, pady=10)

canvas_main = tk.Canvas(output_container, bg="#ecf0f1")

scrollbar_main = ttk.Scrollbar(output_container, orient="vertical", command=canvas_main.yview)

output_frame = tk.Frame(canvas_main, bg="#ecf0f1")

output_frame.bind(
    "<Configure>",
    lambda e: canvas_main.configure(
        scrollregion=canvas_main.bbox("all")
    )
)

canvas_main.create_window((0, 0), window=output_frame, anchor="nw")
canvas_main.configure(yscrollcommand=scrollbar_main.set)

canvas_main.pack(side="left", fill="both", expand=True)
scrollbar_main.pack(side="right", fill="y")

root.mainloop()


