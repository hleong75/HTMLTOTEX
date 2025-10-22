# EPUB to LaTeX Converter

Un convertisseur **ultra-puissant et robuste** pour transformer vos fichiers EPUB en documents LaTeX de haute qualité, avec préservation complète du style et une mise en page agréable à lire.

## ✨ Caractéristiques

- **Conversion complète** : Transforme tous les éléments EPUB (chapitres, sections, paragraphes)
- **Préservation du style** : Maintient le formatage (gras, italique, souligné, etc.)
- **Support des médias** : Gère les images, tableaux, listes, liens
- **Structure intelligente** : Génère automatiquement table des matières et métadonnées
- **LaTeX optimisé** : Produit un code LaTeX propre et lisible
- **Robuste** : Gestion d'erreurs complète et traitement des cas limites

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
| `<h1>` - `<h6>` | `\chapter`, `\section`, etc. | Titres hiérarchiques |
| `<p>` | Paragraphes | Paragraphes avec espacement |
| `<b>`, `<strong>` | `\textbf{}` | Texte en gras |
| `<i>`, `<em>` | `\textit{}`, `\emph{}` | Texte en italique |
| `<u>` | `\underline{}` | Texte souligné |
| `<ul>`, `<ol>` | `itemize`, `enumerate` | Listes à puces/numérotées |
| `<table>` | `tabular` | Tableaux |
| `<img>` | `\includegraphics` | Images avec légendes |
| `<a>` | `\href{}` | Liens hypertexte |
| `<blockquote>` | `quote` | Citations |
| `<pre>`, `<code>` | `verbatim` | Code source |
| `<sub>`, `<sup>` | Mode mathématique | Indices et exposants |

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

- `inputenc`, `fontenc` : Support UTF-8 et encodage
- `babel` : Support multilingue
- `graphicx` : Inclusion d'images
- `hyperref` : Liens hypertexte et métadonnées PDF
- `geometry` : Configuration des marges
- `booktabs` : Tableaux professionnels
- `microtype` : Typographie améliorée
- `ulem` : Texte barré
- Et plus encore...

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

## 💡 Améliorations futures

- Support des notes de bas de page
- Conversion des formules mathématiques MathML
- Options de personnalisation du style LaTeX
- Support des EPUB3 avec contenus interactifs
- Interface graphique (GUI)

## 🙏 Remerciements

Développé avec ❤️ pour la communauté LaTeX et EPUB.

Bibliothèques utilisées :
- [ebooklib](https://github.com/aerkalov/ebooklib) : Manipulation des fichiers EPUB
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) : Parsing HTML
- [lxml](https://lxml.de/) : Traitement XML performant

---

**Note** : Ce convertisseur est conçu pour produire des documents LaTeX de haute qualité. Pour de meilleurs résultats, nous recommandons de réviser et d'ajuster manuellement le fichier LaTeX généré selon vos besoins spécifiques.