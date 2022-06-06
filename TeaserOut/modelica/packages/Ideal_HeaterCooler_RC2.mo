package Ideal_HeaterCooler_RC2

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
    parameter Boolean Heater_on = true "Activates the heater" annotation(
      Dialog(tab = "Heater"));
    parameter Boolean Cooler_on = true "Activates the cooler" annotation(
      Dialog(tab = "Cooler"));
    parameter Real h_heater = 0 "Upper limit controller output of the heater" annotation(
      Dialog(tab = "Heater", group = "Controller"));
    parameter Real l_heater = 0 "Lower limit controller output of the heater" annotation(
      Dialog(tab = "Heater", group = "Controller"));
    parameter Real KR_heater = 1000 "Gain of the heating controller" annotation(
      Dialog(tab = "Heater", group = "Controller"));
    parameter Modelica.SIunits.Time TN_heater = 1 "Time constant of the heating controller" annotation(
      Dialog(tab = "Heater", group = "Controller"));
    parameter Real h_cooler = 0 "Upper limit controller output of the cooler" annotation(
      Dialog(tab = "Cooler", group = "Controller"));
    parameter Real l_cooler = 0 "Lower limit controller output of the cooler" annotation(
      Dialog(tab = "Cooler", group = "Controller"));
    parameter Real KR_cooler = 1000 "Gain of the cooling controller" annotation(
      Dialog(tab = "Cooler", group = "Controller"));
    parameter Modelica.SIunits.Time TN_cooler = 1 "Time constant of the cooling controller" annotation(
      Dialog(tab = "Cooler", group = "Controller"));
    parameter Boolean recOrSep = false "Use record or seperate parameters" annotation(
      choices(choice = false "Seperate", choice = true "Record", radioButtons = true));
    Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow Cooling if Cooler_on annotation(
      Placement(transformation(extent = {{26, -23}, {6, -2}})));
    AixLib.Controls.Continuous.PITemp pITempCool(rangeSwitch = false, h = h_cooler, l = l_cooler, KR = KR_cooler, TN = TN_cooler) if Cooler_on "PI control for cooler" annotation(
      Placement(transformation(extent = {{-20, -10}, {0, -30}})));
    AixLib.Controls.Continuous.PITemp pITempHeat(rangeSwitch = false, h = h_heater, l = l_heater, KR = KR_heater, TN = TN_heater) if Heater_on "PI control for heater" annotation(
      Placement(transformation(extent = {{-20, 10}, {0, 30}})));
    Modelica.Blocks.Interfaces.RealOutput heatingPower(final quantity = "HeatFlowRate", final unit = "W") if Heater_on "Power for heating" annotation(
      Placement(transformation(extent = {{80, 20}, {120, 60}}), iconTransformation(extent = {{80, 20}, {120, 60}})));
    Modelica.Blocks.Interfaces.RealOutput coolingPower(final quantity = "HeatFlowRate", final unit = "W") if Cooler_on "Power for cooling" annotation(
      Placement(transformation(extent = {{80, -26}, {120, 14}}), iconTransformation(extent = {{80, -26}, {120, 14}})));
    Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow prescribedHeatFlow annotation(
      Placement(visible = true, transformation(origin = {130, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput indoor_flux annotation(
      Placement(visible = true, transformation(origin = {162, -78}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {50, -88}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow Heating annotation(
      Placement(visible = true, transformation(extent = {{26, 22}, {6, 2}}, rotation = 0)));
  equation
    connect(pITempHeat.heatPort, heatCoolRoom) annotation(
      Line(points = {{-16, 11}, {-16, -40}, {90, -40}}, color = {191, 0, 0}, smooth = Smooth.None));
    connect(pITempCool.y, Cooling.Q_flow) annotation(
      Line(points = {{-1, -20}, {26, -20}, {26, -12.5}}, color = {0, 0, 127}, smooth = Smooth.None));
    connect(Cooling.port, heatCoolRoom) annotation(
      Line(points = {{6, -12.5}, {2.4, -12.5}, {2.4, -40}, {90, -40}}, color = {191, 0, 0}, smooth = Smooth.None));
    connect(pITempCool.heatPort, heatCoolRoom) annotation(
      Line(points = {{-16, -11}, {-16, -40}, {90, -40}}, color = {191, 0, 0}, smooth = Smooth.None));
    connect(Cooling.Q_flow, coolingPower) annotation(
      Line(points = {{26, -12.5}, {56, -12.5}, {56, -6}, {100, -6}}, color = {0, 0, 127}));
    connect(heatCoolRoom, prescribedHeatFlow.port) annotation(
      Line(points = {{90, -40}, {140, -40}}, color = {191, 0, 0}));
    connect(indoor_flux, prescribedHeatFlow.Q_flow) annotation(
      Line(points = {{162, -78}, {162, -81}, {120, -81}, {120, -40}}, color = {0, 0, 127}));
    connect(Heating.Q_flow, heatingPower) annotation(
      Line(points = {{26, 12}, {26, 40}, {100, 40}}, color = {0, 0, 127}));
    connect(Heating.Q_flow, pITempHeat.y) annotation(
      Line(points = {{26, 12}, {26, 20}, {-1, 20}}, color = {0, 0, 127}));
    connect(Heating.port, heatCoolRoom) annotation(
      Line(points = {{6, 12}, {2, 12}, {2, -40}, {90, -40}}, color = {191, 0, 0}));
    annotation(
      Documentation(info = "<html>
   <h4><span style=\"color:#008000\">Overview</span></h4>
   <p>This is the base class of an ideal heater and/or cooler. It is used in full ideal heater/cooler models as an extension. It extends another base class and adds some basic elements.</p>
   </html>", revisions = "<html>
   <ul>
   <li><i>October, 2015&nbsp;</i> by Moritz Lauster:<br/>Adapted to Annex60 and restructuring, implementing new functionalities</li>
   </ul>
   <ul>
   <li><i>June, 2014&nbsp;</i> by Moritz Lauster:<br/>Added some basic documentation</li>
   </ul>
   </html>"),
      Diagram(coordinateSystem(preserveAspectRatio = false, extent = {{-100, -100}, {100, 100}})),
      Icon(coordinateSystem(preserveAspectRatio = false, extent = {{-100, -100}, {100, 100}})));
  end PartialHeaterCoolerPI;
  annotation(
    uses(Modelica(version = "3.2.3")));
end Ideal_HeaterCooler_RC2;