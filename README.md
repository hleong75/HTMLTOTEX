# EPUB to LaTeX Converter

Un convertisseur **ultra-puissant et robuste** pour transformer vos fichiers EPUB en documents LaTeX de haute qualité, avec préservation complète du style et une mise en page agréable à lire.

## ✨ Caractéristiques

- **Conversion complète** : Transforme tous les éléments EPUB (chapitres, sections, paragraphes)
- **Support étendu des balises HTML** : Plus de 40 balises HTML différentes supportées
- **Préservation du style** : Maintient le formatage (gras, italique, souligné, surligné, etc.)
- **Support des médias** : Gère les images, tableaux, listes, liens
- **Listes imbriquées** : Support complet des listes à plusieurs niveaux
- **Listes de définitions** : Conversion des listes de définitions HTML
- **HTML5 sémantique** : Support des balises sémantiques modernes (header, footer, aside, etc.)
- **Tableaux avec légendes** : Support des légendes de tableaux
- **Mise en page professionnelle** : Utilisation automatique de `\newpage`, `\clearpage` pour une pagination optimale
- **Structure intelligente** : Génère automatiquement table des matières et métadonnées
- **LaTeX optimisé** : Produit un code LaTeX propre et lisible
- **Robuste** : Gestion d'erreurs complète et traitement des cas limites
- **Compatibilité EPUB** : Supporte tous les formats EPUB valides

## 📋 Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/hleong75/HTMLTOTEX.git
cd HTMLTOTEX
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Utilisation basique

```bash
python epub2tex.py livre.epub
```

Cela créera un fichier `livre.tex` dans le même répertoire.

### Spécifier un fichier de sortie

```bash
python epub2tex.py livre.epub mon_document.tex
```

### Exemples

```bash
# Convertir un roman
python epub2tex.py roman.epub

# Convertir avec sortie personnalisée
python epub2tex.py manuel.epub output/manuel_converti.tex

# Afficher l'aide
python epub2tex.py --help
```

## 📖 Fonctionnalités détaillées

### Éléments supportés

| Élément HTML | Conversion LaTeX | Description |
|--------------|------------------|-------------|
| **Structure de document** |||
| `<h1>` - `<h6>` | `\chapter`, `\section`, etc. | Titres hiérarchiques avec sauts de page |
| `<p>` | Paragraphes | Paragraphes avec espacement |
| `<div>`, `<section>`, `<article>` | Conteneurs | Éléments de structure |
| `<header>`, `<footer>` | Espacement vertical | En-têtes et pieds de page |
| `<main>` | Contenu principal | Corps du document |
| `<aside>` | `quotation` | Contenu complémentaire |
| `<nav>` | Ignoré | Navigation (non imprimable) |
| **Formatage de texte** |||
| `<b>`, `<strong>` | `\textbf{}` | Texte en gras |
| `<i>`, `<em>` | `\textit{}`, `\emph{}` | Texte en italique |
| `<u>` | `\underline{}` | Texte souligné |
| `<mark>` | `\hl{}` | Texte surligné en jaune |
| `<s>`, `<del>`, `<strike>` | `\sout{}` | Texte barré |
| `<ins>` | `\underline{}` | Texte inséré |
| `<small>` | `{\small }` | Texte en petite taille |
| `<code>`, `<tt>`, `<kbd>`, `<samp>` | `\texttt{}` | Police monospace |
| `<var>` | `\textit{}` | Variables |
| `<abbr>` | `\textsc{}` | Abréviations en petites capitales |
| `<cite>` | `\textit{}` | Citations |
| `<q>` | Guillemets typographiques | Citations courtes |
| `<dfn>` | `\emph{}` | Définitions |
| **Indices et exposants** |||
| `<sub>` | Mode mathématique | Indices |
| `<sup>` | Mode mathématique | Exposants |
| **Listes** |||
| `<ul>` | `itemize` | Listes à puces (avec support des listes imbriquées) |
| `<ol>` | `enumerate` | Listes numérotées (avec support des listes imbriquées) |
| `<dl>`, `<dt>`, `<dd>` | `description` | Listes de définitions |
| **Tableaux** |||
| `<table>` | `tabular` | Tableaux avec support des légendes |
| `<caption>` | `\caption{}` | Légendes de tableaux |
| **Images et figures** |||
| `<img>` | `\includegraphics` | Images avec légendes |
| `<figure>`, `<figcaption>` | `figure` | Figures avec légendes |
| **Liens et références** |||
| `<a>` | `\href{}` | Liens hypertexte |
| **Citations et blocs** |||
| `<blockquote>` | `quote` | Citations longues |
| `<pre>`, `<code>` | `verbatim` | Blocs de code source |
| `<address>` | `flushleft` (italique) | Adresses |
| **Séparateurs** |||
| `<br>` | `\\` or espace | Saut de ligne (devient espace dans les titres) |
| `<hr>` | `\rule{}` | Ligne horizontale avec espacement |
| `<wbr>` | `\-` | Césure suggérée |
| **Éléments spéciaux** |||
| `<time>`, `<data>` | Texte extrait | Données temporelles |
| `<audio>`, `<video>`, `<canvas>` | Texte placeholder | Médias non-textuels |
| `<meter>`, `<progress>`, `<output>` | Texte extrait | Éléments interactifs |

**Note importante :** Les balises `<br>` dans les titres (`<h1>` à `<h6>`) sont automatiquement converties en espaces au lieu de sauts de ligne pour éviter les erreurs de compilation LaTeX avec le package `titlesec`.

### Structure du document LaTeX généré

Le fichier LaTeX généré inclut :

- **Préambule complet** avec packages nécessaires
- **Métadonnées** (titre, auteur, date) extraites de l'EPUB
- **Table des matières** automatique
- **Support multilingue** (français et anglais)
- **Hyperliens** cliquables et colorés
- **Images** extraites dans un sous-dossier `images/`
- **Mise en page professionnelle** avec marges et espacement optimaux

### Packages LaTeX inclus

Le convertisseur génère un document LaTeX avec les packages suivants :

**Encodage et polices :**
- `inputenc`, `fontenc` : Support UTF-8 et encodage
- `lmodern` : Polices modernes

**Support linguistique :**
- `babel` : Support multilingue (français et anglais)

**Graphiques et images :**
- `graphicx` : Inclusion d'images
- `float` : Positionnement flottant

**Mise en page :**
- `geometry` : Configuration des marges
- `setspace` : Espacement des lignes
- `titlesec` : Formatage des sections

**Couleurs et mise en forme :**
- `xcolor` : Support des couleurs
- `soul` : Surlignage de texte
- `ulem` : Texte barré et souligné

**Tableaux :**
- `booktabs` : Tableaux professionnels
- `tabularx` : Tableaux adaptatifs
- `longtable` : Tableaux multi-pages
- `array` : Amélioration des tableaux

**Listes :**
- `enumitem` : Personnalisation des listes

**Hyperliens :**
- `hyperref` : Liens hypertexte et métadonnées PDF

**Typographie :**
- `microtype` : Typographie améliorée

**Code :**
- `fancyvrb` : Environnements verbatim améliorés

Et plus encore...

## 📂 Structure des fichiers de sortie

Après conversion, vous obtiendrez :

```
votre_repertoire/
├── livre.tex          # Document LaTeX principal
└── images/            # Dossier contenant les images extraites
    ├── image_0_cover.jpg
    ├── image_1_diagram.png
    └── ...
```

## 🔧 Compilation du LaTeX

Une fois la conversion terminée, compilez le document LaTeX :

```bash
# Avec pdflatex
pdflatex livre.tex
pdflatex livre.tex  # Deuxième passe pour la table des matières

# Ou avec XeLaTeX (recommandé pour l'UTF-8)
xelatex livre.tex
xelatex livre.tex

# Ou avec LuaLaTeX
lualatex livre.tex
lualatex livre.tex
```

## 🎯 Cas d'usage

- **Publications académiques** : Convertir des livres électroniques en thèses ou articles
- **Documentation technique** : Transformer des manuels EPUB en PDF professionnels
- **Édition** : Préparer des manuscrits pour l'impression
- **Archives** : Convertir des bibliothèques numériques en format LaTeX éditable

## 🛠️ Développement

### Structure du code

- `epub2tex.py` : Script principal du convertisseur
- `EPUBToLaTeXConverter` : Classe principale gérant la conversion
- Méthodes de conversion spécialisées pour chaque type d'élément HTML
- Gestion robuste des caractères spéciaux LaTeX

### Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Forker le projet
2. Créer une branche pour votre fonctionnalité
3. Committer vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est distribué sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🐛 Signaler un bug

Si vous rencontrez un problème, veuillez ouvrir une issue sur GitHub avec :
- Le fichier EPUB problématique (si possible)
- Le message d'erreur complet
- Votre version de Python et des dépendances

### Problèmes connus et résolus

**✓ Résolu :** Erreur "Paragraph ended before \ttl@straight@i was complete"
- **Symptôme v2.2 :** Erreur de compilation LaTeX lors de l'utilisation de `<h5>` et `<h6>` dans les EPUBs
- **Cause v2.2 :** Les commandes `\paragraph` et `\subparagraph` nécessitent un formatage spécial (pas de ligne vide après)
- **Solution v2.2 :** Les commandes `\paragraph` et `\subparagraph` sont maintenant générées avec un retour à la ligne simple
- **Version v2.2 :** Corrigé dans la version 2.2

- **Symptôme v2.1 :** Erreur de compilation LaTeX lors de la présence de balises `<br>` dans les titres
- **Cause v2.1 :** Les commandes de section LaTeX ne peuvent pas contenir de sauts de ligne (`\\`)
- **Solution v2.1 :** Les balises `<br>` dans les titres sont maintenant converties en espaces
- **Version v2.1 :** Corrigé dans la version 2.1

## 💡 Améliorations futures

- Support des notes de bas de page
- Conversion des formules mathématiques MathML
- Options de personnalisation du style LaTeX
- Support des EPUB3 avec contenus interactifs avancés
- Interface graphique (GUI)
- Support des index et glossaires
- Conversion des SVG en TikZ

## 🙏 Remerciements

Développé avec ❤️ pour la communauté LaTeX et EPUB.

Bibliothèques utilisées :
- [ebooklib](https://github.com/aerkalov/ebooklib) : Manipulation des fichiers EPUB
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) : Parsing HTML
- [lxml](https://lxml.de/) : Traitement XML performant

---

**Note** : Ce convertisseur est conçu pour produire des documents LaTeX de haute qualité. Pour de meilleurs résultats, nous recommandons de réviser et d'ajuster manuellement le fichier LaTeX généré selon vos besoins spécifiques.