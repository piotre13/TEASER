 
within Residential_test.ResidentialApartmentBlock_1.ResidentialApartmentBlock_1_Models;
model ResidentialApartmentBlock_1_SingleDwelling
  "This is the simulation model of SingleDwelling within building ResidentialApartmentBlock_1 with traceable ID None"

  extends AixLib.Fluid.FMI.ExportContainers.ThermalZone(
    redeclare final package Medium = Modelica.Media.Air.DryAirNasa,
    nPorts =  2);
  AixLib.Fluid.Sensors.MassFlowRate senMasFlon[nPorts](redeclare final package Medium = Modelica.Media.Air.DryAirNasa) "Mass flow rate sensor to connect thermal adapter with thermal zone."
  annotation (Placement(transformation(extent={{-88,110},{-68,130}})));
  AixLib.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(
    calTSky=AixLib.BoundaryConditions.Types.SkyTemperatureCalculation.TemperaturesAndSkyCover,
    computeWetBulbTemperature=false,
    filNam=Modelica.Utilities.Files.loadResource("modelica://Residential_test/DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"),
    TBlaSkySou = AixLib.BoundaryConditions.Types.DataSource.File,
    HInfHorSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    HSou = AixLib.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HDifHor,
    TDewPoiSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    TDryBulSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    ceiHeiSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    opaSkyCovSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    pAtmSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    relHumSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    totSkyCovSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    winDirSou = AixLib.BoundaryConditions.Types.DataSource.Input,
    winSpeSou = AixLib.BoundaryConditions.Types.DataSource.Input)
    "Weather data reader"
    annotation (Placement(transformation(extent={{-98,52},{-78,72}})));

  Ideal_HeaterCooler_RC2.HeaterCoolerController heaterCoolerController() annotation(
    Placement(visible = true, transformation(origin = {26, -68}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));

  Ideal_HeaterCooler_RC2.HeaterCoolerPI heaterCoolerPI(Cooler_on = true, Heater_on = true, h_coolerr = -1, h_heaterr = 165000, l_coolerr = -1650000, staOrDynn = true) annotation(
    Placement(visible = true, transformation(origin = {86, -34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
 
  Modelica.Blocks.Interfaces.RealInput Tset_Heat_in(start = 273.15 + 20) annotation(
    Placement(visible = true, transformation(origin = {108, -108}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {-102, -86}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
 
  Modelica.Blocks.Interfaces.RealInput Tset_Cool_in(start = 273.25 + 25) annotation(
    Placement(visible = true, transformation(origin = {68, -110}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {-40, -68}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
 
  Modelica.Blocks.Interfaces.RealOutput P_Heat_ou annotation(
    Placement(visible = true, transformation(origin = {178, -44}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {170, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
 
  Modelica.Blocks.Interfaces.RealOutput P_Cool_ou annotation(
    Placement(visible = true, transformation(origin = {196, -54}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-54, -78}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));

  AixLib.BoundaryConditions.SolarIrradiation.DiffusePerez HDifTil[6](    each outSkyCon=true,
    each outGroCon=true,
    til={1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 0.0, 0.0},
    each lat = 0.88645272708792,
    azi = {3.141592653589793, 0.0, 1.5707963267948966, -1.5707963267948966, 0.0, 0.0})
    "Calculates diffuse solar radiation on titled surface for all directions"
    annotation (Placement(transformation(extent={{-68,20},{-48,40}})));
  AixLib.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil[6](    til={1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 0.0, 0.0},
    each lat =  0.88645272708792,
    azi={3.141592653589793, 0.0, 1.5707963267948966, -1.5707963267948966, 0.0, 0.0})
    "Calculates direct solar radiation on titled surface for all directions"
    annotation (Placement(transformation(extent={{-68,52},{-48,72}})));
  AixLib.ThermalZones.ReducedOrder.SolarGain.CorrectionGDoublePane corGDoublePane(n=6,  UWin=3.001169286735091)
    "Correction factor for solar transmission"
    annotation (Placement(transformation(extent={{6,54},{26,74}})));
  AixLib.ThermalZones.ReducedOrder.RC.TwoElements
  thermalZoneTwoElements(
    redeclare package Medium = Modelica.Media.Air.DryAirNasa,
    VAir=896.0,
    hConExt=2.3635550772032947,
    hConWin=2.7,
    gWin=0.75,
    ratioWinConRad=0.02,
    nExt=1,
    RExt={0.00015084029268367494},
    CExt={81900977.50896597},
    hRad=5.0,
    AInt=1194.6666666666667,
    hConInt=2.3250000000000006,
    nInt=1,
    RInt={5.610715581761099e-05},
    CInt={275756919.7710094},
    RWin=0.0035556097362753453,
    RExtRem=0.002919251468311393,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    extWallRC(thermCapExt(each der_T(fixed=true))),
    intWallRC(thermCapInt(each der_T(fixed=true))),
    nOrientations=6,
    AWin={11.484200000000001, 11.484200000000001, 11.484200000000001, 11.484200000000001, 0.0, 0.0},
    ATransparent={11.484200000000001, 11.484200000000001, 11.484200000000001, 11.484200000000001, 0.0, 0.0},
    AExt={44.8826, 44.8826, 44.8826, 44.8826, 45.514, 45.514}, nPorts = 2)
    "Thermal zone"
    annotation (Placement(transformation(extent={{44,-2},{92,34}})));
  AixLib.ThermalZones.ReducedOrder.EquivalentAirTemperature.VDI6007WithWindow eqAirTemp(
    n=6,
    wfGro=0.14851895293826808,
    wfWall={0.1887095555662707, 0.1887095555662707, 0.1887095555662707, 0.1887095555662707, 0.0966428247966491, 0.0},
    wfWin={0.25, 0.25, 0.25, 0.25, 0.0, 0.0},
    withLongwave=true,
    aExt=0.5,
    hConWallOut=19.999999999999996,
    hRad=4.999999999999999,
    hConWinOut=20.0,
    TGro=286.15) "Computes equivalent air temperature"
    annotation (Placement(transformation(extent={{-24,-14},{-4,6}})));
  Modelica.Blocks.Math.Add solRad[6]
    "Sums up solar radiation of both directions"
    annotation (Placement(transformation(extent={{-38,6},{-28,16}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature
    "Prescribed temperature for exterior walls outdoor surface temperature"
    annotation (Placement(transformation(extent={{8,-6},{20,6}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature1
    "Prescribed temperature for windows outdoor surface temperature"
    annotation (Placement(transformation(extent={{8,14},{20,26}})));
  Modelica.Thermal.HeatTransfer.Components.Convection thermalConductorWin
    "Outdoor convective heat transfer of windows"
    annotation (Placement(transformation(extent={{38,16},{28,26}})));
  Modelica.Thermal.HeatTransfer.Components.Convection thermalConductorWall
    "Outdoor convective heat transfer of walls"
    annotation (Placement(transformation(extent={{36,6},{26,-4}})));
  Modelica.Blocks.Sources.Constant const[6](each k=0)
    "Sets sunblind signal to zero (open)"
    annotation (Placement(transformation(extent={{-20,14},{-14,20}})));
  AixLib.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(
    transformation(extent={{-100,-10},{-66,22}}),iconTransformation(
    extent={{-70,-12},{-50,8}})));
  Modelica.Blocks.Sources.Constant hConWall(k=25.0*270.5584)
    "Outdoor coefficient of heat transfer for walls"
    annotation (Placement(
    transformation(
    extent={{-4,-4},{4,4}},
    rotation=90,
    origin={30,-16})));
  Modelica.Blocks.Sources.Constant hConvWin(k=25.0*45.936800000000005)
    "Outdoor coefficient of heat transfer for windows"
    annotation (Placement(
    transformation(
    extent={{4,-4},{-4,4}},
    rotation=90,
    origin={32,38})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow personsRad
    "Radiative heat flow of persons"
    annotation (Placement(transformation(extent={{48,-42},{68,-22}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow personsConv
    "Convective heat flow of persons"
    annotation (Placement(transformation(extent={{48,-62},{68,-42}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow machinesConv
    "Convective heat flow of machines"
    annotation (Placement(transformation(extent={{48,-84},{68,-64}})));
  Modelica.Blocks.Interfaces.RealInput personsRad_in(start=0) annotation(
    Placement(visible = true, transformation(origin = {-120, -30}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-108, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput personsConv_in(start=0) annotation(
    Placement(visible = true, transformation(origin = {-120, -54}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-108, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput machinesConv_in(start=0) annotation(
    Placement(visible = true, transformation(origin = {-120, -76}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-108, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput heatCoolRoom_in(start=0) annotation(
    Placement(visible = true, transformation(origin = {34, -120}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {-108, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow heatCoolRoom annotation(
    Placement(visible = true, transformation(extent = {{50, -102}, {70, -82}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput Tair_ou annotation(
    Placement(visible = true, transformation(origin = {170, 32}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {136, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput DryBulb(start=273.15+20) annotation(
    Placement(visible = true, transformation(origin = {-145, 77}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput TotSkyCvr(start=0.5) annotation(
    Placement(visible = true, transformation(origin = {-145, 45}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput DirNormRad(start=0) annotation(
    Placement(visible = true, transformation(origin = {-137, 7}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput DifHorzRad(start=0) annotation(
    Placement(visible = true, transformation(origin = {-145, 13}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput HorzIRSky(start=0) annotation(
    Placement(visible = true, transformation(origin = {-137, 21}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput Atmos_Pressure(start=101325) annotation(
    Placement(visible = true, transformation(origin = {-145, 93}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput WindDir(start=60) annotation(
    Placement(visible = true, transformation(origin = {-145, 29}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput Ceiling_Hgt(start=20000) annotation(
    Placement(visible = true, transformation(origin = {-137, 53}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput WindSpd(start=1) annotation(
    Placement(visible = true, transformation(origin = {-137, 37}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput DewPoint(start=273.15+10) annotation(
    Placement(visible = true, transformation(origin = {-137, 85}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput RelHum(start=0.5) annotation(
    Placement(visible = true, transformation(origin = {-137, 69}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput OpaqSkyCvr(start=0.5) annotation(
    Placement(visible = true, transformation(origin = {-145, 61}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput windowIndoorSurface_in(start=0) annotation(
    Placement(visible = true, transformation(origin = {48, -10}, extent = {{-4, -4}, {4, 4}}, rotation = 90), iconTransformation(origin = {48, -6}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput intWallIndoorSurface_in(start=0) annotation(
    Placement(visible = true, transformation(origin = {56, -10}, extent = {{-4, -4}, {4, 4}}, rotation = 90), iconTransformation(origin = {48, -6}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput extWallIndoorSurface_in(start=0) annotation(
    Placement(visible = true, transformation(origin = {52, -10}, extent = {{-4, -4}, {4, 4}}, rotation = 90), iconTransformation(origin = {48, -6}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
   Modelica.Blocks.Math.UnitConversions.To_degC to_degC annotation(
    Placement(visible = true, transformation(origin = {140, 32}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Blocks.Math.UnitConversions.To_degC to_degC1 annotation(
      Placement(visible = true, transformation(origin = {-6, -62}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));

equation
  connect(eqAirTemp.TEqAirWin, prescribedTemperature1.T)
    annotation (Line(
    points={{-3,-0.2},{0,-0.2},{0,20},{6.8,20}},   color={0,0,127}));
  connect(eqAirTemp.TEqAir, prescribedTemperature.T)
    annotation (Line(points={{-3,-4},{4,-4},{4,0},{6.8,0}},
    color={0,0,127}));
  connect(weaDat.weaBus, weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,18},{-84,18},{-84,12},{-83,12},{-83,6}},
    color={255,204,51},
    thickness=0.5), Text(
    string="%second",
    index=1,
    extent={{6,3},{6,3}}));
  connect(weaBus.TDryBul, eqAirTemp.TDryBul)
    annotation (Line(
    points={{-83,6},{-83,-2},{-38,-2},{-38,-10},{-26,-10}},
    color={255,204,51},
    thickness=0.5), Text(
    string="%first",
    index=-1,
    extent={{-6,3},{-6,3}}));
  connect(personsRad_in, personsRad.Q_flow) annotation(
    Line(points = {{-120, -30}, {48, -30}, {48, -32}}, color = {0, 0, 127}));
  connect(personsConv_in, personsConv.Q_flow) annotation(
    Line(points = {{-120, -54}, {48, -54}, {48, -52}}, color = {0, 0, 127}));
  connect(machinesConv_in, machinesConv.Q_flow) annotation(
    Line(points = {{-120, -76}, {48, -76}, {48, -74}}, color = {0, 0, 127}));
  connect(heatCoolRoom.port, thermalZoneTwoElements.intGainsConv) annotation(
    Line(points = {{70, -92}, {92, -92}, {92, 20}}, color = {191, 0, 0}));
  connect(heatCoolRoom_in, heatCoolRoom.Q_flow) annotation(
    Line(points = {{34, -120}, {34, -92}, {50, -92}}, color = {0, 0, 127}));
  connect(thermalZoneTwoElements.TAir, to_degC.u) annotation(
    Line(points = {{94, 32}, {128, 32}}, color = {0, 0, 127}));
  connect(to_degC.y, Tair_ou) annotation(
    Line(points = {{151, 32}, {170, 32}}, color = {0, 0, 127}));
  connect(weaDat.pAtm_in, Atmos_Pressure) annotation(
    Line(points = {{-98, 76}, {-104, 76}, {-104, 93}, {-145, 93}}, color = {0, 0, 127}));
  connect(weaDat.TDewPoi_in, DewPoint) annotation(
    Line(points = {{-98, 74}, {-114, 74}, {-114, 86}, {-136, 86}}, color = {0, 0, 127}));
  connect(weaDat.TDryBul_in, DryBulb) annotation(
    Line(points = {{-98, 72}, {-120, 72}, {-120, 77}, {-145, 77}}, color = {0, 0, 127}));
  connect(weaDat.relHum_in, RelHum) annotation(
    Line(points = {{-98, 68}, {-120, 68}, {-120, 70}, {-136, 70}}, color = {0, 0, 127}));
  connect(weaDat.opaSkyCov_in, OpaqSkyCvr) annotation(
    Line(points = {{-98, 64}, {-130, 64}, {-130, 61}, {-145, 61}}, color = {0, 0, 127}));
  connect(weaDat.ceiHei_in, Ceiling_Hgt) annotation(
    Line(points = {{-98, 62}, {-128, 62}, {-128, 54}, {-136, 54}}, color = {0, 0, 127}));
  connect(weaDat.totSkyCov_in, TotSkyCvr) annotation(
    Line(points = {{-98, 60}, {-124, 60}, {-124, 46}, {-144, 46}}, color = {0, 0, 127}));
  connect(weaDat.winSpe_in, WindSpd) annotation(
    Line(points = {{-98, 58}, {-120, 58}, {-120, 38}, {-136, 38}}, color = {0, 0, 127}));
  connect(weaDat.winDir_in, WindDir) annotation(
    Line(points = {{-98, 56}, {-116, 56}, {-116, 30}, {-144, 30}}, color = {0, 0, 127}));
  connect(weaDat.HInfHor_in, HorzIRSky) annotation(
    Line(points = {{-98, 54}, {-112, 54}, {-112, 22}, {-136, 22}}, color = {0, 0, 127}));
  connect(weaDat.HDifHor_in, DifHorzRad) annotation(
    Line(points = {{-98, 52}, {-110, 52}, {-110, 14}, {-144, 14}}, color = {0, 0, 127}));
  connect(weaDat.HDirNor_in, DirNormRad) annotation(
    Line(points = {{-98, 52}, {-106, 52}, {-106, 8}, {-136, 8}}, color = {0, 0, 127}));
    connect(theZonAda.heaPorAir, thermalZoneTwoElements.intGainsConv) annotation(
    Line(points = {{-120, 152}, {94, 152}, {94, 20}, {92, 20}}, color = {191, 0, 0}));
  connect(theZonAda.ports, senMasFlon.port_a) annotation(
    Line(points = {{-120, 160}, {-88, 160}, {-88, 120}}, color = {0, 127, 255}, thickness = 0.5));
  connect(senMasFlon.port_b, thermalZoneTwoElements.ports[1:2]) annotation(
    Line(points = {{-68, 120}, {84, 120}, {84, -2}}, color = {0, 127, 255}));
  connect(thermalZoneTwoElements.windowIndoorSurface, windowIndoorSurface_in) annotation(
    Line(points = {{48, -2}, {48, -10}}, color = {191, 0, 0}));
  connect(thermalZoneTwoElements.extWallIndoorSurface, extWallIndoorSurface_in) annotation(
    Line(points = {{52, -2}, {52, -10}}, color = {191, 0, 0}));
  connect(thermalZoneTwoElements.intWallIndoorSurface, intWallIndoorSurface_in) annotation(
    Line(points = {{56, -2}, {56, -10}}, color = {191, 0, 0}));
  connect(const.y, eqAirTemp.sunblind)
    annotation (Line(points={{-13.7,17},{-12,17},{-12,8},{-14,8},{-14,8}},
    color={0,0,127}));
  connect(HDifTil.HSkyDifTil, corGDoublePane.HSkyDifTil)
    annotation (Line(
    points={{-47,36},{-28,36},{-6,36},{-6,66},{4,66}}, color={0,0,127}));
  connect(HDirTil.H, corGDoublePane.HDirTil)
    annotation (Line(points={{-47,62},{-10,62},{-10,70},{4,70}},
    color={0,0,127}));
  connect(HDirTil.H,solRad. u1)
    annotation (Line(points={{-47,62},{-42,62},{-42,
    14},{-39,14}}, color={0,0,127}));
  connect(HDirTil.inc, corGDoublePane.inc)
    annotation (Line(points={{-47,58},{4,58},{4,58}}, color={0,0,127}));
  connect(HDifTil.H,solRad. u2)
    annotation (Line(points={{-47,30},{-44,30},{-44,
    8},{-39,8}}, color={0,0,127}));
  connect(HDifTil.HGroDifTil, corGDoublePane.HGroDifTil)
    annotation (Line(
    points={{-47,24},{-4,24},{-4,62},{4,62}}, color={0,0,127}));
  connect(solRad.y, eqAirTemp.HSol)
    annotation (Line(points={{-27.5,11},{-26,11},{-26,2},{-26,2}},
    color={0,0,127}));
    connect(weaDat.weaBus, HDifTil[1].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[1].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[2].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[2].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[3].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[3].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[4].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[4].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[5].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[5].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[6].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[6].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
  connect(personsRad.port, thermalZoneTwoElements.intGainsRad)
    annotation (Line(
    points={{68,-32},{84,-32},{100,-32},{100,24},{92.2,24}},
    color={191,0,0}));
  connect(thermalConductorWin.solid, thermalZoneTwoElements.window)
    annotation (
     Line(points={{38,21},{40,21},{40,20},{43.8,20}}, color={191,0,0}));
  connect(prescribedTemperature1.port, thermalConductorWin.fluid)
    annotation (Line(points={{20,20},{28,20},{28,21}}, color={191,0,0}));
  connect(thermalZoneTwoElements.extWall, thermalConductorWall.solid)
    annotation (Line(points={{43.8,12},{40,12},{40,1},{36,1}},
    color={191,0,0}));
  connect(thermalConductorWall.fluid, prescribedTemperature.port)
    annotation (Line(points={{26,1},{24,1},{24,0},{20,0}}, color={191,0,0}));
  connect(hConWall.y, thermalConductorWall.Gc)
    annotation (Line(points={{30,-11.6},{30,-4},{31,-4}}, color={0,0,127}));
  connect(hConvWin.y, thermalConductorWin.Gc)
    annotation (Line(points={{32,33.6},{32,26},{33,26}}, color={0,0,127}));
  connect(weaBus.TBlaSky, eqAirTemp.TBlaSky)
    annotation (Line(
    points={{-83,6},{-58,6},{-58,2},{-32,2},{-32,-4},{-26,-4}},
    color={255,204,51},
    thickness=0.5), Text(
    string="%first",
    index=-1,
    extent={{-6,3},{-6,3}}));
  connect(machinesConv.port, thermalZoneTwoElements.intGainsConv)
    annotation (
    Line(points={{68,-74},{82,-74},{96,-74},{96,20},{92,20}}, color={191,
    0,0}));
  connect(personsConv.port, thermalZoneTwoElements.intGainsConv)
    annotation (
    Line(points={{68,-52},{96,-52},{96,20},{92,20}}, color={191,0,0}));
  connect(corGDoublePane.solarRadWinTrans, thermalZoneTwoElements.solRad)
    annotation (Line(points={{27,64},{34,64},{40,64},{40,31},{43,31}}, color={0,
    0,127}));
  

  
  
  connect(heaterCoolerController.heaterActive, heaterCoolerPI.heaterActive) annotation(
    Line(points = {{34, -66}, {93, -66}, {93, -41}}, color = {255, 0, 255}));
  connect(heaterCoolerController.coolerActive, heaterCoolerPI.coolerActive) annotation(
    Line(points = {{34, -70}, {79, -70}, {79, -41}}, color = {255, 0, 255}));
  connect(Tset_Cool_in, heaterCoolerPI.setPointCool) annotation(
    Line(points = {{68, -110}, {68, -73.5}, {84, -73.5}, {84, -41}}, color = {0, 0, 127}));
  connect(Tset_Heat_in, heaterCoolerPI.setPointHeat) annotation(
    Line(points = {{108, -108}, {108, -84}, {88, -84}, {88, -41}}, color = {0, 0, 127}));
  connect(heaterCoolerPI.heatingPower, P_Heat_ou) annotation(
    Line(points = {{96, -30}, {117, -30}, {117, -44}, {178, -44}}, color = {0, 0, 127}));
  connect(heaterCoolerPI.coolingPower, P_Cool_ou) annotation(
    Line(points = {{96, -35}, {141, -35}, {141, -54}, {196, -54}}, color = {0, 0, 127}));
  connect(heaterCoolerPI.heatCoolRoom, thermalZoneTwoElements.intGainsConv) annotation(
    Line(points = {{95, -38}, {102, -38}, {102, 22}}, color = {191, 0, 0}));
  connect(weaBus.TDryBul, to_degC1.u) annotation(
    Line(points = {{-88, -10}, {-74, -10}, {-74, -66}}, color = {0, 0, 127}));
  connect(to_degC1.y, heaterCoolerController.TDryBul) annotation(
    Line(points = {{-50, -66}, {16, -66}, {16, -62}}, color = {0, 0, 127}));

  annotation (experiment(
  StartTime=0,
  StopTime=31536000,
  Interval=3600,
  __Dymola_Algorithm="Cvode"),
  __Dymola_experimentSetupOutput(equidistant=true,
  events=false));
  

end ResidentialApartmentBlock_1_SingleDwelling;
