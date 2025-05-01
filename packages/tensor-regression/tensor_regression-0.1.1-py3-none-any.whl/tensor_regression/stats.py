import functools
from typing import Any, Literal

import numpy as np


@functools.singledispatch
def get_simple_attributes(value: Any, precision: int | None) -> Any:
    """Function used to get simple statistics about a tensor / value / other.

    Register a custom handler for this if you want to add support for a new type.
    """
    raise NotImplementedError(
        f"get_simple_attributes doesn't have a registered handler for values of type {type(value)}"
    )


@get_simple_attributes.register(type(None))
def _get_none_attributes(value: None, precision: int | None):
    return {"type": "None"}


@get_simple_attributes.register(bool)
@get_simple_attributes.register(int)
@get_simple_attributes.register(float)
@get_simple_attributes.register(str)
def _get_bool_attributes(value: Any, precision: int | None):
    return {"value": value, "type": type(value).__name__}


@get_simple_attributes.register(list)
def list_simple_attributes(some_list: list[Any], precision: int | None):
    return {
        "length": len(some_list),
        "item_types": sorted(set(type(item).__name__ for item in some_list)),
        **{
            f"{i}": get_simple_attributes(item, precision=precision)
            for i, item in enumerate(
                some_list[:10]  # don't show all items, becomes redundant.
            )
        },
    }


@get_simple_attributes.register(dict)
def dict_simple_attributes(some_dict: dict[str, Any], precision: int | None):
    return {k: get_simple_attributes(v, precision=precision) for k, v in some_dict.items()}


def _maybe_round(v, precision: int | None):
    if precision is not None:
        if isinstance(v, int) or (isinstance(v, np.ndarray) and v.dtype.kind == "i"):
            return v
        return np.format_float_scientific(v, precision=precision)
    return v


@get_simple_attributes.register(np.ndarray)
def ndarray_simple_attributes(array: np.ndarray, precision: int | None) -> dict:
    return {
        "shape": tuple(array.shape),
        "dtype": f"numpy.{array.dtype}",
        # "hash": _hash(array),
        "min": _maybe_round(array.min().item(), precision=precision),
        "max": _maybe_round(array.max().item(), precision=precision),
        "sum": _maybe_round(array.sum().item(), precision=precision),
        "mean": _maybe_round(array.mean().item(), precision=precision),
    }


try:
    import torch

    @get_simple_attributes.register(torch.Tensor)
    def tensor_simple_attributes(tensor: torch.Tensor, precision: int | None) -> dict:
        if tensor.is_nested:
            # assert not [tensor_i.any() for tensor_i in tensor.unbind()], tensor
            # TODO: It might be a good idea to make a distinction here between '0' as the default, and
            # '0' as a value in the tensor? Hopefully this should be clear enough.
            tensor = tensor.to_padded_tensor(padding=0.0)

        return {
            "shape": _get_shape_ish(tensor),
            "dtype": str(tensor.dtype),
            # "hash": _hash(tensor),
            "min": _maybe_round(tensor.min().item(), precision),
            "max": _maybe_round(tensor.max().item(), precision),
            "sum": _maybe_round(tensor.sum().item(), precision),
            "mean": _maybe_round(tensor.float().mean().item(), precision),
            "device": (
                "cpu"
                if tensor.device.type == "cpu"
                else f"{tensor.device.type}:{tensor.device.index}"
            ),
        }

    def _get_shape_ish(t: torch.Tensor) -> tuple[int | Literal["?"], ...]:
        if not t.is_nested:
            return tuple(t.shape)
        dim_sizes = []
        for dim in range(t.ndim):
            try:
                dim_sizes.append(t.size(dim))
            except RuntimeError:
                dim_sizes.append("?")
        return tuple(dim_sizes)
except ImportError:
    pass
