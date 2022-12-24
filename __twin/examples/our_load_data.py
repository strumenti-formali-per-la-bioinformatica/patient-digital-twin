from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy import interpolate
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from pathlib import Path

def our_load_physiology(window_size=1000):

    dir = str(Path('__twin/').parent.absolute())

    #shape(2500,13)
    x_ras = pd.read_csv((str(dir) + '/' + 'DKD_drug-5_glu-6_infection-0_renal-normal.csv'))
    #print(np.shape(x_ras))

    #shape(1808,27), prende le feature dalla colonna 1
    x_cardio = pd.read_csv((str(dir) + '/' + 'CARDIO_drug-0_glu-6_infection-0_renal-normal.csv'), index_col=0)
    #print(np.shape(x_cardio))

    #shape(1808,5), mantiene solo le prime 5 colonne
    x_cardio = x_cardio[['t2', 'Pra', 'Prv', 'Pla', 'Plv']]
    #print(np.shape(x_cardio))

    #shape(2500,11) , elimina per qualche motivo questi 2 valori
    x_ras.drop(['angII_norm', 'IR'], axis=1, inplace=True)
    #print(np.shape(x_ras))

    #tempo relativo a ras, shape(2500,) valori distanziati di 2 milliscondi, si parte da 0 si arriva a 5 secondi
    tx_ras = x_ras["t"]
    #print(tx_ras)

    #tempo relativo a cardio, shape(1808,)
    tx_cardio = x_cardio['t2']
    #print(tx_cardio)

    #300 valori fra 3 e 4.99, scarta i primi 3 secondi di tx_ras per qualche motivo ignoto
    t1 = np.linspace(3, 4.99, 300)
    #300 valori fra 0.8 e 4.6 intervallo che coincide con tx_cardio
    t2 = np.linspace(0.8, 4.6, 300)

    #f sarà l'interpolazione fra il tempo e tutti i valori di una colonna, e questo viene fatto per tutte le colonne considerate
    x_list = []
    for c in list(x_ras.columns) + list(x_cardio.columns):
        if c in x_ras.columns:
                f = interpolate.interp1d(tx_ras, x_ras[c].values)
                x_list.append(f(t1))
        elif c in x_cardio.columns:
                f = interpolate.interp1d(tx_cardio, x_cardio[c].values)
                x_list.append(f(t2))

    #shape(16,300)
    #print(np.shape(x_list[0]))

    #shape(300,16), tramite interpolazione siamo passati da (1808,5) + (2500,11) a (300,16)
    x = np.vstack(x_list).T
    x = x.astype('float32')
    #print(np.shape(x))

    #per qualche motivo concatena 20 volte x trasposto shape(6000,16)
    reps = 20
    x = np.tile(x.T, reps=reps).T
    #print(np.shape(x))

    #6000 valori distanziati di 0.01 partendo da 0 arrivando a 60.11
    t1 = np.arange(0, len(x)) / (np.max(t1) * reps)
    #print(t1[5999])

    #6000 valori distanziati di poco più di 0.01 partendo da 0 arrivando a 65.20
    t2 = np.arange(0, len(x)) / (np.max(t2) * reps)
    #print(t2[5999])

    #sostituisce i valori presenti nella prima colonna con t1 e i valori nella 12 colonna con t2
    x[:, 0] = t1
    x[:, 11] = t2

    scaler = StandardScaler()
    scaler = scaler.fit(x)
    x = scaler.transform(x)

    samples = []
    labels = []
    t_list_1 = []
    t_list_2 = []
    #parte da 0 arriva a 4001
    for batch in range(x.shape[0] - 2 * window_size + 1):
        #print(f"{batch} - {batch + window_size - 2} -> {batch + window_size - 1} - {batch + 2 * window_size - 3}")
        samples.append(x[batch:batch + window_size - 2])
        labels.append(x[batch + window_size - 1:batch + 2 * window_size - 3])
        t_list_1.append(t1[batch + window_size - 1:batch + 2 * window_size - 3])
        t_list_2.append(t2[batch + window_size - 1:batch + 2 * window_size - 3])

    #ogni sample cosi come ogni lable sarà una lista di valori, cioè
    #il primo sample saranno i valori x[0:998] mentre la prima label saranno i valori x[999:1997]
    #il secondo sample saranno i valori x[1:999] mentre la prima label saranno i valori x[1000:1998]
    #l'utlimo sample saranno i valori x[4000:4998] mentre la prima label saranno i valori x[4999:5997]
    #t_list_1 e t_list_2 stesso procedimento ma i valori sono presi da t1 e t2

    #trasformazione liste in numpy array, samples e lables shape(4001,998,16)
    #4001 elmenti da 998 righe e 16 colonne l'uno
    samples = np.array(samples)
    labels = np.array(labels)
    t_list_1 = np.array(t_list_1)
    t_list_2 = np.array(t_list_2)

    x_train, x_test, y_train, y_test = train_test_split(samples, labels, test_size=0.30, random_state=42,shuffle=True)

    #print(np.shape(X_train),np.shape(y_train))
    #print(np.shape(X_test),np.shape(y_test))

    addendum = {
            "RAS": [t_list_1, x_ras.columns],
            "CARDIO": [t_list_2, x_cardio.columns],
        }


    features = list(x_ras.columns) + list(x_cardio.columns)
    #print(features)

    elist = [
            #colonne relative a x_ras lega ognuno con se stesso (crea un nodo???)
            ('t', 't'), ('angI', 'angI'), ('Inhibition', 'Inhibition'),
            ('Renin', 'Renin'),('AGT', 'AGT'), ('angII', 'angII'),
            ('diacid', 'diacid'), ('ang17', 'ang17'), ('at1r', 'at1r'), 
            ('at2r', 'at2r'), ('ACE2', 'ACE2'),

            #colonne relative a x_ras lega il tempo con tutti
            ('t', 'angI'), ('t', 'Inhibition'), ('t', 'Renin'), ('t', 'AGT'),
            ('t', 'angII'), ('t', 'diacid'),('t', 'ang17'), ('t', 'at1r'), 
            ('t', 'at2r'), ('t', 'ACE2'),

            #colonne relative a x_ras legami angI
            ('AGT', 'angI'), ('Renin', 'angI'), ('angI', 'ang17'), ('angI', 'angII'), 

            #colonne relative a x_ras legami angII
            ('diacid', 'angII'),('angII', 'Renin'),('angII', 'ang17'), ('angII', 'at1r'),
            ('angII', 'at2r'),

            #colonne relative a x_ras legami ACE2
            ('ACE2', 'ang17'), ('ACE2', 'angI'),

            #colonne relative a x_cardio lega tempo con tutti
            ('t2', 'Pra'), ('t2', 'Prv'), ('t2', 'Pla'), ('t2', 'Plv'),

            #colonne relative a x_cardio lega tutti 4 valori restanti fra loro
            ('Pra', 'Prv'), ('Pra', 'Pla'), ('Pra', 'Plv'),
            ('Prv', 'Pra'), ('Prv', 'Pla'), ('Pra', 'Plv'),
            ('Pla', 'Pra'), ('Pla', 'Prv'), ('Pla', 'Plv'),
            ('Plv', 'Pra'), ('Plv', 'Prv'), ('Plv', 'Pla'),
        ]


    #64% train shape(2560,998,16)
    #print(np.shape(x_train),np.shape(y_train))
    #16% validation shape(640,998,16)
    #print(np.shape(x_val),np.shape(y_val))
    #20% test shape(801,998,16)
    #print(np.shape(x_test),np.shape(y_test))

    #edge_list creata in base alle combinazioni create i elist
    edge_list = []
    for edge in elist:
        i = features.index(edge[0])
        j = features.index(edge[1])
        edge_list.append((i, j))

    return x_train, y_train, x_test, y_test, edge_list, addendum, scaler