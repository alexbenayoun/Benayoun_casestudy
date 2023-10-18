# -*- coding: utf-8 -*-
import pickle
import json
import numpy as np

def charger_modele(chemin_modele):
    with open(chemin_modele, 'rb') as file:
        modele = pickle.load(file)
    return modele

def traiter_input(chemin_fichier):
    with open(chemin_fichier, 'r') as file:
        data = json.load(file)
    norms=[]
    for entry in data:
        n = entry["norm"]
        norms.append(n)
    return norms

def average(data):      # returns the average of data
    s=0
    if len(data)==0:
        return 0
    for a in data:
        s=s+a
    return s/len(data)

def sigma(data,m):      # returns the standard deviation of data
    s=0
    if len(data)==0:
        return 0
    for a in data:
        s=s+(a-m)*(a-m)
    return np.sqrt(s/len(data))

def dataset(data):
    X=[]
    for norm in data:
        n1=len(norm)        # length of norm
        maxi=max(norm)      # max of norm
        m=average(norm)     # average of norm
        sig=sigma(norm,m)   # std of norm
        m1=average(norm[0:int(n1/3)])             # average of the 1st part of norm
        m2=average(norm[int(n1/3):int(2*n1/3)])   # average of the 2nd part of norm
        m3=average(norm[int(2*n1/3):n1])          # average of the 3rd part of norm
        X.append( [m, maxi, sig, n1, m2-m1, m3-m2] )
    return X

def predict(model1,model2,X):
    ypred=[]
    for x in X:
        Xtest=np.array(x).reshape(1,-1)
        y_pred = model1.predict(Xtest)[0] # prediction of the 1st model
        if y_pred==0:       # prediction = "run"
            ypred.append(6)
        if y_pred==1:       # prediction = "walk"
            ypred.append(7)
        if y_pred==2:       # prediction = others
            y_pred1 = model2.predict(Xtest)[0]    # prediction of the 2nd model
        if y_pred1<6:     # prediction = "dribble", "tackle", "no action", "shot", "pass" or "cross"
            ypred.append(y_pred1)
        if y_pred1==6:    # prediction = "rest"
            ypred.append(8)
    return ypred

def res(pred,norms):
    labels=[]
    for p in pred:
        if p==0:
            labels.append("dribble")
        if p==1:
            labels.append("tackle")
        if p==2:
            labels.append("no action")
        if p==3:
            labels.append("shot")
        if p==4:
            labels.append("pass")
        if p==5:
            labels.append("cross")
        if p==6:
            labels.append("run")
        if p==7:
            labels.append("walk")
        if p==8:
            labels.append("rest")
    return [{"label": label, "norm": norm} for norm, label in zip(norms, labels)]

def main():

    game_nb = int(input("How many games do you want to generate? "))

    for i in range(game_nb):
        chemin_fichier = input(f"Please provide a path to a JSON file for the game{i+1}: ")

        RF1 = charger_modele("modele1.pkl")     # 1st model
        RF2 = charger_modele("modele2.pkl")     # 2nd model
        normes = traiter_input(chemin_fichier)  # Retrieve the norms from the file
        X = dataset(normes)                     # Build a dataset
        predictions=predict(RF1,RF2,X)          # Make predictions
        out=res(predictions,normes)
        print("------------------")
        print("New game:")
        print(out)                              # Print the resulting game
        with open(f"generated_match_{i+1}.json", "w") as outfile:
            json.dump(out, outfile)               # Create a unique JSON file with the output for each game

if __name__ == '__main__':
    main()
