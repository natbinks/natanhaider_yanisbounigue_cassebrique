from tkinter import Tk, Label, Button, StringVar, Canvas

cv = Tk()
nbscore=StringVar()
labelJeu = Label(cv, text = 'score', fg = 'purple')

#labelJeu = Label.config
labelJeu.place(relx=0.95, rely=0)

buttonQuitt = Button (cv, text="QUITTER", fg = 'red', command = cv.destroy)

buttonQuitt.place(relx=0.95, rely=0.95)

#nom fenetre
cv.title('casse brique')

#taille fenetre
cv.geometry('700x500+700+500')

#couleur fond de la fenetre
cv['bg']='grey'

#fond jeu en canva
largeur=625
longueur=450
canvas=Canvas(cv, width=largeur, height=longueur, bg='black')
canvas.pack(padx=0, pady=0)

#centrage du canva selon l'axe y
canvas.pack(pady=25) 

#mise en place et fonctionnement de la raquette
largeur_raquette = 100
hauteur_raquette = 15
vitesse = 30

#position initiale au centre en bas
x_init = (largeur / 2) - (largeur_raquette / 2)
y_init = longueur - 30

#création du rectangle de la raquette
raquette = canvas.create_rectangle(
    x_init, y_init, 
    x_init + largeur_raquette, y_init + hauteur_raquette, 
    fill='cyan'
)

#fonctionnalité de déplacement
def gauche(event):
    #on récupère les coordonnées [x1, y1, x2, y2]
    coords = canvas.coords(raquette)
    #pas dépacer a gauche
    if coords[0] > 0:
        canvas.move(raquette, -vitesse, 0)

def droite(event):
    coords = canvas.coords(raquette)
    #pas dépasser a droite
    if coords[2] < largeur:
        canvas.move(raquette, vitesse, 0)

#lie fleches au canva
cv.bind("<Left>", gauche)
cv.bind("<Right>", droite)

#fait en sorte que le canva reconnaisse touches du clavier
#cv.focus_set()

#def jouer():
rayon = 10
x_balle = largeur / 2
y_balle = longueur / 2

vitesse_x = 5 
vitesse_y = -5 

balle = canvas.create_oval(
    x_balle - rayon, y_balle - rayon, 
    x_balle + rayon, y_balle + rayon, 
    outline='red', fill='red'
)

def deplacer_balle():
    global vitesse_x, vitesse_y
    
    canvas.move(balle, vitesse_x, vitesse_y)
    
    coords_balle = canvas.coords(balle)
    
    if coords_balle[0] <= 0 or coords_balle[2] >= largeur:
        vitesse_x = -vitesse_x 
        
    if coords_balle[1] <= 0:
        vitesse_y = -vitesse_y 
        
    if coords_balle[3] >= longueur:
        vitesse_y = -vitesse_y 
        print("Perdu ! (Mais ça rebondit pour le test)")

    coords_raquette = canvas.coords(raquette)
    
    if coords_balle[3] >= coords_raquette[1] and coords_balle[3] <= coords_raquette[3]:
        if coords_balle[2] >= coords_raquette[0] and coords_balle[0] <= coords_raquette[2]:
            vitesse_y = -abs(vitesse_y)
            
    cv.after(30, deplacer_balle)

deplacer_balle()
#bouton jouer
#boutonjouer = Button(cv, text='Jouer!!!', command=jouer)
#boutonjouer.place(relx=0.5 , rely=0.5)



cv.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os

# ==========================================
# STRUCTURES DE DONNÉES REQUISES
# ==========================================

class Pile:
    #ajout des méthodes dépiler et empiler
    def __init__(self):
        self.elements = []
    def empiler(self, item):
        self.elements.append(item)
    def depiler(self):
        return self.elements.pop() if not self.est_vide() else None
    def est_vide(self):
        return len(self.elements) == 0

class File:
    #ajout des méthodes défiler et enfiler
    def __init__(self):
        self.elements = []
    def enfiler(self, item):
        self.elements.append(item)
    def defiler(self):
        return self.elements.pop(0) if not self.est_vide() else None
    def est_vide(self):
        return len(self.elements) == 0



class Brique:
    
    def __init__(self, canvas, x1, y1, largeur, hauteur, est_bleue):
        self.canvas = canvas
        self.est_bleue = est_bleue
        self.vies = 2 if est_bleue else 1
        couleur = "blue" if est_bleue else "white"
        
        self.id = self.canvas.create_rectangle(x1, y1, x1 + largeur, y1 + hauteur, fill=couleur, outline="grey")#création du canvas

    def recevoir_coup(self):
        #enlève 1 point de vie à la brique touchée par la balle les bleues ont 2 pv et les blanches 1 pv
        self.vies -= 1
        if self.vies <= 0:
            self.canvas.delete(self.id)
            return True
        else:
            self.canvas.itemconfig(self.id, fill="white") #devient blanche après un coup
            return False

class Raquette:
    
    def __init__(self, canvas, fenetre_largeur, fenetre_longueur):
        self.canvas = canvas
        self.largeur_raquette = 120
        self.hauteur_raquette = 15
        self.vitesse = 30
        self.fenetre_largeur = fenetre_largeur
        self.y_init = fenetre_longueur - 40
        
        
        self.id = self.canvas.create_rectangle(0, 0, 0, 0, fill='cyan')#création du canvas
        self.reinitialiser_position()

    def reinitialiser_position(self):
        #mettre la raquette au milieu dès qu'on lance la partie
        x_init = (self.fenetre_largeur / 2) - (self.largeur_raquette / 2)
        self.canvas.coords(self.id, x_init, self.y_init, x_init + self.largeur_raquette, self.y_init + self.hauteur_raquette)

    def deplacer_gauche(self):
        if self.canvas.coords(self.id)[0] > 0:
            self.canvas.move(self.id, -self.vitesse, 0)

    def deplacer_droite(self):
        if self.canvas.coords(self.id)[2] < self.fenetre_largeur:
            self.canvas.move(self.id, self.vitesse, 0)

    def get_coords(self):
        #get pour obtenir les coordonnées de la raquette
        return self.canvas.coords(self.id)

class Balle:
   
    def __init__(self, canvas, raquette, fenetre_largeur, fenetre_longueur):
        self.canvas = canvas
        self.raquette = raquette
        self.rayon = 10
        self.fenetre_largeur = fenetre_largeur
        self.fenetre_longueur = fenetre_longueur
        
        self.vitesse_x_ref = 5
        self.vitesse_y_ref = -5
        self.vitesse_x = self.vitesse_x_ref
        self.vitesse_y = self.vitesse_y_ref
        
        self.en_mouvement = False
        self.id = self.canvas.create_oval(0, 0, 0, 0, outline='red', fill='red')#création du canvas 

    def definir_vitesse(self, vx, vy):
        self.vitesse_x_ref = vx
        self.vitesse_y_ref = vy

    def reinitialiser_position(self):
        self.en_mouvement = False
        coords_r = self.raquette.get_coords()
        centre_rx = (coords_r[0] + coords_r[2]) / 2
        y_raquette = coords_r[1]
        
        self.canvas.coords(self.id, centre_rx - self.rayon, y_raquette - (self.rayon * 2), centre_rx + self.rayon, y_raquette)
        self.vitesse_x = self.vitesse_x_ref
        self.vitesse_y = self.vitesse_y_ref

    def suivre_raquette(self, direction):
        #suit la raquette avant le début de la partie et avant l'appui de la touche espace
        if not self.en_mouvement:
            if direction == "gauche" and self.raquette.get_coords()[0] > 0:
                self.canvas.move(self.id, -self.raquette.vitesse, 0)
            elif direction == "droite" and self.raquette.get_coords()[2] < self.fenetre_largeur:
                self.canvas.move(self.id, self.raquette.vitesse, 0)

    def lancer(self):
        #permet de récupérer l'information que la balle est en mouvement
        self.en_mouvement = True

    def deplacer(self):
        if not self.en_mouvement: return "ARRET"
        
        self.canvas.move(self.id, self.vitesse_x, self.vitesse_y)
        coords = self.canvas.coords(self.id)
        
        #rebondi sur les murs
        if coords[0] <= 0 or coords[2] >= self.fenetre_largeur:
            self.vitesse_x = -self.vitesse_x 
        if coords[1] <= 0:
            self.vitesse_y = -self.vitesse_y 
            
        #quand la balle touche le sol
        if coords[3] >= self.fenetre_longueur:
            return "PERDU"
            
        return "OK"

    def inverser_y(self):
        #c'est le rebond sur la raquette
        self.vitesse_y = -self.vitesse_y
        
    def forcer_monter(self):
        #permet d'éviter les bugs de rebond
        self.vitesse_y = -abs(self.vitesse_y)

    def get_coords(self):
        return self.canvas.coords(self.id)


#classe permettant de gérer le jeu
class JeuCasseBrique:
    def __init__(self, root):
        #initialisation de la fenêtre de jeu
        self.root = root
        self.root.title("Casse Brique")
        self.root.geometry("900x750+300+100")
        self.couleur_fond = "#f0f2f5"
        self.root.config(bg=self.couleur_fond)
        dossier_script = os.path.dirname(os.path.abspath(__file__))
        chemin_menu = os.path.join(dossier_script, "menu_bg.png")
        chemin_jeu = os.path.join(dossier_script, "jeu_bg.png")

        try:
            self.img_menu = tk.PhotoImage(file=chemin_menu)
            self.img_jeu = tk.PhotoImage(file=chemin_jeu)
        except Exception as e:
            messagebox.showwarning("Problème d'image",f"Impossible de charger l'image.\n\nDétail de l'erreur :\n{e}",
    )
        self.img_menu = None
        self.img_jeu = None

        self.historique_menus = Pile()
        self.journal_evenements = File()
        self.liste_briques = []

        self.jeu_en_cours = False
        self.score_actuel = 0
        self.vies = 3
        self.niveau_difficulte = "Normal"

        self.style_boutons()
        self.creer_interface()
        self.afficher_menu(self.menu_principal)
    
    def style_boutons(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        #style des boutons du menu
        style.configure(
            "Modern.TButton",
            font=("Helvetica", 11, "bold"),
            background="#1877f2",
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            padding=(15, 10)
        )
        style.map("Modern.TButton", background=[("active", "#166fe5"), ("pressed", "#1464cc")])

        #style du bouton quitter
        style.configure(
            "Quitter.TButton",
            font=("Helvetica", 11, "bold"),
            background="#dc3545",
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            padding=(15, 10)
        )
        style.map("Quitter.TButton", background=[("active", "#c82333"), ("pressed", "#bd2130")])

    def creer_interface(self):
        #menu principale
        self.menu_principal = tk.Frame(self.root, bg=self.couleur_fond)
        
        #fond du menu principal
        if self.img_menu:
            fond_menu1 = tk.Label(self.menu_principal, image=self.img_menu)
            fond_menu1.place(x=0, y=0, relwidth=1, relheight=1)
            fond_menu1.lower()

        tk.Label(self.menu_principal, text="CASSE BRIQUE", font=("Helvetica", 35, "bold"), fg="#1c1e21", bg=self.couleur_fond).pack(pady=60)
        self.label_difficulte = tk.Label(self.menu_principal, text="Difficulté : Normal", bg=self.couleur_fond, fg="#606770", font=("Helvetica", 14))
        self.label_difficulte.pack(pady=10)
        
        ttk.Button(self.menu_principal, text="Lancer la partie", style="Modern.TButton", width=25, command=self.lancer_jeu).pack(pady=10)
        ttk.Button(self.menu_principal, text="Choisir la difficulté", style="Modern.TButton", width=25, command=lambda: self.afficher_menu(self.menu_difficulte)).pack(pady=10)
        ttk.Button(self.menu_principal, text="Quitter le jeu", style="Quitter.TButton", width=25, command=self.root.destroy).pack(pady=10)

        #menu difficulté
        self.menu_difficulte = tk.Frame(self.root, bg=self.couleur_fond)
        
        #fond du menu difficulté
        if self.img_menu:
            fond_menu2 = tk.Label(self.menu_difficulte, image=self.img_menu)
            fond_menu2.place(x=0, y=0, relwidth=1, relheight=1)
            fond_menu2.lower()

        tk.Label(self.menu_difficulte, text="CHOISIR LA VITESSE", font=("Helvetica", 25, "bold"), fg="#1c1e21", bg=self.couleur_fond).pack(pady=60)
        
        ttk.Button(self.menu_difficulte, text="Lent", style="Modern.TButton", width=20, command=lambda: self.choisir_difficulte("Lent", 3, -3)).pack(pady=10)
        ttk.Button(self.menu_difficulte, text="Normal", style="Modern.TButton", width=20, command=lambda: self.choisir_difficulte("Normal", 5, -5)).pack(pady=10)
        ttk.Button(self.menu_difficulte, text="Rapide", style="Modern.TButton", width=20, command=lambda: self.choisir_difficulte("Rapide", 8, -8)).pack(pady=10)
        ttk.Button(self.menu_difficulte, text="Retour", style="Modern.TButton", width=20, command=self.retour_menu).pack(pady=40)

        # Écran de Jeu
        self.ecran_jeu = tk.Frame(self.root, bg=self.couleur_fond)
        barre_info = tk.Frame(self.ecran_jeu, bg=self.couleur_fond)
        barre_info.pack(fill='x', padx=50, pady=10)
        #ecriture en f-string
        self.label_vies = tk.Label(barre_info, text=f'Vies : {self.vies}', fg='#f5a623', bg=self.couleur_fond, font=("Helvetica", 14, "bold"))
        self.label_vies.pack(side='left', padx=20)
        
        self.label_score = tk.Label(barre_info, text='Score : 0', fg='#1877f2', bg=self.couleur_fond, font=("Helvetica", 14, "bold"))
        self.label_score.pack(side='left')

        ttk.Button(barre_info, text="ABANDONNER", style="Quitter.TButton", command=self.abandonner).pack(side='right')

        self.largeur_canevas = 800
        self.longueur_canevas = 650
        self.canvas = tk.Canvas(self.ecran_jeu, width=self.largeur_canevas, height=self.longueur_canevas, bg='black', highlightthickness=0)
        self.canvas.pack(pady=10)

        #fond du canva dans le jeu
        if self.img_jeu:
            self.canvas.create_image(self.largeur_canevas/2, self.longueur_canevas/2, image=self.img_jeu)

        #creation de la raquette et de la balle
        self.raquette = Raquette(self.canvas, self.largeur_canevas, self.longueur_canevas)
        self.balle = Balle(self.canvas, self.raquette, self.largeur_canevas, self.longueur_canevas)

        #bind des touches
        self.root.bind("<Left>", self.action_gauche)
        self.root.bind("<Right>", self.action_droite)
        self.root.bind("<space>", self.action_espace)

    def afficher_menu(self, menu_cible):
        if hasattr(self, 'menu_actuel') and self.menu_actuel:
            self.menu_actuel.pack_forget()
            self.historique_menus.empiler(self.menu_actuel)
        self.menu_actuel = menu_cible
        self.menu_actuel.pack(fill="both", expand=True)

    def retour_menu(self):
        if not self.historique_menus.est_vide():
            self.menu_actuel.pack_forget()
            self.menu_actuel = self.historique_menus.depiler()
            self.menu_actuel.pack(fill="both", expand=True)

    def choisir_difficulte(self, nom, vx, vy):
        self.balle.definir_vitesse(vx, vy)
        self.niveau_difficulte = nom
        self.label_difficulte.config(text=f"Difficulté : {nom}")
        self.retour_menu()

    def abandonner(self):
        self.jeu_en_cours = False
        self.balle.en_mouvement = False
        self.historique_menus = Pile() 
        self.afficher_menu(self.menu_principal)

    def lancer_jeu(self):
        self.ecran_jeu.pack_forget()
        self.menu_principal.pack_forget()
        self.menu_actuel = self.ecran_jeu
        self.ecran_jeu.pack(fill="both", expand=True)
        self.initialiser_partie()

    def initialiser_partie(self):
        self.score_actuel = 0
        self.vies = 3
        self.jeu_en_cours = True
        self.actualiser_hud()
        
        for b in self.liste_briques:
            self.canvas.delete(b.id)
        self.liste_briques.clear()
        
        self.generer_briques()
        self.reinitialiser_manche()

    def reinitialiser_manche(self):
        self.canvas.delete("texte_info")
        self.raquette.reinitialiser_position()
        self.balle.reinitialiser_position()
        self.canvas.create_text(self.largeur_canevas/2, self.longueur_canevas/2 + 50, text="Appuyez sur ESPACE pour lancer", fill="white", font=("Helvetica", 16), tags="texte_info")

    def generer_briques(self):
        proba_bleue = {"Lent": 0.1, "Normal": 0.3, "Rapide": 0.6}.get(self.niveau_difficulte, 0.3)
        lignes = {"Lent": 3, "Normal": 5, "Rapide": 7}.get(self.niveau_difficulte, 5)
        colonnes, w_brique, h_brique, espace = 10, 70, 25, 5
        
        decalage_x = (self.largeur_canevas - (colonnes * (w_brique + espace))) / 2
        
        for l in range(lignes):
            for c in range(colonnes):
                x1 = decalage_x + c * (w_brique + espace)
                y1 = 50 + l * (h_brique + espace)
                est_bleue = random.random() < proba_bleue
                
                brique = Brique(self.canvas, x1, y1, w_brique, h_brique, est_bleue)
                self.liste_briques.append(brique)

    def actualiser_hud(self):
        self.label_score.config(text=f"Score : {self.score_actuel}")
        self.label_vies.config(text=f"Vies : {self.vies}")

    #action du joueur en jeu
    def action_gauche(self, event):
        self.balle.suivre_raquette("gauche")
        self.raquette.deplacer_gauche()

    def action_droite(self, event):
        self.balle.suivre_raquette("droite")
        self.raquette.deplacer_droite()

    def action_espace(self, event):
        if self.jeu_en_cours and not self.balle.en_mouvement:
            self.canvas.delete("texte_info")
            self.balle.lancer()
            self.boucle_jeu()

    #boucle du jeu permettant de jouer au jeu
    def boucle_jeu(self):
        if not self.jeu_en_cours or not self.balle.en_mouvement: return
        
        etat_balle = self.balle.deplacer()
        
        if etat_balle == "PERDU":
            self.vies -= 1
            self.actualiser_hud()
            self.journal_evenements.enfiler("Vie perdue")
            if self.vies <= 0:
                self.canvas.create_text(self.largeur_canevas/2, self.longueur_canevas/2, text="GAME OVER", fill="#dc3545", font=("Helvetica", 50, "bold"), tags="texte_info")
                self.jeu_en_cours = False
            else:
                self.reinitialiser_manche()
            return 
            
        coords_b = self.balle.get_coords()
        coords_r = self.raquette.get_coords()
        
        #attention colision de la raquette a la balle
        if coords_b[3] >= coords_r[1] and coords_b[3] <= coords_r[3] and coords_b[2] >= coords_r[0] and coords_b[0] <= coords_r[2]:
            self.balle.forcer_monter()
            
        #colision briques et balle
        objets_touches = self.canvas.find_overlapping(*coords_b)
        for obj_id in objets_touches:
            brique_touchee = next((b for b in self.liste_briques if b.id == obj_id), None)
            
            if brique_touchee:
                self.balle.inverser_y()
                detruite = brique_touchee.recevoir_coup()
                
                if detruite:
                    self.liste_briques.remove(brique_touchee)
                    self.score_actuel += 10
                    self.journal_evenements.enfiler("Brique détruite")
                else:
                    self.score_actuel += 5
                    
                self.actualiser_hud()
                
                if len(self.liste_briques) == 0:
                    self.canvas.create_text(self.largeur_canevas/2, self.longueur_canevas/2, text="VICTOIRE !", fill="#28a745", font=("Helvetica", 50, "bold"), tags="texte_info")
                    self.jeu_en_cours = False
                    self.balle.en_mouvement = False
                break 
                
        self.root.after(30, self.boucle_jeu)

#
if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = JeuCasseBrique(fenetre)
    fenetre.mainloop()