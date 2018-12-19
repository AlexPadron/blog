import json
import os

import click
from flask import Flask, Markup, render_template
import markdown

from config import app_config


PAGES_DIR = 'pages/'
HOME_PAGE_TEMPLATE = 'home_page.html'
BLOG_PAGE_TEMPLATE = 'blog_page.html'
flask_app = Flask(__name__.split('.')[0])


all_md_content = {}
for md_file in os.listdir(PAGES_DIR):
    # skip .* files and metadata files
    if md_file.startswith('.') or md_file.endswith('.json'):
        continue

    md_path = PAGES_DIR + md_file

    with open(md_path) as f:
        md_content = f.read()

    md_key = md_file.replace('.md', '')

    with open(PAGES_DIR + md_key + '.json') as f:
        metadata = json.loads(f.read())

    all_md_content[md_key] = {
        'metadata': metadata,
        'content': md_content,
    }


@flask_app.route('/statusz', methods=['GET'], strict_slashes=False)
def statusz():
    """Get the statusz"""
    return 'Kowalski, status report!<br><br> -> Excellent', 200

@flask_app.route('/pages/<page>', methods=['GET'], strict_slashes=False)
def render_page(page):
    """Render content for a single page"""
    if page not in all_md_content:
        return 'Oh no! page not found', 200

    content = all_md_content[page]['content']
    markup_content = Markup(markdown.markdown(content))
    return render_template(BLOG_PAGE_TEMPLATE, content=markup_content)


@flask_app.route('/', methods=['GET'], strict_slashes=False)
def home_page():
    """Render the home page"""
    pages = [
        dict(url=x, **all_md_content[x]['metadata'])
        for x in all_md_content.keys()
    ]
    return render_template(HOME_PAGE_TEMPLATE, pages=pages, )


@click.group()
def cli():
    """Cli group"""
    pass


@cli.command()
def run():
    """Wrapper to kick off simple server"""
    flask_app.run(
        host=app_config.FLASK_HOST,
        port=app_config.FLASK_PORT,
        debug=app_config.FLASK_DEBUG
    )


if __name__ == '__main__':
    cli()
