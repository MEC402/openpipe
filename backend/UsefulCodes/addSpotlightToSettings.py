import json
import re

str="""1400-1600 World in Art 	guid: 200/133 		74 assets
Adoration of the Magi		guid: 200/158		34 assets
Africa					guid: 200/44		162 assets
American West			guid: 200/234		53 assets
Ancient Oaxaca			guid: 200/91		43 assets Animals Doing People Ths 	guid: 200/203		89 assets 
Architectural Interiors		guid: 200/165		37 assets 
Art and Social Change		guid: 200/221		21 assets
 Autumn					guid: 200/243		45 assets
Baroque					guid: 200/116 		68 assets 
Best Sellers of MAges		guid: 200/170		15 assets 
Birds of Prey				guid: 200/185		209 assets 
Blankets and Quilts		guid: 200/179		68 assets 
Blue					guid: 200/191		149 assets Botanical Prints			guid: 200/210		33 assets Brass & Percussion		guid: 200/244		54 assets 
Cats					guid: 200/41		45 assets Children in Art			guid: 200/241		5 assets+
Chinese Landscapes		guid: 200/68		36 assets
Crowning Jewels			guid: 200/143		49 assets 
Dance					guid: 200/233		55 assets
Dogs					guid: 200/59		48 assets 
Dr. Louis A. Peck			guid: 200/197		53 assets 
Drawing					guid: 200/193		158 assets 
Dress					guid: 200/22		815 assets
Dutch Golden Age			guid: 200/123		21 assets 
Early Islamic Texts and Textiles	guid: 200/215		27 assets 
Egypt's Pharaohs			guid: 200/63		39 assets 
Fantastic Beasts & Where to Find Them	
guid: 200/31		43 assets
Festive Feasts			guid: 200/81		36 assets 
Fifty-Three Stations of the Tokaido	
guid: 200/228		16 assets 
Gardens					guid: 200/86		86 assets 
Ghosts and the Afterlife	guid: 200/162		28 assets 
Gold					guid: 200/26		453 assets 
Grand Tour				guid: 200/187		25 assets 
Greek Vases				guid: 200/83		93 assets 
Halloween				guid: 200/105		65 assets
Hands					guid: 200/85		17 assets 
Horses					guid: 200/167		70 assets 
Hudson River School		guid: 200/152		68 assets 
Impasto					guid: 200/192		56 assets
Impressionism			guid: 200/163		22 assets 
India Rasa				guid: 200/45		42 assets 
Insects					guid: 200/120		57 assets 
Islamic Ceramics			guid: 200/46		59 assets 
Islamic Metalwork			guid: 200/219		23 assets
Jade in Mesoamerica		guid: 200/87		24 assets 
Japanese Wood Block		guid: 200/93		46 assets 
Landscape Views			guid: 200/238		24 assets 
Making Music				guid: 200/245		23 assets+ 
Masks Around the World	guid: 200/77		23 assets 
Medieval Arts			guid: 200/51		115 assets 
Medieval Culture			guid: 200/50		50 assets 
Medieval Devotionals		guid: 200/49		59 assets 
Mesoamerica				guid: 200/141		322 assets
Mondo Menagerie			guid: 200/232		59 assets 
Mughal Illustration			guid: 200/180		37 assets 
Native American West		guid: 200/231		22 assets 
Neoclassical				guid: 200/217		21 assets 
Netsuke Sculptures		guid: 200/166		41 assets 
Northern Renaissance		guid: 200/70		72 assets
Olmec					guid: 200/129		59 assets 
Orange					guid: 200/190		25 assets 
Orchestra				guid: 200/168		116 assets 
Painting					guid: 200/27		531 assets 
Paris					guid: 200/20		887 assets 
Pastels					guid: 200/224		22 assets 
Persian Illustration			guid: 200/174		205 assets 
Perspective				guid: 200/201		22 assets 
Photography				guid: 200/109		200 assets 
Plague Saints			guid: 200/67		44 assets 
Portrait					guid: 200/25		365 assets
Portrait Traditions			guid: 200/222		220 assets 
Pre-Raphaelites			guid: 200/104		36 assets 
Printmaking				guid: 200/88		87 assets 
Qing Dynasty				guid: 200/135		53 assets
Queen Isabella of Spain's Book of Hours	
guid: 200/156		41 assets 
Rainbows				guid: 200/78		21 assets 
Red						guid: 200/211		147 assets 
Reliquaries				guid: 200/80		91 assets 
Rembrandt				guid: 200/21		429 assets
Renaissance Media		guid: 200/24		678 assets 
Rococo					guid: 200/148		95 assets *fix
Roman Frescos			guid: 200/178		13 assets 
Romanticism				guid: 200/117		46 assets
Samurai					guid: 200/140		28 assets 
Self-Portraits				guid: 200/145		23 assets 
Shining Armor			guid: 200/48		28 assets
Snow					guid: 200/76		20 assets 
South Pacific Islands		guid: 200/52		51 assets 
Southeast Asia			guid: 200/173		213 assets 
Spring					guid: 200/227		91 assets 
Stained Glass			guid: 200/225		78 assets 
Still Life in Asian Painting	guid: 200/155		10 assets 
Techniques in Painting		guid: 200/119		50 assets 
Teotihuacan | Birthplace	guid: 200/90		57 assets
Textures and Patterns		guid: 200/189		45 assets 
The Age of Austen		guid: 200/146		42 assets 
Tiger Kings				guid: 200/54		22 assets 
Triptychs and Diptychs		guid: 200/71		23 assets 
Vincent van Gogh			guid: 200/108		27 assets 
Waters of Japan			guid: 200/73		16 assets 
William Blake Illuminations	guid: 200/186		19 assets 
Women's Impressionism	guid: 200/208		16 assets 
	(copy over/merge Painting Women in 19th c.?)
Woodblock Prints			guid: 200/199		68 assets 
Yuan Dynasty			guid: 200/115		21 assets 
Zodiac					guid: 200/169		54 assets
"""

a=re.findall( r'guid: 200/(.*?)\t', str)
print(a)
aa=[]
for i in a :
    b={"groupName": "spotlight","key": "preset","value": "200/"+i}
    aa.append(b)

print(json.dumps({"root":aa}))