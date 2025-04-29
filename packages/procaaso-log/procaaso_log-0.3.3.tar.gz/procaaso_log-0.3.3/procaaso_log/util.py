from typing import Dict, Any, TypeVar, Union, List
from functools import reduce

Mergable = Union[bool, str, int, float, List[Any], Dict[str, Any]]

TSource = TypeVar("TSource")


def patch_merge(source: TSource, patch: TSource) -> TSource:
    """Recursively merge two objects

    Args:
        source (TSource): Mutated object to merge into
        patch (TSource): Patch object to inject into source

    Raises:
        NotImplementedError: When two objects can't be merged

    Returns:
        TSource: The source object with merged contents
    """
    key = None
    try:
        if source is None or isinstance(source, (bool, str, int, float)):
            # border case for first run or if source is a primitive
            source = patch
        elif isinstance(source, list):
            if isinstance(patch, list):
                source = list(set(source) | set(patch))  # type: ignore
            else:
                raise TypeError('merge non-list "%s" into list "%s"' % (patch, source))
        elif isinstance(source, dict):
            # dicts must be merged
            if isinstance(patch, dict):
                for key in patch:
                    if key in source:
                        source[key] = patch_merge(source[key], patch[key])
                    else:
                        source[key] = patch[key]
            else:
                raise TypeError('merge non-dict "%s" into dict "%s"' % (patch, source))
        else:
            raise NotImplementedError('merge "%s" into "%s"' % (patch, source))
    except Exception as e:
        raise NotImplementedError(
            'merge "%s" in key "%s" when merging "%s" into "%s"'
            % (e, key, patch, source)
        ) from e

    return source


def merge_dict_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Reduce a set of logging dict config objects into one merged object

    Returns:
        Dict[str, Any]: Reduced dict config
    """
    return reduce(patch_merge, configs, {})
