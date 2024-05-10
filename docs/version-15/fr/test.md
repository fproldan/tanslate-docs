# Unité de traitement

Une unité de manutention est une abstraction permettant de suivre les quantités d'articles déplacés ou stockés ensemble. Il ne remplace pas les numéros de lot ou de série, la fabrication d'un article ou la fonctionnalité de l'offre groupée de produits, mais peut les compléter afin de saisir facilement des informations qui nécessiteraient autrement de nombreuses frappes au clavier.

En attribuant un identifiant unique à l'unité de manutention, il est possible de capturer via un scanner l'article, la quantité nette, l'unité de mesure et l'horodatage de la transaction précédente, puis d'agir sur ces informations dans leur contexte, conformément à la [matrice de décision]( ./matrix.md). Beam ajoute un nouveau doctype, Handling Unit, pour implémenter cette fonctionnalité dans ERPNext.

![Capture d'écran de la liste des types de documents de l'unité de manutention. La liste montre plusieurs nouvelles unités de manutention créées pour les articles reçus via un reçu d'achat.](./assets/handling_unit_list.png)

## Vues de liste
Généralement, l'analyse d'une unité de manutention dans une vue de liste filtrera pour afficher toutes les transactions du type de document avec l'unité de manutention appropriée.

## Reçu
Pour les reçus d'achat, les unités de manutention sont générées et ne peuvent pas être fournies par l'utilisateur.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | 40 pièces |


## Facture d'achat
Pour les factures d'achat avec la case "Mettre à jour le stock" cochée, les unités de manutention sont générées et ne peuvent pas être fournies par l'utilisateur.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | 40 pièces |

Lorsque « Mettre à jour le stock » n'est _pas_ coché, ils peuvent être numérisés pour faciliter la saisie des données mais il n'y a aucun effet dans le grand livre des stocks.

## Bon de livraison
Pour le bon de livraison, les unités de manutention sont consommées. Dans le cas où une quantité inférieure à la quantité totale associée à l'unité de manutention est livrée, l'unité de manutention existante fera référence à la quantité (nette) restante.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | 20 pièces |

Grand livre des stocks ou transaction ultérieure
| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | 20 pièces |


## Facture de vente
Pour une Facture de vente où « Mettre à jour le stock » est coché, les Unités de manutention sont consommées. Dans le cas où une quantité inférieure à la quantité totale associée à l'unité de manutention est livrée, l'unité de manutention existante fera référence à la quantité (nette) restante.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | 15 ch |

Grand livre des stocks ou transaction ultérieure
| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | 5 pièces |

Lorsque "Mettre à jour le stock" n'est _pas_ coché, ils peuvent être numérisés pour faciliter la saisie des données mais il n'y a aucun effet dans le grand livre des stocks.

La capture d'écran suivante montre le grand livre des stocks pour l'article Cloudberry. La première ligne montre la réception de 60 livres de fruits via un reçu d'achat, et la deuxième ligne est après la vente de 25 livres via une facture de vente comportant une « mise à jour du stock ». Notez que les deux transactions font référence à la même unité de manutention.

![Capture d'écran du grand livre des stocks retraçant la réception et les ventes de l'article Cloudberry.](./assets/stock_ledger_after_sale.png)

## Entrée de stock

### Envoi à l'entrepreneur, transfert de matériel pour la fabrication et transfert de matériel
Lorsque l'article est transféré d'un entrepôt à un autre, une nouvelle unité de manutention est générée, même si l'intégralité de l'unité de manutention est transférée. Dans le cas où une quantité inférieure à la quantité totale associée à une unité de manutention est déplacée d'un entrepôt à un autre, une nouvelle unité de manutention est générée pour les nouvelles unités. Des analyses ou recherches ultérieures de l'unité de manutention originale (123) renverront le reste ou la quantité nette.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ----------------------- | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | -40 pièce |
| Cocoprune | Entrepôt sous-traitant | 456 | 40 pièces |

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | -20 pièce |
| Cocoprune | Travaux en cours | 456 | 20 pièces |


Lors de l'annulation d'une entrée de stock, l'utilisateur aura la possibilité de recombiner ou de laisser les unités de manutention rester suivies séparément.

![Capture d'écran de la boîte de dialogue de recombinaison](./assets/recombine.png)

### Reconditionnement et fabrication

Dans le cas d'un reconditionnement, d'une sortie de matière ou d'une consommation de matières pour fabrication, une nouvelle unité de manutention est générée pour les nouvelles quantités.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | -40 pièce |
| Cocoprune | Débarras | 789 | 1 boîte de 40 |


Dans le cas où une quantité inférieure à la quantité totale associée à une unité de manutention est consommée, des analyses ou recherches ultérieures de l'unité de manutention d'origine (123) renverront le reste ou la quantité nette.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | -20 pièce |
| Purée de Cocoprune | Travaux en cours | 012 | 1 litre |
| Cocoprune | Ferraille | | 1 pièce |

#### Article mis au rebut de la nomenclature
Dans une entrée de stock de fabrication ou de réemballage, les articles rebutés peuvent être activés pour créer une unité de manutention correspondant à leur quantité de rebut. Cela peut être modifié après la soumission d'une nomenclature.

![Capture d'écran des éléments de rebut de la nomenclature montrant la configuration](./assets/bom_scrap_item.png)

### Problème de matériaux, consommation de matériaux pour la fabrication

Dans ces deux cas, il n’y a pas de mouvement compensatoire ni de création d’articles.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | -20 pièce |


| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Travaux en cours | 123 | -20 pièce |

### Réception du matériel
Dans le cas d'une entrée de matériel, une nouvelle unité de manutention est générée pour chaque article.

| Article | Entrepôt | Unité de manutention | Quantité |
| ---------------- | ------------------ | ---------- | ---------- :|
| Cocoprune | Débarras | 123 | 20 pièces |