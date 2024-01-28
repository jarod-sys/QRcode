# QRcode
## Le code que nous avons implementé comporte essentiellement en trois grandes parties:

- Un fichier Qrcode.py : Pour la parallèlisation.(production des 10000 qrcodes).
- Un fichier projet.py: où nous trouvons une classe 'ProjetQrcode' qui constitue le coprs du programme.
- Un fichier fonctions.py: au sein duquel on retrouve une classe du nom "QRcode"
  qui comporte l'ensemble des fonctions implementer pour la réalisation du projet.
- Un fichier test.py: où nous effectuons les tests unitaires jugés necessaire
  pour le bon fonctionnement du programme.


Nous avons par ailleurs importé  quatre modules fondamentaux de python pour simplifier le code:
- Numpy: pour une meilleur manipulation des matrices
- Matplotlib pyplot: pour les visualisations graphiques
- Operator: donc le seul interêt était l'utilisation de la fonction xor (ou exclusif)
- sys: pour récupérer la variable d'entrée.

les fonctions implementer ont éte concues essentiellement pour les objectifs majeurs suivants:
- implementer le polynôme générateur: c'est par définition un produit fini de polynômes
  de degré un. la fonction implementée est: def Generateur():
- La determination du code de correction d'erreur: qui est basée sur le principe de 
  division Euclidienne dans l'anneau principale GF(256).
  la fonction implementée est: def DivisionEuclidienne():
- le remplissage en ZIG_ZIG: ce dernier a été possible grâce a un calcul minutieux 
  que nous avons effectué. la fonction implementée est: def Remplissage_ZIGZAG():
- la division en bloc et l'entrelacement: qui suit le principe edicté par le tutoriel.
les fonction implementées sont  def DivisionEnBloc et def Entrelacement (respectivement).

les autres fonctions n'ont constitué qu'une boite à outils pour parvenir à ces fins majeures.
Toutefois, le code est dûment commenté comme recommandé pour une meilleure comprehension de 
ce dernier. 

Pour produit une QRcode, compiler tout simplement le fichier Qrcode.py:
- En local: entrez comme argument 0 (une convention): il vous sera alors demandé d'entrer un message.
  le code choisit automatiquement la version et le niveau de correction d'erreur en fonction de la taille du message entré.
  pour afficher ce dernier, allez d'abord dans le fichier fonctions.py et ensuite retirez le '#' devant 
 (c'est dans la fonction Plot).
- Sur le cluster: Lancez tout simplement le fichier soumission.sh.

  