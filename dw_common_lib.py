class dict_to_object(object):
    def __init__(self, dictionary):
        def _traverse(key, element):
            if isinstance(element, dict): return key, DictToObject(element)
            else: return key, element

        self.__dict__.update(
            dict(_traverse(k, v) for k, v in dictionary.items()))
