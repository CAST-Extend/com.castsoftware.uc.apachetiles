# com.castsoftware.uc.apachetiles

# Apache Tiles Analyzer

# Introduction
The goal of this extension is to provide the support of Apache Tiles (https://tiles.apache.org/)  
Mostly for FP calculation usage. 
This extension has been built and tested against Apache Tiles 3.0.5 

# Additional type of objects bring by this extension

Objects being part of Tiles Metamodel : Tiles Definition, Tiles Attribute

![Tiles MetaModel](/ApacheTiles_MetaModel.jpg)


# Cases covered by this extension

The following cases are covered by the extension :
- creation of objects for Tiles Definition / Tiles Attribute 
- creation of Belong links from Tiles Definitions to Tiles Attribute 
- creation of links from Tiles Definition to other Tiles Definition (extends) 
- creation of Call links from Definition / Tiles Attribute to JSP 
- creation of Call links from JSP to Definition / Tiles Attribute to JSP 

# Sample graphical view 

![Tiles sample view in Enlighten](/ApacheTiles_sample_view_Enlighten.jpg)

# How to contribute

This technical package is deliver "as-is". It has been used in a limited number of situations. 
This package has been tested in CAST 8.1.x, 8.2,x

For bugs, feature requests, and contributions contact Thierry Guégan t.guegan@castsoftware.com. You may also send a thank you if you find this useful.
