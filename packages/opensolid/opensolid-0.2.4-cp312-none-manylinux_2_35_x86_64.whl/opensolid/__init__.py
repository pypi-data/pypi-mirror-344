"""A collection of classes for 2D/3D geometric modelling."""

from __future__ import annotations

import contextvars
import ctypes
import platform
from contextvars import ContextVar
from ctypes import CDLL, POINTER, c_char_p, c_double, c_int64, c_size_t, c_void_p
from pathlib import Path
from typing import Any, Union, overload


def _load_library() -> CDLL:
    """Load the native library from the same directory as __init__.py."""
    match platform.system():
        case "Windows":
            lib_file_name = "opensolid-ffi.dll"
        case "Darwin":
            lib_file_name = "libopensolid-ffi.dylib"
        case "Linux":
            lib_file_name = "libopensolid-ffi.so"
        case unsupported_system:
            raise OSError(unsupported_system + " is not yet supported")
    self_dir = Path(__file__).parent
    lib_path = self_dir / lib_file_name
    return ctypes.cdll.LoadLibrary(str(lib_path))


_lib: CDLL = _load_library()

# Define the signatures of the C API functions
# (also an early sanity check to make sure the library has been loaded OK)
_lib.opensolid_init.argtypes = []
_lib.opensolid_malloc.argtypes = [c_size_t]
_lib.opensolid_malloc.restype = c_void_p
_lib.opensolid_free.argtypes = [c_void_p]
_lib.opensolid_release.argtypes = [c_void_p]

# Initialize the Haskell runtime
_lib.opensolid_init()


class Error(Exception):
    """An error that may be thrown by OpenSolid functions."""


class _Text(ctypes.Union):
    _fields_ = (("as_char", c_char_p), ("as_void", c_void_p))


def _text_to_str(ptr: _Text) -> str:
    decoded = ptr.as_char.decode("utf-8")
    _lib.opensolid_free(ptr.as_void)
    return decoded


def _str_to_text(s: str) -> _Text:
    encoded = s.encode("utf-8")
    buffer = ctypes.create_string_buffer(encoded)
    return _Text(as_char=ctypes.cast(buffer, c_char_p))


def _list_argument(list_type: Any, array: Any) -> Any:  # noqa: ANN401
    return list_type(len(array), array)


def _error(message: str) -> Any:  # noqa: ANN401
    raise Error(message)


class Tolerance:
    """Manages a tolerance context value.

    Many functions in OpenSolid require a tolerance to be set.
    You should generally choose a value that is
    much smaller than any meaningful size/dimension in the geometry you're modelling,
    but significantly *larger* than any expected numerical roundoff that might occur.
    A good default choice is roughly one-billionth of the overall size of your geometry;
    for 'human-scale' things (say, from an earring up to a house)
    that means that one nanometer is a reasonable value to use.

    Passing a tolerance into every function that needed one would get very verbose,
    and it's very common to choose a single tolerance value and use it throughout a project.
    However, it's also occasionally necessary to set a different tolerance for some code.
    This class allows managing tolerances using Python's ``with`` statement, e.g.::

        with Tolerance(Length.nanometer):
            do_something()
            do_something_else()
            with Tolerance(Angle.degrees(0.001)):
                compare_two_angles()
            do_more_things()

    In the above code, the ``Length.nanometer`` tolerance value
    will be used for ``do_something()`` and ``do_something_else()``
    (and any functions they call).
    The ``Angle.degrees(0.001))`` tolerance value
    will then be used for ``compare_two_angles()``,
    and then the ``Length.nanometer`` tolerance value will be restored
    and used for ``do_more_things()``.
    """

    Value = Union[float, "Length", "Area", "Angle"]

    _value: Value
    _token: contextvars.Token[Value] | None = None

    def __init__(self, value: Value) -> None:
        self._value = value

    def __enter__(self) -> None:
        """Set the given tolerance as the currently active one."""
        assert self._token is None
        self._token = _tolerance.set(self._value)

    def __exit__(
        self, _exception_type: object, _exception_value: object, _traceback: object
    ) -> None:
        """Restore the previous tolerance as the currently active one."""
        assert self._token is not None
        _tolerance.reset(self._token)
        self._token = None

    @staticmethod
    def current() -> Value:
        """Get the current tolerance value."""
        try:
            return _tolerance.get()
        except LookupError as error:
            message = 'No tolerance set, please set one using "with Tolerance(...)"'
            raise LookupError(message) from error


_tolerance: ContextVar[Tolerance.Value] = ContextVar("tolerance")


def _current_tolerance[T](expected_type: type[T]) -> T:
    current_tolerance = Tolerance.current()
    if not isinstance(current_tolerance, expected_type):
        message = (
            "Expected a tolerance of type "
            + expected_type.__name__
            + " but current tolerance is of type "
            + type(current_tolerance).__name__
        )
        raise TypeError(message)
    return current_tolerance


def _float_tolerance() -> float:
    return _current_tolerance(float)


def _length_tolerance() -> Length:
    return _current_tolerance(Length)


def _area_tolerance() -> Area:
    return _current_tolerance(Area)


def _angle_tolerance() -> Angle:
    return _current_tolerance(Angle)


class _Tuple2_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_void_p), ("field1", c_void_p)]


class _List_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", POINTER(c_void_p))]


class _Tuple2_c_int64_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", c_void_p)]


class _Tuple3_c_void_p_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_void_p), ("field1", c_void_p), ("field2", c_void_p)]


class _Tuple3_Text_c_void_p_List_c_void_p(ctypes.Structure):
    _fields_ = [("field0", _Text), ("field1", c_void_p), ("field2", _List_c_void_p)]


class _Result_c_int64(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", _Text), ("field2", c_int64)]


class _Tuple3_c_void_p_c_double_c_double(ctypes.Structure):
    _fields_ = [("field0", c_void_p), ("field1", c_double), ("field2", c_double)]


class _Tuple2_c_void_p_c_double(ctypes.Structure):
    _fields_ = [("field0", c_void_p), ("field1", c_double)]


class _Tuple4_c_void_p_List_c_void_p_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [
        ("field0", c_void_p),
        ("field1", _List_c_void_p),
        ("field2", c_void_p),
        ("field3", c_void_p),
    ]


class _Tuple4_c_void_p_Text_List_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [
        ("field0", c_void_p),
        ("field1", _Text),
        ("field2", _List_c_void_p),
        ("field3", c_void_p),
    ]


class _Tuple4_c_void_p_c_void_p_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [
        ("field0", c_void_p),
        ("field1", c_void_p),
        ("field2", c_void_p),
        ("field3", c_void_p),
    ]


class _Result_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", _Text), ("field2", c_void_p)]


class _Tuple5_c_void_p_c_void_p_c_void_p_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [
        ("field0", c_void_p),
        ("field1", c_void_p),
        ("field2", c_void_p),
        ("field3", c_void_p),
        ("field4", c_void_p),
    ]


class _Tuple3_c_void_p_c_double_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_void_p), ("field1", c_double), ("field2", c_void_p)]


class _List_List_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", POINTER(_List_c_void_p))]


class _Tuple3_c_double_c_void_p_c_double(ctypes.Structure):
    _fields_ = [("field0", c_double), ("field1", c_void_p), ("field2", c_double)]


class _Tuple2_c_double_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_double), ("field1", c_void_p)]


class _Tuple2_c_double_List_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_double), ("field1", _List_c_void_p)]


class _Tuple2_c_void_p_List_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_void_p), ("field1", _List_c_void_p)]


class _Tuple4_c_void_p_List_c_void_p_c_void_p_List_c_void_p(ctypes.Structure):
    _fields_ = [
        ("field0", c_void_p),
        ("field1", _List_c_void_p),
        ("field2", c_void_p),
        ("field3", _List_c_void_p),
    ]


class _Tuple5_c_double_c_void_p_c_void_p_c_void_p_c_double(ctypes.Structure):
    _fields_ = [
        ("field0", c_double),
        ("field1", c_void_p),
        ("field2", c_void_p),
        ("field3", c_void_p),
        ("field4", c_double),
    ]


class _Tuple4_c_void_p_c_double_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [
        ("field0", c_void_p),
        ("field1", c_double),
        ("field2", c_void_p),
        ("field3", c_void_p),
    ]


class _Tuple4_c_double_c_void_p_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [
        ("field0", c_double),
        ("field1", c_void_p),
        ("field2", c_void_p),
        ("field3", c_void_p),
    ]


class _Tuple3_c_double_c_double_c_double(ctypes.Structure):
    _fields_ = [("field0", c_double), ("field1", c_double), ("field2", c_double)]


class _Tuple3_List_c_void_p_c_void_p_c_void_p(ctypes.Structure):
    _fields_ = [("field0", _List_c_void_p), ("field1", c_void_p), ("field2", c_void_p)]


class _Tuple2_List_c_void_p_List_c_void_p(ctypes.Structure):
    _fields_ = [("field0", _List_c_void_p), ("field1", _List_c_void_p)]


class _Result_List_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", _Text), ("field2", _List_c_void_p)]


class _Tuple2_c_double_c_double(ctypes.Structure):
    _fields_ = [("field0", c_double), ("field1", c_double)]


class _Tuple3_c_int64_c_int64_c_int64(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", c_int64), ("field2", c_int64)]


class _Maybe_c_void_p(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", c_void_p)]


class _List_c_double(ctypes.Structure):
    _fields_ = [("field0", c_int64), ("field1", POINTER(c_double))]


class Length:
    """A length in millimeters, meters, inches etc.

    Represented internally as a value in meters.
    """

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Length:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Length)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: Length = None  # type: ignore[assignment]
    """The zero value."""

    @staticmethod
    def meters(value: float) -> Length:
        """Construct a length from a number of meters."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Length_meters_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    @staticmethod
    def centimeters(value: float) -> Length:
        """Construct a length from a number of centimeters."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Length_centimeters_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    @staticmethod
    def millimeters(value: float) -> Length:
        """Construct a length value from a number of millimeters."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Length_millimeters_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    @staticmethod
    def micrometers(value: float) -> Length:
        """Construct a length from a number of micrometers."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Length_micrometers_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    @staticmethod
    def nanometers(value: float) -> Length:
        """Construct a length from a number of nanometers."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Length_nanometers_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    @staticmethod
    def inches(value: float) -> Length:
        """Construct a length from a number of inches."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Length_inches_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    @staticmethod
    def pixels(value: float) -> Length:
        """Construct a length from a number of CSS pixels."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Length_pixels_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    def in_meters(self) -> float:
        """Convert a length to a number of meters."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Length_inMeters(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_centimeters(self) -> float:
        """Convert a length to a number of centimeters."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Length_inCentimeters(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_millimeters(self) -> float:
        """Convert a length to a number of millimeters."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Length_inMillimeters(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_micrometers(self) -> float:
        """Convert a length to a number of micrometers."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Length_inMicrometers(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_nanometers(self) -> float:
        """Convert a length to a number of nanometers."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Length_inNanometers(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_inches(self) -> float:
        """Convert a length to a number of inches."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Length_inInches(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_pixels(self) -> float:
        """Convert a length into a number of CSS pixels."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Length_inPixels(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def is_zero(self) -> bool:
        """Check if a length is zero, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_Length_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``.

        Note that this is an *exact* comparison; for a tolerant comparison
        (one which will return true if two values are *almost* equal)
        you'll likely want to use an ``is_zero()`` method instead.
        """
        if not isinstance(other, Length):
            return False
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, other._ptr)
        output = c_int64()
        _lib.opensolid_Length_eq(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def _compare(self, other: Length) -> int:
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, other._ptr)
        output = c_int64()
        _lib.opensolid_Length_compare(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def __lt__(self, other: Length) -> bool:
        """Return ``self < other``."""
        return self._compare(other) < 0

    def __le__(self, other: Length) -> bool:
        """Return ``self <= other``."""
        return self._compare(other) <= 0

    def __ge__(self, other: Length) -> bool:
        """Return ``self >= other``."""
        return self._compare(other) >= 0

    def __gt__(self, other: Length) -> bool:
        """Return ``self > other``."""
        return self._compare(other) > 0

    def __neg__(self) -> Length:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Length_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    def __abs__(self) -> Length:
        """Return ``abs(self)``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Length_abs(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    @overload
    def __add__(self, rhs: Length) -> Length:
        pass

    @overload
    def __add__(self, rhs: LengthRange) -> LengthRange:
        pass

    @overload
    def __add__(self, rhs: LengthCurve) -> LengthCurve:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_add_Length_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_add_Length_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_add_Length_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: Length) -> Length:
        pass

    @overload
    def __sub__(self, rhs: LengthRange) -> LengthRange:
        pass

    @overload
    def __sub__(self, rhs: LengthCurve) -> LengthCurve:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_sub_Length_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_sub_Length_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_sub_Length_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> Length:
        pass

    @overload
    def __mul__(self, rhs: Length) -> Area:
        pass

    @overload
    def __mul__(self, rhs: Range) -> LengthRange:
        pass

    @overload
    def __mul__(self, rhs: LengthRange) -> AreaRange:
        pass

    @overload
    def __mul__(self, rhs: Curve) -> LengthCurve:
        pass

    @overload
    def __mul__(self, rhs: LengthCurve) -> AreaCurve:
        pass

    @overload
    def __mul__(self, rhs: Direction2d) -> Displacement2d:
        pass

    @overload
    def __mul__(self, rhs: Vector2d) -> Displacement2d:
        pass

    @overload
    def __mul__(self, rhs: Displacement2d) -> AreaVector2d:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement2d._new(output)
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement2d._new(output)
            case Displacement2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_mul_Length_Displacement2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector2d._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> Length:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> float:
        pass

    @overload
    def __truediv__(self, rhs: Range) -> LengthRange:
        pass

    @overload
    def __truediv__(self, rhs: LengthRange) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Curve) -> LengthCurve:
        pass

    @overload
    def __truediv__(self, rhs: LengthCurve) -> Curve:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Length_div_Length_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Length_div_Length_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_div_Length_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_div_Length_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_div_Length_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Length_div_Length_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case _:
                return NotImplemented

    def __floordiv__(self, rhs: Length) -> int:
        """Return ``self // rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_int64()
        _lib.opensolid_Length_floorDiv_Length_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def __mod__(self, rhs: Length) -> Length:
        """Return ``self % rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Length_mod_Length_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def __rmul__(self, lhs: float) -> Length:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Length_mul_Float_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        return "Length.meters(" + str(self.in_meters()) + ")"


def _length_zero() -> Length:
    output = c_void_p()
    _lib.opensolid_Length_zero(c_void_p(), ctypes.byref(output))
    return Length._new(output)


Length.zero = _length_zero()


class Area:
    """An area in square meters, square inches etc.

    Represented internally as a value in square meters.
    """

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Area:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Area)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: Area = None  # type: ignore[assignment]
    """The zero value."""

    @staticmethod
    def square_meters(value: float) -> Area:
        """Construct an area from a number of square meters."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Area_squareMeters_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Area._new(output)

    @staticmethod
    def square_inches(value: float) -> Area:
        """Construct an area from a number of square inches."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Area_squareInches_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Area._new(output)

    def in_square_meters(self) -> float:
        """Convert an area to a number of square meters."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Area_inSquareMeters(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_square_inches(self) -> float:
        """Convert an area to a number of square inches."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Area_inSquareInches(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def is_zero(self) -> bool:
        """Check if an area is zero, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_area_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_Area_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``.

        Note that this is an *exact* comparison; for a tolerant comparison
        (one which will return true if two values are *almost* equal)
        you'll likely want to use an ``is_zero()`` method instead.
        """
        if not isinstance(other, Area):
            return False
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, other._ptr)
        output = c_int64()
        _lib.opensolid_Area_eq(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def _compare(self, other: Area) -> int:
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, other._ptr)
        output = c_int64()
        _lib.opensolid_Area_compare(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def __lt__(self, other: Area) -> bool:
        """Return ``self < other``."""
        return self._compare(other) < 0

    def __le__(self, other: Area) -> bool:
        """Return ``self <= other``."""
        return self._compare(other) <= 0

    def __ge__(self, other: Area) -> bool:
        """Return ``self >= other``."""
        return self._compare(other) >= 0

    def __gt__(self, other: Area) -> bool:
        """Return ``self > other``."""
        return self._compare(other) > 0

    def __neg__(self) -> Area:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Area_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Area._new(output)

    def __abs__(self) -> Area:
        """Return ``abs(self)``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Area_abs(ctypes.byref(inputs), ctypes.byref(output))
        return Area._new(output)

    @overload
    def __add__(self, rhs: Area) -> Area:
        pass

    @overload
    def __add__(self, rhs: AreaRange) -> AreaRange:
        pass

    @overload
    def __add__(self, rhs: AreaCurve) -> AreaCurve:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_add_Area_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case AreaRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_add_Area_AreaRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case AreaCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_add_Area_AreaCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: Area) -> Area:
        pass

    @overload
    def __sub__(self, rhs: AreaRange) -> AreaRange:
        pass

    @overload
    def __sub__(self, rhs: AreaCurve) -> AreaCurve:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_sub_Area_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case AreaRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_sub_Area_AreaRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case AreaCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_sub_Area_AreaCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> Area:
        pass

    @overload
    def __mul__(self, rhs: Range) -> AreaRange:
        pass

    @overload
    def __mul__(self, rhs: Curve) -> AreaCurve:
        pass

    @overload
    def __mul__(self, rhs: Direction2d) -> AreaVector2d:
        pass

    @overload
    def __mul__(self, rhs: Vector2d) -> AreaVector2d:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Area_mul_Area_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_mul_Area_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_mul_Area_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_mul_Area_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector2d._new(output)
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_mul_Area_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector2d._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> Area:
        pass

    @overload
    def __truediv__(self, rhs: Area) -> float:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> Length:
        pass

    @overload
    def __truediv__(self, rhs: Range) -> AreaRange:
        pass

    @overload
    def __truediv__(self, rhs: LengthRange) -> LengthRange:
        pass

    @overload
    def __truediv__(self, rhs: AreaRange) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Curve) -> AreaCurve:
        pass

    @overload
    def __truediv__(self, rhs: LengthCurve) -> LengthCurve:
        pass

    @overload
    def __truediv__(self, rhs: AreaCurve) -> Curve:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Area_div_Area_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Area_div_Area_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_div_Area_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_div_Area_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_div_Area_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case AreaRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_div_Area_AreaRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_div_Area_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_div_Area_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case AreaCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Area_div_Area_AreaCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case _:
                return NotImplemented

    def __floordiv__(self, rhs: Area) -> int:
        """Return ``self // rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_int64()
        _lib.opensolid_Area_floorDiv_Area_Area(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def __mod__(self, rhs: Area) -> Area:
        """Return ``self % rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Area_mod_Area_Area(ctypes.byref(inputs), ctypes.byref(output))
        return Area._new(output)

    def __rmul__(self, lhs: float) -> Area:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Area_mul_Float_Area(ctypes.byref(inputs), ctypes.byref(output))
        return Area._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        return "Area.square_meters(" + str(self.in_square_meters()) + ")"


def _area_zero() -> Area:
    output = c_void_p()
    _lib.opensolid_Area_zero(c_void_p(), ctypes.byref(output))
    return Area._new(output)


Area.zero = _area_zero()


class Angle:
    """An angle in degrees, radians, turns etc.

    Represented internally as a value in radians.
    """

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Angle:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Angle)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: Angle = None  # type: ignore[assignment]
    """The zero value."""

    golden_angle: Angle = None  # type: ignore[assignment]
    """The [golden angle](https://en.wikipedia.org/wiki/Golden_angle)."""

    radian: Angle = None  # type: ignore[assignment]
    """One radian."""

    full_turn: Angle = None  # type: ignore[assignment]
    """One full turn, or 360 degrees."""

    half_turn: Angle = None  # type: ignore[assignment]
    """One half turn, or 180 degrees."""

    quarter_turn: Angle = None  # type: ignore[assignment]
    """One quarter turn, or 90 degrees."""

    pi: Angle = None  # type: ignore[assignment]
    """π radians, or 180 degrees."""

    two_pi: Angle = None  # type: ignore[assignment]
    """2π radians, or 360 degrees."""

    @staticmethod
    def radians(value: float) -> Angle:
        """Construct an angle from a number of radians."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Angle_radians_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    @staticmethod
    def degrees(value: float) -> Angle:
        """Construct an angle from a number of degrees."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Angle_degrees_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    @staticmethod
    def turns(value: float) -> Angle:
        """Construct an angle from a number of turns.

        One turn is equal to 360 degrees.
        """
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Angle_turns_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    @staticmethod
    def acos(value: float) -> Angle:
        """Compute the inverse cosine of a value."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Angle_acos_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    @staticmethod
    def asin(value: float) -> Angle:
        """Compute the inverse sine of a value."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Angle_asin_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    @staticmethod
    def atan(value: float) -> Angle:
        """Compute the inverse tangent of a value."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Angle_atan_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    def in_radians(self) -> float:
        """Convert an angle to a number of radians."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Angle_inRadians(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_degrees(self) -> float:
        """Convert an angle to a number of degrees."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Angle_inDegrees(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def in_turns(self) -> float:
        """Convert an angle to a number of turns.

        One turn is equal to 360 degrees.
        """
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Angle_inTurns(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def is_zero(self) -> bool:
        """Check if an angle is zero, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_angle_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_Angle_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def sin(self) -> float:
        """Compute the sine of an angle."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Angle_sin(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def cos(self) -> float:
        """Compute the cosine of an angle."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Angle_cos(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def tan(self) -> float:
        """Compute the tangent of an angle."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Angle_tan(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``.

        Note that this is an *exact* comparison; for a tolerant comparison
        (one which will return true if two values are *almost* equal)
        you'll likely want to use an ``is_zero()`` method instead.
        """
        if not isinstance(other, Angle):
            return False
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, other._ptr)
        output = c_int64()
        _lib.opensolid_Angle_eq(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def _compare(self, other: Angle) -> int:
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, other._ptr)
        output = c_int64()
        _lib.opensolid_Angle_compare(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def __lt__(self, other: Angle) -> bool:
        """Return ``self < other``."""
        return self._compare(other) < 0

    def __le__(self, other: Angle) -> bool:
        """Return ``self <= other``."""
        return self._compare(other) <= 0

    def __ge__(self, other: Angle) -> bool:
        """Return ``self >= other``."""
        return self._compare(other) >= 0

    def __gt__(self, other: Angle) -> bool:
        """Return ``self > other``."""
        return self._compare(other) > 0

    def __neg__(self) -> Angle:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Angle_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    def __abs__(self) -> Angle:
        """Return ``abs(self)``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Angle_abs(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    @overload
    def __add__(self, rhs: Angle) -> Angle:
        pass

    @overload
    def __add__(self, rhs: AngleRange) -> AngleRange:
        pass

    @overload
    def __add__(self, rhs: AngleCurve) -> AngleCurve:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_add_Angle_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Angle._new(output)
            case AngleRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_add_Angle_AngleRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case AngleCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_add_Angle_AngleCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: Angle) -> Angle:
        pass

    @overload
    def __sub__(self, rhs: AngleRange) -> AngleRange:
        pass

    @overload
    def __sub__(self, rhs: AngleCurve) -> AngleCurve:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_sub_Angle_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Angle._new(output)
            case AngleRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_sub_Angle_AngleRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case AngleCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_sub_Angle_AngleCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> Angle:
        pass

    @overload
    def __mul__(self, rhs: Range) -> AngleRange:
        pass

    @overload
    def __mul__(self, rhs: Curve) -> AngleCurve:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Angle_mul_Angle_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Angle._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_mul_Angle_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_mul_Angle_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> Angle:
        pass

    @overload
    def __truediv__(self, rhs: Angle) -> float:
        pass

    @overload
    def __truediv__(self, rhs: Range) -> AngleRange:
        pass

    @overload
    def __truediv__(self, rhs: AngleRange) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Curve) -> AngleCurve:
        pass

    @overload
    def __truediv__(self, rhs: AngleCurve) -> Curve:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Angle_div_Angle_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Angle._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Angle_div_Angle_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_div_Angle_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case AngleRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_div_Angle_AngleRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_div_Angle_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case AngleCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Angle_div_Angle_AngleCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case _:
                return NotImplemented

    def __floordiv__(self, rhs: Angle) -> int:
        """Return ``self // rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_int64()
        _lib.opensolid_Angle_floorDiv_Angle_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def __mod__(self, rhs: Angle) -> Angle:
        """Return ``self % rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Angle_mod_Angle_Angle(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    def __rmul__(self, lhs: float) -> Angle:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Angle_mul_Float_Angle(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        return "Angle.degrees(" + str(self.in_degrees()) + ")"


def _angle_zero() -> Angle:
    output = c_void_p()
    _lib.opensolid_Angle_zero(c_void_p(), ctypes.byref(output))
    return Angle._new(output)


Angle.zero = _angle_zero()


def _angle_golden_angle() -> Angle:
    output = c_void_p()
    _lib.opensolid_Angle_goldenAngle(c_void_p(), ctypes.byref(output))
    return Angle._new(output)


Angle.golden_angle = _angle_golden_angle()


def _angle_radian() -> Angle:
    output = c_void_p()
    _lib.opensolid_Angle_radian(c_void_p(), ctypes.byref(output))
    return Angle._new(output)


Angle.radian = _angle_radian()


def _angle_full_turn() -> Angle:
    output = c_void_p()
    _lib.opensolid_Angle_fullTurn(c_void_p(), ctypes.byref(output))
    return Angle._new(output)


Angle.full_turn = _angle_full_turn()


def _angle_half_turn() -> Angle:
    output = c_void_p()
    _lib.opensolid_Angle_halfTurn(c_void_p(), ctypes.byref(output))
    return Angle._new(output)


Angle.half_turn = _angle_half_turn()


def _angle_quarter_turn() -> Angle:
    output = c_void_p()
    _lib.opensolid_Angle_quarterTurn(c_void_p(), ctypes.byref(output))
    return Angle._new(output)


Angle.quarter_turn = _angle_quarter_turn()


def _angle_pi() -> Angle:
    output = c_void_p()
    _lib.opensolid_Angle_pi(c_void_p(), ctypes.byref(output))
    return Angle._new(output)


Angle.pi = _angle_pi()


def _angle_two_pi() -> Angle:
    output = c_void_p()
    _lib.opensolid_Angle_twoPi(c_void_p(), ctypes.byref(output))
    return Angle._new(output)


Angle.two_pi = _angle_two_pi()


class Range:
    """A range of unitless values, with a lower bound and upper bound."""

    _ptr: c_void_p

    def __init__(self, first_value: float, second_value: float) -> None:
        """Construct a range from its lower and upper bounds.

        The order of the two arguments does not matter;
        the minimum of the two will be used as the lower bound of the range
        and the maximum will be used as the upper bound.

        If either argument is NaN,
        then the result will be an open/infinite range
        (with endpoints negative infinity and positive infinity).
        """
        inputs = _Tuple2_c_double_c_double(first_value, second_value)
        self._ptr = c_void_p()
        _lib.opensolid_Range_constructor_Float_Float(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> Range:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Range)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    unit: Range = None  # type: ignore[assignment]
    """The range with endoints [0,1]."""

    @staticmethod
    def constant(value: float) -> Range:
        """Construct a zero-width range containing a single value."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Range_constant_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    @staticmethod
    def zero_to(value: float) -> Range:
        """Create a range from zero to the given value."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Range_zeroTo_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    @staticmethod
    def symmetric(*, width: float) -> Range:
        """Create a range symmetric about zero, with the given width.

        The lower bound of the range will be -w/2 and the upper bound will be w/2.
        """
        inputs = c_double(width)
        output = c_void_p()
        _lib.opensolid_Range_symmetric_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    @staticmethod
    def hull(values: list[float]) -> Range:
        """Build a range containing all values in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_double,
                (c_double * len(values))(*[c_double(item) for item in values]),
            )
            if values
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_Range_hull_NonEmptyFloat(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Range._new(output)

    @staticmethod
    def aggregate(ranges: list[Range]) -> Range:
        """Build a range containing all ranges in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(ranges))(*[item._ptr for item in ranges]),
            )
            if ranges
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_Range_aggregate_NonEmptyRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Range._new(output)

    def endpoints(self) -> tuple[float, float]:
        """Get the lower and upper bounds of a range."""
        inputs = self._ptr
        output = _Tuple2_c_double_c_double()
        _lib.opensolid_Range_endpoints(ctypes.byref(inputs), ctypes.byref(output))
        return (output.field0, output.field1)

    def lower_bound(self) -> float:
        """Get the lower bound of a range."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Range_lowerBound(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def upper_bound(self) -> float:
        """Get the upper bound of a range."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Range_upperBound(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def intersection(self, other: Range) -> Range | None:
        """Attempt to find the intersection of two ranges."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = _Maybe_c_void_p()
        _lib.opensolid_Range_intersection_Range(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Range._new(c_void_p(output.field1)) if output.field0 == 0 else None

    def includes(self, value: float) -> bool:
        """Check if a given value is included in a range.

        Note that this does *not* use a tolerance, so use with care -
        for example, a value *just* outside the range (due to numerical roundoff)
        will be reported as not included.
        """
        inputs = _Tuple2_c_double_c_void_p(value, self._ptr)
        output = c_int64()
        _lib.opensolid_Range_includes_Float(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def contains(self, other: Range) -> bool:
        """Check if one range contains another.

        Note that this does *not* use a tolerance, so use with care -
        for example, a range that extends *just* outside another range (due to numerical
        roundoff) will be reported as not contained by that range.
        """
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_Range_contains_Range(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __neg__(self) -> Range:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Range_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    def __abs__(self) -> Range:
        """Return ``abs(self)``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Range_abs(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    @overload
    def __add__(self, rhs: float) -> Range:
        pass

    @overload
    def __add__(self, rhs: Range) -> Range:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Range_add_Range_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_add_Range_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: float) -> Range:
        pass

    @overload
    def __sub__(self, rhs: Range) -> Range:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Range_sub_Range_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_sub_Range_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> Range:
        pass

    @overload
    def __mul__(self, rhs: Range) -> Range:
        pass

    @overload
    def __mul__(self, rhs: Length) -> LengthRange:
        pass

    @overload
    def __mul__(self, rhs: Area) -> AreaRange:
        pass

    @overload
    def __mul__(self, rhs: Angle) -> AngleRange:
        pass

    @overload
    def __mul__(self, rhs: LengthRange) -> LengthRange:
        pass

    @overload
    def __mul__(self, rhs: AreaRange) -> AreaRange:
        pass

    @overload
    def __mul__(self, rhs: AngleRange) -> AngleRange:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Range_mul_Range_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_mul_Range_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_mul_Range_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_mul_Range_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_mul_Range_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_mul_Range_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case AreaRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_mul_Range_AreaRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case AngleRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_mul_Range_AngleRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Range) -> Range:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Range_div_Range_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Range_div_Range_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case _:
                return NotImplemented

    def __radd__(self, lhs: float) -> Range:
        """Return ``lhs <> self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Range_add_Float_Range(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    def __rsub__(self, lhs: float) -> Range:
        """Return ``lhs - self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Range_sub_Float_Range(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    def __rmul__(self, lhs: float) -> Range:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Range_mul_Float_Range(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    def __rtruediv__(self, lhs: float) -> Range:
        """Return ``lhs / self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Range_div_Float_Range(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        low, high = self.endpoints()
        return "Range(" + str(low) + "," + str(high) + ")"


def _range_unit() -> Range:
    output = c_void_p()
    _lib.opensolid_Range_unit(c_void_p(), ctypes.byref(output))
    return Range._new(output)


Range.unit = _range_unit()


class LengthRange:
    """A range of length values, with a lower bound and upper bound."""

    _ptr: c_void_p

    def __init__(self, first_value: Length, second_value: Length) -> None:
        """Construct a range from its lower and upper bounds.

        The order of the two arguments does not matter;
        the minimum of the two will be used as the lower bound of the range
        and the maximum will be used as the upper bound.

        If either argument is NaN,
        then the result will be an open/infinite range
        (with endpoints negative infinity and positive infinity).
        """
        inputs = _Tuple2_c_void_p_c_void_p(first_value._ptr, second_value._ptr)
        self._ptr = c_void_p()
        _lib.opensolid_LengthRange_constructor_Length_Length(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> LengthRange:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(LengthRange)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def constant(value: Length) -> LengthRange:
        """Construct a zero-width range containing a single value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_LengthRange_constant_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    @staticmethod
    def zero_to(value: Length) -> LengthRange:
        """Create a range from zero to the given value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_LengthRange_zeroTo_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    @staticmethod
    def symmetric(*, width: Length) -> LengthRange:
        """Create a range symmetric about zero, with the given width.

        The lower bound of the range will be -w/2 and the upper bound will be w/2.
        """
        inputs = width._ptr
        output = c_void_p()
        _lib.opensolid_LengthRange_symmetric_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    @staticmethod
    def meters(a: float, b: float) -> LengthRange:
        """Construct a length range from lower and upper bounds given in meters."""
        inputs = _Tuple2_c_double_c_double(a, b)
        output = c_void_p()
        _lib.opensolid_LengthRange_meters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    @staticmethod
    def centimeters(a: float, b: float) -> LengthRange:
        """Construct a length range from lower and upper bounds given in centimeters."""
        inputs = _Tuple2_c_double_c_double(a, b)
        output = c_void_p()
        _lib.opensolid_LengthRange_centimeters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    @staticmethod
    def millimeters(a: float, b: float) -> LengthRange:
        """Construct a length range from lower and upper bounds given in millimeters."""
        inputs = _Tuple2_c_double_c_double(a, b)
        output = c_void_p()
        _lib.opensolid_LengthRange_millimeters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    @staticmethod
    def inches(a: float, b: float) -> LengthRange:
        """Construct a length range from lower and upper bounds given in inches."""
        inputs = _Tuple2_c_double_c_double(a, b)
        output = c_void_p()
        _lib.opensolid_LengthRange_inches_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    @staticmethod
    def hull(values: list[Length]) -> LengthRange:
        """Build a range containing all values in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(values))(*[item._ptr for item in values]),
            )
            if values
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_LengthRange_hull_NonEmptyLength(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    @staticmethod
    def aggregate(ranges: list[LengthRange]) -> LengthRange:
        """Build a range containing all ranges in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(ranges))(*[item._ptr for item in ranges]),
            )
            if ranges
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_LengthRange_aggregate_NonEmptyLengthRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    def endpoints(self) -> tuple[Length, Length]:
        """Get the lower and upper bounds of a range."""
        inputs = self._ptr
        output = _Tuple2_c_void_p_c_void_p()
        _lib.opensolid_LengthRange_endpoints(ctypes.byref(inputs), ctypes.byref(output))
        return (
            Length._new(c_void_p(output.field0)),
            Length._new(c_void_p(output.field1)),
        )

    def intersection(self, other: LengthRange) -> LengthRange | None:
        """Attempt to find the intersection of two ranges."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = _Maybe_c_void_p()
        _lib.opensolid_LengthRange_intersection_LengthRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(c_void_p(output.field1)) if output.field0 == 0 else None

    def includes(self, value: Length) -> bool:
        """Check if a given value is included in a range.

        Note that this does *not* use a tolerance, so use with care -
        for example, a value *just* outside the range (due to numerical roundoff)
        will be reported as not included.
        """
        inputs = _Tuple2_c_void_p_c_void_p(value._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_LengthRange_includes_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return bool(output.value)

    def contains(self, other: LengthRange) -> bool:
        """Check if one range contains another.

        Note that this does *not* use a tolerance, so use with care -
        for example, a range that extends *just* outside another range (due to numerical
        roundoff) will be reported as not contained by that range.
        """
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_LengthRange_contains_LengthRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return bool(output.value)

    def __neg__(self) -> LengthRange:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_LengthRange_neg(ctypes.byref(inputs), ctypes.byref(output))
        return LengthRange._new(output)

    def __abs__(self) -> LengthRange:
        """Return ``abs(self)``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_LengthRange_abs(ctypes.byref(inputs), ctypes.byref(output))
        return LengthRange._new(output)

    @overload
    def __add__(self, rhs: LengthRange) -> LengthRange:
        pass

    @overload
    def __add__(self, rhs: Length) -> LengthRange:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_add_LengthRange_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_add_LengthRange_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: LengthRange) -> LengthRange:
        pass

    @overload
    def __sub__(self, rhs: Length) -> LengthRange:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_sub_LengthRange_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_sub_LengthRange_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> LengthRange:
        pass

    @overload
    def __mul__(self, rhs: LengthRange) -> AreaRange:
        pass

    @overload
    def __mul__(self, rhs: Length) -> AreaRange:
        pass

    @overload
    def __mul__(self, rhs: Range) -> LengthRange:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_LengthRange_mul_LengthRange_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_mul_LengthRange_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_mul_LengthRange_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_mul_LengthRange_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> LengthRange:
        pass

    @overload
    def __truediv__(self, rhs: LengthRange) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Range) -> LengthRange:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_LengthRange_div_LengthRange_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_div_LengthRange_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_div_LengthRange_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthRange_div_LengthRange_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> LengthRange:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_LengthRange_mul_Float_LengthRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthRange._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        low, high = self.endpoints()
        return (
            "LengthRange.meters("
            + str(low.in_meters())
            + ","
            + str(high.in_meters())
            + ")"
        )


class AreaRange:
    """A range of area values, with a lower bound and upper bound."""

    _ptr: c_void_p

    def __init__(self, first_value: Area, second_value: Area) -> None:
        """Construct a range from its lower and upper bounds.

        The order of the two arguments does not matter;
        the minimum of the two will be used as the lower bound of the range
        and the maximum will be used as the upper bound.

        If either argument is NaN,
        then the result will be an open/infinite range
        (with endpoints negative infinity and positive infinity).
        """
        inputs = _Tuple2_c_void_p_c_void_p(first_value._ptr, second_value._ptr)
        self._ptr = c_void_p()
        _lib.opensolid_AreaRange_constructor_Area_Area(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> AreaRange:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(AreaRange)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def constant(value: Area) -> AreaRange:
        """Construct a zero-width range containing a single value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_AreaRange_constant_Area(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaRange._new(output)

    @staticmethod
    def square_meters(a: float, b: float) -> AreaRange:
        """Construct an area range from lower and upper bounds given in square meters."""
        inputs = _Tuple2_c_double_c_double(a, b)
        output = c_void_p()
        _lib.opensolid_AreaRange_squareMeters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaRange._new(output)

    @staticmethod
    def zero_to(value: Area) -> AreaRange:
        """Create a range from zero to the given value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_AreaRange_zeroTo_Area(ctypes.byref(inputs), ctypes.byref(output))
        return AreaRange._new(output)

    @staticmethod
    def symmetric(*, width: Area) -> AreaRange:
        """Create a range symmetric about zero, with the given width.

        The lower bound of the range will be -w/2 and the upper bound will be w/2.
        """
        inputs = width._ptr
        output = c_void_p()
        _lib.opensolid_AreaRange_symmetric_Area(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaRange._new(output)

    @staticmethod
    def hull(values: list[Area]) -> AreaRange:
        """Build a range containing all values in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(values))(*[item._ptr for item in values]),
            )
            if values
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_AreaRange_hull_NonEmptyArea(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaRange._new(output)

    @staticmethod
    def aggregate(ranges: list[AreaRange]) -> AreaRange:
        """Build a range containing all ranges in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(ranges))(*[item._ptr for item in ranges]),
            )
            if ranges
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_AreaRange_aggregate_NonEmptyAreaRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaRange._new(output)

    def endpoints(self) -> tuple[Area, Area]:
        """Get the lower and upper bounds of a range."""
        inputs = self._ptr
        output = _Tuple2_c_void_p_c_void_p()
        _lib.opensolid_AreaRange_endpoints(ctypes.byref(inputs), ctypes.byref(output))
        return (Area._new(c_void_p(output.field0)), Area._new(c_void_p(output.field1)))

    def intersection(self, other: AreaRange) -> AreaRange | None:
        """Attempt to find the intersection of two ranges."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = _Maybe_c_void_p()
        _lib.opensolid_AreaRange_intersection_AreaRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaRange._new(c_void_p(output.field1)) if output.field0 == 0 else None

    def includes(self, value: Area) -> bool:
        """Check if a given value is included in a range.

        Note that this does *not* use a tolerance, so use with care -
        for example, a value *just* outside the range (due to numerical roundoff)
        will be reported as not included.
        """
        inputs = _Tuple2_c_void_p_c_void_p(value._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_AreaRange_includes_Area(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return bool(output.value)

    def contains(self, other: AreaRange) -> bool:
        """Check if one range contains another.

        Note that this does *not* use a tolerance, so use with care -
        for example, a range that extends *just* outside another range (due to numerical
        roundoff) will be reported as not contained by that range.
        """
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_AreaRange_contains_AreaRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return bool(output.value)

    def __neg__(self) -> AreaRange:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaRange_neg(ctypes.byref(inputs), ctypes.byref(output))
        return AreaRange._new(output)

    def __abs__(self) -> AreaRange:
        """Return ``abs(self)``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaRange_abs(ctypes.byref(inputs), ctypes.byref(output))
        return AreaRange._new(output)

    @overload
    def __add__(self, rhs: AreaRange) -> AreaRange:
        pass

    @overload
    def __add__(self, rhs: Area) -> AreaRange:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case AreaRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_add_AreaRange_AreaRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_add_AreaRange_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: AreaRange) -> AreaRange:
        pass

    @overload
    def __sub__(self, rhs: Area) -> AreaRange:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case AreaRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_sub_AreaRange_AreaRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_sub_AreaRange_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> AreaRange:
        pass

    @overload
    def __mul__(self, rhs: Range) -> AreaRange:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AreaRange_mul_AreaRange_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_mul_AreaRange_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> AreaRange:
        pass

    @overload
    def __truediv__(self, rhs: AreaRange) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> LengthRange:
        pass

    @overload
    def __truediv__(self, rhs: Area) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Range) -> AreaRange:
        pass

    @overload
    def __truediv__(self, rhs: LengthRange) -> LengthRange:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AreaRange_div_AreaRange_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case AreaRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_div_AreaRange_AreaRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_div_AreaRange_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_div_AreaRange_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_div_AreaRange_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaRange._new(output)
            case LengthRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaRange_div_AreaRange_LengthRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthRange._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> AreaRange:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaRange_mul_Float_AreaRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaRange._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        low, high = self.endpoints()
        return (
            "AreaRange.square_meters("
            + str(low.in_square_meters())
            + ","
            + str(high.in_square_meters())
            + ")"
        )


class AngleRange:
    """A range of angle values, with a lower bound and upper bound."""

    _ptr: c_void_p

    def __init__(self, first_value: Angle, second_value: Angle) -> None:
        """Construct a range from its lower and upper bounds.

        The order of the two arguments does not matter;
        the minimum of the two will be used as the lower bound of the range
        and the maximum will be used as the upper bound.

        If either argument is NaN,
        then the result will be an open/infinite range
        (with endpoints negative infinity and positive infinity).
        """
        inputs = _Tuple2_c_void_p_c_void_p(first_value._ptr, second_value._ptr)
        self._ptr = c_void_p()
        _lib.opensolid_AngleRange_constructor_Angle_Angle(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> AngleRange:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(AngleRange)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def constant(value: Angle) -> AngleRange:
        """Construct a zero-width range containing a single value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_AngleRange_constant_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    @staticmethod
    def zero_to(value: Angle) -> AngleRange:
        """Create a range from zero to the given value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_AngleRange_zeroTo_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    @staticmethod
    def symmetric(*, width: Angle) -> AngleRange:
        """Create a range symmetric about zero, with the given width.

        The lower bound of the range will be -w/2 and the upper bound will be w/2.
        """
        inputs = width._ptr
        output = c_void_p()
        _lib.opensolid_AngleRange_symmetric_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    @staticmethod
    def radians(a: float, b: float) -> AngleRange:
        """Construct an angle range from lower and upper bounds given in radians."""
        inputs = _Tuple2_c_double_c_double(a, b)
        output = c_void_p()
        _lib.opensolid_AngleRange_radians_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    @staticmethod
    def degrees(a: float, b: float) -> AngleRange:
        """Construct an angle range from lower and upper bounds given in degrees."""
        inputs = _Tuple2_c_double_c_double(a, b)
        output = c_void_p()
        _lib.opensolid_AngleRange_degrees_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    @staticmethod
    def turns(a: float, b: float) -> AngleRange:
        """Construct an angle range from lower and upper bounds given in turns."""
        inputs = _Tuple2_c_double_c_double(a, b)
        output = c_void_p()
        _lib.opensolid_AngleRange_turns_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    @staticmethod
    def hull(values: list[Angle]) -> AngleRange:
        """Build a range containing all values in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(values))(*[item._ptr for item in values]),
            )
            if values
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_AngleRange_hull_NonEmptyAngle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    @staticmethod
    def aggregate(ranges: list[AngleRange]) -> AngleRange:
        """Build a range containing all ranges in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(ranges))(*[item._ptr for item in ranges]),
            )
            if ranges
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_AngleRange_aggregate_NonEmptyAngleRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    def endpoints(self) -> tuple[Angle, Angle]:
        """Get the lower and upper bounds of a range."""
        inputs = self._ptr
        output = _Tuple2_c_void_p_c_void_p()
        _lib.opensolid_AngleRange_endpoints(ctypes.byref(inputs), ctypes.byref(output))
        return (
            Angle._new(c_void_p(output.field0)),
            Angle._new(c_void_p(output.field1)),
        )

    def intersection(self, other: AngleRange) -> AngleRange | None:
        """Attempt to find the intersection of two ranges."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = _Maybe_c_void_p()
        _lib.opensolid_AngleRange_intersection_AngleRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(c_void_p(output.field1)) if output.field0 == 0 else None

    def includes(self, value: Angle) -> bool:
        """Check if a given value is included in a range.

        Note that this does *not* use a tolerance, so use with care -
        for example, a value *just* outside the range (due to numerical roundoff)
        will be reported as not included.
        """
        inputs = _Tuple2_c_void_p_c_void_p(value._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_AngleRange_includes_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return bool(output.value)

    def contains(self, other: AngleRange) -> bool:
        """Check if one range contains another.

        Note that this does *not* use a tolerance, so use with care -
        for example, a range that extends *just* outside another range (due to numerical
        roundoff) will be reported as not contained by that range.
        """
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_AngleRange_contains_AngleRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return bool(output.value)

    def __neg__(self) -> AngleRange:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AngleRange_neg(ctypes.byref(inputs), ctypes.byref(output))
        return AngleRange._new(output)

    def __abs__(self) -> AngleRange:
        """Return ``abs(self)``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AngleRange_abs(ctypes.byref(inputs), ctypes.byref(output))
        return AngleRange._new(output)

    @overload
    def __add__(self, rhs: AngleRange) -> AngleRange:
        pass

    @overload
    def __add__(self, rhs: Angle) -> AngleRange:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case AngleRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleRange_add_AngleRange_AngleRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleRange_add_AngleRange_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: AngleRange) -> AngleRange:
        pass

    @overload
    def __sub__(self, rhs: Angle) -> AngleRange:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case AngleRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleRange_sub_AngleRange_AngleRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleRange_sub_AngleRange_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> AngleRange:
        pass

    @overload
    def __mul__(self, rhs: Range) -> AngleRange:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AngleRange_mul_AngleRange_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleRange_mul_AngleRange_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> AngleRange:
        pass

    @overload
    def __truediv__(self, rhs: AngleRange) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Angle) -> Range:
        pass

    @overload
    def __truediv__(self, rhs: Range) -> AngleRange:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AngleRange_div_AngleRange_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case AngleRange():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleRange_div_AngleRange_AngleRange(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleRange_div_AngleRange_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Range._new(output)
            case Range():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleRange_div_AngleRange_Range(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleRange._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> AngleRange:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_AngleRange_mul_Float_AngleRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleRange._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        low, high = self.endpoints()
        return (
            "AngleRange.degrees("
            + str(low.in_degrees())
            + ","
            + str(high.in_degrees())
            + ")"
        )


class Color:
    """An RGB color value."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Color:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Color)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    red: Color = None  # type: ignore[assignment]
    """Scarlet Red from the Tango icon theme."""

    dark_red: Color = None  # type: ignore[assignment]
    """Dark Scarlet Red from the Tango icon theme."""

    light_orange: Color = None  # type: ignore[assignment]
    """Light Orange from the Tango icon theme."""

    orange: Color = None  # type: ignore[assignment]
    """Orange from the Tango icon theme."""

    dark_orange: Color = None  # type: ignore[assignment]
    """Dark Orange from the Tango icon theme."""

    light_yellow: Color = None  # type: ignore[assignment]
    """Light Butter from the Tango icon theme."""

    yellow: Color = None  # type: ignore[assignment]
    """Butter from the Tango icon theme."""

    dark_yellow: Color = None  # type: ignore[assignment]
    """Dark Butter from the Tango icon theme."""

    light_green: Color = None  # type: ignore[assignment]
    """Light Chameleon from the Tango icon theme."""

    green: Color = None  # type: ignore[assignment]
    """Chameleon from the Tango icon theme."""

    dark_green: Color = None  # type: ignore[assignment]
    """Dark Chameleon from the Tango icon theme."""

    light_blue: Color = None  # type: ignore[assignment]
    """Light Sky Blue from the Tango icon theme."""

    blue: Color = None  # type: ignore[assignment]
    """Sky Blue from the Tango icon theme."""

    dark_blue: Color = None  # type: ignore[assignment]
    """Dark Sky Blue from the Tango icon theme."""

    light_purple: Color = None  # type: ignore[assignment]
    """Light Plum from the Tango icon theme."""

    purple: Color = None  # type: ignore[assignment]
    """Plum from the Tango icon theme."""

    dark_purple: Color = None  # type: ignore[assignment]
    """Dark Plum from the Tango icon theme."""

    light_brown: Color = None  # type: ignore[assignment]
    """Light Chocolate from the Tango icon theme."""

    brown: Color = None  # type: ignore[assignment]
    """Chocolate from the Tango icon theme."""

    dark_brown: Color = None  # type: ignore[assignment]
    """Dark Chocolate from the Tango icon theme."""

    black: Color = None  # type: ignore[assignment]
    """Black."""

    white: Color = None  # type: ignore[assignment]
    """White."""

    light_grey: Color = None  # type: ignore[assignment]
    """Aluminium 1/6 from the Tango icon theme."""

    grey: Color = None  # type: ignore[assignment]
    """Aluminium 2/6 from the Tango icon theme."""

    dark_grey: Color = None  # type: ignore[assignment]
    """Aluminium 3/6 from the Tango icon theme."""

    light_gray: Color = None  # type: ignore[assignment]
    """Aluminium 1/6 from the Tango icon theme."""

    gray: Color = None  # type: ignore[assignment]
    """Aluminium 2/6 from the Tango icon theme."""

    dark_gray: Color = None  # type: ignore[assignment]
    """Aluminium 3/6 from the Tango icon theme."""

    light_charcoal: Color = None  # type: ignore[assignment]
    """Aluminium 4/6 from the Tango icon theme."""

    charcoal: Color = None  # type: ignore[assignment]
    """Aluminium 5/6 from the Tango icon theme."""

    dark_charcoal: Color = None  # type: ignore[assignment]
    """Aluminium 6/6 from the Tango icon theme."""

    @staticmethod
    def rgb(red: float, green: float, blue: float) -> Color:
        """Construct a color from its RGB components, in the range [0,1]."""
        inputs = _Tuple3_c_double_c_double_c_double(red, green, blue)
        output = c_void_p()
        _lib.opensolid_Color_rgb_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Color._new(output)

    @staticmethod
    def rgb_255(red: int, green: int, blue: int) -> Color:
        """Construct a color from its RGB components, in the range [0,255]."""
        inputs = _Tuple3_c_int64_c_int64_c_int64(red, green, blue)
        output = c_void_p()
        _lib.opensolid_Color_rgb255_Int_Int_Int(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Color._new(output)

    @staticmethod
    def hsl(hue: Angle, saturation: float, lightness: float) -> Color:
        """Construct a color from its hue, saturation and lightness values."""
        inputs = _Tuple3_c_void_p_c_double_c_double(hue._ptr, saturation, lightness)
        output = c_void_p()
        _lib.opensolid_Color_hsl_Angle_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Color._new(output)

    @staticmethod
    def from_hex(hex_string: str) -> Color:
        """Construct a color from a hex string such as '#f3f3f3' or 'f3f3f3'."""
        inputs = _str_to_text(hex_string)
        output = c_void_p()
        _lib.opensolid_Color_fromHex_Text(ctypes.byref(inputs), ctypes.byref(output))
        return Color._new(output)

    def to_hex(self) -> str:
        """Convert a color to a hex string such as '#f3f3f3'."""
        inputs = self._ptr
        output = _Text()
        _lib.opensolid_Color_toHex(ctypes.byref(inputs), ctypes.byref(output))
        return _text_to_str(output)

    def components(self) -> tuple[float, float, float]:
        """Get the RGB components of a color as values in the range [0,1]."""
        inputs = self._ptr
        output = _Tuple3_c_double_c_double_c_double()
        _lib.opensolid_Color_components(ctypes.byref(inputs), ctypes.byref(output))
        return (output.field0, output.field1, output.field2)

    def components_255(self) -> tuple[int, int, int]:
        """Get the RGB components of a color as values in the range [0,255]."""
        inputs = self._ptr
        output = _Tuple3_c_int64_c_int64_c_int64()
        _lib.opensolid_Color_components255(ctypes.byref(inputs), ctypes.byref(output))
        return (output.field0, output.field1, output.field2)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        r, g, b = self.components_255()
        return "Color.rgb_255(" + str(r) + "," + str(g) + "," + str(b) + ")"


def _color_red() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_red(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.red = _color_red()


def _color_dark_red() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkRed(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_red = _color_dark_red()


def _color_light_orange() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightOrange(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_orange = _color_light_orange()


def _color_orange() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_orange(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.orange = _color_orange()


def _color_dark_orange() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkOrange(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_orange = _color_dark_orange()


def _color_light_yellow() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightYellow(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_yellow = _color_light_yellow()


def _color_yellow() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_yellow(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.yellow = _color_yellow()


def _color_dark_yellow() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkYellow(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_yellow = _color_dark_yellow()


def _color_light_green() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightGreen(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_green = _color_light_green()


def _color_green() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_green(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.green = _color_green()


def _color_dark_green() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkGreen(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_green = _color_dark_green()


def _color_light_blue() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightBlue(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_blue = _color_light_blue()


def _color_blue() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_blue(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.blue = _color_blue()


def _color_dark_blue() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkBlue(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_blue = _color_dark_blue()


def _color_light_purple() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightPurple(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_purple = _color_light_purple()


def _color_purple() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_purple(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.purple = _color_purple()


def _color_dark_purple() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkPurple(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_purple = _color_dark_purple()


def _color_light_brown() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightBrown(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_brown = _color_light_brown()


def _color_brown() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_brown(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.brown = _color_brown()


def _color_dark_brown() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkBrown(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_brown = _color_dark_brown()


def _color_black() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_black(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.black = _color_black()


def _color_white() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_white(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.white = _color_white()


def _color_light_grey() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightGrey(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_grey = _color_light_grey()


def _color_grey() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_grey(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.grey = _color_grey()


def _color_dark_grey() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkGrey(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_grey = _color_dark_grey()


def _color_light_gray() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightGray(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_gray = _color_light_gray()


def _color_gray() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_gray(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.gray = _color_gray()


def _color_dark_gray() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkGray(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_gray = _color_dark_gray()


def _color_light_charcoal() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_lightCharcoal(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.light_charcoal = _color_light_charcoal()


def _color_charcoal() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_charcoal(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.charcoal = _color_charcoal()


def _color_dark_charcoal() -> Color:
    output = c_void_p()
    _lib.opensolid_Color_darkCharcoal(c_void_p(), ctypes.byref(output))
    return Color._new(output)


Color.dark_charcoal = _color_dark_charcoal()


class Vector2d:
    """A unitless vector in 2D."""

    _ptr: c_void_p

    def __init__(self, x_component: float, y_component: float) -> None:
        """Construct a vector from its X and Y components."""
        inputs = _Tuple2_c_double_c_double(x_component, y_component)
        self._ptr = c_void_p()
        _lib.opensolid_Vector2d_constructor_Float_Float(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> Vector2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Vector2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: Vector2d = None  # type: ignore[assignment]
    """The zero vector."""

    @staticmethod
    def unit(direction: Direction2d) -> Vector2d:
        """Construct a unit vector in the given direction."""
        inputs = direction._ptr
        output = c_void_p()
        _lib.opensolid_Vector2d_unit_Direction2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    @staticmethod
    def xy(x_component: float, y_component: float) -> Vector2d:
        """Construct a vector from its X and Y components."""
        inputs = _Tuple2_c_double_c_double(x_component, y_component)
        output = c_void_p()
        _lib.opensolid_Vector2d_xy_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    @staticmethod
    def y(y_component: float) -> Vector2d:
        """Construct a vector from just a Y component.

        The X component will be set to zero.
        """
        inputs = c_double(y_component)
        output = c_void_p()
        _lib.opensolid_Vector2d_y_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Vector2d._new(output)

    @staticmethod
    def x(x_component: float) -> Vector2d:
        """Construct a vector from just an X component.

        The Y component will be set to zero.
        """
        inputs = c_double(x_component)
        output = c_void_p()
        _lib.opensolid_Vector2d_x_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Vector2d._new(output)

    @staticmethod
    def polar(magnitude: float, angle: Angle) -> Vector2d:
        """Construct a vector from its magnitude (length) and angle."""
        inputs = _Tuple2_c_double_c_void_p(magnitude, angle._ptr)
        output = c_void_p()
        _lib.opensolid_Vector2d_polar_Float_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    @staticmethod
    def from_components(components: tuple[float, float]) -> Vector2d:
        """Construct a vector from a pair of X and Y components."""
        inputs = _Tuple2_c_double_c_double(components[0], components[1])
        output = c_void_p()
        _lib.opensolid_Vector2d_fromComponents_Tuple2FloatFloat(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    def components(self) -> tuple[float, float]:
        """Get the X and Y components of a vector as a tuple."""
        inputs = self._ptr
        output = _Tuple2_c_double_c_double()
        _lib.opensolid_Vector2d_components(ctypes.byref(inputs), ctypes.byref(output))
        return (output.field0, output.field1)

    def x_component(self) -> float:
        """Get the X component of a vector."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Vector2d_xComponent(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def y_component(self) -> float:
        """Get the Y component of a vector."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Vector2d_yComponent(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def direction(self) -> Direction2d:
        """Attempt to get the direction of a vector.

        The current tolerance will be used to check if the vector is zero
        (and therefore does not have a direction).
        """
        inputs = _Tuple2_c_double_c_void_p(_float_tolerance(), self._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_Vector2d_direction(ctypes.byref(inputs), ctypes.byref(output))
        return (
            Direction2d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def normalize(self) -> Vector2d:
        """Normalize a vector.

        If the original vector is exactly zero, then the result will be zero as well.
        Otherwise, the result will be a unit vector.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Vector2d_normalize(ctypes.byref(inputs), ctypes.byref(output))
        return Vector2d._new(output)

    def angle(self) -> Angle:
        """Get the angle of a vector.

        The angle is measured counterclockwise from the positive X axis, so:

          * A vector in the positive X direction has an angle of zero.
          * A vector in the positive Y direction has an angle of 90 degrees.
          * A vector in the negative Y direction has an angle of -90 degrees.
          * It is not defined whether a vector exactly in the negative X direction has
            an angle of -180 or +180 degrees. (Currently it is reported as having an
            angle of +180 degrees, but this should not be relied upon.)

        The returned angle will be between -180 and +180 degrees.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Vector2d_angle(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    def is_zero(self) -> bool:
        """Check if a vector is zero, within the current tolerance."""
        inputs = _Tuple2_c_double_c_void_p(_float_tolerance(), self._ptr)
        output = c_int64()
        _lib.opensolid_Vector2d_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __neg__(self) -> Vector2d:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Vector2d_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Vector2d._new(output)

    def __add__(self, rhs: Vector2d) -> Vector2d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Vector2d_add_Vector2d_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    def __sub__(self, rhs: Vector2d) -> Vector2d:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Vector2d_sub_Vector2d_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    @overload
    def __mul__(self, rhs: float) -> Vector2d:
        pass

    @overload
    def __mul__(self, rhs: Length) -> Displacement2d:
        pass

    @overload
    def __mul__(self, rhs: Area) -> AreaVector2d:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Vector2d_mul_Vector2d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector2d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector2d_mul_Vector2d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement2d._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector2d_mul_Vector2d_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector2d._new(output)
            case _:
                return NotImplemented

    def __truediv__(self, rhs: float) -> Vector2d:
        """Return ``self / rhs``."""
        inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
        output = c_void_p()
        _lib.opensolid_Vector2d_div_Vector2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    @overload
    def dot(self, rhs: Vector2d) -> float:
        pass

    @overload
    def dot(self, rhs: Displacement2d) -> Length:
        pass

    @overload
    def dot(self, rhs: AreaVector2d) -> Area:
        pass

    @overload
    def dot(self, rhs: Direction2d) -> float:
        pass

    def dot(self, rhs):
        """Compute the dot product of two vector-like values."""
        match rhs:
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Vector2d_dot_Vector2d_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Displacement2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector2d_dot_Vector2d_Displacement2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case AreaVector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector2d_dot_Vector2d_AreaVector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Vector2d_dot_Vector2d_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case _:
                return NotImplemented

    @overload
    def cross(self, rhs: Vector2d) -> float:
        pass

    @overload
    def cross(self, rhs: Displacement2d) -> Length:
        pass

    @overload
    def cross(self, rhs: AreaVector2d) -> Area:
        pass

    @overload
    def cross(self, rhs: Direction2d) -> float:
        pass

    def cross(self, rhs):
        """Compute the cross product of two vector-like values."""
        match rhs:
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Vector2d_cross_Vector2d_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Displacement2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector2d_cross_Vector2d_Displacement2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case AreaVector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector2d_cross_Vector2d_AreaVector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Vector2d_cross_Vector2d_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> Vector2d:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Vector2d_mul_Float_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        x, y = self.components()
        return "Vector2d.xy(" + str(x) + "," + str(y) + ")"


def _vector2d_zero() -> Vector2d:
    output = c_void_p()
    _lib.opensolid_Vector2d_zero(c_void_p(), ctypes.byref(output))
    return Vector2d._new(output)


Vector2d.zero = _vector2d_zero()


class Displacement2d:
    """A displacement vector in 2D."""

    _ptr: c_void_p

    def __init__(self, x_component: Length, y_component: Length) -> None:
        """Construct a vector from its X and Y components."""
        inputs = _Tuple2_c_void_p_c_void_p(x_component._ptr, y_component._ptr)
        self._ptr = c_void_p()
        _lib.opensolid_Displacement2d_constructor_Length_Length(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> Displacement2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Displacement2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: Displacement2d = None  # type: ignore[assignment]
    """The zero vector."""

    @staticmethod
    def xy(x_component: Length, y_component: Length) -> Displacement2d:
        """Construct a vector from its X and Y components."""
        inputs = _Tuple2_c_void_p_c_void_p(x_component._ptr, y_component._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement2d_xy_Length_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @staticmethod
    def x(x_component: Length) -> Displacement2d:
        """Construct a vector from just an X component.

        The Y component will be set to zero.
        """
        inputs = x_component._ptr
        output = c_void_p()
        _lib.opensolid_Displacement2d_x_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @staticmethod
    def y(y_component: Length) -> Displacement2d:
        """Construct a vector from just a Y component.

        The X component will be set to zero.
        """
        inputs = y_component._ptr
        output = c_void_p()
        _lib.opensolid_Displacement2d_y_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @staticmethod
    def polar(magnitude: Length, angle: Angle) -> Displacement2d:
        """Construct a vector from its magnitude (length) and angle."""
        inputs = _Tuple2_c_void_p_c_void_p(magnitude._ptr, angle._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement2d_polar_Length_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @staticmethod
    def meters(x_component: float, y_component: float) -> Displacement2d:
        """Construct a vector from its X and Y components given in meters."""
        inputs = _Tuple2_c_double_c_double(x_component, y_component)
        output = c_void_p()
        _lib.opensolid_Displacement2d_meters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @staticmethod
    def centimeters(x_component: float, y_component: float) -> Displacement2d:
        """Construct a vector from its X and Y components given in centimeters."""
        inputs = _Tuple2_c_double_c_double(x_component, y_component)
        output = c_void_p()
        _lib.opensolid_Displacement2d_centimeters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @staticmethod
    def millimeters(x_component: float, y_component: float) -> Displacement2d:
        """Construct a vector from its X and Y components given in millimeters."""
        inputs = _Tuple2_c_double_c_double(x_component, y_component)
        output = c_void_p()
        _lib.opensolid_Displacement2d_millimeters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @staticmethod
    def inches(x_component: float, y_component: float) -> Displacement2d:
        """Construct a vector from its X and Y components given in inches."""
        inputs = _Tuple2_c_double_c_double(x_component, y_component)
        output = c_void_p()
        _lib.opensolid_Displacement2d_inches_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @staticmethod
    def from_components(components: tuple[Length, Length]) -> Displacement2d:
        """Construct a vector from a pair of X and Y components."""
        inputs = _Tuple2_c_void_p_c_void_p(components[0]._ptr, components[1]._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement2d_fromComponents_Tuple2LengthLength(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    def components(self) -> tuple[Length, Length]:
        """Get the X and Y components of a vector as a tuple."""
        inputs = self._ptr
        output = _Tuple2_c_void_p_c_void_p()
        _lib.opensolid_Displacement2d_components(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Length._new(c_void_p(output.field0)),
            Length._new(c_void_p(output.field1)),
        )

    def x_component(self) -> Length:
        """Get the X component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement2d_xComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def y_component(self) -> Length:
        """Get the Y component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement2d_yComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def direction(self) -> Direction2d:
        """Attempt to get the direction of a vector.

        The current tolerance will be used to check if the vector is zero
        (and therefore does not have a direction).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_Displacement2d_direction(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Direction2d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def normalize(self) -> Vector2d:
        """Normalize a vector.

        If the original vector is exactly zero, then the result will be zero as well.
        Otherwise, the result will be a unit vector.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement2d_normalize(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    def angle(self) -> Angle:
        """Get the angle of a vector.

        The angle is measured counterclockwise from the positive X axis, so:

          * A vector in the positive X direction has an angle of zero.
          * A vector in the positive Y direction has an angle of 90 degrees.
          * A vector in the negative Y direction has an angle of -90 degrees.
          * It is not defined whether a vector exactly in the negative X direction has
            an angle of -180 or +180 degrees. (Currently it is reported as having an
            angle of +180 degrees, but this should not be relied upon.)

        The returned angle will be between -180 and +180 degrees.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement2d_angle(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    def is_zero(self) -> bool:
        """Check if a displacement is zero, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_Displacement2d_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __neg__(self) -> Displacement2d:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement2d_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Displacement2d._new(output)

    def __add__(self, rhs: Displacement2d) -> Displacement2d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement2d_add_Displacement2d_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    def __sub__(self, rhs: Displacement2d) -> Displacement2d:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement2d_sub_Displacement2d_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    @overload
    def __mul__(self, rhs: float) -> Displacement2d:
        pass

    @overload
    def __mul__(self, rhs: Length) -> AreaVector2d:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Displacement2d_mul_Displacement2d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement2d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement2d_mul_Displacement2d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector2d._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> Displacement2d:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> Vector2d:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Displacement2d_div_Displacement2d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement2d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement2d_div_Displacement2d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector2d._new(output)
            case _:
                return NotImplemented

    @overload
    def dot(self, rhs: Displacement2d) -> Area:
        pass

    @overload
    def dot(self, rhs: Vector2d) -> Length:
        pass

    @overload
    def dot(self, rhs: Direction2d) -> Length:
        pass

    def dot(self, rhs):
        """Compute the dot product of two vector-like values."""
        match rhs:
            case Displacement2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement2d_dot_Displacement2d_Displacement2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement2d_dot_Displacement2d_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement2d_dot_Displacement2d_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case _:
                return NotImplemented

    @overload
    def cross(self, rhs: Displacement2d) -> Area:
        pass

    @overload
    def cross(self, rhs: Vector2d) -> Length:
        pass

    @overload
    def cross(self, rhs: Direction2d) -> Length:
        pass

    def cross(self, rhs):
        """Compute the cross product of two vector-like values."""
        match rhs:
            case Displacement2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement2d_cross_Displacement2d_Displacement2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement2d_cross_Displacement2d_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement2d_cross_Displacement2d_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> Displacement2d:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement2d_mul_Float_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        x, y = self.components()
        return (
            "Displacement2d.meters("
            + str(x.in_meters())
            + ","
            + str(y.in_meters())
            + ")"
        )


def _displacement2d_zero() -> Displacement2d:
    output = c_void_p()
    _lib.opensolid_Displacement2d_zero(c_void_p(), ctypes.byref(output))
    return Displacement2d._new(output)


Displacement2d.zero = _displacement2d_zero()


class AreaVector2d:
    """A vector in 2D with units of area."""

    _ptr: c_void_p

    def __init__(self, x_component: Area, y_component: Area) -> None:
        """Construct a vector from its X and Y components."""
        inputs = _Tuple2_c_void_p_c_void_p(x_component._ptr, y_component._ptr)
        self._ptr = c_void_p()
        _lib.opensolid_AreaVector2d_constructor_Area_Area(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> AreaVector2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(AreaVector2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: AreaVector2d = None  # type: ignore[assignment]
    """The zero vector."""

    @staticmethod
    def xy(x_component: Area, y_component: Area) -> AreaVector2d:
        """Construct a vector from its X and Y components."""
        inputs = _Tuple2_c_void_p_c_void_p(x_component._ptr, y_component._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector2d_xy_Area_Area(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector2d._new(output)

    @staticmethod
    def x(x_component: Area) -> AreaVector2d:
        """Construct a vector from just an X component.

        The Y component will be set to zero.
        """
        inputs = x_component._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector2d_x_Area(ctypes.byref(inputs), ctypes.byref(output))
        return AreaVector2d._new(output)

    @staticmethod
    def y(y_component: Area) -> AreaVector2d:
        """Construct a vector from just a Y component.

        The X component will be set to zero.
        """
        inputs = y_component._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector2d_y_Area(ctypes.byref(inputs), ctypes.byref(output))
        return AreaVector2d._new(output)

    @staticmethod
    def polar(magnitude: Area, angle: Angle) -> AreaVector2d:
        """Construct a vector from its magnitude (length) and angle."""
        inputs = _Tuple2_c_void_p_c_void_p(magnitude._ptr, angle._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector2d_polar_Area_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector2d._new(output)

    @staticmethod
    def square_meters(x_component: float, y_component: float) -> AreaVector2d:
        """Construct a vector from its X and Y components given in square meters."""
        inputs = _Tuple2_c_double_c_double(x_component, y_component)
        output = c_void_p()
        _lib.opensolid_AreaVector2d_squareMeters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector2d._new(output)

    @staticmethod
    def from_components(components: tuple[Area, Area]) -> AreaVector2d:
        """Construct a vector from a pair of X and Y components."""
        inputs = _Tuple2_c_void_p_c_void_p(components[0]._ptr, components[1]._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector2d_fromComponents_Tuple2AreaArea(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector2d._new(output)

    def components(self) -> tuple[Area, Area]:
        """Get the X and Y components of a vector as a tuple."""
        inputs = self._ptr
        output = _Tuple2_c_void_p_c_void_p()
        _lib.opensolid_AreaVector2d_components(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (Area._new(c_void_p(output.field0)), Area._new(c_void_p(output.field1)))

    def x_component(self) -> Area:
        """Get the X component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector2d_xComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Area._new(output)

    def y_component(self) -> Area:
        """Get the Y component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector2d_yComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Area._new(output)

    def direction(self) -> Direction2d:
        """Attempt to get the direction of a vector.

        The current tolerance will be used to check if the vector is zero
        (and therefore does not have a direction).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_area_tolerance()._ptr, self._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_AreaVector2d_direction(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Direction2d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def normalize(self) -> Vector2d:
        """Normalize a vector.

        If the original vector is exactly zero, then the result will be zero as well.
        Otherwise, the result will be a unit vector.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector2d_normalize(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    def angle(self) -> Angle:
        """Get the angle of a vector.

        The angle is measured counterclockwise from the positive X axis, so:

          * A vector in the positive X direction has an angle of zero.
          * A vector in the positive Y direction has an angle of 90 degrees.
          * A vector in the negative Y direction has an angle of -90 degrees.
          * It is not defined whether a vector exactly in the negative X direction has
            an angle of -180 or +180 degrees. (Currently it is reported as having an
            angle of +180 degrees, but this should not be relied upon.)

        The returned angle will be between -180 and +180 degrees.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector2d_angle(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    def is_zero(self) -> bool:
        """Check if an area vector is zero, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_area_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_AreaVector2d_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __neg__(self) -> AreaVector2d:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector2d_neg(ctypes.byref(inputs), ctypes.byref(output))
        return AreaVector2d._new(output)

    def __add__(self, rhs: AreaVector2d) -> AreaVector2d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector2d_add_AreaVector2d_AreaVector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector2d._new(output)

    def __sub__(self, rhs: AreaVector2d) -> AreaVector2d:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector2d_sub_AreaVector2d_AreaVector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector2d._new(output)

    def __mul__(self, rhs: float) -> AreaVector2d:
        """Return ``self * rhs``."""
        inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
        output = c_void_p()
        _lib.opensolid_AreaVector2d_mul_AreaVector2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector2d._new(output)

    @overload
    def __truediv__(self, rhs: float) -> AreaVector2d:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> Displacement2d:
        pass

    @overload
    def __truediv__(self, rhs: Area) -> Vector2d:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AreaVector2d_div_AreaVector2d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector2d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector2d_div_AreaVector2d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement2d._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector2d_div_AreaVector2d_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector2d._new(output)
            case _:
                return NotImplemented

    @overload
    def dot(self, rhs: Vector2d) -> Area:
        pass

    @overload
    def dot(self, rhs: Direction2d) -> Area:
        pass

    def dot(self, rhs):
        """Compute the dot product of two vector-like values."""
        match rhs:
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector2d_dot_AreaVector2d_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector2d_dot_AreaVector2d_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case _:
                return NotImplemented

    @overload
    def cross(self, rhs: Vector2d) -> Area:
        pass

    @overload
    def cross(self, rhs: Direction2d) -> Area:
        pass

    def cross(self, rhs):
        """Compute the cross product of two vector-like values."""
        match rhs:
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector2d_cross_AreaVector2d_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector2d_cross_AreaVector2d_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> AreaVector2d:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector2d_mul_Float_AreaVector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector2d._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        x, y = self.components()
        return (
            "AreaVector2d.square_meters("
            + str(x.in_square_meters())
            + ","
            + str(y.in_square_meters())
            + ")"
        )


def _areavector2d_zero() -> AreaVector2d:
    output = c_void_p()
    _lib.opensolid_AreaVector2d_zero(c_void_p(), ctypes.byref(output))
    return AreaVector2d._new(output)


AreaVector2d.zero = _areavector2d_zero()


class Direction2d:
    """A direction in 2D.

    This is effectively a type-safe unit vector.
    """

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Direction2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Direction2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    x: Direction2d = None  # type: ignore[assignment]
    """The X direction."""

    y: Direction2d = None  # type: ignore[assignment]
    """The Y direction."""

    @staticmethod
    def from_angle(angle: Angle) -> Direction2d:
        """Construct a direction from an angle.

        The angle is measured counterclockwise from the positive X direction, so:

          * An angle of zero corresponds to the positive X direction
          * An angle of 90 degrees corresponds to the positive Y direction
          * An angle of 180 degrees (or -180 degrees) corresponds to the negative X direction
        """
        inputs = angle._ptr
        output = c_void_p()
        _lib.opensolid_Direction2d_fromAngle_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction2d._new(output)

    @staticmethod
    def degrees(value: float) -> Direction2d:
        """Construct a direction from an angle given in degrees.

        See 'fromAngle' for details.
        """
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Direction2d_degrees_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction2d._new(output)

    @staticmethod
    def radians(value: float) -> Direction2d:
        """Construct a direction from an angle given in radians.

        See 'fromAngle' for details.
        """
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Direction2d_radians_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction2d._new(output)

    def to_angle(self) -> Angle:
        """Convert a direction to an angle.

        The angle is measured counterclockwise from the positive X direction, so:

          * The positive X direction has an angle of zero.
          * The positive Y direction has an angle of 90 degrees.
          * The negative Y direction has an angle of -90 degrees.
          * It is not defined whether the negative X direction has an angle of -180 or
            +180 degrees. (Currently it is reported as having an angle of +180 degrees,
            but this should not be relied upon.)

        The returned angle will be between -180 and +180 degrees.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Direction2d_toAngle(ctypes.byref(inputs), ctypes.byref(output))
        return Angle._new(output)

    def angle_to(self, other: Direction2d) -> Angle:
        """Measure the signed angle from one direction to another.

        The angle will be measured counterclockwise from the first direction to the
        second, and will always be between -180 and +180 degrees.
        """
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Direction2d_angleTo_Direction2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Angle._new(output)

    def components(self) -> tuple[float, float]:
        """Get the XY components of a direction as a tuple."""
        inputs = self._ptr
        output = _Tuple2_c_double_c_double()
        _lib.opensolid_Direction2d_components(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (output.field0, output.field1)

    def x_component(self) -> float:
        """Get the X component of a direction."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Direction2d_xComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def y_component(self) -> float:
        """Get the Y component of a direction."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Direction2d_yComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def __neg__(self) -> Direction2d:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Direction2d_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Direction2d._new(output)

    @overload
    def __mul__(self, rhs: float) -> Vector2d:
        pass

    @overload
    def __mul__(self, rhs: Length) -> Displacement2d:
        pass

    @overload
    def __mul__(self, rhs: Area) -> AreaVector2d:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Direction2d_mul_Direction2d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector2d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction2d_mul_Direction2d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement2d._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction2d_mul_Direction2d_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector2d._new(output)
            case _:
                return NotImplemented

    @overload
    def dot(self, rhs: Direction2d) -> float:
        pass

    @overload
    def dot(self, rhs: Vector2d) -> float:
        pass

    @overload
    def dot(self, rhs: Displacement2d) -> Length:
        pass

    @overload
    def dot(self, rhs: AreaVector2d) -> Area:
        pass

    def dot(self, rhs):
        """Compute the dot product of two vector-like values."""
        match rhs:
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Direction2d_dot_Direction2d_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Direction2d_dot_Direction2d_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Displacement2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction2d_dot_Direction2d_Displacement2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case AreaVector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction2d_dot_Direction2d_AreaVector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case _:
                return NotImplemented

    @overload
    def cross(self, rhs: Direction2d) -> float:
        pass

    @overload
    def cross(self, rhs: Vector2d) -> float:
        pass

    @overload
    def cross(self, rhs: Displacement2d) -> Length:
        pass

    @overload
    def cross(self, rhs: AreaVector2d) -> Area:
        pass

    def cross(self, rhs):
        """Compute the cross product of two vector-like values."""
        match rhs:
            case Direction2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Direction2d_cross_Direction2d_Direction2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Direction2d_cross_Direction2d_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Displacement2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction2d_cross_Direction2d_Displacement2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case AreaVector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction2d_cross_Direction2d_AreaVector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> Vector2d:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Direction2d_mul_Float_Direction2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        return "Direction2d.degrees(" + str(self.to_angle().in_degrees()) + ")"


def _direction2d_x() -> Direction2d:
    output = c_void_p()
    _lib.opensolid_Direction2d_x(c_void_p(), ctypes.byref(output))
    return Direction2d._new(output)


Direction2d.x = _direction2d_x()


def _direction2d_y() -> Direction2d:
    output = c_void_p()
    _lib.opensolid_Direction2d_y(c_void_p(), ctypes.byref(output))
    return Direction2d._new(output)


Direction2d.y = _direction2d_y()


class Point2d:
    """A point in 2D, defined by its X and Y coordinates."""

    _ptr: c_void_p

    def __init__(self, x_coordinate: Length, y_coordinate: Length) -> None:
        """Construct a point from its X and Y coordinates."""
        inputs = _Tuple2_c_void_p_c_void_p(x_coordinate._ptr, y_coordinate._ptr)
        self._ptr = c_void_p()
        _lib.opensolid_Point2d_constructor_Length_Length(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> Point2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Point2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    origin: Point2d = None  # type: ignore[assignment]
    """The point with coordinates (0,0)."""

    @staticmethod
    def xy(x_coordinate: Length, y_coordinate: Length) -> Point2d:
        """Construct a point from its X and Y coordinates."""
        inputs = _Tuple2_c_void_p_c_void_p(x_coordinate._ptr, y_coordinate._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_xy_Length_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    @staticmethod
    def x(x_coordinate: Length) -> Point2d:
        """Construct a point along the X axis, with the given X coordinate."""
        inputs = x_coordinate._ptr
        output = c_void_p()
        _lib.opensolid_Point2d_x_Length(ctypes.byref(inputs), ctypes.byref(output))
        return Point2d._new(output)

    @staticmethod
    def y(y_coordinate: Length) -> Point2d:
        """Construct a point along the Y axis, with the given Y coordinate."""
        inputs = y_coordinate._ptr
        output = c_void_p()
        _lib.opensolid_Point2d_y_Length(ctypes.byref(inputs), ctypes.byref(output))
        return Point2d._new(output)

    @staticmethod
    def meters(x_coordinate: float, y_coordinate: float) -> Point2d:
        """Construct a point from its X and Y coordinates given in meters."""
        inputs = _Tuple2_c_double_c_double(x_coordinate, y_coordinate)
        output = c_void_p()
        _lib.opensolid_Point2d_meters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    @staticmethod
    def centimeters(x_coordinate: float, y_coordinate: float) -> Point2d:
        """Construct a point from its X and Y coordinates given in centimeters."""
        inputs = _Tuple2_c_double_c_double(x_coordinate, y_coordinate)
        output = c_void_p()
        _lib.opensolid_Point2d_centimeters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    @staticmethod
    def millimeters(x_coordinate: float, y_coordinate: float) -> Point2d:
        """Construct a point from its X and Y coordinates given in millimeters."""
        inputs = _Tuple2_c_double_c_double(x_coordinate, y_coordinate)
        output = c_void_p()
        _lib.opensolid_Point2d_millimeters_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    @staticmethod
    def inches(x_coordinate: float, y_coordinate: float) -> Point2d:
        """Construct a point from its X and Y coordinates given in inches."""
        inputs = _Tuple2_c_double_c_double(x_coordinate, y_coordinate)
        output = c_void_p()
        _lib.opensolid_Point2d_inches_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    @staticmethod
    def from_coordinates(coordinates: tuple[Length, Length]) -> Point2d:
        """Construct a point from a pair of X and Y coordinates."""
        inputs = _Tuple2_c_void_p_c_void_p(coordinates[0]._ptr, coordinates[1]._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_fromCoordinates_Tuple2LengthLength(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def coordinates(self) -> tuple[Length, Length]:
        """Get the X and Y coordinates of a point."""
        inputs = self._ptr
        output = _Tuple2_c_void_p_c_void_p()
        _lib.opensolid_Point2d_coordinates(ctypes.byref(inputs), ctypes.byref(output))
        return (
            Length._new(c_void_p(output.field0)),
            Length._new(c_void_p(output.field1)),
        )

    def x_coordinate(self) -> Length:
        """Get the X coordinate of a point."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Point2d_xCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    def y_coordinate(self) -> Length:
        """Get the Y coordinate of a point."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Point2d_yCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    def distance_to(self, other: Point2d) -> Length:
        """Compute the distance from one point to another."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_distanceTo_Point2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def midpoint(self, other: Point2d) -> Point2d:
        """Find the midpoint between two points."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_midpoint_Point2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def place_on(self, plane: Plane3d) -> Point3d:
        """Convert a 2D point to 3D point by placing it on a plane.

        Given a 2D point defined within a plane's coordinate system,
        this returns the corresponding 3D point.
        """
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_placeOn_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def scale_along(self, axis: Axis2d, scale: float) -> Point2d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_scaleAlong_Axis2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def scale_about(self, point: Point2d, scale: float) -> Point2d:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_scaleAbout_Point2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def mirror_across(self, axis: Axis2d) -> Point2d:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_mirrorAcross_Axis2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def translate_by(self, displacement: Displacement2d) -> Point2d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_translateBy_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def translate_in(self, direction: Direction2d, distance: Length) -> Point2d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Point2d_translateIn_Direction2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def translate_along(self, axis: Axis2d, distance: Length) -> Point2d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_translateAlong_Axis2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def rotate_around(self, point: Point2d, angle: Angle) -> Point2d:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_rotateAround_Point2d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    @overload
    def __sub__(self, rhs: Point2d) -> Displacement2d:
        pass

    @overload
    def __sub__(self, rhs: Displacement2d) -> Point2d:
        pass

    @overload
    def __sub__(self, rhs: Curve2d) -> DisplacementCurve2d:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case Point2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Point2d_sub_Point2d_Point2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement2d._new(output)
            case Displacement2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Point2d_sub_Point2d_Displacement2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Point2d._new(output)
            case Curve2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Point2d_sub_Point2d_Curve2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return DisplacementCurve2d._new(output)
            case _:
                return NotImplemented

    def __add__(self, rhs: Displacement2d) -> Point2d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Point2d_add_Point2d_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        x, y = self.coordinates()
        return "Point2d.meters(" + str(x.in_meters()) + "," + str(y.in_meters()) + ")"


def _point2d_origin() -> Point2d:
    output = c_void_p()
    _lib.opensolid_Point2d_origin(c_void_p(), ctypes.byref(output))
    return Point2d._new(output)


Point2d.origin = _point2d_origin()


class UvPoint:
    """A point in UV parameter space."""

    _ptr: c_void_p

    def __init__(self, u_coordinate: float, v_coordinate: float) -> None:
        """Construct a point from its U and V coordinates."""
        inputs = _Tuple2_c_double_c_double(u_coordinate, v_coordinate)
        self._ptr = c_void_p()
        _lib.opensolid_UvPoint_constructor_Float_Float(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> UvPoint:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(UvPoint)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    origin: UvPoint = None  # type: ignore[assignment]
    """The point with coordinates (0,0)."""

    @staticmethod
    def from_coordinates(coordinates: tuple[float, float]) -> UvPoint:
        """Construct a point from a pair of U and V coordinates."""
        inputs = _Tuple2_c_double_c_double(coordinates[0], coordinates[1])
        output = c_void_p()
        _lib.opensolid_UvPoint_fromCoordinates_Tuple2FloatFloat(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def coordinates(self) -> tuple[float, float]:
        """Get the U and V coordinates of a point."""
        inputs = self._ptr
        output = _Tuple2_c_double_c_double()
        _lib.opensolid_UvPoint_coordinates(ctypes.byref(inputs), ctypes.byref(output))
        return (output.field0, output.field1)

    def u_coordinate(self) -> float:
        """Get the U coordinate of a point."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_UvPoint_uCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def v_coordinate(self) -> float:
        """Get the V coordinate of a point."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_UvPoint_vCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def distance_to(self, other: UvPoint) -> float:
        """Compute the distance from one point to another."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_double()
        _lib.opensolid_UvPoint_distanceTo_UvPoint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def midpoint(self, other: UvPoint) -> UvPoint:
        """Find the midpoint between two points."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_midpoint_UvPoint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def scale_along(self, axis: UvAxis, scale: float) -> UvPoint:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_scaleAlong_UvAxis_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def scale_about(self, point: UvPoint, scale: float) -> UvPoint:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_scaleAbout_UvPoint_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def mirror_across(self, axis: UvAxis) -> UvPoint:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_mirrorAcross_UvAxis(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def translate_by(self, displacement: Vector2d) -> UvPoint:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_translateBy_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def translate_in(self, direction: Direction2d, distance: float) -> UvPoint:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(direction._ptr, distance, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_translateIn_Direction2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def translate_along(self, axis: UvAxis, distance: float) -> UvPoint:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, distance, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_translateAlong_UvAxis_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def rotate_around(self, point: UvPoint, angle: Angle) -> UvPoint:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_rotateAround_UvPoint_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    @overload
    def __sub__(self, rhs: UvPoint) -> Vector2d:
        pass

    @overload
    def __sub__(self, rhs: Vector2d) -> UvPoint:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case UvPoint():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_UvPoint_sub_UvPoint_UvPoint(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector2d._new(output)
            case Vector2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_UvPoint_sub_UvPoint_Vector2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return UvPoint._new(output)
            case _:
                return NotImplemented

    def __add__(self, rhs: Vector2d) -> UvPoint:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_UvPoint_add_UvPoint_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        x, y = self.coordinates()
        return "UvPoint(" + str(x) + "," + str(y) + ")"


def _uvpoint_origin() -> UvPoint:
    output = c_void_p()
    _lib.opensolid_UvPoint_origin(c_void_p(), ctypes.byref(output))
    return UvPoint._new(output)


UvPoint.origin = _uvpoint_origin()


class Bounds2d:
    """A bounding box in 2D."""

    _ptr: c_void_p

    def __init__(self, x_coordinate: LengthRange, y_coordinate: LengthRange) -> None:
        """Construct a bounding box from its X and Y coordinate ranges."""
        inputs = _Tuple2_c_void_p_c_void_p(x_coordinate._ptr, y_coordinate._ptr)
        self._ptr = c_void_p()
        _lib.opensolid_Bounds2d_constructor_LengthRange_LengthRange(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> Bounds2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Bounds2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def constant(point: Point2d) -> Bounds2d:
        """Construct a zero-size bounding box containing a single point."""
        inputs = point._ptr
        output = c_void_p()
        _lib.opensolid_Bounds2d_constant_Point2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    @staticmethod
    def from_corners(first_point: Point2d, second_point: Point2d) -> Bounds2d:
        """Construct a bounding box from two corner points."""
        inputs = _Tuple2_c_void_p_c_void_p(first_point._ptr, second_point._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_fromCorners_Point2d_Point2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    @staticmethod
    def hull(points: list[Point2d]) -> Bounds2d:
        """Construct a bounding box containing all points in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(points))(*[item._ptr for item in points]),
            )
            if points
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_Bounds2d_hull_NonEmptyPoint2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    @staticmethod
    def aggregate(bounds: list[Bounds2d]) -> Bounds2d:
        """Construct a bounding box containing all bounding boxes in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(bounds))(*[item._ptr for item in bounds]),
            )
            if bounds
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_Bounds2d_aggregate_NonEmptyBounds2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def coordinates(self) -> tuple[LengthRange, LengthRange]:
        """Get the X and Y coordinate ranges of a bounding box."""
        inputs = self._ptr
        output = _Tuple2_c_void_p_c_void_p()
        _lib.opensolid_Bounds2d_coordinates(ctypes.byref(inputs), ctypes.byref(output))
        return (
            LengthRange._new(c_void_p(output.field0)),
            LengthRange._new(c_void_p(output.field1)),
        )

    def x_coordinate(self) -> LengthRange:
        """Get the X coordinate range of a bounding box."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Bounds2d_xCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return LengthRange._new(output)

    def y_coordinate(self) -> LengthRange:
        """Get the Y coordinate range of a bounding box."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Bounds2d_yCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return LengthRange._new(output)

    def scale_along(self, axis: Axis2d, scale: float) -> Bounds2d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_scaleAlong_Axis2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def scale_about(self, point: Point2d, scale: float) -> Bounds2d:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_scaleAbout_Point2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def mirror_across(self, axis: Axis2d) -> Bounds2d:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_mirrorAcross_Axis2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def translate_by(self, displacement: Displacement2d) -> Bounds2d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_translateBy_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def translate_in(self, direction: Direction2d, distance: Length) -> Bounds2d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Bounds2d_translateIn_Direction2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def translate_along(self, axis: Axis2d, distance: Length) -> Bounds2d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_translateAlong_Axis2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def rotate_around(self, point: Point2d, angle: Angle) -> Bounds2d:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_rotateAround_Point2d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def __add__(self, rhs: Displacement2d) -> Bounds2d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_add_Bounds2d_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def __sub__(self, rhs: Displacement2d) -> Bounds2d:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds2d_sub_Bounds2d_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds2d._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        x, y = self.coordinates()
        return "Bounds2d(" + repr(x) + "," + repr(y) + ")"


class UvBounds:
    """A bounding box in UV parameter space."""

    _ptr: c_void_p

    def __init__(self, u_coordinate: Range, v_coordinate: Range) -> None:
        """Construct a bounding box from its U and V coordinate ranges."""
        inputs = _Tuple2_c_void_p_c_void_p(u_coordinate._ptr, v_coordinate._ptr)
        self._ptr = c_void_p()
        _lib.opensolid_UvBounds_constructor_Range_Range(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> UvBounds:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(UvBounds)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def constant(point: UvPoint) -> UvBounds:
        """Construct a zero-size bounding box containing a single point."""
        inputs = point._ptr
        output = c_void_p()
        _lib.opensolid_UvBounds_constant_UvPoint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    @staticmethod
    def from_corners(first_point: UvPoint, second_point: UvPoint) -> UvBounds:
        """Construct a bounding box from two corner points."""
        inputs = _Tuple2_c_void_p_c_void_p(first_point._ptr, second_point._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_fromCorners_UvPoint_UvPoint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    @staticmethod
    def hull(points: list[UvPoint]) -> UvBounds:
        """Construct a bounding box containing all points in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(points))(*[item._ptr for item in points]),
            )
            if points
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_UvBounds_hull_NonEmptyUvPoint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    @staticmethod
    def aggregate(bounds: list[UvBounds]) -> UvBounds:
        """Construct a bounding box containing all bounding boxes in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(bounds))(*[item._ptr for item in bounds]),
            )
            if bounds
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_UvBounds_aggregate_NonEmptyUvBounds(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def coordinates(self) -> tuple[Range, Range]:
        """Get the X and Y coordinate ranges of a bounding box."""
        inputs = self._ptr
        output = _Tuple2_c_void_p_c_void_p()
        _lib.opensolid_UvBounds_coordinates(ctypes.byref(inputs), ctypes.byref(output))
        return (
            Range._new(c_void_p(output.field0)),
            Range._new(c_void_p(output.field1)),
        )

    def u_coordinate(self) -> Range:
        """Get the U coordinate range of a bounding box."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_UvBounds_uCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    def v_coordinate(self) -> Range:
        """Get the V coordinate range of a bounding box."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_UvBounds_vCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Range._new(output)

    def scale_along(self, axis: UvAxis, scale: float) -> UvBounds:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_scaleAlong_UvAxis_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def scale_about(self, point: UvPoint, scale: float) -> UvBounds:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_scaleAbout_UvPoint_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def mirror_across(self, axis: UvAxis) -> UvBounds:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_mirrorAcross_UvAxis(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def translate_by(self, displacement: Vector2d) -> UvBounds:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_translateBy_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def translate_in(self, direction: Direction2d, distance: float) -> UvBounds:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(direction._ptr, distance, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_translateIn_Direction2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def translate_along(self, axis: UvAxis, distance: float) -> UvBounds:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, distance, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_translateAlong_UvAxis_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def rotate_around(self, point: UvPoint, angle: Angle) -> UvBounds:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_rotateAround_UvPoint_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def __add__(self, rhs: Vector2d) -> UvBounds:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_add_UvBounds_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def __sub__(self, rhs: Vector2d) -> UvBounds:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_UvBounds_sub_UvBounds_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvBounds._new(output)

    def __repr__(self) -> str:
        """Return a human-readable representation of this value."""
        u, v = self.coordinates()
        return "UvBounds(" + repr(u) + "," + repr(v) + ")"


class Curve:
    """A parametric curve definining a unitless value in terms of a parameter value."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Curve:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Curve)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: Curve = None  # type: ignore[assignment]
    """A curve equal to zero everywhere."""

    t: Curve = None  # type: ignore[assignment]
    """A curve parameter.

    In other words, a curve whose value is equal to its input parameter.
    When defining parametric curves, you will typically start with 'Curve.t'
    and then use arithmetic operators etc. to build up more complex curves.
    """

    @staticmethod
    def constant(value: float) -> Curve:
        """Create a curve with the given constant value."""
        inputs = c_double(value)
        output = c_void_p()
        _lib.opensolid_Curve_constant_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    @staticmethod
    def line(start: float, end: float) -> Curve:
        """Create a curve that linearly interpolates from the first value to the second."""
        inputs = _Tuple2_c_double_c_double(start, end)
        output = c_void_p()
        _lib.opensolid_Curve_line_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve._new(output)

    def squared(self) -> Curve:
        """Compute the square of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Curve_squared(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def sqrt(self) -> Curve:
        """Compute the square root of a curve."""
        inputs = _Tuple2_c_double_c_void_p(_float_tolerance(), self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve_sqrt(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def evaluate(self, parameter_value: float) -> float:
        """Evaluate a curve at a given parameter value.

        The parameter value should be between 0 and 1.
        """
        inputs = _Tuple2_c_double_c_void_p(parameter_value, self._ptr)
        output = c_double()
        _lib.opensolid_Curve_evaluate_Float(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def zeros(self) -> list[Curve.Zero]:
        """Find all points at which the given curve is zero.

        This includes not only points where the curve *crosses* zero,
        but also where it is *tangent* to zero.
        For example, y=x-3 crosses zero at x=3,
        while y=(x-3)^2 is tangent to zero at x=3.

        We define y=x-3 as having a zero of order 0 at x=3,
        since only the "derivative of order zero" (the curve itself)
        is zero at that point.
        Similarly, y=(x-3)^2 has a zero of order 1 at x=3,
        since the first derivative (but not the second derivative)
        is zero at that point.

        Currently, this function up to third-order zeros
        (e.g. y=x^4 has a third-order zero at x=0,
        since everything up to the third derivative is zero at x=0).

        The current tolerance is used to determine
        whether a given point should be considered a zero,
        and of what order.
        For example, the curve y=x^2-0.0001 is *exactly* zero at x=0.01 and x=-0.01.
        However, note that the curve is also very close to zero at x=0,
        and at that point the first derivative is *also* zero.
        In many cases, it is reasonable to assume that
        the 0.0001 is an artifact of numerical roundoff,
        and the curve actually has a single zero of order 1 at x=0.
        The current tolerance is used to choose which case to report.
        In this example, a tolerance of 0.000001
        would mean that we consider 0.0001 a meaningful value (not just roundoff),
        so we would end up reporting two order-0 zeros at x=0.01 and x=-0.01.
        On the other hand, a tolerance of 0.01 would mean that
        we consider 0.0001 as just roundoff error,
        so we would end up reporting a single order-1 zero at x=0
        (the point at which the *first derivative* is zero).
        """
        inputs = _Tuple2_c_double_c_void_p(_float_tolerance(), self._ptr)
        output = _Result_List_c_void_p()
        _lib.opensolid_Curve_zeros(ctypes.byref(inputs), ctypes.byref(output))
        return (
            [
                Curve.Zero._new(c_void_p(item))
                for item in [
                    output.field2.field1[index] for index in range(output.field2.field0)
                ]
            ]
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def is_zero(self) -> bool:
        """Check if a curve is zero everywhere, within the current tolerance."""
        inputs = _Tuple2_c_double_c_void_p(_float_tolerance(), self._ptr)
        output = c_int64()
        _lib.opensolid_Curve_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __neg__(self) -> Curve:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Curve_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    @overload
    def __add__(self, rhs: float) -> Curve:
        pass

    @overload
    def __add__(self, rhs: Curve) -> Curve:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Curve_add_Curve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_add_Curve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: float) -> Curve:
        pass

    @overload
    def __sub__(self, rhs: Curve) -> Curve:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Curve_sub_Curve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_sub_Curve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> Curve:
        pass

    @overload
    def __mul__(self, rhs: Curve) -> Curve:
        pass

    @overload
    def __mul__(self, rhs: Length) -> LengthCurve:
        pass

    @overload
    def __mul__(self, rhs: Area) -> AreaCurve:
        pass

    @overload
    def __mul__(self, rhs: Angle) -> AngleCurve:
        pass

    @overload
    def __mul__(self, rhs: LengthCurve) -> LengthCurve:
        pass

    @overload
    def __mul__(self, rhs: AreaCurve) -> AreaCurve:
        pass

    @overload
    def __mul__(self, rhs: AngleCurve) -> AngleCurve:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Curve_mul_Curve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_mul_Curve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_mul_Curve_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_mul_Curve_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_mul_Curve_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_mul_Curve_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case AreaCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_mul_Curve_AreaCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case AngleCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_mul_Curve_AngleCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> Curve:
        pass

    @overload
    def __truediv__(self, rhs: Curve) -> Curve:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Curve_div_Curve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve_div_Curve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case _:
                return NotImplemented

    def __radd__(self, lhs: float) -> Curve:
        """Return ``lhs <> self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve_add_Float_Curve(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def __rsub__(self, lhs: float) -> Curve:
        """Return ``lhs - self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve_sub_Float_Curve(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def __rmul__(self, lhs: float) -> Curve:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve_mul_Float_Curve(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def __rtruediv__(self, lhs: float) -> Curve:
        """Return ``lhs / self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve_div_Float_Curve(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    class Zero:
        """A point where a given curve is equal to zero."""

        _ptr: c_void_p

        @staticmethod
        def _new(ptr: c_void_p) -> Curve.Zero:
            """Construct directly from an underlying C pointer."""
            obj = object.__new__(Curve.Zero)
            obj._ptr = ptr
            return obj

        def __del__(self) -> None:
            """Free the underlying Haskell value."""
            _lib.opensolid_release(self._ptr)

        def location(self) -> float:
            """Get the parameter value at which the curve is zero."""
            inputs = self._ptr
            output = c_double()
            _lib.opensolid_CurveZero_location(
                ctypes.byref(inputs), ctypes.byref(output)
            )
            return output.value

        def order(self) -> int:
            """Check whether the zero is a crossing zero, a tangent zero etc.

            * An order 0 zero means the curve crosses zero at the given location,
              with a non-zero first derivative.
            * An order 1 zero means the first derivative is also zero at the given
              location, but the second derivative is not (that is, the curve just
              'touches' zero at that point).
            * An order 2 zero means the first and second derivatives are zero at the
              given location, etc.
            """
            inputs = self._ptr
            output = c_int64()
            _lib.opensolid_CurveZero_order(ctypes.byref(inputs), ctypes.byref(output))
            return output.value

        def sign(self) -> int:
            """Check whether the curve 'curves up' or 'curves down' at the zero.

            A positive sign means that the curve is positive to the right of the zero
            (for a crossing zero, that means the curve will be negative to the left,
            but for an order 1 tangent zero, that means the curve will also be positive
            to the left!). Similarly, a negative sign means that the curve is negative
            to the right of the zero.
            """
            inputs = self._ptr
            output = c_int64()
            _lib.opensolid_CurveZero_sign(ctypes.byref(inputs), ctypes.byref(output))
            return output.value


def _curve_zero() -> Curve:
    output = c_void_p()
    _lib.opensolid_Curve_zero(c_void_p(), ctypes.byref(output))
    return Curve._new(output)


Curve.zero = _curve_zero()


def _curve_t() -> Curve:
    output = c_void_p()
    _lib.opensolid_Curve_t(c_void_p(), ctypes.byref(output))
    return Curve._new(output)


Curve.t = _curve_t()


class LengthCurve:
    """A parametric curve definining a length in terms of a parameter value."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> LengthCurve:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(LengthCurve)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: LengthCurve = None  # type: ignore[assignment]
    """A curve equal to zero everywhere."""

    @staticmethod
    def constant(value: Length) -> LengthCurve:
        """Create a curve with the given constant value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_LengthCurve_constant_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthCurve._new(output)

    @staticmethod
    def line(start: Length, end: Length) -> LengthCurve:
        """Create a curve that linearly interpolates from the first value to the second."""
        inputs = _Tuple2_c_void_p_c_void_p(start._ptr, end._ptr)
        output = c_void_p()
        _lib.opensolid_LengthCurve_line_Length_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthCurve._new(output)

    def squared(self) -> AreaCurve:
        """Compute the square of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_LengthCurve_squared(ctypes.byref(inputs), ctypes.byref(output))
        return AreaCurve._new(output)

    def evaluate(self, parameter_value: float) -> Length:
        """Evaluate a curve at a given parameter value.

        The parameter value should be between 0 and 1.
        """
        inputs = _Tuple2_c_double_c_void_p(parameter_value, self._ptr)
        output = c_void_p()
        _lib.opensolid_LengthCurve_evaluate_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def zeros(self) -> list[Curve.Zero]:
        """Find all points at which the given curve is zero.

        This includes not only points where the curve *crosses* zero,
        but also where it is *tangent* to zero.
        For example, y=x-3 crosses zero at x=3,
        while y=(x-3)^2 is tangent to zero at x=3.

        We define y=x-3 as having a zero of order 0 at x=3,
        since only the "derivative of order zero" (the curve itself)
        is zero at that point.
        Similarly, y=(x-3)^2 has a zero of order 1 at x=3,
        since the first derivative (but not the second derivative)
        is zero at that point.

        Currently, this function up to third-order zeros
        (e.g. y=x^4 has a third-order zero at x=0,
        since everything up to the third derivative is zero at x=0).

        The current tolerance is used to determine
        whether a given point should be considered a zero,
        and of what order.
        For example, the curve y=x^2-0.0001 is *exactly* zero at x=0.01 and x=-0.01.
        However, note that the curve is also very close to zero at x=0,
        and at that point the first derivative is *also* zero.
        In many cases, it is reasonable to assume that
        the 0.0001 is an artifact of numerical roundoff,
        and the curve actually has a single zero of order 1 at x=0.
        The current tolerance is used to choose which case to report.
        In this example, a tolerance of 0.000001
        would mean that we consider 0.0001 a meaningful value (not just roundoff),
        so we would end up reporting two order-0 zeros at x=0.01 and x=-0.01.
        On the other hand, a tolerance of 0.01 would mean that
        we consider 0.0001 as just roundoff error,
        so we would end up reporting a single order-1 zero at x=0
        (the point at which the *first derivative* is zero).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = _Result_List_c_void_p()
        _lib.opensolid_LengthCurve_zeros(ctypes.byref(inputs), ctypes.byref(output))
        return (
            [
                Curve.Zero._new(c_void_p(item))
                for item in [
                    output.field2.field1[index] for index in range(output.field2.field0)
                ]
            ]
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def is_zero(self) -> bool:
        """Check if a curve is zero everywhere, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_LengthCurve_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __neg__(self) -> LengthCurve:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_LengthCurve_neg(ctypes.byref(inputs), ctypes.byref(output))
        return LengthCurve._new(output)

    @overload
    def __add__(self, rhs: LengthCurve) -> LengthCurve:
        pass

    @overload
    def __add__(self, rhs: Length) -> LengthCurve:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_add_LengthCurve_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_add_LengthCurve_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: LengthCurve) -> LengthCurve:
        pass

    @overload
    def __sub__(self, rhs: Length) -> LengthCurve:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_sub_LengthCurve_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_sub_LengthCurve_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> LengthCurve:
        pass

    @overload
    def __mul__(self, rhs: LengthCurve) -> AreaCurve:
        pass

    @overload
    def __mul__(self, rhs: Length) -> AreaCurve:
        pass

    @overload
    def __mul__(self, rhs: Curve) -> LengthCurve:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_LengthCurve_mul_LengthCurve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_mul_LengthCurve_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_mul_LengthCurve_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_mul_LengthCurve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> LengthCurve:
        pass

    @overload
    def __truediv__(self, rhs: LengthCurve) -> Curve:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> Curve:
        pass

    @overload
    def __truediv__(self, rhs: Curve) -> LengthCurve:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_LengthCurve_div_LengthCurve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_div_LengthCurve_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_div_LengthCurve_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_LengthCurve_div_LengthCurve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> LengthCurve:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_LengthCurve_mul_Float_LengthCurve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return LengthCurve._new(output)


def _lengthcurve_zero() -> LengthCurve:
    output = c_void_p()
    _lib.opensolid_LengthCurve_zero(c_void_p(), ctypes.byref(output))
    return LengthCurve._new(output)


LengthCurve.zero = _lengthcurve_zero()


class AreaCurve:
    """A parametric curve definining an area in terms of a parameter value."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> AreaCurve:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(AreaCurve)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: AreaCurve = None  # type: ignore[assignment]
    """A curve equal to zero everywhere."""

    @staticmethod
    def constant(value: Area) -> AreaCurve:
        """Create a curve with the given constant value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_AreaCurve_constant_Area(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaCurve._new(output)

    @staticmethod
    def line(start: Area, end: Area) -> AreaCurve:
        """Create a curve that linearly interpolates from the first value to the second."""
        inputs = _Tuple2_c_void_p_c_void_p(start._ptr, end._ptr)
        output = c_void_p()
        _lib.opensolid_AreaCurve_line_Area_Area(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaCurve._new(output)

    def sqrt(self) -> LengthCurve:
        """Compute the square root of a curve."""
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaCurve_sqrt(ctypes.byref(inputs), ctypes.byref(output))
        return LengthCurve._new(output)

    def evaluate(self, parameter_value: float) -> Area:
        """Evaluate a curve at a given parameter value.

        The parameter value should be between 0 and 1.
        """
        inputs = _Tuple2_c_double_c_void_p(parameter_value, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaCurve_evaluate_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Area._new(output)

    def zeros(self) -> list[Curve.Zero]:
        """Find all points at which the given curve is zero.

        This includes not only points where the curve *crosses* zero,
        but also where it is *tangent* to zero.
        For example, y=x-3 crosses zero at x=3,
        while y=(x-3)^2 is tangent to zero at x=3.

        We define y=x-3 as having a zero of order 0 at x=3,
        since only the "derivative of order zero" (the curve itself)
        is zero at that point.
        Similarly, y=(x-3)^2 has a zero of order 1 at x=3,
        since the first derivative (but not the second derivative)
        is zero at that point.

        Currently, this function up to third-order zeros
        (e.g. y=x^4 has a third-order zero at x=0,
        since everything up to the third derivative is zero at x=0).

        The current tolerance is used to determine
        whether a given point should be considered a zero,
        and of what order.
        For example, the curve y=x^2-0.0001 is *exactly* zero at x=0.01 and x=-0.01.
        However, note that the curve is also very close to zero at x=0,
        and at that point the first derivative is *also* zero.
        In many cases, it is reasonable to assume that
        the 0.0001 is an artifact of numerical roundoff,
        and the curve actually has a single zero of order 1 at x=0.
        The current tolerance is used to choose which case to report.
        In this example, a tolerance of 0.000001
        would mean that we consider 0.0001 a meaningful value (not just roundoff),
        so we would end up reporting two order-0 zeros at x=0.01 and x=-0.01.
        On the other hand, a tolerance of 0.01 would mean that
        we consider 0.0001 as just roundoff error,
        so we would end up reporting a single order-1 zero at x=0
        (the point at which the *first derivative* is zero).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_area_tolerance()._ptr, self._ptr)
        output = _Result_List_c_void_p()
        _lib.opensolid_AreaCurve_zeros(ctypes.byref(inputs), ctypes.byref(output))
        return (
            [
                Curve.Zero._new(c_void_p(item))
                for item in [
                    output.field2.field1[index] for index in range(output.field2.field0)
                ]
            ]
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def is_zero(self) -> bool:
        """Check if a curve is zero everywhere, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_area_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_AreaCurve_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __neg__(self) -> AreaCurve:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaCurve_neg(ctypes.byref(inputs), ctypes.byref(output))
        return AreaCurve._new(output)

    def __add__(self, rhs: AreaCurve) -> AreaCurve:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_AreaCurve_add_AreaCurve_AreaCurve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaCurve._new(output)

    def __sub__(self, rhs: AreaCurve) -> AreaCurve:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_AreaCurve_sub_AreaCurve_AreaCurve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaCurve._new(output)

    @overload
    def __mul__(self, rhs: float) -> AreaCurve:
        pass

    @overload
    def __mul__(self, rhs: Curve) -> AreaCurve:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AreaCurve_mul_AreaCurve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaCurve_mul_AreaCurve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> AreaCurve:
        pass

    @overload
    def __truediv__(self, rhs: AreaCurve) -> Curve:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> LengthCurve:
        pass

    @overload
    def __truediv__(self, rhs: Area) -> Curve:
        pass

    @overload
    def __truediv__(self, rhs: Curve) -> AreaCurve:
        pass

    @overload
    def __truediv__(self, rhs: LengthCurve) -> LengthCurve:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AreaCurve_div_AreaCurve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case AreaCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaCurve_div_AreaCurve_AreaCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaCurve_div_AreaCurve_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaCurve_div_AreaCurve_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaCurve_div_AreaCurve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaCurve._new(output)
            case LengthCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaCurve_div_AreaCurve_LengthCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return LengthCurve._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> AreaCurve:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaCurve_mul_Float_AreaCurve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaCurve._new(output)


def _areacurve_zero() -> AreaCurve:
    output = c_void_p()
    _lib.opensolid_AreaCurve_zero(c_void_p(), ctypes.byref(output))
    return AreaCurve._new(output)


AreaCurve.zero = _areacurve_zero()


class AngleCurve:
    """A parametric curve definining an angle in terms of a parameter value."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> AngleCurve:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(AngleCurve)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: AngleCurve = None  # type: ignore[assignment]
    """A curve equal to zero everywhere."""

    @staticmethod
    def constant(value: Angle) -> AngleCurve:
        """Create a curve with the given constant value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_AngleCurve_constant_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleCurve._new(output)

    @staticmethod
    def line(start: Angle, end: Angle) -> AngleCurve:
        """Create a curve that linearly interpolates from the first value to the second."""
        inputs = _Tuple2_c_void_p_c_void_p(start._ptr, end._ptr)
        output = c_void_p()
        _lib.opensolid_AngleCurve_line_Angle_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleCurve._new(output)

    def sin(self) -> Curve:
        """Compute the sine of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AngleCurve_sin(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def cos(self) -> Curve:
        """Compute the cosine of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AngleCurve_cos(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def evaluate(self, parameter_value: float) -> Angle:
        """Evaluate a curve at a given parameter value.

        The parameter value should be between 0 and 1.
        """
        inputs = _Tuple2_c_double_c_void_p(parameter_value, self._ptr)
        output = c_void_p()
        _lib.opensolid_AngleCurve_evaluate_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Angle._new(output)

    def zeros(self) -> list[Curve.Zero]:
        """Find all points at which the given curve is zero.

        This includes not only points where the curve *crosses* zero,
        but also where it is *tangent* to zero.
        For example, y=x-3 crosses zero at x=3,
        while y=(x-3)^2 is tangent to zero at x=3.

        We define y=x-3 as having a zero of order 0 at x=3,
        since only the "derivative of order zero" (the curve itself)
        is zero at that point.
        Similarly, y=(x-3)^2 has a zero of order 1 at x=3,
        since the first derivative (but not the second derivative)
        is zero at that point.

        Currently, this function up to third-order zeros
        (e.g. y=x^4 has a third-order zero at x=0,
        since everything up to the third derivative is zero at x=0).

        The current tolerance is used to determine
        whether a given point should be considered a zero,
        and of what order.
        For example, the curve y=x^2-0.0001 is *exactly* zero at x=0.01 and x=-0.01.
        However, note that the curve is also very close to zero at x=0,
        and at that point the first derivative is *also* zero.
        In many cases, it is reasonable to assume that
        the 0.0001 is an artifact of numerical roundoff,
        and the curve actually has a single zero of order 1 at x=0.
        The current tolerance is used to choose which case to report.
        In this example, a tolerance of 0.000001
        would mean that we consider 0.0001 a meaningful value (not just roundoff),
        so we would end up reporting two order-0 zeros at x=0.01 and x=-0.01.
        On the other hand, a tolerance of 0.01 would mean that
        we consider 0.0001 as just roundoff error,
        so we would end up reporting a single order-1 zero at x=0
        (the point at which the *first derivative* is zero).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_angle_tolerance()._ptr, self._ptr)
        output = _Result_List_c_void_p()
        _lib.opensolid_AngleCurve_zeros(ctypes.byref(inputs), ctypes.byref(output))
        return (
            [
                Curve.Zero._new(c_void_p(item))
                for item in [
                    output.field2.field1[index] for index in range(output.field2.field0)
                ]
            ]
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def is_zero(self) -> bool:
        """Check if a curve is zero everywhere, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_angle_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_AngleCurve_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def __neg__(self) -> AngleCurve:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AngleCurve_neg(ctypes.byref(inputs), ctypes.byref(output))
        return AngleCurve._new(output)

    @overload
    def __add__(self, rhs: AngleCurve) -> AngleCurve:
        pass

    @overload
    def __add__(self, rhs: Angle) -> AngleCurve:
        pass

    def __add__(self, rhs):
        """Return ``self <> rhs``."""
        match rhs:
            case AngleCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleCurve_add_AngleCurve_AngleCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleCurve_add_AngleCurve_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __sub__(self, rhs: AngleCurve) -> AngleCurve:
        pass

    @overload
    def __sub__(self, rhs: Angle) -> AngleCurve:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case AngleCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleCurve_sub_AngleCurve_AngleCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleCurve_sub_AngleCurve_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __mul__(self, rhs: float) -> AngleCurve:
        pass

    @overload
    def __mul__(self, rhs: Curve) -> AngleCurve:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AngleCurve_mul_AngleCurve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleCurve_mul_AngleCurve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> AngleCurve:
        pass

    @overload
    def __truediv__(self, rhs: AngleCurve) -> Curve:
        pass

    @overload
    def __truediv__(self, rhs: Angle) -> Curve:
        pass

    @overload
    def __truediv__(self, rhs: Curve) -> AngleCurve:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AngleCurve_div_AngleCurve_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case AngleCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleCurve_div_AngleCurve_AngleCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Angle():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleCurve_div_AngleCurve_Angle(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve._new(output)
            case Curve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AngleCurve_div_AngleCurve_Curve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AngleCurve._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> AngleCurve:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_AngleCurve_mul_Float_AngleCurve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AngleCurve._new(output)


def _anglecurve_zero() -> AngleCurve:
    output = c_void_p()
    _lib.opensolid_AngleCurve_zero(c_void_p(), ctypes.byref(output))
    return AngleCurve._new(output)


AngleCurve.zero = _anglecurve_zero()


class Drawing2d:
    """A set of functions for constructing 2D drawings."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Drawing2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Drawing2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    black_stroke: Drawing2d.Attribute = None  # type: ignore[assignment]
    """Black stroke for curves and borders."""

    no_fill: Drawing2d.Attribute = None  # type: ignore[assignment]
    """Set shapes to have no fill."""

    @staticmethod
    def to_svg(view_box: Bounds2d, entities: list[Drawing2d.Entity]) -> str:
        """Render some entities to SVG.

        The given bounding box defines the overall size of the drawing,
        and in general should contain all the drawing entities
        (unless you *want* to crop some of them).
        """
        inputs = _Tuple2_c_void_p_List_c_void_p(
            view_box._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(entities))(*[item._ptr for item in entities]),
            ),
        )
        output = _Text()
        _lib.opensolid_Drawing2d_toSVG_Bounds2d_ListDrawing2dEntity(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return _text_to_str(output)

    @staticmethod
    def write_svg(
        path: str, view_box: Bounds2d, entities: list[Drawing2d.Entity]
    ) -> None:
        """Render SVG to a file.

        The given bounding box defines the overall size of the drawing,
        and in general should contain all the drawing entities
        (unless you *want* to crop some of them).
        """
        inputs = _Tuple3_Text_c_void_p_List_c_void_p(
            _str_to_text(path),
            view_box._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(entities))(*[item._ptr for item in entities]),
            ),
        )
        output = _Result_c_int64()
        _lib.opensolid_Drawing2d_writeSVG_Text_Bounds2d_ListDrawing2dEntity(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return None if output.field0 == 0 else _error(_text_to_str(output.field1))

    @staticmethod
    def group(entities: list[Drawing2d.Entity]) -> Drawing2d.Entity:
        """Group several entities into a single entity."""
        inputs = _list_argument(
            _List_c_void_p,
            (c_void_p * len(entities))(*[item._ptr for item in entities]),
        )
        output = c_void_p()
        _lib.opensolid_Drawing2d_group_ListDrawing2dEntity(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Drawing2d.Entity._new(output)

    @staticmethod
    def polygon(
        attributes: list[Drawing2d.Attribute], vertices: list[Point2d]
    ) -> Drawing2d.Entity:
        """Create a polygon with the given attributes and vertices."""
        inputs = _Tuple2_List_c_void_p_List_c_void_p(
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(attributes))(*[item._ptr for item in attributes]),
            ),
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(vertices))(*[item._ptr for item in vertices]),
            ),
        )
        output = c_void_p()
        _lib.opensolid_Drawing2d_polygon_ListDrawing2dAttribute_ListPoint2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Drawing2d.Entity._new(output)

    @staticmethod
    def circle(
        attributes: list[Drawing2d.Attribute],
        *,
        center_point: Point2d,
        diameter: Length,
    ) -> Drawing2d.Entity:
        """Create a circle with the given attributes, center point and diameter."""
        inputs = _Tuple3_List_c_void_p_c_void_p_c_void_p(
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(attributes))(*[item._ptr for item in attributes]),
            ),
            center_point._ptr,
            diameter._ptr,
        )
        output = c_void_p()
        _lib.opensolid_Drawing2d_circle_ListDrawing2dAttribute_Point2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Drawing2d.Entity._new(output)

    @staticmethod
    def curve(
        attributes: list[Drawing2d.Attribute], max_error: Length, curve: Curve2d
    ) -> Drawing2d.Entity:
        """Draw a curve with the given attributes and accuracy."""
        inputs = _Tuple3_List_c_void_p_c_void_p_c_void_p(
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(attributes))(*[item._ptr for item in attributes]),
            ),
            max_error._ptr,
            curve._ptr,
        )
        output = c_void_p()
        _lib.opensolid_Drawing2d_curve_ListDrawing2dAttribute_Length_Curve2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Drawing2d.Entity._new(output)

    @staticmethod
    def stroke_color(color: Color) -> Drawing2d.Attribute:
        """Set the stroke color for curves and borders."""
        inputs = color._ptr
        output = c_void_p()
        _lib.opensolid_Drawing2d_strokeColor_Color(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Drawing2d.Attribute._new(output)

    @staticmethod
    def fill_color(color: Color) -> Drawing2d.Attribute:
        """Set the fill color for shapes."""
        inputs = color._ptr
        output = c_void_p()
        _lib.opensolid_Drawing2d_fillColor_Color(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Drawing2d.Attribute._new(output)

    class Entity:
        """A drawing entity such as a shape or group."""

        _ptr: c_void_p

        @staticmethod
        def _new(ptr: c_void_p) -> Drawing2d.Entity:
            """Construct directly from an underlying C pointer."""
            obj = object.__new__(Drawing2d.Entity)
            obj._ptr = ptr
            return obj

        def __del__(self) -> None:
            """Free the underlying Haskell value."""
            _lib.opensolid_release(self._ptr)

    class Attribute:
        """A drawing attribute such as fill color or stroke width."""

        _ptr: c_void_p

        @staticmethod
        def _new(ptr: c_void_p) -> Drawing2d.Attribute:
            """Construct directly from an underlying C pointer."""
            obj = object.__new__(Drawing2d.Attribute)
            obj._ptr = ptr
            return obj

        def __del__(self) -> None:
            """Free the underlying Haskell value."""
            _lib.opensolid_release(self._ptr)


def _drawing2d_black_stroke() -> Drawing2d.Attribute:
    output = c_void_p()
    _lib.opensolid_Drawing2d_blackStroke(c_void_p(), ctypes.byref(output))
    return Drawing2d.Attribute._new(output)


Drawing2d.black_stroke = _drawing2d_black_stroke()


def _drawing2d_no_fill() -> Drawing2d.Attribute:
    output = c_void_p()
    _lib.opensolid_Drawing2d_noFill(c_void_p(), ctypes.byref(output))
    return Drawing2d.Attribute._new(output)


Drawing2d.no_fill = _drawing2d_no_fill()


class Axis2d:
    """An axis in 2D, defined by an origin point and direction."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Axis2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Axis2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    x: Axis2d = None  # type: ignore[assignment]
    """The X axis."""

    y: Axis2d = None  # type: ignore[assignment]
    """The Y axis."""

    def mirror_across(self, axis: Axis2d) -> Axis2d:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis2d_mirrorAcross_Axis2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis2d._new(output)

    def translate_by(self, displacement: Displacement2d) -> Axis2d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis2d_translateBy_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis2d._new(output)

    def translate_in(self, direction: Direction2d, distance: Length) -> Axis2d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Axis2d_translateIn_Direction2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis2d._new(output)

    def translate_along(self, axis: Axis2d, distance: Length) -> Axis2d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis2d_translateAlong_Axis2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis2d._new(output)

    def rotate_around(self, point: Point2d, angle: Angle) -> Axis2d:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis2d_rotateAround_Point2d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis2d._new(output)


def _axis2d_x() -> Axis2d:
    output = c_void_p()
    _lib.opensolid_Axis2d_x(c_void_p(), ctypes.byref(output))
    return Axis2d._new(output)


Axis2d.x = _axis2d_x()


def _axis2d_y() -> Axis2d:
    output = c_void_p()
    _lib.opensolid_Axis2d_y(c_void_p(), ctypes.byref(output))
    return Axis2d._new(output)


Axis2d.y = _axis2d_y()


class UvAxis:
    """An axis in 2D, defined by an origin point and direction."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> UvAxis:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(UvAxis)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    u: Axis2d = None  # type: ignore[assignment]
    """The U axis."""

    v: Axis2d = None  # type: ignore[assignment]
    """The V axis."""


def _uvaxis_u() -> Axis2d:
    output = c_void_p()
    _lib.opensolid_UvAxis_u(c_void_p(), ctypes.byref(output))
    return Axis2d._new(output)


UvAxis.u = _uvaxis_u()


def _uvaxis_v() -> Axis2d:
    output = c_void_p()
    _lib.opensolid_UvAxis_v(c_void_p(), ctypes.byref(output))
    return Axis2d._new(output)


UvAxis.v = _uvaxis_v()


class Vector3d:
    """A unitless vector in 3D."""

    _ptr: c_void_p

    def __init__(
        self, x_component: float, y_component: float, z_component: float
    ) -> None:
        """Construct a vector from its XYZ components."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_component, y_component, z_component
        )
        self._ptr = c_void_p()
        _lib.opensolid_Vector3d_constructor_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> Vector3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Vector3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: Vector3d = None  # type: ignore[assignment]
    """The zero vector."""

    @staticmethod
    def unit(direction: Direction3d) -> Vector3d:
        """Construct a unit vector in the given direction."""
        inputs = direction._ptr
        output = c_void_p()
        _lib.opensolid_Vector3d_unit_Direction3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    @staticmethod
    def xyz(x_component: float, y_component: float, z_component: float) -> Vector3d:
        """Construct a vector from its XYZ components."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_component, y_component, z_component
        )
        output = c_void_p()
        _lib.opensolid_Vector3d_xyz_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    @staticmethod
    def x(x_component: float) -> Vector3d:
        """Construct a vector from just an X component.

        The Y and Z components will be set to zero.
        """
        inputs = c_double(x_component)
        output = c_void_p()
        _lib.opensolid_Vector3d_x_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Vector3d._new(output)

    @staticmethod
    def y(y_component: float) -> Vector3d:
        """Construct a vector from just a Y component.

        The X and Z components will be set to zero.
        """
        inputs = c_double(y_component)
        output = c_void_p()
        _lib.opensolid_Vector3d_y_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Vector3d._new(output)

    @staticmethod
    def z(z_component: float) -> Vector3d:
        """Construct a vector from just a Z component.

        The X and Y components will be set to zero.
        """
        inputs = c_double(z_component)
        output = c_void_p()
        _lib.opensolid_Vector3d_z_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Vector3d._new(output)

    @staticmethod
    def from_components(components: tuple[float, float, float]) -> Vector3d:
        """Construct a vector from a tuple of XYZ components."""
        inputs = _Tuple3_c_double_c_double_c_double(
            components[0], components[1], components[2]
        )
        output = c_void_p()
        _lib.opensolid_Vector3d_fromComponents_Tuple3FloatFloatFloat(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    def components(self) -> tuple[float, float, float]:
        """Get the XYZ components of a vector as a tuple."""
        inputs = self._ptr
        output = _Tuple3_c_double_c_double_c_double()
        _lib.opensolid_Vector3d_components(ctypes.byref(inputs), ctypes.byref(output))
        return (output.field0, output.field1, output.field2)

    def x_component(self) -> float:
        """Get the X component of a vector."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Vector3d_xComponent(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def y_component(self) -> float:
        """Get the Y component of a vector."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Vector3d_yComponent(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def z_component(self) -> float:
        """Get the Z component of a vector."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Vector3d_zComponent(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def direction(self) -> Direction3d:
        """Attempt to get the direction of a vector.

        The current tolerance will be used to check if the vector is zero
        (and therefore does not have a direction).
        """
        inputs = _Tuple2_c_double_c_void_p(_float_tolerance(), self._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_Vector3d_direction(ctypes.byref(inputs), ctypes.byref(output))
        return (
            Direction3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def is_zero(self) -> bool:
        """Check if a vector is zero, within the current tolerance."""
        inputs = _Tuple2_c_double_c_void_p(_float_tolerance(), self._ptr)
        output = c_int64()
        _lib.opensolid_Vector3d_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def rotate_in(self, direction: Direction3d, angle: Angle) -> Vector3d:
        """Rotate a vector in a given direction.

        This is equivalent to rotating around an axis with the given direction.
        """
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, angle._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Vector3d_rotateIn_Direction3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    def rotate_around(self, axis: Axis3d, angle: Angle) -> Vector3d:
        """Rotate around the given axis by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Vector3d_rotateAround_Axis3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    def mirror_in(self, direction: Direction3d) -> Vector3d:
        """Mirror in a particular direction.

        This is equivalent to mirroring across a plane with the given normal direction.
        """
        inputs = _Tuple2_c_void_p_c_void_p(direction._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Vector3d_mirrorIn_Direction3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    def mirror_across(self, plane: Plane3d) -> Vector3d:
        """Mirror across the given plane."""
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Vector3d_mirrorAcross_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    def scale_in(self, direction: Direction3d, scale: float) -> Vector3d:
        """Scale (stretch) in the given direction by the given scaling factor.

        This is equivalent to scaling along an axis with the given direction.
        """
        inputs = _Tuple3_c_void_p_c_double_c_void_p(direction._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Vector3d_scaleIn_Direction3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    def scale_along(self, axis: Axis3d, scale: float) -> Vector3d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Vector3d_scaleAlong_Axis3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    def __neg__(self) -> Vector3d:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Vector3d_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Vector3d._new(output)

    def __add__(self, rhs: Vector3d) -> Vector3d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Vector3d_add_Vector3d_Vector3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    def __sub__(self, rhs: Vector3d) -> Vector3d:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Vector3d_sub_Vector3d_Vector3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    @overload
    def __mul__(self, rhs: float) -> Vector3d:
        pass

    @overload
    def __mul__(self, rhs: Length) -> Displacement3d:
        pass

    @overload
    def __mul__(self, rhs: Area) -> AreaVector3d:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Vector3d_mul_Vector3d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector3d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector3d_mul_Vector3d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector3d_mul_Vector3d_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case _:
                return NotImplemented

    def __truediv__(self, rhs: float) -> Vector3d:
        """Return ``self / rhs``."""
        inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
        output = c_void_p()
        _lib.opensolid_Vector3d_div_Vector3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)

    @overload
    def dot(self, rhs: Vector3d) -> float:
        pass

    @overload
    def dot(self, rhs: Displacement3d) -> Length:
        pass

    @overload
    def dot(self, rhs: AreaVector3d) -> Area:
        pass

    @overload
    def dot(self, rhs: Direction3d) -> float:
        pass

    def dot(self, rhs):
        """Compute the dot product of two vector-like values."""
        match rhs:
            case Vector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Vector3d_dot_Vector3d_Vector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Displacement3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector3d_dot_Vector3d_Displacement3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case AreaVector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector3d_dot_Vector3d_AreaVector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Direction3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Vector3d_dot_Vector3d_Direction3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case _:
                return NotImplemented

    @overload
    def cross(self, rhs: Vector3d) -> Vector3d:
        pass

    @overload
    def cross(self, rhs: Displacement3d) -> Displacement3d:
        pass

    @overload
    def cross(self, rhs: AreaVector3d) -> AreaVector3d:
        pass

    @overload
    def cross(self, rhs: Direction3d) -> Vector3d:
        pass

    def cross(self, rhs):
        """Compute the cross product of two vector-like values."""
        match rhs:
            case Vector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector3d_cross_Vector3d_Vector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector3d._new(output)
            case Displacement3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector3d_cross_Vector3d_Displacement3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case AreaVector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector3d_cross_Vector3d_AreaVector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case Direction3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Vector3d_cross_Vector3d_Direction3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector3d._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> Vector3d:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Vector3d_mul_Float_Vector3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)


def _vector3d_zero() -> Vector3d:
    output = c_void_p()
    _lib.opensolid_Vector3d_zero(c_void_p(), ctypes.byref(output))
    return Vector3d._new(output)


Vector3d.zero = _vector3d_zero()


class Displacement3d:
    """A displacement vector in 3D."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Displacement3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Displacement3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: Displacement3d = None  # type: ignore[assignment]
    """The zero vector."""

    @staticmethod
    def xyz(
        x_component: Length, y_component: Length, z_component: Length
    ) -> Displacement3d:
        """Construct a vector from its X, Y and Z components."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            x_component._ptr, y_component._ptr, z_component._ptr
        )
        output = c_void_p()
        _lib.opensolid_Displacement3d_xyz_Length_Length_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @staticmethod
    def x(x_component: Length) -> Displacement3d:
        """Construct a vector from just an X component.

        The Y and Z components will be set to zero.
        """
        inputs = x_component._ptr
        output = c_void_p()
        _lib.opensolid_Displacement3d_x_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @staticmethod
    def y(y_component: Length) -> Displacement3d:
        """Construct a vector from just a Y component.

        The X and Z components will be set to zero.
        """
        inputs = y_component._ptr
        output = c_void_p()
        _lib.opensolid_Displacement3d_y_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @staticmethod
    def z(z_component: Length) -> Displacement3d:
        """Construct a vector from just a Z component.

        The X and Y components will be set to zero.
        """
        inputs = z_component._ptr
        output = c_void_p()
        _lib.opensolid_Displacement3d_z_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @staticmethod
    def meters(
        x_component: float, y_component: float, z_component: float
    ) -> Displacement3d:
        """Construct a vector from its XYZ components given in meters."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_component, y_component, z_component
        )
        output = c_void_p()
        _lib.opensolid_Displacement3d_meters_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @staticmethod
    def centimeters(
        x_component: float, y_component: float, z_component: float
    ) -> Displacement3d:
        """Construct a vector from its XYZ components given in centimeters."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_component, y_component, z_component
        )
        output = c_void_p()
        _lib.opensolid_Displacement3d_centimeters_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @staticmethod
    def millimeters(
        x_component: float, y_component: float, z_component: float
    ) -> Displacement3d:
        """Construct a vector from its XYZ components given in millimeters."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_component, y_component, z_component
        )
        output = c_void_p()
        _lib.opensolid_Displacement3d_millimeters_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @staticmethod
    def inches(
        x_component: float, y_component: float, z_component: float
    ) -> Displacement3d:
        """Construct a vector from its XYZ components given in inches."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_component, y_component, z_component
        )
        output = c_void_p()
        _lib.opensolid_Displacement3d_inches_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @staticmethod
    def from_components(components: tuple[Length, Length, Length]) -> Displacement3d:
        """Construct a vector from a tuple of XYZ components."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            components[0]._ptr, components[1]._ptr, components[2]._ptr
        )
        output = c_void_p()
        _lib.opensolid_Displacement3d_fromComponents_Tuple3LengthLengthLength(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    def components(self) -> tuple[Length, Length, Length]:
        """Get the XYZ components of a vector as a tuple."""
        inputs = self._ptr
        output = _Tuple3_c_void_p_c_void_p_c_void_p()
        _lib.opensolid_Displacement3d_components(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Length._new(c_void_p(output.field0)),
            Length._new(c_void_p(output.field1)),
            Length._new(c_void_p(output.field2)),
        )

    def x_component(self) -> Length:
        """Get the X component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement3d_xComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def y_component(self) -> Length:
        """Get the Y component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement3d_yComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def z_component(self) -> Length:
        """Get the Z component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement3d_zComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def direction(self) -> Direction3d:
        """Attempt to get the direction of a vector.

        The current tolerance will be used to check if the vector is zero
        (and therefore does not have a direction).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_Displacement3d_direction(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Direction3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def is_zero(self) -> bool:
        """Check if a displacement is zero, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_Displacement3d_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def rotate_in(self, direction: Direction3d, angle: Angle) -> Displacement3d:
        """Rotate a vector in a given direction.

        This is equivalent to rotating around an axis with the given direction.
        """
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, angle._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Displacement3d_rotateIn_Direction3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    def rotate_around(self, axis: Axis3d, angle: Angle) -> Displacement3d:
        """Rotate around the given axis by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement3d_rotateAround_Axis3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    def mirror_in(self, direction: Direction3d) -> Displacement3d:
        """Mirror in a particular direction.

        This is equivalent to mirroring across a plane with the given normal direction.
        """
        inputs = _Tuple2_c_void_p_c_void_p(direction._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement3d_mirrorIn_Direction3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    def mirror_across(self, plane: Plane3d) -> Displacement3d:
        """Mirror across the given plane."""
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement3d_mirrorAcross_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    def scale_in(self, direction: Direction3d, scale: float) -> Displacement3d:
        """Scale (stretch) in the given direction by the given scaling factor.

        This is equivalent to scaling along an axis with the given direction.
        """
        inputs = _Tuple3_c_void_p_c_double_c_void_p(direction._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement3d_scaleIn_Direction3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    def scale_along(self, axis: Axis3d, scale: float) -> Displacement3d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement3d_scaleAlong_Axis3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    def __neg__(self) -> Displacement3d:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Displacement3d_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Displacement3d._new(output)

    def __add__(self, rhs: Displacement3d) -> Displacement3d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement3d_add_Displacement3d_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    def __sub__(self, rhs: Displacement3d) -> Displacement3d:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement3d_sub_Displacement3d_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)

    @overload
    def __mul__(self, rhs: float) -> Displacement3d:
        pass

    @overload
    def __mul__(self, rhs: Length) -> AreaVector3d:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Displacement3d_mul_Displacement3d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement3d_mul_Displacement3d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case _:
                return NotImplemented

    @overload
    def __truediv__(self, rhs: float) -> Displacement3d:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> Vector3d:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Displacement3d_div_Displacement3d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement3d_div_Displacement3d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector3d._new(output)
            case _:
                return NotImplemented

    @overload
    def dot(self, rhs: Displacement3d) -> Area:
        pass

    @overload
    def dot(self, rhs: Vector3d) -> Length:
        pass

    @overload
    def dot(self, rhs: Direction3d) -> Length:
        pass

    def dot(self, rhs):
        """Compute the dot product of two vector-like values."""
        match rhs:
            case Displacement3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement3d_dot_Displacement3d_Displacement3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Vector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement3d_dot_Displacement3d_Vector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case Direction3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement3d_dot_Displacement3d_Direction3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case _:
                return NotImplemented

    @overload
    def cross(self, rhs: Displacement3d) -> AreaVector3d:
        pass

    @overload
    def cross(self, rhs: Vector3d) -> Displacement3d:
        pass

    @overload
    def cross(self, rhs: Direction3d) -> Displacement3d:
        pass

    def cross(self, rhs):
        """Compute the cross product of two vector-like values."""
        match rhs:
            case Displacement3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement3d_cross_Displacement3d_Displacement3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case Vector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement3d_cross_Displacement3d_Vector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case Direction3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Displacement3d_cross_Displacement3d_Direction3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> Displacement3d:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Displacement3d_mul_Float_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement3d._new(output)


def _displacement3d_zero() -> Displacement3d:
    output = c_void_p()
    _lib.opensolid_Displacement3d_zero(c_void_p(), ctypes.byref(output))
    return Displacement3d._new(output)


Displacement3d.zero = _displacement3d_zero()


class AreaVector3d:
    """A vector in 3D with units of area."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> AreaVector3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(AreaVector3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: AreaVector3d = None  # type: ignore[assignment]
    """The zero vector."""

    @staticmethod
    def xyz(x_component: Area, y_component: Area, z_component: Area) -> AreaVector3d:
        """Construct a vector from its X, Y and Z components."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            x_component._ptr, y_component._ptr, z_component._ptr
        )
        output = c_void_p()
        _lib.opensolid_AreaVector3d_xyz_Area_Area_Area(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    @staticmethod
    def x(x_component: Area) -> AreaVector3d:
        """Construct a vector from just an X component.

        The Y and Z components will be set to zero.
        """
        inputs = x_component._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector3d_x_Area(ctypes.byref(inputs), ctypes.byref(output))
        return AreaVector3d._new(output)

    @staticmethod
    def y(y_component: Area) -> AreaVector3d:
        """Construct a vector from just a Y component.

        The X and Z components will be set to zero.
        """
        inputs = y_component._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector3d_y_Area(ctypes.byref(inputs), ctypes.byref(output))
        return AreaVector3d._new(output)

    @staticmethod
    def z(z_component: Area) -> AreaVector3d:
        """Construct a vector from just a Z component.

        The X and Y components will be set to zero.
        """
        inputs = z_component._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector3d_z_Area(ctypes.byref(inputs), ctypes.byref(output))
        return AreaVector3d._new(output)

    @staticmethod
    def square_meters(
        x_component: float, y_component: float, z_component: float
    ) -> AreaVector3d:
        """Construct a vector from its XYZ components given in square meters."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_component, y_component, z_component
        )
        output = c_void_p()
        _lib.opensolid_AreaVector3d_squareMeters_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    @staticmethod
    def from_components(components: tuple[Area, Area, Area]) -> AreaVector3d:
        """Construct a vector from a tuple of XYZ components."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            components[0]._ptr, components[1]._ptr, components[2]._ptr
        )
        output = c_void_p()
        _lib.opensolid_AreaVector3d_fromComponents_Tuple3AreaAreaArea(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def components(self) -> tuple[Area, Area, Area]:
        """Get the XYZ components of a vector as a tuple."""
        inputs = self._ptr
        output = _Tuple3_c_void_p_c_void_p_c_void_p()
        _lib.opensolid_AreaVector3d_components(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Area._new(c_void_p(output.field0)),
            Area._new(c_void_p(output.field1)),
            Area._new(c_void_p(output.field2)),
        )

    def x_component(self) -> Area:
        """Get the X component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector3d_xComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Area._new(output)

    def y_component(self) -> Area:
        """Get the Y component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector3d_yComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Area._new(output)

    def z_component(self) -> Area:
        """Get the Z component of a vector."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector3d_zComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Area._new(output)

    def direction(self) -> Direction3d:
        """Attempt to get the direction of a vector.

        The current tolerance will be used to check if the vector is zero
        (and therefore does not have a direction).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_area_tolerance()._ptr, self._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_AreaVector3d_direction(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Direction3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def is_zero(self) -> bool:
        """Check if an area vector is zero, within the current tolerance."""
        inputs = _Tuple2_c_void_p_c_void_p(_area_tolerance()._ptr, self._ptr)
        output = c_int64()
        _lib.opensolid_AreaVector3d_isZero(ctypes.byref(inputs), ctypes.byref(output))
        return bool(output.value)

    def rotate_in(self, direction: Direction3d, angle: Angle) -> AreaVector3d:
        """Rotate a vector in a given direction.

        This is equivalent to rotating around an axis with the given direction.
        """
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, angle._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_AreaVector3d_rotateIn_Direction3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def rotate_around(self, axis: Axis3d, angle: Angle) -> AreaVector3d:
        """Rotate around the given axis by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_rotateAround_Axis3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def mirror_in(self, direction: Direction3d) -> AreaVector3d:
        """Mirror in a particular direction.

        This is equivalent to mirroring across a plane with the given normal direction.
        """
        inputs = _Tuple2_c_void_p_c_void_p(direction._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_mirrorIn_Direction3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def mirror_across(self, plane: Plane3d) -> AreaVector3d:
        """Mirror across the given plane."""
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_mirrorAcross_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def scale_in(self, direction: Direction3d, scale: float) -> AreaVector3d:
        """Scale (stretch) in the given direction by the given scaling factor.

        This is equivalent to scaling along an axis with the given direction.
        """
        inputs = _Tuple3_c_void_p_c_double_c_void_p(direction._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_scaleIn_Direction3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def scale_along(self, axis: Axis3d, scale: float) -> AreaVector3d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_scaleAlong_Axis3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def __neg__(self) -> AreaVector3d:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_AreaVector3d_neg(ctypes.byref(inputs), ctypes.byref(output))
        return AreaVector3d._new(output)

    def __add__(self, rhs: AreaVector3d) -> AreaVector3d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_add_AreaVector3d_AreaVector3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def __sub__(self, rhs: AreaVector3d) -> AreaVector3d:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_sub_AreaVector3d_AreaVector3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    def __mul__(self, rhs: float) -> AreaVector3d:
        """Return ``self * rhs``."""
        inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_mul_AreaVector3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)

    @overload
    def __truediv__(self, rhs: float) -> AreaVector3d:
        pass

    @overload
    def __truediv__(self, rhs: Length) -> Displacement3d:
        pass

    @overload
    def __truediv__(self, rhs: Area) -> Vector3d:
        pass

    def __truediv__(self, rhs):
        """Return ``self / rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_AreaVector3d_div_AreaVector3d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector3d_div_AreaVector3d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector3d_div_AreaVector3d_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector3d._new(output)
            case _:
                return NotImplemented

    @overload
    def dot(self, rhs: Vector3d) -> Area:
        pass

    @overload
    def dot(self, rhs: Direction3d) -> Area:
        pass

    def dot(self, rhs):
        """Compute the dot product of two vector-like values."""
        match rhs:
            case Vector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector3d_dot_AreaVector3d_Vector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case Direction3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector3d_dot_AreaVector3d_Direction3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case _:
                return NotImplemented

    @overload
    def cross(self, rhs: Vector3d) -> AreaVector3d:
        pass

    @overload
    def cross(self, rhs: Direction3d) -> AreaVector3d:
        pass

    def cross(self, rhs):
        """Compute the cross product of two vector-like values."""
        match rhs:
            case Vector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector3d_cross_AreaVector3d_Vector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case Direction3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_AreaVector3d_cross_AreaVector3d_Direction3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> AreaVector3d:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_AreaVector3d_mul_Float_AreaVector3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return AreaVector3d._new(output)


def _areavector3d_zero() -> AreaVector3d:
    output = c_void_p()
    _lib.opensolid_AreaVector3d_zero(c_void_p(), ctypes.byref(output))
    return AreaVector3d._new(output)


AreaVector3d.zero = _areavector3d_zero()


class Direction3d:
    """A direction in 3D.

    This is effectively a type-safe unit vector.
    """

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Direction3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Direction3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    x: Direction3d = None  # type: ignore[assignment]
    """The X direction."""

    y: Direction3d = None  # type: ignore[assignment]
    """The Y direction."""

    z: Direction3d = None  # type: ignore[assignment]
    """The Z direction."""

    def perpendicular_direction(self) -> Direction3d:
        """Generate an arbitrary direction perpendicular to the given one."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Direction3d_perpendicularDirection(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction3d._new(output)

    def angle_to(self, other: Direction3d) -> Angle:
        """Measure the angle from one direction to another.

        The result will always be between 0 and 180 degrees.
        """
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Direction3d_angleTo_Direction3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Angle._new(output)

    def components(self) -> tuple[float, float, float]:
        """Get the XYZ components of a direction as a tuple."""
        inputs = self._ptr
        output = _Tuple3_c_double_c_double_c_double()
        _lib.opensolid_Direction3d_components(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (output.field0, output.field1, output.field2)

    def x_component(self) -> float:
        """Get the X component of a direction."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Direction3d_xComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def y_component(self) -> float:
        """Get the Y component of a direction."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Direction3d_yComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def z_component(self) -> float:
        """Get the Z component of a direction."""
        inputs = self._ptr
        output = c_double()
        _lib.opensolid_Direction3d_zComponent(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return output.value

    def rotate_in(self, direction: Direction3d, angle: Angle) -> Direction3d:
        """Rotate a direction in a given other direction.

        This is equivalent to rotating around an axis with the given direction.
        """
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, angle._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Direction3d_rotateIn_Direction3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction3d._new(output)

    def rotate_around(self, axis: Axis3d, angle: Angle) -> Direction3d:
        """Rotate around the given axis by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Direction3d_rotateAround_Axis3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction3d._new(output)

    def mirror_in(self, direction: Direction3d) -> Direction3d:
        """Mirror a direction in a given other direction.

        This is equivalent to mirroring across a plane with the given normal direction.
        """
        inputs = _Tuple2_c_void_p_c_void_p(direction._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Direction3d_mirrorIn_Direction3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction3d._new(output)

    def mirror_across(self, plane: Plane3d) -> Direction3d:
        """Mirror across the given plane."""
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Direction3d_mirrorAcross_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction3d._new(output)

    def __neg__(self) -> Direction3d:
        """Return ``-self``."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Direction3d_neg(ctypes.byref(inputs), ctypes.byref(output))
        return Direction3d._new(output)

    @overload
    def __mul__(self, rhs: float) -> Vector3d:
        pass

    @overload
    def __mul__(self, rhs: Length) -> Displacement3d:
        pass

    @overload
    def __mul__(self, rhs: Area) -> AreaVector3d:
        pass

    def __mul__(self, rhs):
        """Return ``self * rhs``."""
        match rhs:
            case float() | int():
                inputs = _Tuple2_c_void_p_c_double(self._ptr, rhs)
                output = c_void_p()
                _lib.opensolid_Direction3d_mul_Direction3d_Float(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector3d._new(output)
            case Length():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction3d_mul_Direction3d_Length(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case Area():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction3d_mul_Direction3d_Area(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case _:
                return NotImplemented

    @overload
    def dot(self, rhs: Direction3d) -> float:
        pass

    @overload
    def dot(self, rhs: Vector3d) -> float:
        pass

    @overload
    def dot(self, rhs: Displacement3d) -> Length:
        pass

    @overload
    def dot(self, rhs: AreaVector3d) -> Area:
        pass

    def dot(self, rhs):
        """Compute the dot product of two vector-like values."""
        match rhs:
            case Direction3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Direction3d_dot_Direction3d_Direction3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Vector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_double()
                _lib.opensolid_Direction3d_dot_Direction3d_Vector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return output.value
            case Displacement3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction3d_dot_Direction3d_Displacement3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Length._new(output)
            case AreaVector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction3d_dot_Direction3d_AreaVector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Area._new(output)
            case _:
                return NotImplemented

    @overload
    def cross(self, rhs: Direction3d) -> Vector3d:
        pass

    @overload
    def cross(self, rhs: Vector3d) -> Vector3d:
        pass

    @overload
    def cross(self, rhs: Displacement3d) -> Displacement3d:
        pass

    @overload
    def cross(self, rhs: AreaVector3d) -> AreaVector3d:
        pass

    def cross(self, rhs):
        """Compute the cross product of two vector-like values."""
        match rhs:
            case Direction3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction3d_cross_Direction3d_Direction3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector3d._new(output)
            case Vector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction3d_cross_Direction3d_Vector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Vector3d._new(output)
            case Displacement3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction3d_cross_Direction3d_Displacement3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case AreaVector3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Direction3d_cross_Direction3d_AreaVector3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return AreaVector3d._new(output)
            case _:
                return NotImplemented

    def __rmul__(self, lhs: float) -> Vector3d:
        """Return ``lhs * self``."""
        inputs = _Tuple2_c_double_c_void_p(lhs, self._ptr)
        output = c_void_p()
        _lib.opensolid_Direction3d_mul_Float_Direction3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector3d._new(output)


def _direction3d_x() -> Direction3d:
    output = c_void_p()
    _lib.opensolid_Direction3d_x(c_void_p(), ctypes.byref(output))
    return Direction3d._new(output)


Direction3d.x = _direction3d_x()


def _direction3d_y() -> Direction3d:
    output = c_void_p()
    _lib.opensolid_Direction3d_y(c_void_p(), ctypes.byref(output))
    return Direction3d._new(output)


Direction3d.y = _direction3d_y()


def _direction3d_z() -> Direction3d:
    output = c_void_p()
    _lib.opensolid_Direction3d_z(c_void_p(), ctypes.byref(output))
    return Direction3d._new(output)


Direction3d.z = _direction3d_z()


class Point3d:
    """A point in 3D, defined by its XYZ coordinates."""

    _ptr: c_void_p

    def __init__(
        self, x_coordinate: Length, y_coordinate: Length, z_coordinate: Length
    ) -> None:
        """Construct a point from its XYZ coordinates."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            x_coordinate._ptr, y_coordinate._ptr, z_coordinate._ptr
        )
        self._ptr = c_void_p()
        _lib.opensolid_Point3d_constructor_Length_Length_Length(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> Point3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Point3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    origin: Point3d = None  # type: ignore[assignment]
    """The point with coordinates (0,0, 0)."""

    @staticmethod
    def xyz(
        x_coordinate: Length, y_coordinate: Length, z_coordinate: Length
    ) -> Point3d:
        """Construct a point from its X, Y and Z coordinates."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            x_coordinate._ptr, y_coordinate._ptr, z_coordinate._ptr
        )
        output = c_void_p()
        _lib.opensolid_Point3d_xyz_Length_Length_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    @staticmethod
    def x(x_coordinate: Length) -> Point3d:
        """Construct a point along the X axis, with the given X coordinate."""
        inputs = x_coordinate._ptr
        output = c_void_p()
        _lib.opensolid_Point3d_x_Length(ctypes.byref(inputs), ctypes.byref(output))
        return Point3d._new(output)

    @staticmethod
    def y(y_coordinate: Length) -> Point3d:
        """Construct a point along the Y axis, with the given Y coordinate."""
        inputs = y_coordinate._ptr
        output = c_void_p()
        _lib.opensolid_Point3d_y_Length(ctypes.byref(inputs), ctypes.byref(output))
        return Point3d._new(output)

    @staticmethod
    def z(z_coordinate: Length) -> Point3d:
        """Construct a point along the Z axis, with the given Z coordinate."""
        inputs = z_coordinate._ptr
        output = c_void_p()
        _lib.opensolid_Point3d_z_Length(ctypes.byref(inputs), ctypes.byref(output))
        return Point3d._new(output)

    @staticmethod
    def meters(
        x_coordinate: float, y_coordinate: float, z_coordinate: float
    ) -> Point3d:
        """Construct a point from its X, Y and Z coordinates given in meters."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_coordinate, y_coordinate, z_coordinate
        )
        output = c_void_p()
        _lib.opensolid_Point3d_meters_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    @staticmethod
    def centimeters(
        x_coordinate: float, y_coordinate: float, z_coordinate: float
    ) -> Point3d:
        """Construct a point from its X, Y and Z coordinates given in centimeters."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_coordinate, y_coordinate, z_coordinate
        )
        output = c_void_p()
        _lib.opensolid_Point3d_centimeters_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    @staticmethod
    def millimeters(
        x_coordinate: float, y_coordinate: float, z_coordinate: float
    ) -> Point3d:
        """Construct a point from its X, Y and Z coordinates given in millimeters."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_coordinate, y_coordinate, z_coordinate
        )
        output = c_void_p()
        _lib.opensolid_Point3d_millimeters_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    @staticmethod
    def inches(
        x_coordinate: float, y_coordinate: float, z_coordinate: float
    ) -> Point3d:
        """Construct a point from its X, Y and Z coordinates given in inches."""
        inputs = _Tuple3_c_double_c_double_c_double(
            x_coordinate, y_coordinate, z_coordinate
        )
        output = c_void_p()
        _lib.opensolid_Point3d_inches_Float_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    @staticmethod
    def from_coordinates(coordinates: tuple[Length, Length, Length]) -> Point3d:
        """Construct a point from a tuple of X, Y and Z coordinates."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            coordinates[0]._ptr, coordinates[1]._ptr, coordinates[2]._ptr
        )
        output = c_void_p()
        _lib.opensolid_Point3d_fromCoordinates_Tuple3LengthLengthLength(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def coordinates(self) -> tuple[Length, Length, Length]:
        """Get the XYZ coordinates of a point as a tuple."""
        inputs = self._ptr
        output = _Tuple3_c_void_p_c_void_p_c_void_p()
        _lib.opensolid_Point3d_coordinates(ctypes.byref(inputs), ctypes.byref(output))
        return (
            Length._new(c_void_p(output.field0)),
            Length._new(c_void_p(output.field1)),
            Length._new(c_void_p(output.field2)),
        )

    def x_coordinate(self) -> Length:
        """Get the X coordinate of a point."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Point3d_xCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    def y_coordinate(self) -> Length:
        """Get the Y coordinate of a point."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Point3d_yCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    def z_coordinate(self) -> Length:
        """Get the Z coordinate of a point."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Point3d_zCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    def distance_to(self, other: Point3d) -> Length:
        """Compute the distance from one point to another."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_distanceTo_Point3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def midpoint(self, other: Point3d) -> Point3d:
        """Find the midpoint between two points."""
        inputs = _Tuple2_c_void_p_c_void_p(other._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_midpoint_Point3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def scale_along(self, axis: Axis3d, scale: float) -> Point3d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_scaleAlong_Axis3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def scale_about(self, point: Point3d, scale: float) -> Point3d:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_scaleAbout_Point3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def mirror_across(self, plane: Plane3d) -> Point3d:
        """Mirror across the given plane."""
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_mirrorAcross_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def translate_by(self, displacement: Displacement3d) -> Point3d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_translateBy_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def translate_in(self, direction: Direction3d, distance: Length) -> Point3d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Point3d_translateIn_Direction3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def translate_along(self, axis: Axis3d, distance: Length) -> Point3d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_translateAlong_Axis3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    def rotate_around(self, axis: Axis3d, angle: Angle) -> Point3d:
        """Rotate around the given axis by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_rotateAround_Axis3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)

    @overload
    def __sub__(self, rhs: Point3d) -> Displacement3d:
        pass

    @overload
    def __sub__(self, rhs: Displacement3d) -> Point3d:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case Point3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Point3d_sub_Point3d_Point3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Displacement3d._new(output)
            case Displacement3d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Point3d_sub_Point3d_Displacement3d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Point3d._new(output)
            case _:
                return NotImplemented

    def __add__(self, rhs: Displacement3d) -> Point3d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Point3d_add_Point3d_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point3d._new(output)


def _point3d_origin() -> Point3d:
    output = c_void_p()
    _lib.opensolid_Point3d_origin(c_void_p(), ctypes.byref(output))
    return Point3d._new(output)


Point3d.origin = _point3d_origin()


class Bounds3d:
    """A bounding box in 3D."""

    _ptr: c_void_p

    def __init__(
        self,
        x_coordinate: LengthRange,
        y_coordinate: LengthRange,
        z_coordinate: LengthRange,
    ) -> None:
        """Construct a bounding box from its XYZ coordinate ranges."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            x_coordinate._ptr, y_coordinate._ptr, z_coordinate._ptr
        )
        self._ptr = c_void_p()
        _lib.opensolid_Bounds3d_constructor_LengthRange_LengthRange_LengthRange(
            ctypes.byref(inputs), ctypes.byref(self._ptr)
        )

    @staticmethod
    def _new(ptr: c_void_p) -> Bounds3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Bounds3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def constant(point: Point3d) -> Bounds3d:
        """Construct a zero-size bounding box containing a single point."""
        inputs = point._ptr
        output = c_void_p()
        _lib.opensolid_Bounds3d_constant_Point3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    @staticmethod
    def from_corners(first_point: Point3d, second_point: Point3d) -> Bounds3d:
        """Construct a bounding box from two corner points."""
        inputs = _Tuple2_c_void_p_c_void_p(first_point._ptr, second_point._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_fromCorners_Point3d_Point3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    @staticmethod
    def hull(points: list[Point3d]) -> Bounds3d:
        """Construct a bounding box containing all points in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(points))(*[item._ptr for item in points]),
            )
            if points
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_Bounds3d_hull_NonEmptyPoint3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    @staticmethod
    def aggregate(bounds: list[Bounds3d]) -> Bounds3d:
        """Construct a bounding box containing all bounding boxes in the given non-empty list."""
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(bounds))(*[item._ptr for item in bounds]),
            )
            if bounds
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_Bounds3d_aggregate_NonEmptyBounds3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def coordinates(self) -> tuple[LengthRange, LengthRange, LengthRange]:
        """Get the XYZ coordinate ranges of a bounding box as a tuple."""
        inputs = self._ptr
        output = _Tuple3_c_void_p_c_void_p_c_void_p()
        _lib.opensolid_Bounds3d_coordinates(ctypes.byref(inputs), ctypes.byref(output))
        return (
            LengthRange._new(c_void_p(output.field0)),
            LengthRange._new(c_void_p(output.field1)),
            LengthRange._new(c_void_p(output.field2)),
        )

    def x_coordinate(self) -> LengthRange:
        """Get the X coordinate range of a bounding box."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Bounds3d_xCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return LengthRange._new(output)

    def y_coordinate(self) -> LengthRange:
        """Get the Y coordinate range of a bounding box."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Bounds3d_yCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return LengthRange._new(output)

    def z_coordinate(self) -> LengthRange:
        """Get the Z coordinate range of a bounding box."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Bounds3d_zCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return LengthRange._new(output)

    def scale_along(self, axis: Axis3d, scale: float) -> Bounds3d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_scaleAlong_Axis3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def scale_about(self, point: Point3d, scale: float) -> Bounds3d:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_scaleAbout_Point3d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def mirror_across(self, plane: Plane3d) -> Bounds3d:
        """Mirror across the given plane."""
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_mirrorAcross_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def translate_by(self, displacement: Displacement3d) -> Bounds3d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_translateBy_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def translate_in(self, direction: Direction3d, distance: Length) -> Bounds3d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Bounds3d_translateIn_Direction3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def translate_along(self, axis: Axis3d, distance: Length) -> Bounds3d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_translateAlong_Axis3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def rotate_around(self, axis: Axis3d, angle: Angle) -> Bounds3d:
        """Rotate around the given axis by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_rotateAround_Axis3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def __add__(self, rhs: Displacement3d) -> Bounds3d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_add_Bounds3d_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)

    def __sub__(self, rhs: Displacement3d) -> Bounds3d:
        """Return ``self - rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Bounds3d_sub_Bounds3d_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Bounds3d._new(output)


class Axis3d:
    """An axis in 3D, defined by an origin point and direction."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Axis3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Axis3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    x: Axis3d = None  # type: ignore[assignment]
    """The global X axis."""

    y: Axis3d = None  # type: ignore[assignment]
    """The global Y axis."""

    z: Axis3d = None  # type: ignore[assignment]
    """The global Z axis."""

    def origin_point(self) -> Point3d:
        """Get the origin point of an axis."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Axis3d_originPoint(ctypes.byref(inputs), ctypes.byref(output))
        return Point3d._new(output)

    def direction(self) -> Direction3d:
        """Get the direction of an axis."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Axis3d_direction(ctypes.byref(inputs), ctypes.byref(output))
        return Direction3d._new(output)

    def normal_plane(self) -> Plane3d:
        """Construct a plane normal (perpendicular) to the given axis.

        The origin point of the plane will be the origin point of the axis,
        and the normal direction of the plane will be the direction of the axis.
        The X and Y directions of the plane will be chosen arbitrarily.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Axis3d_normalPlane(ctypes.byref(inputs), ctypes.byref(output))
        return Plane3d._new(output)

    def move_to(self, point: Point3d) -> Axis3d:
        """Move an axis so that its origin point is the given point.

        The direction of the axis will remain unchanged.
        """
        inputs = _Tuple2_c_void_p_c_void_p(point._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis3d_moveTo_Point3d(ctypes.byref(inputs), ctypes.byref(output))
        return Axis3d._new(output)

    def reverse(self) -> Axis3d:
        """Reverse an axis (negate/reverse its direction).

        The origin point of the axis will remain unchanged.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Axis3d_reverse(ctypes.byref(inputs), ctypes.byref(output))
        return Axis3d._new(output)

    def mirror_across(self, plane: Plane3d) -> Axis3d:
        """Mirror across the given plane."""
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis3d_mirrorAcross_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis3d._new(output)

    def translate_by(self, displacement: Displacement3d) -> Axis3d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis3d_translateBy_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis3d._new(output)

    def translate_in(self, direction: Direction3d, distance: Length) -> Axis3d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Axis3d_translateIn_Direction3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis3d._new(output)

    def translate_along(self, axis: Axis3d, distance: Length) -> Axis3d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis3d_translateAlong_Axis3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis3d._new(output)

    def rotate_around(self, axis: Axis3d, angle: Angle) -> Axis3d:
        """Rotate around the given axis by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Axis3d_rotateAround_Axis3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Axis3d._new(output)


def _axis3d_x() -> Axis3d:
    output = c_void_p()
    _lib.opensolid_Axis3d_x(c_void_p(), ctypes.byref(output))
    return Axis3d._new(output)


Axis3d.x = _axis3d_x()


def _axis3d_y() -> Axis3d:
    output = c_void_p()
    _lib.opensolid_Axis3d_y(c_void_p(), ctypes.byref(output))
    return Axis3d._new(output)


Axis3d.y = _axis3d_y()


def _axis3d_z() -> Axis3d:
    output = c_void_p()
    _lib.opensolid_Axis3d_z(c_void_p(), ctypes.byref(output))
    return Axis3d._new(output)


Axis3d.z = _axis3d_z()


class Plane3d:
    """A plane in 3D, defined by an origin point and two perpendicular X and Y directions.

    The normal direction  of the plane is then defined as
    the cross product of its X and Y directions.
    """

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Plane3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Plane3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    xy: Plane3d = None  # type: ignore[assignment]
    """The XY plane.

    A plane whose X direction is the global X direction
    and whose Y direction is the global Y direction.
    """

    yx: Plane3d = None  # type: ignore[assignment]
    """The YX plane.

    A plane whose X direction is the global Y direction
    and whose Y direction is the global X direction.
    """

    zx: Plane3d = None  # type: ignore[assignment]
    """The ZX plane.

    A plane whose X direction is the global Z direction
    and whose Y direction is the global X direction.
    """

    xz: Plane3d = None  # type: ignore[assignment]
    """The XZ plane.

    A plane whose X direction is the global X direction
    and whose Y direction is the global Z direction.
    """

    yz: Plane3d = None  # type: ignore[assignment]
    """The YZ plane.

    A plane whose X direction is the global Y direction
    and whose Y direction is the global Z direction.
    """

    zy: Plane3d = None  # type: ignore[assignment]
    """The ZY plane.

    A plane whose X direction is the global Z direction
    and whose Y direction is the global Y direction.
    """

    @staticmethod
    def from_x_axis(axis: Axis3d) -> Plane3d:
        """Construct a plane having the given X axis.

        A perpendicular Y direction will be chosen arbitrarily.
        """
        inputs = axis._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_fromXAxis_Axis3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)

    @staticmethod
    def from_y_axis(axis: Axis3d) -> Plane3d:
        """Construct a plane having the given Y axis.

        A perpendicular X direction will be chosen arbitrarily.
        """
        inputs = axis._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_fromYAxis_Axis3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)

    def origin_point(self) -> Point3d:
        """Get the origin point of a plane.

        This is the 3D point corresponding to (0,0) in the plane's local coordinates.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_originPoint(ctypes.byref(inputs), ctypes.byref(output))
        return Point3d._new(output)

    def normal_direction(self) -> Direction3d:
        """Get the normal direction of a plane."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_normalDirection(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Direction3d._new(output)

    def normal_axis(self) -> Axis3d:
        """Construct an axis normal (perpendicular) to a plane.

        The origin point of the axis will be the origin point of the plane,
        and the direction of the axis will be the normal direction of the plane.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_normalAxis(ctypes.byref(inputs), ctypes.byref(output))
        return Axis3d._new(output)

    def xn_plane(self) -> Plane3d:
        """Construct a plane from the X and normal directions of the given plane.

        The returned plane will have the same origin point as the original plane.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_xnPlane(ctypes.byref(inputs), ctypes.byref(output))
        return Plane3d._new(output)

    def nx_plane(self) -> Plane3d:
        """Construct a plane from the normal and X directions of the given plane.

        The returned plane will have the same origin point as the original plane.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_nxPlane(ctypes.byref(inputs), ctypes.byref(output))
        return Plane3d._new(output)

    def yn_plane(self) -> Plane3d:
        """Construct a plane from the Y and normal directions of the given plane.

        The returned plane will have the same origin point as the original plane.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_ynPlane(ctypes.byref(inputs), ctypes.byref(output))
        return Plane3d._new(output)

    def ny_plane(self) -> Plane3d:
        """Construct a plane from the normal and Y directions of the given plane.

        The returned plane will have the same origin point as the original plane.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_nyPlane(ctypes.byref(inputs), ctypes.byref(output))
        return Plane3d._new(output)

    def x_direction(self) -> Direction3d:
        """Get the X direction of a plane."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_xDirection(ctypes.byref(inputs), ctypes.byref(output))
        return Direction3d._new(output)

    def y_direction(self) -> Direction3d:
        """Get the Y direction of a plane."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_yDirection(ctypes.byref(inputs), ctypes.byref(output))
        return Direction3d._new(output)

    def x_axis(self) -> Axis3d:
        """Get the X axis of a plane.

        This is an axis formed from the plane's origin point and X direction.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_xAxis(ctypes.byref(inputs), ctypes.byref(output))
        return Axis3d._new(output)

    def y_axis(self) -> Axis3d:
        """Get the Y axis of a plane.

        This is an axis formed from the plane's origin point and Y direction.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_yAxis(ctypes.byref(inputs), ctypes.byref(output))
        return Axis3d._new(output)

    def move_to(self, point: Point3d) -> Plane3d:
        """Move a plane so that its origin point is the given point.

        The orientation of the plane will remain unchanged.
        """
        inputs = _Tuple2_c_void_p_c_void_p(point._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Plane3d_moveTo_Point3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)

    def flip_x(self) -> Plane3d:
        """Reverse a plane's X direction, which also reverses the plane's normal direction."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_flipX(ctypes.byref(inputs), ctypes.byref(output))
        return Plane3d._new(output)

    def flip_y(self) -> Plane3d:
        """Reverse a plane's Y direction, which also reverses the plane's normal direction."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Plane3d_flipY(ctypes.byref(inputs), ctypes.byref(output))
        return Plane3d._new(output)

    def offset_by(self, distance: Length) -> Plane3d:
        """Offset a plane in its normal direction by the given distance."""
        inputs = _Tuple2_c_void_p_c_void_p(distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Plane3d_offsetBy_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)

    def mirror_across(self, plane: Plane3d) -> Plane3d:
        """Mirror across the given plane."""
        inputs = _Tuple2_c_void_p_c_void_p(plane._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Plane3d_mirrorAcross_Plane3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)

    def translate_by(self, displacement: Displacement3d) -> Plane3d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Plane3d_translateBy_Displacement3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)

    def translate_in(self, direction: Direction3d, distance: Length) -> Plane3d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Plane3d_translateIn_Direction3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)

    def translate_along(self, axis: Axis3d, distance: Length) -> Plane3d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Plane3d_translateAlong_Axis3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)

    def rotate_around(self, axis: Axis3d, angle: Angle) -> Plane3d:
        """Rotate around the given axis by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Plane3d_rotateAround_Axis3d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Plane3d._new(output)


def _plane3d_xy() -> Plane3d:
    output = c_void_p()
    _lib.opensolid_Plane3d_xy(c_void_p(), ctypes.byref(output))
    return Plane3d._new(output)


Plane3d.xy = _plane3d_xy()


def _plane3d_yx() -> Plane3d:
    output = c_void_p()
    _lib.opensolid_Plane3d_yx(c_void_p(), ctypes.byref(output))
    return Plane3d._new(output)


Plane3d.yx = _plane3d_yx()


def _plane3d_zx() -> Plane3d:
    output = c_void_p()
    _lib.opensolid_Plane3d_zx(c_void_p(), ctypes.byref(output))
    return Plane3d._new(output)


Plane3d.zx = _plane3d_zx()


def _plane3d_xz() -> Plane3d:
    output = c_void_p()
    _lib.opensolid_Plane3d_xz(c_void_p(), ctypes.byref(output))
    return Plane3d._new(output)


Plane3d.xz = _plane3d_xz()


def _plane3d_yz() -> Plane3d:
    output = c_void_p()
    _lib.opensolid_Plane3d_yz(c_void_p(), ctypes.byref(output))
    return Plane3d._new(output)


Plane3d.yz = _plane3d_yz()


def _plane3d_zy() -> Plane3d:
    output = c_void_p()
    _lib.opensolid_Plane3d_zy(c_void_p(), ctypes.byref(output))
    return Plane3d._new(output)


Plane3d.zy = _plane3d_zy()


class VectorCurve2d:
    """A parametric curve defining a 2D unitless vector in terms of a parameter value."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> VectorCurve2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(VectorCurve2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: VectorCurve2d = None  # type: ignore[assignment]
    """The constant zero vector."""

    @staticmethod
    def constant(value: Vector2d) -> VectorCurve2d:
        """Create a curve with a constant value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_VectorCurve2d_constant_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return VectorCurve2d._new(output)

    @staticmethod
    def xy(x_component: Curve, y_component: Curve) -> VectorCurve2d:
        """Create a curve from its X and Y component curves."""
        inputs = _Tuple2_c_void_p_c_void_p(x_component._ptr, y_component._ptr)
        output = c_void_p()
        _lib.opensolid_VectorCurve2d_xy_Curve_Curve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return VectorCurve2d._new(output)

    def evaluate(self, parameter_value: float) -> Vector2d:
        """Evaluate a curve at a given parameter value.

        The parameter value should be between 0 and 1.
        """
        inputs = _Tuple2_c_double_c_void_p(parameter_value, self._ptr)
        output = c_void_p()
        _lib.opensolid_VectorCurve2d_evaluate_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Vector2d._new(output)


def _vectorcurve2d_zero() -> VectorCurve2d:
    output = c_void_p()
    _lib.opensolid_VectorCurve2d_zero(c_void_p(), ctypes.byref(output))
    return VectorCurve2d._new(output)


VectorCurve2d.zero = _vectorcurve2d_zero()


class DisplacementCurve2d:
    """A parametric curve defining a 2D displacement vector in terms of a parameter value."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> DisplacementCurve2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(DisplacementCurve2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    zero: DisplacementCurve2d = None  # type: ignore[assignment]
    """The constant zero vector."""

    @staticmethod
    def constant(value: Displacement2d) -> DisplacementCurve2d:
        """Create a curve with a constant value."""
        inputs = value._ptr
        output = c_void_p()
        _lib.opensolid_DisplacementCurve2d_constant_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return DisplacementCurve2d._new(output)

    @staticmethod
    def xy(x_component: LengthCurve, y_component: LengthCurve) -> DisplacementCurve2d:
        """Create a curve from its X and Y component curves."""
        inputs = _Tuple2_c_void_p_c_void_p(x_component._ptr, y_component._ptr)
        output = c_void_p()
        _lib.opensolid_DisplacementCurve2d_xy_LengthCurve_LengthCurve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return DisplacementCurve2d._new(output)

    def evaluate(self, parameter_value: float) -> Displacement2d:
        """Evaluate a curve at a given parameter value.

        The parameter value should be between 0 and 1.
        """
        inputs = _Tuple2_c_double_c_void_p(parameter_value, self._ptr)
        output = c_void_p()
        _lib.opensolid_DisplacementCurve2d_evaluate_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Displacement2d._new(output)


def _displacementcurve2d_zero() -> DisplacementCurve2d:
    output = c_void_p()
    _lib.opensolid_DisplacementCurve2d_zero(c_void_p(), ctypes.byref(output))
    return DisplacementCurve2d._new(output)


DisplacementCurve2d.zero = _displacementcurve2d_zero()


class Curve2d:
    """A parametric curve in 2D space."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Curve2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Curve2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def constant(point: Point2d) -> Curve2d:
        """Create a degenerate curve that is actually just a single point."""
        inputs = point._ptr
        output = c_void_p()
        _lib.opensolid_Curve2d_constant_Point2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def xy(x_coordinate: LengthCurve, y_coordinate: LengthCurve) -> Curve2d:
        """Create a curve from its X and Y coordinate curves."""
        inputs = _Tuple2_c_void_p_c_void_p(x_coordinate._ptr, y_coordinate._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_xy_LengthCurve_LengthCurve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def line(start_point: Point2d, end_point: Point2d) -> Curve2d:
        """Create a line between two points."""
        inputs = _Tuple2_c_void_p_c_void_p(start_point._ptr, end_point._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_line_Point2d_Point2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def arc(start_point: Point2d, end_point: Point2d, swept_angle: Angle) -> Curve2d:
        """Create an arc with the given start point, end point and swept angle.

        A positive swept angle means the arc turns counterclockwise (turns to the left),
        and a negative swept angle means it turns clockwise (turns to the right).
        For example, an arc with a swept angle of positive 90 degrees
        is quarter circle that turns to the left.
        """
        inputs = _Tuple4_c_void_p_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr, start_point._ptr, end_point._ptr, swept_angle._ptr
        )
        output = c_void_p()
        _lib.opensolid_Curve2d_arc_Point2d_Point2d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def polar_arc(
        *, center_point: Point2d, radius: Length, start_angle: Angle, end_angle: Angle
    ) -> Curve2d:
        """Create an arc with the given center point, radius, start angle and end angle."""
        inputs = _Tuple4_c_void_p_c_void_p_c_void_p_c_void_p(
            center_point._ptr, radius._ptr, start_angle._ptr, end_angle._ptr
        )
        output = c_void_p()
        _lib.opensolid_Curve2d_polarArc_Point2d_Length_Angle_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def swept_arc(
        center_point: Point2d, start_point: Point2d, swept_angle: Angle
    ) -> Curve2d:
        """Create an arc with the given center point, start point and swept angle.

        The start point will be swept around the center point by the given angle.
        """
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            center_point._ptr, start_point._ptr, swept_angle._ptr
        )
        output = c_void_p()
        _lib.opensolid_Curve2d_sweptArc_Point2d_Point2d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def corner_arc(
        corner_point: Point2d,
        incoming_direction: Direction2d,
        outgoing_direction: Direction2d,
        *,
        radius: Length,
    ) -> Curve2d:
        """Create an arc for rounding off the corner between two straight lines."""
        inputs = _Tuple5_c_void_p_c_void_p_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr,
            corner_point._ptr,
            incoming_direction._ptr,
            outgoing_direction._ptr,
            radius._ptr,
        )
        output = c_void_p()
        _lib.opensolid_Curve2d_cornerArc_Point2d_Direction2d_Direction2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def circle(*, center_point: Point2d, diameter: Length) -> Curve2d:
        """Create a circle with the given center point and diameter."""
        inputs = _Tuple2_c_void_p_c_void_p(center_point._ptr, diameter._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_circle_Point2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def bezier(control_points: list[Point2d]) -> Curve2d:
        """Construct a Bezier curve from its control points.

        For example,

        > Curve2d.bezier (NonEmpty.four p1 p2 p3 p4))

        will return a cubic Bezier curve with the given four control points.
        """
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(control_points))(
                    *[item._ptr for item in control_points]
                ),
            )
            if control_points
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_Curve2d_bezier_NonEmptyPoint2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @staticmethod
    def hermite(
        start_point: Point2d,
        start_derivatives: list[Displacement2d],
        end_point: Point2d,
        end_derivatives: list[Displacement2d],
    ) -> Curve2d:
        """Construct a Bezier curve with the given endpoints and derivatives at those endpoints.

        For example,

        > Curve2d.hermite p1 [v1] p2 [v2]

        will result in a cubic spline from @p1@ to @p2@ with first derivative equal to @v1@ at @p1@ and
        first derivative equal to @v2@ at @p2@.

        The numbers of derivatives at each endpoint do not have to be equal; for example,

        > Curve2d.hermite p1 [v1] p2 []

        will result in a quadratic spline from @p1@ to @p2@ with first derivative at @p1@ equal to @v1@.

        In general, the degree of the resulting spline will be equal to 1 plus the total number of
        derivatives given.
        """
        inputs = _Tuple4_c_void_p_List_c_void_p_c_void_p_List_c_void_p(
            start_point._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(start_derivatives))(
                    *[item._ptr for item in start_derivatives]
                ),
            ),
            end_point._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(end_derivatives))(
                    *[item._ptr for item in end_derivatives]
                ),
            ),
        )
        output = c_void_p()
        _lib.opensolid_Curve2d_hermite_Point2d_ListDisplacement2d_Point2d_ListDisplacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    def start_point(self) -> Point2d:
        """Get the start point of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Curve2d_startPoint(ctypes.byref(inputs), ctypes.byref(output))
        return Point2d._new(output)

    def end_point(self) -> Point2d:
        """Get the end point of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Curve2d_endPoint(ctypes.byref(inputs), ctypes.byref(output))
        return Point2d._new(output)

    def evaluate(self, parameter_value: float) -> Point2d:
        """Evaluate a curve at a given parameter value.

        The parameter value should be between 0 and 1.
        """
        inputs = _Tuple2_c_double_c_void_p(parameter_value, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_evaluate_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Point2d._new(output)

    def derivative(self) -> DisplacementCurve2d:
        """Get the derivative of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Curve2d_derivative(ctypes.byref(inputs), ctypes.byref(output))
        return DisplacementCurve2d._new(output)

    def reverse(self) -> Curve2d:
        """Reverse a curve, so that the start point is the end point and vice versa."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Curve2d_reverse(ctypes.byref(inputs), ctypes.byref(output))
        return Curve2d._new(output)

    def x_coordinate(self) -> LengthCurve:
        """Get the X coordinate of a 2D curve as a scalar curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Curve2d_xCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return LengthCurve._new(output)

    def y_coordinate(self) -> LengthCurve:
        """Get the Y coordinate of a 2D curve as a scalar curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_Curve2d_yCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return LengthCurve._new(output)

    def scale_along(self, axis: Axis2d, scale: float) -> Curve2d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_scaleAlong_Axis2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    def scale_about(self, point: Point2d, scale: float) -> Curve2d:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_scaleAbout_Point2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    def mirror_across(self, axis: Axis2d) -> Curve2d:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_mirrorAcross_Axis2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    def translate_by(self, displacement: Displacement2d) -> Curve2d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_translateBy_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    def translate_in(self, direction: Direction2d, distance: Length) -> Curve2d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Curve2d_translateIn_Direction2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    def translate_along(self, axis: Axis2d, distance: Length) -> Curve2d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_translateAlong_Axis2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    def rotate_around(self, point: Point2d, angle: Angle) -> Curve2d:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_rotateAround_Point2d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    def __add__(self, rhs: DisplacementCurve2d) -> Curve2d:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_Curve2d_add_Curve2d_DisplacementCurve2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Curve2d._new(output)

    @overload
    def __sub__(self, rhs: DisplacementCurve2d) -> Curve2d:
        pass

    @overload
    def __sub__(self, rhs: Curve2d) -> DisplacementCurve2d:
        pass

    @overload
    def __sub__(self, rhs: Point2d) -> DisplacementCurve2d:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case DisplacementCurve2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve2d_sub_Curve2d_DisplacementCurve2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return Curve2d._new(output)
            case Curve2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve2d_sub_Curve2d_Curve2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return DisplacementCurve2d._new(output)
            case Point2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_Curve2d_sub_Curve2d_Point2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return DisplacementCurve2d._new(output)
            case _:
                return NotImplemented


class UvCurve:
    """A parametric curve in 2D space."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> UvCurve:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(UvCurve)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def constant(point: UvPoint) -> UvCurve:
        """Create a degenerate curve that is actually just a single point."""
        inputs = point._ptr
        output = c_void_p()
        _lib.opensolid_UvCurve_constant_UvPoint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def uv(u_coordinate: Curve, v_coordinate: Curve) -> UvCurve:
        """Create a curve from its X and Y coordinate curves."""
        inputs = _Tuple2_c_void_p_c_void_p(u_coordinate._ptr, v_coordinate._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_uv_Curve_Curve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def line(start_point: UvPoint, end_point: UvPoint) -> UvCurve:
        """Create a line between two points."""
        inputs = _Tuple2_c_void_p_c_void_p(start_point._ptr, end_point._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_line_UvPoint_UvPoint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def arc(start_point: UvPoint, end_point: UvPoint, swept_angle: Angle) -> UvCurve:
        """Create an arc with the given start point, end point and swept angle.

        A positive swept angle means the arc turns counterclockwise (turns to the left),
        and a negative swept angle means it turns clockwise (turns to the right).
        For example, an arc with a swept angle of positive 90 degrees
        is quarter circle that turns to the left.
        """
        inputs = _Tuple4_c_double_c_void_p_c_void_p_c_void_p(
            _float_tolerance(), start_point._ptr, end_point._ptr, swept_angle._ptr
        )
        output = c_void_p()
        _lib.opensolid_UvCurve_arc_UvPoint_UvPoint_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def polar_arc(
        *, center_point: UvPoint, radius: float, start_angle: Angle, end_angle: Angle
    ) -> UvCurve:
        """Create an arc with the given center point, radius, start angle and end angle."""
        inputs = _Tuple4_c_void_p_c_double_c_void_p_c_void_p(
            center_point._ptr, radius, start_angle._ptr, end_angle._ptr
        )
        output = c_void_p()
        _lib.opensolid_UvCurve_polarArc_UvPoint_Float_Angle_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def circle(*, center_point: UvPoint, diameter: float) -> UvCurve:
        """Create a circle with the given center point and diameter."""
        inputs = _Tuple2_c_void_p_c_double(center_point._ptr, diameter)
        output = c_void_p()
        _lib.opensolid_UvCurve_circle_UvPoint_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def swept_arc(
        center_point: UvPoint, start_point: UvPoint, swept_angle: Angle
    ) -> UvCurve:
        """Create an arc with the given center point, start point and swept angle.

        The start point will be swept around the center point by the given angle.
        """
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            center_point._ptr, start_point._ptr, swept_angle._ptr
        )
        output = c_void_p()
        _lib.opensolid_UvCurve_sweptArc_UvPoint_UvPoint_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def corner_arc(
        corner_point: UvPoint,
        incoming_direction: Direction2d,
        outgoing_direction: Direction2d,
        *,
        radius: float,
    ) -> UvCurve:
        """Create an arc for rounding off the corner between two straight lines."""
        inputs = _Tuple5_c_double_c_void_p_c_void_p_c_void_p_c_double(
            _float_tolerance(),
            corner_point._ptr,
            incoming_direction._ptr,
            outgoing_direction._ptr,
            radius,
        )
        output = c_void_p()
        _lib.opensolid_UvCurve_cornerArc_UvPoint_Direction2d_Direction2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def bezier(control_points: list[UvPoint]) -> UvCurve:
        """Construct a Bezier curve from its control points.

        For example,

        > Curve2d.bezier (NonEmpty.four p1 p2 p3 p4))

        will return a cubic Bezier curve with the given four control points.
        """
        inputs = (
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(control_points))(
                    *[item._ptr for item in control_points]
                ),
            )
            if control_points
            else _error("List is empty")
        )
        output = c_void_p()
        _lib.opensolid_UvCurve_bezier_NonEmptyUvPoint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @staticmethod
    def hermite(
        start_point: UvPoint,
        start_derivatives: list[Vector2d],
        end_point: UvPoint,
        end_derivatives: list[Vector2d],
    ) -> UvCurve:
        """Construct a Bezier curve with the given endpoints and derivatives at those endpoints.

        For example,

        > Curve2d.hermite p1 [v1] p2 [v2]

        will result in a cubic spline from @p1@ to @p2@ with first derivative equal to @v1@ at @p1@ and
        first derivative equal to @v2@ at @p2@.

        The numbers of derivatives at each endpoint do not have to be equal; for example,

        > Curve2d.hermite p1 [v1] p2 []

        will result in a quadratic spline from @p1@ to @p2@ with first derivative at @p1@ equal to @v1@.

        In general, the degree of the resulting spline will be equal to 1 plus the total number of
        derivatives given.
        """
        inputs = _Tuple4_c_void_p_List_c_void_p_c_void_p_List_c_void_p(
            start_point._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(start_derivatives))(
                    *[item._ptr for item in start_derivatives]
                ),
            ),
            end_point._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(end_derivatives))(
                    *[item._ptr for item in end_derivatives]
                ),
            ),
        )
        output = c_void_p()
        _lib.opensolid_UvCurve_hermite_UvPoint_ListVector2d_UvPoint_ListVector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    def start_point(self) -> UvPoint:
        """Get the start point of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_UvCurve_startPoint(ctypes.byref(inputs), ctypes.byref(output))
        return UvPoint._new(output)

    def end_point(self) -> UvPoint:
        """Get the end point of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_UvCurve_endPoint(ctypes.byref(inputs), ctypes.byref(output))
        return UvPoint._new(output)

    def evaluate(self, parameter_value: float) -> UvPoint:
        """Evaluate a curve at a given parameter value.

        The parameter value should be between 0 and 1.
        """
        inputs = _Tuple2_c_double_c_void_p(parameter_value, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_evaluate_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvPoint._new(output)

    def derivative(self) -> VectorCurve2d:
        """Get the derivative of a curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_UvCurve_derivative(ctypes.byref(inputs), ctypes.byref(output))
        return VectorCurve2d._new(output)

    def reverse(self) -> UvCurve:
        """Reverse a curve, so that the start point is the end point and vice versa."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_UvCurve_reverse(ctypes.byref(inputs), ctypes.byref(output))
        return UvCurve._new(output)

    def u_coordinate(self) -> Curve:
        """Get the X coordinate of a 2D curve as a scalar curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_UvCurve_uCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def v_coordinate(self) -> Curve:
        """Get the Y coordinate of a 2D curve as a scalar curve."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_UvCurve_vCoordinate(ctypes.byref(inputs), ctypes.byref(output))
        return Curve._new(output)

    def scale_along(self, axis: UvAxis, scale: float) -> UvCurve:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_scaleAlong_UvAxis_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    def scale_about(self, point: UvPoint, scale: float) -> UvCurve:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_scaleAbout_UvPoint_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    def mirror_across(self, axis: UvAxis) -> UvCurve:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_mirrorAcross_UvAxis(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    def translate_by(self, displacement: Vector2d) -> UvCurve:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_translateBy_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    def translate_in(self, direction: Direction2d, distance: float) -> UvCurve:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(direction._ptr, distance, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_translateIn_Direction2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    def translate_along(self, axis: UvAxis, distance: float) -> UvCurve:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, distance, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_translateAlong_UvAxis_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    def rotate_around(self, point: UvPoint, angle: Angle) -> UvCurve:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_rotateAround_UvPoint_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    def __add__(self, rhs: VectorCurve2d) -> UvCurve:
        """Return ``self <> rhs``."""
        inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
        output = c_void_p()
        _lib.opensolid_UvCurve_add_UvCurve_VectorCurve2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvCurve._new(output)

    @overload
    def __sub__(self, rhs: VectorCurve2d) -> UvCurve:
        pass

    @overload
    def __sub__(self, rhs: UvCurve) -> VectorCurve2d:
        pass

    @overload
    def __sub__(self, rhs: UvPoint) -> VectorCurve2d:
        pass

    def __sub__(self, rhs):
        """Return ``self - rhs``."""
        match rhs:
            case VectorCurve2d():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_UvCurve_sub_UvCurve_VectorCurve2d(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return UvCurve._new(output)
            case UvCurve():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_UvCurve_sub_UvCurve_UvCurve(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return VectorCurve2d._new(output)
            case UvPoint():
                inputs = _Tuple2_c_void_p_c_void_p(self._ptr, rhs._ptr)
                output = c_void_p()
                _lib.opensolid_UvCurve_sub_UvCurve_UvPoint(
                    ctypes.byref(inputs), ctypes.byref(output)
                )
                return VectorCurve2d._new(output)
            case _:
                return NotImplemented


class Region2d:
    """A closed 2D region (possibly with holes), defined by a set of boundary curves."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Region2d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Region2d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def bounded_by(curves: list[Curve2d]) -> Region2d:
        """Create a region bounded by the given curves.

        The curves may be given in any order,
        do not need to have consistent directions
        and can form multiple separate loops if the region has holes.
        However, the curves must not overlap or intersect (other than at endpoints)
        and there must not be any gaps between them.
        """
        inputs = _Tuple2_c_void_p_List_c_void_p(
            _length_tolerance()._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(curves))(*[item._ptr for item in curves]),
            ),
        )
        output = _Result_c_void_p()
        _lib.opensolid_Region2d_boundedBy_ListCurve2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Region2d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def rectangle(bounding_box: Bounds2d) -> Region2d:
        """Create a rectangular region.

        Fails if the given bounds are empty
        (zero area, i.e. zero width in either direction).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, bounding_box._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_Region2d_rectangle_Bounds2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Region2d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def circle(*, center_point: Point2d, diameter: Length) -> Region2d:
        """Create a circular region.

        Fails if the given dimeter is zero.
        """
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr, center_point._ptr, diameter._ptr
        )
        output = _Result_c_void_p()
        _lib.opensolid_Region2d_circle_Point2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Region2d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def polygon(points: list[Point2d]) -> Region2d:
        """Create a polygonal region from the given points.

        The last point will be connected back to the first point automatically if needed
        (you do not have to close the polygon manually, although it will still work if you do).
        """
        inputs = _Tuple2_c_void_p_List_c_void_p(
            _length_tolerance()._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(points))(*[item._ptr for item in points]),
            ),
        )
        output = _Result_c_void_p()
        _lib.opensolid_Region2d_polygon_ListPoint2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Region2d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def outer_loop(self) -> list[Curve2d]:
        """Get the list of curves forming the outer boundary of the region.

        The curves will be in counterclockwise order around the region,
        and will each be in the counterclockwise direction.
        """
        inputs = self._ptr
        output = _List_c_void_p()
        _lib.opensolid_Region2d_outerLoop(ctypes.byref(inputs), ctypes.byref(output))
        return [
            Curve2d._new(c_void_p(item))
            for item in [output.field1[index] for index in range(output.field0)]
        ]

    def inner_loops(self) -> list[list[Curve2d]]:
        """Get the lists of curves (if any) forming the holes within the region.

        The curves will be in clockwise order around each hole,
        and each curve will be in the clockwise direction.
        """
        inputs = self._ptr
        output = _List_List_c_void_p()
        _lib.opensolid_Region2d_innerLoops(ctypes.byref(inputs), ctypes.byref(output))
        return [
            [
                Curve2d._new(c_void_p(item))
                for item in [item.field1[index] for index in range(item.field0)]
            ]
            for item in [output.field1[index] for index in range(output.field0)]
        ]

    def boundary_curves(self) -> list[Curve2d]:
        """Get all boundary curves (outer boundary plus any holes) of the given region."""
        inputs = self._ptr
        output = _List_c_void_p()
        _lib.opensolid_Region2d_boundaryCurves(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return [
            Curve2d._new(c_void_p(item))
            for item in [output.field1[index] for index in range(output.field0)]
        ]

    def fillet(self, points: list[Point2d], *, radius: Length) -> Region2d:
        """Fillet a region at the given corner points, with the given radius.

        Fails if any of the given points are not actually corner points of the region
        (within the given tolerance),
        or if it is not possible to solve for a given fillet
        (e.g. if either of the adjacent edges is not long enough).
        """
        inputs = _Tuple4_c_void_p_List_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(points))(*[item._ptr for item in points]),
            ),
            radius._ptr,
            self._ptr,
        )
        output = _Result_c_void_p()
        _lib.opensolid_Region2d_fillet_ListPoint2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Region2d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def scale_along(self, axis: Axis2d, scale: float) -> Region2d:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Region2d_scaleAlong_Axis2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Region2d._new(output)

    def scale_about(self, point: Point2d, scale: float) -> Region2d:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_Region2d_scaleAbout_Point2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Region2d._new(output)

    def mirror_across(self, axis: Axis2d) -> Region2d:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Region2d_mirrorAcross_Axis2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Region2d._new(output)

    def translate_by(self, displacement: Displacement2d) -> Region2d:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Region2d_translateBy_Displacement2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Region2d._new(output)

    def translate_in(self, direction: Direction2d, distance: Length) -> Region2d:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            direction._ptr, distance._ptr, self._ptr
        )
        output = c_void_p()
        _lib.opensolid_Region2d_translateIn_Direction2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Region2d._new(output)

    def translate_along(self, axis: Axis2d, distance: Length) -> Region2d:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(axis._ptr, distance._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Region2d_translateAlong_Axis2d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Region2d._new(output)

    def rotate_around(self, point: Point2d, angle: Angle) -> Region2d:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_Region2d_rotateAround_Point2d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Region2d._new(output)


class UvRegion:
    """A closed 2D region (possibly with holes), defined by a set of boundary curves."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> UvRegion:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(UvRegion)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    unit: UvRegion = None  # type: ignore[assignment]
    """The unit square in UV space."""

    @staticmethod
    def bounded_by(curves: list[UvCurve]) -> UvRegion:
        """Create a region bounded by the given curves.

        The curves may be given in any order,
        do not need to have consistent directions
        and can form multiple separate loops if the region has holes.
        However, the curves must not overlap or intersect (other than at endpoints)
        and there must not be any gaps between them.
        """
        inputs = _Tuple2_c_double_List_c_void_p(
            _float_tolerance(),
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(curves))(*[item._ptr for item in curves]),
            ),
        )
        output = _Result_c_void_p()
        _lib.opensolid_UvRegion_boundedBy_ListUvCurve(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            UvRegion._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def rectangle(bounding_box: UvBounds) -> UvRegion:
        """Create a rectangular region.

        Fails if the given bounds are empty
        (zero area, i.e. zero width in either direction).
        """
        inputs = _Tuple2_c_double_c_void_p(_float_tolerance(), bounding_box._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_UvRegion_rectangle_UvBounds(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            UvRegion._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def circle(*, center_point: UvPoint, diameter: float) -> UvRegion:
        """Create a circular region.

        Fails if the given dimeter is zero.
        """
        inputs = _Tuple3_c_double_c_void_p_c_double(
            _float_tolerance(), center_point._ptr, diameter
        )
        output = _Result_c_void_p()
        _lib.opensolid_UvRegion_circle_UvPoint_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            UvRegion._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def outer_loop(self) -> list[UvCurve]:
        """Get the list of curves forming the outer boundary of the region.

        The curves will be in counterclockwise order around the region,
        and will each be in the counterclockwise direction.
        """
        inputs = self._ptr
        output = _List_c_void_p()
        _lib.opensolid_UvRegion_outerLoop(ctypes.byref(inputs), ctypes.byref(output))
        return [
            UvCurve._new(c_void_p(item))
            for item in [output.field1[index] for index in range(output.field0)]
        ]

    def inner_loops(self) -> list[list[UvCurve]]:
        """Get the lists of curves (if any) forming the holes within the region.

        The curves will be in clockwise order around each hole,
        and each curve will be in the clockwise direction.
        """
        inputs = self._ptr
        output = _List_List_c_void_p()
        _lib.opensolid_UvRegion_innerLoops(ctypes.byref(inputs), ctypes.byref(output))
        return [
            [
                UvCurve._new(c_void_p(item))
                for item in [item.field1[index] for index in range(item.field0)]
            ]
            for item in [output.field1[index] for index in range(output.field0)]
        ]

    def boundary_curves(self) -> list[UvCurve]:
        """Get all boundary curves (outer boundary plus any holes) of the given region."""
        inputs = self._ptr
        output = _List_c_void_p()
        _lib.opensolid_UvRegion_boundaryCurves(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return [
            UvCurve._new(c_void_p(item))
            for item in [output.field1[index] for index in range(output.field0)]
        ]

    def scale_along(self, axis: UvAxis, scale: float) -> UvRegion:
        """Scale (stretch) along the given axis by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvRegion_scaleAlong_UvAxis_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvRegion._new(output)

    def scale_about(self, point: UvPoint, scale: float) -> UvRegion:
        """Scale uniformly about the given point by the given scaling factor."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(point._ptr, scale, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvRegion_scaleAbout_UvPoint_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvRegion._new(output)

    def mirror_across(self, axis: UvAxis) -> UvRegion:
        """Mirror across the given axis."""
        inputs = _Tuple2_c_void_p_c_void_p(axis._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvRegion_mirrorAcross_UvAxis(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvRegion._new(output)

    def translate_by(self, displacement: Vector2d) -> UvRegion:
        """Translate by the given displacement."""
        inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvRegion_translateBy_Vector2d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvRegion._new(output)

    def translate_in(self, direction: Direction2d, distance: float) -> UvRegion:
        """Translate in the given direction by the given distance."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(direction._ptr, distance, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvRegion_translateIn_Direction2d_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvRegion._new(output)

    def translate_along(self, axis: UvAxis, distance: float) -> UvRegion:
        """Translate along the given axis by the given distance."""
        inputs = _Tuple3_c_void_p_c_double_c_void_p(axis._ptr, distance, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvRegion_translateAlong_UvAxis_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvRegion._new(output)

    def rotate_around(self, point: UvPoint, angle: Angle) -> UvRegion:
        """Rotate around the given point by the given angle."""
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(point._ptr, angle._ptr, self._ptr)
        output = c_void_p()
        _lib.opensolid_UvRegion_rotateAround_UvPoint_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return UvRegion._new(output)


def _uvregion_unit() -> UvRegion:
    output = c_void_p()
    _lib.opensolid_UvRegion_unit(c_void_p(), ctypes.byref(output))
    return UvRegion._new(output)


UvRegion.unit = _uvregion_unit()


class Body3d:
    """A solid body in 3D, defined by a set of boundary surfaces."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Body3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Body3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def extruded(
        sketch_plane: Plane3d, profile: Region2d, distance: LengthRange
    ) -> Body3d:
        """Create an extruded body from a sketch plane and profile."""
        inputs = _Tuple4_c_void_p_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr, sketch_plane._ptr, profile._ptr, distance._ptr
        )
        output = _Result_c_void_p()
        _lib.opensolid_Body3d_extruded_Plane3d_Region2d_LengthRange(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Body3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def revolved(
        sketch_plane: Plane3d, profile: Region2d, axis: Axis2d, angle: Angle
    ) -> Body3d:
        """Create a revolved body from a sketch plane and profile.

        Note that the revolution profile and revolution axis
        are both defined within the given sketch plane.

        A positive angle will result in a counterclockwise revolution around the axis,
        and a negative angle will result in a clockwise revolution.
        """
        inputs = _Tuple5_c_void_p_c_void_p_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr,
            sketch_plane._ptr,
            profile._ptr,
            axis._ptr,
            angle._ptr,
        )
        output = _Result_c_void_p()
        _lib.opensolid_Body3d_revolved_Plane3d_Region2d_Axis2d_Angle(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Body3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def block(bounding_box: Bounds3d) -> Body3d:
        """Create a rectangular block body.

        Fails if the given bounds are empty
        (the width, height or depth is zero).
        """
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, bounding_box._ptr)
        output = _Result_c_void_p()
        _lib.opensolid_Body3d_block_Bounds3d(ctypes.byref(inputs), ctypes.byref(output))
        return (
            Body3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def sphere(*, center_point: Point3d, diameter: Length) -> Body3d:
        """Create a sphere with the given center point and diameter.

        Fails if the diameter is zero.
        """
        inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr, center_point._ptr, diameter._ptr
        )
        output = _Result_c_void_p()
        _lib.opensolid_Body3d_sphere_Point3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Body3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def cylinder(
        start_point: Point3d, end_point: Point3d, *, diameter: Length
    ) -> Body3d:
        """Create a cylindrical body from a start point, end point and diameter.

        Fails if the cylinder length or diameter is zero.
        """
        inputs = _Tuple4_c_void_p_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr, start_point._ptr, end_point._ptr, diameter._ptr
        )
        output = _Result_c_void_p()
        _lib.opensolid_Body3d_cylinder_Point3d_Point3d_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Body3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    @staticmethod
    def cylinder_along(
        axis: Axis3d, distance: LengthRange, *, diameter: Length
    ) -> Body3d:
        """Create a cylindrical body along a given axis.

        In addition to the axis itself, you will need to provide:

        - Where along the axis the cylinder starts and ends
          (given as a range of distances along the axis).
        - The cylinder diameter.

        Failes if the cylinder length or diameter is zero.
        """
        inputs = _Tuple4_c_void_p_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr, axis._ptr, distance._ptr, diameter._ptr
        )
        output = _Result_c_void_p()
        _lib.opensolid_Body3d_cylinderAlong_Axis3d_LengthRange_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return (
            Body3d._new(c_void_p(output.field2))
            if output.field0 == 0
            else _error(_text_to_str(output.field1))
        )

    def write_stl(self, path: str, mesh_constraints: list[Mesh.Constraint]) -> None:
        """Write a body to a binary STL file, using units of millimeters."""
        inputs = _Tuple4_c_void_p_Text_List_c_void_p_c_void_p(
            _length_tolerance()._ptr,
            _str_to_text(path),
            (
                _list_argument(
                    _List_c_void_p,
                    (c_void_p * len(mesh_constraints))(
                        *[item._ptr for item in mesh_constraints]
                    ),
                )
                if mesh_constraints
                else _error("List is empty")
            ),
            self._ptr,
        )
        output = _Result_c_int64()
        _lib.opensolid_Body3d_writeSTL_Text_NonEmptyMeshConstraint(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return None if output.field0 == 0 else _error(_text_to_str(output.field1))


class Mesh:
    """Meshing-related functionality."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Mesh:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Mesh)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def max_error(error: Length) -> Mesh.Constraint:
        """Specify the maximum error/deviation of the mesh from the actual shape."""
        inputs = error._ptr
        output = c_void_p()
        _lib.opensolid_Mesh_maxError_Length(ctypes.byref(inputs), ctypes.byref(output))
        return Mesh.Constraint._new(output)

    @staticmethod
    def max_size(size: Length) -> Mesh.Constraint:
        """Specify the maximum size of any triangle in the mesh."""
        inputs = size._ptr
        output = c_void_p()
        _lib.opensolid_Mesh_maxSize_Length(ctypes.byref(inputs), ctypes.byref(output))
        return Mesh.Constraint._new(output)

    class Constraint:
        """A constraint on the quality of some mesh to be produced."""

        _ptr: c_void_p

        @staticmethod
        def _new(ptr: c_void_p) -> Mesh.Constraint:
            """Construct directly from an underlying C pointer."""
            obj = object.__new__(Mesh.Constraint)
            obj._ptr = ptr
            return obj

        def __del__(self) -> None:
            """Free the underlying Haskell value."""
            _lib.opensolid_release(self._ptr)


class Scene3d:
    """A set of functions for constructing 3D scenes."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> Scene3d:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(Scene3d)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def body(
        mesh_constraints: list[Mesh.Constraint],
        material: Scene3d.Material,
        body: Body3d,
    ) -> Scene3d.Entity:
        """Render the given body with the given material.

        The body will first be converted to a mesh using the given constraints.
        """
        inputs = _Tuple4_c_void_p_List_c_void_p_c_void_p_c_void_p(
            _length_tolerance()._ptr,
            (
                _list_argument(
                    _List_c_void_p,
                    (c_void_p * len(mesh_constraints))(
                        *[item._ptr for item in mesh_constraints]
                    ),
                )
                if mesh_constraints
                else _error("List is empty")
            ),
            material._ptr,
            body._ptr,
        )
        output = c_void_p()
        _lib.opensolid_Scene3d_body_NonEmptyMeshConstraint_Scene3dMaterial_Body3d(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Scene3d.Entity._new(output)

    @staticmethod
    def group(entities: list[Scene3d.Entity]) -> Scene3d.Entity:
        """Group several entities into a single one.

        Useful to allow multiple entities to be transformed as a group.
        """
        inputs = _list_argument(
            _List_c_void_p,
            (c_void_p * len(entities))(*[item._ptr for item in entities]),
        )
        output = c_void_p()
        _lib.opensolid_Scene3d_group_ListScene3dEntity(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Scene3d.Entity._new(output)

    @staticmethod
    def metal(base_color: Color, roughness: float) -> Scene3d.Material:
        """Create a metallic material with the given color and roughness."""
        inputs = _Tuple2_c_void_p_c_double(base_color._ptr, roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_metal_Color_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Scene3d.Material._new(output)

    @staticmethod
    def aluminum(roughness: float) -> Scene3d.Material:
        """Create an aluminum material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_aluminum_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Scene3d.Material._new(output)

    @staticmethod
    def brass(roughness: float) -> Scene3d.Material:
        """Create a brass material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_brass_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Scene3d.Material._new(output)

    @staticmethod
    def chromium(roughness: float) -> Scene3d.Material:
        """Create a chromium material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_chromium_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Scene3d.Material._new(output)

    @staticmethod
    def copper(roughness: float) -> Scene3d.Material:
        """Create a copper material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_copper_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Scene3d.Material._new(output)

    @staticmethod
    def gold(roughness: float) -> Scene3d.Material:
        """Create a gold material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_gold_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Scene3d.Material._new(output)

    @staticmethod
    def iron(roughness: float) -> Scene3d.Material:
        """Create an iron material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_iron_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Scene3d.Material._new(output)

    @staticmethod
    def nickel(roughness: float) -> Scene3d.Material:
        """Create a nickel material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_nickel_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Scene3d.Material._new(output)

    @staticmethod
    def silver(roughness: float) -> Scene3d.Material:
        """Create a silver material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_silver_Float(ctypes.byref(inputs), ctypes.byref(output))
        return Scene3d.Material._new(output)

    @staticmethod
    def titanium(roughness: float) -> Scene3d.Material:
        """Create a titanium material with the given roughness."""
        inputs = c_double(roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_titanium_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Scene3d.Material._new(output)

    @staticmethod
    def nonmetal(base_color: Color, roughness: float) -> Scene3d.Material:
        """Create a non-metallic material with the given color and roughness."""
        inputs = _Tuple2_c_void_p_c_double(base_color._ptr, roughness)
        output = c_void_p()
        _lib.opensolid_Scene3d_nonmetal_Color_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Scene3d.Material._new(output)

    @staticmethod
    def material(
        base_color: Color, *, metallic: float, roughness: float
    ) -> Scene3d.Material:
        """Create a material with the given base color, metallic factor and roughness."""
        inputs = _Tuple3_c_void_p_c_double_c_double(
            base_color._ptr, metallic, roughness
        )
        output = c_void_p()
        _lib.opensolid_Scene3d_material_Color_Float_Float(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Scene3d.Material._new(output)

    @staticmethod
    def write_glb(
        path: str, ground_plane: Plane3d, entities: list[Scene3d.Entity]
    ) -> None:
        """Write a scene to a binary glTF file.

        The given plane will be used as the ground plane, with:
        - the origin of the plane being the global origin,
        - the normal direction of the plane being the global up direction (positive Y in glTF), and
        - the positive X direction of the plane being the 'forwards' direction (positive Z in glTF).
        """
        inputs = _Tuple3_Text_c_void_p_List_c_void_p(
            _str_to_text(path),
            ground_plane._ptr,
            _list_argument(
                _List_c_void_p,
                (c_void_p * len(entities))(*[item._ptr for item in entities]),
            ),
        )
        output = _Result_c_int64()
        _lib.opensolid_Scene3d_writeGLB_Text_Plane3d_ListScene3dEntity(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return None if output.field0 == 0 else _error(_text_to_str(output.field1))

    class Entity:
        """A scene entity such as a mesh or group."""

        _ptr: c_void_p

        @staticmethod
        def _new(ptr: c_void_p) -> Scene3d.Entity:
            """Construct directly from an underlying C pointer."""
            obj = object.__new__(Scene3d.Entity)
            obj._ptr = ptr
            return obj

        def __del__(self) -> None:
            """Free the underlying Haskell value."""
            _lib.opensolid_release(self._ptr)

        def translate_by(self, displacement: Displacement3d) -> Scene3d.Entity:
            """Translate by the given displacement."""
            inputs = _Tuple2_c_void_p_c_void_p(displacement._ptr, self._ptr)
            output = c_void_p()
            _lib.opensolid_Scene3dEntity_translateBy_Displacement3d(
                ctypes.byref(inputs), ctypes.byref(output)
            )
            return Scene3d.Entity._new(output)

        def translate_in(
            self, direction: Direction3d, distance: Length
        ) -> Scene3d.Entity:
            """Translate in the given direction by the given distance."""
            inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
                direction._ptr, distance._ptr, self._ptr
            )
            output = c_void_p()
            _lib.opensolid_Scene3dEntity_translateIn_Direction3d_Length(
                ctypes.byref(inputs), ctypes.byref(output)
            )
            return Scene3d.Entity._new(output)

        def translate_along(self, axis: Axis3d, distance: Length) -> Scene3d.Entity:
            """Translate along the given axis by the given distance."""
            inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
                axis._ptr, distance._ptr, self._ptr
            )
            output = c_void_p()
            _lib.opensolid_Scene3dEntity_translateAlong_Axis3d_Length(
                ctypes.byref(inputs), ctypes.byref(output)
            )
            return Scene3d.Entity._new(output)

        def rotate_around(self, axis: Axis3d, angle: Angle) -> Scene3d.Entity:
            """Rotate around the given axis by the given angle."""
            inputs = _Tuple3_c_void_p_c_void_p_c_void_p(
                axis._ptr, angle._ptr, self._ptr
            )
            output = c_void_p()
            _lib.opensolid_Scene3dEntity_rotateAround_Axis3d_Angle(
                ctypes.byref(inputs), ctypes.byref(output)
            )
            return Scene3d.Entity._new(output)

    class Material:
        """A material applied to a mesh."""

        _ptr: c_void_p

        @staticmethod
        def _new(ptr: c_void_p) -> Scene3d.Material:
            """Construct directly from an underlying C pointer."""
            obj = object.__new__(Scene3d.Material)
            obj._ptr = ptr
            return obj

        def __del__(self) -> None:
            """Free the underlying Haskell value."""
            _lib.opensolid_release(self._ptr)


class SpurGear:
    """A metric spur gear."""

    _ptr: c_void_p

    @staticmethod
    def _new(ptr: c_void_p) -> SpurGear:
        """Construct directly from an underlying C pointer."""
        obj = object.__new__(SpurGear)
        obj._ptr = ptr
        return obj

    def __del__(self) -> None:
        """Free the underlying Haskell value."""
        _lib.opensolid_release(self._ptr)

    @staticmethod
    def metric(*, num_teeth: int, module: Length) -> SpurGear:
        """Create a metric spur gear with the given number of teeth and module."""
        inputs = _Tuple2_c_int64_c_void_p(num_teeth, module._ptr)
        output = c_void_p()
        _lib.opensolid_SpurGear_metric_Int_Length(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return SpurGear._new(output)

    def num_teeth(self) -> int:
        """Get the number of teeth of a gear."""
        inputs = self._ptr
        output = c_int64()
        _lib.opensolid_SpurGear_numTeeth(ctypes.byref(inputs), ctypes.byref(output))
        return output.value

    def module(self) -> Length:
        """Get the module of a gear."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_SpurGear_module(ctypes.byref(inputs), ctypes.byref(output))
        return Length._new(output)

    def pitch_diameter(self) -> Length:
        """Get the pitch diameter of a gear."""
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_SpurGear_pitchDiameter(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def outer_diameter(self) -> Length:
        """Get the outer diameter of a gear.

        This is equal to the pitch diameter plus twice the module.
        """
        inputs = self._ptr
        output = c_void_p()
        _lib.opensolid_SpurGear_outerDiameter(
            ctypes.byref(inputs), ctypes.byref(output)
        )
        return Length._new(output)

    def profile(self) -> list[Curve2d]:
        """Get the outer profile of a gear as a list of curves, centered at the origin.

        This is just the profile of the gear teeth themselves,
        and does not include a bore hole or anything else
        (lightening holes etc.).
        It is expected that you will combine this with
        any additional curves you want
        (likely at least one circle for a bore hole)
        and then construct a profile region from the combined set of curves
        that you can then extrude to form a gear body.
        """
        inputs = _Tuple2_c_void_p_c_void_p(_length_tolerance()._ptr, self._ptr)
        output = _List_c_void_p()
        _lib.opensolid_SpurGear_profile(ctypes.byref(inputs), ctypes.byref(output))
        return [
            Curve2d._new(c_void_p(item))
            for item in [output.field1[index] for index in range(output.field0)]
        ]


__all__ = [
    "Angle",
    "AngleCurve",
    "AngleRange",
    "Area",
    "AreaCurve",
    "AreaRange",
    "AreaVector2d",
    "AreaVector3d",
    "Axis2d",
    "Axis3d",
    "Body3d",
    "Bounds2d",
    "Bounds3d",
    "Color",
    "Curve",
    "Curve2d",
    "Direction2d",
    "Direction3d",
    "Displacement2d",
    "Displacement3d",
    "DisplacementCurve2d",
    "Drawing2d",
    "Length",
    "LengthCurve",
    "LengthRange",
    "Mesh",
    "Plane3d",
    "Point2d",
    "Point3d",
    "Range",
    "Region2d",
    "Scene3d",
    "SpurGear",
    "Tolerance",
    "UvAxis",
    "UvBounds",
    "UvCurve",
    "UvPoint",
    "UvRegion",
    "Vector2d",
    "Vector3d",
    "VectorCurve2d",
]
