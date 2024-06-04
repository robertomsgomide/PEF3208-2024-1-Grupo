import tkinter as tk
from tkinter import messagebox
from anastruct import SystemElements

def add_c_force_entry():
    global c_force_entries, row_count, node_options, axis_options
    row_count += 1
    force_label = tk.Label(frame, text="Force " + str(row_count) + ":")
    force_label.grid(row=row_count, column=0, padx=5, pady=5)
    
    node_label = tk.Label(frame, text="Node:")
    node_label.grid(row=row_count, column=1, padx=5, pady=5)
    node_var = tk.StringVar(window)
    node_var.set(node_options[0])
    node_option = tk.OptionMenu(frame, node_var, *node_options)
    node_option.grid(row=row_count, column=2, padx=5, pady=5)

    axis_label = tk.Label(frame, text="Axis:")
    axis_label.grid(row=row_count, column=3, padx=5, pady=5)
    axis_var = tk.StringVar(window)
    axis_var.set(axis_options[0])
    axis_option = tk.OptionMenu(frame, axis_var, *axis_options)
    axis_option.grid(row=row_count, column=4, padx=5, pady=5)


    force_entry = tk.Entry(frame)
    force_entry.grid(row=row_count, column=5, padx=5, pady=5)
    
    c_force_entries.append((node_var, axis_var, force_entry))

def add_d_force_entry():
    global d_force_entries, row_count, segment_options
    row_count += 1
    force_label = tk.Label(frame, text="Force " + str(row_count) + ":")
    force_label.grid(row=row_count, column=0, padx=5, pady=5)
    
    node_label = tk.Label(frame, text="Segment:")
    node_label.grid(row=row_count, column=1, padx=5, pady=5)
    node_var = tk.StringVar(window)
    node_var.set(segment_options[0])
    node_option = tk.OptionMenu(frame, node_var, *segment_options)
    node_option.grid(row=row_count, column=2, padx=5, pady=5)
    
    force_entry = tk.Entry(frame)
    force_entry.grid(row=row_count, column=3, padx=5, pady=5)
    
    d_force_entries.append((node_var, force_entry))

def submit():
    c_forces = []
    for node_var, axis_var, force_entry in c_force_entries:
        try:
            force = float(force_entry.get())
            axis_id = str(axis_var.get())
            node_id = int(node_var.get())
            c_forces.append((node_id, axis_id, force))
        except ValueError:
            messagebox.showerror("Error", "Invalid input for force.")
            return
        
    d_forces = []
    for node_var, force_entry in d_force_entries:
        try:
            force = float(force_entry.get())
            node_id = int(node_var.get())
            d_forces.append((node_id, force))
        except ValueError:
            messagebox.showerror("Error", "Invalid input for force.")
            return
        
    calculate_button.config(state="active")

    
    ss.add_element(location=[[0, 0], [0, 2]])
    ss.add_element(location=[[0, 2], [0, 4]])
    ss.add_element(location=[[0, 4], [3, 4]])
    ss.add_element(location=[[3, 4], [4, 4]])
    ss.add_element(location=[[4, 4], [6, 4]])
    ss.add_element(location=[[6, 4], [7, 4]])
    
    ss.add_internal_hinge(node_id=3)
    ss.add_internal_hinge(node_id=5)
    
    ss.add_support_fixed(node_id=1)
    ss.add_support_roll(node_id=4)
    ss.add_support_roll(node_id=6)
    
    for node_id, axis_id, force in c_forces:
        if axis_id == "X":
            ss.point_load(node_id=node_id, Fx =force)
        else:
            ss.point_load(node_id=node_id, Fy=force)

    for node_id, force in d_forces:
        ss.q_load(q=force, element_id=node_id)
    
    ss.show_structure()
    ss.solve()
    #ss.show_reaction_force()


ss = SystemElements()

# Create tkinter window
window = tk.Tk()
window.title("Input Forces")

c_force_entries = []
d_force_entries = []
row_count = 0
node_options = [1, 2, 3, 4, 5, 6, 7]  # Assuming these are the available node IDs
segment_options = [1, 2, 3, 4, 5, 6]  # Assuming these are the available node IDs
axis_options = ["X", "Y"]

# Frame to contain the force entry widgets
frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

# Button to add a new force entry
add_button = tk.Button(window, text="Add Concentrated Load", command=add_c_force_entry)
add_button.pack(pady=5)

# Button to add a new force entry
add_button = tk.Button(window, text="Add Distributed Load", command=add_d_force_entry)
add_button.pack(pady=5)

# Button to submit forces
submit_button = tk.Button(window, text="Submit", command = submit)
submit_button.pack(pady=5)

calculate_button = tk.Button(window, text="Reaction Forces", command=ss.show_reaction_force, state="disabled")
calculate_button.pack(pady=5)

# Run tkinter event loop
window.mainloop()
