#TEASER - FMU pipeline
##annotations pre simulation:
1. nel nuovo template bisognerebbe ricopiare una a una le annotazioni dei componenti dal pacchetto così che quando si carica su OMEdit non vcenga brutto e tutto sbalòlato
2. ridefinire i template e i modelli modelica in modo che input e output e parametri 
   1. rifare il modello in modelica per bene
   2. rifare il package per heater cooler per bene
   3. rifare template per TEASER
3. siano ordinati e ci sia uno standard fisso per il passaggio datoi tra un modello e i suoi sottomodelli
4. **PROBLEMA** create_fmu() ---> Modelica2Fmu() salva le fmu nella cartella in cui si trova, difficile da integrare in PrjArchetypes(class) 
5. estrarre la possibilità di simulare la fmu con gli input da file come quando simulo in modelica per test STAND ALONE
   1. **Risolto**: nel template per teaser ho cambiato da **ln 24-35 .Input in .File**
   2. in particular line 26 .File inplace of .Input_HDirNor_HDifHor
6. 
##annotations FMU simulation:
1. model_description sembra non contenere gli input gia separati per creare un record, invece gli output si
2. trovare un modo per facilmente retrivare gli inputs
#Folder Structure
   
