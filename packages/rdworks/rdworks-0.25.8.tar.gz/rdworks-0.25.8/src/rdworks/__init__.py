__version__ = '0.25.8'

from rdworks.xml import list_predefined_xml, get_predefined_xml, parse_xml
from rdworks.units import ev2kcalpermol, hartree2ev, hartree2kcalpermol, periodictable
from rdworks.readin import read_csv, merge_csv, read_dataframe, read_smi, read_sdf, read_mae 
from rdworks.std import desalt_smiles, standardize_smiles, standardize
from rdworks.tautomers import complete_tautomers
from rdworks.stereoisomers import complete_stereoisomers
from rdworks.ionized import IonizedStates
from rdworks.rgroup import expand_rgroup, most_common, most_common_in_NP
from rdworks.scaffold import scaffold_network, scaffold_tree, BRICS_fragmented, BRICS_fragment_indices
from rdworks.matchedseries import MatchedSeries
from rdworks.descriptor import rd_descriptor, rd_descriptor_f
from rdworks.utils import fix_decimal_places_in_list, fix_decimal_places_in_dict, mae_to_dict, mae_rd_index
from rdworks.display import svg
from rdworks.conf import Conf
from rdworks.mol import Mol
from rdworks.mollibr import MolLibr

from rdkit import rdBase, RDLogger
rdkit_logger = RDLogger.logger().setLevel(RDLogger.CRITICAL)

import logging

main_logger = logging.getLogger()
main_logger.setLevel(logging.INFO) # level: DEBUG < INFO < WARNING < ERROR < CRITICAL
logger_formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger_ch = logging.StreamHandler()
logger_ch.setFormatter(logger_formatter)
main_logger.addHandler(logger_ch)


__rdkit_version__ = rdBase.rdkitVersion
