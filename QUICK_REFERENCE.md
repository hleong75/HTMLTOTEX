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
- **Chapitres** : `<h1>` → `\chapter{}` (avec `\clearpage`)
- **Sections** : `<h2>` → `\section{}` (avec `\newpage`)
- **Sous-sections** : `<h3>` → `\subsection{}`
- **Sous-sous-sections** : `<h4>` → `\subsubsection{}`
- **Paragraphes** : `<h5>` → `\paragraph{}`
- **Sous-paragraphes** : `<h6>` → `\subparagraph{}`
- **Paragraphes** : `<p>` → Paragraphes LaTeX
- **Conteneurs** : `<div>`, `<section>`, `<article>`, `<main>` → Préservés

### Formatage de Texte
- **Gras** : `<b>`, `<strong>` → `\textbf{}`
- **Italique** : `<i>`, `<em>` → `\textit{}`, `\emph{}`
- **Souligné** : `<u>`, `<ins>` → `\underline{}`
- **Surligné** : `<mark>` → `\hl{}` (jaune)
- **Barré** : `<s>`, `<del>`, `<strike>` → `\sout{}`
- **Code** : `<code>`, `<kbd>`, `<samp>`, `<tt>` → `\texttt{}`
- **Variable** : `<var>` → `\textit{}`
- **Abréviation** : `<abbr>` → `\textsc{}`
- **Citation** : `<cite>`, `<dfn>` → `\emph{}`
- **Citation courte** : `<q>` → Guillemets typographiques
- **Petit texte** : `<small>` → `{\small }`
- **Indice** : `<sub>` → Mode math `$_{}`
- **Exposant** : `<sup>` → Mode math `$^{}`

### Listes
- **À puces** : `<ul>` → `\begin{itemize}` (support imbrication)
- **Numérotées** : `<ol>` → `\begin{enumerate}` (support imbrication)
- **Définitions** : `<dl>`, `<dt>`, `<dd>` → `\begin{description}`

### Tableaux
- `<table>` → `\begin{tabular}` avec bordures
- `<caption>` → `\caption{}` pour les légendes

### Médias
- **Images** : `<img>` → `\includegraphics{}`
  - Extraction automatique dans `/images`
  - Support des légendes (attribut `alt`)
- **Figures** : `<figure>`, `<figcaption>` → `\begin{figure}` avec légende

### Liens
- **Externes** : `<a href="http...">` → `\href{}{}`
- **Internes** : Préservés comme texte

### Blocs de Contenu
- **Citations** : `<blockquote>` → `\begin{quote}`
- **Code source** : `<pre>` → `\begin{verbatim}`
- **Adresse** : `<address>` → `\begin{flushleft}` (italique)
- **Aparté** : `<aside>` → `\begin{quotation}`

### HTML5 Sémantique
- **En-tête/Pied** : `<header>`, `<footer>` → Avec espacement vertical
- **Navigation** : `<nav>` → Ignoré (non imprimé)

### Séparateurs
- **Ligne horizontale** : `<hr>` → `\rule{}` avec espacement
- **Saut de ligne** : `<br>` → `\\`
- **Césure** : `<wbr>` → `\-`

### Éléments Spéciaux
- **Temps/Données** : `<time>`, `<data>` → Texte extrait
- **Médias** : `<audio>`, `<video>`, `<canvas>` → Placeholder texte
- **Interactifs** : `<meter>`, `<progress>`, `<output>` → Texte extrait

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
# Créer un EPUB de test basique
python create_sample_epub.py

# Créer un EPUB de test complet avec tous les tags
python create_comprehensive_test_epub.py

# Tester le convertisseur (tests de base)
python test_converter.py

# Tester toutes les nouvelles fonctionnalités
python test_comprehensive.py

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
- `lmodern` : Polices modernes
- `babel` : Support français/anglais
- `graphicx`, `float` : Images
- `hyperref` : Liens hypertexte
- `xcolor` : Couleurs
- `soul` : Surlignage de texte
- `geometry` : Marges
- `booktabs`, `tabularx`, `longtable`, `array` : Tableaux
- `microtype` : Typographie améliorée
- `setspace` : Espacement
- `ulem` : Texte barré et souligné
- `enumitem` : Listes personnalisées
- `fancyvrb` : Code verbatim amélioré
- `titlesec` : Formatage des sections

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
5. Les médias audio/vidéo sont remplacés par du texte placeholder

## Gestion des Erreurs

Le convertisseur est robuste et affiche :
- ✓ Messages de succès pour les opérations réussies
- ⚠️ Avertissements pour les erreurs non-critiques (continue la conversion)
- ✗ Erreurs critiques qui arrêtent la conversion

Le convertisseur gère :
- Fichiers EPUB corrompus ou invalides
- Métadonnées manquantes
- Images manquantes
- Contenu HTML malformé
- Encodages variés

## Support et Contribution

- **Issues** : https://github.com/hleong75/HTMLTOTEX/issues
- **Pull Requests** : Bienvenues !
- **Documentation** : Voir README.md

## Licence

MIT License - Voir le fichier LICENSE pour plus de détails.
