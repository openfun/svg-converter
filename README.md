SVG Converter REST API
----------------------

This is for now a very simple server that will accept an SVG file (POST) as an input and later be able to convert it
 to a PDF or PNG file. This is using Inkscape in the background and can be made to use Cairosvg.

Example of use via curl:

curl -X POST -F "file=@model.svg" -F "csrfmiddlewaretoken=N92mmDrmtT0GZ747Y5pHejFJLwONcH5s"  http://192.168.2.100:8000/svgfiles/?format=json

<That will return a file identifier>

curl -X GET  http://192.168.2.100:8000/converter/png/converter7nu1vbyr > test.png


Requirements
------------

It can be installed as a simple django application using a deployment script such as 
https://github.com/jcalazan/ansible-django-stack

 
TODO
----

For now this is very basic, but we could imagine (it is actually very crude, but works...):
- caching : make sure that we don't need to transform the file each time
- use of django storage
- storage of svg in the database instead of in the temp file folder



