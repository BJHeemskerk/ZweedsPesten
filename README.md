# ZweedsPesten
Deze repository is gemaakt om Zweeds Pesten te simuleren in python. Hiervoor is het spel op een eenvoudige manier opgebouwd en is er de mogelijkheid om zelf spelers met eigen strategieen toe te voegen.

## Modulaire Programmatuur
Om de code overzichtelijk, herbruikbaar en per taak logisch op te delen, hebben wij gebruik gemaakt van 3 code-eenheden: 
- Python-script utils.py met de mechanieken van een ronde van het spel “Zweeds Pesten”.
- Python-script main.py dat een template voor de speler en daarvan ervende spelerstrategieen bevat
- Jupyter Notebook ZweedsPestenTesten.ipynb  met de algemene flow van het programma

### utils.py
De kern van het spel wordt gedefinieerd in utils.py. Dit script bevat de logica van het spelmechaniek. Het script bevat de hoofdlus van het spel in de vorm van game_loop().  
<vul ik later nog aan als ik het heb bekeken per stukje code>  Moet nog gebeuren

### main.py
Dan is het main.py dat utils.py aanroept. Het script main.py zorgt voor een structuur om het spel heen en implementeert verschillende speelstrategieën. De structuur die main.py implementeert het bijhouden van de verschillende statussen van de kaarten, dus de kaarten die de speler in de hand heeft, die open op tafel liggen en die verborgen zijn. Class Player zorgt ervoor dat de fictieve spelers van het spel bepaalde moves kunnen doen als zij aan de beurt zijn, zoals het afleggen en opleggen vna kaarten. Fictieve Spelersclasses, in dit geval vernoemd naar de leden van onze groep, erven van Player, zodat deze spelers een bepaalde strategie kunnen toepassen.

### ZweedsPestenTesten.ipynb
De hoofdlus van het spel vindt plaats in het notebook. De gameloop zorgt ervoor dat het spel beurt voor beurt wordt gespeeld. Het spel komt ten einde als er een speler wint, waarna diens naam wordt toegevoegd aan de lijst van winnaars. En daarna gaat het spel verder, totdat er een iemand is die niet heeft gewonnen. Het notebook biedt dus een autonome simulatie van Zweeds Pesten waarbij alle logica voor het trekken van kaarten, het doen van zetten en het controleren van wie de winnaar is is geprogrammeerd. Verder wordt het verloop van het spel geprint. Een hoger getal bij "verbose" geeft aan dat er meer informatie van de stappen wordt geprint in de output, terwijl een lager getal aangeeft dat er een basisniveau aan informatie wordt uitgeprint.



## Strategieën
In deze paragraaf zullen de strategieën uit Python-script main.py worden besproken. Dit script bevat een aantal spelerstrategieën die kunnen worden gebezigd bij de simulatie van het spel Zweeds Pesten. 

### Strategie “Busse”
De strategie Busse heeft als plan om altijd de laagst mogelijke, valide kaarten te spelen. Dit doet Busse altijd voordat hij kijkt naar eventuele speciale kaarten. Wanneer de speciale kaarten aan bod komen speelt Busse als eerst de 10, dan de 2 en als laatste pas de 3. Voor het neerleggen van de display kaarten volgt Busse de volledig omgekeerde volgorde, waarbij eerst de 3, dan de 2 en vervolgens de 10 wordt neergelegd. Als deze er niet zijn legt hij display kaarten neer van hoog naar laag. Busse zorgt er ook voor dat hij nooit zomaar de stapel pakt of een kaart niet speelt uit zijn hand. Mocht hij twee of meer kaarten kunnen spelen speelt hij er dus altijd twee of meer.

### Strategie “LowNoon”
De strategie LowNoon volgt exact dezelfde logica als Busse, met een paar twists. LowNoon heeft een 70% kans om bij het selecteren van niet speciale kaarten om te spelen (dus niet bij het neerleggen) om de laagst mogelijke kaart te spelen. Daarnaast is er een 30% kans om de hoogst mogelijke kaart te spelen uit de hand (waarbij speciale kaarten niet meetellen). Ook is er een 20% kans om af te wijken van de strategie, waarbij LowNoon een willekeurig valide kaart speelt uit de hand.

### Strategie “Tim”
De "Tim"-strategie is een unieke strategie die niet als doel heeft om te winnen, maar om niet te verliezen. Ik heb deze strategie geprogrammeerd met als hoofdfilosofie om zoveel mogelijk goede kaarten te verzamelen.
Dit wordt gedaan door in het begin kaarten zoals een 9 of een J te spelen. De spelers die daarna komen, zullen waarschijnlijk hogere kaarten opleggen, zoals een Q, K of A. Bij de Tim-strategie pak je vervolgens de stapel op het moment dat er alleen maar goede kaarten in zitten.
Hoe goed een stapel is om te pakken, wordt berekend door aan elke kaart een waarde toe te kennen. De slechtste kaart, een 4, heeft bijvoorbeeld een waarde van -25, terwijl de beste kaarten, zoals een 2, 10 of A, een waarde van 20 hebben. De strategie berekent vervolgens de gemiddelde waarde van een stapel kaarten. Als de stapel een waarde heeft van minimaal 17, dan is het de moeite waard om deze te pakken. Anders wordt de slechtst mogelijke kaart gespeeld.

### Strategie “Low”
<Zelfde als Jasper volgens mij!>

### Strategie “Jasper”
Strategie "Jasper" kenmerkt zich door de nadruk te leggen op het uitspelen van lage kaarten. De waarde van de kaarten is volgens een eigen list, genaamd LOW_play_values opgesteld. De strategie maakt dus geen gebruik van list CARD_VALUES. 
De LOW_play_values met de waarden van verschillende kaarten werkt door bij het kiezen van de kaarten die open op tafel komen te liggen. De hoogst gewaardeerde kaarten uit LOW_play_values zijn allereerst de 3, daarna de 10 en daarna de 2 en daarna de kaarten van de Aas tot en met de 4. Als een speler dus een 3 krijgt, dan zal die open op tafel komen te liggen, omdat die de hoogste waarde heeft gekregen volgens LOW_play_values.
Wat verder nog interessant is aan deze strategie is dat er bij de Jasper-strategie wordt nooit de aflegstapel in de hand wordt genomen (take), tenzij de speler niet anders kan.

### Strategie “Justice-and-Terror”
De Justice_and_Terror-strategie is een hybride strategie die onderdelen van de "Tim"-strategie en de "Jasper"-strategie met elkaar combineert. Het heeft met de Jasper-strategie gemeenschappelijk dat de list LOW_play_values wordt gebruikt om een alternatieve lijst met waarderingen te geven ten opzichte van de constant list CARD_VALUES. Dus de manier van het uitspelen van kaarten en het uitkiezen van kaarten die open worden gelegd komt daarmee overeen. 
Echter, bij beslissingen die worden genomen wanneer er een optie is om meerdere kaarten van dezelfde waarde tegelijk uit te leggen (zoals drie 7ens), wordt Tim-strategie-logica gebruikt. Deze logica stelt dat wanneer de gemiddelde waarde van die kaarten minder is dan 4, er maar 1 van de kaarten die dezelfde waarden hebben wordt opgelegd.

### Strategie “Natasja”
Deze strategie is vrij conservatief, waarbij steeds lage kaarten worden uitgespeeld. Maar de strategie bevat een verrassingselement: een aanval waarbij een hoge kaart op een stapel met lagere kaarten wordt gelegd. 
Bij de “Natasja”-strategie pakt de speler de stapel telkens als er een maximum van 7 kaarten op tafel ligt, waarbij het gemiddelde van de kaarten minimaal 8 moet zijn (volgens de constante list van waarden genaamd CARD_VALUES). Een kanttekening moet daarbij worden geplaatst. Een speler zal bij een potje dat in het echt wordt gespeeld waarschijnlijk niet alle kaarten die afgelegd zijn onthouden, noch steeds telkens het  gemiddelde van de aflegstapel uitrekenen en bijhouden. Echter benadert het nemen van het gemiddelde en het bijhouden van het aantal kaarten op de aflegstapel de situatie waarbij een speler ongeveer een idee heeft van de hoeveelheid kaarten op de stapel en de hoogte van de kaarten die erin liggen.
Als deze kaart in de hand is genomen zal de speler eenmaal een hoge kaart opleggen als de aflegstapel minimaal 5 kaarten bevat en maximaal een gemiddelde waarde van 7.5 heeft. De speler legt dan een Q op en als die er niet is een K en als die er niet is een A. Deze strategie beoogt op deze manier af te dwingen dat een volgende speler de steeds groter wordende stapel kaarten op tafel moet pakken. In de code wordt dit de q-strategie genoemd, vernoemd naar de laagste hoge kaart, de Q, die wordt opgelegd als voldaan is aan de voorwaarden.
Het pakken van de stapel en het uitspelen van een “onverwacht” hoge kaart geschiedt slechts eenmaal in het spel, omdat het een riskante strategie is. 
Het is een riskante strategie,  omdat de speler een valstrik zet voor de vijand, die een averechtse uitwerking kan hebben. De speler neemt een risico door een potentieel grote stapel kaarten (maximaal 7) in de hand te nemen en dat deze kaarten niet op tijd kunnen worden uitgespeeld. Ook loopt de speler het risico dat als de speler voor de Q-strategie een hoge kaart uitspeelt, de andere spelers ook hoge kaarten hebben en het moment van het in de hand moeten nemen van de stapel kaarten uiteindelijk bij de speler uitvalt.
