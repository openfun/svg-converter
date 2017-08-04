class SVGFile(object):
    def __init__(self, **kwargs):
        for field in ('id', 'file'):
            setattr(self, field, kwargs.get(field, None))


