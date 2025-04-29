import decimal
from collections import OrderedDict
from copy import copy
from typing import Any, Iterable, NotRequired, Optional, TypedDict

from pyetr.atoms.terms import ArbitraryObject, OpenTerm, Term, get_open_equivalent
from pyetr.atoms.terms.function import Function, NumFunc
from pyetr.dependency import (
    Dependency,
    DependencyRelation,
    dependencies_from_sets,
    dependencies_to_sets,
)

Universal = ArbitraryObject
Existential = ArbitraryObject


class ParsingError(Exception):
    def __init__(self, msg: str) -> None:  # pragma: not covered
        """
        Error in the parsing process

        Args:
            message (str): Reason for error
        """
        super().__init__(msg)


def check_brackets(s: str) -> Optional[tuple[str, int] | tuple[str, int, int]]:
    stack = []
    bracket_map = {")": "(", "]": "[", "}": "{"}
    open_brackets = set(bracket_map.values())
    inv_bracket_map = {v: k for k, v in bracket_map.items()}
    for i, char in enumerate(s):
        if char in open_brackets:  # is open
            stack.append((char, i))
        elif char in bracket_map:  # is close
            if stack and stack[-1][0] == bracket_map[char]:
                stack.pop()
            else:
                if stack:
                    last_bracket_added = stack[-1][0]
                    last_bracket_pos = stack[-1][1]
                    expected_close = inv_bracket_map[last_bracket_added]
                    return (
                        f"Expected '{expected_close}' for open at char {last_bracket_pos} but received '{char}' at char {i}",
                        i,
                        last_bracket_pos,
                    )
                else:
                    return f"Unmatched closing bracket '{char}' at position {i}", i

    if stack:
        unmatched = stack[-1]
        return (
            f"Unmatched opening bracket '{unmatched[0]}' at position {unmatched[1]}",
            unmatched[1],
        )

    return None


class Variable:
    """
    Representation of a variable in parser form.
    """

    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Variable name={self.name}>"

    def to_string(self, **kwargs: Any) -> str:
        return self.name

    @classmethod
    def from_pyparsing(cls, t: Any):
        return cls(t[0])

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        if self.name in name_mappings:
            return name_mappings[self.name]
        else:
            return self.name


class Quantified:
    """
    Represents a quantifier and variable pair in parser form.
    """

    variable: Variable
    quantifier: str

    def __init__(self, variable: Variable, quantifier: str) -> None:
        if quantifier == "A":
            self.quantifier = "∀"
        elif quantifier == "E":
            self.quantifier = "∃"
        else:
            self.quantifier = quantifier
        self.variable = variable

    def __repr__(self) -> str:
        return f"<Quantified variable={self.variable} quantifier={self.quantifier}>"

    def to_string(self, **kwargs: Any) -> str:
        return self.quantifier + self.variable.to_string(**kwargs)

    def to_english(self, name_mappings: dict[str, str], **kwargs: Any) -> str:
        raise ValueError("Cannot call directly")

    @classmethod
    def from_pyparsing(cls, t: Any):
        variables = t[0].variables
        assert len(variables) == 1
        quantifier = t[0].quantifier
        variable = variables[0]
        return cls(variable, quantifier)


def get_variable_map_and_dependencies(
    quantifieds: list[Quantified],
) -> tuple[dict[str, ArbitraryObject], DependencyRelation]:
    """
    Get the variable map and dependency relation based on a list of quantifiers.

    Args:
        quantifieds (list[Quantified]): A list of quantifier and variable pairs.

    Returns:
        tuple[dict[str, ArbitraryObject], DependencyRelation]: The tuple is formed of two parts:
            dict[str, ArbitraryObject]: The variable map
            DependencyRelation: The dependency relation.
    """
    variable_map: dict[str, ArbitraryObject] = {}
    encountered_universals: list[tuple[Universal, set[Existential]]] = []
    existentials: set[Existential] = set()
    universals: set[Universal] = set()
    for quantified in quantifieds:
        if quantified.quantifier == "∃":
            arb_obj = ArbitraryObject(name=quantified.variable.name)
            existentials.add(arb_obj)
            for _, exi_set in encountered_universals:
                exi_set.add(arb_obj)
        else:
            arb_obj = ArbitraryObject(name=quantified.variable.name)
            universals.add(arb_obj)
            encountered_universals.append((arb_obj, set()))

        if quantified.variable.name not in variable_map:
            variable_map[quantified.variable.name] = arb_obj
        else:
            raise ParsingError(
                f"Variable {quantified.variable.name} appears twice in quantifiers"
            )

    return variable_map, DependencyRelation(
        universals=universals,
        existentials=existentials,
        dependencies=dependencies_from_sets(encountered_universals),
    )


def merge_terms_with_opens(
    terms: list[Term], open_term_sets: list[list[tuple[Term, OpenTerm]]]
) -> list[tuple[Term, list[OpenTerm]]]:
    """
    Combines a list of terms from inside an object, and combines them

    Args:
        terms (list[Term]): A list of terms inside an atom [A, B]
        open_term_sets (list[list[tuple[Term, OpenTerm]]]): The open terms associated with
        each as here: [[(A, openA1), (A, openA2)],[(B, openB1)]]

    Returns:
        list[tuple[Term, list[OpenTerm]]]: The merged form:
            [(A, [openA1, B]), (A, [openA2, B]), (B, [A, openB1])]
    """
    new_terms = [get_open_equivalent(t) for t in terms]
    new_terms_sets: list[tuple[Term, list[OpenTerm]]] = []
    for i, open_terms in enumerate(open_term_sets):
        if len(open_terms) > 0:
            for t, open_term in open_terms:
                fresh_terms = copy(new_terms)
                fresh_terms[i] = open_term
                new_terms_sets.append((t, fresh_terms))
    return new_terms_sets


def order_quantifieds(
    unordered_quantifieds: OrderedDict[str, Quantified], dependencies: list[Dependency]
) -> list[Quantified]:
    """
    Order the quantifieds based on the dependencies

    Args:
        unordered_quantifieds (OrderedDict[str, Quantified]): a mapping from name to Quantified
        dependencies (frozenset[Dependency]): The dependencies from the dependency relation

    Returns:
        list[Quantified]: An ordered list of quantified.
    """
    # All unspecified exis get put to the front
    # The ordering is based on the right most having the least
    # restrictions, then moving left with more and more deps
    # Therefore, we must start with the smallest exi sets
    exis_used: list[str] = []
    univs_used: list[str] = []
    dep_sets = dependencies_to_sets(dependencies)
    sorted_universals: list[tuple[int, ArbitraryObject, set[ArbitraryObject]]] = sorted(
        [(len(exi_set), uni, exi_set) for uni, exi_set in dep_sets],
        key=lambda tup: tup[0],
    )
    final_out: list[Quantified] = []
    for _, uni, exi_set in sorted_universals:
        # Fill list from the front
        new_exis: list[Quantified] = []
        for exi in sorted(exi_set, key=str):
            if exi.name not in exis_used:
                exis_used.append(exi.name)
                new_exis.append(unordered_quantifieds[exi.name])
        univs_used.append(uni.name)
        final_out = [unordered_quantifieds[uni.name], *new_exis, *final_out]

    for name, quantified in sorted(unordered_quantifieds.items()):
        if quantified.quantifier == "∃":
            if name not in exis_used:
                final_out.insert(0, quantified)
        elif quantified.quantifier == "∀":
            if name not in univs_used:
                final_out.append(quantified)
        else:
            assert False

    # continued sections must be sorted
    if len(final_out) > 0:
        new_final_out: list[Quantified] = []
        prev_quant = final_out[0].quantifier
        current_section: list[Quantified] = [final_out[0]]
        for quant in final_out[1:]:
            current_quant = quant.quantifier
            if prev_quant != current_quant:
                new_final_out += sorted(current_section, key=str)
                current_section = [quant]
                prev_quant = current_quant
            else:
                current_section.append(quant)
        new_final_out += sorted(current_section, key=str)
        return new_final_out
    else:
        return final_out


def get_quantifiers(dependency_relation: DependencyRelation) -> list[Quantified]:
    """
    Gets the list of quantifieds based on the dependency relation

    Args:
        dependency_relation (DependencyRelation): The dependency relation.

    Returns:
        list[Quantified]: The ordered quantifiers.
    """
    unordered_quantifieds: OrderedDict[str, Quantified] = OrderedDict()
    for exi in dependency_relation.ordered_exis():
        if exi.name not in unordered_quantifieds:
            unordered_quantifieds[exi.name] = Quantified(
                variable=Variable(name=exi.name), quantifier="∃"
            )
    for uni in dependency_relation.ordered_unis():
        if uni.name not in unordered_quantifieds:
            unordered_quantifieds[uni.name] = Quantified(
                variable=Variable(name=uni.name), quantifier="∀"
            )
    return order_quantifieds(unordered_quantifieds, dependency_relation.ordered_deps())


def funcs_converter(f_iter: Iterable[Function | NumFunc]) -> list[Function]:
    output: list[Function] = []
    for f in f_iter:
        if isinstance(f, Function):
            output.append(f)
        else:
            output.append(Function.numeric(f))
    return output


ctx = decimal.Context()
ctx.prec = 20


def convert_float_to_dec(f: float, round_ints: bool) -> str | int:
    """
    Converts a float to decimal form.

    Args:
        f (float): The float to convert
        round_ints (bool): Whether to round integers or not

    Returns:
        str | int: The converted form
    """
    if round_ints:
        if round(f) == f:
            return round(f)
        else:
            return format(ctx.create_decimal(repr(f)), "f")
    else:
        return format(ctx.create_decimal(repr(f)), "f")


class StringConversion(TypedDict):
    round_ints: NotRequired[bool]
