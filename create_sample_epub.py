#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a sample EPUB file for testing the epub2tex converter.
"""

from ebooklib import epub
import os

def create_sample_epub(output_path='sample.epub'):
    """Create a comprehensive sample EPUB file with various elements."""
    
    # Create book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('sample-epub-123')
    book.set_title('Guide Complet de Test EPUB')
    book.set_language('fr')
    book.add_author('Jean Dupont')
    book.add_metadata('DC', 'date', '2025')
    
    # Create chapters with various HTML elements
    
    # Chapter 1: Introduction with formatting
    c1 = epub.EpubHtml(
        title='Introduction',
        file_name='chap_01.xhtml',
        lang='fr'
    )
    c1.content = '''
    <html>
    <head><title>Introduction</title></head>
    <body>
        <h1>Introduction</h1>
        <p>Bienvenue dans ce <b>guide complet</b> de test pour le convertisseur EPUB vers LaTeX. 
        Ce document contient <em>divers éléments</em> pour tester la <u>robustesse</u> de la conversion.</p>
        
        <p>Le convertisseur doit être capable de gérer :</p>
        <ul>
            <li>Le formatage de texte (gras, italique, souligné)</li>
            <li>Les listes à puces et numérotées</li>
            <li>Les tableaux complexes</li>
            <li>Les liens et références</li>
        </ul>
        
        <h2>Objectifs du document</h2>
        <p>Ce document a pour but de démontrer la <strong>puissance</strong> et la 
        <em>robustesse</em> du convertisseur EPUB to LaTeX.</p>
    </body>
    </html>
    '''
    book.add_item(c1)
    
    # Chapter 2: Lists and formatting
    c2 = epub.EpubHtml(
        title='Listes et Formatage',
        file_name='chap_02.xhtml',
        lang='fr'
    )
    c2.content = '''
    <html>
    <head><title>Listes et Formatage</title></head>
    <body>
        <h1>Listes et Formatage Avancé</h1>
        
        <h2>Listes à puces</h2>
        <ul>
            <li>Premier élément en <b>gras</b></li>
            <li>Deuxième élément en <i>italique</i></li>
            <li>Troisième élément avec <code>code</code></li>
            <li>Quatrième élément normal</li>
        </ul>
        
        <h2>Listes numérotées</h2>
        <ol>
            <li>Première étape : <strong>Analyser</strong> le fichier EPUB</li>
            <li>Deuxième étape : <em>Extraire</em> le contenu</li>
            <li>Troisième étape : Convertir en LaTeX</li>
            <li>Quatrième étape : Générer le fichier final</li>
        </ol>
        
        <h2>Formatage de texte</h2>
        <p>Voici différents types de formatage :</p>
        <p><b>Texte en gras</b> et <strong>texte important</strong></p>
        <p><i>Texte en italique</i> et <em>texte emphase</em></p>
        <p><u>Texte souligné</u> pour l'attention</p>
        <p>Texte avec <sub>indice</sub> et <sup>exposant</sup></p>
        <p>Du <code>code inline</code> dans un paragraphe</p>
        
        <h2>Citations</h2>
        <blockquote>
        <p>« La simplicité est la sophistication suprême. »</p>
        <p>— Léonard de Vinci</p>
        </blockquote>
    </body>
    </html>
    '''
    book.add_item(c2)
    
    # Chapter 3: Tables
    c3 = epub.EpubHtml(
        title='Tableaux',
        file_name='chap_03.xhtml',
        lang='fr'
    )
    c3.content = '''
    <html>
    <head><title>Tableaux</title></head>
    <body>
        <h1>Tableaux et Données</h1>
        
        <h2>Tableau simple</h2>
        <table>
            <tr>
                <th>Nom</th>
                <th>Type</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>EPUB</td>
                <td>Format</td>
                <td>Format de livre électronique</td>
            </tr>
            <tr>
                <td>LaTeX</td>
                <td>Format</td>
                <td>Système de composition de documents</td>
            </tr>
            <tr>
                <td>Conversion</td>
                <td>Processus</td>
                <td>Transformation d'un format à l'autre</td>
            </tr>
        </table>
        
        <h2>Tableau de comparaison</h2>
        <table>
            <tr>
                <th>Caractéristique</th>
                <th>HTML</th>
                <th>LaTeX</th>
            </tr>
            <tr>
                <td>Formatage</td>
                <td>Balises</td>
                <td>Commandes</td>
            </tr>
            <tr>
                <td>Images</td>
                <td>&lt;img&gt;</td>
                <td>\\includegraphics</td>
            </tr>
            <tr>
                <td>Tableaux</td>
                <td>&lt;table&gt;</td>
                <td>tabular</td>
            </tr>
        </table>
    </body>
    </html>
    '''
    book.add_item(c3)
    
    # Chapter 4: Links and code
    c4 = epub.EpubHtml(
        title='Liens et Code',
        file_name='chap_04.xhtml',
        lang='fr'
    )
    c4.content = '''
    <html>
    <head><title>Liens et Code</title></head>
    <body>
        <h1>Liens Hypertexte et Blocs de Code</h1>
        
        <h2>Liens externes</h2>
        <p>Pour plus d'informations, consultez :</p>
        <ul>
            <li><a href="https://www.latex-project.org/">Le site officiel de LaTeX</a></li>
            <li><a href="https://www.python.org/">Le site de Python</a></li>
            <li><a href="https://github.com/">GitHub</a> pour le code source</li>
        </ul>
        
        <h2>Bloc de code</h2>
        <p>Exemple de code Python :</p>
        <pre>
def hello_world():
    """Fonction simple de démonstration."""
    print("Bonjour le monde !")
    return True

if __name__ == "__main__":
    hello_world()
        </pre>
        
        <h2>Ligne horizontale</h2>
        <p>Séparation visuelle :</p>
        <hr/>
        <p>Contenu après la ligne</p>
    </body>
    </html>
    '''
    book.add_item(c4)
    
    # Chapter 5: Special characters and conclusion
    c5 = epub.EpubHtml(
        title='Caractères Spéciaux',
        file_name='chap_05.xhtml',
        lang='fr'
    )
    c5.content = '''
    <html>
    <head><title>Caractères Spéciaux</title></head>
    <body>
        <h1>Caractères Spéciaux et Conclusion</h1>
        
        <h2>Caractères spéciaux LaTeX</h2>
        <p>Le convertisseur doit gérer correctement ces caractères :</p>
        <ul>
            <li>Esperluette : &amp;</li>
            <li>Pourcentage : %</li>
            <li>Dollar : $</li>
            <li>Dièse : #</li>
            <li>Underscore : _</li>
            <li>Accolades : { et }</li>
            <li>Tilde : ~</li>
            <li>Circonflexe : ^</li>
            <li>Backslash : \\</li>
        </ul>
        
        <h2>Accents français</h2>
        <p>Les accents doivent être préservés : é, è, ê, à, ù, ç, ï, ô</p>
        <p>Mots avec accents : <b>élégant</b>, <i>français</i>, <u>naïveté</u></p>
        
        <h2>Conclusion</h2>
        <p>Ce document de test démontre la capacité du convertisseur à gérer :</p>
        <ol>
            <li>La <strong>structure hiérarchique</strong> (chapitres, sections)</li>
            <li>Le <em>formatage de texte</em> complet</li>
            <li>Les <b>listes</b> numérotées et à puces</li>
            <li>Les <u>tableaux</u> avec en-têtes</li>
            <li>Les liens hypertexte externes</li>
            <li>Les blocs de code source</li>
            <li>Les caractères spéciaux et accents</li>
        </ol>
        
        <blockquote>
        <p>« Un bon convertisseur préserve non seulement le contenu, mais aussi l'intention 
        et l'esthétique du document original. »</p>
        </blockquote>
        
        <p>Merci d'avoir testé ce convertisseur EPUB vers LaTeX !</p>
    </body>
    </html>
    '''
    book.add_item(c5)
    
    # Define table of contents
    book.toc = (
        epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
        epub.Link('chap_02.xhtml', 'Listes et Formatage', 'lists'),
        epub.Link('chap_03.xhtml', 'Tableaux', 'tables'),
        epub.Link('chap_04.xhtml', 'Liens et Code', 'links'),
        epub.Link('chap_05.xhtml', 'Caractères Spéciaux', 'special'),
    )
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define spine
    book.spine = ['nav', c1, c2, c3, c4, c5]
    
    # Write EPUB file
    epub.write_epub(output_path, book)
    print(f"✓ Sample EPUB created: {output_path}")

if __name__ == '__main__':
    create_sample_epub()
