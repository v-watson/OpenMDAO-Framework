"""
Variable meant to contain a VariableTree of a particular type.
"""

#public symbols
__all__ = ["VarTree"]

from inspect import isclass

from enthought.traits.api import Instance

from openmdao.main.variable import Variable, gui_excludes
from openmdao.main.vartree import VariableTree


class VarTree(Variable):
    """ A Variable for a :class:`VariableTree` of a particular type. """

    def __init__(self, klass=VariableTree, allow_none=True, **metadata):
        default_value = None

        if isinstance(klass, VariableTree):
            default_value = klass
            klass = klass.__class__
            if 'iotype' in metadata:
                default_value._iotype = metadata['iotype']
            else:
                metadata['iotype'] = default_value.iotype
        else:
            if isclass(klass) and issubclass(klass, VariableTree):
                if 'iotype' not in metadata:
                    raise ValueError('default_value is a class and no iotype'
                                     ' specified')
#                default_value = klass()
            else:
                raise TypeError('default_value must be a VariableTree instance'
                                ' or subclass')

        metadata.setdefault('copy', 'deep')
        self._allow_none = allow_none
        self.klass = klass
        self._instance = Instance(klass=klass, allow_none=False, factory=None,
                                  args=None, kw=None, **metadata)
        if default_value:
            self._instance.default_value = default_value
        else:
            default_value = self._instance.default_value
        super(VarTree, self).__init__(default_value, **metadata)

    def validate(self, obj, name, value):
        """ Validates that a specified value is valid for this trait. """
        if value is None:
            if self._allow_none:
                return value
            self.validate_failed(obj, name, value)

        try:
            value = self._instance.validate(obj, name, value)
        except Exception:
            obj.raise_exception('%s must be an instance of %s.%s' %
                                (name, self._instance.klass.__module__,
                                 self._instance.klass.__name__), TypeError)
        return value

    def post_setattr(self, obj, name, value):
        """ VariableTrees must know their place within the hierarchy, so set
        their parent here.  This keeps side effects out of validate(). """
        if value.parent is not obj:
            value.parent = obj
        value._iotype = self.iotype

    def get_attribute(self, name, value, trait, meta):
        """Return the attribute dictionary for this variable. This dict is
        used by the GUI to populate the edit UI. Slots also return an
        attribute dictionary for the slot pane.

        name: str
          Name of variable

        value: object
          The value of the variable

        trait: CTrait
          The variable's trait

        meta: dict
          Dictionary of metadata for this variable
        """
        io_attr = {}
        io_attr['name'] = name
        io_attr['type'] = trait.trait_type.klass.__name__
        io_attr['ttype'] = 'vartree'

        for field in meta:
            if field not in gui_excludes:
                io_attr[field] = meta[field]

        return io_attr, None

