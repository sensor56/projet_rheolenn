
// Micrologiciel (firmware) pour régulation chauffage solaire
// avec le shield Rheolenn
// Janvier 2015

// Tous droits réservés - X. HINAULT - www.mon-club-elec.fr
// Licence GPLv3 

// Tout produit ou projet basé sur ou dérivé de ce logiciel doit etre opensource et libre
// Voir le descriptif de la licence GPL v3 pour connaitre vos droits d'utilisation 
// http://www.gnu.org/licenses/gpl.html


// inclusion des librairies utilisées
#include <Utils.h> // inclusion de la librairie
#include <OneWire.h> // librairie pour capteur OneWire
// atttention : utiliser librairie supportant tableau de bus onewire : https://github.com/prashantdev/arduino-OneWire 

//===== variables de broche =====

//-- broches circulateurs
const int nombreCirculateurs=4; // nombre de circulateurs - 4 max
int broches_circulateur[nombreCirculateurs]={7,6,5,4}; // broches des circulateurs - dispo sur broches 4 à 7 
int etatCirculateur[nombreCirculateurs]={LOW,LOW,LOW,LOW};

//-- broches capteurs onewire
const int nombreOnewire=2; // nombre de capteur OneWire 
int broches_OneWire[nombreOnewire]={14,15}; // broches des capteurs Onewire - utilise broches numériques 

// ===== variables globales utiles =====

//-- one wire
byte adresse[8]; // Tableau de 8 octets pour stockage du code d'adresse 64 bits du composant One Wire
byte data[12]; // Tableau de 12 octets pour lecture des 9 registres de RAM et des 3 registres d'EEPROM du capteur One Wire

int temperature=0; // variable entiere pour stocker la température brute
float temperaturef=0.0; // variable décimale pour stocker la température réelle

//---- code d'instruction du capteur
const int modeLecture=0xBE;
const int lancerMesure=0x44;

//-- temperature
float mesureBrute[2]={0,0};// Tableau de variables pour acquisition résultat brut de conversion analogique numérique
float mesure[2]={0,0}; // Tableau de variables à virgule pour calcul valeur en millivolts
float temperatures[2]={0.0,0.0}; // tableau des températures

//-- reception serie 
String chaineReception=""; // déclare un String
long params[6]; // déclare un tableau de long - taille en fonction nombre max paramètres attendus

//-- parametrages capteurs
const int ballon=0; // index ballon
const int panneau=1; // index panneau

float correct[2]={0.0, 0.0}; // coefficient correctino mesure mV

//---- variables gestion delais
long millis0Mesure=0; 
long delaiMesure=5000; // toutes les n millisecondes

long millis0CircON=0; 
long delaiCircON=30000; // 5 minutes = 300 000 millisecondes - 30 000 pour test

//--- variables régulation 
float deltaCapteurs=0.0; // ecart entre les capteurs
float deltaDeclenchement=2.0; // delta declenchement en degres - 7 en réel - 2 en test 

//-- divers
int debug=true;  // variable drapeau activation messages 
int flagAuto=false; // variable pour regulation auto

// --- Déclaration des objets utiles pour les fonctionnalités utilisées ---
Utils utils; // déclare objet racine d'accès aux fonctions de la librairie Utils

//-- declarer autant de capteur que necessaire
OneWire capteurs_bus[nombreOnewire];

//OneWire  capteur(broches_OneWire);  // crée un objet One Wire sur la broche voulue

//xxxxxxxxxxxxxxxxx fonction setup xxxxxxxxxxxxxxxxxx
// exécutée une fois au démarrage
void setup() {

  // mise en sortie des broches de circulateur 
  for (int i=0; i<nombreCirculateurs; i++){
    pinMode(broches_circulateur[i],OUTPUT); // met la broche en sortie
    
    // circulateurs OFF au démarrage
    etatCirculateur[i]=LOW; 
    digitalWrite(broches_circulateur[i], etatCirculateur[i]); // eteint circulateur

  }

   // initialisation des bus de capteurs avec broches utilisées 
  for (int i=0; i<nombreOnewire; i++){
    capteurs_bus[i].setPin(broches_OneWire[i]); 
  }
   
   
   // initilisation série + message accueil 
  Serial.begin(115200); // Initialisation vitesse port Série
  // Utiliser vitesse idem coté Terminal série

  Serial.println("Chaines de controle reconnues:"); // message initial
  Serial.println("CIRC(0-3,0/1)"); 
  Serial.println("initSensor(indexBus)"); 
  Serial.println("getTemp(indexBus)"); 
  Serial.println("setAuto(0/1)"); 
  
  
} // fin setup


//xxxxxxxxxxxxxxx fonction loop xxxxxxxxxxxxxxxxx
// exécutée en boucle 

void loop() {

    //==== gestion regulation ====
    if (millis()-millis0Mesure>delaiMesure) { // si delai écoulé, on fait une mesure

    millis0Mesure=millis(); 
    
    if (flagAuto==true) {
       mesureCapteurs(); 
       regulation(0); // passe index circulateur à réguler
    } // fin flag auto
    
    } // fin if mesure

  
    //======= reception serie et analyse chaine de controle recue ==========
  
    //chaineReception=utils.waitingString(true);// avec debug
    chaineReception=utils.waitingString();// sans debug

    if (chaineReception!="") { // si une chaine a été reçue

       // --- gestion controle DS18B20 --- 
       //if (chaineReception=="getTemp()")Serial.println(getTemp(0)); // forme simple
       if(utils.testInstructionLong(chaineReception,"getTemp(",1,params)==true) Serial.println(getTemp(params[0])); 
       if(utils.testInstructionLong(chaineReception,"setAuto(",1,params)==true) flagAuto=params[0], Serial.println(flagAuto); 
       
       //else if (chaineReception=="initSensor()") initSensor(0); // forme simple - la fonction realise elle-meme son affichage serie
       else if(utils.testInstructionLong(chaineReception,"initSensor(",1,params)==true) initSensor(params[0]); // pas println  - la fonction realise elle-meme son affichage serie
       
        // --- gestion controle relais par port série 
    	else if(utils.testInstructionLong(chaineReception,"CIRC(",2,params)==true) { // si chaine LED(valeur) bine reçue

        	if (debug) Serial.println("Arduino a recu les parametres : " + (String)params[0]+"|"+(String)params[1]);

         	 digitalWrite(broches_circulateur[params[0]],params[1]); // on applique la valeur PWM sur la LED

    	} // fin si testInstructionLong==true


    } // fin // si une chaine a été reçue

} // fin loop


//XXXXXXXXXXXXXXXXXXXXXXX FONCTIONS DEDIEES DS18B20 XXXXXXXXXXXXXXXXXXX
//----- fonction initSensor() ------
void initSensor(int indexIn){
  // la fonction affiche sur port serie chaine xx:xx:xx:xx:xx|DS:xxxxx|CRC:xx

  //---- détection des capteurs présents sur le bus One Wire
  
  //Serial.println("*** Capteur present sur le bus 1-wire *** ");
  while (capteurs_bus[indexIn].search(adresse)!= true) { }// attend qu'un capteur soit détecté
    // la fonction search renvoie la valeur VRAI si un élément 1-wire est trouvé. Stocke son adresse dans le tableau adresse
    // adresse correspond à l'adresse de début du tableau adresse[8] déclaré ... 
  
    //Serial.print (" 1 capteur 1-wire present avec code adresse 64 bits : ");
    
    //--- affichage des 64 bits d'adresse au format hexadécimal
     for(int i = 0; i < 8; i++) { // l'adresse renvoyée par la fonction search est stockée sur 8 octets
     
      if (adresse[i]<16) Serial.print('0'); // pour affichage des O poids fort au format hexadécimal
      Serial.print(adresse[i], HEX); // affiche 1 à 1 les 8 octets du tableau adresse au format hexadécimal
      Serial.print(":");
  
       } // fin for 
  
    Serial.print("|"); 
    
    //---- test du type de capteur ---- 
    // le type du capteur est donné par le 1er octet du code adresse 64 bits
    // Valeur 0x28 pour capteur type DS18B20, 0x10 pour type DS18S20, 0x22 pour type DS1820
    if (adresse[0]==0x28) Serial.print ("DS:18B20");  
    //else Serial.println ("Le capteur n'est pas reconnu en tant que DS18B20."); 
    else Serial.print ("DS:-----"); 

    Serial.print("|"); 
    
    //----- contrôle du code CRC ----
    // le dernier octet de l'adresse 64bits est un code de contrôle CRC 
    // à l'aide de la fonction crc8 on peut vérifier si ce code est valide
    if (capteurs_bus[indexIn].crc8( adresse, 7) == adresse[7]) // vérification validité code CRC de l'adresse 64 bits
    // le code CRC de l'adresse 64 bits est le 8ème octet de l'adresse (index 7 du tableau)
    {
      //Serial.println ("Verification du code CRC de l'adresse 64 bits de ce capteur : VALIDE !"); 
      Serial.print("CRC:OK");
    }
    else
    {
      //Serial.println ("Verification du code CRC de l'adresse 64 bits de ce capteur : NON VALIDE !");   
      Serial.print("CRC:PB");  
    }
    
    Serial.println(""); // fin 
  
} // fin init sensor

//-------------- fonction getTemp de mesure de la température 
float getTemp(int indexIn){
  
   //--------- lancer une mesure --------
  capteurs_bus[indexIn].reset(); // initialise le bus 1-wire avant la communication avec un capteur donné
  capteurs_bus[indexIn].select(adresse); // sélectionne le capteur ayant l'adresse 64 bits contenue dans le tableau envoyé à la fonction
  capteurs_bus[indexIn].write(lancerMesure,1); // lance la mesure et alimente le capteur par la broche de donnée

    //-------- pause d'une seconde ----- 
    delay(1000);     // au moins 750 ms
               // il faudrait mettre une instruction capteur.depower ici, mais le reset va le faire
               
    // ----------- lire les 9 octets de la RAM (appelé Scratchpad) ----
      capteurs_bus[indexIn].reset(); // initialise le bus 1-wire avant la communication avec un capteur donné
      capteurs_bus[indexIn].select(adresse); // sélectionne le capteur ayant l'adresse 64 bits contenue dans le tableau envoyé à la fonction
      capteurs_bus[indexIn].write(modeLecture,1); // lance la mesure et alimente le capteur par la broche de donnée
      
    for ( int i = 0; i < 9; i++) {           // 9 octets de RAM stockés dans 9 octets
        data[i] = capteurs_bus[indexIn].read();             // lecture de l'octet de rang i stocké dans tableau data
        //Serial.println(data[i]); 
      }
      
    
    //----- test de validité des valeurs reçues par contrôle du code CRC  ----
    
    //Serial.println("");
    //Serial.println("---- Resultat de mesure de la temperature ---- ");
    
      // le dernier (9ème) octet de la RAM est un code de contrôle CRC 
      // à l'aide de la fonction crc8 on peut vérifier si ce code est valide
      if (capteurs_bus[indexIn].crc8( data, 8) == data[8]) // vérification validité code CRC des valeurs reçues
      {
        //Serial.println ("Verification du code CRC des Registres : VALIDE !"); 
      
      }
      else
      {
        //Serial.println ("Verification du code CRC des Registres : NON VALIDE !"); 
        return (-88.88); // valeur si probleme
      }
      
      
      //----- réalisation d'une mesure de température--- 
    data[1]=data[1] & B10000111; // met à 0 les bits de signes inutiles
    temperature=data[1]; // bits de poids fort
    temperature=temperature<<8; // décalage de 8 bits vers la gauche = vers les bits de poids fort
    temperature=temperature+data[0]; // bits de poids faible ici mis dans les 8 premiers bits
    
    //Serial.print ("Mesure brute ="); 
    //Serial.println (temperature); 
    
    // --- en mode 12 bits, la résolution est de 0.0625°C - cf datasheet DS18B20
    temperaturef=float(temperature)*6.25;
    temperaturef=temperaturef/100.0;
    
    //Serial.print ("Mesure Finale ="); 
    //Serial.print (temperaturef,2); 
    //Serial.println (" Degres Celsius. "); 

    return (temperaturef); 
    
} // fin getTemp

//XXXXXXXXXXXXXXXX FONCTIONS REGULATION XXXXXXXXXXXXXXXXXXXXXXXx
void mesureCapteurs() {
 
     //=========== gestion des mesures =================
    //for (int i=0; i<sizeof(capteurs)/2; i++) { 
     for (int i=0; i<nombreOnewire; i++) { 

         initSensor(i); 
         temperatures[i]=getTemp(i); 
         Serial.println(temperatures[i]); 
    } // fin for
    
    Serial.println("-----------"); 
    
} // fin mesureCapteurs

void regulation(int indexIn){
  
    //======= calcul differentiel temperature =====
    //Serial.print(temperatures[panneau]), Serial.println(temperatures[ballon]); 
    deltaCapteurs=temperatures[panneau]-temperatures[ballon];
    Serial.print("Diff="), Serial.print(deltaCapteurs), Serial.println("C"); 
    
    //lcd.setCursor(0,2); // debut 3eme ligne
    //lcd.print("Diff:"), lcd.print(deltaCapteurs), lcd.print(" "); 
    
    //========== logique de régulation ==========

    if (etatCirculateur[indexIn]==LOW){ // si pompe eteinte
    
      if (deltaCapteurs>=deltaDeclenchement) { 
        etatCirculateur[indexIn]=HIGH;
        digitalWrite(broches_circulateur[indexIn], etatCirculateur[indexIn]); // met la broche dans l'etat voulu
        millis0CircON=millis(); 
      } // fin if
    
    } // fin if LOW
      
    else { // si etat circ== HIGH
    
        if (millis()-millis0CircON>delaiCircON) { // si delai ON ecoule

          etatCirculateur[indexIn]=LOW; // éteint le circulateur
          digitalWrite(broches_circulateur[indexIn], etatCirculateur[indexIn]); // met la broche dans l'etat voulu

          //lcd.setCursor(0,3); // debut 4eme ligne
          //lcd.print("             ");    // efface
          
        } // fin if millis0CircON
        
       else { // si ON en cours, on affiche le decompte des secondes
                
           //lcd.setCursor(0,3); // debut 4eme ligne
           //lcd.print((millis()-millis0CircON)/1000);       
        } // fin else
    
    } // fin else

    // affiche etat circulateur
    Serial.print("Etat Circulateur =");
    if (etatCirculateur[indexIn]) Serial.println("ON"); else Serial.println("OFF");
    
    //lcd.setCursor(10,2); // milieu 3eme ligne
    //lcd.print("Circ :"); 
    //if (etatCirculateur) lcd.print("ON "); else lcd.print("OFF");
   Serial.println("---------------");
  
} // fin regulation


