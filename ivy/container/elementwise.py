# local
from ivy.container.base import ContainerBase

# ToDo: implement all methods here as public instance methods


# noinspection PyUnresolvedReferences
class ContainerWithElementwise(ContainerBase):

    def __init__(self):
        import ivy.functional.ivy.elementwise as elementwise
        ContainerBase.__init__(self, elementwise)
