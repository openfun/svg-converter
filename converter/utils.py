import cairosvg
from tempfile import NamedTemporaryFile
import subprocess

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

