import os
import tempfile
import subprocess
import logging
import shutil
import webbrowser
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def select_source_folder():
    folder_selected = filedialog.askdirectory()
    source_entry.delete(0, END)
    source_entry.insert(0, folder_selected)
    logger.info(f"Source folder selected: {folder_selected}")

def select_icon_file():
    file_selected = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    icon_entry.delete(0, END)
    icon_entry.insert(0, file_selected)
    logger.info(f"Icon file selected: {file_selected}")

def select_background_file():
    file_selected = filedialog.askopenfilename(filetypes=[("Image Files", "*.bmp;*.jpg;*.jpeg;*.png")])
    background_entry.delete(0, END)
    background_entry.insert(0, file_selected)
    logger.info(f"Background file selected: {file_selected}")

def create_inno_script(source_folder, output_dir, ico_file, main_script, custom_script, install_dir, background_file):
    return f"""
[Setup]
AppName={os.path.basename(source_folder)}
AppVersion=1.0
DefaultDirName={install_dir}\\{os.path.basename(source_folder)}
DefaultGroupName={os.path.basename(source_folder)}
OutputDir={output_dir}
OutputBaseFilename=setup
SetupIconFile={ico_file}
WizardImageFile={background_file}
WizardSmallImageFile={background_file}

[Files]
Source: "{source_folder}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{{group}}\\{os.path.basename(source_folder)}"; Filename: "{{app}}\\{main_script}"; WorkingDir: "{{app}}"; IconFilename: "{ico_file}"
Name: "{{commondesktop}}\\{os.path.basename(source_folder)}"; Filename: "{{app}}\\{main_script}"; WorkingDir: "{{app}}"; IconFilename: "{ico_file}"

[Run]
; This section is intentionally left empty to remove the "Run..." option
"""

def save_and_convert():
    source_folder = source_entry.get()
    icon_file = icon_entry.get()
    background_file = background_entry.get()
    custom_script = script_text.get(1.0, END).strip() or "--onefile --noconsole"
    install_dir = install_dir_entry.get() or f"C:\\Users\\{os.getlogin()}\\AppData\\Local"

    if not os.path.isdir(source_folder):
        messagebox.showerror("Error", "Invalid source folder")
        logger.error("Invalid source folder selected.")
        return
    
    if not os.path.isfile(icon_file):
        messagebox.showerror("Error", "Invalid icon file")
        logger.error("Invalid icon file selected.")
        return
    
    if not os.path.isfile(background_file):
        messagebox.showerror("Error", "Invalid background file")
        logger.error("Invalid background file selected.")
        return

    try:
        logger.info("Starting installer creation process...")
        with tempfile.TemporaryDirectory() as tmpdirname:
            ico_file_temp = os.path.join(tmpdirname, 'icon.ico')
            img = Image.open(icon_file)
            img.save(ico_file_temp, format='ICO', sizes=[(256, 256)])
            logger.info("Icon file converted to ICO.")

            main_script = next((f for f in os.listdir(source_folder) if f.endswith('.py') and 'main' in f), None)
            if not main_script:
                messagebox.showerror("Error", "No main script found in the source folder")
                logger.error("No main script found in the source folder.")
                return

            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            output_dir = os.path.join(desktop_path, f"{os.path.basename(source_folder)}-Setup")
            os.makedirs(output_dir, exist_ok=True)

            ico_file_output = os.path.join(output_dir, 'icon.ico')
            shutil.copyfile(ico_file_temp, ico_file_output)

            background_temp = os.path.join(tmpdirname, 'background.bmp')
            bg_img = Image.open(background_file)
            bg_img = bg_img.convert('RGB')
            bg_img.save(background_temp, format='BMP')

            inno_script = create_inno_script(source_folder, output_dir, ico_file_output, main_script, custom_script, install_dir, background_temp)
            script_path = os.path.join(tmpdirname, 'installer.iss')
            with open(script_path, 'w') as file:
                file.write(inno_script)
            logger.info("Inno Setup script created.")

            iscc_path = "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
            subprocess.run([iscc_path, script_path], check=True)

            messagebox.showinfo("Success", f"Installer created successfully in {output_dir}")
            logger.info(f"Installer created successfully in {output_dir}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to create installer: {e}")
        logger.error(f"Failed to create installer: {e}")

def clear_script():
    script_text.delete(1.0, END)
    script_text.insert(END, "--onefile --noconsole")

def install_inno():
    webbrowser.open("https://jrsoftware.org/download.php/is.exe?site=1")

# Création de la fenêtre principale Tkinter
fenetre = Tk()
fenetre.geometry('1200x700')
fenetre.title('Convert Python Application to EXE with Inno Setup')
fenetre.configure(bg='#092A3E')

# Configuration de la police
try:
    fenetre.option_add('*Font', 'Copperplate-Gothic-Std-32')
except TclError:
    messagebox.showwarning("Warning", "Copperplate Gothic font not found. Using default font.")

# Création du menu
menu_bar = Menu(fenetre)
dependence_menu = Menu(menu_bar, tearoff=0)
dependence_menu.add_command(label="Install Inno", command=install_inno)
menu_bar.add_cascade(label="Dependence", menu=dependence_menu)
fenetre.config(menu=menu_bar)

# Champ pour le dossier source
source_label = Label(fenetre, text="Source Folder:", fg='white', bg='#092A3E', font=('Copperplate Gothic', 14))
source_label.pack(pady=10)
source_entry = Entry(fenetre, width=100, font=('Copperplate Gothic', 12))
source_entry.pack(pady=5)
source_button = Button(fenetre, text="Browse", command=select_source_folder, font=('Copperplate Gothic', 12))
source_button.pack(pady=5)

# Champ pour le fichier icône
icon_label = Label(fenetre, text="Icon File (.png):", fg='white', bg='#092A3E', font=('Copperplate Gothic', 14))
icon_label.pack(pady=10)
icon_entry = Entry(fenetre, width=100, font=('Copperplate Gothic', 12))
icon_entry.pack(pady=5)
icon_button = Button(fenetre, text="Browse", command=select_icon_file, font=('Copperplate Gothic', 12))
icon_button.pack(pady=5)

# Champ pour le fichier de fond
background_label = Label(fenetre, text="Background File (.bmp, .jpg, .jpeg, .png):", fg='white', bg='#092A3E', font=('Copperplate Gothic', 14))
background_label.pack(pady=10)
background_entry = Entry(fenetre, width=100, font=('Copperplate Gothic', 12))
background_entry.pack(pady=5)
background_button = Button(fenetre, text="Browse", command=select_background_file, font=('Copperplate Gothic', 12))
background_button.pack(pady=5)

# Champ pour le chemin d'installation
install_dir_label = Label(fenetre, text="Installation Directory:", fg='white', bg='#092A3E', font=('Copperplate Gothic', 14))
install_dir_label.pack(pady=10)
install_dir_entry = Entry(fenetre, width=100, font=('Copperplate Gothic', 12))
install_dir_entry.pack(pady=5)
install_dir_entry.insert(0, f"C:\\Users\\{os.getlogin()}\\AppData\\Local")

# Champ pour le script personnalisé
script_label = Label(fenetre, text="Custom Batch Script:", fg='white', bg='#092A3E', font=('Copperplate Gothic', 14))
script_label.pack(pady=10)
script_text = Text(fenetre, width=100, height=10, font=('Courier', 12), wrap=WORD)
script_text.pack(pady=5)
script_text.insert(END, "--onefile --noconsole")

# Boutons de manipulation de script
script_buttons_frame = Frame(fenetre, bg='#092A3E')
script_buttons_frame.pack(pady=10)
save_button = Button(script_buttons_frame, text="Save & Convert", command=save_and_convert, font=('Copperplate Gothic', 14))
save_button.pack(side=LEFT, padx=10)
clear_button = Button(script_buttons_frame, text="Clear Script", command=clear_script, font=('Copperplate Gothic', 14))
clear_button.pack(side=LEFT, padx=10)

# Label créé par
created_by_label = Label(fenetre, text="Created by Soniceurs", fg='white', bg='#092A3E', font=('Copperplate Gothic', 12))
created_by_label.pack(side=BOTTOM, pady=20)

fenetre.mainloop()
