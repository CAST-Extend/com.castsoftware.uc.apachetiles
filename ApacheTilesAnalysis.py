'''
Created on 2 feb 2017

@author: TGU
'''
import cast.analysers.jee
import logging
import xml.etree.ElementTree as ET
from cast.analysers import Bookmark
 
class TilesAnalysis(cast.analysers.jee.Extension):
 
    def __init__(self):
        self.NbApacheTilesTilesDefinitionCreated = 0
        self.NbApacheTilesPutAttributeCreated = 0 
        self.apacheTilesDefinition = {}
        self.apacheTilesPutAttribute = {}
 
    def start_analysis(self,options):
        
        #Save in the _local base the XML files 
        cast.analysers.log.info('Starting Tiles analysis')
        cast.analysers.log.info("=============== xpath tiles ") 
        options.handle_xml_with_xpath('/tiles-definitions') # Tiles definition files 
        
    def end_analysis(self):
        cast.analysers.log.info('Number of Apache Tiles Tiles Definition objects created : ' + str(self.NbApacheTilesTilesDefinitionCreated))
        cast.analysers.log.info('Number of Apache Tiles Put Attribute objects created : ' + str(self.NbApacheTilesPutAttributeCreated))
        
        
    def start_xml_file(self,file):
        
        xmlfilepath = file.get_path() 
        cast.analysers.log.info('Scanning XML file : ' + xmlfilepath)
               
        if not file.get_path() or len(xmlfilepath.strip()) == 0: 
            return      
        
        if "web.xml" in xmlfilepath or "pom.xml" in xmlfilepath:
            return     
        
        #if 'tiles-' in xmlfilepath: 
        self.analyseXMLTilesFile(xmlfilepath, file)
            
     
    def analyseXMLTilesFile(self, xmlfilepath, file):     
        
        cast.analysers.log.info('Scanning XML Tiles files for reference to JSP or JSPX : ' + xmlfilepath)

        tree = ET.parse(xmlfilepath)
        root = tree.getroot()         
    
        for definition in root.iter('definition'):
            cast.analysers.log.info('Reading the XML file : definition node')        # return a dictionary containing the elements 
            definition_name = definition.attrib.get("name")
            cast.analysers.log.info('Definition Name : ' + definition_name)
            definition_extends = definition.attrib.get("extends") 
            cast.analysers.log.info('Definition extends : ' + str(definition_extends))
            definition_template = definition.attrib.get("template") 
            cast.analysers.log.info('Definition template : ' + str(definition_template))
            
            if not (str(definition_template)).endswith('.jsp') and not (str(definition_template)).endswith('.jspx'): 
                logging.info('==> Skip this definition as it is not a jsp or jspx file')
                definition_template = ''
            
            if not definition_name in self.apacheTilesDefinition: 
                objectDefinition = cast.analysers.CustomObject()
                objectDefinition.set_name(definition_name)
                objectDefinition.set_type('TilesDefinition')
                objectDefinition.set_parent(file)
                objectDefinition.save()
                self.NbApacheTilesTilesDefinitionCreated += 1         
                bookmark = Bookmark(file, 1, 1, -1, -1) # TODO : find exact position 
                objectDefinition.save_position(bookmark)
                objectDefinition.save_property('TilesDefinition.definition_extends', str(definition_extends))
                objectDefinition.save_property('TilesDefinition.definition_template', str(definition_template))
                self.apacheTilesDefinition[definition_name] = objectDefinition 
            else: 
                cast.analysers.log.info('==== Definition [' + definition_name + '] already defined in the file ' + xmlfilepath) 
            
            for attribute in definition.iter('put-attribute'):
                cast.analysers.log.info('==== Reading the XML file : put-attribute node')        # return a dictionary containing the elements 
                put_attribute_name = attribute.attrib.get("name")
                cast.analysers.log.info('==== put_attribute Name : ' + put_attribute_name)
                put_attribute_value = attribute.attrib.get("value") 
                cast.analysers.log.info('==== put_attribute Value : ' + str(put_attribute_value))

                if not str(definition_name + "." + put_attribute_name) in self.apacheTilesPutAttribute: # to manage duplicate definition in xml files
                    objectPut_Attribute = cast.analysers.CustomObject()
                    objectPut_Attribute.set_name(put_attribute_name)
                    objectPut_Attribute.set_type('TilesAttribute')
                    objectPut_Attribute.set_parent(self.apacheTilesDefinition[definition_name])
                    objectPut_Attribute.save()
                    self.NbApacheTilesPutAttributeCreated +=1                 
                    bookmark = Bookmark(file, 1, 1, -1, -1) # TODO : find exact position 
                    objectPut_Attribute.save_position(bookmark)
                    objectPut_Attribute.save_property('TilesAttribute.put_attribute_value', str(put_attribute_value))
                    self.apacheTilesPutAttribute[str(definition_name + "." + put_attribute_name)] = attribute
                else: 
                    cast.analysers.log.info('==== put_attribute Value [' + put_attribute_name + '] already defined for the TilesDef [' + definition_name + ']')  
                
                
    def analyseXMLSpringWebFlowFile(self, xmlfilepath, file):        
        pass
