# -*- coding: utf-8 -*-
#
# Yade documentation build configuration file, created by
# sphinx-quickstart on Mon Nov 16 21:49:34 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# relevant posts to sphinx ML
# http://groups.google.com/group/sphinx-dev/browse_thread/thread/b4fbc8d31d230fc4
# http://groups.google.com/group/sphinx-dev/browse_thread/thread/118598245d5f479b

#####################
## custom yade roles
#####################
##
## http://docutils.sourceforge.net/docs/howto/rst-roles.html

import sys, os, re
from docutils import nodes
from sphinx import addnodes
from sphinx.roles import XRefRole
import docutils

#
# needed for creating hyperlink targets.
# it should be cleand up and unified for both LaTeX and HTML via
# the pending_xref node which gets resolved to real link target
# by sphinx automatically once all docs have been processed.
#
# xrefs: http://groups.google.com/group/sphinx-dev/browse_thread/thread/d719d19307654548
#
#
import __builtin__
if 'latex' in sys.argv: __builtin__.writer='latex'
elif 'html' in sys.argv: __builtin__.writer='html'
elif 'epub' in sys.argv: __builtin__.writer='epub'
else: raise RuntimeError("Must have either 'latex' or 'html' on the command line (hack for reference styles)")

sys.path.append(os.path.abspath('./..'))

def yaderef_role(role,rawtext,text,lineno,inliner,options={},content=[]):
	"Handle the :yref:`` role, by making hyperlink to yade.wrapper.*. It supports :yref:`Link text<link target>` syntax, like usual hyperlinking roles."
	id=rawtext.split(':',2)[2][1:-1]
	txt=id; explicitText=False
	m=re.match('(.*)\s*<(.*)>\s*',id)
	if m:
		explicitText=True
		txt,id=m.group(1),m.group(2)
	id=id.replace('::','.')
	#node=nodes.reference(rawtext,docutils.utils.unescape(txt),refuri='http://beta.arcig.cz/~eudoxos/yade/doxygen/?search=%s'%id,**options)
	#node=nodes.reference(rawtext,docutils.utils.unescape(txt),refuri='yade.wrapper.html#yade.wrapper.%s'%id,**options)
	return [mkYrefNode(id,txt,rawtext,role,explicitText,lineno,options)],[]

def yadesrc_role(role,rawtext,lineno,inliner,options={},content=[]):
	"Handle the :ysrc:`` role, making hyperlink to git repository webpage with that path. Supports :ysrc:`Link text<file/name>` syntax, like usual hyperlinking roles. If target ends with ``/``, it is assumed to be a directory."
	id=rawtext.split(':',2)[2][1:-1]
	txt=id
	m=re.match('(.*)\s*<(.*)>\s*',id)
	if m:
		txt,id=m.group(1),m.group(2)
	return [nodes.reference(rawtext,docutils.utils.unescape(txt),refuri='https://github.com/yade/trunk/blob/master/%s'%id)],[] ### **options should be passed to nodes.reference as well

# map modules to their html (rst) filenames. Used for sub-modules, where e.g. SpherePack is yade._packSphere.SpherePack, but is documented from yade.pack.rst
moduleMap={
	'yade._packPredicates':'yade.pack',
	'yade._packSpheres':'yade.pack',
	'yade._packObb':'yade.pack'
}

class YadeXRefRole(XRefRole):
	#def process_link
	def process_link(self, env, refnode, has_explicit_title, title, target):
		print 'TARGET:','yade.wrapper.'+target
		return '[['+title+']]','yade.wrapper.'+target

def mkYrefNode(target,text,rawtext,role,explicitText,lineno,options={}):
	"""Create hyperlink to yade target. Targets starting with literal 'yade.' are absolute, but the leading 'yade.' will be stripped from the link text. Absolute tergets are supposed to live in page named yade.[module].html, anchored at #yade.[module2].[rest of target], where [module2] is identical to [module], unless mapped over by moduleMap.
	
	Other targets are supposed to live in yade.wrapper (such as c++ classes)."""

	writer=__builtin__.writer # to make sure not shadowed by a local var
	import string
	if target.startswith('yade.'):
		module='.'.join(target.split('.')[0:2])
		module2=(module if module not in moduleMap.keys() else moduleMap[module])
		if target==module: target='' # to reference the module itself
		uri=('%%%s#%s'%(module2,target) if writer=='latex' else '%s.html#%s'%(module2,target))
		if not explicitText and module!=module2:
			text=module2+'.'+'.'.join(target.split('.')[2:])
		text=string.replace(text,'yade.','',1)
	elif target.startswith('external:'):
		exttarget=target.split(':',1)[1]
		if not explicitText: text=exttarget
		target=exttarget if '.' in exttarget else 'module-'+exttarget
		uri=(('%%external#%s'%target) if writer=='latex' else 'external.html#%s'%target)
	else:
		uri=(('%%yade.wrapper#yade.wrapper.%s'%target) if writer=='latex' else 'yade.wrapper.html#yade.wrapper.%s'%target)
		#print writer,uri
	return nodes.reference(rawtext,docutils.utils.unescape(text),refuri=uri,**options)
	#return [refnode],[]

def ydefault_role(role,rawtext,text,lineno,inliner,options={},content=[]):
	"Handle the :ydefault:`something` role. fixSignature handles it now in the member signature itself, this merely expands to nothing."
	return [],[]
def yattrtype_role(role,rawtext,text,lineno,inliner,options={},content=[]):
	"Handle the :yattrtype:`something` role. fixSignature handles it now in the member signature itself, this merely expands to nothing."
	return [],[]
# FIXME: should return readable representation of bits of the number (yade.wrapper.AttrFlags enum)
def yattrflags_role(role,rawtext,text,lineno,inliner,options={},content=[]):
	"Handle the :yattrflags:`something` role. fixSignature handles it now in the member signature itself."
	return [],[]

from docutils.parsers.rst import roles
def yaderef_role_2(type,rawtext,text,lineno,inliner,options={},content=[]): return YadeXRefRole()('yref',rawtext,text,lineno,inliner,options,content)
roles.register_canonical_role('yref', yaderef_role)
roles.register_canonical_role('ysrc', yadesrc_role)
roles.register_canonical_role('ydefault', ydefault_role)
roles.register_canonical_role('yattrtype', yattrtype_role)
roles.register_canonical_role('yattrflags', yattrflags_role)


## http://sphinx.pocoo.org/config.html#confval-rst_epilog
rst_epilog = """

.. |yupdate| replace:: *(auto-updated)*
.. |ycomp| replace:: *(auto-computed)*
.. |ystatic| replace:: *(static)*
"""

import collections
def customExclude(app, what, name, obj, skip, options):
	if name=='clone':
		if 'Serializable.clone' in str(obj): return False
		return True
	#escape crash on non iterable __doc__ in some qt object
	if hasattr(obj,'__doc__') and obj.__doc__ and not isinstance(obj.__doc__, collections.Iterable): return True
	if hasattr(obj,'__doc__') and obj.__doc__ and ('|ydeprecated|' in obj.__doc__ or '|yhidden|' in obj.__doc__): return True
	#if re.match(r'\b(__init__|__reduce__|__repr__|__str__)\b',name): return True
	if name.startswith('_'):
		if name=='__init__':
			# skip boost classes with parameterless ctor (arg1=implicit self)
			if obj.__doc__=="\n__init__( (object)arg1) -> None": return True
			# skip undocumented ctors
			if not obj.__doc__: return True
			# skip default ctor for serializable, taking dict of attrs
			if obj.__doc__=='\n__init__( (object)arg1) -> None\n\nobject __init__(tuple args, dict kwds)': return True
			#for i,l in enumerate(obj.__doc__.split('\n')): print name,i,l,'##'
			return False
		return True
	return False

def isBoostFunc(what,obj):
	return what=='function' and obj.__repr__().startswith('<Boost.Python.function object at 0x')

def isBoostMethod(what,obj):
	"I don't know how to distinguish boost and non-boost methods..."
	return what=='method' and obj.__repr__().startswith('<unbound method ');

def replaceLaTeX(s):
	# replace single non-escaped dollars $...$ by :math:`...`
	# then \$ by single $
	s=re.sub(r'(?<!\\)\$([^\$]+)(?<!\\)\$',r'\ :math:`\1`\ ',s)
	return re.sub(r'\\\$',r'$',s)

def fixSrc(app,docname,source):
	source[0]=replaceLaTeX(source[0])

def fixDocstring(app,what,name,obj,options,lines):
	# remove empty default roles, which is not properly interpreted by docutils parser
	for i in range(0,len(lines)):
		lines[i]=lines[i].replace(':ydefault:``','')
		lines[i]=lines[i].replace(':yattrtype:``','')
		lines[i]=lines[i].replace(':yattrflags:``','')
		#lines[i]=re.sub(':``',':` `',lines[i])
	# remove signature of boost::python function docstring, which is the first line of the docstring
	if isBoostFunc(what,obj):
		l2=boostFuncSignature(name,obj)[1]
		# we must replace lines one by one (in-place) :-|
		# knowing that l2 is always shorter than lines (l2 is docstring with the signature stripped off)
		for i in range(0,len(lines)):
			lines[i]=l2[i] if i<len(l2) else ''
	elif isBoostMethod(what,obj):
		l2=boostFuncSignature(name,obj)[1]
		for i in range(0,len(lines)):
			lines[i]=l2[i] if i<len(l2) else ''
	# LaTeX: replace $...$ by :math:`...`
	# must be done after calling boostFuncSignature which uses original docstring
	for i in range(0,len(lines)): lines[i]=replaceLaTeX(lines[i])


def boostFuncSignature(name,obj,removeSelf=False):
	"""Scan docstring of obj, returning tuple of properly formatted boost python signature
	(first line of the docstring) and the rest of docstring (as list of lines).
	The rest of docstring is stripped of 4 leading spaces which are automatically
	added by boost.
	
	removeSelf will attempt to remove the first argument from the signature.
	"""
	doc=obj.__doc__
	if doc==None: # not a boost method
		return None,None
	nname=name.split('.')[-1]
	docc=doc.split('\n')
	if len(docc)<2: return None,docc
	doc1=docc[1]
	# functions with weird docstring, likely not documented by boost
	if not re.match('^'+nname+r'(.*)->.*$',doc1):
		return None,docc
	if doc1.endswith(':'): doc1=doc1[:-1]
	strippedDoc=doc.split('\n')[2:]
	# check if all lines are padded
	allLinesHave4LeadingSpaces=True
	for l in strippedDoc:
		if l.startswith('    '): continue
		allLinesHave4LeadingSpaces=False; break
	# remove the padding if so
	if allLinesHave4LeadingSpaces: strippedDoc=[l[4:] for l in strippedDoc]
	for i in range(len(strippedDoc)):
		# fix signatures inside docstring (one function with multiple signatures)
		strippedDoc[i],n=re.subn(r'([a-zA-Z_][a-zA-Z0-9_]*\() \(object\)arg1(, |)',r'\1',strippedDoc[i].replace('->','→'))
	# inspect dosctring after mangling
	if 'getViscoelasticFromSpheresInteraction' in name and False:
		print name
		print strippedDoc
		print '======================'
		for l in strippedDoc: print l
		print '======================'
	sig=doc1.split('(',1)[1]
	if removeSelf:
		# remove up to the first comma; if no comma present, then the method takes no arguments
		# if [ precedes the comma, add it to the result (ugly!)
		try:
			ss=sig.split(',',1)
			if ss[0].endswith('['): sig='['+ss[1]
			else: sig=ss[1]
		except IndexError:
			# grab the return value
			try:
				sig=') -> '+sig.split('->')[-1]
		#if 'Serializable' in name: print 1000*'#',name
			except IndexError:
				sig=')'
	return '('+sig,strippedDoc

def fixSignature(app, what, name, obj, options, signature, return_annotation):
	#print what,name,obj,signature#,dir(obj)
	if what=='attribute':
		doc=unicode(obj.__doc__)
		ret=''
		m=re.match('.*:ydefault:`(.*?)`.*',doc)
		if m:
			typ=''
			#try:
			#	clss='.'.join(name.split('.')[:-1])
			#	instance=eval(clss+'()')
			#	typ='; '+getattr(instance,name.split('.')[-1]).__class__.__name__
			#	if typ=='; NoneType': typ=''
			#except TypeError: ##no registered converted
			#	typ=''
			dfl=m.group(1)
			m2=re.match(r'\s*\(\s*\(\s*void\s*\)\s*\"(.*)\"\s*,\s*(.*)\s*\)\s*',dfl)
			if m2: dfl="%s, %s"%(m2.group(2),m2.group(1))
			if dfl!='': ret+=' (='+dfl+'%s)'%typ
			else: ret+=' (=uninitalized%s)'%typ
		#m=re.match('.*\[(.{,8})\].*',doc)
		#m=re.match('.*:yunit:`(.?*)`.*',doc)
		#if m:
		#	units=m.group(1)
		#	print '@@@@@@@@@@@@@@@@@@@@@',name,units
		#	ret+=' ['+units+']'
		return ret,None
	elif what=='class':
		ret=[]
		if len(obj.__bases__)>0:
			base=obj.__bases__[0]
			while base.__module__!='Boost.Python':
				ret+=[base.__name__]
				if len(base.__bases__)>0: base=base.__bases__[0]
				else: break
		if len(ret):
			return ' (inherits '+u' → '.join(ret)+')',None
		else: return None,None
	elif isBoostFunc(what,obj):
		sig=boostFuncSignature(name,obj)[0] or ' (wrapped c++ function)'
		return sig,None
	elif isBoostMethod(what,obj):
		sig=boostFuncSignature(name,obj,removeSelf=True)[0]
		return sig,None
	#else: print what,name,obj.__repr__()
	#return None,None
		

from sphinx import addnodes
def parse_ystaticattr(env,attr,attrnode):
	m=re.match(r'([a-zA-Z0-9_]+)\.(.*)\(=(.*)\)',attr)
	if not m:
		print 100*'@'+' Static attribute %s not matched'%attr
		attrnode+=addnodes.desc_name(attr,attr)
	klass,name,default=m.groups()
	#attrnode+=addnodes.desc_type('static','static')
	attrnode+=addnodes.desc_name(name,name)
	plist=addnodes.desc_parameterlist()
	if default=='': default='unspecified'
	plist+=addnodes.desc_parameter('='+default,'='+default)
	attrnode+=plist
	attrnode+=addnodes.desc_annotation('  [static]','  [static]')
	return klass+'.'+name

#############################
## set tab size
###################
## http://groups.google.com/group/sphinx-dev/browse_thread/thread/35b8071ffe9a8feb
def setup(app):
	from sphinx.highlighting import lexers
	from pygments.lexers.compiled import CppLexer
	lexers['cpp'] = CppLexer(tabsize=3) 
	lexers['c++'] = CppLexer(tabsize=3) 
	from pygments.lexers.agile import PythonLexer
	lexers['python'] = PythonLexer(tabsize=3) 

	app.connect('source-read',fixSrc)
	
	app.connect('autodoc-skip-member',customExclude)
	app.connect('autodoc-process-signature',fixSignature)
	app.connect('autodoc-process-docstring',fixDocstring)
	app.add_description_unit('ystaticattr',None,objname='static attribute',indextemplate='pair: %s; static method',parse_node=parse_ystaticattr)


import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

#
# HACK: change ipython console regexp from ipython_console_highlighting.py
import re
sys.path.append(os.path.abspath('.'))

import yade.config

if 1:
	if yade.runtime.ipython_version<12:
		import ipython_directive as id
	else:
		if 12<=yade.runtime.ipython_version<13:
			import ipython_directive012 as id
                elif 13<=yade.runtime.ipython_version<200:
			import ipython_directive013 as id
                else:
			import ipython_directive200 as id

	#The next four lines are for compatibility with IPython 0.13.1
	ipython_rgxin =re.compile(r'(?:In |Yade )\[(\d+)\]:\s?(.*)\s*')
	ipython_rgxout=re.compile(r'(?:Out| ->  )\[(\d+)\]:\s?(.*)\s*')
	ipython_promptin ='Yade [%d]:'
	ipython_promptout=' ->  [%d]: '
	ipython_cont_spaces='     '
	#For IPython <=0.12, the following lines are used
	id.rgxin =re.compile(r'(?:In |Yade )\[(\d+)\]:\s?(.*)\s*')
	id.rgxout=re.compile(r'(?:Out| ->  )\[(\d+)\]:\s?(.*)\s*')
	id.rgxcont=re.compile(r'(?:   +)\.\.+:\s?(.*)\s*')
	id.fmtin  ='Yade [%d]:'
	id.fmtout =' ->  [%d]: '  # for some reason, out and cont must have the trailing space
	id.fmtcont='     .\D.: '
	id.rc_override=dict(prompt_in1="Yade [\#]:",prompt_in2="     .\D.:",prompt_out=r" ->  [\#]: ")
	if yade.runtime.ipython_version<12:
		id.reconfig_shell()

	import ipython_console_highlighting as ich
	ich.IPythonConsoleLexer.input_prompt = re.compile("(Yade \[[0-9]+\]: )")
	ich.IPythonConsoleLexer.output_prompt = re.compile("(( ->  |Out)|\[[0-9]+\]: )")
	ich.IPythonConsoleLexer.continue_prompt = re.compile("\s+\.\.\.+:")


extensions = [
		'sphinx.ext.autodoc',
		'sphinx.ext.autosummary',
		'sphinx.ext.coverage',
		'sphinx.ext.pngmath',
		'sphinx.ext.graphviz',
		'sphinx.ext.viewcode',
		'sphinx.ext.inheritance_diagram',
		'matplotlib.sphinxext.plot_directive',
		'matplotlib.sphinxext.only_directives',
		#'matplotlib.sphinxext.mathmpl',
		'ipython_console_highlighting',
		'youtube',
		'sphinx.ext.todo',
		]


if yade.runtime.ipython_version<12:
	extensions.append('ipython_directive')
else:
	if 12<=yade.runtime.ipython_version<13:
		extensions.append('ipython_directive012')
        elif 13<=yade.runtime.ipython_version<200:
		extensions.append('ipython_directive013')
        else:
		extensions.append('ipython_directive200')

# the sidebar extension
if False:
	if writer=='html':
		extensions+=['sphinx.ext.sidebar']

	sidebar_all=True
	sidebar_relling=True
	#sidebar_abbrev=True
	sidebar_tocdepth=3

## http://trac.sagemath.org/sage_trac/attachment/ticket/7549/trac_7549-doc_inheritance_underscore.patch
# GraphViz includes dot, neato, twopi, circo, fdp. 
graphviz_dot = 'dot' 
inheritance_graph_attrs = { 'rankdir' : 'BT' } 
inheritance_node_attrs = { 'height' : 0.5, 'fontsize' : 12, 'shape' : 'oval' } 
inheritance_edge_attrs = {} 

my_latex_preamble=r'''
\usepackage{euler} % must be loaded before fontspec for the whole doc (below); this must be kept for pngmath, however
\usepackage{hyperref}
\usepackage{amsmath}
\usepackage{amsbsy}
%\usepackage{mathabx}
\usepackage{underscore}
\usepackage[all]{xy}

% Metadata of the pdf output
\hypersetup{pdftitle={Reference Manual}}
\hypersetup{pdfauthor={Vaclav Smilauer; Emanuele Catalano; Bruno Chareyre; Sergei Dorofeenko; Jerome Duriez; Nolan Dyck; Burak Er; Jan Elias; Alexander Eulitz; Anton Gladky; Christian Jakob; Francois Kneib; Janek Kozicki; Donia Marzougui; Raphael Maurin; Chiara Modenese; Luc Scholtes; Luc Sibille; Jan Stransky; Thomas Sweijen; Klaus Thoeni; Chao Yuan}}
\hypersetup{pdfkeywords={Discrete element method; dem; yade; documentation; manual; python; c++; git}}

% symbols
\let\mat\boldsymbol % matrix
\let\vec\boldsymbol % vector
\let\tens\boldsymbol % tensor

\def\normalized#1{\widehat{#1}}
\def\locframe#1{\widetilde{#1}}

% timestep
\def\Dt{\Delta t}
\def\Dtcr{\Dt_{\rm cr}}

% algorithm complexity
\def\bigO#1{\ensuremath{\mathcal{O}(#1)}}

% variants for greek symbols
\let\epsilon\varepsilon
\let\theta\vartheta
\let\phi\varphi

% shorthands
\let\sig\sigma
\let\eps\epsilon

% variables at different points of time 
\def\prev#1{#1^-}
\def\pprev#1{#1^\ominus}
\def\curr#1{#1^{\circ}}
\def\nnext#1{#1^\oplus}
\def\next#1{#1^+}

% shorthands for geometry
\def\currn{\curr{\vec{n}}}
\def\currC{\curr{\vec{C}}}
\def\uT{\vec{u}_T}
\def\curruT{\curr{\vec{u}}_T}
\def\prevuT{\prev{\vec{u}}_T}
\def\currn{\curr{\vec{n}}}
\def\prevn{\prev{\vec{n}}}

% motion
\def\pprevvel{\pprev{\dot{\vec{u}}}}
\def\nnextvel{\nnext{\dot{\vec{u}}}}
\def\curraccel{\curr{\ddot{\vec{u}}}}
\def\prevpos{\prev{\vec{u}}}
\def\currpos{\curr{\vec{u}}}
\def\nextpos{\next{\vec{u}}}
\def\curraaccel{\curr{\dot{\vec{\omega}}}}
\def\pprevangvel{\pprev{\vec{\omega}}}
\def\nnextangvel{\nnext{\vec{\omega}}}
\def\loccurr#1{\curr{\locframe{#1}}}


\def\numCPU{n_{\rm cpu}}
\DeclareMathOperator{\Align}{Align}
\DeclareMathOperator{\sign}{sgn}


% sorting algorithms
\def\isleq#1{\currelem{#1}\ar@/^/[ll]^{\leq}}
\def\isnleq#1{\currelem{#1}\ar@/^/[ll]^{\not\leq}}
\def\currelem#1{\fbox{$#1$}}
\def\sortSep{||}
\def\sortInv{\hbox{\phantom{||}}}
\def\sortlines#1{\xymatrix@=3pt{#1}}
\def\crossBound{||\mkern-18mu<}

'''

pngmath_latex_preamble=r'\usepackage[active]{preview}'+my_latex_preamble

pngmath_use_preview=True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index-toctree-reference'

# General information about the project.
project = u'Yade'
copyright = u'2009, Václav Šmilauer'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = 'Yade documentation 2nd ed.'
# The full version, including alpha/beta/rc tags.
release = 'Yade documentation 2nd ed.'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build','../_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['yade.']


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'default'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {'stickysidebar':'true','collapsiblesidebar':'true','rightsidebar':'false'}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '../fig/yade-logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '../fig/yade-favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static-html']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

html_index='index.html'

# Additional templates that should be rendered to pages, maps page names to
# template names.
html_additional_pages = { 'index':'index.html'}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'Yadedoc'


# -- Options for LaTeX output --------------------------------------------------

my_maketitle=r'''
\begin{titlepage}

\begin{flushright}
\hrule{}

% Upper part of the page
\begin{flushright}
\includegraphics[width=0.15\textwidth]{yade-logo.png}\par
\end{flushright}
\vspace{20 mm}
\text{\sffamily\bfseries\Huge Reference Manual}\\
\vspace{20 mm}
%\vspace{70 mm}
\begin{sffamily}\bfseries\Large
V\'{a}clav \v{S}milauer, Emanuele Catalano, Bruno Chareyre, Sergei Dorofeenko, J\'er\^ome Duriez, Nolan Dyck, Jan Eliáš, Burak Er, Alexander Eulitz, Anton Gladky, Christian Jakob, Fran\c{c}ois Kneib, Janek Kozicki, Donia Marzougui, Rapha\"el Maurin, Chiara Modenese, Luc Scholt\`{e}s, Luc Sibille, Jan Str\'{a}nsk\'{y}, Thomas Sweijen, Klaus Thoeni, Chao Yuan
\end{sffamily}
\vspace{20 mm}
\hrule{}
\vfill
\textit{\large Yade Documentation 2nd edition, 2015}\\
\textit{based on Yade 1.14.0}\\
\end{flushright}

\end{titlepage}


\text{\sffamily\bfseries\large Citing this document:}\\
\v{S}milauer V. et al. (2015). Reference Manual. In:\textit{Yade Documentation 2nd ed.} doi:10.5281/zenodo.34045. http://yade-dem.org\\
See also http://yade-dem/doc/citing.html.

'''


latex_elements=dict(
	papersize='a4paper',
	fontpkg=r'''
\usepackage{euler}
\usepackage{fontspec,xunicode,xltxtra}
%\setmainfont[BoldFont={LMRoman10 Bold}]{CMU Concrete} %% CMU Concrete must be installed by hand as otf
	''',
	utf8extra='',
	fncychap='',
	preamble=my_latex_preamble,
	footer='',
	inputenc='',
	fontenc='',
	maketitle=my_maketitle,
)

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
   ('index-toctree-reference', 'YadeReference.tex', u'Reference Manual',
   u'Václav Šmilauer et al.', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = '../fig/yade-logo.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True
