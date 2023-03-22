from collections.abc import Callable

SeqReader = Callable[[str], str] 
print(type(SeqReader))