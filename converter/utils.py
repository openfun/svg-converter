import hashlib

from tempfile import NamedTemporaryFile
import subprocess
import os
import glob
import tempfile
from converter.models import SVGFile


CONVERSION_TOOL_INKSCAPE = 1
CONVERSION_TOOL_CAIROSVG = 2
CONVERTED_FILES_PREFIX = 'converter'

def svg_converter(svgstringin, content_type="image/png", conversiontool=CONVERSION_TOOL_INKSCAPE):
    """
        This function callse Inkscape to convert to png or pdf. Cairosvg was not mature enough to enable nice styles or
        flowtext
        """
    convertedvalstring = ''
    if conversiontool == CONVERSION_TOOL_INKSCAPE:
        convertedvalstring = __convert_via_inkscape(svgstringin, content_type)
    else:
        convertedvalstring = cairosvg.surface.PDFSurface.convert(svgstringin)
    return convertedvalstring

def __convert_via_inkscape(stringin, content_type="image/png"):
    infile =  NamedTemporaryFile(delete=True)
    outfile = NamedTemporaryFile(delete=True)
    infile.write(stringin)
    infile.flush()
    exportarg = '--export-png='
    if content_type == "image/png":
        exportarg = '--export-png='
    elif content_type == "application/pdf":
        exportarg = '--export-pdf='
    subprocess.call(['inkscape', '-z','--export-background=#FFFFFF','--file=' + infile.name, exportarg + outfile.name])
    stringout = outfile.read()
    infile.close()
    outfile.close()
    return stringout


def get_file_hash(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda: f.read(128 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def get_all_files():
    filelist = []
    class Fileobject(object):
        def __init__(self, url, size):
            self.url = url
            self.size = size

    for fname in glob.glob(os.path.join(tempfile.gettempdir(), CONVERTED_FILES_PREFIX + "*")):
        fsize = os.path.getsize(fname)
        fo =  get_file_obj_for_serializer(fname,fsize)
        filelist. append(SVGFile(id = os.path.basename(fname), file = fo))
    return filelist

def get_file_obj_for_serializer(fname, fsize):
    class Fileobject(object):
        def __init__(self, url, size):
            self.url = url
            self.size = size
    return Fileobject(url= fname, size =fsize)

def get_file_content(filenameidentifier, format):
    filepath = os.path.join(tempfile.gettempdir(), filenameidentifier)
    outstring = ''
    mimetype = 'image/png'
    if os.path.exists(filepath):
        with open(filepath,'rb') as f:
            if format == 'pdf':
                mimetype = 'application/pdf'

            outstring = svg_converter(f.read(), content_type=mimetype)

    return (mimetype, outstring)