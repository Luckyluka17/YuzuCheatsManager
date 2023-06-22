import codecs
import json
import os
import sys
import time
import tkinter as tk
import webbrowser as web
from getpass import getuser
from threading import Thread
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo, showwarning

import requests
import wget
from bs4 import BeautifulSoup
from pypresence import Presence

window = tk.Tk()
launch_window = tk.Tk()

start_time = time.time()

# Version actuelle du logiciel
version = 1.9


# Téléchargement des fichiers requis (fichiers temporaires)
dfiles = [
    ["https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/img/logo100px.png", "logo100px.png"],
    ["https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/img/icon.ico", "icon.ico"],
    ["https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/img/logodev100px.png", "logodev100px.png"],
    ["https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/img/Brands-icons/discord-icon.png", "discord_logo.png"],
    ["https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/img/Brands-icons/github-icon.png", "github_logo.png"]
]
# Vérification du dossier temporaire
if not os.path.exists(f"{os.getcwd()}\\YuzuCheatsManager"):
    os.mkdir(f"{os.getcwd()}\\YuzuCheatsManager")

# Cacher la fenêtre principale le temps que le logiciel télécharge les assets
window.withdraw()

launch_window.title("YuzuCheatsManager")
launch_window.geometry("200x90")
launch_window.resizable(False, False)
launch_window.overrideredirect(True)

if not os.path.exists(f"{os.getcwd()}\\YuzuCheatsManager\\launch.png"):
    wget.download("https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/img/logo50px.png", f"{os.getcwd()}\\YuzuCheatsManager\\launch.png")

launch_image = tk.PhotoImage(master=launch_window, file=f"{os.getcwd()}\\YuzuCheatsManager\\launch.png")

ttk.Label(
    launch_window,
    image=launch_image
).place(x=15, y=20)

ttk.Label(
    launch_window,
    text="Démarrage",
    font=("Calibri", 17)
).place(x=80, y=20)

ttk.Label(
    launch_window,
    text=f"Version {version}",
    font=("Calibri", 8)
).place(x=83, y=50)

launch_window.eval('tk::PlaceWindow . center')
launch_window.update()

for file in dfiles:
    try:
        os.remove(f"{os.getcwd()}\\YuzuCheatsManager\\{file[1]}")
    except:
        pass

for file in dfiles:
    wget.download(file[0], f"{os.getcwd()}\\YuzuCheatsManager\\{file[1]}")

# Suppression de l'installeur si il est présent
if os.path.exists("updater.bat"):
    os.remove("updater.bat")

games_list = {}
game_name = ""
default_settings = {
    "verify_updates": True,
    "notify_incompatible_games": True,
    "yuzu_folder": f"C:\\Users\\{getuser()}\\AppData\\Roaming\\yuzu\\",
    "language": "Français",
    "discord_rpc": True,
    "auth_key": "",
    "cheats_names": {},
    "dev_mode": False,
    "servers": {
        "Switch Cheats": "https://github.com/ibnux/switch-cheat/tree/master/atmosphere/titles/"
    },
    "actual_server": 1,
}


# Mise en place des variables tkinter
verify_updates = tk.BooleanVar()
notify_incompatible_games = tk.BooleanVar()
toggle_language = tk.IntVar()
discord_rpc = tk.BooleanVar()
auth_key_preview = ""
cheats_names = {}
dev_mode = tk.BooleanVar()
toggle_provider = tk.IntVar()

def update_ycm():
    launch_window.destroy()
    wget.download("https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/src/updater.bat", "updater.bat")
    os.startfile("updater.bat")
    window.destroy()
    sys.exit()


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
    discord_rpc.set(settings["discord_rpc"])
    cheats_names = settings['cheats_names']
    dev_mode.set(settings["dev_mode"])
    toggle_provider.set(settings["actual_server"])
    actual_server = settings["servers"][str(list(settings["servers"].keys())[settings["actual_server"]-1])]
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
    discord_rpc.set(settings["discord_rpc"])
    cheats_names = settings['cheats_names']
    dev_mode.set(settings["dev_mode"])
    toggle_provider.set(settings["actual_server"])
    actual_server = settings["servers"][str(list(settings["servers"].keys())[settings["actual_server"]-1])]

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
                "developper": plugin_data['developper'],
                "category": plugin_data['category']
            }

            del plugin_data
        except:
            print("Erreur plugin invalide")


# Vérification et mise en place des serveurs customs
if not settings["servers"].get("Switch Cheats") == "https://github.com/ibnux/switch-cheat/tree/master/atmosphere/titles/":
    showerror("Erreur", "Une erreur est survenue lors de la vérification des serveurs. Vérifiez votre fichier des paramètres.")
    sys.exit()
else:
    servers = settings["servers"]


# Vérification de la version installée et comparaison avec la dernière version + affichage du message d'information s'il y en a un
with requests.get("https://raw.githubusercontent.com/Luckyluka17/YuzuCheatsManager/main/appinfo.json") as r:
    data_app = json.loads(r.text)

if data_app["latest-version"] > version and verify_updates.get() == True:
    update_ycm()
    
if data_app["informations"] != "":
    window.withdraw()
    showinfo("Information", data_app["informations"])

# Démarrer la RPC Discord
if discord_rpc.get() == True:
    try:
        RPC = Presence(1022537407448490125)
        RPC.connect()
        RPC.update(
            details=f"Installez des cheats sur Yuzu",
            state=f"Plugins installés : {len(plugins)}",
            large_image="logo",
            large_text="Yuzu Cheats Manager",
            buttons=[{"label": "Télécharger le logiciel", "url": "https://yuzucheatsmanager.tk/downloads"}],
            start=int(time.time())
        )
    except:
        print("Discord n'est pas detecté")


# Récupérer les images
if dev_mode.get():
    img_home = tk.PhotoImage(master=window, file=f"{os.getcwd()}\\YuzuCheatsManager\\logodev100px.png")
else:
    img_home = tk.PhotoImage(master=window,file=f"{os.getcwd()}\\YuzuCheatsManager\\logo100px.png")
img_discord = tk.PhotoImage(master=window, file=f"{os.getcwd()}\\YuzuCheatsManager\\discord_logo.png")
img_github = tk.PhotoImage(master=window, file=f"{os.getcwd()}\\YuzuCheatsManager\\github_logo.png")

# Vérifier le dossier Yuzu et télécharger les données des jeux
if os.path.exists(f"{settings['yuzu_folder']}\\load\\"):
    games = os.listdir(f"{settings['yuzu_folder']}load\\")
    for game in games:
        if "." in game:
            games.remove(game)
    
    try:
        for game in games:
            with requests.get("https://raw.githubusercontent.com/blawar/titledb/master/BE.fr.json") as r:
                data = json.loads(r.text)
                r.close()

            games_data = {}

            for key in data.keys():
                games_data[str(data[key]["id"])] = str(data[key]["name"])

            

            del data
            if game in games_data:
                games[games.index(game)] = games_data[game].replace("™", "").replace("+", "avec").upper()
                games_list[games_data[game].replace("™", "").replace("+", "avec").upper()] = game
                print("Jeu trouvé : " + game)
            
        print(games_list)
    except:
        showerror("Erreur", data_language["messages"]["error_messages"]["8"])
        sys.exit()
else:
    showerror("Erreur", data_language["messages"]["error_messages"]["1"])
    sys.exit()

def download_cheats():
    if cb1.get() == "":
        showerror("Erreur", data_language["messages"]["error_messages"]["2"])
    else:
        try:
            with requests.get(f"{actual_server}{games_list[cb1.get()]}/cheats") as r:
                    soup = BeautifulSoup(r.content, 'html.parser')
                    if os.path.exists(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}") == False:
                        os.mkdir(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}")
                    if os.path.exists(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats") == False:
                        os.mkdir(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats")
                    if os.listdir(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats") == []:
                        # Vérifier si le dépôt des cheats possède des cheats pour ce jeu, si oui, alors téléchargement
                        test = []
                        for f in soup.find_all(class_="js-navigation-open Link--primary"):
                            test.append(f.text)
                        if test == []:
                            os.system("rmdir /s /q " + f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}")
                            showerror("Erreur", "Le dépôt de cheats actuel ne possède pas de cheat(s) pour ce jeu.")
                        else:
                            for i in soup.find_all(class_="js-navigation-open Link--primary"):
                                file_name = i.text
                                wget.download(f"{actual_server.replace('/tree', '').replace('https://github.com/', 'https://raw.githubusercontent.com/')}{games_list[cb1.get()]}/cheats/{file_name}", f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{file_name.upper()}")
                            showinfo("Téléchargements des cheats", data_language["messages"]["info_messages"]["1"])
                        del test
                    else:
                        showerror("Erreur", data_language["messages"]["error_messages"]["3"])
        except KeyError:
            showerror("Erreur", "Jeu invalide.")


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
            "discord_rpc": discord_rpc.get(),
            "auth_key": "",
            "cheats_names": cheats_names,
            "dev_mode": dev_mode.get(),
            "servers": servers,
            "actual_server": toggle_provider.get(),
        }
        json.dump(settings, f, indent=4)

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
        if data == ['\n'] or data == [] or data == ['']:
            showwarning("Attention", data_language["messages"]["warning_messages"]["1"])
        else:
            try:
                data.remove('')
            except:
                pass
        
        if '\n' in data:
            data.remove('\n')

        try:
            for d in data:
                d_temp = d.split("]")
                tree.insert(parent='', text='', index="end", values=(d_temp[0], d_temp[1].replace("\n", "|").replace("||", "|")))
                del d_temp
        except:
            data.pop(0)
            for d in data:
                d_temp = d.split("]")
                tree.insert(parent='', text='', index="end", values=(d_temp[0], d_temp[1].replace("\n", "|").replace("||", "|")))
                del d_temp

        if cb2.get() in cheats_names:
            cheat_name.delete(0, tk.END)
            cheat_name.insert(0, cheats_names[cb2.get()])
        else:
            cheat_name.delete(0, tk.END)


        print(data)

    def edit_file():
        if "PyText Editor (FR)" in plugins.keys():
            file2edit = f'{settings["yuzu_folder"]}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{cb2.get()}'
            exec(codecs.open("Plugins\\PyText Editor\\plugin.py", "r", "utf-8").read().replace("''", file2edit.replace("\\", "\\\\")))
        else:
            os.system(f'notepad "{settings["yuzu_folder"]}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats\\{cb2.get()}"')


    def apply_name():
        if cb2.get() != "" or cb2.get() != " ":
            if cheat_name != "" or not cheat_name.startswith(" "):
                cheats_names[cb2.get()] = cheat_name.get()
        apply_settings()

    
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
    window1.iconbitmap(f"{os.getcwd()}\\YuzuCheatsManager\\icon.ico")
    window1.resizable(False, False)
    window1.geometry("600x330")

    ttk.Label(
        window1,
        text=f"{data_language['texts']['2']} {cb1.get()}",
        font=("Calibri", 15),
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

    # Récupérer tous les fichiers du répertoire de cheats
    cheats_files = os.listdir(f"{settings['yuzu_folder']}load\\{games_list[cb1.get()]}\\{games_list[cb1.get()]}\\cheats")


    cb2 = ttk.Combobox(
        window1,
        values=cheats_files,
        state="readonly",
    )
    cb2.place(x=385, y=265)

    ttk.Label(
        window1,
        text=data_language["texts"]["5"],
        font=("Calibri", 12),
    ).place(x=265, y=263)

    ttk.Label(
        window1,
        text="Nom du cheat",
        font=("Calibri", 12),
    ).place(x=265, y=292)

    cheat_name = ttk.Entry(
        window1,
        width=23,
    )
    cheat_name.place(x=385, y=292)

    bouton10 = tk.Button(
        window1,
        text="✅",
        cursor="hand2",
        font=("Calibri", 8),
        command=apply_name
    )
    bouton10.place(x=530, y=291)

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

    window1.configure()
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
    yuzu_folder = askdirectory(title="Séléctionnez le dossier de Yuzu").replace("/", "\\")
    if os.path.exists(f"{yuzu_folder}\\nand") and os.path.exists(f"{yuzu_folder}\\load"):
        apply_settings()
        showinfo("Dossier de Yuzu modifié", data_language["messages"]["info_messages"]["3"])
    else:
        yuzu_folder = settings["yuzu_folder"]
        showerror("Erreur", data_language["messages"]["error_messages"]["7"])


window.title("Yuzu Cheat Manager")
window.iconbitmap(f"{os.getcwd()}\\YuzuCheatsManager\\icon.ico")
window.geometry("400x282")
window.resizable(False, False)

window.deiconify()

menubar = tk.Menu()
file_menu = tk.Menu(tearoff=0)
help_menu = tk.Menu(tearoff=0)
settings_menu = tk.Menu(tearoff=0)
language_menu = tk.Menu(tearoff=0)
plugins_menu = tk.Menu(tearoff=0)
provider_menu = tk.Menu(tearoff=0)
ycm_menu = tk.Menu(tearoff=0)

# Menu principal
menubar.add_cascade(label=data_language["head_menu"]["file_menu"]["title"], menu=file_menu)
menubar.add_cascade(label=data_language["head_menu"]["ycm_menu"]["title"], menu=ycm_menu)
menubar.add_cascade(label=data_language["head_menu"]["plugins_menu"]["title"], menu=plugins_menu)
menubar.add_cascade(label=data_language["head_menu"]["help_menu"]["title"], menu=help_menu)
# Menu Fichier
file_menu.add_command(label=data_language["head_menu"]["file_menu"]["1"], command=download_cheats)
file_menu.add_command(label=data_language["head_menu"]["file_menu"]["2"], command=open_cheat_manager1)
file_menu.add_command(label=data_language["head_menu"]["file_menu"]["5"], command=lambda: os.startfile(f"{settings['yuzu_folder']}\\load\\{games_list[cb1.get()]}\\"))
file_menu.add_cascade(label=data_language["head_menu"]["settings_menu"]["title"], menu=settings_menu)
file_menu.add_separator()
file_menu.add_command(label=data_language["head_menu"]["file_menu"]["4"], command=sys.exit)
# Menu des paramètres
settings_menu.add_checkbutton(label=data_language["head_menu"]["settings_menu"]["1"], variable=verify_updates, command=apply_settings)
settings_menu.add_checkbutton(label=data_language["head_menu"]["settings_menu"]["2"], variable=notify_incompatible_games, command=apply_settings)
settings_menu.add_command(label=data_language["head_menu"]["settings_menu"]["3"], command=change_yuzu_folder)
settings_menu.add_cascade(label=data_language["head_menu"]["language_menu"]["title"], menu=language_menu)
settings_menu.add_checkbutton(label=data_language["head_menu"]["settings_menu"]["4"], variable=discord_rpc, command=apply_settings)
settings_menu.add_checkbutton(label="Developper Mode", variable=dev_mode, command=apply_settings)
settings_menu.add_cascade(label=data_language["head_menu"]["settings_menu"]["6"], menu=provider_menu)
# Menu de séléction des langues
language_menu.add_radiobutton(label="Français", variable=toggle_language, command=apply_settings, value=1)
language_menu.add_radiobutton(label="English", variable=toggle_language, command=apply_settings, value=2)
# Menu plugins
for plugin in plugins.keys():
    plugins_menu.add_command(label=f"{plugin} | {plugins[plugin]['version']} | {plugins[plugin]['developper']}")
plugins_menu.add_separator()
plugins_menu.add_command(label=data_language["head_menu"]["plugins_menu"]["1"], command=lambda: web.open("https://www.yuzucheatsmanager.tk/plugins.html#"))
# Menu YuzuCheatsManager
ycm_menu.add_command(label=data_language["head_menu"]["ycm_menu"]["1"], command=update_ycm)
ycm_menu.add_command(label=data_language["head_menu"]["ycm_menu"]["3"], state="disabled")
# Menu Aide
help_menu.add_command(label=data_language["head_menu"]["help_menu"]["2"], command=lambda: web.open("https://discord.gg/KvjkS3P3Gh"))
help_menu.add_command(label=data_language["head_menu"]["help_menu"]["3"], command=lambda: web.open('https://docs.yuzucheatsmanager.tk'))
# Menu fournisseur
for server in servers:
    provider_menu.add_radiobutton(label=f"{server} | {servers[server]}", variable=toggle_provider, value=list(servers.keys()).index(server)+1, command=apply_settings)
provider_menu.add_separator()
provider_menu.add_command(label="Liste des serveurs publiques disponible sur notre site internet. Il", state="disabled")
provider_menu.add_command(label="est probable que si vous utilisez des dépôts autres que sur Github votre", state="disabled")
provider_menu.add_command(label="IP soit partagée, soyez prudent. Nous ne sommes pas responsables en cas", state="disabled")
provider_menu.add_command(label="de problème.", state="disabled")

# Supression des espaces dans la liste games
for i in range(len(games)):
    if '' in games:
        games.remove('')

games.sort()

ttk.Label(
    window,
    text=" ",
    font=("Calibri", 8)
).pack()

ttk.Label(
    window,
    image=img_home
).pack()

ttk.Label(
    window,
    text=" ",
    font=("Calibri", 5)
).pack()

ttk.Label(
    window,
    text=data_language["texts"]["1"],
    font=("Calibri", 15)
).pack()

cb1 = ttk.Combobox(
    window,
    values=games,
    state="readonly",
    width=45,
    cursor="hand2"
)
cb1.pack()

bouton1 = ttk.Button(
    window,
    text=data_language["buttons"]["1"],
    cursor="hand2",
    command=download_cheats
)
bouton1.place(x=50, y=200)

bouton2 = ttk.Button(
    window,
    text=data_language["buttons"]["2"],
    cursor="hand2",
    command=open_cheat_manager1
)
bouton2.place(x=180, y=200)

tk.Button(
    window,
    image=img_discord,
    highlightthickness=0,
    bd=0,
    cursor="hand2",
    command=lambda: web.open('https://discord.gg/SGHtzYbvRx')
).place(x=10, y=245)

tk.Button(
    window,
    image=img_github,
    highlightthickness=0,
    bd=0,
    cursor="hand2",
    command=lambda: web.open('https://github.com/Luckyluka17/YuzuCheatsManager')
).place(x=50, y=245)

if dev_mode.get():
    ttk.Label(
        window,
        text=f"[Dev mode] Temps de génération de la GUI : {round(time.time()-start_time, ndigits=2)}s | Version {version} (latest : {data_app['latest-version']})",
        font=("Calibri", 8)
    ).place(x=5, y=240)

# Vérifier si un jeu est invalide ou non
if '' in games_list.keys() and settings['notify_incompatible_games'] == True:
    showwarning("Attention", data_language["messages"]["warning_messages"]["2"])

window.config(menu=menubar)
launch_window.destroy()
window.deiconify()
window.eval('tk::PlaceWindow . center')
window.mainloop()