"""Base schema set."""

import odin


class BaseSchema(odin.AnnotatedResource, abstract=True):
    """base metadata schema to use."""

    class Meta:
        """Meta class."""

        type_field = "type"
        namespace = None
