from __future__ import annotations

import typing

from pyetr.atoms import OpenPredicateAtom, PredicateAtom
from pyetr.atoms.terms import (
    ArbitraryObject,
    FunctionalTerm,
    OpenFunctionalTerm,
    OpenTerm,
    QuestionMark,
    RealNumber,
    Term,
)
from pyetr.issues import IssueStructure
from pyetr.parsing.common import get_quantifiers
from pyetr.stateset import SetOfStates

from .items import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Falsum,
    Implies,
    Item,
    LogicEmphasis,
    LogicPredicate,
    LogicReal,
    Truth,
    Variable,
)

if typing.TYPE_CHECKING:
    from pyetr.view import View


class FOLNotSupportedError(Exception):
    """
    Used for errors where the first order logic parser does not support a view.
    """

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


def convert_term(term: Term, open_terms: list[tuple[Term, OpenTerm]]) -> Item:
    """
    Used to convert a term and list of open terms back into an item.

    Args:
        term (Term): The term to convert.
        open_terms (list[tuple[Term, OpenTerm]]): The list of open terms relevant to
            the term.

    Returns:
        Item: The term in item form.
    """
    if any([isinstance(o, QuestionMark) for _, o in open_terms]):
        remaining_terms = [
            (t, o) for t, o in open_terms if not isinstance(o, QuestionMark)
        ]
        return LogicEmphasis(arg=convert_term(term, remaining_terms))
    if isinstance(term, FunctionalTerm):
        new_subterms: list[Item] = []
        for i, subterm in enumerate(term.t):
            rel_open_terms: list[tuple[Term, OpenTerm]] = []
            for t, o in open_terms:
                assert isinstance(o, OpenFunctionalTerm)
                assert isinstance(o.t, tuple)
                rel_open_terms.append((t, o.t[i]))
            new_subterms.append(convert_term(subterm, rel_open_terms))
        if isinstance(term.f, RealNumber):
            return LogicReal(num=term.f.num)
        return LogicPredicate(name=term.f.name, args=new_subterms)

    elif isinstance(term, ArbitraryObject):
        return Variable(term.name)
    else:
        raise ValueError(f"Invalid term {term} provided")


def convert_atom(
    atom: PredicateAtom,
    issue_structure: IssueStructure,
    issue_atoms: list[PredicateAtom],
) -> LogicPredicate | BoolNot:
    """
    Converts predicate atom and related issues into Item

    Args:
        atom (PredicateAtom): The predicate atom to convert.
        issue_structure (IssueStructure): The issue structure
        issue_atoms (list[PredicateAtom]): The relevant issue atoms

    Returns:
        LogicPredicate | BoolNot: The converted atom
    """
    open_atoms: list[tuple[Term, OpenPredicateAtom]] = []
    for i, (term, open_atom) in enumerate(issue_structure.sorted_iter()):
        issue_atom = issue_atoms[i]
        if issue_atom == atom:
            assert isinstance(open_atom, OpenPredicateAtom)
            open_atoms.append((term, open_atom))

    new_terms: list[Item] = []
    for i, term in enumerate(atom.terms):
        open_terms = [(t, o.terms[i]) for t, o in open_atoms]
        new_terms.append(convert_term(term, open_terms))
    inner = LogicPredicate(name=atom.predicate.name, args=new_terms)
    if atom.predicate.verifier:
        return inner
    else:
        return BoolNot(inner)


def unparse_set_of_states(s: SetOfStates, issue_structure: IssueStructure) -> Item:
    """
    Unparses a set of states and issue structure into item form

    Args:
        s (SetOfStates): A set of states to unparse
        issue_structure (IssueStructure): The issue structure

    Returns:
        Item: The unparsed item.
    """
    if s.is_falsum:
        return Falsum()
    elif s.is_verum:
        return Truth()
    else:
        assert len(s) > 0
        issue_atoms = [o(t) for t, o in issue_structure.sorted_iter()]
        if len(s) == 1:
            state = next(iter(s))
            assert len(state) > 0
            new_atoms: list[LogicPredicate | BoolNot] = []
            for atom in state:
                if not isinstance(atom, PredicateAtom):
                    raise FOLNotSupportedError(
                        f"Non predicate atom: {atom}  found - FOL not supported"
                    )
                new_atoms.append(convert_atom(atom, issue_structure, issue_atoms))
            if len(new_atoms) == 1:
                return new_atoms[0]
            else:
                return BoolAnd(new_atoms)
        else:
            new_ands: list[LogicPredicate | BoolNot | BoolAnd | Truth] = []
            for state in s.sorted_iter():
                if len(state) == 0:
                    new_item = Truth()
                else:
                    new_atoms = []
                    for atom in state.sorted_iter():
                        if not isinstance(atom, PredicateAtom):
                            raise FOLNotSupportedError(
                                f"Non predicate atom: {atom}  found - FOL not supported"
                            )
                        new_atoms.append(
                            convert_atom(atom, issue_structure, issue_atoms)
                        )
                    if len(new_atoms) == 1:
                        new_item = new_atoms[0]
                    else:
                        new_item = BoolAnd(new_atoms)
                new_ands.append(new_item)
            return BoolOr(new_ands)


def view_to_items(v: View) -> list[Item]:
    """
    Unparses a view back to a parser object representation

    Args:
        v (View): The input view

    Raises:
        FOLNotSupportedError: View not supported by fol parser

    Returns:
        list[Item]: The parser object representation
    """
    if not all([w.is_null for w in v.weights.values()]):
        raise FOLNotSupportedError(f"View: {v} contain weights")
    main_item: Item
    if v.supposition.is_verum:
        main_item = unparse_set_of_states(v.stage, v.issue_structure)
    else:
        stage = unparse_set_of_states(v.stage, v.issue_structure)
        supposition = unparse_set_of_states(v.supposition, v.issue_structure)
        main_item = Implies(supposition, stage)
    return [*get_quantifiers(v.dependency_relation), main_item]
