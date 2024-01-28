#coding: utf-8

from projet import ProjetQrcode

from sys import argv


num=int(argv[1])
qrcode=ProjetQrcode()
#Sur le cluster on a 10 jobs; de 1 à 10.
if 1<=num<=10:
    with open("list.txt","r") as f:
        position_curseur=1
        while position_curseur<=1000*(num-1):
            f.readline()
            position_curseur+=1

        while 1000*(num-1)<position_curseur<=1000*num:
            message=f.readline()
            print(position_curseur)
            qrcode.Set_message(message)
            namefile="file/QRcode{}".format(position_curseur)
            qrcode.Set_namefile(namefile)
            qrcode.Run()
            position_curseur+=1
    print("programme termine avec succes!")
#En local entrez comme argument 0.
elif num==0:
    qrcode=ProjetQrcode()
    msg=input("Entrez un message:")
    qrcode.Set_message(msg)
    qrcode.Set_namefile("QRcodeTest")
    qrcode.Run()
else: 
    print("Argument non valide")


