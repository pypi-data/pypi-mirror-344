import propertiesIO
def new(filepath):
    """
    Create a new properties
    """
    return propertiesIO.parse(filepath)
def get(filepath, key):
    """
    Get a property value
    """
    properties = propertiesIO.parse(filepath)
    return properties.get(properties, key)
def put(properties, key, value):
    properties.put(key, value)
def has(properties, key):
    return properties.has_key(key)
