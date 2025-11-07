| IP              | HOSTNAME         | PASSWORD |
| --------------- | ---------------- | -------- |
| 192.168.170.142 | tls-ca-mautie    | mautie   |
| 192.168.170.116 | tls-serv-mautie  | mautie   |
| 192.168.170.141 | tls-ca-mauryco   | mauryco  |
| 192.168.170.115 | tls-serv-mauryco | mauryco  |

**Question 1:**

1. Calcul de chiffrement des messages en utilisant RSA: $M = C^d(mod n)$
2. La méthode de Diffie-Hellman permet la vérification d'identité dans un système.
3. Un certificat contient la signature du fournisseur de certificat, la clé publique de la cible du certificat, l'adresse de la machine contenant la clé privé de la cible du certificat et les infos de vérification.
4. étapes:
  1. Récupération du certificat d'alice
  2. Récupération du certificat de root-ca
  3. vérification 

5. La longueur de n est de 1024 bits. n = p * q
Rappel des calculs pour chiffrer un message M

On a les clés :
Clé publique : (n, e)
Clé privée : (n, d)

Chiffrement: 𝐶 = 𝑀<sup>𝑒</sup> mod 𝑛

où :
M est le message converti en nombre,
e est l’exposant public,
C est le message chiffré.

Déchiffrement: 𝑀 = 𝐶<sup>𝑑</sup> mod n

où :
d est l’exposant privé.
Le "publicExposant" n'est pas difficile à deviner pour un pirate car il n'est pas secret, il est public. Mais ce n'est pas un problème car la sécurité repose sur la difficulté de factoriser n pour retrouver p et q, et donc d.

6. Il ne faut pas chiffré la clé publique, la privée doit être chiffré pour éviter qu'une personne n'utilise la clé dès qu'il a voler la machine.
7. L'encode utilisé pour la clé est l'encodage PEM, il a pour avantage qu'il est facile à stocker dans des fichiers txt.
8. Dans le fichier de la clé publique, nous retrouvons n et e. Il est intéressant de disposer d'un fichier ne contenant que la clé publique afin que d'autres personnes puisses chiffrer avec cette clé sans comprometre la clé privée.
9. La clé publique du destinataire de notre message doit être utilisé afin de pouvoir chiffré le message en question.
10. 
```bash
openssl pkeyutl -encrypt -pubin -inkey pub.mauryco.pem -in clair.txt -out cipher.bin -pkeyopt rsa_padding_mode:pkcs1
```
est la fonction permettant de chiffrer un message dans `clair.txt` à destination du propriétaire de la clé privé de la clé publique `pub.mauryco.pem`.

11.  Les fichiers sont différents et c'est normal car il y a de l'aléatoire lorsque l'on chiffre un message.

12.  L'option permet d'afficher le certificat du server. Ici il est en a 3.

13.  x509 est le format standard international pour les certificats numériques. Le sujet du certificat est Université Grenoble Alpe.
C=Pays
ST=Province
L=Ville
O=Organisation
CN=Common Name
L'organisation qui a fourni le contrat est GEANT Verenining.

14.  i: issuer, s: subject 

15. Le certificat contient la clé publique associée à la clé privée du serveur. Il a été signé avec l’algorithme sha384WithRSAEncryption. L’attribut CN (Common Name) indique le nom de domaine principal pour lequel le certificat est valide, ici [www.univ-grenoble-alpes.fr](http://www.univ-grenoble-alpes.fr). Les autres noms de domaine pour lesquels le certificat peut être utilisé figurent dans l’attribut Subject Alternative Name (SAN) : DNS:.univ-grenoble-alpes.fr, DNS:univ-grenoble-alpes.fr. La période de validité du certificat s’étend du 18 décembre 2024 à 00:00:00 GMT au 18 décembre 2025 à 23:59:59 GMT. Le lien vers le fichier .crl sert à vérifier si le certificat ou d’autres certificats émis par la même autorité ont été révoqués.

16.  Le certificat a été signé par GEANT Vereniging. La formule de calcul de la signature présente dans le certificat est $S=E(H(M))$.
17. Le sujet de ce certificat est GEANT Vereniging. La taille de la clé publique du certificat est de 4096 bits. Il a été signé par USERTrust RSA Certification Authority.
18. 
Université Grenoble Alpes\
    └──GEANT Vereniging\
        └── The USERTRUST Network\
            └──Comodo

Le certificat permettant de valider celui de "The USERTRUST Network" (n2) est le certificat de "Comodo" et se trove dans le système.

19. $Signature=Sign_{clé \space privé \space de \space l'émetteur}(HASH(TBSCertificate))$
TBSCertificate = “To Be Signed Certificate”, c’est la partie du certificat qui contient les infos : Subject, Public Key, Validity, Extensions…
Dans le cas d’un certificat racine auto-signé, l’émetteur et le sujet sont identiques, donc on signe avec sa propre clé privée.


CA RACINE: 192.168.170.178
