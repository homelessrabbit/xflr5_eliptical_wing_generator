#This code generates an XML file required to import an elliptical wing model with given dimensions into XFLR5.

import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


foilName = "foil_1234" 
wingSpan_m = 3 
chordLenght_m =0.4
n = 32    #number of sections  
m = 2     #control parameter for section distribution

########## Definition of Eliptical Wing ##########
a = wingSpan_m / 2 
b = chordLenght_m 
t = np.linspace(0,1,n)
X = a*(1-np.exp(-t*m))
X = X * (a / X[-1])
Y = np.sqrt(np.abs((1-(np.square(X)/a**2))*b**2))
Y[-1] = Y[-2] / 3
Offset = (Y[0] - Y) / 2
print(X)
##################################################
root = ET.Element("explane", version="1.0")
units = ET.SubElement(root, "Units")
length_unit_to_meter = ET.SubElement(units, "length_unit_to_meter")
length_unit_to_meter.text = "1"
mass_unit_to_kg = ET.SubElement(units, "mass_unit_to_kg")
mass_unit_to_kg.text = "1"

wing = ET.SubElement(root, "wing")
name = ET.SubElement(wing, "Name")
name.text = "Wing"
type_element = ET.SubElement(wing, "Type")
type_element.text = "MAINWING"
color = ET.SubElement(wing, "Color")
red = ET.SubElement(color, "red")
red.text = "189"
green = ET.SubElement(color, "green")
green.text = "168"
blue = ET.SubElement(color, "blue")
blue.text = "136"
alpha = ET.SubElement(color, "alpha")
alpha.text = "255"
description = ET.SubElement(wing, "Description")
description.text = ""
position = ET.SubElement(wing, "Position")
position.text = "0, 0, 0"
tilt_angle = ET.SubElement(wing, "Tilt_angle")
tilt_angle.text = "0.000"
symmetric = ET.SubElement(wing, "Symetric")
symmetric.text = "true"
is_fin = ET.SubElement(wing, "isFin")
is_fin.text = "false"
is_double_fin = ET.SubElement(wing, "isDoubleFin")
is_double_fin.text = "false"
is_sym_fin = ET.SubElement(wing, "isSymFin")
is_sym_fin.text = "false"
inertia = ET.SubElement(wing, "Inertia")
volume_mass = ET.SubElement(inertia, "Volume_Mass")
volume_mass.text = "0.000"

sections = ET.SubElement(wing,"Sections")

for i in range(len(X)):
    section = ET.SubElement(sections,"Section")
    y_position = ET.SubElement(section,"y_position")
    y_position.text = f"{X[i]:.3f}"
    chord = ET.SubElement(section,"Chord")
    chord.text = f"{Y[i]:.3f}"
    x_offset = ET.SubElement(section, "xOffset")
    x_offset.text = f"{Offset[i]:.3f}"
    dihedral = ET.SubElement(section,"Dihedral")
    dihedral.text = f"{0:.3f}"
    twist = ET.SubElement(section,"Twist")
    twist.text = f"{0:.3f}"
    x_number_of_panels = ET.SubElement(section,"x_number_of_panels")
    x_number_of_panels.text = "13"
    x_panel_distribution = ET.SubElement(section,"x_panel_distribution")
    x_panel_distribution.text = "COSINE"
    y_number_of_panels = ET.SubElement(section,"y_number_of_panels")
    y_number_of_panels.text = "5"
    y_panel_distribution = ET.SubElement(section,"y_panel_distribution")
    x_panel_distribution.text = "INVERSE SINE"
    left_side_foil_name = ET.SubElement(section,"Left_Side_FoilName")
    left_side_foil_name.text = foilName
    right_side_foil_name = ET.SubElement(section,"Right_Side_FoilName")
    right_side_foil_name.text = foilName



xml_string = ET.tostring(root, encoding="utf-8")
parsed_xml = minidom.parseString(xml_string)
pretty_xml = parsed_xml.toprettyxml(indent="    ")  


with open("wing_data.xml", "w", encoding="utf-8") as file:
    file.write(pretty_xml)