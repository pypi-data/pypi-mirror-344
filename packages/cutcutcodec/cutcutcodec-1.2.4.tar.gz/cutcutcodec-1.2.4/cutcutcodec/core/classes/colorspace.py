#!/usr/bin/env python3

"""Contains all the colorspace informations."""

import logging
import typing

import sympy

from cutcutcodec.config.config import Config
from cutcutcodec.core.colorspace.cst import PRIMARIES, SYMBS, TRC


class Colorspace:
    """Structure to ensure color space consistency.

    See :py:mod:`cutcutcodec.core.colorspace` for more details and explanations.

    Attributes
    ----------
    space : str
        The main space name, one of "y'pbpr", "r'g'b'", "rgb", "xyz".
        It is defined in :py:const:`cutcutcodec.core.colorspace.cst.SYMBS`.
    primaries : str or None
        The tristimulus primaries colors name (gamut).
        All available values are the keys of :py:const:`cutcutcodec.core.colorspace.cst.PRIMARIES`,
        defined in the module :py:mod:`cutcutcodec.core.colorspace.cst`.
    symbols : tuple[sympy.Symbol, sympy.Symbol, sympy.Symbol]
        The sympy symbols used as input of the expression given by the methode ``to``.
    transfer : str or None
        The non-linear transfer function name (gamma).
        All available values are the keys of :py:const:`cutcutcodec.core.colorspace.cst.TRC`,
        defined in the module :py:mod:`cutcutcodec.core.colorspace.cst`.
    """

    def __init__(
        self,
        space: str | typing.Self,
        primaries: typing.Optional[str] = None,
        transfer: typing.Optional[str] = None,

    ):
        """Parse the colorspace.

        Parameters
        ----------
        space : Colorspace | str
            The colorspace formatted as {name}[_{colorspace}],
            with name in "y'pbpr", "r'g'b'", "rgb", "xyz" (readonly).
            When several names are given, the first matching in alphabetic order is taken.
        primaries : str, optional
            If supplied, this is given priority over ``space`` for the gamut (read and write).
        transfer : str, optional
            If supplied, this is given priority over ``space`` for the gamma (read and write).
        """
        # easy str to Colorspace cast or copy
        if isinstance(space, Colorspace):
            self.__setstate__(space.__getstate__())
            return

        # parse space
        assert isinstance(space, str), space.__class__.__name__
        space = space.lower()
        if len(spaces := [p for p in SYMBS if space.startswith(p)]) != 1:
            raise ValueError(f"failed to understand the color space {space}")
        self._space = spaces.pop()

        # parse primaries
        self._primaries = None
        if primaries is None:
            if colors := [c for c in sorted(PRIMARIES) if c in space]:
                self._primaries = colors.pop(0)
        else:
            assert isinstance(primaries, str), primaries.__class__.__name__
            self._primaries = primaries.lower()

        # parse transfer
        self._transfer = None
        if transfer is None:
            if colors := [c for c in sorted(TRC) if c in space]:
                self._transfer = colors.pop(0)
        else:
            assert isinstance(transfer, str), transfer.__class__.__name__
            self._transfer = transfer.lower()

        # verifications
        self._primaries = self._check_primaries(self._primaries)
        self._transfer = self._check_transfer(self._transfer)

    def _check_primaries(self, primaries: str) -> str:
        """Ensure primaries is provided if it is required."""
        # verification
        if self._space in {"xyz"}:
            if primaries:
                logging.warning("the given primaries %s is useless in %s", primaries, self._space)
                return None
        elif primaries is None:
            raise AttributeError(f"the primaries must be provided for the space {self._space}")
        elif primaries not in PRIMARIES:
            raise ValueError(f"the provided primaries {primaries} is no in {PRIMARIES}")
        # simplification for unicity
        if primaries is not None:
            primaries = min(p for p, t in PRIMARIES.items() if t == PRIMARIES[primaries])
        return primaries

    def _check_transfer(self, transfer: str):
        """Ensure transfer is provided if it is required."""
        # verification
        if self._space in {"xyz", "rgb"}:
            if transfer:
                logging.warning("the given transfer %s is useless in %s", transfer, self._space)
                return None
        elif transfer is None:
            raise AttributeError(f"the transfer must be provided for the space {self._space}")
        elif transfer not in TRC:
            raise ValueError(f"the provided transfer {transfer} is no in {TRC}")
        # simplification for unicity
        if transfer is not None:
            transfer = min(p for p, t in TRC.items() if str(t) == str(TRC[transfer]))
        return transfer

    @classmethod
    def from_default_target(cls) -> typing.Self:
        """Create the default y'pbpr working colorspace.

        The default primaries and transfer are taken from the attributes
        ``target_prim`` and ``target_trc``
        of the class :py:class:`cutcutcodec.config.config.Config`.

        The default value can be overwitten in the file ~/.config/cutcutcodec/conf.ini

        Examples
        --------
        >>> from cutcutcodec.core.classes.colorspace import Colorspace
        >>> Colorspace.from_default_target()
        Colorspace("y'pbpr", 'bt709', 'iec61966-2-1, iec61966_2_1')
        >>>
        """
        return cls("y'pbpr", Config().target_prim, Config().target_trc)

    @classmethod
    def from_default_target_rgb(cls) -> typing.Self:
        """Construct same as ``from_default_target`` in r'g'b' space."""
        return cls("r'g'b'", Config().target_prim, Config().target_trc)

    @classmethod
    def from_default_working(cls) -> typing.Self:
        """Create the default rgb working colorspace.

        The default primaries is taken from the attribute ``working_prim``
        of the class :py:class:`cutcutcodec.config.config.Config`.

        The default value can be overwitten in the file ~/.config/cutcutcodec/conf.ini

        Examples
        --------
        >>> from cutcutcodec.core.classes.colorspace import Colorspace
        >>> Colorspace.from_default_working()
        Colorspace('rgb', 'bt709')
        >>>
        """
        return cls("rgb", Config().working_prim, None)

    @property
    def primaries(self) -> None | str:
        """Return the gamut name."""
        return self._primaries

    @primaries.setter
    def primaries(self, primaries: str):
        """Change the primaries."""
        assert isinstance(primaries, str), primaries.__class__.__name__
        primaries = primaries.lower()
        self._primaries = self._check_primaries(primaries)

    @property
    def space(self) -> str:
        """Return the main colorspace name."""
        return self._space

    @property
    def symbols(self) -> tuple[sympy.Symbol, sympy.Symbol, sympy.Symbol]:
        """Return the space symbols."""
        return SYMBS[self._space]

    def to(
        self, dst: typing.Self | str,
    ) -> tuple[sympy.core.basic.Basic, sympy.core.basic.Basic, sympy.core.basic.Basic]:
        """Alias to :py:func:`cutcutcodec.core.colorspace.func.convert`."""
        from cutcutcodec.core.colorspace.func import convert  # pylint: disable=C0415
        return convert(self, dst)

    @property
    def transfer(self) -> None | str:
        """Return the gamut name."""
        return self._transfer

    @transfer.setter
    def transfer(self, transfer: str):
        """Change the transfer."""
        assert isinstance(transfer, str), transfer.__class__.__name__
        transfer = transfer.lower()
        self._transfer = self._check_transfer(transfer)

    def __bool__(self) -> bool:
        """Return always True."""
        return True

    def __eq__(self, other: str | typing.Self) -> bool:
        """Return True if self == other."""
        match other:
            case Colorspace():
                return self.__getstate__() == other.__getstate__()
            case str():
                return self.__getstate__() == Colorspace(other).__getstate__()
        return NotImplemented

    def __getstate__(self) -> object:
        """Serialize the colospace."""
        return (self._space, self._primaries, self._transfer)

    def __hash__(self) -> int:
        """For hash tables."""
        return hash(self.__getstate__())

    def __repr__(self) -> str:
        """Give a nice representation of self."""
        args = [self._space]
        if self._primaries is not None:
            args.append(self._primaries)
            if self._transfer is not None:
                args.append(self._transfer)
        return f"{self.__class__.__name__}({', '.join(map(repr, args))})"

    def __setstate__(self, state: object):
        """Deserialize the colorspace."""
        self._space, self._primaries, self._transfer = state
