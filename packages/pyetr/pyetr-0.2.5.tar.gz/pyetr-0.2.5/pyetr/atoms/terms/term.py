__all__ = ["Term", "ArbitraryObject", "FunctionalTerm"]

from abc import abstractmethod
from typing import cast

from .abstract_term import AbstractArbitraryObject, AbstractFunctionalTerm, AbstractTerm


class Term(AbstractTerm):
    @property
    @abstractmethod
    def arb_objects(self) -> set["ArbitraryObject"]:
        """
        The arbitrary objects in the term.

        Returns:
            set[ArbitraryObject]: The set of arbitrary objects
        """
        ...

    @abstractmethod
    def _replace_arbs(
        self,
        replacements: dict["ArbitraryObject", "Term"],
    ) -> "Term":
        """
        Replaces one arbitrary object found in the term with another term from a mapping.

        Args:
            replacements (dict[ArbitraryObject, Term]): Mapping of replacements.

        Returns:
            Self: The term with replacements made.
        """
        ...

    @abstractmethod
    def replace_term(
        self,
        old_term: "Term",
        new_term: "Term",
    ) -> "Term":
        """
        Replaces a single term with a another single term.

        Args:
            old_term (Term): The term to be replaced
            new_term (Term): The new term

        Returns:
            Self: The new instance of the atom
        """
        ...


class ArbitraryObject(AbstractArbitraryObject, Term):
    @property
    def arb_objects(self) -> set["ArbitraryObject"]:
        return {self}

    def _replace_arbs(
        self,
        replacements: dict["ArbitraryObject", Term],
    ) -> Term:
        if self in replacements:
            return replacements[self]
        return self

    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ) -> Term:
        if self == old_term:
            return new_term
        else:
            return self


class FunctionalTerm(AbstractFunctionalTerm[Term], Term):
    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_set: set[ArbitraryObject] = set()
        for term in self.t:
            if isinstance(term, FunctionalTerm):
                output_set |= term.arb_objects
            elif isinstance(term, ArbitraryObject):
                output_set.add(term)
            else:
                assert False
        return output_set

    def _replace_arbs(
        self,
        replacements: dict[ArbitraryObject, Term],
    ) -> "FunctionalTerm":
        new_terms: list[Term] = []
        for term in self.t:
            if term in replacements:
                replacement = replacements[cast(ArbitraryObject, term)]
            else:
                if isinstance(term, FunctionalTerm):
                    replacement = term._replace_arbs(replacements)
                elif isinstance(term, ArbitraryObject):
                    replacement = term
                else:
                    assert False
            new_terms.append(replacement)
        return FunctionalTerm(f=self.f, t=tuple(new_terms))

    def replace_term(
        self,
        old_term: Term,
        new_term: Term,
    ) -> Term:
        if self == old_term:
            return new_term
        else:
            new_terms = [
                term.replace_term(old_term=old_term, new_term=new_term)
                for term in self.t
            ]
            return FunctionalTerm(f=self.f, t=tuple(new_terms))


# Changed if clause in 4.2 to separate Arbitrary Objects from FunctionalTerm
