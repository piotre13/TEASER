# FMU SPECIFICS

## BuildingRC.fmu
This FMU simulate the thermal behaviour of a Two element house extracted from teaser Tabula archetypes.
It only computes the thermal evolution of the envelope.

    - inputs:
        - Atmos_Pressure
        - Ceiling_Hgt
        - DewPoint
        - DifHorzRad
        - DirNormRad
        - DryBulb
        - HorzIRSky
        - RelHum
        - TotSkyCvr
        - WindDir
        - WindSpd
        - extWallIndoorSurface_in
        - fluPor[1].forward.T  
        - fluPor[2].forward.T
        - fluPor[1].m_flow
        - fluPor[2].m_flow
        - heatCoolRoom_in
        - intWallIndoorSurface_in
        - machinesConv_in
        - personConv_in
        - personRad_in
        - windowIndoorSurface_in
    
    - outputs:
        - Tair_ou
        - fluPor[1].backward.T
        - fluPor[2].backward.T
        - heatCoolRoom_ou

## PI_TempController.fmu
This FMU act as a PID controller on the indor temperature set point. It is able to estimate the thermal load needed (given the thermal condition of the house) to achieve a specific temperature set-point.
    
    - inputs:
        - heatCoolRoom_in
        - setPoint
        - onOff

    - outputs:
        - LoadThermal_ou      