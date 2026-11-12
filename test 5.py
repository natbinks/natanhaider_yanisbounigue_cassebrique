import tkinter as tk
import random

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
        
        self.id = self.canvas.create_rectangle(x1, y1, x1 + largeur, y1 + hauteur, fill=couleur, outline="grey")

    def recevoir_coup(self):
        #enlève 1 point de vie à la brique touchée par la balle les bleues ont 2 pv et les blanches 1 pv
        self.vies -= 1
        if self.vies <= 0:
            self.canvas.delete(self.id)
            return True
        else:
            self.canvas.itemconfig(self.id, fill="white") # Devient blanche après un coup
            return False

class Raquette:
    def __init__(self, canvas, fenetre_largeur, fenetre_longueur):
        self.canvas = canvas
        self.largeur_raquette = 120
        self.hauteur_raquette = 15
        self.vitesse = 30
        self.fenetre_largeur = fenetre_largeur
        self.y_init = fenetre_longueur - 40
        
        # Création initiale
        self.id = self.canvas.create_rectangle(0, 0, 0, 0, fill='cyan')
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
        self.id = self.canvas.create_oval(0, 0, 0, 0, outline='red', fill='red')

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
        self.root.title('Casse Brique')
        self.root.geometry('900x750+300+100')
        self.root.config(bg='grey')

        self.historique_menus = Pile()
        self.journal_evenements = File()
        self.liste_briques = [] 

        self.jeu_en_cours = False
        self.score_actuel = 0
        self.vies = 3
        self.niveau_difficulte = "Normal"

        self.creer_interface()
        self.afficher_menu(self.menu_principal)

    def creer_interface(self):
        #menu Principal
        self.menu_principal = tk.Frame(self.root, bg='grey')
        tk.Label(self.menu_principal, text="CASSE BRIQUE", font=("Arial", 35, "bold"), bg='grey').pack(pady=60)
        self.label_difficulte = tk.Label(self.menu_principal, text="Difficulté : Normal", bg='grey', font=("Arial", 14))
        self.label_difficulte.pack(pady=10)
        tk.Button(self.menu_principal, text="Lancer la partie", command=self.lancer_jeu, width=25, height=2).pack(pady=10)
        tk.Button(self.menu_principal, text="Choisir la difficulté", command=lambda: self.afficher_menu(self.menu_difficulte), width=25, height=2).pack(pady=10)
        tk.Button(self.menu_principal, text="Quitter le jeu", command=self.root.destroy, width=25, height=2, fg="red").pack(pady=10)

        #menu Difficulté
        self.menu_difficulte = tk.Frame(self.root, bg='grey')
        tk.Label(self.menu_difficulte, text="CHOISIR LA VITESSE", font=("Arial", 25, "bold"), bg='grey').pack(pady=60)
        tk.Button(self.menu_difficulte, text="Lent", command=lambda: self.choisir_difficulte("Lent", 3, -3), width=20, height=2).pack(pady=10)
        tk.Button(self.menu_difficulte, text="Normal", command=lambda: self.choisir_difficulte("Normal", 5, -5), width=20, height=2).pack(pady=10)
        tk.Button(self.menu_difficulte, text="Rapide", command=lambda: self.choisir_difficulte("Rapide", 8, -8), width=20, height=2).pack(pady=10)
        tk.Button(self.menu_difficulte, text="Retour", command=self.retour_menu, width=20, height=2).pack(pady=40)

        #écran de Jeu
        self.ecran_jeu = tk.Frame(self.root, bg='grey')
        barre_info = tk.Frame(self.ecran_jeu, bg='grey')
        barre_info.pack(fill='x', padx=50, pady=10)
        
        self.label_vies = tk.Label(barre_info, text=f'Vies : {self.vies}', fg='gold', bg='grey', font=("Arial", 14, "bold"))
        self.label_vies.pack(side='left', padx=20)
        
        self.label_score = tk.Label(barre_info, text='Score : 0', fg='purple', bg='grey', font=("Arial", 14, "bold"))
        self.label_score.pack(side='left')

        tk.Button(barre_info, text="ABANDONNER", fg='red', font=("Arial", 10, "bold"), command=self.abandonner).pack(side='right')

        self.largeur_canevas = 800
        self.longueur_canevas = 650
        self.canvas = tk.Canvas(self.ecran_jeu, width=self.largeur_canevas, height=self.longueur_canevas, bg='black')
        self.canvas.pack(pady=10)

        #création de la balle et de la raquette
        self.raquette = Raquette(self.canvas, self.largeur_canevas, self.longueur_canevas)
        self.balle = Balle(self.canvas, self.raquette, self.largeur_canevas, self.longueur_canevas)

        # Binds
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
        self.actualiser_interface()
        
        for b in self.liste_briques:
            self.canvas.delete(b.id)
        self.liste_briques.clear()
        
        self.generer_briques()
        self.reinitialiser_manche()

    def reinitialiser_manche(self):
        self.canvas.delete("texte_info")
        self.raquette.reinitialiser_position()
        self.balle.reinitialiser_position()
        self.canvas.create_text(self.largeur_canevas/2, self.longueur_canevas/2 + 50, text="Appuyez sur ESPACE pour lancer", fill="white", font=("Arial", 16), tags="texte_info")

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

    def actualiser_interface(self):
        self.label_score.config(text=f"Score : {self.score_actuel}")
        self.label_vies.config(text=f"Vies : {self.vies}")

    #déplacement et actions du joueur
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

    #boucle principale du jeu
    def boucle_jeu(self):
        if not self.jeu_en_cours or not self.balle.en_mouvement: return
        
        etat_balle = self.balle.deplacer()
        
        if etat_balle == "PERDU":
            self.vies -= 1
            self.actualiser_interface()
            self.journal_evenements.enfiler("Vie perdue")
            if self.vies <= 0:
                self.canvas.create_text(self.largeur_canevas/2, self.longueur_canevas/2, text="GAME OVER", fill="red", font=("Arial", 50, "bold"), tags="texte_info")
                self.jeu_en_cours = False
            else:
                self.reinitialiser_manche()
            return 
            
        coords_b = self.balle.get_coords()
        coords_r = self.raquette.get_coords()
        
        #collision raquette
        if coords_b[3] >= coords_r[1] and coords_b[3] <= coords_r[3] and coords_b[2] >= coords_r[0] and coords_b[0] <= coords_r[2]:
            self.balle.forcer_monter()
            
        #collision briques
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
                    
                self.actualiser_interface()
                
                if len(self.liste_briques) == 0:
                    self.canvas.create_text(self.largeur_canevas/2, self.longueur_canevas/2, text="VICTOIRE !", fill="green", font=("Arial", 50, "bold"), tags="texte_info")
                    self.jeu_en_cours = False
                    self.balle.en_mouvement = False
                break 
                
        self.root.after(30, self.boucle_jeu)

if __name__ == "__main__":
    fenetre = tk.Tk()
    app = JeuCasseBrique(fenetre)
    fenetre.mainloop()