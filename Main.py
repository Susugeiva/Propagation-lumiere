"""Indexation:
    
    v[a,b,c]: a:[0, tot_trajec]; Point considéré
              b:{0,1}; vecteur position ou dérivée du vecteur position
              c: {0,1}; Coordonnée du vecteur considéré"""



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d


from Indice import n_grad, n_interface, n_prisme, n_amas
from Résolution_equation_mouvement import dérivée, RK4, dérivée_3D, RK4_3D
from Prisme import prisme
from Modèles import propagation_grad, propagation_interface, propagation_prisme, faisceau_prisme


#Conversion en unité SI:
al = 9.461e15 #m
m_S = 1.988e30 #kg

paramètres = {"Pas d'intégration": 1e2*al,             #en km
              "Longueur du trajet": 10e5*al,               #abscisse curviligne, en km
              "Position initiale": [0,0.5],              #coordonnées du point de départ du rayon
              "Angle initial": np.pi/15,              #angle avec l'horizontale, en rad
              "Fonction dérivée": dérivée_3D,             #fonction utilisée pour le calcul de dérivée
              "Calcul d'indice": n_amas,               #fonction utilisée pour le calcul de l'indice
              "Pas de calcul du gradient": 0.1,
              "Indice 1 gradient": 2,
              "Indice 2 gradient": 1,
              "Hauteur du gradient": 100,
              "Indice 1 interface": 1,
              "Indice 2 interface": 2,
              "Position dioptre": 150,
              "Indice en dehors du prisme": 1.5,
              "Lambda": 634,
              "Nombre lambda": 20,          #nm
              "Prisme": (2,8,6),        #Géométrie du prisme (x1, x2, y3), prisme de base x1x2 au sol, de hauteur y3
              "Verre": (1.72, 29.3),    #propriétés du verre; tuple : (nD, Nombre d'Abbe)  
              "Vitesse lumière": 3e8,   #m/s
              "Constante G": 6.67e-11,  #m^3.kg^-1.s^-2    
              "Masse amas": 1e14*m_S,   #kg 
              "Concentration": 10,      #plus il est grand, plus la masse est concentrée au centre
              "R": 5e6*al,
              "Position centre galaxie": [0, 0, -8e5*al],   #toujours fixé --> position initiale
              "Position centre amas": [0, 0, -8e5*al/2],    #peut être modifié mais dois toujours être le centre de la galaxie et l'observateur 
              "Angle initial en 3D": (0,np.pi/746386783)}          #(theta,beta)    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



s,v = RK4_3D(paramètres)

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot3D(v[:,0,0], v[:,0,1], v[:,0,2], 'gray')

xdata, ydata, zdata = paramètres["Position centre galaxie"]
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='cool')

x,y,z = paramètres["Position centre amas"]
ax.scatter3D(x, y, z, c=z, cmap='gnuplot')

ax.scatter3D(0, 0, 0, c=0, cmap='Pastel1')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.view_init(25, 65)
fig

#ax.set_xlim(-1e13, 1e13)
#ax.set_zlim(minmax)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  DICTIONNAIRES OPTIMISÉS SELON LES MODÈLES  ~~~~~~~~~~~~~~~~~~~~~~

opti_interface = {"Pas d'intégration": 0.01,          #en m     
              "Longueur du trajet": 30,               #abscisse curviligne, en m
              "Position initiale": [0,0],             
              "Angle initial": np.pi/5,               
              "Fonction dérivée": dérivée,             
              "Calcul d'indice": n_interface,               
              "Pas de calcul du gradient": 0.01,
              "Indice 1 interface": 1,
              "Indice 2 interface": 1.33,
              "Position dioptre": 5}  

#propagation_interface(opti_interface)  

opti_gradient = {"Pas d'intégration": 1,               #en m
              "Longueur du trajet": 120,               #abscisse curviligne, en m
              "Position initiale": [0,0],              
              "Angle initial": np.pi/8,                
              "Fonction dérivée": dérivée,             
              "Calcul d'indice": n_grad,               
              "Pas de calcul du gradient": 0.1,
              "Indice 1 gradient": 2,
              "Indice 2 gradient": 1,
              "Hauteur du gradient": 100}

#propagation_grad(opti_gradient)       
  

opti_prisme = {"Pas d'intégration": 0.01,               #en m
              "Longueur du trajet": 15,                #abscisse curviligne, en m
              "Position initiale": [0,0],              
              "Angle initial": np.pi/9,              
              "Fonction dérivée": dérivée,             
              "Calcul d'indice": n_prisme,               
              "Pas de calcul du gradient": 0.1,
              "Indice en dehors du prisme": 1.33,
              "Lambda": 537,                           
              "Prisme": (3,9,6),   
              "Verre": (1.72, 29.3)}

#propagation_prisme(opti_prisme)


opti_faisceau = {"Pas d'intégration": 0.01,               
              "Longueur du trajet": 20,               
              "Position initiale": [0,0.5],              
              "Angle initial": np.pi/15,              
              "Fonction dérivée": dérivée,             
              "Calcul d'indice": n_prisme,               
              "Pas de calcul du gradient": 0.1,
              "Indice en dehors du prisme": 1.5,
              "Nombre lambda": 35,                         
              "Prisme": (2,8,6),           
              "Verre": (1.72, 29.3)}       

#faisceau_prisme(opti_faisceau)

