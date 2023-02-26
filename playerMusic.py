from tkinter import*  # importer les modules nécessaires
from pygame import mixer
import pygame.mixer
from tkinter import Listbox, filedialog
from PIL import Image, ImageTk
from tkinter import simpledialog 
import os, sys
import tkinter.ttk as ttk
import time
from mutagen.mp3 import MP3

WHITE = "#FFFFFF"
BLACK = "#000000"

  
root = Tk()
root.title("playerMusic")
root.configure(background=BLACK)
root.resizable(width=False, height=False )
root.geometry("500x450")

frame=Frame(root)
frame.pack(side=TOP, fill=X)

mixer.init()

# charger l'image
image_son = Image.open("images/img.jpg")


# redimensionner l'image à une taille de 480x300
image_son = image_son.resize((480, 300), Image.ANTIALIAS)

# créer un objet PhotoImage à partir de l'image redimensionnée
photo = ImageTk.PhotoImage(image_son)

# créer un label et lui assigner l'image
label_image = Label(frame, image=photo)
label_image.pack(side=LEFT)




# spécifier le dossier contenant les fichiers de musique
MusicFolder = f"musique/"

# lister tous les fichiers de musique dans le dossier spécifié
play_music= os.listdir('musique')
ACTIVE = 0


# sélectionner la musique active à jouer
song=play_music[ACTIVE]

# charger la musique sélectionnée en tant qu'objet MP3
song_mut = MP3(MusicFolder+song)

# obtenir la durée de la musique
music_length = song_mut.info.length


#Définition de la fonction qui ajuste le volume du lecteur de musique
def set_volume(x):
    mixer.music.set_volume(slide_song.get()/100)
    volume = mixer.music.get_volume()
    slide_label.config(text= volume)
    

#Définition de la fonction qui charge et joue la musique à partir de l'emplacement actif de la barre de lecture  
def bar(x): 
    song=play_music[ACTIVE]
    mixer.music.load(MusicFolder+song)
    mixer.music.play(loops=0, start=int(slide_bar.get()))
    slide_bar_label.config(text=f'{int(slide_bar.get())}')
      

#Création de la barre de volume verticale
slide_song = ttk.Scale(frame, from_=0, to=100, orient=VERTICAL, value=0, length=100, command=set_volume)    
slide_song.pack(side=RIGHT, fill=X)


#Affichage de la valeur actuelle du volume dans une étiquette
slide_label = Label(frame, text="0")
slide_label.pack(side=RIGHT, fill=X)

#Création de la barre de lecture horizontale pour la musique
frame_button = Frame(root, bg='oldlace')
frame_button.pack(side=BOTTOM, fill=X)

slide_bar =ttk.Scale(frame_button, from_=0, to=music_length, orient=HORIZONTAL, value=0, length=360, command=bar)
slide_bar.grid(row=1, column=0, columnspan=5, padx=5, pady=5)


#Affichage de la valeur actuelle de la barre de lecture dans une étiquette
slide_bar_label = Label(frame_button, text="0")
slide_bar_label.grid(row=2, column=0, columnspan=5, padx=7, pady=7)


#Affichage de la durée totale de la musique dans une étiquette
durée = Label(frame_button, text=" ", bd=1, relief=GROOVE, anchor=E)
durée.grid(row=2, column=3, columnspan=5, padx=5, pady=5)


    


# Fonction pour passer à la chanson suivante
def next_song():
    global ACTIVE
    # On incrémente ACTIVE pour passer à la chanson suivante
    ACTIVE += 1
    song = play_music[ACTIVE]
    
    # On charge la nouvelle chanson    
    mixer.music.load(MusicFolder+song)
    # On la joue en boucle (loops=0 signifie qu'on ne la joue qu'une fois)
    mixer.music.play(loops=0) 
    song_mut = MP3(MusicFolder+song) 
    
    # On récupère la durée de la chanson en secondes
    music_length = song_mut.info.length  
    
    # On configure la barre de progression pour qu'elle affiche la durée totale de la chanson
    slide_bar.config(to=music_length, value=0)
   
# Fonction pour passer à la chanson précédente   
def previous_song():
    global ACTIVE
    
    ACTIVE -= 1
    song = play_music[ACTIVE]
    
    mixer.music.load(MusicFolder+song)
    mixer.music.play(loops=0) 
    
    # On réinitialise la barre de progression
    reset_slider()
    
# Fonction pour arrêter la lecture de la chanson en cours    
def stop(): 
    mixer.music.stop()
    durée.config(text=" ")
    slide_bar.config(value=0)
    

# Variable globale indiquant si la lecture est en pause ou non    
global paused
paused = False

# Fonction pour mettre la lecture en pause ou reprendre la lecture
def pause(this_paused):
    global paused
    paused = this_paused
    if paused:
        
        # Si la lecture est en pause, on la reprend
        mixer.music.unpause()
        paused = False
        
    else:
        # Si la lecture n'est pas en pause, on la met en pause
        mixer.music.pause()
        paused = True

# Fonction pour démarrer la lecture de la chanson en cours
def play(): 
   
    song=play_music[ACTIVE]
    mixer.music.load(MusicFolder+song)
    mixer.music.play(loops=0)
    
    duration_song()
    
    # On configure le bouton play pour qu'il mette la lecture en pause lorsqu'on clique dessus
    playe_btn.config(command=lambda: (mixer.music.unpause(), reset_slider())) 
   
    

# Fonction pour réinitialiser la barre de progression
def reset_slider():
    slide_bar.set(0)


# Fonction pour afficher la durée de la chanson et mettre à jour la barre de progression
def duration_song():
    global ACTIVE, long, temps, convert_time, convert_long
  
    temps = (mixer.music.get_pos()/1000)
    #slide_bar_label.config(text=f"Slider:{int(slide_bar.get()) and int(temps)}%")
    
    
    convert_time = time.strftime('%M:%S', time.gmtime(temps))
    
    song = play_music[ACTIVE] 
    
    mut_song = MP3(MusicFolder+song)
    
    long = mut_song.info.length
    
    convert_long = time.strftime('%M:%S', time.gmtime(long))
     
     
    temps+=1
    if int(slide_bar.get()) == int(long):
        next_song()
    
    
    elif int(slide_bar.get()) == int(temps):
        
        position=int(long)
        slide_bar.config(to=position , value=int(temps))
    
        
    else:
        
        position=int(long)
        slide_bar.config(to=position , value=int(slide_bar.get()))
        convert_time = time.strftime('%M:%S', time.gmtime(int(slide_bar.get())))

        durée.config(text=f'Time:{convert_time} of {convert_long}')
        next_time = int(slide_bar.get()) + 1
        slide_bar.config(value=next_time)
   
    
    durée.after(1000, duration_song)

def add_song():
    select_song = filedialog.askopenfilename(title="Sélectionner une chanson", filetypes=[("Fichiers audio", "*.mp3;*.wav;*.ogg")])
    if select_song:
        play_music.append(select_song)
        print("La chanson", select_song, "a été ajoutée à la liste de lecture.")
    else:
        print("Aucune chanson n'a été sélectionnée.")


def delete_song():
    selected_song = filedialog.askopenfilename(title="Sélectionner une chanson", filetypes=[("Fichiers audio", "*.mp3;*.wav;*.ogg")])
    if selected_song:
        if selected_song in play_music:
        
            play_music.remove(selected_song)
    
   

gauche_btn_img = Image.open('images/backward.png')
gauche_btn_img = gauche_btn_img.resize((50, 50), Image.ANTIALIAS)
gauche_btn_img = ImageTk.PhotoImage(gauche_btn_img)
gauche_btn = Button(frame_button, image=gauche_btn_img, command=previous_song)
gauche_btn.grid(row=0, column=0, padx=(60,10), pady=0)



stop_btn_img=Image.open('images/stop.png')
stop_btn_img = stop_btn_img.resize((50, 50), Image.ANTIALIAS)
stop_btn_img = ImageTk.PhotoImage(stop_btn_img)
stop_btn = Button(frame_button, image=stop_btn_img, command=stop)
stop_btn.grid(row=0, column=1, padx=10, pady=0)



playe_btn_img = Image.open('images/play.png')
playe_btn_img = playe_btn_img.resize((50, 50), Image.ANTIALIAS)
playe_btn_img = ImageTk.PhotoImage(playe_btn_img)
playe_btn = Button(frame_button, image=playe_btn_img, command=play)
playe_btn.grid(row=0, column=2, padx=10, pady=0)


pause_btn_img=Image.open('images/pause.png')
pause_btn_img = pause_btn_img.resize((50, 50), Image.ANTIALIAS)
pause_btn_img = ImageTk.PhotoImage(pause_btn_img)
pause_btn = Button(frame_button, image=pause_btn_img, command=lambda : pause(paused))
pause_btn.grid(row=0, column=3, padx=10, pady=0)



droite_btn_img = Image.open('images/forward.png')
droite_btn_img = droite_btn_img.resize((50, 50), Image.ANTIALIAS)
droite_btn_img = ImageTk.PhotoImage(droite_btn_img)
droite_btn = Button(frame_button, image=droite_btn_img, command=next_song)
droite_btn.grid(row=0, column=4, padx=(10,30), pady=0)


menubar = Menu(root)
root.config(menu=menubar)
filemenu=Menu(menubar, tearoff=0)

menubar.add_cascade(label="fichier", menu=filemenu)
filemenu.add_command(label="add_one_song", command=add_song)
filemenu.add_separator()
filemenu.add_command(label="delete", command=delete_song)



root.mainloop()


