'''
Created on 2 feb 2017

@author: TGU
'''
import cast_upgrades.cast_upgrade_1_5_16 # @UnusedImport

from cast.application import ApplicationLevelExtension, ReferenceFinder, create_link
import logging

class TilesApplication(ApplicationLevelExtension):

    def __init__(self):      
        self.jsp = {} 
        self.tilesDef = {}
        self.tilesDefWebapp = {}
        self.tilesPutAtt = {}
        self.tilesPutAttWebapp = {}        
        
    def end_application(self, application):
        self.global_nb_links = 0 
        self.deployFolder = (application.get_managment_base().get_deploy_path()).replace("\\", "/") 
        logging.info('deployPath  = ' + self.deployFolder)


        self.JSP_List(application)
        
        # tests lines 
        #file_full_name = "C:\\CASTMSdvptextensions\\Deploy\\CPP2017\\mapi\\mapi\\mapi\\administration\\src\\main\\webapp\\WEB-INF\\tiles\\structure\\modifier\\tiles-modifier.xml" 
        #file_full_name = "C:\\CASTMSAIFECPP2017\\Deploy\\CPP2017\\My Package\\mapi\\administration\\src\\main\\webapp\\WEB-INF\\tiles\\utilisateur\\tiles-utilisateur.xml"
        #self.display_XMLTiles_files(application, file_full_name)
        # end tests lines  
        
        self.ApacheTilesDefinitionList(application)
        self.ApacheTilesDefinitionWebappList(application)
        self.ApacheTilesPutAttributeList(application)                        
        self.ApacheTilesPutAttributeWebappList(application)                
        self.callLinkFromTilesDefToTilesAttribute(application)
        
        self.links_from_Tiles_to_JSP(application)
        self.links_from_JSP_to_Tiles(application)
        
        logging.info("Nb of links created globally : " + str(self.global_nb_links)) 
        

    def JSP_List(self, application): 
           
        for o in application.get_files(['CAST_Web_File']): 
            
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            
            if (not o.get_path().lower().endswith('.jsp')) and (not o.get_path().lower().endswith('.jspx')): # check if JSP file
                continue
            
            if not ('webapp') in o.get_path():            # check webapp in JSP name 
                logging.info("jsp_name without webapp = " + str(o.get_fullname()))
                continue
            
            jsp_name = str(o.get_fullname()).split('webapp')[1].replace(']', '').replace('\\', '/')
            jsp_name = jsp_name.replace('.jspx', '').replace('.jsp', '') # delete the file extension 
            #logging.info("jsp_name = [" + jsp_name + "]") 
            self.jsp[jsp_name] = o    
    
    def ApacheTilesDefinitionList(self, application):
    
        nb_TilesDef = 0 
        for tilesDef in application.objects().has_type('TilesDefinition'):     
            tilesDef_full_name = tilesDef.get_fullname()
            #logging.info("tilesDefinition Name = [" + tilesDef_full_name + "]") 
            self.tilesDef[tilesDef_full_name] = tilesDef 
            nb_TilesDef += 1
            
        logging.debug("Nb of Tiles Definitions : " + str(nb_TilesDef))        
 
    def ApacheTilesDefinitionWebappList(self, application):
    
        nb_TilesDef = 0 
        for tilesDef in application.objects().has_type('TilesDefinition'):     
            tilesDef_name = tilesDef.get_name()
            #logging.info("tilesDefinition Name = [" + tilesDef_name + "]") 
            webapp = self.webapp_container(tilesDef) 
            #logging.info("tilesDefinition Name = [" + webapp + "#" + tilesDef_name + "]") 
            self.tilesDefWebapp[webapp + "#" + tilesDef_name] = tilesDef 
            nb_TilesDef += 1
            
        logging.debug("Nb of Tiles Definitions : " + str(nb_TilesDef))                 
 
    def ApacheTilesPutAttributeList(self, application):
    
        nb_putAtt = 0 
        for putAtt in application.objects().has_type('TilesAttribute'):     
            putAtt_name = putAtt.get_name()
            #logging.info("Put-Attribute Name = [" + putAtt_name + "]") 
            self.tilesPutAtt[putAtt_name] = putAtt 
            nb_putAtt += 1
            
        logging.debug("Nb of Tiles Put-Attribute : " + str(nb_putAtt))      
 
 
    def ApacheTilesPutAttributeWebappList(self, application):
    
        nb_putAtt = 0 
        for putAtt in application.objects().has_type('TilesAttribute'):     
            putAtt_name = putAtt.get_name()
            #logging.info("Put-Attribute Name = [" + putAtt_name + "]") 
            webapp = self.webapp_container(putAtt) 
            #logging.info("Put-Attribute Name = [" + webapp + "#" + putAtt_name + "]") 
            self.tilesPutAttWebapp[webapp + "#" + putAtt_name] = putAtt 
            nb_putAtt += 1
            
        logging.debug("Nb of Put-Attribute Definitions : " + str(nb_putAtt))              
                       
    def callLinkFromTilesDefToTilesAttribute(self, application): 
        
        nb_TilesAttribute = 0 
        nb_links = 0 
        
        for tilesAttribute in application.objects().has_type('TilesAttribute'):
            nb_TilesAttribute += 1     
            # find the parent of the object 
            #tilesDef_fullname = '.'.join(tilesAttribute.get_fullname().split('.')[:-1])
            tilesDef_fullname =  tilesAttribute.get_fullname()[:-(len(tilesAttribute.get_name())+1)]
            
            #logging.info("tilesAttribute full Name = [" + str(tilesAttribute.get_fullname()) + "]") 
            #logging.info("tilesDefinition full Name = [" + tilesDef_fullname + "]") 
            if tilesDef_fullname in self.tilesDef: 
                tilesDef = self.tilesDef[tilesDef_fullname]
                #logging.info(" Creating call link between tileDef = [" + tilesDef_fullname + "] and TilesAttribute = [" + str(tilesAttribute.get_fullname()) + "]") 
                create_link('callLink', tilesDef, tilesAttribute)
                nb_links += 1
            else: 
                logging.info(" Did not find the Tiles Definition parent of the TilesAttribute = [" + str(tilesAttribute) + "]")
                logging.info(" Full name of the Tiles Definition not found = [" + tilesDef_fullname + "]")
                
        logging.debug("Nb of Tiles Attributes : " + str(nb_TilesAttribute))                        
        logging.debug("Nb of call links created between Tiles Definitions and Tiles Attributes : " + str(nb_links))        
                
    def links_from_Tiles_to_JSP(self, application):
        
        nb_links = 0 
        
        #for tilesDef in application.search_objects(category='TilesDefinition', load_properties=True):
        for tilesDef in application.objects().has_type('TilesDefinition').load_property('TilesDefinition.definition_template'):     
            # check if file is analyzed source code, or if it generated (Unknown)

            logging.info("tilesDefinition Name1 = " + tilesDef.get_name()) 
            jspTarget_name = tilesDef.get_property('TilesDefinition.definition_template') 
            if not jspTarget_name == None: 
                logging.info("jsp target name = [" + str(jspTarget_name) + "]") 
                jspTarget_name = jspTarget_name.replace('.jspx', '').replace('.jsp', '')
                logging.info("jsp target name = [" + str(jspTarget_name) + "]") 
                try: 
                    create_link('callLink', tilesDef, self.jsp[jspTarget_name])
                    nb_links += 1 
                except KeyError: 
                    logging.info("jsp or jspx not found")
        
        logging.debug("Nb of links created between Tiles definition tags and JSP : " + str(nb_links))        
        self.global_nb_links = self.global_nb_links + nb_links    
        
        nb_links = 0 

        for tilesDef in application.objects().has_type('TilesDefinition').load_property('TilesDefinition.definition_extends'):     
            # check if file is analyzed source code, or if it generated (Unknown)

            logging.info("tilesDefinition Name2 = " + tilesDef.get_name()) 
            tilesDef_webapp = self.webapp_container(tilesDef)      
            logging.info("tilesDefinition Webapp = " + str(tilesDef_webapp)) 
            tilesDefTarget_name = tilesDef.get_property('TilesDefinition.definition_extends')
            logging.info("TilesDefinition target = [" + str(tilesDefTarget_name) + "]") 

            # Searching in TilesDefinition 
            if (tilesDef_webapp + "#" + tilesDefTarget_name.replace("\\", "/") ) in self.tilesDefWebapp: 
                target = self.tilesDefWebapp[tilesDef_webapp + "#" + tilesDefTarget_name.replace("\\", "/") ]
                logging.debug("target tilesDef = [" + str(target) + "]") 
                create_link('callLink', tilesDef, target) 
                nb_links += 1 


        logging.debug("Nb of links created between Tiles definition tags and another Tiles Definition : " + str(nb_links))        
        self.global_nb_links = self.global_nb_links + nb_links  
           
        nb_links = 0 
        nb_links2 = 0 
            
        #for putAtt in application.search_objects(category='TilesAttribute', load_properties=True):
        for putAtt in application.objects().has_type('TilesAttribute').load_property('TilesAttribute.put_attribute_value'):     
            # check if file is analyzed source code, or if it generated (Unknown)

            logging.info("TilesAttribute Name = " + putAtt.get_name()) 
            put_attribute_value = putAtt.get_property('TilesAttribute.put_attribute_value')
            logging.info("TilesAttribute Value = [" + str(put_attribute_value) + ']') 
            if put_attribute_value is None:
                logging.info("TilesAttribute Value is null") 
            if not put_attribute_value is None: 
                if put_attribute_value.endswith('.jsp') or put_attribute_value.endswith('.jspx'):  # link to a JSP 
                    jspTarget_name = put_attribute_value
                    jspTarget_name = jspTarget_name.replace('.jspx', '').replace('.jsp', '')
                    logging.info("jsp(x) target = [" + str(jspTarget_name) + "] should be called from [" + str(putAtt) + "]") 
                    try: 
                        create_link('callLink', putAtt, self.jsp[jspTarget_name])    
                        nb_links += 1 
                    except KeyError: 
                        logging.info("jsp not found")
                if (not put_attribute_value.endswith('.jsp')) and (not put_attribute_value.endswith('.jspx')):    # link to a Tiles Definition 
                    tilesDef_target = put_attribute_value 
                    logging.info("Tiles Definition target = [" + str(tilesDef_target) + "]") 
                    
                    
                    tiles_webapp = self.webapp_container(putAtt)      
                                    
                    # Searching in TilesDefinition 
                    if (tiles_webapp + "#" + tilesDef_target.replace("\\", "/") ) in self.tilesDefWebapp: 
                        logging.info("**** Tiles Definition target found") 
                        target = self.tilesDefWebapp[tiles_webapp + "#" + tilesDef_target.replace("\\", "/")]
                        logging.debug("target tiles = [" + str(target) + "]") 
                        create_link('callLink', putAtt, target) 
                        nb_links2 += 1 

        logging.debug("Nb of links created between Tiles put-attribute tags and JSP : " + str(nb_links))  
        logging.debug("Nb of links created between Tiles put-attribute tags and Definition tag : " + str(nb_links2))  
        self.global_nb_links = self.global_nb_links + nb_links + nb_links2        
        
    def links_from_JSP_to_Tiles(self, application):
        nb_links = 0 
        nb_links2 = 0 
        nb_links3 = 0 
        nb_notfound = 0 
        
        logging.info("==> solves the following problem : Missing links between JSP and Tiles")    

        # 1. search all references in all files
 
        logging.info("Scanning jsp and jspx files for calls to Tiles tags")
                        
        # 2. scan each JSP file 
        # we search a pattern
        jsp_access = ReferenceFinder()
        jsp_access.add_pattern("Mapping", before="tiles:insertAttribute", element="[ \n\r\t]+name[ \n\r\t]*\=[ \n\r\t]*[A-Za-z0-9\=_\-\.\" ]+", after="")
 
        links = []
        
        # iterate all objects of the application     
        for o in application.get_files(['CAST_Web_File']): 

            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
                    
            if (not o.get_path().lower().endswith('.jsp')) and (not o.get_path().lower().endswith('.jspx')): # check if JSP file
                continue
            
            #logging.debug("JSP name = [" + o.get_path() + "]") 
            jsp_webapp = self.webapp_container(o)      
            #logging.debug("JSP webapp = [" + jsp_webapp + "]") 
            
            for reference in jsp_access.find_references_in_file(o):
                #logging.debug("Reference [" + reference.value + "]")      
                
                # manipulate the reference pattern found
                if not 'name=\"' in reference.value:
                    continue
                searched_tiles_tag_name = reference.value.split("\"")[1] 
                #logging.debug("searching [" + searched_tiles_tag_name + "]")
                #logging.debug('searching [' + jsp_webapp + '#' + searched_tiles_tag_name.replace("\\", "/") + ']')
                
                # Searching in TilesDefinition 
                if (jsp_webapp + "#" + searched_tiles_tag_name.replace("\\", "/") ) in self.tilesDefWebapp: 
                    target = self.tilesDefWebapp[jsp_webapp + "#" + searched_tiles_tag_name.replace("\\", "/") ]
                    #logging.debug("target tilesDef = [" + str(target) + "]") 
                    create_link('callLink', o, target) 
                    nb_links += 1 
                # Searching in Put-attribute  
                elif (jsp_webapp + "#" + searched_tiles_tag_name.replace("\\", "/") ) in self.tilesPutAttWebapp: 
                    target = self.tilesPutAttWebapp[jsp_webapp + "#" + searched_tiles_tag_name.replace("\\", "/") ]
                    #logging.debug("target put-attribute = [" + str(target) + "]") 
                    create_link('callLink', o, target) 
                    nb_links2 += 1
                else: 
                    logging.debug("target not a tilesDef neither of put-attribute in the same webapp as the JSP = [" + str(searched_tiles_tag_name) + "] search was [" + jsp_webapp + "#" + searched_tiles_tag_name.replace("\\", "/")  + "]")
                    if searched_tiles_tag_name in self.tilesPutAtt:
                        target = self.tilesPutAtt[searched_tiles_tag_name]
                        logging.debug("creating a less targeted link : target tilesDef = [" + str(target) + "]") 
                        create_link('callLink', o, target) 
                        nb_links3 += 1 
                    else: 
                        logging.debug("no link created between the JSP and the tilesDef or put-attribute") 
                        nb_notfound += 1                       
                                           
        # 3. Create the links
        for link in links:
            logging.debug("Creating link between " + str(link[1]) + " and " + str(link[2]))
            create_link(*link)
            
                
        logging.debug("Nb of links created between JSP and Tiles Definition tags : " + str(nb_links))
        logging.debug("Nb of links created between JSP and Tiles put-attribute tags : " + str(nb_links2))
        logging.debug("Nb of links created between JSP and Tiles put-attribute tags without targeting the webapp: " + str(nb_links3))
        logging.debug("Nb of links not created between JSP and Tiles Definition or put-attribute tags : " + str(nb_notfound))
        
        self.global_nb_links = self.global_nb_links + nb_links + nb_links2 + nb_links3   


    def file_container(self, myObject):
        object_full_name = myObject.get_fullname()
        logging.info('Object full name = ' + object_full_name) 
        file_path = object_full_name.split(']')[0].replace('[', '')
        logging.info('Object file path = ' + file_path) 
        return file_path
        
    def webapp_container(self, myObject): 
        object_full_name = myObject.get_fullname()
        if '\\' in object_full_name: 
            object_full_name = object_full_name.replace("\\", "/")
        #logging.info('Object full name = ' + object_full_name) 
        webapp = object_full_name.split('WEB-INF')[0].replace('[', '')
        #logging.info('Object webapp  = ' + webapp) 
        webapp = webapp.replace(self.deployFolder, '')
        #logging.info('Object webapp  = [' + webapp + ']') 
        return webapp                    

        