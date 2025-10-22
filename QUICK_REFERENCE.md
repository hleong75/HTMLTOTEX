# Guide de Référence Rapide - EPUB to LaTeX

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation de Base

```bash
# Conversion simple
python epub2tex.py livre.epub

# Avec fichier de sortie personnalisé
python epub2tex.py livre.epub mon_livre.tex
```

## Éléments Supportés

### Structure du Document
- **Chapitres** : `<h1>` → `\chapter{}`
- **Sections** : `<h2>` → `\section{}`
- **Sous-sections** : `<h3>` → `\subsection{}`
- **Paragraphes** : `<p>` → Paragraphes LaTeX

### Formatage de Texte
- **Gras** : `<b>`, `<strong>` → `\textbf{}`
- **Italique** : `<i>`, `<em>` → `\textit{}`, `\emph{}`
- **Souligné** : `<u>` → `\underline{}`
- **Code** : `<code>` → `\texttt{}`
- **Indice** : `<sub>` → Mode math `$_{}`
- **Exposant** : `<sup>` → Mode math `$^{}`

### Listes
- **À puces** : `<ul>` → `\begin{itemize}`
- **Numérotées** : `<ol>` → `\begin{enumerate}`

### Tableaux
- `<table>` → `\begin{tabular}` avec bordures

### Médias
- **Images** : `<img>` → `\includegraphics{}`
  - Extraction automatique dans `/images`
  - Support des légendes (attribut `alt`)

### Liens
- **Externes** : `<a href="http...">` → `\href{}{}`
- **Internes** : Préservés comme texte

### Autres
- **Citations** : `<blockquote>` → `\begin{quote}`
- **Code source** : `<pre>` → `\begin{verbatim}`
- **Ligne horizontale** : `<hr>` → `\rule{}`
- **Saut de ligne** : `<br>` → `\\`

## Caractères Spéciaux

Le convertisseur échappe automatiquement :
- `&` → `\&`
- `%` → `\%`
- `$` → `\$`
- `#` → `\#`
- `_` → `\_`
- `{` et `}` → `\{` et `\}`
- `~` → `\textasciitilde{}`
- `^` → `\textasciicircum{}`
- `\` → `\textbackslash{}`

## Compilation LaTeX

```bash
# Avec pdfLaTeX
pdflatex livre.tex
pdflatex livre.tex  # Deuxième passe pour TOC

# Avec XeLaTeX (recommandé pour UTF-8)
xelatex livre.tex
xelatex livre.tex

# Avec LuaLaTeX
lualatex livre.tex
lualatex livre.tex
```

## Tests

```bash
# Créer un EPUB de test
python create_sample_epub.py

# Tester le convertisseur
python test_converter.py

# Voir les exemples d'utilisation
python example_usage.py
```

## Structure des Fichiers de Sortie

```
votre_dossier/
├── livre.tex              # Document LaTeX principal
└── images/                # Images extraites (si présentes)
    ├── image_0_cover.jpg
    └── ...
```

## Packages LaTeX Inclus

Le document généré inclut :
- `inputenc`, `fontenc` : Encodage UTF-8
- `babel` : Support français/anglais
- `graphicx` : Images
- `hyperref` : Liens hypertexte
- `geometry` : Marges
- `booktabs`, `tabularx` : Tableaux
- `microtype` : Typographie
- `setspace` : Espacement
- `ulem` : Texte barré
- `enumitem` : Listes personnalisées

## Métadonnées

Extraction automatique depuis l'EPUB :
- **Titre** → `\title{}`
- **Auteur(s)** → `\author{}`
- **Date** → `\date{}`

## Options Avancées

### Aide
```bash
python epub2tex.py --help
```

### Version
```bash
python epub2tex.py --version
```

## Dépannage

### Problème : "Required libraries not installed"
**Solution** : `pip install -r requirements.txt`

### Problème : LaTeX ne compile pas
**Solution** : Vérifiez que tous les packages LaTeX requis sont installés

### Problème : Images manquantes
**Solution** : Assurez-vous que le dossier `images/` est au même niveau que le fichier `.tex`

### Problème : Caractères accentués mal affichés
**Solution** : Utilisez `xelatex` au lieu de `pdflatex`

## Limitations Connues

1. Les formules mathématiques MathML ne sont pas encore supportées
2. Les notes de bas de page ne sont pas converties
3. Les contenus EPUB3 interactifs sont ignorés
4. Les CSS personnalisées ne sont pas appliquées

## Support et Contribution

- **Issues** : https://github.com/hleong75/HTMLTOTEX/issues
- **Pull Requests** : Bienvenues !
- **Documentation** : Voir README.md

## Licence

MIT License - Voir le fichier LICENSE pour plus de détails.
