
## Importer le fichier  #1.txt et le stocker dans une variable en gérant l'encodage utf-8
var = open("#1.txt", "r", encoding="utf-8")
## Afficher le contenu de var
print(var.read())