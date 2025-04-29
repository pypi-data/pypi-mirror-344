from __future__ import annotations

__all__ = [
    "Rate",
    "RateMeta",
    "RateMixin",
]

import copy
import warnings
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterator,
)

import libsbml
import numpy as np
from typing_extensions import Self

from . import BaseModel, CompoundMixin, ParameterMixin
from .utils import (
    check_function_arity,
    convert_id_to_sbml,
    get_formatted_function_source_code,
    patch_lambda_function_name,
    warning_on_one_line,
)

if TYPE_CHECKING:
    from modelbase.typing import Array

warnings.formatwarning = warning_on_one_line  # type: ignore


class Rate:
    """A container for a rate"""

    def __init__(
        self,
        name: str,
        function: Callable[..., float],
        substrates: list[str],
        products: list[str],
        modifiers: list[str],
        dynamic_variables: list[str],
        parameters: list[str],
        reversible: bool,
        args: list[str],
    ) -> None:
        self.name = name
        self.function = function
        self.substrates = substrates
        self.products = products
        self.modifiers = modifiers
        self.parameters = parameters
        self.dynamic_variables = dynamic_variables
        self.args = args
        self.reversible = reversible

    def _check_rate_dynamic_variables(self) -> None:
        if self.reversible:
            difference = set(self.dynamic_variables).difference(
                self.substrates + self.products + self.modifiers
            )
            targets = "substrates, products or modifiers"
        else:
            difference = set(self.dynamic_variables).difference(
                self.substrates + self.modifiers
            )
            targets = "substrates or modifiers"
        if difference:
            warnings.warn(
                f"Supplied dynamic variables {difference} for rate {self.name} that aren't in {targets}"
            )

    def _check_rate_args(self) -> None:
        difference = set(self.args).difference(self.dynamic_variables + self.parameters)
        if self.reversible:
            targets = "substrates, products, modifiers or parameters"
        else:
            targets = "substrates, modifiers or parameters"
        if difference:
            warnings.warn(
                f"Supplied args {difference} for rate {self.name} that aren't in {targets}"
            )

    def check_consistency(self) -> None:
        """Check if args and arity of the rate are ok."""
        self._check_rate_dynamic_variables()
        self._check_rate_args()
        if not check_function_arity(function=self.function, arity=len(self.args)):
            warnings.warn(f"Function arity does not match args of {self.name}")

    def __repr__(self) -> str:
        return repr(self.__dict__)

    def __str__(self) -> str:
        return f"{self.function.__name__}({', '.join(self.args)}) -> {', '.join(self.products)}"

    def keys(self) -> list[str]:
        """Get all valid keys of the rate"""
        return [
            "function",
            "substrates",
            "products",
            "modifiers",
            "dynamic_variables",
            "parameters",
            "reversible",
            "args",
        ]

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __iter__(self) -> Iterator:
        yield "function", self.function
        yield "substrates", self.substrates
        yield "products", self.products
        yield "modifiers", self.modifiers
        yield "parameters", self.parameters
        yield "dynamic_variables", self.dynamic_variables
        yield "args", self.args
        yield "reversible", self.reversible

    def copy(self) -> Rate:
        """Create a copy of the rate"""
        return copy.deepcopy(self)


@dataclass
class RateMeta:
    """Meta-info container for rates."""

    common_name: str | None = None
    unit: str | None = None
    gibbs0: float | None = None
    ec: str | None = None
    database_links: dict = field(default_factory=dict)
    notes: dict = field(default_factory=dict)
    sbml_function: str | None = None
    python_function: str | None = None


class RateMixin(ParameterMixin, CompoundMixin, BaseModel):
    """Mixin adding rate functions."""

    def __init__(
        self,
        rates: dict[str, Rate] | None = None,
        functions: dict[str, Callable[..., float]] | None = None,
    ) -> None:
        self.rates: dict[str, Rate] = {}
        self.functions: dict[str, Callable[..., float]] = {}
        if rates is not None:
            self.add_rates(rates=rates)
        if functions is not None:
            self.add_functions(functions=functions)

    ##########################################################################
    # Meta Info
    ##########################################################################

    def update_rate_meta_info(self, rate: str, meta_info: dict) -> Self:
        """Update meta info of a rate.

        Parameters
        ----------
        rate : str
            Name of the rate
        meta_info : dict
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}

        """
        self.update_meta_info(component="rates", meta_info={rate: meta_info})
        return self

    ##########################################################################
    # Basic rate functions
    ##########################################################################

    def add_function(self, function_name: str, function: Callable[..., float]) -> Self:
        """Add a function to the model"""
        if function.__name__ == "<lambda>":
            patch_lambda_function_name(function=function, name=function_name)

        self.functions[function_name] = function
        return self

    def add_functions(self, functions: dict[str, Callable[..., float]]) -> Self:
        """Add multiple functions to the model"""
        for function_name, function in functions.items():
            self.add_function(function_name=function_name, function=function)
        return self

    def update_function(
        self, function_name: str, function: Callable[..., float]
    ) -> Self:
        """Update a function"""
        if function.__name__ == "<lambda>":
            patch_lambda_function_name(function=function, name=function_name)
        self.functions[function_name] = function
        return self

    def update_functions(self, functions: dict[str, Callable[..., float]]) -> Self:
        """Update multiple functions"""
        for function_name, function in functions.items():
            self.update_function(function_name, function)
        return self

    def remove_function(self, function_name: str) -> Self:
        """Remove a function from the model"""
        del self.functions[function_name]
        return self

    def remove_functions(self, function_names: list[str]) -> Self:
        """Remove multiple functions from the model"""
        for function_name in function_names:
            self.remove_function(function_name)
        return self

    def _check_rate_consistency(self, rate: Rate) -> None:
        rate.check_consistency()

    def add_rate(
        self,
        rate_name: str,
        function: Callable[..., float],
        substrates: list[str] | None = None,
        products: list[str] | None = None,
        modifiers: list[str] | None = None,
        dynamic_variables: list[str] | None = None,
        parameters: list[str] | None = None,
        reversible: bool = False,
        args: list[str] | None = None,
        check_consistency: bool = True,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Add a rate function to the model.

        The Python function will get the function arguments in the following order:
        [**substrates, **(products if reversible), **modifiers, **parameters.]

        Parameters
        ----------
        rate_name
            Name of the rate function
        function
            Python method calculating the rate equation
        substrates
            Names of the substrates
        products
            Names of the products
        modifiers
            Names of the modifiers. E.g time.
        parameters
            Names of the parameters
        reversible
            Whether the reaction is reversible.
        meta_info
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}

        Warns
        -----
        UserWarning
            If rate is already in the model

        Examples
        --------
        def mass_action(S, k1):
            return k1 * S

        m.add_reaction(
            rate_name="v1",
            function=mass_action,
            stoichiometry={"X": -1},
            parameters=["k1"],
        )

        def reversible_mass_action(S, P, k_fwd, k_bwd):
            return k_fwd * S - k_bwd * P

        m.add_reaction(
            rate_name="v2",
            function=reversible_mass_action,
            stoichiometry={"X": -1, "Y": 1},
            parameters=["k2_fwd", "k2_bwd"],
            reversible=True,
        )

        """
        if rate_name in self.rates:
            warnings.warn(f"Overwriting rate {rate_name}")
            self.remove_rate(rate_name=rate_name)

        patch_lambda_function_name(function=function, name=rate_name)

        if substrates is None:
            substrates = []
        if products is None:
            products = []
        if parameters is None:
            parameters = []
        if modifiers is None:
            modifiers = []
        if dynamic_variables is None:
            if reversible:
                dynamic_variables = substrates + products + modifiers
            else:
                dynamic_variables = substrates + modifiers
        if args is None:
            args = dynamic_variables + parameters

        rate = Rate(
            name=rate_name,
            function=function,
            parameters=parameters,
            substrates=substrates,
            products=products,
            modifiers=modifiers,
            reversible=reversible,
            dynamic_variables=dynamic_variables,
            args=args,
        )
        self.rates[rate_name] = rate

        self.meta_info.setdefault("rates", {}).setdefault(
            rate_name,
            RateMeta(**meta_info),  # type: ignore
        )

        if check_consistency:
            self._check_rate_consistency(rate)
        return self

    def add_rates(
        self,
        rates: dict[str, Any],
        meta_info: dict[str, Any] | None = None,
    ) -> Self:
        """Add multiple rates to the model.

        See Also
        --------
        add_rate

        """
        meta_info = {} if meta_info is None else meta_info
        for rate_name, rate in rates.items():
            info = meta_info.get(rate_name, {})
            self.add_rate(rate_name=rate_name, **rate, **info)
        return self

    def update_rate(
        self,
        rate_name: str,
        function: Callable[..., float] | None = None,
        substrates: list[str] | None = None,
        products: list[str] | None = None,
        modifiers: list[str] | None = None,
        parameters: list[str] | None = None,
        reversible: bool | None = None,
        dynamic_variables: list[str] | None = None,
        args: list[str] | None = None,
        check_consistency: bool = True,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Update an existing rate.

        Parameters
        ----------
        rate_name
            Name of the rate function
        function
            Python method calculating the rate equation
        substrates
            Names of the substrates
        products
            Names of the products
        modifiers
            Names of the modifiers. E.g time.
        parameters
            Names of the parameters
        reversible
            Whether the reaction is reversible.
        meta_info
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}

        See Also
        --------
        add_rate

        """
        rate = self.rates[rate_name]
        reversible_changed = False
        args_have_changed = False

        if function is not None:
            patch_lambda_function_name(function=function, name=rate_name)
            rate.function = function

        if substrates is not None:
            args_have_changed = True
            rate.substrates = substrates
        else:
            substrates = rate.substrates

        if products is not None:
            args_have_changed = True
            rate.products = products
        else:
            products = rate.products

        if parameters is not None:
            args_have_changed = True
            rate.parameters = parameters
        else:
            parameters = rate.parameters

        if modifiers is not None:
            args_have_changed = True
            rate.modifiers = modifiers
        else:
            modifiers = rate.modifiers

        if reversible is not None:
            reversible_changed = True
            rate.reversible = reversible
        else:
            reversible = rate.reversible

        if dynamic_variables is not None:
            args_have_changed = True
            rate.dynamic_variables = dynamic_variables
        elif reversible_changed or args_have_changed:
            if rate.reversible:
                dynamic_variables = substrates + products + modifiers
            else:
                dynamic_variables = substrates + modifiers
            rate.dynamic_variables = dynamic_variables
        else:
            dynamic_variables = rate.dynamic_variables

        if args is not None:
            dynamic_variables = [i for i in args if i in rate.dynamic_variables]
            rate.dynamic_variables = dynamic_variables
            rate.args = args
        elif reversible_changed or args_have_changed:
            args = dynamic_variables + parameters
            rate.args = args
        else:
            args = rate.args

        if check_consistency:
            self._check_rate_consistency(rate)
        self.update_rate_meta_info(rate_name, meta_info)
        return self

    def update_rates(
        self,
        rates: dict,
        meta_info: dict[str, Any] | None = None,
    ) -> Self:
        """Update multiple rates."""
        meta_info = {} if meta_info is None else meta_info
        for rate_name, rate in rates.items():
            info = meta_info.get(rate_name, {})
            self.update_rate(rate_name, **rate, **info)
        return self

    def remove_rate(self, rate_name: str) -> Self:
        """Remove a rate function from the model.

        Parameters
        ----------
        rate_name : str
            Name of the rate

        """
        del self.rates[rate_name]
        return self

    def remove_rates(self, rate_names: list[str]) -> Self:
        """Remove multiple rate functions from the model.

        Parameters
        ----------
        rate_names : iterable(str)
            Names of the rates

        """
        for rate_name in rate_names:
            self.remove_rate(rate_name=rate_name)
        return self

    def get_rate_names(self) -> list[str]:
        """Return all rate names."""
        return list(self.rates)

    def get_rate_function(self, rate_name: str) -> Callable[..., float]:
        """Get the function of a rate."""
        return self.rates[rate_name].function

    def get_rate_parameters(self, rate_name: str) -> list[str]:
        """Get the parameters of a rate."""
        return list(self.rates[rate_name].parameters)

    def get_rate_substrates(self, rate_name: str) -> list[str]:
        """Get the substrates of a rate."""
        return list(self.rates[rate_name].substrates)

    def get_rate_products(self, rate_name: str) -> list[str]:
        """Get the products of a rate."""
        return list(self.rates[rate_name].products)

    def get_rate_modifiers(self, rate_name: str) -> list[str]:
        """Get the modifiers of a rate."""
        return list(self.rates[rate_name].modifiers)

    def get_rate_dynamic_variables(self, rate_name: str) -> list[str]:
        """Get the dynamic variables of a rate."""
        return list(self.rates[rate_name].dynamic_variables)

    def get_rate_args(self, rate_name: str) -> list[str]:
        """Get the rate function arguments of a rate."""
        return list(self.rates[rate_name].args)

    def get_rate_names_containing(self, component: str) -> list[str]:
        return [name for name, rate in self.rates.items() if component in rate.args]

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def _get_fluxes(
        self,
        *,
        fcd: dict[str, float],
    ) -> dict[str, float]:
        # args = self.parameters | fcd # python 3.9+ syntax
        args = {**self.get_all_parameters(), **fcd}
        fluxes = {}
        for name, rate in self.rates.items():
            try:
                fluxes[name] = float(rate.function(*(args[arg] for arg in rate.args)))
            except KeyError as e:
                msg = f"Could not find argument {e} for rate {name}"
                raise KeyError(msg) from e
        return fluxes

    def _get_fluxes_array(
        self,
        *,
        fcd: dict[str, float],
    ) -> dict[str, Array]:
        # args = self.parameters | fcd # python 3.9+ syntax
        args = {**self.get_all_parameters(), **fcd}
        fluxes = {}
        for name, rate in self.rates.items():
            try:
                fluxes[name] = np.atleast_1d(
                    rate.function(*(args[arg] for arg in rate.args))
                )
            except KeyError as e:
                msg = f"Could not find argument {e} for rate {name}"
                raise KeyError(msg) from e
        return fluxes

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_function_source_code(self) -> str:
        function_strings = []
        for name, function in self.functions.items():
            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="function"
            )
            function_strings.append(function_code)
        return "\n".join(sorted(function_strings))

    def _generate_rates_source_code(
        self, *, include_meta_info: bool = True
    ) -> tuple[str, str]:
        """Generate modelbase source code for rates.

        See Also
        --------
        generate_model_source_code

        """
        rate_functions = set()
        rates = []

        for name, rate in self.rates.items():
            function = rate.function
            substrates = rate.substrates
            products = rate.products
            modifiers = rate.modifiers
            parameters = rate.parameters
            reversible = rate.reversible
            args = rate.args

            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="rate"
            )
            rate_functions.add(function_code)
            rate_definition = (
                "m.add_rate(\n"
                f"    rate_name={name!r},\n"
                f"    function={function.__name__},\n"
                f"    substrates={substrates},\n"
                f"    products={products},\n"
                f"    modifiers={modifiers},\n"
                f"    parameters={parameters},\n"
                f"    reversible={reversible},\n"
                f"    args={args},\n"
            )
            if include_meta_info:
                meta_info = self._get_nonzero_meta_info(component="rates")
                try:
                    info = meta_info[name]
                    rate_definition += f"    **{info}\n"
                except KeyError:
                    pass
            rate_definition += ")"
            rates.append(rate_definition)
        return "\n".join(sorted(rate_functions)), "\n".join(rates)

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_rates(self, *, sbml_model: libsbml.Model) -> None:
        """Convert the rates into sbml reactions.

        Parameters
        ----------
        sbml_model : libsbml.Model

        """
        for rate_id, rate in self.rates.items():
            meta_info = self.meta_info["rates"][rate_id]

            rxn = sbml_model.createReaction()
            rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))
            name = meta_info.common_name
            if name:
                rxn.setName(name)
            rxn.setFast(False)
            rxn.setReversible(rate.reversible)

            substrates: defaultdict[str, int] = defaultdict(int)
            products: defaultdict[str, int] = defaultdict(int)
            for compound in rate.substrates:
                substrates[compound] += 1
            for compound in rate.products:
                products[compound] += 1

            for compound, stoichiometry in substrates.items():
                sref = rxn.createReactant()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))
                sref.setStoichiometry(stoichiometry)
                sref.setConstant(False)

            for compound, stoichiometry in products.items():
                sref = rxn.createProduct()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))
                sref.setStoichiometry(stoichiometry)
                sref.setConstant(False)

            for compound in rate.modifiers:
                sref = rxn.createModifier()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))

            function = meta_info.sbml_function
            if function is not None:
                kinetic_law = rxn.createKineticLaw()
                kinetic_law.setMath(libsbml.parseL3Formula(function))
