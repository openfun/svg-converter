from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from converter.utils import svg_converter
from converter.utils import CONVERTED_FILES_PREFIX

from rest_framework.permissions import AllowAny

import tempfile
import os
from django.http import HttpResponse


class SVGUploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (AllowAny,)

    def put(self, request, filename, format = None):
        file_obj = request.data['file']

        (fd, temp_path) = tempfile.mkstemp(prefix=CONVERTED_FILES_PREFIX)
        with os.fdopen(fd, 'wb') as f:
            f.write(file_obj.read())
            f.close()
            tempfilename = os.path.basename(temp_path)

        datajson = { 'identifier': tempfilename}

        return Response(status=200,data=datajson)


def get_convert_file(request, filenameidentifier, format):
    filepath = os.path.join(tempfile.gettempdir(), filenameidentifier)
    datajson = {'success': False,}
    if os.path.exists(filepath):
        with open(filepath,'rb') as f:
            data = ''
            destformat = 'image/png'

            if format == 'pdf':
                destformat = 'application/pdf'

            outstring = svg_converter(f.read(), content_type=destformat)
            return HttpResponse(outstring, destformat)

    return HttpResponse(status=500)

