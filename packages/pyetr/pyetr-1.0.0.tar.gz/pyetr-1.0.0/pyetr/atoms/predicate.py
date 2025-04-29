class Predicate:
    """
    Represents the predicate object in the atom.
    """

    name: str
    verifier: bool
    arity: int

    def __init__(self, name: str, arity: int, _verifier: bool = True) -> None:
        """
        Args:
            name (str): The name of the predicate
            arity (int): The number of arguments the predicate requires
            _verifier (bool, optional): True if the predicate is not negated. Defaults to True.
        """
        self.verifier = _verifier
        self.name = name
        self.arity = arity

    def __invert__(self):
        return Predicate(name=self.name, arity=self.arity, _verifier=not self.verifier)

    @property
    def detailed(self) -> str:
        return repr(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Predicate):
            return False
        return (
            self.name == other.name
            and self.arity == other.arity
            and self.verifier == other.verifier
        )

    def __hash__(self) -> int:
        return hash((self.name, self.arity, self.verifier))

    def __repr__(self) -> str:
        return f"<Predicate name={self.name} arity={self.arity}>"


equals_predicate = Predicate("==", 2)
