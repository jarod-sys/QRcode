#coding: utf-8

#...................................MODULES IMPORTANTS................................................#


import fonctions


class ProjetQrcode():
    def __init__(self):
        self.msg=""
        self.namefile=""
    #.............................................DEBUT DU PROGRAMME.......................................................#

    #........................................CREATION D'UN OBJET QRcode....................................................#

        self.command=fonctions.QRcode()

    def Set_message(self,msg):
        self.msg=msg
    def Set_namefile(self,name):
        self.namefile=name


    def Run(self):

        message = self.msg
        # .............................CHOIX DE LA VERSION ET DU NIVEAU DE CORRECTION D'ERREUR ..................................#

        version_NiveauCorrection=self.command.VersionETNiveauCorrection(message)
        print("La version:{}\nNiveau de correction d'erreur:{}".format(version_NiveauCorrection[0],version_NiveauCorrection[1]))

        #..................................OBTENTION DU MESSAGE A CODER EVENTUELLEMENT PAR BLOCS...............................#


        data_encoding=self.command.EncodageDesDonnees(message)


        blocsDonnees=self.command.DivisionEnBloc(message,data_encoding)


        #...............................................POLYNOME GENERATEUR....................................................#

        generateur=self.command.Generateur(message)

        #.......................DIVISION EUCLIDIENNE DANS GF(256): POUR OBTENIR EC PAR BLOCS...................................#

        Errors_Coding_Corrector=self.command.DivisionMultiple(blocsDonnees,generateur)

        #.......................................................ENTRELACEMENT..................................................#

        DonneeEntrelacees=self.command.Entrelacement(blocsDonnees)

        CodeCorrestionErreur=self.command.Entrelacement(Errors_Coding_Corrector)


        chaine_format_final=self.command.InfoSurLeFormat(6,version_NiveauCorrection[1])

        #..........................................MESSAGE COMPLET: CODE DE REED SOLOMON.......................................#


        Final_Message=self.command.CodeReedSolomon(DonneeEntrelacees,CodeCorrestionErreur,version_NiveauCorrection[0])


        #..........................................CREATION DE LA MATRICE DU QRCODE............................................#

        data_matrix=self.command.MatriceQRcode(chaine_format_final,version_NiveauCorrection[0])

        #..............................................REMPLISSAGE EN ZIG ZAG..................................................#

        self.command.Remplissage_ZIG_ZAG(data_matrix,Final_Message,version_NiveauCorrection[0])

        #..............................................APPLICATION DU MASQUE ET AFFICHAGE......................................#

        self.command.Masque((data_matrix),version_NiveauCorrection[0])

        #................................................... AFFICHAGE.......................................................#

        self.command.Plot(data_matrix,self.namefile)

        #..............................................FIN DU PROGRAMME........................................................#


if __name__ == '__main__':
    print("Programme terminé avec succes")






































