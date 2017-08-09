SVG Converter REST API
----------------------

This is for now a very simple server that will accept an SVG file (POST) as an input and later be able to convert it
 to a PDF or PNG file. This is using Inkscape in the background and can be made to use Cairosvg.

Example of use via curl:

>  curl -X POST -F 'file=@_model.svg' -H 'Authorization: Token 48de857eedb88797209521a1695b0dc8d614afd4' http://127.0.0.1:8989/svgfiles/


It will return a file identifier which will be then used to get a specific version of the file (pdf or png): 

> curl -X GET  http://127.0.0.1:8989/converter/png/converterc7nu1vbyr > test.png


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



