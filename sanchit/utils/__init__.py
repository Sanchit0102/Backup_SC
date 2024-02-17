from .utils import CommonUtils
from .sample import Sample
from .trim import Trim
from .screenshot import Screenshot


class Methods(Sample, Trim, Screenshot):
    pass


class Utilities(CommonUtils, Methods):
    pass