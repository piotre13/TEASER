La cartella contiene gli script di test che ho sviluppato per estrarre i modelli RC (2 elementi per adesso) e convertirti in FMU.
Scusa, i riferimenti e le path bisogna cambiarli perchè non sono universali

in generale per estrarre:
1) test_teaser_backend.py per creare i progetti di teaser ed ottenere i modelli modelica ready-to-export in FMU (c'è un parametro booleano fmu_io per attivare o disattivare), nel __name__ == '__main__' c'è un dict per dire quali edifici estrarre
2) test_omc_backend.py per usare OMPython, importare il modello modelica e convertirlo in FMU

il resto sono alcuni script che sono modifiche della libreria teaser.

altra cosa importante. l'FMU cosi ottenuta ha diversi input meteo da dovergli passare, oltre ai gains ecc. ti consiglio di usare la funzione dump della libreria fmpy per vedere quali sono gli input e output dell'FMU. Se non gli passi tutti i dati meteo, FMU si tiene i valori iniziali.

Altra cosa, in questo momento sono riuscito ad estrarre FMU con un solver base, che dipende fortemente dallo step di integrazione, e quindi per adesso non è possibile utilizzare stepsize superioroi a 300 secondi se non ricordo male. 

Daniele