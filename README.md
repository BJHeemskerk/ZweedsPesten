# Zweeds Pesten - Strategie Analyse

Welkom bij de GitHub-repository voor de analyse en ontwikkeling van strategieën voor het kaartspel **Zweeds Pesten**. Dit project bevat code en notebooks waarin verschillende strategieën worden getest en geëvalueerd.

## 🃏 Wat is Zweeds Pesten?

Zweeds Pesten is een kaartspel dat vaak in de pauzes wordt gespeeld door ons en onze klasgenoten van ADS&AI. Het spel is variant op het, in Nederland populaire, kaartspel Pesten. Bij Zweeds pesten draait het om het leggen van kaarten die hetzelfde of hoger zijn dan de kaart die boven op de aflegstapel ligt. Ook zijn er, net als bij pesten, speciale kaarten die jouw sneller naar de overwinning kunnen brengen of die de tegenstander kunnen belemmeren. Het uiteindelijk doel van het spel is gelijk aan dat van pesten, zorgen dat je als eerste geen kaarten meer hebt. De volledig gehanteerde regels zijn te vinden in [`Regels`](Regels.txt).

## 🎯 Waarom een strategie analyse

Zweeds Pesten is vrij genoeg voor het gebruiken van vele verschillende strategieën en interessante tactieken tijdens het verloop van het spel. Het maken van een strategie analyse helpt met het vergroten van de inzicht in de mogelijke strategieën die een speler kan gebruiken om zo vaak mogelijk te winnen.

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

| Strategie            | Speelstijl       | Neemt stapel? | Speciale focus | Sterkte                                      | Zwakte                                       |
|----------------------|-----------------|--------------|----------------|----------------------------------------------|----------------------------------------------|
| **Player**           | Willekeurig     | Ja, willekeurig | Geen strategie | Gemakkelijk te implementeren, snel te testen | Zeer onvoorspelbaar, geen tactische overwegingen |
| **Busse**            | Conservatief    | Nee | Lage kaarten eerst, speciale kaarten op volgorde | Stabiele en voorzichtige aanpak, minder risico | Beperkte flexibiliteit, kan niet snel reageren op veranderende situaties |
| **LowNoon**          | Gemengd         | Nee | 70% laagste kaart, 30% hoogste kaart, 20% kans op willekeurig | Variatie in keuzes, onverwachte wendingen | Minder consistent dan Busse, onvoorspelbare beslissingen |
| **Tim**              | Verzamelen      | Ja, slimme keuze | Goede kaarten verzamelen, stapelwaarde berekenen | Strategie met een langetermijnvisie, goede voorbereiding | Kan te passief zijn, niet altijd effectief op korte termijn |
| **Low**              | Simpel          | Nee | Altijd de laagste kaart spelen | Zeer voorspelbaar, makkelijk te implementeren | Zeer passief, geen offensieve strategie |
| **Jasper**           | Laag & efficiënt | Nee | Lage kaarten eerst, dubbele kaarten snel uitspelen | Snel en efficiënt met kaarten, maakt gebruik van dubbele kaarten | Onvoldoende focus op de stapel, kan soms te snel spelen |
| **Justice-and-Terror** | Hybride | Nee | Jasper-logica + Tim’s stapelwaarde-berekening | Flexibel en hybride, kan reageren op verschillende scenario's | Complexe beslissingen, kan niet altijd optimaal presteren |
| **Natasja**          | Risicovol       | Ja, éénmalig | Stapel pakken en strategisch een hoge kaart spelen als valstrik | Kan verrassend zijn, neemt risico’s die anderen kunnen verrassen | Risico dat het misgaat, moeilijk om de timing perfect te krijgen |

## 📜 Licentie

Dit project is beschikbaar onder de **MIT License**. Zie [`LICENSE`](LICENSE) voor meer details.
