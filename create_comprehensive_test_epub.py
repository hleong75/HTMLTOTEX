#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a comprehensive test EPUB file with all supported HTML tags.
"""

from ebooklib import epub
import os

def create_comprehensive_test_epub(output_path='comprehensive_test.epub'):
    """Create a comprehensive EPUB file with all supported HTML elements."""
    
    # Create book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('comprehensive-test-epub-456')
    book.set_title('Test Complet de Tous les Tags HTML')
    book.set_language('fr')
    book.add_author('Test Auteur')
    book.add_metadata('DC', 'date', '2025')
    
    # Chapter 1: New text formatting tags
    c1 = epub.EpubHtml(
        title='Formatage Avancé',
        file_name='chap_01.xhtml',
        lang='fr'
    )
    c1.content = '''
    <html>
    <head><title>Formatage Avancé</title></head>
    <body>
        <h1>Test des Nouveaux Tags de Formatage</h1>
        
        <h2>Tags de texte</h2>
        <p>Texte avec <mark>surbrillance</mark> en jaune.</p>
        <p>Texte <s>barré avec s</s> et <del>barré avec del</del>.</p>
        <p>Texte <ins>inséré</ins> souligné.</p>
        <p>Raccourci clavier : <kbd>Ctrl+C</kbd> pour copier.</p>
        <p>Exemple de sortie : <samp>Hello, World!</samp></p>
        <p>Variable mathématique : <var>x</var> = 5</p>
        <p>Abréviation : <abbr title="HyperText Markup Language">HTML</abbr></p>
        <p>Citation courte : <q>La vie est belle</q></p>
        <p>Définition : <dfn>EPUB</dfn> est un format de livre électronique.</p>
        <p>Horodatage : <time datetime="2025-01-15">15 janvier 2025</time></p>
        
        <h2>Ligne de séparation</h2>
        <p>Contenu avant la ligne</p>
        <hr/>
        <p>Contenu après la ligne</p>
    </body>
    </html>
    '''
    book.add_item(c1)
    
    # Chapter 2: Lists with nesting
    c2 = epub.EpubHtml(
        title='Listes Complexes',
        file_name='chap_02.xhtml',
        lang='fr'
    )
    c2.content = '''
    <html>
    <head><title>Listes Complexes</title></head>
    <body>
        <h1>Listes Imbriquées et Définitions</h1>
        
        <h2>Listes imbriquées</h2>
        <ul>
            <li>Premier niveau - élément 1
                <ul>
                    <li>Deuxième niveau - sous-élément 1</li>
                    <li>Deuxième niveau - sous-élément 2
                        <ul>
                            <li>Troisième niveau</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li>Premier niveau - élément 2</li>
        </ul>
        
        <h2>Liste de définitions</h2>
        <dl>
            <dt>HTML</dt>
            <dd>HyperText Markup Language - langage de balisage pour le web</dd>
            
            <dt>CSS</dt>
            <dd>Cascading Style Sheets - feuilles de style en cascade</dd>
            
            <dt>LaTeX</dt>
            <dd>Système de composition de documents de haute qualité</dd>
            
            <dt>EPUB</dt>
            <dd>Electronic Publication - format de livre électronique</dd>
        </dl>
    </body>
    </html>
    '''
    book.add_item(c2)
    
    # Chapter 3: Semantic HTML5
    c3 = epub.EpubHtml(
        title='HTML5 Sémantique',
        file_name='chap_03.xhtml',
        lang='fr'
    )
    c3.content = '''
    <html>
    <head><title>HTML5 Sémantique</title></head>
    <body>
        <h1>Tags Sémantiques HTML5</h1>
        
        <header>
            <h2>En-tête du Document</h2>
            <p>Ceci est un en-tête sémantique avec <strong>header</strong>.</p>
        </header>
        
        <main>
            <article>
                <h2>Article Principal</h2>
                <p>Ceci est le contenu principal dans une balise <code>article</code>.</p>
                
                <section>
                    <h3>Section dans l'article</h3>
                    <p>Une section avec du contenu structuré.</p>
                </section>
            </article>
            
            <aside>
                <h3>Information Complémentaire</h3>
                <p>Ceci est une note latérale avec <code>aside</code>.</p>
                <p>Elle contient des informations complémentaires.</p>
            </aside>
        </main>
        
        <footer>
            <p>Pied de page du document avec <strong>footer</strong>.</p>
            <address>
                Contact : test@example.com<br/>
                123 Rue de Test, Paris
            </address>
        </footer>
        
        <nav>
            <p>Cette navigation sera ignorée dans le PDF final.</p>
            <ul>
                <li><a href="#home">Accueil</a></li>
                <li><a href="#about">À propos</a></li>
            </ul>
        </nav>
    </body>
    </html>
    '''
    book.add_item(c3)
    
    # Chapter 4: Tables with captions
    c4 = epub.EpubHtml(
        title='Tableaux Avancés',
        file_name='chap_04.xhtml',
        lang='fr'
    )
    c4.content = '''
    <html>
    <head><title>Tableaux Avancés</title></head>
    <body>
        <h1>Tableaux avec Légendes</h1>
        
        <h2>Tableau avec caption</h2>
        <table>
            <caption>Liste des langages de programmation populaires</caption>
            <tr>
                <th>Langage</th>
                <th>Paradigme</th>
                <th>Année</th>
            </tr>
            <tr>
                <td>Python</td>
                <td>Multi-paradigme</td>
                <td>1991</td>
            </tr>
            <tr>
                <td>JavaScript</td>
                <td>Multi-paradigme</td>
                <td>1995</td>
            </tr>
            <tr>
                <td>Java</td>
                <td>Orienté objet</td>
                <td>1995</td>
            </tr>
        </table>
        
        <h2>Tableau de données</h2>
        <table>
            <caption>Comparaison des formats de documents</caption>
            <tr>
                <th>Format</th>
                <th>Extension</th>
                <th>Type</th>
            </tr>
            <tr>
                <td>PDF</td>
                <td>.pdf</td>
                <td>Portable</td>
            </tr>
            <tr>
                <td>EPUB</td>
                <td>.epub</td>
                <td>Reflowable</td>
            </tr>
            <tr>
                <td>LaTeX</td>
                <td>.tex</td>
                <td>Source</td>
            </tr>
        </table>
    </body>
    </html>
    '''
    book.add_item(c4)
    
    # Chapter 5: Figures
    c5 = epub.EpubHtml(
        title='Figures et Citations',
        file_name='chap_05.xhtml',
        lang='fr'
    )
    c5.content = '''
    <html>
    <head><title>Figures et Citations</title></head>
    <body>
        <h1>Figures et Blocs de Citations</h1>
        
        <h2>Citations étendues</h2>
        <blockquote>
            <p>« Le génie, c'est 1% d'inspiration et 99% de transpiration. »</p>
            <p>— Thomas Edison</p>
        </blockquote>
        
        <blockquote>
            <p>« Il n'y a que deux choses infinies : l'univers et la bêtise humaine,
            et encore pour l'univers, je n'en suis pas sûr. »</p>
            <p>— Albert Einstein</p>
        </blockquote>
        
        <h2>Code multi-lignes</h2>
        <pre>
# Exemple de fonction Python
def fibonacci(n):
    """Calcule la suite de Fibonacci."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
        </pre>
        
        <h2>Caractères spéciaux LaTeX</h2>
        <p>Test des caractères qui doivent être échappés :</p>
        <ul>
            <li>Pourcentage 100%</li>
            <li>Dollar $50</li>
            <li>Underscore file_name</li>
            <li>Esperluette : Tom &amp; Jerry</li>
            <li>Dièse #hashtag</li>
            <li>Accolades { et }</li>
            <li>Tilde ~</li>
            <li>Circonflexe ^</li>
        </ul>
    </body>
    </html>
    '''
    book.add_item(c5)
    
    # Chapter 6: Mixed content
    c6 = epub.EpubHtml(
        title='Contenu Mixte',
        file_name='chap_06.xhtml',
        lang='fr'
    )
    c6.content = '''
    <html>
    <head><title>Contenu Mixte</title></head>
    <body>
        <h1>Contenu Mixte et Complexe</h1>
        
        <h2>Combinaisons de formatage</h2>
        <p>Texte avec <b>gras et <i>gras italique</i></b> imbriqués.</p>
        <p>Texte avec <u>souligné et <code>code souligné</code></u>.</p>
        <p>Formule : E = mc<sup>2</sup> et H<sub>2</sub>O</p>
        
        <h2>Liste ordonnée complexe</h2>
        <ol>
            <li>Étape 1 : <strong>Préparation</strong>
                <ul>
                    <li>Collecter les données</li>
                    <li>Nettoyer les données</li>
                </ul>
            </li>
            <li>Étape 2 : <em>Analyse</em>
                <ul>
                    <li>Exploration statistique</li>
                    <li>Visualisation</li>
                </ul>
            </li>
            <li>Étape 3 : <u>Résultats</u>
                <ul>
                    <li>Interprétation</li>
                    <li>Conclusions</li>
                </ul>
            </li>
        </ol>
        
        <h2>Liens et références</h2>
        <p>Pour plus d'informations :</p>
        <ul>
            <li>Site officiel : <a href="https://www.latex-project.org/">LaTeX Project</a></li>
            <li>Documentation : <a href="https://www.overleaf.com/learn">Overleaf Learn</a></li>
            <li>Communauté : <a href="https://tex.stackexchange.com/">TeX StackExchange</a></li>
        </ul>
        
        <h2>Paragraphes avec breaks</h2>
        <p>Première ligne<br/>
        Deuxième ligne après un break<br/>
        Troisième ligne</p>
        
        <hr/>
        
        <h2>Conclusion</h2>
        <p>Ce document teste <mark>tous les tags HTML</mark> supportés par le convertisseur.
        Il garantit que le <abbr>TEX</abbr> généré est <strong>sans erreur</strong> et avec
        un <em>style impeccable</em>.</p>
    </body>
    </html>
    '''
    book.add_item(c6)
    
    # Define table of contents
    book.toc = (
        epub.Link('chap_01.xhtml', 'Formatage Avancé', 'fmt'),
        epub.Link('chap_02.xhtml', 'Listes Complexes', 'lists'),
        epub.Link('chap_03.xhtml', 'HTML5 Sémantique', 'html5'),
        epub.Link('chap_04.xhtml', 'Tableaux Avancés', 'tables'),
        epub.Link('chap_05.xhtml', 'Figures et Citations', 'figures'),
        epub.Link('chap_06.xhtml', 'Contenu Mixte', 'mixed'),
    )
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define spine
    book.spine = ['nav', c1, c2, c3, c4, c5, c6]
    
    # Write EPUB file
    epub.write_epub(output_path, book)
    print(f"✓ Comprehensive test EPUB created: {output_path}")

if __name__ == '__main__':
    create_comprehensive_test_epub()
