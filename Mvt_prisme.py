# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:05:52 2021

@author: sugei
"""

import numpy as np

def dérivée_prisme(u_prec, u, s, n, ds, dl, l, n1):
    """ u_prec : coordonnées au pas précédent
        u : coordonnées au pas actuel
        s : abscisse curviligne au pas actuel
        ds : voir step
        n : ici n_prisme
    """
    # u est un tuple (r, dr/ds). /!\ r et dr/dt sont des vecteurs
    
    du = np.empty(np.shape(u))
    
    dn = n(u[0], l, n1) - n(u_prec[0], l, n1)
    
    dn_x = n(u[0], l, n1) - n(u[0] - dl * np.array([1,0]), l, n1) #Problème
    
    dn_y = n(u[0], l, n1) - n(u[0] - dl * np.array([0,1]), l, n1)
    
    
    grad_n = (dn_x/dl) * np.array([1,0]) + (dn_y/dl) * np.array([0,1])
    
    #print("grad_n =", grad_n)
    
    du[0] = u[1]
    du[1] = grad_n - dn/ds * u[1]
    
    return du # une liste , (dr/ds, d^2(r) / ds^2)

def RK4_prisme(tot_trajec, step, v_ini, derive, n, dl, l, n1):
    """ tot_trajec : longueur totale parcourue en abscisse curviligne (float)
        step : pas d'intégration (float)
        v_ini : paramètres initiaux (array 2x2)
        derive : fonction qui traduit l'équa diff
        n : fonction de calcul d'indice
        dl : déplacement infinitasimal (calcul du gradient)
        l : lambda
        n1 : indice du milieu dans lequel se trouve le prisme
    """
    # Création du tableau d'abscisse curviligne
    
    num_points = int(tot_trajec / step) + 1     # nombre d'éléments
    s = np.linspace(0, tot_trajec, num_points) #tableau d'abscisse curviligne, on commence obligatoirement à 0

    # initialisation du tableau v, à 3 dimensions: Pour chaque pas --> deux vecteurs de dimension 2
    v = np.empty((num_points,2,2))
    


    # condition initiale
    v[0] = v_ini 
    v[1] = np.array([v_ini[0] + step * v_ini[1], v_ini[1]])

    # boucle for
    
    for i in range(2,num_points):
        """print("i = ", i)
        
        print("x[i-2] = ", v[i-2,0,0])
        
        print("x[i-1] = ", v[i-1,0,0])
        
        print("dx = ",v[i-1,0,0] - v[i-2, 0, 0])
        """
        
        
        
        #On change la fonction utilisée pour le calcul de dérivée
        
        d1 = derive(v[i-2],v[i-1], s[i-1], n,step, dl, l, n1)
        
        d2 = derive(v[i-2]+ d1 * step/2 , v[i-1] + d1 * step/2, s[i-1] + step/2, n,step, dl, l, n1)
        
        d3 = derive(v[i-2]+ d2 * step/2 , v[i-1] + d2 * step/2, s[i-1] + step/2, n,step, dl, l, n1)
        
        d4 = derive(v[i-2] + d3 * step , v[i-1] + d3 * step, s[i-1] + step, n,step, dl, l, n1)
        
        v[i] = v[i-1] + (d1 + 2 * d2 + 2 * d3 + d4) * step / 6
        
        
   
    # argument de sortie
    return s , v
