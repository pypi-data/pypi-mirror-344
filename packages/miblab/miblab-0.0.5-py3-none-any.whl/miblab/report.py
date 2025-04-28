import sys
import os
import shutil
import csv

try:
    import pylatex as pl
    from pylatex.utils import NoEscape
    import_error = False
except:
    import_error = True

# filepaths need to be identified with importlib_resources
# rather than __file__ as the latter does not work at runtime
# when the package is installed via pip install

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

static = importlib_resources.files('miblab.static')
layout = importlib_resources.files('miblab.layout')
cover = str(static.joinpath('cover.jpg'))
epflreport = str(static.joinpath('epflreport.cls'))

#path = os.path.abspath("")

def force_move(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    os.rename(src, dst)

def force_copy(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copy(src, dst)

def force_move_dir(src, dst):
    force_copy_dir(src, dst)
    shutil.rmtree(src)

def force_copy_dir(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)



class Report(pl.Document):
    """
    Generate pdf reports in miblab style. 

    Parameters
    ----------
    reportpath : str
        Path to the folder where the report should be saved.
    title : str
        The title of the report.
    subtitle : str  
        The subtitle of the report.
    subject : str
        The subject of the report.
    author : str
        The author of the report.
    affiliation : str
        The affiliation of the author.
    contact : str
        The contact person for the report.
    institute : str
        The institute of the author.
    department : str
        The department of the author.
    email : str
        The email of the author.

    Example
    -------

    .. code-block:: python

        from miblab import Report

        # Where to save the report
        path = 'path/to/report/folder'

        # Setup the report
        doc = Report(path, title='My Report', author='Me')

        # Add a chapter
        doc.chapter('Chapter 1')

        # Add a section
        doc.section('Section 1')

        # Start a new page
        doc.clearpage()

        # Add a subsection
        doc.subsection('Section 1')

        # Add a figure
        doc.figure('figure.png', caption='This is a figure.')

        # Add a table
        doc.table('table.csv', caption='This is a table.')

        # Build the pdf report
        doc.build(doc)

    Note
    ----
    `miblab.Report` inherits from pylatex.Document, so can be used 
    in the same way as a pylatex.Document for full customization 
    options.
            
    """

    def __init__(
            self,
            reportpath,
            title='MIBLAB report', 
            subtitle='Subtitle', 
            subject='Subject',
            author='miblab.org',
            affiliation='https://miblab.org',  
            contact='Steven Sourbron',
            institute='University of Sheffield',
            department='Section of Medical Imaging and Technologies',
            email='s.sourbron@sheffield.ac.uk',      
        ):
        if import_error:
            raise NotImplementedError(
                'Please install miblab as pip install miblab[report]'
                'to use this function.'
            )
        super().__init__()
        self.path = reportpath
        setup(
            self, reportpath, title, subtitle, subject, author,
            affiliation, contact, institute, department, email,
        )

    def clearpage(self):
        """Continue on a new page.
        """
        self.append(NoEscape('\\clearpage'))

    def chapter(self, title):
        """Add a chapter to the report.

        Args:
            title (str): Chapter title.
        """
        chapter(self, title)


    def section(self, title, clearpage=False):
        """Add a section to the report.

        Args:
            title (str): Chapter title.
            clearpage (bool, optional): Start section on a new page
        """
        section(self, title, clearpage)


    def subsection(self, title, clearpage=False):
        """Add a subsection to the report.

        Args:
            title (str): Chapter title.
            clearpage (bool, optional): Start section on a new page
        """
        subsection(self, title, clearpage)


    def figure(self, file, width='6in', caption=None):
        """Add a figure to the report.

        Args:
            file (str): Path to the figure file.
            width (str, optional): Figure width. Defaults to '6in'.
            caption (str, optional): Caption for the figure. Defaults to None.
        """
        figure(self, file, width, caption)


    def table(self, file, cwidth=None, caption=None):
        """Add a table to the report.
        
        The table is created from a csv file. The first row is used as the header.

        Args:
            file (str): Path to the csv file.
            cwidth (str, optional): Column width. Defaults to None (automaticaly chosen).
            caption (str, optional): Caption for the table. Defaults to None.
        """
        table(self, file, cwidth, caption)


    def build(self, filename='report'):
        """Create the report.

        Parameters
        ----------
        filename (str, optional): str
            The name of the report. Defaults to 'report

        Raises
        ------
        NotImplementedError
            If miblab is not installed.
        """
        build(self, self.path, filename)




def setup(
        doc : pl.Document,
        reportpath,
        title='MIBLAB report', 
        subtitle='Subtitle', 
        subject='Subject',
        author='miblab.org',
        affiliation='https://miblab.org',  
        contact='Steven Sourbron',
        institute='University of Sheffield',
        department='Section of Medical Imaging and Technologies',
        email='s.sourbron@sheffield.ac.uk',       
    ):
    """Setup the report document.
    
    Parameters
    ----------
    doc : pylatex.Document
    reportpath : str
        Path to the folder where the report should be saved.
    title : str
        The title of the report.
    subtitle : str  
        The subtitle of the report.
    subject : str
        The subject of the report.
    author : str
        The author of the report.
    affiliation : str
        The affiliation of the author.
    contact : str
        The contact person for the report.
    institute : str
        The institute of the author.
    department : str
        The department of the author.
    email : str
        The email of the author.
        
    Returns
    -------             
    doc : pylatex.Document
        The report document.
    """
    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[report]'
            'to use this function.'
        )
    dst = os.path.abspath("")
    outputpath = os.path.join(reportpath, 'report')
    force_copy(cover, os.path.join(dst, 'cover.jpg'))
    force_copy(epflreport, os.path.join(dst, 'epflreport.cls'))
    force_copy_dir(layout._paths[0], os.path.join(outputpath, 'layout'))
    #doc = pl.Document()
    #doc = Report()
    doc.documentclass = pl.Command('documentclass',"epflreport")
    makecover(doc, title, subtitle, subject, author, affiliation)
    titlepage(doc, reportpath, contact, institute, department, email)

    doc.append(pl.NewPage())
    doc.append(NoEscape('\\tableofcontents'))
    doc.append(NoEscape('\\mainmatter'))
    #return doc


def makecover(
        doc: pl.Document, 
        title='MIBLAB report', 
        subtitle='Subtitle', 
        subject='Subject',
        author='miblab.org',
        affiliation='https://miblab.org',  
    ):
    """Add a cover page to the report.
    
    Parameters
    ----------
    doc : pylatex.Document
        The report document.
    title : str
        The title of the report.
    subtitle : str  
        The subtitle of the report.
    subject : str
        The subject of the report.
    author : str
        The author of the report.
    affiliation : str
        The affiliation of the author.
    """
    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[report]'
            'to use this function.')
    # Cover page
    doc.append(NoEscape('\\frontmatter'))
    doc.append(pl.Command('title', title))
    doc.append(pl.Command('subtitle', subtitle))
    doc.append(pl.Command('author', author))
    doc.append(pl.Command('subject', subject))
    doc.append(pl.Command('affiliation', affiliation))
    doc.append(pl.Command('coverimage', 'cover.jpg')) 
    doc.append(pl.Command('definecolor', arguments = ['title','HTML','FF0000'])) # Color for cover title
    doc.append(NoEscape('\\makecover'))


def titlepage(
        doc:pl.Document, 
        reportpath,
        contact='Steven Sourbron',
        institute='University of Sheffield',
        department='Section of Medical Imaging and Technologies',
        email='s.sourbron@sheffield.ac.uk',
    ):
    """Add a title page to the report.

    Parameters
    ----------
    doc : pylatex.Document
        The report document.
    reportpath : str
        Path to the folder where the report should be saved.
    contact : str
        The contact person for the report.
    institute : str
        The institute of the author.
    department : str
        The department of the author.
    email : str
        The email of the author.

    Raises
    ------
    NotImplementedError
        If miblab is not installed.
    """

    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[report]'
            'to use this function.')
    # Title page
    doc.append(pl.Command('begin', 'titlepage'))
    doc.append(pl.Command('begin', 'center'))
    # Title
    doc.append(NoEscape('\\makeatletter'))
    doc.append(NoEscape('\\largetitlestyle\\fontsize{45}{45}\\selectfont\\@title'))
    doc.append(NoEscape('\\makeatother'))
    # Subtitle
    doc.append(NoEscape('\\linebreak'))
    doc.append(NoEscape('\\makeatletter'))
    doc.append(
        pl.Command(
            'ifdefvoid', 
            arguments=[
                NoEscape('\\@subtitle'),
                '',
                NoEscape('\\bigskip\\titlestyle\\fontsize{20}{20}\\selectfont\\@subtitle'),
            ]
        )
    )
    # Author
    doc.append(NoEscape('\\makeatother'))
    doc.append(NoEscape('\\linebreak'))
    doc.append(NoEscape('\\bigskip'))
    doc.append(NoEscape('\\bigskip'))
    doc.append('by')
    doc.append(NoEscape('\\linebreak'))
    doc.append(NoEscape('\\bigskip'))
    doc.append(NoEscape('\\bigskip'))
    doc.append(NoEscape('\\makeatletter'))
    doc.append(NoEscape('\\largetitlestyle\\fontsize{25}{25}\\selectfont\\@author'))
    doc.append(NoEscape('\\makeatother'))
    doc.append(NoEscape('\\vfill'))
    # Table with information
    doc.append(NoEscape('\\large'))
    with doc.create(pl.Tabular('ll')) as tab:
        tab.add_hline()
        tab.add_row(['Report compiled by: ', contact])
        tab.add_row(['Institute: ', institute])
        tab.add_row(['Department: ', department])
        tab.add_row(['Email: ', email])
        tab.add_row(['Date: ', NoEscape('\\today')])
        tab.add_hline()
    # TRISTAN logo
    with doc.create(pl.Figure(position='b!')) as pic:
        pic.append(pl.Command('centering'))
        im = os.path.join(reportpath, 'report', 'layout', 'tristan-logo.jpg')
        pic.add_image(im, width='2in')
    doc.append(pl.Command('end', 'center'))
    doc.append(pl.Command('end', 'titlepage'))


def chapter(doc, title):
    """Add a chapter to the report.

    Args:
        doc (pylatex.Document): Insert in this document.
        title (str): Chapter title.
    """
    doc.append(NoEscape('\\clearpage'))
    doc.append(pl.Command('chapter', title)) 


def section(doc, title, clearpage=False):
    """Add a section to the report.

    Args:
        doc (pylatex.Document): Insert in this document.
        title (str): Chapter title.
        clearpage (bool, optional): Start section on a new page
    """
    if clearpage:
        doc.append(NoEscape('\\clearpage'))
    doc.append(pl.Section(title)) 


def subsection(doc, title, clearpage=False):
    """Add a subsection to the report.

    Args:
        doc (pylatex.Document): Insert in this document.
        title (str): Chapter title.
        clearpage (bool, optional): Start section on a new page
    """
    if clearpage:
        doc.append(NoEscape('\\clearpage'))
    doc.append(pl.Subsection(title)) 


def figure(doc, file, width='6in', caption=None):
    """Add a figure to the report.

    Args:
        doc (pylatex.Document): Insert in this document.
        file (str): Path to the figure file.
        width (str, optional): Figure width. Defaults to '6in'.
        caption (str, optional): Caption for the figure. Defaults to None.
    """
    if not os.path.exists(file):
        raise ValueError(
            f"Cannot insert figure.\n"
            f"Figure source file {file} does not exist."
        )
    with doc.create(pl.Figure(position='h!')) as pic:
        pic.add_image(file, width=width)
        if caption is not None:
            pic.add_caption(caption)


def table(doc, file, cwidth=None, caption=None):
    """Add a table to the report.
    
    The table is created from a csv file. The first row is used as the header.

    Args:
        doc (pylatex.Document): Insert in this document.
        file (str): Path to the csv file.
        cwidth (str, optional): Column width. Defaults to None (automaticaly chosen).
        caption (str, optional): Caption for the table. Defaults to None.
    """
    if not os.path.exists(file):
        raise ValueError(
            f"Cannot insert table.\n"
            f"Table source file {file} does not exist."
        )
    with open(file, mode='r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    cols = len(data[0]) - 1
    if cwidth is None:
        format = 'r' + 'c'*cols
    else:
        format = '|p{'+str(cwidth)+'cm}|'+('p{'+str(cwidth)+'cm}|')*cols
    with doc.create(pl.LongTable(format)) as table:
        table.add_hline()
        table.add_row(header)
        table.add_hline()
        for row in data:
            table.add_row(row)
        table.add_hline()
        if caption is not None:
            for char in ['_','#','$','%','&','{','}','^']:
                caption = caption.replace(char, '\\'+char)
            table.append(NoEscape(r'\caption{'+caption+r'} \\'))


def build(
        doc: pl.Document, 
        reportpath,
        filename='report',  
    ):
    """Create the report.

    Parameters
    ----------
    doc : pylatex.Document
        The report document.
    reportpath : str
        Path to the folder where the report should be saved.
    filename (str, optional): str
        The name of the report. Defaults to 'report

    Raises
    ------
    NotImplementedError
        If miblab is not installed.
    """
    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[report]'
            'to use this function.')
    path = os.path.abspath("")
    # Create report
    outputpath = os.path.join(reportpath, 'report')
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    
    # Build twice so all references are correct
    for _ in [1,2]:
        try:
            doc.generate_pdf(
                filename, 
                clean=False, 
                clean_tex=False, 
                compiler='pdfLaTeX', 
                compiler_args=['-output-directory', outputpath],
            )
        except UnicodeDecodeError:
            raise RuntimeError(
                "Can't build LaTeX file due to incorrect "
                "formatting. \nTo debug, build the document section "
                "by section."
            )

    # Move all files to output folder and clean up
    force_move(os.path.join(path, 'cover.jpg'), os.path.join(outputpath, 'cover.jpg'))
    force_move(os.path.join(path, 'epflreport.cls'), os.path.join(outputpath, 'epflreport.cls'))
    force_move(os.path.join(path, filename+'.tex'), os.path.join(outputpath, filename+'.tex'))


