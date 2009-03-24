
#public symbols
__all__ = ["Factory"]

__version__ = "0.1"

    
class Factory(object):
    """Base class for objects that know how to create other objects
    based on a type argument and several optional arguments (version,
    server id, resource description, and name.
    """
    def __init__(self):
        pass
        
    def create(self, typname, name=None, version=None, server=None, 
               res_desc=None):
        """Return an object of type typename, using the specified
        package version, server location, and resource description.
        
        """
        raise NotImplementedError('create')
                
                
                    