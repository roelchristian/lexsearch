from src import cache_dir, stylesheet_path
from bs4 import BeautifulSoup

# TODO - rewrite this function to use jinja2


def render_html_from_json(data):
    '''
    renders a dictionary as an html page
    '''

    metadata = data['metadata']
    sections = data['sections']['section']

    ra_number = metadata['ra_details']['serial_number']

    html =f'''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta lang="en">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta description="Lex Search is a free and open source tool for searching the laws and jurisprudence of the Philippines.">
    <link rel="stylesheet" href="{stylesheet_path}">
    <title>LexSearch - RA {ra_number}</title>
    </head>
    <body>
    <h1>Republic Act {ra_number}</h1>
    <article>
    <div class="metadata-div">
    <p>RA Number: {metadata['ra_details']['serial_number']}</p>
    <p>RA Title: {metadata['ra_details']['long_title']}</p>
    <p>Congress: {metadata['congress']['congress_long_name']}</p>
    <div class="lex-search-small-print">
        <p>This file was generated by Lex Search, a free and open source tool for searching the laws and jurisprudence of the Philippines. For more information, visit <a href="https://github.com/roelchristian/lexsearch">the project's GitHub page</a>.</p>
        <p>
        <span class="small-print-link"><a href="https://github.com/roelchristian/lexsearch/blob/master/LICENSE">Licensed under MIT</a></span>
        <span class="small-print-link"><a href="https://github.com/roelchristian/lexsearch/blob/master/DISCLAIMER.MD">Disclaimer</a></span>
        </p>
    </div>
    </div>
    <div id = "sections">
    '''
    print(sections)
    for section in sections:
        html += f'''
        <div class="section">
        <h2 class="section-number">Section {section['section_number']}</h2>
        <div class="section-text">'''
        
    # wrap each paragraph in <p> tags on each line
        for paragraph in section['section_text'].splitlines():
            # replace non-Ascii characters with HTML entities
            paragraph = paragraph.encode('ascii', 'xmlcharrefreplace').decode('ascii')
        
            html += f'<p>{paragraph}</p>'
        


        html += '''
            </div>
            </div>
            '''
    html += '''        

    </div>
    </article>
    </body>
    </html>'''

    return html


def strip_html_tags(html):
    '''
    strips html tags from a string
    '''
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

