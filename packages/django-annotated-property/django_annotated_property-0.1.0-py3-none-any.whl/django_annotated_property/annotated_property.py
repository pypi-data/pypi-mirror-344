from functools import wraps

def annotated_property(_func=None, *, annotation=None):
    """
    Decorator for property that checks if such annotation exists on the instance.
    Can save a lot of queries if the annotation is present.

    By default, it will look for an attribute named `annotated_<property_name>`.
    If you want to check for a different attribute, pass its name as `annotation` argument.

    Example:
        @annotated_property(annotation="custom_annotation_name")
        def my_property(self):
            ...
    """

    def decorator(func):
        prop_name = func.__name__
        annotation_name_to_check = annotation if annotation is not None else f"annotated_{prop_name}"

        @wraps(func)
        def _fget(self):
            if hasattr(self, annotation_name_to_check):
                # If the annotation exists, return its value (including None)
                return getattr(self, annotation_name_to_check)
            else:
                return func(self)
        return property(_fget)

    if _func is None:
        return decorator
    else:
        return decorator(_func)