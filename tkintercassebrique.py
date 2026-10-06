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

def jouer():
    pass
#bouton jouer
#boutonjouer = Button(cv, text='Jouer!!!', command=jouer)
#boutonjouer.place(relx=0.5 , rely=0.5)



cv.mainloop()