// --- Programme Arduino ---
// par X. HINAULT - 01/2010 

// --- Que fait ce programme ? ---
/* Affiche des messages texte sur l'afficheur LCD*/

// --- Fonctionnalités utilisées ---
// Utilise un afficheur LCD 4x20 en mode 4 bits 

//**************** Entête déclarative *******
// A ce niveau sont déclarées les librairies, les constantes, les variables...

// --- Inclusion des librairies utilisées ---
#include <LiquidCrystal.h> // Inclusion de la librairie pour afficheur LCD 

// --- Déclaration des constantes ---

// --- constantes des broches ---

const int RS=4; //declaration constante de broche 
const int E=5; //declaration constante de broche 

const int D4=10; //declaration constante de broche 
const int D5=11; //declaration constante de broche 
const int D6=12; //declaration constante de broche 
const int D7=13; //declaration constante de broche 

const int BP_encodeur=7; // declaration constante
const int APPUI=LOW; 

// --- Déclaration des variables globales ---

// --- Initialisation des fonctionnalités utilisées ---
LiquidCrystal lcd(RS, E, D4, D5, D6, D7);// initialisation LCD en mode 4 bits 

//**************** FONCTION SETUP = Code d'initialisation *****
// La fonction setup() est exécutée en premier et 1 seule fois, au démarrage du programme

void setup()   { // debut de la fonction setup()

Serial.begin(115200); 
Serial.println("Arduino OK"); 

pinMode(BP_encodeur,OUTPUT); 
digitalWrite(BP_encodeur, HIGH); // rappel au +

// --- ici instructions à exécuter au démarrage --- 

lcd.begin(20,4); // Initialise le LCD avec 20 colonnes x 4 lignes 

delay(10); // pause rapide pour laisser temps initialisation

// Test du LCD

lcd.print("LCD OK") ; // affiche la chaîne texte - message de test
delay(2000); // pause de 2 secondes

lcd.clear(); // // efface écran et met le curseur en haut à gauche
delay(10); // pour laisser temps effacer écran

} // fin de la fonction setup()
// ********************************************************************************

//*************** FONCTION LOOP = Boucle sans fin = coeur du programme *************
// la fonction loop() s'exécute sans fin en boucle aussi longtemps que l'Arduino est sous tension

void loop(){ // debut de la fonction loop()

if (digitalRead(BP_encodeur)==APPUI) Serial.println("Appui encodeur"); 

/*
lcd.print("Arduino...") ; // affiche la chaîne texte - message de test
delay(2000); // pause de 2 secondes

lcd.setCursor(9, 1) ; // 10ème col - 2ème ligne - positionne le curseur à l'endroit voulu (colonne, ligne) (1ère=0 !) 
lcd.print("...pour te") ; // affiche la chaîne texte - message de test
delay(2000); // pause de 2 secondes

lcd.setCursor(4, 2) ; // 5ème col - 3ème ligne - positionne le curseur à l'endroit voulu (colonne, ligne) (1ère=0 !) 
lcd.print("...servir") ; // affiche la chaîne texte - message de test
delay(2000); // pause de 2 secondes

lcd.setCursor(12, 3) ; // 13ème col - 4ème ligne - positionne le curseur à l'endroit voulu (colonne, ligne) (1ère=0 !) 
lcd.print("...amigo") ; // affiche la chaîne texte - message de test
delay(2000); // pause de 2 secondes

lcd.clear(); // // efface écran et met le curseur en haut à gauche
delay(10); // pour laisser temps effacer écran
*/
// --- ici instructions à exécuter par le programme principal --- 

} // fin de la fonction loop() - le programme recommence au début de la fonction loop sans fin
// ********************************************************************************

// --- Fin programme ---

// --- Mémo instructions ---

// var_int = digitalRead(Pin); //lit état de la broche indiquée et renvoie valeur HIGH ou LOW 
// digitalWrite(pin, value) ; // met la valeur HIGH ou LOW sur la broche indiquée
// digitalRead(pin) ; // lit l'état d'une broche numérique en entrée et renvoie la valeur HIGH ou LOW présente sur la broche

// --- mémo boucle -- 
//for (int i=0; i <= 10; i++); // boucle simple 
//delay(300); // pause en millisecondes 
// ----- memo LCD --- 
// LiquidCrystal(rs, enable, d4, d5, d6, d7) ; // initialisation 4 bits
// lcd.begin(cols, rows); // initialisation nombre colonne/ligne
// 
// lcd.clear(); // efface écran et met le curseur en haut à gauche
// lcd.home(); // repositionne le curseur en haut et à gauche SANS effacer écran
// 
// lcd.setCursor(col, row) ; // positionne le curseur à l'endroit voulu (colonne, ligne) (1ère=0 !) 
// lcd.print("texte") ; // affiche la chaîne texte
// 
// lcd.cursor() ; // affiche la ligne de base du curseur 
// lcd.noCursor() ; // cache le curseur 
// lcd.blink() ; // fait clignoter le curseur
// lcd.noBlink() ;// stoppe le clignotement du curseur
// lcd.noDisplay() ; // éteint le LCD sans modifier affichage
// lcd.display() ; // rallume le LCD sans modif affichage
// 
// lcd.scrollDisplayLeft(); // décale l'affichage d'une colonne vers la gauche
// lcd.scrollDisplayRight(); // décale l'affichage d'une colonne vers la droite 
// lcd.autoscroll() ; // les nouveaux caractères poussent les caractères déjà affichés
// noAutoscroll(); // stoppe le mode autoscroll


