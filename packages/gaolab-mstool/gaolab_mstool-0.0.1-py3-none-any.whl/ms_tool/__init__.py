_hard_dependencies = ("numpy", "lxml", "pyarrow")



for _dependency in _hard_dependencies:
    try:
        __import__(_dependency)
    except ImportError as _e:  # pragma: no cover
        raise ImportError(
            f"Unable to import required dependency {_dependency}. "
            "Please see the traceback for details."
        ) from _e

del _hard_dependencies, _dependency

from ms_tool import *
from ms_tool.expasy_rules import cleavage_rules
from ms_tool.raw_file_tool import ThermoRAW
from ms_tool.mzml_file_tool import convert_mzml_to_parquet, read_mzml, base64_decoder, base64_encoder, mass_bin_function, pretty_print_xml_structure


__doc__ = """
ms-tool - powerful tools for mass spectrometry data processing
=====================================================================

**ms-tool** is a Python package for mass spectrometry data processing, 
developed by the Gao lab at University of Illinois Chicago. This tools
is **FREE** to use for research purposes and **prohibited** for any 
for-profit and commercial usage. For all for-profit and commercial use, 
please contact Gao lab and University of Illinois to obtain a license.

Main Tools
-------------
Here are a brief overview of the ms-tool modules:

  - fasta processing
  - peptide calculation
  - mass spectrum manipulation
  - database search results visualization
"""

__all__ = ["cleavage_rules", "ThermoRAW", "convert_mzml_to_parquet", "read_mzml", "base64_decoder", "base64_encoder", "mass_bin_function", "pretty_print_xml_structure"]
