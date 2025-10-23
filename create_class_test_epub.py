#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a test EPUB file with class attributes for testing class-aware conversion.
"""

from ebooklib import epub
import os

def create_class_test_epub(output_path='class_test.epub'):
    """Create an EPUB file with various class attributes."""
    
    # Create book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('class-test-epub-001')
    book.set_title('Test de Classes CSS')
    book.set_language('fr')
    book.add_author('Test Author')
    book.add_metadata('DC', 'date', '2025')
    
    # Create chapter with class attributes
    c1 = epub.EpubHtml(
        title='Test Classes',
        file_name='chap_01.xhtml',
        lang='fr'
    )
    c1.content = '''
    <html>
    <head><title>Test Classes</title></head>
    <body>
        <h1>Test des Attributs de Classe</h1>
        
        <p class="important">Ce paragraphe a la classe "important" et devrait être mis en évidence.</p>
        
        <p class="note">Ce paragraphe a la classe "note" pour indiquer une remarque.</p>
        
        <p class="warning">Ce paragraphe a la classe "warning" pour un avertissement.</p>
        
        <p>Paragraphe normal sans classe.</p>
        
        <div class="highlight">
            <p>Contenu dans une div avec la classe "highlight".</p>
            <p>Plusieurs paragraphes peuvent être inclus.</p>
        </div>
        
        <h2 class="special-heading">Titre avec Classe Spéciale</h2>
        <p>Texte après le titre avec classe.</p>
        
        <blockquote class="epigraph">
            <p>« Une citation avec la classe "epigraph". »</p>
        </blockquote>
        
        <ul class="checklist">
            <li class="done">Élément terminé</li>
            <li class="pending">Élément en cours</li>
            <li class="todo">Élément à faire</li>
        </ul>
        
        <table class="data-table">
            <caption>Tableau avec classe "data-table"</caption>
            <tr>
                <th>Colonne 1</th>
                <th>Colonne 2</th>
            </tr>
            <tr class="highlight-row">
                <td>Ligne en surbrillance</td>
                <td>Données</td>
            </tr>
            <tr>
                <td>Ligne normale</td>
                <td>Données</td>
            </tr>
        </table>
        
        <p>Test de <span class="code-inline">code avec classe</span> dans le texte.</p>
        
        <p class="author-note">Note de l'auteur avec formatage spécial.</p>
        
        <div class="box info">
            <h3>Information</h3>
            <p>Contenu dans une boîte d'information avec classe "box info".</p>
        </div>
    </body>
    </html>
    '''
    book.add_item(c1)
    
    # Define table of contents
    book.toc = (
        epub.Link('chap_01.xhtml', 'Test Classes', 'test'),
    )
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define spine
    book.spine = ['nav', c1]
    
    # Write EPUB file
    epub.write_epub(output_path, book)
    print(f"✓ Class test EPUB created: {output_path}")

if __name__ == '__main__':
    create_class_test_epub()
