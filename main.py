import tkinter as tk
from individual import individual_mode
from comparative import comparative_mode

def open_individual_mode():
    """Open Individual Mode for simulation."""
    individual_mode()

def open_comparative_mode():
    """Open Comparative Mode for simulation."""
    comparative_mode()

def main():
    """Main function to launch the GUI."""
    root = tk.Tk()
    root.title("Page Replacement Algorithm Simulator")
    root.geometry("600x400")

    label_title = tk.Label(root, text="Page Replacement Simulator", font=("Arial", 18, "bold"))
    label_title.pack(pady=20)

    btn_individual = tk.Button(
        root, text="Individual Mode", font=("Arial", 14), command=open_individual_mode
    )
    btn_individual.pack(pady=20)

    btn_comparative = tk.Button(
        root, text="Comparative Mode", font=("Arial", 14), command=open_comparative_mode
    )
    btn_comparative.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
