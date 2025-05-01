import pint
import pint_pandas
import uncertainties
from unpaac import uncrts
from string import Formatter
from PySide6.QtCore import Qt, QAbstractTableModel

NO_UNIT_STRING = "No Unit"
HEADER_UNIT_PREFIX = " \n/ "
HEADER_UNIT_SUFFIX = ""


class ShorthandFormatter(Formatter):
    """Custom formatter for handling quantities with units and uncertainties."""

    def format_field(self, value, format_spec):
        if isinstance(value, uncertainties.UFloat) or isinstance(value, pint.Quantity):
            return f"{value:{format_spec}SP}"
        return str(value)


class PintUncertaintyModel(QAbstractTableModel):
    """A Qt model for displaying data with units and uncertainties."""

    def __init__(
        self,
        dataframe,
        deconvolute: bool = False,
        significant_digits: int = 1,
        header_unit_prefix: str = HEADER_UNIT_PREFIX,
        header_unit_suffix: str = HEADER_UNIT_SUFFIX,
        ureg: pint.UnitRegistry = pint.UnitRegistry(),
    ) -> None:
        super().__init__()
        self.deconvolute = deconvolute
        self.significant_digits = significant_digits
        self._header_unit_prefix = header_unit_prefix
        self._header_unit_suffix = header_unit_suffix
        self._ureg = ureg
        self._data = dataframe
        self._data_to_display = None
        self._frmtr = ShorthandFormatter()
        self._convert_data()

    def _convert_data(self) -> None:
        """Convert the data based on deconvolution or convolution mode."""
        if self.deconvolute:
            df = self._data.uncrts.deconvolute()
        else:
            df = self._data.uncrts.convolute()
        self._data_to_display = df.pint.dequantify()

    def rowCount(self, parent=None) -> int:
        if self._data_to_display is None:
            return 0
        return self._data_to_display.shape[0]

    def columnCount(self, parent=None) -> int:
        if self._data_to_display is None:
            return 0
        return self._data_to_display.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self._data_to_display.iat[index.row(), index.column()]
            return self._frmtr.format(f"{{0:.{self.significant_digits}u}}", value)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight | Qt.AlignVCenter
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            measure = str(self._data_to_display.columns[section][0])
            unit_long = self._data_to_display.columns[section][1]
            if unit_long == NO_UNIT_STRING:
                return measure
            try:
                unit = self._ureg.get_symbol(unit_long)
                return f"{measure}{self._header_unit_prefix}{unit}{self._header_unit_suffix}"
            except Exception as e:
                return measure
        return None

    def set_uncertainty_mode(self, deconvolute: bool) -> None:
        """Set the uncertainty mode (deconvolution or convolution)."""
        if self.deconvolute != deconvolute:
            self.deconvolute = deconvolute
            self._convert_data()
            self.layoutChanged.emit()
