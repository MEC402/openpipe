# from webdav3.client import WebDavXmlUtils
# from webdav3.urn import Urn


# class TestApp(unittest.TestCase):
#
#     @classmethod
#     # def testInsertCollection(self):
#     #     result=BL().insertIntoCollection('test')
#
#     # def testInsertMetaTag(self):
#     #     mt={"openpipe_canonical_id": "124256"
#     #     ,"openpipe_canonical_title": "Lion on the Watch"
#     #     ,"openpipe_canonical_source": "Cleveland"
#     #     ,"openpipe_canonical_largeImage": "https://openaccess-cdn.clevelandart.org/1945.25/1945.25_print.jpg"
#     #     ,"openpipe_canonical_largeImageDimensions": "3400,2439"
#     #     ,"openpipe_canonical_smallImage": "https://openaccess-cdn.clevelandart.org/1945.25/1945.25_web.jpg"
#     #     ,"openpipe_canonical_smallImageDimensions": "1245,893"
#     #     ,'openpipe_canonical_artist': "Jean-Léon Gérôme (French, 1824-1904)"
#     #     ,'openpipe_canonical_culture': "France, 19th century"
#     #     ,'openpipe_canonical_classification': "OpenPipe"
#     #     ,'openpipe_canonical_genre': "art-fi"
#     #     ,'openpipe_canonical_medium': "OpenPipe Pixels"
#     #     ,'openpipe_canonical_nation': "OpenPipe People"
#     #     ,'openpipe_canonical_city': "OpenPipe City"
#     #     ,'openpipe_canonical_tags': "OpenPipeTag"
#     #     ,'openpipe_canonical_fullImage': "http://mec402.boisestate.edu/cgi-bin/assetSources/getClevelandConvertedTif.py?id=124256"
#     #     ,'openpipe_canonical_fullImageDimensions': "4000,3000"
#     #     ,'openpipe_canonical_date': "CE 1880 JAN 01 00:00:00"
#     #     ,'openpipe_canonical_firstDate': "CE 1880 JAN 01 00:00:00"
#     #     ,'openpipe_canonical_lastDate': "CE 1890 JAN 01 00:00:00"
#     #     ,'id': "124256"
#     #     ,'accession_number': "1945.25"
#     #     ,'share_license_status': "CC0"
#     #     ,'tombstone': "Lion on the Watch, c. 1885. Jean-Léon Gérôme (French, 1824-1904). Oil on wood panel; framed: 105 x 133 x 13.5 cm (41 5/16 x 52 3/8 x 5 5/16 in.); unframed: 72.3 x 100.5 cm (28 7/16 x 39 9/16 in.). The Cleveland Museum of Art, Gift of Mrs. F. W. Gehring in memory of her husband, F. W. Gehring 1945.25"
#     #     ,'current_location': "null"
#     #     ,'title': "Lion on the Watch"
#     #     ,'title_in_original_language': "null"
#     #     ,'series': "null"
#     #     ,'series_in_original_language': "null"
#     #     ,'creation_date': "c. 1885"
#     #     ,'creation_date_earliest': "1880"
#     #     ,'creation_date_latest': "1890"
#     #     ,'creators': "[{description:Jean-Léon Gérôme (French, 1824-1904),extent:null,qualifier:null,role:artist,biography:Born in Vesoul near the Swiss border, Jean-Léon Gérôme grew up in comfort. His goldsmith father approved of his decision to become an artist and supported his study in Paris with Delaroche (q.v.) during the early 1840s. Delaroches interest in historical reconstruction, precise detail, and smooth picture surface had a significant effect on the young student. After failing to win the Prix de Rome in 1846, which his father pressured him to enter, Gérôme decided to make his name at the Salons. His debut there in 1847 with A Cock Fight (Musée dOrsay, Paris) was a huge success and brought him and his fellow neo-Grecs, as they were called, much attention. Several important commissions and purchases followed, including church decoration and the huge historical picture The Age of Augustus (Musée dOrsay, Paris) that emulated the kind of classicizing panorama of Delaroche in the hemicycle for the École des Beaux-Arts. Gérôme also studied briefly with Charles Gleyre (1808-1874) after Delaroche closed his studio in 1842. Gleyres travel and sketches from the Near and Middle East may also have played a critical role in introducing the young artist to another major interest of his career, orientalist subject matter. With the twenty thousand francs paid for The Age of Augustus, the artist treated himself to a trip to Constantinople with his actor-friend Edmond Got. Further travels to the Middle East followed, and Gérôme exhibited his first Egyptian themes in the 1857 Salon. \r\nIn the 1878 Universal Exposition in Paris, he exhibited his first attempts at sculpture, which corresponded closely with his painted works, first following their themes, then serving as models for his canvases, especially the Pygmalion pictures. During the 1880s he was, like several other artists, drawn to incorporate polychromy and various precious and semi-precious materials into his sculpture; this was known to be a widespread practice among ancient sculptors, and it heightened the illusion of lifelikeness as well as the decorative aspect of these works. \r\nAlthough he had not succeeded at the École des Beaux-Arts, Gérôme received one of three prestigious professorships in 1863 following the somewhat controversial reforms of the fine arts institutions in Paris. His official rather than academic achievements made him a good candidate to lead the new generation of French painters out of the decadence into which many believed French art had fallen. He taught hundreds of students in his atelier at the École as well as at his independent studio and had an especially strong impact on his American students, such as Thomas Eakins (1844-1916) and Frederick Arthur Bridgman (1847-1928). Although the majority of Gérômes students remember him as an exacting but fair master, he showed intractable resistance to the new modes of impressionism and symbolism and campaigned against the acceptance of Gustave Caillebottes (1843-1893) bequest of such art to the French state. \r\nIn 1863 Gérôme married Marie Goupil, the daughter of well-known international art dealer Adolphe Goupil, who became the exclusive representative of his work. Goupil not only sold his son-in-laws pictures through his branches in Europe and New York, but he also disseminated their reputation through photographic reproductions.1 Gérôme received all the highest honors awarded to nineteenth-century artists and achieved considerable financial success.\r\n1. See Linda Whiteley, \Goupil, (Jean-Michel-) Adolphe,\ Dictionary of Art (London, 1996), 13:228; and Musée Goupil, Conservatoire de Limage Industrielle Bordeaux, État des lieux 1 (Bordeaux, 1994), esp. 9-36.,name_in_original_language:null,birth_year:1824,death_year:1904}]"
#     #     ,'culture': "[France, 19th century]"
#     #     ,'technique': "oil on wood panel"
#     #     ,'support_materials': "[]"
#     #     ,'department': "Modern European Painting and Sculpture"
#     #     ,'collection': "Mod Euro - Painting 1800-1960"
#     #     ,'type': "Painting"
#     #     ,'measurements': "Framed: 105 x 133 x 13.5 cm (41 5/16 x 52 3/8 x 5 5/16 in.); Unframed: 72.3 x 100.5 cm (28 7/16 x 39 9/16 in.)"
#     #     ,'dimensions': "{framed:{height:1.05,width:1.33,depth:0.135},unframed:{height:0.723,width:1.005}}"
#     #     ,'state_of_the_work': "null"
#     #     ,'edition_of_the_work': "null"
#     #     ,'creditline': "Gift of Mrs. F. W. Gehring in memory of her husband, F. W. Gehring"
#     #     ,'copyright': "null"
#     #     ,'inscriptions': "[{inscription:Signed lower left: j. l. gerome\r\n\r\n,inscription_translation:null,inscription_remark:null}]"
#     #     ,'exhibitions': "{current:[{title:Baron Gros, Painter of Battles: The First Romantic Painter,description:<i>Baron Gros, Painter of Battles: The First Romantic Painter</i>. The Cleveland Museum of Art, Cleveland, OH (organizer) (March 8-April 15, 1956).,opening_date:1956-03-08T05:00:00},{title:Animals as Romantic Icons in French Art,description:<i>Animals as Romantic Icons in French Art</i>. The Cleveland Museum of Art, Cleveland, OH (organizer) (April 6-July 27, 1986).,opening_date:1986-04-06T04:00:00},{title:Jean-Léon Gérôme,description:<i>Jean-Léon Gérôme</i>. J. Paul Getty Museum (June 15-September 12, 2010); Musée dOrsay (organizer) (October 18, 2010-January 23, 2011).,opening_date:2010-06-15T00:00:00}],legacy:[Dayton Art Institute; Minneapolis Institute of Arts; Baltimore, Walters Art Gallery. Jean-Léon Gérôme 1824-1904 (1972-73), no. 35 (repr.).<br>J. Paul Getty Museum, Los Angeles (6/15/2010 - 9/12/2010) and Musée dOrsay, Paris (10/18/2010 - 1/23/2011):  \Jean-Léon Gérôme\]}"
#     #     ,'provenance': "[{description:Frederick Gehring, Cleveland. Given to the CMA in 1945.,citations:[],footnotes:null,date:null}]"
#     #     ,'find_spot': "null"
#     #     ,'related_works': "[]"
#     #     ,'fun_fact': "null"
#     #     ,'digital_description': "null"
#     #     ,'wall_description': "In addition to his fascination with the classical past, Gérôme was one of the leading painters of \orientalist\ subjects-exotic and romantic themes inspired by Napoleonic adventures abroad, romantic literature, and European colonialism. From 1855, Gérôme travelled regularly in Turkey, Egypt, and Asia Minor. Long fascinated by African animals, he sketched lions in the Paris zoo as a student and later hunted them on safari in North Africa."
#     #     ,'citations': "[{citation:Ackerman, Gerald M. <em>Jean-Léon Gérôme: monographie révisée, catalogue raisonné mis à jour</em>. Courbevoie: ACR, 2000.,page_number:Reproduced and mentioned: pp. 372-373, cat. 529,url:null}]"
#     #     ,'catalogue_raisonne': "null"
#     #     ,'url': "https://clevelandart.org/art/1945.25"
#     #     ,'images': "{web:{url:https://openaccess-cdn.clevelandart.org/1945.25/1945.25_web.jpg,filename:1945.25_web.jpg,filesize:703311,width:1245,height:893},print:{url:https://openaccess-cdn.clevelandart.org/1945.25/1945.25_print.jpg,filename:1945.25_print.jpg,filesize:5052714,width:3400,height:2439},full:{url:https://openaccess-cdn.clevelandart.org/1945.25/1945.25_full.tif,filename:1945.25_full.tif,filesize:75060664,width:5904,height:4236}}"
#     #     ,'updated_at': "2019-11-25 09:04:20.151000"
#     #     ,'metaDataId': '2'}
#     #
#     #     mt2={'openpipe_canonical_id': '135428', 'openpipe_canonical_title': 'Hunting near Hartenfels Castle', 'openpipe_canonical_source': 'Cleveland', 'openpipe_canonical_largeImage': 'https://openaccess-cdn.clevelandart.org/1958.425/1958.425_print.jpg', 'openpipe_canonical_largeImageDimensions': '3400,2332', 'openpipe_canonical_smallImage': 'https://openaccess-cdn.clevelandart.org/1958.425/1958.425_web.jpg', 'openpipe_canonical_smallImageDimensions': '1263,866', 'openpipe_canonical_artist': 'Lucas Cranach (German, 1472-1553)', 'openpipe_canonical_culture': 'Germany, 16th century', 'openpipe_canonical_classification': 'OpenPipe', 'openpipe_canonical_genre': 'art-fi', 'openpipe_canonical_medium': 'OpenPipe Pixels', 'openpipe_canonical_nation': 'OpenPipe People', 'openpipe_canonical_city': 'OpenPipe City', 'openpipe_canonical_tags': 'OpenPipeTag', 'openpipe_canonical_fullImage': 'http://mec402.boisestate.edu/cgi-bin/assetSources/getClevelandConvertedTif.py?id=135428', 'openpipe_canonical_fullImageDimensions': '4000,3000', 'openpipe_canonical_date': 'CE 1540 JAN 01 00:00:00', 'openpipe_canonical_firstDate': 'CE 1540 JAN 01 00:00:00', 'openpipe_canonical_lastDate': 'CE 1540 JAN 01 00:00:00', 'id': '135428', 'accession_number': '1958.425', 'share_license_status': 'CC0', 'tombstone': 'Hunting near Hartenfels Castle, 1540. Lucas Cranach (German, 1472-1553). Oil, originally on wood, transferred to masonite; framed: 133 x 185.5 x 7.3 cm (52 3/8 x 73 1/16 x 2 7/8 in.); unframed: 116.8 x 170.2 cm (46 x 67 in.). The Cleveland Museum of Art, John L. Severance Fund 1958.425', 'current_location': '114 Late Northern Renaissance', 'title': 'Hunting near Hartenfels Castle', 'title_in_original_language': 'null', 'series': 'null', 'series_in_original_language': 'null', 'creation_date': '1540', 'creation_date_earliest': '1540', 'creation_date_latest': '1540', 'creators': '[{description:Lucas Cranach (German, 1472-1553),extent:null,qualifier:null,role:artist,biography:null,name_in_original_language:null,birth_year:1472,death_year:1553}]', 'culture': '[Germany, 16th century]', 'technique': 'oil, originally on wood, transferred to masonite', 'support_materials': '[]', 'department': 'European Painting and Sculpture', 'collection': 'P - German before 1800', 'type': 'Painting', 'measurements': 'Framed: 133 x 185.5 x 7.3 cm (52 3/8 x 73 1/16 x 2 7/8 in.); Unframed: 116.8 x 170.2 cm (46 x 67 in.)', 'dimensions': '{framed:{height:1.33,width:1.855,depth:0.073},unframed:{height:1.168,width:1.702}}', 'state_of_the_work': 'null', 'edition_of_the_work': 'null', 'creditline': 'John L. Severance Fund', 'copyright': 'null', 'inscriptions': '[{inscription:Signed lower right on boat with a winged serpent, and dated: 1540 [inventory number, lower right: 1577],inscription_translation:null,inscription_remark:null}]', 'exhibitions': '{current:[{title:Juxtapositions,description:<i>Juxtapositions</i>. The Cleveland Museum of Art (September 11-October 10, 1965).,opening_date:1965-09-11T04:00:00},{title:A Cleveland Bestiary,description:<i>A Cleveland Bestiary</i>. The Cleveland Museum of Art (organizer) (October 14-December 16, 1981).,opening_date:1981-10-14T04:00:00},{title:Visions of Landscape: East and West,description:<i>Visions of Landscape: East and West</i>. The Cleveland Museum of Art (organizer) (February 17-March 21, 1982).,opening_date:1982-02-17T05:00:00},{title:Sacred Gifts and Worldly Treasures: Medieval Masterworks from the Cleveland Museum of Art,description:<i>Sacred Gifts and Worldly Treasures: Medieval Masterworks from the Cleveland Museum of Art</i>. National Museum of Bavaria, Munich, Germany (May 10-September 16, 2007); J. Paul Getty Museum (October 30, 2007-January 20, 2008); Frist Center for the Visual Arts (February 13-June 7, 2009).,opening_date:2007-05-10T00:00:00},{title:Lucas Cranach. Laltro rinascimento,description:<i>Lucas Cranach. Laltro rinascimento</i>. Galleria Borghese (organizer) (October 13, 2010-March 3, 2011).,opening_date:2010-10-13T00:00:00},{title:Luther and the Princes,description:<i>Luther and the Princes</i>. Schloss Hartenfels, Torgau, Germany (May 15-November 1, 2015).,opening_date:2015-05-15T00:00:00}],legacy:[<em>Lucas Cranach d. A und Lucas Cranach d. J</em>. Staatliche Museen (duetsches Museum) Berlin, Germany (1937).,<em>Faith and Power: Saxony in the Europe of the Reformation Era</em>. Hartenfels Castle, Torgau, Germany (May 24-October 10, 2004).,<em>Arms and Armor from Imperial Austria</em>. The Cleveland Museum of Art (organizer) Cleveland, OH (February 24-June 1, 2008).]}', 'provenance': '[{description:The Cleveland Museum of Art, Cleveland, Ohio,citations:[],footnotes:null,date:1958-},{description:(M.H. Drey, London, sold to the Cleveland Museum of Art),citations:[{citation:Margaret H. Drey, letter to Henry Sayles Francis, April 9, 1959, in CMA curatorial file.,page_number:null,url:null},{citation:Margaret H. Drey, letter to Henry Sayles Francis, March 18, 1959, in CMA curatorial file.,page_number:null,url:null}],footnotes:null,date:Until 1958},{description:Royal Collection of Saxony, Schloss Hartenfels and Schloss Moritzburg, consigned to M.H. Drey1,citations:[{citation:Margaret H. Drey, letter to Henry Sayles Francis, March 18, 1959, in CMA curatorial file.<br><br><!--block-->,page_number:null,url:null},{citation:Margaret H. Drey, letter to Henry Sayles Francis, April 9, 1959, in CMA curatorial file.,page_number:null,url:null},{citation:<em>Cranach-Ausstellung: Lucas Cranach d. \udcc3\udc84., und Lucas Cranach d. J., Gem\udcc3\udca4lde, Zeichnungen, Graphik, april-juni 1937 im Deutschen Museum Berlin</em>. Berlin: Staatliche Museen, 1937.,page_number:null,url:null},{citation:Schade, Werner, Lucas Cranach, Lucas Cranach, and Hans Cranach. <em>Cranach, a Family of Master Painters</em>. New York: Putnam, 1980.,page_number:null,url:null},{citation:Schuchardt, Christian. <em>Lucas Cranach des Aeltern leben und werke</em>. Leipzig: F.A. Brockhaus, 1851.,page_number:null,url:null}],footnotes:[On October 4, 1543, Cranach was paid 123 florins, 10 groschen, and 8 pfennig for various works (Staatsarchiv, Weimar Reg. Bb. 4551, Bl. 24b (Schuchardt [1851] 162ff.), including a hunting picture presented to Duke Maurice of Saxony [1521-1553], presumably the Cleveland painting. Cranach had been appointed court painter to the Electors of Saxony in 1505 by Frederick the Wise.  A House of Saxony inventory number (1577) is inscribed in the lower right corner of the painting. The painting remained at Schloss Hartenfels, Torgau for generations, and with the Dukes of Saxony at Schloss Moritzburg until the 1950s.],date:1540-1950s}]', 'find_spot': 'null', 'related_works': '[]', 'fun_fact': 'Humans, dogs, and deer make up most of the creatures in this busy scene\udce2\udc80\udc94but not all of them! Look closely at the background to spot a bear and three boars.', 'digital_description': 'null', 'wall_description': 'The Protestant rulers of Saxony commissioned this animated hunt scene, set near their residence seen in the background, Hartenfels Castle (in eastern Germany). John Frederick the Magnanimous, in the bottom left corner, wears dark green hunting attire; he spans his crossbow and waits for his courtiers and dogs to chase a stag across the river. His wife, the Electress Sibylle, stands at right, poised to take the first ceremonial shot. The prince electors of Saxony were passionate practitioners of hunting with dogs\udce2\udc80\udc94elaborate, highly rehearsed occasions, coordinated by the use of signals from hunting horns. Cranach dated this work and his signature is the winged snake at lower right. 1577 in the right corner is an inventory number.', 'citations': '[{citation:Flechsig, Eduard. <em>Cranachstudien</em>. Leipzig, Germany: K.W. Hiersemann, 1900.,page_number:Reproduced: p. 275; Mentioned: p. 288,url:null},{citation:Friedla\udccc\udc88nder, Max J., and Jakob Rosenberg. <em>Die Gema\udccc\udc88lde von Lucas Cranach</em>. Berlin, Germany: Deutscher Verein fu\udccc\udc88r Kunstwissenschaft, 1932.,page_number:Reproduced: no. 331a, p. 91,url:null},{citation:Lilienfein, Heinrich. <em>Lukas Cranach und seine Zeit</em>. Bielefeld, Germany: Velhagen &amp; Klasing, 1944.,page_number:Reproduced: p. 86,url:null},{citation:Kunsthistorisches Museum Wien, Vinzenz Oberhammer, Friderike Klauner, and Gu\udccc\udc88nther Heinz. <em>Katalog der Gema\udccc\udc88ldegalerie</em>. Wien, Austria: Kunsthistorisches Museum, 1958.,page_number:Reproduced: p. 39, no. 117,url:null},{citation:Francis, Henry S. \\The Stag Hunt by Lucas Cranach the Elder and Lucas Cranach the Younger.\\ <em>The Bulletin of The Cleveland Museum of Art XLVI,</em> no. 10 (November, 1959):198-205.,page_number:Reproduced: p. 198-199, fig. 1,url:null},{citation:The Cleveland Museum of Art. <em>Handbook of the Cleveland Museum of Art/1966</em>. Cleveland, OH: The Cleveland Museum of Art, 1966.,page_number:Reproduced: p. 108,url:https://archive.org/details/CMAHandbook1966/page/n132},{citation:The Cleveland Museum of Art. <em>Handbook of the Cleveland Museum of Art/1969</em>. Cleveland, OH: The Cleveland Museum of Art, 1969.,page_number:Reproduced: p. 108,url:https://archive.org/details/CMAHandbook1969/page/n132},{citation:Schu\udccc\udc88tz, Karl. <em>Lucas Cranach der A\udccc\udc88ltere und seine Werkstatt. Jubila\udccc\udc88umsausstellung museumseigener Werke, 1472-1972</em>. Wien, Austria: Kunsthist. Museum, 1972.,page_number:Reproduced: p. 32,url:null},{citation:Museo del Prado. <em>Museo del Prado: cata\udccc\udc81logo de las pinturas</em>. Madrid, Spain: El Museo, 1972.,page_number:Reproduced: 0. 165, no. 2175,url:null},{citation:Lurie, Ann T. <em>The Cleveland Museum of Art Catalogue of Paintings</em>. Cleveland, OH: The Museum, 1982.,page_number:Mentioned: p. 162-165; Reproduced: p. 163,url:null},{citation:Schade, Werner. <em>Die Malerfamilie Cranach</em>. Dresden, Germany: Verlag der Kunst, 1974.,page_number:Reproduced: p. 210 and 211,url:null},{citation:Findeisen, Peter, and Heinrich Magirius. <em>Die Denkmale der Stadt Torgau</em>. Leipzig, Germany: Seemann, VEB, 1976.,page_number:Reproduced: p. 108-109, plates 64, 65,url:null},{citation:The Cleveland Museum of Art. <em>Handbook of the Cleveland Museum of Art/1978</em>. Cleveland, OH: The Cleveland Museum of Art, 1978.,page_number:Reproduced: p. 128,url:https://archive.org/details/CMAHandbook1978/page/n148},{citation:Morse, John D. <em>Old Master Paintings in North America: Over 3000 Masterpieces by 50 Great Artists</em>. New York, NY: Abbeville Press, 1979.,page_number:Reproduced: p. 77,url:null},{citation:Kathman, Barbara A. <em>A Cleveland Bestiary</em>. Cleveland, OH; Cleveland Museum of Art, 1981.,page_number:Reproduced: p. 9; Mentioned: p. 7-11, p. 60,url:null},{citation:The Cleveland Museum of Art. <em>The Cleveland Museum of Art Catalogue of Paintings, Part 3: European Paintings of the 16th, 17th, and 18th Centuries. </em>Cleveland, OH: The Cleveland Museum of Art, 1982.,page_number:Mentioned: p. 162-164; Reproduced: p. 163,url:null},{citation:Weber, Erwin. <em>Cranach and Luther: With Selected Works of the \\Painting Evangelist\\ in the United States</em>. St. Louis, MO: Concordia Pub. House, 1983.,page_number:Reproduced: p. 60, plate 42,url:null},{citation:Grimm, Claus, Johannes Erichsen, and Evamaria Brockhoff. <em>Lucas Cranach: ein Maler-Unternehmer aus Franken</em>. Augsburg, Germany: Haus der Bayerischen Geschichte, 1994.,page_number:Reproduced: no. 131; Mentioned: p. 311-313,url:null},{citation:Fliegel, Stephen N. <em>Arms and Armor: The Cleveland Museum of Art</em>. Cleveland, OH: The Museum, 1998.,page_number:Reproduced: p. 135,url:null},{citation:Kolb, Karin, and Harald Marx. <em>Cranach: [anla\udccc\udc88sslich der Ausstellung Cranach vom 13. November 2005 bis 12. Ma\udccc\udc88rz 2006 in den Kunstsammlungen Chemnitz ; eine Ausstellung in Kooperation mit der Gema\udccc\udc88ldegalerie Alte Meister der Staatlichen Kunstsammlungen Dresden]</em>. Ko\udccc\udc88ln, Germany: Wienand, 2005.,page_number:Reproduced: p. 160, fig. 72,url:null},{citation:Ferino Pagden, Sylvia, and Andreas Beyer. <em>Tizian versus Seisenegger: die Portraits Karls V. mit Hund : ein Holbeinstreit</em>. Turnhout, Belgium: Brepols, 2005.,page_number:Mentioned: p. 169; Reproduced: p. 171, fig. 4a,url:null},{citation:Klein,  Holger A. <em>Sacred Gifts and Worldly Treasures: Medieval Masterworks from the Cleveland Museum of Art</em>. Cleveland, OH: Cleveland Museum of Art, 2007.,page_number:Reproduced: cat. 112, Mentioned: p. 294, 295,url:null},{citation:Fliegel, Stephen N. <em>Arms &amp; Armor: The Cleveland Museum of Art</em>. Cleveland, OH: Cleveland Museum of Art, 2007.,page_number:Reproduced: p. 155,url:null},{citation:<em>Treasures of the Cleveland Museum of Art</em>. London: United Kingdom: Scala Books, 2012.,page_number:Reproduced: p. 168-169,url:null},{citation:Greub, Suzanne. <em>Von Meisterhand: die Cranach-Sammlung des Muse\udccc\udc81e des beaux-arts de Reims</em>. Munich, Germany: Hirmer, 2015.,page_number:Mentioned and reproduced: P. 54-55, Abb. 6,url:null}]', 'catalogue_raisonne': 'null', 'url': 'https://clevelandart.org/art/1958.425', 'images': '{web:{url:https://openaccess-cdn.clevelandart.org/1958.425/1958.425_web.jpg,filename:1958.425_web.jpg,filesize:1094651,width:1263,height:866},print:{url:https://openaccess-cdn.clevelandart.org/1958.425/1958.425_print.jpg,filename:1958.425_print.jpg,filesize:7869098,width:3400,height:2332},full:{url:https://openaccess-cdn.clevelandart.org/1958.425/1958.425_full.tif,filename:1958.425_full.tif,filesize:51477396,width:5000,height:3430}}', 'updated_at': '2019-11-18 10:48:00.615000', 'metaDataId': 5074}
#     #     st=json.dumps(mt2)
#     #     j=json.loads(st)
#     #     BL().insertIntoMetaTags(st)
#
#     # def testDeleteFolderMember(self):
#     #     BL().deleteFolderMember(1,4)
#     #
#     # def testDeleteFolder(self):
#     #     BL().deleteFolder(1)
#
#     # def testUpdateMetaTag(self):
#     #     BL().updateMetaTag(1,'openpipe_canonical_genre','art-fi','openpipe_canonical_genre','horror')
#
#     # def testDeleteMetaTag(self):
#     #     BL().deleteMetaTag(1,'openpipe_canonical_classification','OpenPipe123')
#
#     # def testInsertMetaTag(self):
#     #     BL().insertMetaTag(1,'asd','asd')
#
#     # def testGuid(self):
#     #     print( BL().getGUIDInfo("asset",1))
#
#     # def testGetPublicAssets(cls):
#     #     print(BL().getPublicAsssetsInCollection(20,0,10));
#
#     # def testInsertIntoImages(cls):
#     #     assert (BL().insertIntoImages("aaa","aaa","")==3412)
#
from openpipeAPI.ORM.BL import BL


def testWebdav():
    from webdav3.client import Client

    print("Content-Type: text/html")
    print()

    print("<h1>help</h1>")
    options = {
            'webdav_hostname': "http://mec402.boisestate.edu/",
            'webdav_root': "webdav",
            'webdav_login': "openpipedev",
            'webdav_password': "openPipeArtMaster51",
            'verbose': True
            }
    client = Client(options)
    print(client.root)
    print(client.list())
    directory_urn = Urn(client.root, directory=True)
    response = client.execute_request(action='list', path=directory_urn.quote())
    urns = WebDavXmlUtils.parse_get_list_response(response.content)
    for u in urns[1:]:
        print(u.path())
        print(u.normalize_path(u.path()))
        print(u.quote())
    print(client.check("/cache/Rijks_SK-A-5009.jpg"))
    response = client.execute_request(action='check', path="/cache/Rijks_SK-A-5009.jpg")
    print(response)

    # response = client.execute_request(action='mkdir', path="/cache/test")
    # print(response)
    # client.upload_sync(remote_path="/user_assets/" + "164-next-level.png", local_path="164-next-level.png")

    with open("164-next-level.png", "rb") as local_file:
        client.execute_request(action='upload', path="/user_assets/a.png", data=local_file)


# testWebdav()

# import time
#
# t0 = time.time()
# res=BL().getAllAssets(1,100,'1990-01-01','5000-01-01')
# t1 = time.time()
#
# total = t1-t0
# print("total Time")
# print(total)
#
# print(res)

# BL().saveUploadAsset()

a="ABC"

print(a.lower())