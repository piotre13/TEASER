package Ideal_HeaterCooler_RC2 
model Building_RC2 "This is the simulation model of SingleDwelling within building ResidentialBuilding with traceable ID None"
    extends AixLib.Fluid.FMI.ExportContainers.ThermalZone(redeclare final package Medium = Modelica.Media.Air.DryAirNasa, nPorts = 2);
    AixLib.Fluid.Sensors.MassFlowRate senMasFlon[nPorts](redeclare final package Medium = Modelica.Media.Air.DryAirNasa) "Mass flow rate sensor to connect thermal adapter with thermal zone." annotation(
      Placement(transformation(extent = {{-88, 110}, {-68, 130}})));
    parameter Integer internalGainsMode = 1 "decides which internal gains model for persons is used";
    HeaterCoolerController heaterCoolerController annotation(
      Placement(visible = true, transformation(origin = {48, -68}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    HeaterCoolerPI heaterCoolerPI(Cooler_on = true, Heater_on = true, h_coolerr = -1, h_heaterr = 165000, l_coolerr = -1650000, staOrDynn = false) annotation(
      Placement(visible = true, transformation(origin = {86, -34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput Tset_Heat_in(start = 273.15 + 20) annotation(
      Placement(visible = true, transformation(origin = {108, -108}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {-102, -86}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput Tset_Cool_in(start = 273.15 + 25) annotation(
      Placement(visible = true, transformation(origin = {68, -110}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {-40, -68}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealOutput P_Heat_ou annotation(
      Placement(visible = true, transformation(origin = {178, -44}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {170, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealOutput P_Cool_ou annotation(
      Placement(visible = true, transformation(origin = {196, -54}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-54, -78}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    AixLib.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(HInfHorSou = AixLib.BoundaryConditions.Types.DataSource.File, HSou = AixLib.BoundaryConditions.Types.RadiationDataSource.File, TBlaSkySou = AixLib.BoundaryConditions.Types.DataSource.File, TDewPoiSou = AixLib.BoundaryConditions.Types.DataSource.File, TDryBulSou = AixLib.BoundaryConditions.Types.DataSource.Input, calTSky = AixLib.BoundaryConditions.Types.SkyTemperatureCalculation.HorizontalRadiation, ceiHeiSou = AixLib.BoundaryConditions.Types.DataSource.File, computeWetBulbTemperature = false, filNam = Modelica.Utilities.Files.loadResource("modelica://test_thesis/DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"), opaSkyCovSou = AixLib.BoundaryConditions.Types.DataSource.File, pAtmSou = AixLib.BoundaryConditions.Types.DataSource.File, relHumSou = AixLib.BoundaryConditions.Types.DataSource.File, totSkyCovSou = AixLib.BoundaryConditions.Types.DataSource.File, winDirSou = AixLib.BoundaryConditions.Types.DataSource.File, winSpeSou = AixLib.BoundaryConditions.Types.DataSource.File) "Weather data reader" annotation(
      Placement(visible = true, transformation(extent = {{-100, 50}, {-80, 70}}, rotation = 0)));
    AixLib.BoundaryConditions.SolarIrradiation.DiffusePerez HDifTil[6](each outSkyCon = true, each outGroCon = true, til = {1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 0.0, 0.0}, each lat = 0.88645272708792, azi = {3.141592653589793, 0.0, 1.5707963267948966, -1.5707963267948966, 0.0, 0.0}) "Calculates diffuse solar radiation on titled surface for all directions" annotation(
      Placement(transformation(extent = {{-68, 20}, {-48, 40}})));
    AixLib.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil[6](til = {1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 0.0, 0.0}, each lat = 0.88645272708792, azi = {3.141592653589793, 0.0, 1.5707963267948966, -1.5707963267948966, 0.0, 0.0}) "Calculates direct solar radiation on titled surface for all directions" annotation(
      Placement(transformation(extent = {{-68, 52}, {-48, 72}})));
    AixLib.ThermalZones.ReducedOrder.SolarGain.CorrectionGDoublePane corGDoublePane(n = 6, UWin = 1.8936557576825386) "Correction factor for solar transmission" annotation(
      Placement(transformation(extent = {{6, 54}, {26, 74}})));
    AixLib.ThermalZones.ReducedOrder.RC.TwoElements thermalZoneTwoElements(redeclare package Medium = Modelica.Media.Air.DryAirNasa, VAir = 412.5, hConExt = 1.903592814371258, hConWin = 2.7, gWin = 0.67, ratioWinConRad = 0.029999999999999995, nExt = 1, RExt = {6.643697370214624e-05}, CExt = {131690404.11725213}, hRad = 5.0, AInt = 343.75, hConInt = 2.7, nInt = 1, RInt = {0.0003595246009906691}, CInt = {21472982.80327397}, RWin = 0.011940298507462687, RExtRem = 0.0034792941801327208, energyDynamics = Modelica.Fluid.Types.Dynamics.FixedInitial, extWallRC(thermCapExt(each der_T(fixed = true))), intWallRC(thermCapInt(each der_T(fixed = true))), nOrientations = 6, AWin = {7.5, 7.5, 7.5, 7.5, 0.0, 0.0}, ATransparent = {7.5, 7.5, 7.5, 7.5, 0.0, 0.0}, AExt = {25.500000000000004, 25.500000000000004, 25.500000000000004, 25.500000000000004, 199.5, 199.5}, nPorts = 2) "Thermal zone" annotation(
      Placement(visible = true, transformation(extent = {{54, 0}, {102, 36}}, rotation = 0)));
    AixLib.ThermalZones.ReducedOrder.EquivalentAirTemperature.VDI6007WithWindow eqAirTemp(n = 6, wfGro = 0.4413257276293783, wfWall = {0.04939294537096399, 0.04939294537096399, 0.04939294537096399, 0.04939294537096399, 0.3611024908867657, 0.0}, wfWin = {0.25, 0.25, 0.25, 0.25, 0.0, 0.0}, withLongwave = true, aExt = 0.5, hConWallOut = 20.000000000000007, hRad = 5.0, hConWinOut = 20.0, TGro = 286.15) "Computes equivalent air temperature" annotation(
      Placement(transformation(extent = {{-24, -14}, {-4, 6}})));
    Modelica.Blocks.Math.Add solRad[6] "Sums up solar radiation of both directions" annotation(
      Placement(transformation(extent = {{-38, 6}, {-28, 16}})));
    Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature "Prescribed temperature for exterior walls outdoor surface temperature" annotation(
      Placement(transformation(extent = {{8, -6}, {20, 6}})));
    Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature1 "Prescribed temperature for windows outdoor surface temperature" annotation(
      Placement(transformation(extent = {{8, 14}, {20, 26}})));
    Modelica.Thermal.HeatTransfer.Components.Convection thermalConductorWin "Outdoor convective heat transfer of windows" annotation(
      Placement(transformation(extent = {{38, 16}, {28, 26}})));
    Modelica.Thermal.HeatTransfer.Components.Convection thermalConductorWall "Outdoor convective heat transfer of walls" annotation(
      Placement(visible = true, transformation(extent = {{36, 6}, {26, -4}}, rotation = 0)));
    Modelica.Blocks.Sources.Constant const[6](each k = 0) "Sets sunblind signal to zero (open)" annotation(
      Placement(transformation(extent = {{-20, 14}, {-14, 20}})));
    AixLib.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus" annotation(
      Placement(visible = true, transformation(extent = {{-106, -26}, {-72, 6}}, rotation = 0), iconTransformation(extent = {{-70, -12}, {-50, 8}}, rotation = 0)));
    Modelica.Blocks.Sources.Constant hConWall(k = 25.000000000000004 * 501.0) "Outdoor coefficient of heat transfer for walls" annotation(
      Placement(transformation(extent = {{-4, -4}, {4, 4}}, rotation = 90, origin = {30, -16})));
    Modelica.Blocks.Sources.Constant hConvWin(k = 25.0 * 30.0) "Outdoor coefficient of heat transfer for windows" annotation(
      Placement(transformation(extent = {{4, -4}, {-4, 4}}, rotation = 90, origin = {32, 38})));
    Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow personsRad "Radiative heat flow of persons" annotation(
      Placement(visible = true, transformation(origin = {152, 92}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow personsConv "Convective heat flow of persons" annotation(
      Placement(visible = true, transformation(origin = {130, 118}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow machinesConv "Convective heat flow of machines" annotation(
      Placement(visible = true, transformation(origin = {118, 142}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealInput personsRad_in(start = 0) annotation(
      Placement(visible = true, transformation(origin = {218, 100}, extent = {{-20, -20}, {20, 20}}, rotation = 180), iconTransformation(origin = {-108, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput personsConv_in(start = 0) annotation(
      Placement(visible = true, transformation(origin = {204, 128}, extent = {{-20, -20}, {20, 20}}, rotation = 180), iconTransformation(origin = {-108, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput machinesConv_in(start = 0) annotation(
      Placement(visible = true, transformation(origin = {198, 158}, extent = {{-20, -20}, {20, 20}}, rotation = 180), iconTransformation(origin = {-108, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealOutput Tair_ou annotation(
      Placement(visible = true, transformation(origin = {220, 32}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {136, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput DryBulb(start = 273.15 + 20) annotation(
      Placement(visible = true, transformation(origin = {-153, 81}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput TotSkyCvr(start = 0.5) annotation(
      Placement(visible = true, transformation(origin = {-145, 45}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput DirNormRad(start = 0) annotation(
      Placement(visible = true, transformation(origin = {-137, 7}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput DifHorzRad(start = 0) annotation(
      Placement(visible = true, transformation(origin = {-145, 13}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput HorzIRSky(start = 0) annotation(
      Placement(visible = true, transformation(origin = {-137, 21}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput Atmos_Pressure(start = 101325) annotation(
      Placement(visible = true, transformation(origin = {-145, 93}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput WindDir(start = 60) annotation(
      Placement(visible = true, transformation(origin = {-145, 29}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput Ceiling_Hgt(start = 20000) annotation(
      Placement(visible = true, transformation(origin = {-137, 53}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput WindSpd(start = 1) annotation(
      Placement(visible = true, transformation(origin = {-137, 37}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput DewPoint(start = 273.15 + 10) annotation(
      Placement(visible = true, transformation(origin = {-137, 85}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput RelHum(start = 0.5) annotation(
      Placement(visible = true, transformation(origin = {-149, 71}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput OpaqSkyCvr(start = 0.5) annotation(
      Placement(visible = true, transformation(origin = {-145, 61}, extent = {{-7, -7}, {7, 7}}, rotation = 0), iconTransformation(origin = {-136, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput windowIndoorSurface_in(start = 0) annotation(
      Placement(visible = true, transformation(origin = {-42, -108}, extent = {{-4, -4}, {4, 4}}, rotation = 90), iconTransformation(origin = {48, -6}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput intWallIndoorSurface_in(start = 0) annotation(
      Placement(visible = true, transformation(origin = {-34, -108}, extent = {{-4, -4}, {4, 4}}, rotation = 90), iconTransformation(origin = {48, -6}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Interfaces.RealInput extWallIndoorSurface_in(start = 0) annotation(
      Placement(visible = true, transformation(origin = {-38, -108}, extent = {{-4, -4}, {4, 4}}, rotation = 90), iconTransformation(origin = {48, -6}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
    Modelica.Blocks.Math.UnitConversions.To_degC to_degC annotation(
      Placement(visible = true, transformation(origin = {138, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Blocks.Math.UnitConversions.To_degC to_degC1 annotation(
      Placement(visible = true, transformation(origin = {-6, -62}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  equation
    connect(eqAirTemp.TEqAirWin, prescribedTemperature1.T) annotation(
      Line(points = {{-3, -0.2}, {0, -0.2}, {0, 20}, {6.8, 20}}, color = {0, 0, 127}));
    connect(eqAirTemp.TEqAir, prescribedTemperature.T) annotation(
      Line(points = {{-3, -4}, {4, -4}, {4, 0}, {6.8, 0}}, color = {0, 0, 127}));
    connect(weaDat.weaBus, weaBus) annotation(
      Line(points = {{-80, 60}, {-80, 18}, {-84, 18}, {-84, -10}, {-89, -10}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaBus.TDryBul, eqAirTemp.TDryBul) annotation(
      Line(points = {{-89, -10}, {-26, -10}}, color = {255, 204, 51}, thickness = 0.5));
    connect(personsRad_in, personsRad.Q_flow) annotation(
      Line(points = {{218, 100}, {152, 100}, {152, 102}}, color = {0, 0, 127}));
  connect(personsConv_in, personsConv.Q_flow) annotation(
      Line(points = {{204, 128}, {130, 128}}, color = {0, 0, 127}));
    connect(machinesConv_in, machinesConv.Q_flow) annotation(
      Line(points = {{198, 158}, {198, 157}, {118, 157}, {118, 152}}, color = {0, 0, 127}));
    connect(thermalZoneTwoElements.TAir, to_degC.u) annotation(
      Line(points = {{103, 34}, {126, 34}}, color = {0, 0, 127}));
    connect(to_degC.y, Tair_ou) annotation(
      Line(points = {{149, 34}, {183.5, 34}, {183.5, 32}, {220, 32}}, color = {0, 0, 127}));
    connect(weaDat.pAtm_in, Atmos_Pressure) annotation(
      Line(points = {{-101, 74}, {-104, 74}, {-104, 93}, {-145, 93}}, color = {0, 0, 127}));
    connect(weaDat.TDewPoi_in, DewPoint) annotation(
      Line(points = {{-101, 71}, {-114, 71}, {-114, 85}, {-137, 85}}, color = {0, 0, 127}));
    connect(weaDat.TDryBul_in, DryBulb) annotation(
      Line(points = {{-101, 69}, {-138, 69}, {-138, 81}, {-153, 81}}, color = {0, 0, 127}));
    connect(weaDat.relHum_in, RelHum) annotation(
      Line(points = {{-101, 65}, {-126, 65}, {-126, 71}, {-149, 71}}, color = {0, 0, 127}));
    connect(weaDat.opaSkyCov_in, OpaqSkyCvr) annotation(
      Line(points = {{-101, 63}, {-145, 63}, {-145, 61}}, color = {0, 0, 127}));
    connect(weaDat.ceiHei_in, Ceiling_Hgt) annotation(
      Line(points = {{-101, 60}, {-103.5, 60}, {-103.5, 54}, {-136, 54}}, color = {0, 0, 127}));
    connect(weaDat.totSkyCov_in, TotSkyCvr) annotation(
      Line(points = {{-101, 58}, {-108.5, 58}, {-108.5, 46}, {-144, 46}}, color = {0, 0, 127}));
    connect(weaDat.winSpe_in, WindSpd) annotation(
      Line(points = {{-101, 56}, {-120, 56}, {-120, 38}, {-136, 38}}, color = {0, 0, 127}));
    connect(weaDat.winDir_in, WindDir) annotation(
      Line(points = {{-101, 54}, {-116, 54}, {-116, 30}, {-144, 30}}, color = {0, 0, 127}));
    connect(weaDat.HInfHor_in, HorzIRSky) annotation(
      Line(points = {{-101, 50.5}, {-112, 50.5}, {-112, 22}, {-136, 22}}, color = {0, 0, 127}));
    connect(weaDat.HDifHor_in, DifHorzRad) annotation(
      Line(points = {{-101, 52}, {-110, 52}, {-110, 14}, {-144, 14}}, color = {0, 0, 127}));
    connect(weaDat.HDirNor_in, DirNormRad) annotation(
      Line(points = {{-101, 49}, {-106, 49}, {-106, 8}, {-136, 8}}, color = {0, 0, 127}));
    connect(theZonAda.heaPorAir, thermalZoneTwoElements.intGainsConv) annotation(
      Line(points = {{-120, 152}, {-8, 152}, {-8, 144}, {102, 144}, {102, 22}}, color = {191, 0, 0}));
    connect(theZonAda.ports, senMasFlon.port_a) annotation(
      Line(points = {{-120, 160}, {-88, 160}, {-88, 120}}, color = {0, 127, 255}, thickness = 0.5));
    connect(senMasFlon.port_b, thermalZoneTwoElements.ports[1:2]) annotation(
      Line(points = {{-68, 120}, {93, 120}, {93, 0}}, color = {0, 127, 255}));
    connect(thermalZoneTwoElements.windowIndoorSurface, windowIndoorSurface_in) annotation(
      Line(points = {{58, 0}, {58, -41}, {-42, -41}, {-42, -108}}, color = {191, 0, 0}));
    connect(thermalZoneTwoElements.extWallIndoorSurface, extWallIndoorSurface_in) annotation(
      Line(points = {{62, 0}, {62, -41}, {-38, -41}, {-38, -108}}, color = {191, 0, 0}));
    connect(thermalZoneTwoElements.intWallIndoorSurface, intWallIndoorSurface_in) annotation(
      Line(points = {{66, 0}, {66, -41}, {-34, -41}, {-34, -108}}, color = {191, 0, 0}));
    connect(const.y, eqAirTemp.sunblind) annotation(
      Line(points = {{-13.7, 17}, {-12, 17}, {-12, 8}, {-14, 8}, {-14, 8}}, color = {0, 0, 127}));
    connect(HDifTil.HSkyDifTil, corGDoublePane.HSkyDifTil) annotation(
      Line(points = {{-47, 36}, {-28, 36}, {-6, 36}, {-6, 66}, {4, 66}}, color = {0, 0, 127}));
    connect(HDirTil.H, corGDoublePane.HDirTil) annotation(
      Line(points = {{-47, 62}, {-10, 62}, {-10, 70}, {4, 70}}, color = {0, 0, 127}));
    connect(HDirTil.H, solRad.u1) annotation(
      Line(points = {{-47, 62}, {-42, 62}, {-42, 14}, {-39, 14}}, color = {0, 0, 127}));
    connect(HDirTil.inc, corGDoublePane.inc) annotation(
      Line(points = {{-47, 58}, {4, 58}, {4, 58}}, color = {0, 0, 127}));
    connect(HDifTil.H, solRad.u2) annotation(
      Line(points = {{-47, 30}, {-44, 30}, {-44, 8}, {-39, 8}}, color = {0, 0, 127}));
    connect(HDifTil.HGroDifTil, corGDoublePane.HGroDifTil) annotation(
      Line(points = {{-47, 24}, {-4, 24}, {-4, 62}, {4, 62}}, color = {0, 0, 127}));
    connect(solRad.y, eqAirTemp.HSol) annotation(
      Line(points = {{-27.5, 11}, {-26, 11}, {-26, 2}, {-26, 2}}, color = {0, 0, 127}));
    connect(weaDat.weaBus, HDifTil[1].weaBus) annotation(
      Line(points = {{-80, 60}, {-80, 30}, {-68, 30}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDirTil[1].weaBus) annotation(
      Line(points = {{-80, 60}, {-70, 60}, {-70, 62}, {-68, 62}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDifTil[2].weaBus) annotation(
      Line(points = {{-80, 60}, {-80, 30}, {-68, 30}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDirTil[2].weaBus) annotation(
      Line(points = {{-80, 60}, {-70, 60}, {-70, 62}, {-68, 62}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDifTil[3].weaBus) annotation(
      Line(points = {{-80, 60}, {-80, 30}, {-68, 30}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDirTil[3].weaBus) annotation(
      Line(points = {{-80, 60}, {-70, 60}, {-70, 62}, {-68, 62}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDifTil[4].weaBus) annotation(
      Line(points = {{-80, 60}, {-80, 30}, {-68, 30}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDirTil[4].weaBus) annotation(
      Line(points = {{-80, 60}, {-70, 60}, {-70, 62}, {-68, 62}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDifTil[5].weaBus) annotation(
      Line(points = {{-80, 60}, {-80, 30}, {-68, 30}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDirTil[5].weaBus) annotation(
      Line(points = {{-80, 60}, {-70, 60}, {-70, 62}, {-68, 62}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDifTil[6].weaBus) annotation(
      Line(points = {{-80, 60}, {-80, 30}, {-68, 30}}, color = {255, 204, 51}, thickness = 0.5));
    connect(weaDat.weaBus, HDirTil[6].weaBus) annotation(
      Line(points = {{-80, 60}, {-70, 60}, {-70, 62}, {-68, 62}}, color = {255, 204, 51}, thickness = 0.5));
    connect(personsRad.port, thermalZoneTwoElements.intGainsRad) annotation(
      Line(points = {{152, 82}, {110.1, 82}, {110.1, 26}, {102, 26}}, color = {191, 0, 0}));
    connect(thermalConductorWin.solid, thermalZoneTwoElements.window) annotation(
      Line(points = {{38, 21}, {38, 23.5}, {54, 23.5}, {54, 22}}, color = {191, 0, 0}));
    connect(prescribedTemperature1.port, thermalConductorWin.fluid) annotation(
      Line(points = {{20, 20}, {28, 20}, {28, 21}}, color = {191, 0, 0}));
    connect(thermalZoneTwoElements.extWall, thermalConductorWall.solid) annotation(
      Line(points = {{54, 14}, {54, 9.5}, {36, 9.5}, {36, 1}}, color = {191, 0, 0}));
    connect(thermalConductorWall.fluid, prescribedTemperature.port) annotation(
      Line(points = {{26, 1}, {24, 1}, {24, 0}, {20, 0}}, color = {191, 0, 0}));
    connect(hConWall.y, thermalConductorWall.Gc) annotation(
      Line(points = {{30, -11.6}, {30, -4}, {31, -4}}, color = {0, 0, 127}));
    connect(hConvWin.y, thermalConductorWin.Gc) annotation(
      Line(points = {{32, 33.6}, {32, 26}, {33, 26}}, color = {0, 0, 127}));
    connect(weaBus.TBlaSky, eqAirTemp.TBlaSky) annotation(
      Line(points = {{-89, -10}, {-57.5, -10}, {-57.5, -4}, {-26, -4}}, color = {255, 204, 51}, thickness = 0.5));
    connect(machinesConv.port, thermalZoneTwoElements.intGainsConv) annotation(
      Line(points = {{118, 132}, {118, 77}, {102, 77}, {102, 22}}, color = {191, 0, 0}));
    connect(personsConv.port, thermalZoneTwoElements.intGainsConv) annotation(
      Line(points = {{130, 108}, {130, 66}, {102, 66}, {102, 22}}, color = {191, 0, 0}));
    connect(corGDoublePane.solarRadWinTrans, thermalZoneTwoElements.solRad) annotation(
      Line(points = {{27, 64}, {40, 64}, {40, 33}, {53, 33}}, color = {0, 0, 127}));
    connect(heaterCoolerController.heaterActive, heaterCoolerPI.heaterActive) annotation(
      Line(points = {{56, -66}, {93, -66}, {93, -41}}, color = {255, 0, 255}));
    connect(heaterCoolerController.coolerActive, heaterCoolerPI.coolerActive) annotation(
      Line(points = {{56, -70}, {79, -70}, {79, -41}}, color = {255, 0, 255}));
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
    connect(DryBulb, to_degC1.u) annotation(
      Line(points = {{-153, 81}, {-114, 81}, {-114, -62}, {-18, -62}}, color = {0, 0, 127}));
    connect(to_degC1.y, heaterCoolerController.TDryBul) annotation(
      Line(points = {{6, -62}, {38, -62}}, color = {0, 0, 127}));
    annotation(
      __OpenModelica_simulationFlags(lv = "LOG_STATS", s = "dassl"),
      __OpenModelica_commandLineOptions = "--matchingAlgorithm=PFPlusExt --indexReductionMethod=dynamicStateSelection -d=initialization,NLSanalyticJacobian");
  end Building_RC2;

  model HeaterCoolerController
   parameter Real TThresholdHeater = 15.0;
    parameter Real TThresholdCooler = 26.0;
    Modelica.Blocks.Sources.Constant TAirThresholdHeating(k = TThresholdHeater) "Threshold temperature below which heating is activated" annotation(
      Placement(transformation(extent = {{-56, 6}, {-44, 18}})));
    Modelica.Blocks.Logical.Less less "check if outside temperature below threshold" annotation(
      Placement(transformation(extent = {{-10, -10}, {10, 10}}, rotation = 0, origin = {-2, 20})));
    Modelica.Blocks.Interfaces.BooleanOutput heaterActive "true if heater is active" annotation(
      Placement(transformation(extent = {{100, 10}, {120, 30}}), iconTransformation(extent = {{72, 10}, {92, 30}})));
    Modelica.Blocks.Interfaces.BooleanOutput coolerActive "true if cooler is active" annotation(
      Placement(transformation(extent = {{100, -30}, {120, -10}}), iconTransformation(extent = {{72, -30}, {92, -10}})));
    Modelica.Blocks.Logical.Greater greater "check if outside temperature above threshold" annotation(
      Placement(transformation(extent = {{-10, -10}, {10, 10}}, rotation = 0, origin = {-2, -20})));
    Modelica.Blocks.Sources.Constant TAirThresholdCooling(k = TThresholdCooler) "Threshold temperature above which cooling is activated" annotation(
      Placement(transformation(extent = {{-56, -34}, {-44, -22}})));
    Modelica.Blocks.Interfaces.RealInput TDryBul annotation(
      Placement(visible = true, transformation(origin = {-124, 60}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-106, 60}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  equation
    connect(TAirThresholdHeating.y, less.u2) annotation(
      Line(points = {{-43.4, 12}, {-14, 12}}, color = {0, 0, 127}));
    connect(TAirThresholdCooling.y, greater.u2) annotation(
      Line(points = {{-43.4, -28}, {-14, -28}}, color = {0, 0, 127}));
    connect(less.y, heaterActive) annotation(
      Line(points = {{9, 20}, {110, 20}}, color = {255, 0, 255}));
    connect(greater.y, coolerActive) annotation(
      Line(points = {{9, -20}, {56, -20}, {56, -20}, {110, -20}}, color = {255, 0, 255}));
    connect(TDryBul, less.u1) annotation(
      Line(points = {{-124, 60}, {-26, 60}, {-26, 20}, {-14, 20}}, color = {0, 0, 127}));
    connect(TDryBul, greater.u1) annotation(
      Line(points = {{-124, 60}, {-26, 60}, {-26, -20}, {-14, -20}}, color = {0, 0, 127}));
    annotation(
      Icon(coordinateSystem(preserveAspectRatio = false), graphics = {Rectangle(lineColor = {135, 135, 135}, fillColor = {255, 255, 170}, fillPattern = FillPattern.Solid, extent = {{-80, 80}, {80, -80}}), Text(lineColor = {175, 175, 175}, extent = {{-58, 32}, {62, -20}}, textString = "%name")}),
      Diagram(coordinateSystem(preserveAspectRatio = false)),
      Documentation(info = "<html>
  <h4><span style=\"color: #008000\">Overview </span></h4>
  <p>This is a simple controller which sets a threshold for heating and cooling  based on the outside temperature. This should prevent heating in summer if the AHU lowers the temperature below set temperature of ideal heater and cooler and vice versa in winter.</p>
  </html>", revisions = "<html>
   <ul>
   <li><i>November, 2019&nbsp;</i> by David Jansen:<br/>Initial integration</li>
   </ul>
   </html>"),
      experiment(StartTime = 0, StopTime = 1, Tolerance = 1e-06, Interval = 0.002),
      __OpenModelica_commandLineOptions = "--matchingAlgorithm=PFPlusExt --indexReductionMethod=dynamicStateSelection -d=initialization,NLSanalyticJacobian",
      __OpenModelica_simulationFlags(lv = "LOG_STATS", s = "dassl"));
  

  end HeaterCoolerController;

  model HeaterCoolerPI
    
    parameter Boolean staOrDynn = true "Static or dynamic activation of heater false=dynamic" annotation(choices(choice = true "Static", choice =  false "Dynamic",radioButtons = true));
    
    parameter Boolean Cooler_onn = true"Activates the cooler based on the seasonality";
    parameter Boolean Heater_onn = true "Activates the heater base don the seasonality";
    
    parameter Real h_heaterr = 0 "Upper limit controller output of the heater" annotation(Dialog(tab = "Heater", group = "Controller"));
    parameter Real l_heaterr = 0 "Lower limit controller output of the heater" annotation(Dialog(tab = "Heater", group = "Controller"));
    parameter Real KR_heaterr = 1000 "Gain of the heating controller" annotation(Dialog(tab = "Heater", group = "Controller"));
    parameter Modelica.SIunits.Time TN_heater = 1
      "Time constant of the heating controller" annotation(Dialog(tab = "Heater", group = "Controller"));
    parameter Real h_coolerr = 0 "Upper limit controller output of the cooler"
                                                                             annotation(Dialog(tab = "Cooler", group = "Controller"));
    parameter Real l_coolerr = 0 "Lower limit controller output of the cooler"          annotation(Dialog(tab = "Cooler", group = "Controller"));
    parameter Real KR_coolerr = 1000 "Gain of the cooling controller"
                                                                    annotation(Dialog(tab = "Cooler", group = "Controller",enable=not recOrSepp));
    parameter Modelica.SIunits.Time TN_cooler = 1
      "Time constant of the cooling controller" annotation(Dialog(tab = "Cooler", group = "Controller"));
    parameter Boolean recOrSepp = false "Use record or seperate parameters" annotation(choices(choice =  false
          "Seperate",choice = true "Record",radioButtons = true));
   
    
    extends PartialHeaterCoolerPI (recOrSep = recOrSepp, KR_cooler= KR_coolerr, KR_heater = KR_heaterr, l_cooler = l_coolerr, h_cooler = h_coolerr, l_heater = l_heaterr, h_heater=h_heaterr, Cooler_on = Cooler_onn, Heater_on= Heater_onn);
  
  Modelica.Blocks.Interfaces.RealInput setPointCool(
      final quantity="ThermodynamicTemperature",
      final unit="K",
      displayUnit="degC") if (Cooler_onn)    annotation (
        Placement(transformation(extent={{-120,-60},{-80,-20}}),
          iconTransformation(
          extent={{-20,-20},{20,20}},
          rotation=90,
  
  
          origin={-24,-72})));
    
  Modelica.Blocks.Interfaces.RealInput setPointHeat(
      final quantity="ThermodynamicTemperature",
      final unit="K",
      displayUnit="degC") if (Heater_onn)    annotation (
        Placement(transformation(extent={{-120,20},{-80,60}}), iconTransformation(
          extent={{-20,-20},{20,20}},
          rotation=90,
          origin={22,-72})));
    
    Modelica.Blocks.Sources.BooleanExpression booleanExpressionHeater(y=Heater_onn) if staOrDynn annotation (Placement(transformation(extent={{-52,14},{-33,30}})));
   
    Modelica.Blocks.Sources.BooleanExpression booleanExpressionCooler(y=Cooler_onn) if staOrDynn annotation (Placement(transformation(extent={{-52,-30},{-32,-14}})));
    
    
    Modelica.Blocks.Interfaces.BooleanInput heaterActive if not staOrDynn
      "Switches Controler on and off" annotation (Placement(transformation(extent=
             {{-120,-6},{-80,34}}), iconTransformation(
          extent={{-20,-20},{20,20}},
          rotation=90,
          origin={68,-72})));
    
    Modelica.Blocks.Interfaces.BooleanInput coolerActive if not staOrDynn
      "Switches Controler on and off" annotation (Placement(transformation(extent=
             {{-120,-34},{-80,6}}), iconTransformation(
          extent={{-20,-20},{20,20}},
          rotation=90,
          origin={-70,-72})));
  
  equation
  
    if staOrDynn then
      connect(booleanExpressionHeater.y, pITempHeat.onOff) annotation (Line(points={{-32.05,
            22},{-24,22},{-24,15},{-19,15}}, color={255,0,255},
          pattern=LinePattern.Dash));
      connect(booleanExpressionCooler.y, pITempCool.onOff) annotation (Line(points={{-31,
            -22},{-24,-22},{-24,-15},{-19,-15}}, color={255,0,255},
          pattern=LinePattern.Dash));
    else
      connect(heaterActive, pITempHeat.onOff) annotation (Line(points={{-100,14},{-60,
             14},{-60,15},{-19,15}}, color={255,0,255},
          pattern=LinePattern.Dash));
      connect(pITempCool.onOff, coolerActive) annotation (Line(points={{-19,-15},{-24,
            -15},{-24,-14},{-100,-14}}, color={255,0,255},
          pattern=LinePattern.Dash));
    end if;
    connect(setPointHeat, pITempHeat.setPoint)
      annotation (Line(points={{-100,40},{-18,40},{-18,29}}, color={0,0,127}));
    connect(setPointCool, pITempCool.setPoint) annotation (Line(points={{-100,-40},
            {-58,-40},{-18,-40},{-18,-29}}, color={0,0,127}));
    annotation (Documentation(info = "<html>
   <h4><span style=\"color:#008000\">Overview</span></h4>
   <p>This is just as simple heater and/or cooler with a PI-controller. It can be used as an quasi-ideal source for heating and cooling applications. </p>
   </html>", revisions="<html>
   <ul>
   <li><i>October, 2015&nbsp;</i> by Moritz Lauster:<br/>Adapted to Annex60 and restructuring, combined V1 and V2 as well as seperate parameter and record from EBC Libs</li>
   </ul>
   <ul>
   <li><i>June, 2014&nbsp;</i> by Moritz Lauster:<br/>Added some basic documentation</li>
   </ul>
   </html>"), Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
              {100,100}})),
      Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},{100,
              100}})));
  

  end HeaterCoolerPI;

  partial model PartialHeaterCoolerPI
  
    extends AixLib.Utilities.Sources.HeaterCooler.PartialHeaterCooler;
  
    parameter Boolean Heater_on = true "Activates the heater" annotation(Dialog(tab = "Heater"));
    parameter Boolean Cooler_on = true "Activates the cooler" annotation(Dialog(tab = "Cooler"));
    parameter Real h_heater = 0 "Upper limit controller output of the heater" annotation(Dialog(tab = "Heater", group = "Controller"));
    parameter Real l_heater = 0 "Lower limit controller output of the heater" annotation(Dialog(tab = "Heater", group = "Controller"));
    parameter Real KR_heater = 1000 "Gain of the heating controller" annotation(Dialog(tab = "Heater", group = "Controller"));
    parameter Modelica.SIunits.Time TN_heater = 1
      "Time constant of the heating controller" annotation(Dialog(tab = "Heater", group = "Controller"));
    parameter Real h_cooler = 0 "Upper limit controller output of the cooler"
                                                                             annotation(Dialog(tab = "Cooler", group = "Controller"));
    parameter Real l_cooler = 0 "Lower limit controller output of the cooler"          annotation(Dialog(tab = "Cooler", group = "Controller"));
    parameter Real KR_cooler = 1000 "Gain of the cooling controller"
                                                                    annotation(Dialog(tab = "Cooler", group = "Controller"));
    parameter Modelica.SIunits.Time TN_cooler = 1
      "Time constant of the cooling controller" annotation(Dialog(tab = "Cooler", group = "Controller"));
    parameter Boolean recOrSep = false "Use record or seperate parameters" annotation(choices(choice =  false
          "Seperate",choice = true "Record",radioButtons = true));
    
    Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow Cooling if (Cooler_on)
                                                                     annotation(Placement(transformation(extent={{26,-23},
              {6,-2}})));
    AixLib.Controls.Continuous.PITemp
                   pITempCool(
      rangeSwitch=false,
      h=h_cooler ,
      l=l_cooler,
      KR=KR_cooler ,
      TN=TN_cooler) if (Cooler_on)
      "PI control for cooler"
      annotation (Placement(transformation(extent={{-20,-10},{0,-30}})));
      
    Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow Heating if (Heater_on)
                                                                     annotation(Placement(transformation(extent={{26,22},
              {6,2}})));
              
              
    AixLib.Controls.Continuous.PITemp
                   pITempHeat(
      rangeSwitch=false,
      h= h_heater,
      l= l_heater,
      KR= KR_heater,
      TN= TN_heater) if (Heater_on)
      "PI control for heater" annotation (Placement(transformation(extent={{-20,10},{0,30}})));
    Modelica.Blocks.Interfaces.RealOutput heatingPower(
     final quantity="HeatFlowRate",
     final unit="W") if (Heater_on)    "Power for heating"
      annotation (Placement(transformation(extent={{80,20},{120,60}}),
          iconTransformation(extent={{80,20},{120,60}})));
    Modelica.Blocks.Interfaces.RealOutput coolingPower(
     final quantity="HeatFlowRate",
     final unit="W") if (Cooler_on)    "Power for cooling"
      annotation (Placement(transformation(extent={{80,-26},{120,14}}),
          iconTransformation(extent={{80,-26},{120,14}})));
  equation
    connect(Heating.port, heatCoolRoom) annotation (Line(
          points={{6,12},{2,12},{2,-40},{90,-40}},
          color={191,0,0},
          smooth=Smooth.None));
    connect(pITempHeat.heatPort, heatCoolRoom) annotation (Line(
        points={{-16,11},{-16,-40},{90,-40}},
        color={191,0,0},
        smooth=Smooth.None));
    connect(pITempCool.y, Cooling.Q_flow) annotation (Line(
          points={{-1,-20},{26,-20},{26,-12.5}},
          color={0,0,127},
          smooth=Smooth.None));
    connect(Cooling.port, heatCoolRoom) annotation (Line(
          points={{6,-12.5},{2.4,-12.5},{2.4,-40},{90,-40}},
          color={191,0,0},
          smooth=Smooth.None));
    connect(pITempCool.heatPort, heatCoolRoom) annotation (Line(
        points={{-16,-11},{-16,-40},{90,-40}},
        color={191,0,0},
        smooth=Smooth.None));
    connect(Heating.Q_flow, pITempHeat.y) annotation (Line(points={{26,12},{26,20},{-1,20}}, color={0,0,127}));
    connect(Heating.Q_flow,heatingPower)
      annotation (Line(points={{26,12},{26,40},{100,40}}, color={0,0,127}));
    connect(Cooling.Q_flow,coolingPower)  annotation (Line(points={{26,-12.5},{56,
            -12.5},{56,-6},{100,-6}}, color={0,0,127}));
    annotation (Documentation(info = "<html>
   <h4><span style=\"color:#008000\">Overview</span></h4>
   <p>This is the base class of an ideal heater and/or cooler. It is used in full ideal heater/cooler models as an extension. It extends another base class and adds some basic elements.</p>
   </html>", revisions="<html>
   <ul>
   <li><i>October, 2015&nbsp;</i> by Moritz Lauster:<br/>Adapted to Annex60 and restructuring, implementing new functionalities</li>
   </ul>
   <ul>
   <li><i>June, 2014&nbsp;</i> by Moritz Lauster:<br/>Added some basic documentation</li>
   </ul>
   </html>"),
      Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},{100,
              100}})),
      Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},{100,100}})));
  

  end PartialHeaterCoolerPI;
end Ideal_HeaterCooler_RC2;