import tkinter as tk
import time as t

### --- VARIABLES GLOBALES --- #
size = 10
matrix = [[0 for _ in range(size+2)]for _ in range(size+2)] #la matrice contenant les cellules
repeat = 1 #permet de boucler quand on appuie sur *start*
fill = [0 for _ in range(size)] #liste des lignes. Chaque 0 correspond à une ligne de <matrix> vide
waitTime = 0.1 #temps d'attente entre 2 nouvelles générations avec la fonction *start*

## --- FONCTIONS --- ##
def change_cell(event):
    """
    create or kill a cell on clic
    """
    global matrix
    global fill
    global size
    clicx= ((event.x)//(600//(size)))
    clicy= ((event.y)//(600//(size)))

    near = can.find_closest(event.x, event.y) #permet de tuer la cellule existant à l'endroit cliqué
    if 'cell' in can.gettags(near):
        can.delete(near)
        matrix[clicy+1][clicx+1] = 0
        fill[clicy] -= 1
    else: #permet de faire naitre une cellule à l'endroit cliqué
        can.create_rectangle(((600//(size))*clicx,(600//(size))*clicy),
                             ((600//(size))*(clicx+1),(600//(size))*(clicy+1)),fill="black", tag='cell')
        matrix[clicy+1][clicx+1] = 1
        fill[clicy] += 1

def change_waitTime(event):
    """
    change waitTime to new entry
    """
    global waitTime
    try: #test si l'entrée est acceptable
        waitTime = float(waitEntry.get())
    except:
        return True


def change_size(event):
    """
    change size to new entry
    """
    global size
    global matrix
    global fill
    matrix2 = matrix.copy()
    try: #test si l'entrée est acceptable
        size2 = int(sizeEntry.get())
    except:
        return True
    
    if size2 > size: #pour un agrandissement de la grille
        for _ in range (size2-size):
            matrix2.append([0 for _ in range(size)])
        for _ in range (size2-size+2):
            for line in range(len(matrix2)):
                matrix2[line].append(0)
        fill += (0 for _ in range(size2-size))
    
    elif size2 < size: #pour un rétrécissement de la grille
        for _ in range(size-size2):
            matrix2.pop()
            fill.pop()
        while len(matrix2[size2+1]) > size2+2:
            for line in range(len(matrix2)):
                matrix2[line].pop()

    else: #pour ne pas changer la grille ? c'est évident nan ?
        return True
    size = size2
    matrix = matrix2.copy()
    trace(size)
    surv_or_birth()


def trace(size): #trace la grille de fond. C'est dans le nom.
    """
    draw a grid of size <size>
    :param size: <int> grid size
    """
    can.delete('fond')
    for line in range(size):
       for column in range(size):
           can.create_rectangle((line*(600//(size)), column*(600//(size))), ((line+1)*(600//(size)), (column+1)*(600//(size))),
                                fill='white', tag = 'fond')


def clear(): #supprime toutes les cellules existantes
    """
    reset the grid and stop the generations
    """
    global matrix
    global fill
    global size
    matrix = [[0 for _ in range(size+2)]for _ in range(size+2)]
    fill = [0 for _ in range(size)]
    can.delete('cell')
    stop()

def start(): #nouvelle génération en boucle, avec un temps d'attente entre chaque de <waitTime>
    """
    start a loop of new generations
    """
    global repeat
    global waitTime
    repeat = 1
    while repeat:
        surv_or_birth()
        can.update()
        t.sleep(waitTime)

def stop(): #permet de stopper le *start*
    """
    stop the loop of new generations
    """
    global repeat
    repeat = 0

def surv_or_birth(): #passe à la génération suivante
    """
    create a new generation of cells
    """
    global matrix
    global size
    global fill
    can.delete('cell')
    matrix2 = [[0 for _ in range(size+2)]for _ in range(size+2)]
    compt = 0
    for line in range (1, size+1):
        if line == 0: #c'est ptet pas opti du tout, mais ca regarde si la ligne doit être traitée. 
            if fill[0] > 0 or fill[1] > 0:
                compt = 1
        elif line == size:
            if fill[size-2] > 0 or fill[size-1] > 0:
                compt = 1
        else:
            if fill[line-2] > 0 or fill[line-1] > 0 or fill[line] > 0:
                compt = 1
        if compt == 1:
            for column in range (1, size+1):
                comptCell = 0 #compte le nombre de cellules vivantes autour de la cellule traitée
                if matrix[line-1][column-1] == 1:
                    comptCell += 1

                if matrix[line-1][column] == 1:
                    comptCell += 1
                
                if matrix[line-1][column+1] == 1:
                    comptCell += 1
                
                if matrix[line][column-1] == 1:
                    comptCell += 1
                
                if matrix[line][column+1] == 1:
                    comptCell += 1
                
                if matrix[line+1][column-1] == 1:
                    comptCell += 1

                if matrix[line+1][column] == 1:
                    comptCell += 1

                if matrix[line+1][column+1] == 1:
                    comptCell += 1

                #créer le cellules, selon les cas de naissance ou de survie.
                if matrix[line][column] == 0:
                    if comptCell == 3:
                        matrix2[line][column] = 1
                        fill[line-1] += 1
                 
                elif matrix[line][column] == 1:
                    if 2<=comptCell<=3:
                        matrix2[line][column] = 1
                    else:
                        fill[line-1] -= 1

                draw(line, column, matrix2)
            compt = 0
    #actualise la matrice à la nouvelle matrice
    matrix = matrix2.copy()
    
def draw(line, column, matrix2): #remplit les cases vivantes sur l'affichage
    """
    draw the cells on the grid
    :param line: <int> line where the cell is
    :param column: <int> column where Cell is
    :param matrix2: <list> list of all cells living or not.
    """
    if matrix2[line][column] == 1:
        can.create_rectangle(((600//(size))*(column-1),(600//(size))*(line-1)),
                             ((600//(size))*(column),(600//(size))*(line)),
                             fill="black", tag='cell')
            
    

## --- FENETRE PRINCIPALE --- ##
fen = tk.Tk()
fen.geometry('700x610')
can = tk.Canvas(fen, width=600, height=600, bg="white")
can.pack(side=tk.LEFT)

trace(size)
can.bind("<Button-1>", change_cell)

startBtn = tk.Button(fen, text='Start', width=12, command=start)
startBtn.place(x = 605, y=50)

stopBtn = tk.Button(fen, text='Stop', width=12, command=stop)
stopBtn.place(x=605,y=90)

nextBtn = tk.Button(fen, text='Next', width=12, command=surv_or_birth)
nextBtn.place(x=605,y=130)

clearBtn = tk.Button(fen, text='Clear',width=12, command=clear)
clearBtn.place(x=605, y=170)

sizeLbl = tk.Label(fen, text="size :")
sizeEntry = tk.Entry(fen)
sizeLbl.place(x=605,y=210)
sizeEntry.place(x=605,y=250, width = 93)
sizeEntry.bind('<Return>',change_size)

waitLbl = tk.Label(fen, text="waitTime :")
waitEntry = tk.Entry(fen)
waitLbl.place(x=605,y=290)
waitEntry.place(x=605,y=320, width = 93)
waitEntry.bind('<Return>',change_waitTime)

quitBtn = tk.Button(fen, text='Quit', width=12, command=fen.destroy)
quitBtn.place(x = 605, y=400)

fen.mainloop()


## --- TEST UNITAIRE --- ##
##inutile ya pas de tests :/
if __name__ == '__main__':
    import doctest
    doctest.testmod()