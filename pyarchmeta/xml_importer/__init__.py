from importlib import import_module

from .xml_ import XML_


def take(encoding:str, *args, **kwargs) -> any:

    try:
        if '.' in encoding:
            module_name, class_name = encoding.rsplit('.', 1)
        else:
            module_name = encoding
            class_name = encoding.upper()

        xml_module = import_module('.' + module_name, package='pyarchmeta.xml_importer')

        xml_class = getattr(xml_module, class_name)

        instance = xml_class(*args, **kwargs)


    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our xml encoding collection!'.format(encoding))
    else:
        if not issubclass(xml_class, XML_):
            raise ImportError("We currently don't have {}, but you are welcome to send in the request for it!".format(encoding))

    return instance
