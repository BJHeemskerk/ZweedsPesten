# 🃏 Zweeds Pesten - Strategie Analyse

Welkom bij de GitHub-repository voor de analyse en ontwikkeling van strategieën voor het kaartspel **Zweeds Pesten**. Dit project bevat code en notebooks waarin verschillende strategieën worden getest en geëvalueerd.

## 🂡 Wat is Zweeds Pesten?

Zweeds Pesten is een kaartspel dat vaak in de pauzes wordt gespeeld door ons en onze klasgenoten van ADS&AI. Het spel is variant op het, in Nederland populaire, kaartspel Pesten. Bij Zweeds pesten draait het om het leggen van kaarten die hetzelfde of hoger zijn dan de kaart die boven op de aflegstapel ligt. Ook zijn er, net als bij pesten, speciale kaarten die jouw sneller naar de overwinning kunnen brengen of die de tegenstander kunnen belemmeren. Het uiteindelijk doel van het spel is gelijk aan dat van pesten, zorgen dat je als eerste geen kaarten meer hebt. De volledig gehanteerde regels zijn te vinden in [`Regels`](Regels.txt).

## 📁 Projectstructuur

```plaintext
📁 ZweedsPesten-Strategie
├── 📁 notebooks/
│   ├── 📜 TestenStratBusse.ipynb    # Testen van Busse's strategie
│   ├── 📜 ZweedsPestenTesten.ipynb  # Algemene tests voor strategieën
├── 📁 src/
│   ├── 📜 main.py    # Implementatie van strategieën
│   ├── 📜 utils.py   # Code en functies voor het spel
├── 📜 .gitignore
├── 📜 LICENSE
├── 📜 README.md
├── 📜 requirements.txt
```

## 🚀 Installatie

Volg deze stappen om het project lokaal op te zetten:

1. **Clone de repository**
   ```bash
   git clone https://github.com/jouw-gebruikersnaam/ZweedsPesten-Strategie.git
   cd ZweedsPesten-Strategie
   ```

2. **Installeer de vereiste pakketten**
   ```bash
   pip install -r requirements.txt
   ```

## 🏗 Gebruik

Het is aan te raden om de code enkel via notebooks te gebruiken, gezien er geen functionaliteit is gemaakt voor het runnen van losse bestanden. Je kunt de notebooks openen en uitvoeren met Jupyter Notebook of Jupyter Lab:

```bash
jupyter notebook
```

## 📊 Strategieën

Momenteel zijn de volgende strategieën aanwezig in de code:

### Strategie "Player" (De basis strategie)
De Player-strategie is de standaardimplementatie van een strategie. Deze strategie maakt willekeurige, ondoordachte keuzes. Bij het kiezen van open kaarten (display_cards) kiest deze strategie willekeurig 3 kaarten. Tijdens het spelen van het spel kiest hij een willekeurige kaart om te spelen uit zijn hand en eens in de zoveel tijd zal hij de aflegstapel in de hand nemen. Deze take-actie onderneemt hij dus ook op basis van willekeur. De onderliggende logica bestaat volledig uit willekeurige keuzes zonder tactische overwegingen, wat deze strategie ongeschikt maakt als serieuze spelvariant. Van de spelerstrategieën in de volgende paragrafen bekijken wij wel hoe sterk of hoe zwak ze uitvallen in een simulatie. Wanneer een speler naam geen toegewezen class heeft, wordt de Player class zijn of haar strategie.

### Strategie “Busse”
De strategie Busse heeft als plan om altijd de laagst mogelijke, valide kaarten te spelen. Dit doet Busse altijd voordat hij kijkt naar eventuele speciale kaarten. Wanneer de speciale kaarten aan bod komen speelt Busse als eerst de 10, dan de 2 en als laatste pas de 3. Voor het neerleggen van de display kaarten volgt Busse de volledig omgekeerde volgorde, waarbij eerst de 3, dan de 2 en vervolgens de 10 wordt neergelegd. Als deze er niet zijn legt hij display kaarten neer van hoog naar laag. Busse zorgt er ook voor dat hij nooit zomaar de stapel pakt of een kaart niet speelt uit zijn hand. Mocht hij twee of meer kaarten kunnen spelen speelt hij er dus altijd twee of meer.

### Strategie “LowNoon”
De strategie LowNoon volgt exact dezelfde logica als Busse, met een paar twists. LowNoon heeft een 70% kans om bij het selecteren van niet speciale kaarten om te spelen (dus niet bij het neerleggen) om de laagst mogelijke kaart te spelen. Daarnaast is er een 30% kans om de hoogst mogelijke kaart te spelen uit de hand (waarbij speciale kaarten niet meetellen). Ook is er een 20% kans om af te wijken van de strategie, waarbij LowNoon een willekeurig valide kaart speelt uit de hand.

### Strategie “Tim”
De "Tim"-strategie is een unieke strategie die niet als doel heeft om te winnen, maar om niet te verliezen. Ik heb deze strategie geprogrammeerd met als hoofdfilosofie om zoveel mogelijk goede kaarten te verzamelen.
Dit wordt gedaan door in het begin kaarten zoals een 9 of een J te spelen. De spelers die daarna komen, zullen waarschijnlijk hogere kaarten opleggen, zoals een Q, K of A. Bij de Tim-strategie pak je vervolgens de stapel op het moment dat er alleen maar goede kaarten in zitten.
Hoe goed een stapel is om te pakken, wordt berekend door aan elke kaart een waarde toe te kennen. De slechtste kaart, een 4, heeft bijvoorbeeld een waarde van -25, terwijl de beste kaarten, zoals een 2, 10 of A, een waarde van 20 hebben. De strategie berekent vervolgens de gemiddelde waarde van een stapel kaarten. Als de stapel een waarde heeft van minimaal 17, dan is het de moeite waard om deze te pakken. Anders wordt de slechtst mogelijke kaart gespeeld.

### Strategie “Low”
Kiest altijd de laagste kaart en pakt enkel als de strategie niet kan spelen.

### Strategie “Jasper”
Strategie "Jasper" kenmerkt zich door de nadruk te leggen op het uitspelen van lage kaarten. De waarde van de kaarten is volgens een eigen list, genaamd LOW_play_values opgesteld. De strategie maakt dus geen gebruik van list CARD_VALUES. 
De LOW_play_values met de waarden van verschillende kaarten werkt door bij het kiezen van de kaarten die open op tafel komen te liggen. De hoogst gewaardeerde kaarten uit LOW_play_values zijn allereerst de 3, daarna de 10 en daarna de 2 en daarna de kaarten van de Aas tot en met de 4. Als een speler dus een 3 krijgt, dan zal die open op tafel komen te liggen, omdat die de hoogste waarde heeft gekregen volgens LOW_play_values. Daarnaast heeft de "Jasper strategie" een focus op het zo snel mogelijk spelen van dubbele kaarten. Als in de playable_cards meer dan een keer de zelfde waarde voorkomt dan wordt die eerst gespeeld.
Wat verder nog interessant is aan deze strategie is dat er bij de Jasper-strategie wordt nooit de aflegstapel in de hand wordt genomen (take), tenzij de speler niet anders kan.

### Strategie “Justice-and-Terror”
De Justice_and_Terror-strategie is een hybride strategie die onderdelen van de "Tim"-strategie en de "Jasper"-strategie met elkaar combineert. Het heeft met de Jasper-strategie gemeenschappelijk dat de list LOW_play_values wordt gebruikt om een alternatieve lijst met waarderingen te geven ten opzichte van de constant list CARD_VALUES. Dus de manier van het uitspelen van kaarten en het uitkiezen van kaarten die open worden gelegd komt daarmee overeen. 
Echter, bij beslissingen die worden genomen wanneer er een optie is om meerdere kaarten van dezelfde waarde tegelijk uit te leggen (zoals drie 7ens), wordt Tim-strategie-logica gebruikt. Deze logica stelt dat wanneer de gemiddelde waarde van die kaarten minder is dan 4, er maar 1 van de kaarten die dezelfde waarden hebben wordt opgelegd.

### Strategie “Natasja”
Deze strategie is vrij conservatief, waarbij steeds lage kaarten worden uitgespeeld. Maar de strategie bevat een verrassingselement: een aanval waarbij een hoge kaart op een stapel met lagere kaarten wordt gelegd. Bij de “Natasja”-strategie pakt de speler de stapel telkens als er een maximum van 7 kaarten op tafel ligt, waarbij het gemiddelde van de kaarten minimaal 8 moet zijn (volgens de constante list van waarden genaamd CARD_VALUES). Een kanttekening moet daarbij worden geplaatst. Een speler zal bij een potje dat in het echt wordt gespeeld waarschijnlijk niet alle kaarten die afgelegd zijn onthouden, noch steeds telkens het  gemiddelde van de aflegstapel uitrekenen en bijhouden. Echter benadert het nemen van het gemiddelde en het bijhouden van het aantal kaarten op de aflegstapel de situatie waarbij een speler ongeveer een idee heeft van de hoeveelheid kaarten op de stapel en de hoogte van de kaarten die erin liggen.

Als deze kaart in de hand is genomen zal de speler eenmaal een hoge kaart opleggen als de aflegstapel minimaal 5 kaarten bevat en maximaal een gemiddelde waarde van 7.5 heeft. De speler legt dan een Q op en als die er niet is een K en als die er niet is een A. Deze strategie beoogt op deze manier af te dwingen dat een volgende speler de steeds groter wordende stapel kaarten op tafel moet pakken. In de code wordt dit de q-strategie genoemd, vernoemd naar de laagste hoge kaart, de Q, die wordt opgelegd als voldaan is aan de voorwaarden.

Het pakken van de stapel en het uitspelen van een “onverwacht” hoge kaart geschiedt slechts eenmaal in het spel, omdat het een riskante strategie is. 
Het is een riskante strategie,  omdat de speler een valstrik zet voor de vijand, die een averechtse uitwerking kan hebben. De speler neemt een risico door een potentieel grote stapel kaarten (maximaal 7) in de hand te nemen en dat deze kaarten niet op tijd kunnen worden uitgespeeld. Ook loopt de speler het risico dat als de speler voor de Q-strategie een hoge kaart uitspeelt, de andere spelers ook hoge kaarten hebben en het moment van het in de hand moeten nemen van de stapel kaarten uiteindelijk bij de speler uitvalt.

## 📜 Licentie

Dit project is beschikbaar onder de **MIT License**. Zie [`LICENSE`](LICENSE) voor meer details.
