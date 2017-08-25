import tempfile
import os

from rest_framework import viewsets, status
from rest_framework import authentication, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.conf import settings
from django.http import HttpResponse

from converter.models import SVGFile
from converter.serializers import SVGFileSerializer

from converter.utils import get_all_files, get_file_content, get_file_obj_for_serializer
from converter.utils import CONVERTED_FILES_PREFIX
from converter.utils import get_convert_file


class TokenAuth(object):
    keyword = 'Token'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed('Invalid token')

        token = auth[1].decode()
        if token != settings.AUTH_TOKEN:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (None, token)

    def authenticate_header(self, request):
        return self.keyword


class SVGFileViewSet(viewsets.ViewSet):
    serializer_class = SVGFileSerializer
    authentication_classes = (TokenAuth,)
    permission_classes = tuple()


    def list(self, request):
        serializer = SVGFileSerializer( instance = get_all_files(), many = True)
        return Response (serializer.data)

    def retrieve(self, request, pk = None):
        if 'transform' in request.query_params:
            return get_convert_file(request.query_params['transform'], pk)

        filepath =  os.path.join(tempfile.gettempdir(),pk)
        filesize =  fsize = os.path.getsize(filepath)
        serializer = SVGFileSerializer(
            instance = SVGFile(id = pk, file = get_file_obj_for_serializer(filepath, filesize)) ,
            many = False)
        return Response (serializer.data)


    def create(self, request):
        serializer = SVGFileSerializer( data = request.data )
        if serializer.is_valid():
            (fd, temp_path) = tempfile.mkstemp(prefix=CONVERTED_FILES_PREFIX)
            with os.fdopen(fd, 'wb') as f:
                f.write(serializer.validated_data['file'].read())
                f.close()
                tempfilename = os.path.basename(temp_path)
                return Response({'status': True, 'identifier': tempfilename})

        return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if pk:
            filepath = os.path.join(tempfile.gettempdir(), pk)
            if os.path.exists(filepath):
                os.remove(filepath)
        return Response(status=status.HTTP_200_OK)
