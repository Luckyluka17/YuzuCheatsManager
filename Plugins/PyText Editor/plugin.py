import tkinter as tk
from tkinter.messagebox import showinfo

window3 = tk.Tk()

file = "''"

def save():
    global file, text_area, window3
    with open(file, "w") as f:
        f.write(text_area.get("1.0",'end-1c'))
        f.close()
    showinfo("Succès", "Le fichier a été sauvegardé")
    window3.destroy()


with open(file, "r") as f:
    file_data = f.read()
    f.close()

window3.title("PyText Editor")
window3.geometry("400x500")
window3.resizable(False, False)

save_button1 = tk.Button(
    window3,
    text="Sauvegarder et fermer",
    command=save
)
save_button1.pack()

text_area = tk.Text(
    window3,
    height=400,
    bg='#4d4d4d',
    fg='white',
    font=("Calibri", 13)
)
text_area.pack()

text_area.insert('1.0', file_data)

window3.mainloop()