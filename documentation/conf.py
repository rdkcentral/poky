# Configuration file for the Sphinx documentation builder.
#
# SPDX-License-Identifier: CC-BY-SA-2.0-UK
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys
import datetime
try:
    import yaml
except ImportError:
    sys.stderr.write("The Yocto Project Sphinx documentation requires PyYAML.\
    \nPlease make sure to install pyyaml Python package.\n")
    sys.exit(1)

# current_version = "dev"
# bitbake_version = "" # Leave empty for development branch
# Obtain versions from poky.yaml instead
with open("poky.yaml") as data:
    buff = data.read()
    subst_vars = yaml.safe_load(buff)
    if "DOCCONF_VERSION" not in subst_vars:
        sys.stderr.write("Please set DOCCONF_VERSION in poky.yaml")
        sys.exit(1)
    current_version = subst_vars["DOCCONF_VERSION"]
    if "BITBAKE_SERIES" not in subst_vars:
        sys.stderr.write("Please set BITBAKE_SERIES in poky.yaml")
        sys.exit(1)
    bitbake_version = subst_vars["BITBAKE_SERIES"]

# String used in sidebar
version = 'Version: ' + current_version
if current_version == 'dev':
    version = 'Version: Current Development'
# Version seen in documentation_options.js and hence in js switchers code
release = current_version


# -- Project information -----------------------------------------------------
project = 'The Yocto Project \xae'
copyright = '2010-%s, The Linux Foundation, CC-BY-SA-2.0-UK license' % datetime.datetime.now().year
author = 'The Linux Foundation'

# -- General configuration ---------------------------------------------------

# Prevent building with an outdated version of sphinx
needs_sphinx = "4.0"

# to load local extension from the folder 'sphinx'
sys.path.insert(0, os.path.abspath('sphinx'))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'yocto-vars'
]
autosectionlabel_prefix_document = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'boilerplate.rst']

# master document name. The default changed from contents to index. so better
# set it ourselves.
master_doc = 'index'

# create substitution for project configuration variables
rst_prolog = """
.. |project_name| replace:: %s
.. |copyright| replace:: %s
.. |author| replace:: %s
""" % (project, copyright, author)

# external links and substitutions
extlinks = {
    'bitbake_git': ('https://git.openembedded.org/bitbake%s', None),
    'cve_mitre': ('https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-%s', 'CVE-%s'),
    'cve_nist': ('https://nvd.nist.gov/vuln/detail/CVE-%s', 'CVE-%s'),
    'yocto_home': ('https://www.yoctoproject.org%s', None),
    'yocto_wiki': ('https://wiki.yoctoproject.org/wiki%s', None),
    'yocto_dl': ('https://downloads.yoctoproject.org%s', None),
    'yocto_lists': ('https://lists.yoctoproject.org%s', None),
    'yocto_bugs': ('https://bugzilla.yoctoproject.org%s', None),
    'yocto_ab': ('https://autobuilder.yoctoproject.org%s', None),
    'yocto_docs': ('https://docs.yoctoproject.org%s', None),
    'yocto_git': ('https://git.yoctoproject.org%s', None),
    'yocto_sstate': ('http://sstate.yoctoproject.org%s', None),
    'oe_home': ('https://www.openembedded.org%s', None),
    'oe_lists': ('https://lists.openembedded.org%s', None),
    'oe_git': ('https://git.openembedded.org%s', None),
    'oe_wiki': ('https://www.openembedded.org/wiki%s', None),
    'oe_layerindex': ('https://layers.openembedded.org%s', None),
    'oe_layer': ('https://layers.openembedded.org/layerindex/branch/master/layer%s', None),
    'wikipedia': ('https://en.wikipedia.org/wiki/%s', None),
}

# To be able to use :manpage:`<something>` in the docs.
manpages_url = 'https://manpages.debian.org/{path}'

# Intersphinx config to use cross reference with BitBake user manual
intersphinx_mapping = {
    'bitbake': ('https://docs.yoctoproject.org/bitbake/' + bitbake_version, None)
}

# Suppress "WARNING: unknown mimetype for ..."
suppress_warnings = ['epub.unknown_project_files']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
try:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_options = {
        'sticky_navigation': False,
    }
except ImportError:
    sys.stderr.write("The Sphinx sphinx_rtd_theme HTML theme was not found.\
    \nPlease make sure to install the sphinx_rtd_theme Python package.\n")
    sys.exit(1)

html_logo = 'sphinx-static/YoctoProject_Logo_RGB.jpg'
html_favicon = 'sphinx-static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['sphinx-static']

html_context = {
    'current_version': current_version,
}

# Add customm CSS and JS files
html_css_files = ['theme_overrides.css']
html_js_files = ['switchers.js']

# Hide 'Created using Sphinx' text
html_show_sphinx = False

# Add 'Last updated' on each page
html_last_updated_fmt = '%b %d, %Y'

# Remove the trailing 'dot' in section numbers
html_secnumber_suffix = " "

# We need XeTeX to process special unicode character, sometimes the contributor
# list from the release note contains those.
# See https://docs.readthedocs.io/en/stable/guides/pdf-non-ascii-languages.html.
latex_engine = 'xelatex'
latex_use_xindy = False
latex_elements = {
    'passoptionstopackages': '\\PassOptionsToPackage{bookmarksdepth=5}{hyperref}',
    'preamble': '\\usepackage[UTF8]{ctex}\n\\setcounter{tocdepth}{2}',
}


from sphinx.search import SearchEnglish
from sphinx.search import languages
class DashFriendlySearchEnglish(SearchEnglish):

    # Accept words that can include 'inner' hyphens or dots
    _word_re = re.compile(r'[\w]+(?:[\.\-][\w]+)*')

    js_splitter_code = r"""
function splitQuery(query) {
    return query
        .split(/[^\p{Letter}\p{Number}_\p{Emoji_Presentation}\-\.]+/gu)
        .filter(term => term.length > 0);
}
"""

languages['en'] = DashFriendlySearchEnglish

# Make the EPUB builder prefer PNG to SVG because of issues rendering Inkscape SVG
from sphinx.builders.epub3 import Epub3Builder
Epub3Builder.supported_image_types = ['image/png', 'image/gif', 'image/jpeg']
