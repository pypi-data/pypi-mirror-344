from functools import lru_cache
from typing import Generic, TypeVar, Type, Any, final


T = TypeVar("T")


@final
class EnvironmentVariable(Generic[T]):
    """
    Base class for creating custom wrapper subclasses on the fly.

    Note:
        This is just a base class used to create custom wrapper subclasses on the fly.
        You must never initialize these directly.
        You must use the :func:`create_env` function either on the main module or on an :class:`EnvVarFactory` to initialize your env vars.

    Example:
        Useful for enhancing type hints and __repr__ of variables that hold values you set with env vars.
        Note: This is just a helper class to create custom wrapper classes on the fly.
        You should never initialize these directly.

        Functionally, :class:`EnvironmentVariable` objects will work exactly the same as any instance of specified `typ`.

        In the example below, `some_var` can be used just like any other `int` object.

        .. code-block:: python

            import typed_envs
            some_var = typed_envs.create_env("SET_WITH_THIS_ENV", int, 10)

            >>> isinstance(some_var, int)
            True
            >>> isinstance(some_var, EnvironmentVariable)
            True

        There are only 2 differences between `some_var` and `int(10)`:
        - `some_var` will properly type check as an instance of both `int` and :class:`EnvironmentVariable`
        - `some_var.__repr__()` will include contextual information about the :class:`EnvironmentVariable`.

        .. code-block:: python

            >>> some_var
            EnvironmentVariable[int](name=`SET_WITH_THIS_ENV`, default_value=10, using_default=True)
            >>> str(some_var)
            "10"
            >>> some_var + 5
            15
            >>> 20 / some_var
            2

    See Also:
        :func:`create_env`, :class:`EnvVarFactory`
    """

    # TODO: give these docstrings
    _default_value: Any
    _using_default: bool
    _env_name: str
    _init_arg0: Any

    __origin__: Type[T]

    def __init__(self, *args, **kwargs) -> None:
        if type(self) is EnvironmentVariable:
            raise RuntimeError(
                "You should not initialize these directly, please use the factory"
            )
        try:
            super().__init__(*args, **kwargs)
        except TypeError as e:
            if (
                str(e)
                == "object.__init__() takes exactly one argument (the instance to initialize)"
            ):
                super().__init__()
            else:
                raise

    def __str__(self) -> str:
        base_type = self.__args__
        string_from_base = base_type.__str__(self)
        # NOTE: If this returns True, base type's `__str__` method calls `__repr__` and our custom `__repr__` breaks it.
        if string_from_base == repr(self):
            # We broke it but it's all good, we can fix it with some special case logic.
            return str(bool(self)) if base_type is bool else base_type.__repr__(self)
        return (
            base_type.__str__(self)
            if "object at 0x" in string_from_base
            else string_from_base
        )

    def __repr__(self) -> str:
        if self._using_default:
            return "EnvironmentVariable[{}](name=`{}`, default_value={}, using_default=True])".format(
                self.__args__.__qualname__,
                self._env_name,
                self._default_value,
            )
        else:
            return "EnvironmentVariable[{}](name=`{}`, default_value={}, current_value={}])".format(
                self.__args__.__qualname__,
                self._env_name,
                self._default_value,
                self._init_arg0,
            )

    def __class_getitem__(cls, type_arg: Type[T]) -> Type["EnvironmentVariable[T]"]:
        """
        Returns a mixed subclass of `type_arg` and :class:`EnvironmentVariable` that does 2 things:
         - modifies the __repr__ method so its clear an object's value was set with an env var while when inspecting variables
         - ensures the instance will type check as an :class:`EnvironmentVariable` object without losing information about its actual type

        Aside from these two things, subclass instances will function exactly the same as any other instance of `typ`.
        """
        return _build_subclass(type_arg)


@lru_cache(maxsize=None)
def _build_subclass(type_arg: Type[T]) -> Type["EnvironmentVariable[T]"]:
    """
    Returns a mixed subclass of `type_arg` and :class:`EnvironmentVariable` that does 2 things:
     - modifies the __repr__ method so its clear an object's value was set with an env var while when inspecting variables
     - ensures the instance will type check as an :class:`EnvironmentVariable` object without losing information about its actual type

    Aside from these two things, subclass instances will function exactly the same as any other instance of `typ`.
    """
    typed_cls_name = f"EnvironmentVariable[{type_arg.__name__}]"
    typed_cls_bases = (int if type_arg is bool else type_arg, EnvironmentVariable)
    typed_cls_dict = typed_class_dict = {
        "__repr__": EnvironmentVariable.__repr__,
        "__str__": EnvironmentVariable.__str__,
        "__args__": type_arg,
        "__module__": type_arg.__module__,
        "__qualname__": f"EnvironmentVariable[{type_arg.__qualname__}]",
        "__doc__": type_arg.__doc__,
        "__origin__": EnvironmentVariable,
    }
    if hasattr(type_arg, "__annotations__"):
        typed_cls_dict["__annotations__"] = type_arg.__annotations__
    if hasattr(type_arg, "__parameters__"):
        typed_cls_dict["__parameters__"] = type_arg.__parameters__
    typed_cls = type(typed_cls_name, typed_cls_bases, typed_cls_dict)
    return typed_cls
