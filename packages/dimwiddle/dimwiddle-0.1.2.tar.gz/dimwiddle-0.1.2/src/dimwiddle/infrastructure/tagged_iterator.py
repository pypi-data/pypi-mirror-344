import yaml

class TaggedIterator:
    """
    A tiny marker class to represent the special case of 'tagged_iterator'
    from the YAML file.
    """
    def __init__(self, tag: str, index_by: str):
        self.tag = tag
        self.index_by = index_by

def tagged_iterator_constructor(loader, node):
    """
    Custom constructor for YAML tag '!tagged_iterator'.
    Expects something like: { tag: 'agent', index_by: 'alias' }
    """
    # The node value will be a dict with "tag" and "index_by"
    mapping = loader.construct_mapping(node, deep=True)
    return TaggedIterator(tag=mapping["tag"], index_by=mapping["index_by"])

def register_tagged_iterator():
    """
    Register the tagged_iterator constructor with the YAML SafeLoader.
    This is automatically called when the package is imported.
    """
    yaml.SafeLoader.add_constructor('!tagged_iterator', tagged_iterator_constructor)

# Keep this for backward compatibility but use register_tagged_iterator() for new code
yaml.SafeLoader.add_constructor('!tagged_iterator', tagged_iterator_constructor)