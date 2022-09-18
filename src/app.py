from tkinter import ttk
import tkinter as tk
import wget
import requests
from bs4 import BeautifulSoup
from getpass import getuser
import os
from tkinter.messagebox import showinfo, showerror, showwarning
from threading import Thread
import sys
import json
import codecs
import webbrowser as web

window = tk.Tk()

version = 1.1




games_list = {}
game_name = ""
default_settings = {
    "verify_updates": True,
    "notify_incompatible_games": True,
    "yuzu_folder": f"C:\\Users\\{getuser()}\\AppData\\Roaming\\yuzu\\",
    "language": "Français"
}

verify_updates = tk.BooleanVar()
notify_incompatible_games = tk.BooleanVar()
toggle_language = tk.IntVar()

# Vérification du fichier de paramètres
if os.path.exists("settings.json"):
    try:
        with codecs.open("settings.json", "r", "utf-8") as f:
            settings = json.loads(f.read())
            f.close()
    except:
        with codecs.open("settings.json", "w", "utf-8") as f:
            json.dump(default_settings, f)
            f.close()
    
        with codecs.open("settings.json", "r", "utf-8") as f:
            settings = json.loads(f.read())
            f.close()
else:
    with codecs.open("settings.json", "w", "utf-8") as f:
        json.dump(default_settings, f)
        f.close()
    
    with codecs.open("settings.json", "r", "utf-8") as f:
        settings = json.loads(f.read())
        f.close()


# Application des paramètres récupérés
try:
    verify_updates.set(settings["verify_updates"])
    notify_incompatible_games.set(settings["notify_incompatible_games"])
    yuzu_folder = settings["yuzu_folder"]
    language = settings["language"]
except:
    with codecs.open("settings.json", "w", "utf-8") as f:
        json.dump(default_settings, f)
        f.close()

    with codecs.open("settings.json", "r", "utf-8") as f:
        settings = json.loads(f.read())
        f.close()
    
    verify_updates.set(settings["verify_updates"])
    notify_incompatible_games.set(settings["notify_incompatible_games"])
    yuzu_folder = settings["yuzu_folder"]
    language = settings["language"]

# Récupérer la langue
with requests.get(f"https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/Languages/{language}.json") as r:
    data_language = json.loads(r.text)
    f.close()

if language == "Français":
    toggle_language.set(1)
elif language == "English":
    toggle_language.set(2)


# Scanner les plugins
if not os.path.exists("Plugins"):
    os.mkdir("Plugins")

plugins = {}

for plugin in os.listdir("Plugins"):
    if os.path.exists(f"Plugins\\{plugin}\\plugin.json"):
        try:
            with codecs.open(f"Plugins\\{plugin}\\plugin.json") as f:
                plugin_data = json.loads(f.read())
                f.close()
        
            plugins[plugin_data['name']] = {
                "name": plugin_data['name'],
                "version": plugin_data['version'],
                "developper": plugin_data['developper']
            }

            del plugin_data
        except:
            print("Erreur plugin invalide")

# Vérification de la version installée et comparaison avec la dernière version
with requests.get("https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/appinfo.json") as r:
    data_app = json.loads(r.text)

if data_app["latest-version"] > version:
    showwarning("Nouvelle version", data_language["messages"]["warning_messages"]["3"])
    
# 
if os.path.exists(f"{settings['yuzu_folder']}\\load\\"):
    games = os.listdir(f"{settings['yuzu_folder']}load\\")
    for game in games:
        if "." in game:
            games.remove(game)
    
    for game in games:
        with requests.get(f"https://github.com/ibnux/switch-cheat/tree/master/sxos/titles/{game}") as r:
            soup = BeautifulSoup(r.content, 'html.parser')
            for i in soup.find_all(class_="js-navigation-open Link--primary"):
                game_name = i.text
            games_list[str(game_name).replace("-", " ").replace(".txt", "").replace("™", "").upper()] = game
            games[games.index(game)] = str(game_name).replace("-", " ").replace(".txt", "").replace("™", "").upper()
else:
    showerror("Erreur", data_language["messages"]["error_messages"]["1"])
    exit()

def download_cheats():
    if cb1.get() == "":
        showerror("Erreur", data_language["messages"]["error_messages"]["2"])
    else:
        with requests.get(f"https://github.com/ibnux/switch-cheat/tree/master/sxos/titles/{games_list[cb1.get()]}/cheats") as r:
                soup = BeautifulSoup(r.content, 'html.parser')
                if os.path.exists(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}") == False:
                    os.mkdir(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}")
                if os.path.exists(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats") == False:
                    os.mkdir(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats")
                if os.listdir(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats") == []:
                    for i in soup.find_all(class_="js-navigation-open Link--primary"):
                        file_name = i.text
                        wget.download(f"https://raw.githubusercontent.com/ibnux/switch-cheat/master/sxos/titles/{games_list[cb1.get()]}/cheats/{file_name}", f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{file_name.upper()}")
                    showinfo("Téléchargements de cheats", data_language["messages"]["info_messages"]["1"])
                else:
                    showerror("Erreur", data_language["messages"]["error_messages"]["3"])

def apply_settings():
    global settings
    with open("settings.json", "w") as f:
        if toggle_language.get() == 1:
            language = "Français"
        elif toggle_language.get() == 2:
            language = "English"

        if language != settings["language"]:
            showinfo("Changement de langue", data_language["messages"]["info_messages"]["4"])
        
        settings = {
            "verify_updates": verify_updates.get(),
            "notify_incompatible_games": notify_incompatible_games.get(),
            "yuzu_folder": yuzu_folder,
            "language": language,
        }
        json.dump(settings, f)

def open_cheat_manager():
    def del_all_cheats():
        if cb1.get() != "":
            if os.path.exists(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats"):
                os.system(f'rmdir /s /q "{settings["yuzu_folder"]}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats"')
            window1.destroy()
            showinfo("Cheats supprimés", data_language["messages"]["info_messages"]["2"]) 
        else:
            showerror("Erreur", data_language["messages"]["error_messages"]["2"])

    def get_data():
        tree.delete(*tree.get_children())
        try:
            with open(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{cb2.get()}") as f:
                data = f.read()
                f.close()
        except FileNotFoundError:
            showerror("Erreur", data_language["messages"]["error_messages"]["4"])

        data = data.split("[")
        print(data)
        if data == ['\n']:
            showwarning("Attention", data_language["messages"]["warning_messages"]["1"])
        else:
            data.remove('')

        for d in data:
            d_temp = d.split("]")
            tree.insert(parent='', text='', index="end", values=(d_temp[0], d_temp[1].replace("\n", "|").replace("||", "|")))
            del d_temp
                
        print(data)

    def edit_file():
        if "PyText Editor (FR)" in plugins.keys():
            file2edit = f'{settings["yuzu_folder"]}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{cb2.get()}'
            exec(codecs.open("Plugins\\PyText Editor\\plugin.py", "r", "utf-8").read().replace("''", file2edit.replace("\\", "\\\\")))
        else:
            os.system(f'notepad "{settings["yuzu_folder"]}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{cb2.get()}"')

    def del_selected_cheat():
        try:
            curItem = tree.focus()
            with open(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{cb2.get()}", "r") as f:
                file_content = f.read()
                print(tree.item(curItem))
                file_content = file_content.replace("[" + tree.item(curItem)["values"][0].replace("'", "") + "]", "").replace(tree.item(curItem)["values"][1].replace("|", "\n"), "")
                f.close()
                print(file_content)
            with open(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{cb2.get()}", "w") as f:
                f.write(file_content)
                del file_content
                f.close()
            get_data()
        except:
            showerror("Erreur", data_language["messages"]["error_messages"]["5"])



    window1 = tk.Tk()
    window1.title("Cheats Manager")
    window1.iconbitmap("icon.ico")
    window1.resizable(False, False)
    window1.geometry("600x330")

    ttk.Label(
        window1,
        text=f"{data_language['texts']['2']} {cb1.get()}",
        font=("Calibri", 15)
    ).pack()

    tree = ttk.Treeview(
        window1
    )
    tree['columns']=(data_language["texts"]["3"], data_language["texts"]["4"])
    tree.column('#0', width=0, stretch=False)
    tree.column(data_language["texts"]["3"], anchor='center', width=350)
    tree.column(data_language["texts"]["4"], anchor='center', width=230)

    tree.heading('#0', text='', anchor='center')
    tree.heading(data_language["texts"]["3"], text=data_language["texts"]["3"], anchor='center')
    tree.heading(data_language["texts"]["4"], text=data_language["texts"]["4"], anchor='center')

    tree.pack()

    cb2 = ttk.Combobox(
        window1,
        values=os.listdir(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats"),
        state="readonly",
    )
    cb2.place(x=385, y=265)

    ttk.Label(
        window1,
        text=data_language["texts"]["5"],
        font=("Calibri", 12)
    ).place(x=265, y=263)

    bouton3 = ttk.Button(
        window1,
        text=data_language["buttons"]["4"],
        cursor="hand2",
        command=window1.destroy
    )
    bouton3.place(x=10, y=263)

    bouton4 = ttk.Button(
        window1,
        text=data_language["buttons"]["5"],
        cursor="hand2",
        command=del_all_cheats
    )
    bouton4.place(x=90, y=263)

    bouton5 = tk.Button(
        window1,
        text="✅",
        command=get_data,
        cursor="hand2"
    )
    bouton5.place(x=530, y=261)

    bouton6 = tk.Button(
        window1,
        text="✒️",
        command=edit_file,
        cursor="hand2"
    )
    bouton6.place(x=560, y=261)

    bouton8 = ttk.Button(
        window1,
        text=data_language["buttons"]["6"],
        cursor="hand2",
        command=del_selected_cheat
    )
    bouton8.place(x=37, y=296)

    window1.mainloop()

def open_cheat_manager1():
    if cb1.get() != "":
        if os.path.exists(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats"):
            Thread(target=open_cheat_manager()).run
        else:
            showerror("Erreur", data_language["messages"]["error_messages"]["6"])
    else:
        showerror("Erreur", data_language["messages"]["error_messages"]["2"])

def change_yuzu_folder():
    from tkinter.filedialog import askdirectory
    yuzu_folder = askdirectory(title="Séléctionnez le dossier de Yuzu").replace("/", "\\")
    if os.path.exists(f"{yuzu_folder}\\nand") and os.path.exists(f"{yuzu_folder}\\load"):
        apply_settings()
        showinfo("Dossier de Yuzu modifié", data_language["messages"]["info_messages"]["3"])
    else:
        yuzu_folder = settings["yuzu_folder"]
        showerror("Erreur", data_language["messages"]["error_messages"]["7"])

window.title("Yuzu Cheat Manager")
window.iconbitmap("icon.ico")
window.geometry("400x185")
window.resizable(False, False)

menubar = tk.Menu()
file_menu = tk.Menu(tearoff=0)
help_menu = tk.Menu(tearoff=0)
settings_menu = tk.Menu(tearoff=0)
language_menu = tk.Menu(tearoff=0)
plugins_menu = tk.Menu(tearoff=0)
# Menu principal
menubar.add_cascade(label=data_language["head_menu"]["file_menu"]["title"], menu=file_menu)
menubar.add_cascade(label=data_language["head_menu"]["plugins_menu"]["title"], menu=plugins_menu)
menubar.add_cascade(label=data_language["head_menu"]["help_menu"]["title"], menu=help_menu)
# Menu Fichier
file_menu.add_command(label=data_language["head_menu"]["file_menu"]["1"], command=download_cheats)
file_menu.add_command(label=data_language["head_menu"]["file_menu"]["2"], command=open_cheat_manager1)
file_menu.add_cascade(label=data_language["head_menu"]["settings_menu"]["title"], menu=settings_menu)
file_menu.add_separator()
file_menu.add_command(label=data_language["head_menu"]["file_menu"]["4"], command=sys.exit)
# Menu des paramètres
settings_menu.add_checkbutton(label=data_language["head_menu"]["settings_menu"]["1"], variable=verify_updates, command=apply_settings)
settings_menu.add_checkbutton(label=data_language["head_menu"]["settings_menu"]["2"], variable=notify_incompatible_games, command=apply_settings)
settings_menu.add_command(label=data_language["head_menu"]["settings_menu"]["3"], command=change_yuzu_folder)
settings_menu.add_cascade(label=data_language["head_menu"]["language_menu"]["title"], menu=language_menu)
# Menu de séléction des langues
language_menu.add_radiobutton(label="Français", variable=toggle_language, command=apply_settings, value=1)
language_menu.add_radiobutton(label="English", variable=toggle_language, command=apply_settings, value=2)
# Menu plugins
for plugin in plugins.keys():
    plugins_menu.add_command(label=f"{plugin} | {plugins[plugin]['version']} | {plugins[plugin]['developper']}")
plugins_menu.add_separator()
plugins_menu.add_command(label=data_language["head_menu"]["plugins_menu"]["1"], command=lambda: web.open("https://www.yuzucheatsmanager.tk/plugins.html#"))
# Menu Aide
help_menu.add_command(label=data_language["head_menu"]["help_menu"]["1"], command=lambda: web.open("mailto:contact@luckyluka17.cf"))
help_menu.add_command(label=data_language["head_menu"]["help_menu"]["2"], command=lambda: web.open("https://discord.gg/KvjkS3P3Gh"))
help_menu.add_command(label=data_language["head_menu"]["help_menu"]["3"], command=lambda: web.open("https://github.com/Luckyluka17/YuzuCheatsManager/wiki"))

# Supression des espaces dans la liste games
for i in range(len(games)):
    if '' in games:
        games.remove('')


ttk.Label(
    window,
    text=data_language["texts"]["1"],
    font=("Calibri", 15)
).pack()

cb1 = ttk.Combobox(
    window,
    values=games,
    state="readonly",
    width=40,
    cursor="hand2"
)
cb1.pack()

bouton1 = ttk.Button(
    window,
    text=data_language["buttons"]["1"],
    cursor="hand2",
    command=download_cheats
)
bouton1.place(x=50, y=75)

bouton2 = ttk.Button(
    window,
    text=data_language["buttons"]["2"],
    cursor="hand2",
    command=open_cheat_manager1
)
bouton2.place(x=180, y=75)

bouton7 = ttk.Button(
    window,
    text=data_language["buttons"]["3"],
    cursor="hand2",
    command=lambda: os.startfile(f"{settings['yuzu_folder']}\\load\\{games_list[cb1.get()]}\\")
)
bouton7.place(x=120, y=110)

# Vérifier si un jeu est invalide ou non
if '' in games_list.keys() and settings['notify_incompatible_games'] == True:
    showwarning("Attention", data_language["messages"]["warning_messages"]["2"])

window.config(menu=menubar)
window.mainloop()