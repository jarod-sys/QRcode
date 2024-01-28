#coding:utf-8

#...................................MODULES IMPORTANTS................................................#

from operator import xor # Pour le ou exclusif
import numpy #Pour les matrices
import matplotlib.pyplot as plt #Pour l'affichage de matrice

#.......................................MES FONCTIONS UTILES...............................................#
class QRcode():
    def __init__(self):
        self.champ_de_galois=[]
        self.MonChamp()
    def MonChamp(self):
        self.champ_de_galois = [1 for i in range(256)]
        for k in range(1, 255):
            self.champ_de_galois[k] = 2 * self.champ_de_galois[k - 1]
            if self.champ_de_galois[k] > 255:
                self.champ_de_galois[k] = xor(285, self.champ_de_galois[k])

    def MultiDansGF(self,a,b):
         assert 0<=a<256 and 0<=b<256
         if a!=0 and b!=0:
            p=self.champ_de_galois.index(a)
            q=self.champ_de_galois.index(b)
            if p+q>255:
                r=(p+q)%255
                return self.champ_de_galois[r]
            else:
                r=p+q
                return self.champ_de_galois[r]
         else:
             return 0
    #Pour l'addition on pourra utiliser la fonction booleenne XOR du module operator.
    #les operations algébriques étant définies , on peut définir le produit de deux polynomes à coefficient dans ce corps de Galois
    #Ce principe nous aidera pour calculer le polynome generateur....
    #produit scalaire
    def ProduitScalaireDansGF(self,u,tv,k):
        sum=0
        for i in range (k+1):
            sum=xor(sum,self.MultiDansGF(u[i],tv[k-i]))
        return sum

    # On definit une fonction qui donne l'inverse d'un élément dans GF(256)
    def InverseDansGF(self,a):
        p=self.champ_de_galois.index(a)
        inverse_de_a=self.champ_de_galois[255-p]
        return inverse_de_a

    #On définit une fonction qui additionne deux polynomes.
    def AddPolynome(self,P,Q):
        n=len(P)
        m=len(Q)
        ecart=n-m
        poly=[]
        if ecart>0:
            for i in range(m):
                poly.append(xor(P[i],Q[i]))
            for i in range(m,n):
                poly.append(xor(P[i],0))
            return poly
        elif ecart<0:
            for i in range(n):
                poly.append(xor(P[i], Q[i]))
            for i in range(n,m):
                poly.append(xor(Q[i],0))
            return poly
        else:
            for i in range(n):
                poly.append(xor(P[i], Q[i]))
            return poly

    #On definit le produit de deux polynome ( les degres sont controles ) dans GF(256)
    def ProduitPolynome(self,P,Q,p):
        nombreDezero=len(Q)-len(P)
        for i in range(nombreDezero):
            P.append(0)
        produit=[]
        for j in range(p+1):
            sum=0
            for i in range (j+1):
                sum=xor(sum,self.MultiDansGF(P[i],Q[j-i]))
            produit.append(sum)
        return produit

    #Cette fonction est fondamentale pour obtenir la chaine de format.
    def MiseAJour(self,k,i,var):
        #Quotient.append( k[i+1])
        k[i+1]=0
        k[i]=var
        return k

    #Cette fonction annule les premieres zeros du polynome pour obtenir son degre
    def DegreDupolynome(self,value):
        assert len(value)>0
        compteur=0
        for i in range(len(value)):
            if value[i]==0:
                    compteur+=1
        if compteur==len(value):
            return -1
        element=value[::-1]
        a=[0 for i in range(len(element))]
        for i in range(len(element)):
            a[i]=element[i]
            if a[i]!=0:
                return len(element)-i-1

    #Cette fonction fait le produit d'un scalaire et d'un polynome vu comme un vecteur.
    def ProduitExterieur(self,value,Poly,n):
        produit_par_scalaire=[]
        for i in range(n+1):
            produit_par_scalaire.append(self.MultiDansGF(value,Poly[i]))
        return produit_par_scalaire

    #Cette fonction supprime les premiers zeros d'une liste.
    def SupprimeZeros(self,chaine):
        assert chaine!=[]
        compteur=0
        while 1:
            if not chaine[0]:
                del chaine[0]
                compteur+=1
            else:
                 break
            if len(chaine)==0:
                break
        return compteur

    #cette fonction addition deux polynomes, on envoie le même degré pour simplifier.
    def AddPolynome2(self,P,Q,n):
        try:
            assert len(P)==len(Q) and len(Q)==n
        except AssertionError:
            return -1
        poly=[]
        for i in range(n):
                poly.append(xor((P[i]),(Q[i])))
        return poly

    #Cette fonction nous sert de contrainte lors du remplissage des données dans la matrices
    def InModuleReserver(self,i,j,version):
        intrusion = 0
        taille_QRcode = ((version - 1) * 4 + 21)
        tester=[]
        bool1= (0<=i<8 and 0<=j<8) #finder patterns en haut à gauche
        tester.append(bool1)
        bool2=(taille_QRcode-8<=i<taille_QRcode) and (0<=j<8)#finder en bas à gauche
        tester.append(bool2)
        bool3=(0<=i<8) and (taille_QRcode-8<=j<taille_QRcode)#finder patterns en haut à droit
        tester.append(bool3)
        bool4= (i==4 * version + 9 and j==8) #Dark module
        tester.append(bool4)
        bool5=(i==6 or j==6)#module de synchronisation
        tester.append(bool5)
        bool6= (j==8 and (0<=i<=5 or 7<=i<=8 or taille_QRcode-7<=i<taille_QRcode))#information sur le format
        tester.append(bool6)
        bool7= (i==8 and (0<=j<=5 or 7<=j<=8 or taille_QRcode-8<=j<taille_QRcode))#information sur le format
        tester.append(bool7)
        #On controle les patterns d'alignement
        if version>1:
            positionDesPatternsAlignement={2:(6,18),8:(6,24,42),30:(6,26,52,78,104,130),40:(6,30,58,86,114,142,170)}
            # pour la version 2 le module centrale est a la position (18,18) par exemple.
            Lespositions=positionDesPatternsAlignement[version]
            for l in Lespositions:
                for k in Lespositions:
                    bool = (l == 6 and (k == 6 or k == taille_QRcode - 7)) or (k == 6 and (l == 6 or l== taille_QRcode - 7))
                    if not bool:
                        bool8=(l-2<=i<l+3) and (k-2<=j<k+3)
                        tester.append(bool8)
        #si la version est superieure ou egale a 7 on controle la zone d'information sur la version
        if version>6:
            bool9=(4*version+6<=i<4*version+9) and (0<=j<6)
            tester.append(bool9)
            bool10 = (0<=i<6) and (taille_QRcode - 11<=j <taille_QRcode - 8)
            tester.append(bool10)
        #On verifie le nombre de fois qu'on franchit une zone interdite.
        for i in range(len(tester)):
            if tester[i]==True:
                intrusion+=1
        #Si on a franchi au moins une fois on alerte! Attention! zone reservée.
        if intrusion>=1:
            return False
        else:
            return True

    #Cette fonction nous permet d'appliquer le masque selon le type ( on a 8 exactement)
    def Masque(self,donne,version):
        for i in range(len(donne)):
            for j in range(len(donne)):
                if self.InModuleReserver(i,j,version):
                    #test = (i+j)%2 #0
                    #test=i%2 #1
                    #test=j%3 #2
                    #test=(i+j)%3 #3
                    #test= (int(i/2)+ int(j/3))%2 #4
                    #test = (i*j)%2 + (i*j)%3 #5
                    test = ((i * j) % 2 + (i * j) % 3)%2 #6
                    #test= ((i+j)%2 + (i*j)%3)%2 #7
                    if not test:
                        donne[i,j]=xor(1,int(donne[i,j]))
                else:
                    pass
    #cette fonction determine le polynome generateur
    def Generateur(self,message):
        versionNiveau = self.VersionETNiveauCorrection(message)
        CapaciteECBloc = self.CapaciteECBloc(versionNiveau[0], versionNiveau[1])
        degreNecessaire = CapaciteECBloc[1]
        # Calcul du polynome générateur comme produit de polynomes....
        # On va regarder nos polynome comme un vecteur qui s'annule a partir d'un certain rang
        # Nous commencons avec des polynomes qui ont une structure bien connues: 2^j et 1
        # on définit la fonction générateur
        generateur = [1, 1, 0]
        # on définit un vecteur qui nous permettra de faire la recurrence
        vecteur = [2, 1, 0]
        phantom = []
        # la suite consiste à faire le produit scalaire a chaque iteration et de faire une mise a jour du generateur.
        for i in range(1, degreNecessaire):
            # pour chaque itération on calcule le produit de deux polynomes de dégre 1 et 2.
            for k in range(i+2):
                phantom.append(self.ProduitScalaireDansGF(vecteur, generateur, k))
            # Mise à jour de generateur: on ajoute zero a la fin et on actualise ses premieres valeurs
            generateur.append(0)
            for k in range(i + 2):
                generateur[k] = phantom[k]
            # Mise à jour de vecteur pour le produit suivant;
            vecteur.append(0)
            vecteur[0] = self.champ_de_galois[i+1]
            # on nettoie le phantom et on recommence le processus...
            phantom.clear()
        # À la sortie de cette boucle on supprime le dernier élement pour avoir  le polynome générateur
        long = len(generateur) - 1
        generateur.pop(long)
        return generateur

    #cette fonction determine le mode d'encodage.
    def IndicateurDemode(self, message):
        indicateurDeMode = [("num", "0001"), ("alph", "0010"), ("ascii", "0100")]
        verification=0
        num = message.isnumeric()
        alph = message.isalnum()
        ascii = message.isascii()
        tester = [num, alph, ascii]
        for i in range(3):
            if tester[i]:
                return indicateurDeMode[i]
                break
            else:
                verification+=1
        assert verification==0

    def IndicateurNombreCaractere(self,message):
        valeurDeReference = [9, 26, 40]
        NombreBitParVersionbloc = [{"num": 10, "alph": 9, "ascii": 8}, {"num": 12, "alph": 11, "ascii": 16},{"num": 14, "alph": 13, "ascii": 16}]
        version = self.VersionETNiveauCorrection(message)
        version = version[0]
        for i in range(3):
            if version <= valeurDeReference[i]:
                mode = self.IndicateurDemode(message)
                mode = mode[0]
                return NombreBitParVersionbloc[i][mode]
                break

    def ConvertirEnBinaire(self,message):
        taille_message = len(message)
        # transcription du message selon la norme Ascii. on donne l'équivalent de chaque caractére en code Ascii.
        ascii_number = []
        for k in range(taille_message):
            ascii_number.append(ord(message[k]))
        # Encodage des données en base binaire; on ajoute 0 à gauche si la longueur est inférieure à 8.
        binary_message = []
        for k in range(taille_message):
            if len(format(ascii_number[k], "b")) < 8:
                vars = str(format(ascii_number[k], "b"))
                kr = 8 - len(format(ascii_number[k], "b"))
                for i in range(kr):
                    vars = "0" + vars
                binary_message.append(vars)
                del vars
            else:
                binary_message.append(str(format(ascii_number[k], "b")))
        return binary_message

    #cette fonction convertit une liste d'entier en binaire
    def EntierEnBinaire(self, ListeEntiere):
        binary_message=[]
        taille=len(ListeEntiere)
        for k in range(taille):
            if len(format(ListeEntiere[k], "b")) < 8:
                vars = str(format(ListeEntiere[k], "b"))
                kr = 8 - len(format(ListeEntiere[k], "b"))
                for i in range(kr):
                    vars = "0" + vars
                binary_message.append(vars)
                del vars
            else:
                binary_message.append(str(format(ListeEntiere[k], "b")))
        return binary_message

    def EncodageDesDonnees(self,message):
        taille_message = len(message)
        binary_message=self.ConvertirEnBinaire(message)
        # ......................................PRINCIPE DE COMPLETION DU MESSAGE......................................#
        # On convertir le  nombre de caractères en binaire suivant la version.
        nombreBitRequis = self.IndicateurNombreCaractere(message)
        id_mode = format(taille_message, "b")
        taille_Idmode = len(id_mode)
        if taille_Idmode < nombreBitRequis:
            r = nombreBitRequis - taille_Idmode
            for k in range(r):
                id_mode = "0" + str(id_mode)
        # Ajout de l'Indicateur de mode: indicateur de nombre de caractères.
        bit_fort = []
        mode = self.IndicateurDemode(message)
        mode=mode[1]
        bit_fort.append(mode)
        bit_fort.append(id_mode)
        bit_fort.extend(binary_message)
        binary_message = bit_fort
        # on ajoute des bits de terminaison si la longueur est inferieure de plus de 4 bits: "0000"
        versionNiveau=self.VersionETNiveauCorrection(message)
        CapaciteECBloc=self.CapaciteECBloc(versionNiveau[0],versionNiveau[1])
        NombreTotalDeBit=CapaciteECBloc[0]
        New_taille_m = len("".join(binary_message))
        if NombreTotalDeBit * 8 - New_taille_m > 4:
            binary_message.append("0000")
        else:  # On complete jusqu'a atteindre la taille maximale.
            p = NombreTotalDeBit * 8 - New_taille_m
            for k in range(p):
                binary_message.append("0")

        # on ajoute des zeros pour avoir un multiple 8
        j = len("".join(binary_message))
        if 8*int(j/8)+8-j>0:
            k=8*int(j/8)+8-j
            for i in range(k):
                binary_message.append("0")
        # Ajout de l'octet de remplissage afin d'atteindre la taille maximale: "11101100" "00010001", 236,17
        j=len("".join(binary_message))
        if (NombreTotalDeBit * 8 - j) > 0:
             nombre_Octots_Remplissage = int((NombreTotalDeBit*8-j)/8)
             list_const = ["11101100", "00010001"]*nombre_Octots_Remplissage
             for k in range(nombre_Octots_Remplissage):
                 binary_message.append(list_const[k])
        # On recupere le message binaire.
        data_encoding = "".join(binary_message)  # message à coder ou message d'information en bits.
        return data_encoding

   p(self,message, data_encoding):
        blocs=[]
        poly= []
        var= []
        positionCloison=self.ObtentionPositionblocs(message)
        lgPosition=len(positionCloison)-1 # on compter le nombre d'intervalle
        for j in range(lgPosition):
            poly=[]
            for i in range(positionCloison[j]-1,positionCloison[j+1]-1):
                for k in range(8 * i, 8 * i + 8):
                    var.append(data_encoding[k])
                poly.append((int("".join(var), 2)))
                var.clear()
            blocs.append(poly)
        return blocs

    def ObtentionPositionblocs(self,message):
        description = ["capacité", "EC", "NbreBlocGrp1", "NbreMotgrp1", "NbreBlocGrp2", "NbreMotgrp2"]
        versionNiveau = self.VersionETNiveauCorrection(message)
        CapaciteECBloc = self.CapaciteECBloc(versionNiveau[0], versionNiveau[1])
        positionCloison = []
        for i in range(CapaciteECBloc[2]):
            positionCloison.append((i+1)*CapaciteECBloc[3]+1)
        for i in range(CapaciteECBloc[4]):
            positionCloison.append(CapaciteECBloc[2]*CapaciteECBloc[3] + (i+1)* CapaciteECBloc[5]+1)
        positionCloison.insert(0,1)

        return positionCloison

    def AjouteZero(self,P,nombreZero):
        for i in range(nombreZero):
            P.append(0)
        return P

    def Dividende(self,poly_information,degreGenerateur):
        werty = [0]*(degreGenerateur+1)
        werty[degreGenerateur] = 1
        dividende = self.ProduitPolynome(werty, poly_information,len(poly_information)-1) #43
        return dividende

    def DegreMultiplicateur(self,dividende,diviseur):
        degre_dividende = self.DegreDupolynome(dividende)  # on definit formellement le degre plutart
        degre_diviseur = self.DegreDupolynome(diviseur)  # on definit formellement le degre plutart
        degre_multiplicateur = degre_dividende - degre_diviseur  # 23-16
        if degre_multiplicateur>=0:
            multiplicateur = [0]*(degre_multiplicateur+1)
            # On definit le multiplicateur pour la premiere itertion....
            multiplicateur[degre_multiplicateur] = self.MultiDansGF(self.InverseDansGF(diviseur[degre_diviseur]),
                                                                    dividende[degre_dividende])
            return multiplicateur
        else:
            return []

    def DivisionEuclidienne(self,poly_information,generateur):
        poly_information.reverse()
        degreGenerateur=len(generateur)-1
        poly_information=poly_information
        lgPolyInformation=len(poly_information)
        # on augmente les zeros au polynome generateur pour avoir la même taille que le polynome d'information
        diviseur=self.AjouteZero(generateur,lgPolyInformation-1)
       # on prepare le polynome message
        for i in range(degreGenerateur):
            poly_information.append(0)
        # On multiplie le polynome d'information par un monome de degré le nombre de mots de correction d'erreurs
        dividende=self.Dividende(poly_information,degreGenerateur)
        # On commence la division longeur, tous les ingrédients sont disponbles
        constDegre=len(diviseur)-1
        # On commence la division longue.
        multiplicateur=self.DegreMultiplicateur(dividende,diviseur)
        while 1:  # on fait la division le nombre de fois qu'on a besion des mots correcteurs.
            produit = self.ProduitPolynome(multiplicateur, diviseur,constDegre)
            residu = self.AddPolynome(dividende,produit)
            dividende = residu
            multiplicateur=self.DegreMultiplicateur(dividende,diviseur)
            if len(multiplicateur)==0:
                break
            else:
                pass
        # Le residu est le reste de la division du polynome d'information par le polynome generateur
        for i in range(lgPolyInformation):
            residu.pop()
        residu.reverse()
        #on supprime les premiers zeros s'il y en a
        Errors_Coding_Corrector = residu
        for i in range(degreGenerateur):
            poly_information.pop()
        # Maintenant qu'on a le mot correcteur d'erreur, on peut continuer aisement...
        poly_information.reverse()
        # On supprime les zeros du generateur
        generateur.reverse()
        for i in range(lgPolyInformation-1):
            generateur.pop(0)
        generateur.reverse()
        return  Errors_Coding_Corrector

    def DivisionMultiple(self,blocsPolynome,generateur):
        nombre_de_Division=len(blocsPolynome)
        return [self.DivisionEuclidienne(blocsPolynome[i],generateur) for i in range(nombre_de_Division)]


    def BitPourLeNiveauVersion(self,Niveau):
        MajNiveau = Niveau.upper()
        NiveauDeCorrectionErreur = {"L": "01", "M": "00", "Q": "11", "H": "10"}
        for cle in NiveauDeCorrectionErreur.keys():
            if cle == MajNiveau:
                MajNiveau = NiveauDeCorrectionErreur[cle]
                break
        return MajNiveau

    def InfoSurLeFormat(self,choix_du_masque, Niveau):
        chaine_information_format = []
        numero_de_masque = []
        #Faire un algorithme qui determine la masque
        masque = format(choix_du_masque, 'b')
        for i in range(len(masque)):
            numero_de_masque.append(masque[i])
        if len(numero_de_masque) < 3:
            r = 3 - len(numero_de_masque)
            for i in range(r):
                numero_de_masque.insert(0, '0')

        bit_niveau_correction_erreur =self.BitPourLeNiveauVersion(Niveau)
        longueur = len(bit_niveau_correction_erreur)
        for i in range(longueur):
            numero_de_masque.insert(0, bit_niveau_correction_erreur[longueur - i - 1])
        # information sur le masquage et le niveau de codage de d'erreur
        info_format = []
        for i in range(len(numero_de_masque)):
            info_format.append(int(numero_de_masque[i]))

        # on prepare la chaine d'information en completant le nombre de zero.
        for i in range(15 - len(info_format)):
            info_format.append('0')
        for i in range(15):
            chaine_information_format.append(int(info_format[i]))
        # suppresion des zeros de gauches..
        self.SupprimeZeros(chaine_information_format)
        if len(chaine_information_format):
            # On supprime les zeros de chaine info
            for i in range(len(info_format) - 5):
                info_format.pop()
            # polynome generateur pour obtenir le code de correction d'erreurs
            g = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1] # convention
            diviseur2 = []
            diviseur2 = g
            x = len(chaine_information_format) - len(diviseur2)
            if x > 0:
                for i in range(x):
                    diviseur2.append(0)
        # division euclidienne pour extraire le correcteur de code
        resultat = []
        if len(chaine_information_format):
            while 1:
                resultat = self.AddPolynome2(chaine_information_format, diviseur2, len(diviseur2))
                self.SupprimeZeros(resultat)
                chaine_information_format = resultat
                if x != 0:
                    for i in range(x):
                        diviseur2.pop()
                x = len(chaine_information_format) - len(diviseur2)
                # on fait une mise a jour de g.
                if x > 0:
                    for i in range(x):
                        diviseur2.append(0)
                elif x == 0:
                    pass
                else:
                    break
        # a la fin il faut remplir le resultat par des zeros a gauches pour avoir une longueur de 10.
        if len(chaine_information_format):
            if len(chaine_information_format) < 10:
                sd = 10 - len(chaine_information_format)
                for i in range(sd):
                    chaine_information_format.insert(0, 0)
            # Assembler le bit de format et la correction d'erreur
            info_format.extend(chaine_information_format)
        if not len(chaine_information_format):
            chaine_format_final = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        else:
            chaine_de_masque = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
            chaine_format_final = self.AddPolynome2(chaine_de_masque, info_format, 15)

        return chaine_format_final
        # pour les petits version en n'a pas besoin des chaines d'information sur la version.

    def Entrelacement(self,donnees):
        taille_donnees=len(donnees)
        #on cherche la composante la plus longue
        taille_elt1=len(donnees[0])
        for i in range(taille_donnees):
            if len(donnees[i])>taille_elt1:
                taille_elt1=len(donnees[i])
        #on commence l'entrelacement
        donneesEntrelacees=[]
        for j in range(taille_elt1):
            for i in range(taille_donnees):
                try:
                    donneesEntrelacees.append(donnees[i][j])
                except IndexError:
                    continue
        return donneesEntrelacees

    def Ordonne(self,donnees):
        donnees1=[]
        taille_donnees = len(donnees)
        for i in range(taille_donnees):
            donnees[i].reverse()
            donnees1.append(donnees[i])
        return donnees1

    def CodeReedSolomon(self,DonneeEntrelacees, CodeCorrestionErreur,version):
        DonneeEntrelacees1=self.EntierEnBinaire(DonneeEntrelacees)
        CodeCorrestionErreur1 = self.EntierEnBinaire(CodeCorrestionErreur)
        #Ajout des bits necessaire
        BitParVersion={1:0,2:7,8:0,30:3,40:0}
        nombreBit=BitParVersion[version]
        bit=[]
        for i in range(nombreBit):
            bit.append("0")
        Final_Message = "".join(DonneeEntrelacees1) + "".join(CodeCorrestionErreur1)+\
                        "".join(bit)
        return Final_Message

    def MatriceQRcode(self,chaine_format_final,version):
        # On utilisera essentiellement la bibliothèque numpy pour la manipulation des matrices
        # On calcule la taille du QRcode en fonction de la version.
        taille_QRcode = ((version - 1) * 4 + 21)
        data_matrix = numpy.zeros((taille_QRcode, taille_QRcode))
        finder_patterns = numpy.zeros((7, 7))
        finder_patterns[:, 0] = [1 for i in range(7)]
        finder_patterns[:, 6] = [1 for i in range(7)]
        finder_patterns[0, :] = [1 for i in range(7)]
        finder_patterns[6, :] = [1 for i in range(7)]
        finder_patterns[2:5, 2:5] = numpy.ones((3, 3))
        # on place les modules de recherche dans la matrice data.
        # Premiere modules de recherche
        data_matrix[0:7, 0:7] = finder_patterns
        # deuxieme modules de recherche
        data_matrix[taille_QRcode - 7:taille_QRcode, 0:7] = finder_patterns
        # troisieme modules de recherche
        data_matrix[0:7, taille_QRcode - 7:taille_QRcode] = finder_patterns
        # Ajout des separateur:De la facon dont on a initialiser notre matrice cela se ferra a postiori
        # Ajout des motifs d'alignement:
        Alignement_patterns = numpy.zeros((5, 5))
        Alignement_patterns[:, 0] = [1 for i in range(5)]
        Alignement_patterns[:, 4] = [1 for i in range(5)]
        Alignement_patterns[0, :] = [1 for i in range(5)]
        Alignement_patterns[4, :] = [1 for i in range(5)]
        Alignement_patterns[2, 2] = 1
        # on place le module d'alignement dans la matrice data
        if version>1:
            positionDesPatternsAlignement={2:(6,18),8:(6,24,42),30:(6,26,52,78,104,130),40:(6,30,58,86,114,142,170)}
            # pour la version 2 le module centrale est a la position (18,18)
            Lespositions=positionDesPatternsAlignement[version]
            for i in Lespositions:
                for j in Lespositions:
                    bool=(i==6 and (j==6 or j==taille_QRcode-7)) or (j==6 and (i==6 or i==taille_QRcode-7))
                    if not bool:
                        data_matrix[i-2:i+3, j-2:j+3] = Alignement_patterns
        else:
            pass
        # Ajout des modèles de synchronisation.
        for i in range(8, taille_QRcode - 8):
            if not i % 2:
                data_matrix[6, i] = 1
        for i in range(8, taille_QRcode - 8):
            if not i % 2:
                data_matrix[i, 6] = 1

        # Ajout du module sombre et de la zone reservées
        position_module_sombre = (4 * version + 9, 8)
        data_matrix[position_module_sombre] = 1

        # Ajout de la chaine d'information sur le format.
        for i in range(8):
            if i >= 6:
                data_matrix[8, i + 1] = chaine_format_final[i]
            else:
                data_matrix[8, i] = chaine_format_final[i]
        for i in range(7):
            if i >= 6:
                data_matrix[i + 1, 8] = chaine_format_final[14 - i]
            else:
                data_matrix[i, 8] = chaine_format_final[14 - i]
        # ajout du deuxieme bloc
        for i in range(7):
            data_matrix[taille_QRcode - i - 1, 8] = chaine_format_final[i]
        for i in range(8):
            data_matrix[8, taille_QRcode - i - 1] = chaine_format_final[14 - i]
        #Ajout de l'information sur la version si version >6
        if version>6:
            informationVersion=self.InfoSurLaVersion(version)
            informationVersion.reverse()
            for j in range(6):
                for i in range(4*version+6,4*version+9):
                    data_matrix[i,j]=informationVersion[0]
                    informationVersion.pop(0)
             # ajout du deuxieme bloc
            informationVersion1 = self.InfoSurLaVersion(version)
            informationVersion1.reverse()
            for i in range(6):
                for j in range(taille_QRcode - 11,taille_QRcode - 8):
                    data_matrix[i,j]=informationVersion1[0]
                    informationVersion1.pop(0)
        return data_matrix

    def Remplissage_ZIG_ZAG(self,data_matrix,Final_Message,version):
        compteur=0
        taille_QRcode = ((version - 1) * 4 + 21)
        lachaine = Final_Message
        var = len(lachaine)
        lis = []
        for i in range(var):
            lis.append(int(lachaine[i]))

        sens = 1
        for j in range(1,taille_QRcode-1, 2):
            if j <= taille_QRcode-8:  # si on n'a pas encore atteint le timing patterns, le remplissage en zig zag est normal
                zig_zag = sens % 2
                if zig_zag:
                    for i in range(taille_QRcode):
                        if self.InModuleReserver(taille_QRcode-1- i, taille_QRcode - j,version):
                            data_matrix[taille_QRcode-1 - i, taille_QRcode - j] = lis[0]
                            compteur += 1
                            lis.pop(0)

                        if self.InModuleReserver(taille_QRcode-1  - i, taille_QRcode-1 - j,version):
                            data_matrix[taille_QRcode-1  - i, taille_QRcode-1 - j] = lis[0]
                            compteur += 1
                            lis.pop(0)

                else:
                    for i in range(taille_QRcode):
                        if self.InModuleReserver(i, taille_QRcode- j,version):
                            data_matrix[i, taille_QRcode - j] = lis[0]
                            compteur += 1
                            lis.pop(0)

                        if self.InModuleReserver(i, taille_QRcode-1- j,version):
                            data_matrix[i, taille_QRcode-1- j] = lis[0]
                            compteur += 1
                            lis.pop(0)

            #  sinon On change la facon de remplir.
            else:
                zig_zag = sens % 2
                if zig_zag:
                    for i in range(taille_QRcode):
                        if self.InModuleReserver(taille_QRcode-1 - i, taille_QRcode-1 - j,version):
                            data_matrix[taille_QRcode-1- i, taille_QRcode-1 - j] = lis[0]
                            compteur += 1
                            lis.pop(0)
                        if self.InModuleReserver(taille_QRcode-1 - i, taille_QRcode-2 - j,version):
                            data_matrix[taille_QRcode-1 - i, taille_QRcode-2 - j] = lis[0]
                            compteur += 1
                            lis.pop(0)
                else:
                    for i in range(taille_QRcode):
                        if self.InModuleReserver(i, taille_QRcode-1-j,version):
                            data_matrix[i, taille_QRcode-1- j] = lis[0]
                            compteur += 1
                            lis.pop(0)
                        if self.InModuleReserver(i, taille_QRcode-2- j,version):
                            data_matrix[i, taille_QRcode-2- j] = lis[0]
                            compteur += 1
                            lis.pop(0)

            sens += 1


    def Plot(self,data_matrix,name):
        fig=plt.figure(dpi=300)
        plt.imshow(data_matrix, cmap='Greys')
        plt.axis('off')
        #plt.show()
        fig.savefig(name, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

    def VersionETNiveauCorrection(self, message):
        #cette partie doit etre optimisee.
        longmessage=len(message)
        differenteVersion=[1,2,8,30,40]
        NiveauDeCorrectionErreur = [{"H":7,"Q":11,"M":14,"L":17},{"H":14,"Q":20,"M":26,"L":32},
                                    {"H":84,"Q":108,"M":152,"L":192},{"H":742,"Q":982,"M":1370},
                                    {"H":1273,"Q":1663,"M":2331,"L":2953}]
        for i in range(5):
            for value1 in NiveauDeCorrectionErreur[i].items():
                if longmessage<= value1[1]:
                    NiveauCorrestion =value1[0]
                    version=differenteVersion[i]
                    return version,NiveauCorrestion
                    break
                else:
                    pass

    def CapaciteECBloc(self,version,NiveauCorrection):
        description=["capacité","EC","NbreBlocGrp1","NbreMotgrp1","NbreBlocGrp2","NbreMotgrp2"]
        differenteVersion = [1, 2, 8, 30, 40]
        NiveauDeCorrectionErreur = [{"H": (9,17,1,9,0,0), "Q": (13,13,1,13,0,0), "M": (16,10,1,16,0,0), "L":(19,7,1,19,0,0)}, {"H": (16,28,1,16,0,0), "Q": (22,22,1,22,0,0), "M": (28,16,1,28,0,0), "L": (34,10,1,34,0,0)},
                                    {"H": (86,26,4,14,2,15), "Q": (110,22,4,18,2,19), "M": (154,22,2,38,2,39), "L": (194,24,2,97,0,0)}, {"H": (745,30,23,15,25,16), "Q": (985,30,15,24,25,25), "M": (1373,28,19,47,10,48), "L": (1735,30,5,115,10,116)},
                                    {"H": (1276,30,20,15,61,16), "Q": (1666,30,34,24,34,25), "M": (2334,28,18,47,31,48), "L": (2956,30,19,118,6,119)}]
        indiceVersion=differenteVersion.index(version)
        return NiveauDeCorrectionErreur[indiceVersion][NiveauCorrection]

    def InfoSurLaVersion(self,version):
        chaine_information_version = []
        version= format(version, 'b')
        for i in range(len(version)):
            chaine_information_version.append(int(version[i]))
        if len(chaine_information_version) < 6:
            r = 6 - len(chaine_information_version)
            for i in range(r):
                chaine_information_version.insert(0, 0)
        info=[]
        for i in range(6):
            info.append(chaine_information_version[i])
        # on prepare la chaine d'information en completant le nombre de zero.
        for i in range(18 - len(chaine_information_version)):
            chaine_information_version.append(0)
        # suppresion des zeros de gauches..
        self.SupprimeZeros(chaine_information_version)
        # polynome generateur pour obtenir le code de correction d'erreurs
        g = [1,1,1,1,1,0,0,1,0,0,1,0,1] # convention
        diviseur2 = []
        diviseur2 = g
        x = len(chaine_information_version) - len(diviseur2)
        if x > 0:
            for i in range(x):
                diviseur2.append(0)
        # division euclidienne pour extraire le correcteur de code
        resultat = []
        if len(chaine_information_version):
            while 1:
                resultat = self.AddPolynome2(chaine_information_version, diviseur2, len(diviseur2))
                self.SupprimeZeros(resultat)
                chaine_information_version = resultat
                if x != 0:
                    for i in range(x):
                        diviseur2.pop()
                x = len(chaine_information_version) - len(diviseur2)
                # on fait une mise a jour de g.
                if x > 0:
                    for i in range(x):
                        diviseur2.append(0)
                elif x == 0:
                    pass
                else:
                    break
        # a la fin il faut remplir le resultat par des zeros a gauches pour avoir une longueur de 12.

        if len(chaine_information_version) < 12:
            sd = 12 - len(chaine_information_version)
            for i in range(sd):
                chaine_information_version.insert(0, 0)

        # Assembler le bit de version et la correction d'erreur
        info.extend(chaine_information_version)
        return info
        # pour les petits version en n'a pas besoin des chaines d'information sur la version.



if __name__ == '__main__':
    command=QRcode()
    print ("\n>>> Le champ de Galois:\n")
    print(command.champ_de_galois)
