 
within PRJ_test.ResidentialApartmentBlock_2.ResidentialApartmentBlock_2_DataBase;
record ResidentialApartmentBlock_2_SingleDwelling "ResidentialApartmentBlock_2_SingleDwelling"
  extends AixLib.DataBase.ThermalZones.ZoneBaseRecord(
    T_start = 293.15,
    withAirCap = true,
    VAir = 896.0,
    AZone = 280.0,
    hRad = 5.0,
    lat = 0.88645272708792,
    nOrientations = 6,
    AWin = {11.484200000000001, 11.484200000000001, 11.484200000000001, 11.484200000000001, 0.0, 0.0},
    ATransparent = {11.484200000000001, 11.484200000000001, 11.484200000000001, 11.484200000000001, 0.0, 0.0},
    hConWin = 2.7,
    RWin = 0.0035556097362753453,
    gWin = 0.75,
    UWin= 3.001169286735091,
    ratioWinConRad = 0.02,
    AExt = {44.8826, 44.8826, 44.8826, 44.8826, 45.514, 45.514},
    hConExt = 2.3635550772032947,
    nExt = 1,
    RExt = {0.00015084029268367497},
    RExtRem = 0.002919251468311393 ,
    CExt = {81900977.50896597},
    AInt = 1194.6666666666667,
    hConInt = 2.3250000000000006,
    nInt = 1,
    RInt = {5.6107155817611015e-05},
    CInt = {275756919.7710094},
    AFloor = 0.0,
    hConFloor = 0.0,
    nFloor = 1,
    RFloor = {0.00001},
    RFloorRem =  0.00001,
    CFloor = {0.00001},
    ARoof = 0.0,
    hConRoof = 0.0,
    nRoof = 1,
    RRoof = {0.00001},
    RRoofRem = 0.00001,
    CRoof = {0.00001},
    nOrientationsRoof = 1,
    tiltRoof = {0.0},
    aziRoof = {0.0},
    wfRoof = {0.0},
    aRoof = 0.0,
    aExt = 0.5,
    TSoil = 286.15,
    hConWallOut = 19.999999999999996,
    hRadWall = 4.999999999999999,
    hConWinOut = 20.0,
    hConRoofOut = 0.0,
    hRadRoof = 0.0,
    tiltExtWalls = {1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 0.0, 0.0},
    aziExtWalls = {3.141592653589793, 0.0, 1.5707963267948966, -1.5707963267948966, 0.0, 0.0},
    wfWall = {0.1887095555662707, 0.1887095555662707, 0.1887095555662707, 0.1887095555662707, 0.0966428247966491, 0.0},
    wfWin = {0.25, 0.25, 0.25, 0.25, 0.0, 0.0},
    wfGro = 0.14851895293826808,
    specificPeople = 0.02,
    fixedHeatFlowRatePersons = 70,
    internalGainsMoistureNoPeople = 0.5,
    activityDegree = 1.2,
    ratioConvectiveHeatPeople = 0.5,
    internalGainsMachinesSpecific = 2.0,
    ratioConvectiveHeatMachines = 0.75,
    lightingPowerSpecific = 7.0,
    ratioConvectiveHeatLighting = 0.5,
    useConstantACHrate = false,
    baseACH = 0.2,
    maxUserACH = 1.0,
    maxOverheatingACH = {3.0, 2.0},
    maxSummerACH = {1.0, 283.15, 290.15},
    winterReduction = {0.2, 273.15, 283.15},
    maxIrr = {100.0, 100.0, 100.0, 100.0, 9999.9, 9999.9},
    shadingFactor = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0},
    withAHU = false,
    minAHU = 0.3,
    maxAHU = 0.6,
    hHeat = 14001.756894976292,
    lHeat = 0,
    KRHeat = 100,
    TNHeat = 50,
    HeaterOn = true,
    hCool = 0,
    lCool = -14001.756894976292,
    KRCool = 10000,
    TNCool = 1,
    CoolerOn = false,
    withIdealThresholds = false,
    TThresholdHeater = 288.15,
    TThresholdCooler = 295.15);
end ResidentialApartmentBlock_2_SingleDwelling;
