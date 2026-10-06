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
cv.focus_set()

def jouer():
    pass
#bouton jouer
#boutonjouer = Button(cv, text='Jouer!!!', command=jouer)
#boutonjouer.place(relx=0.5 , rely=0.5)



cv.mainloop()