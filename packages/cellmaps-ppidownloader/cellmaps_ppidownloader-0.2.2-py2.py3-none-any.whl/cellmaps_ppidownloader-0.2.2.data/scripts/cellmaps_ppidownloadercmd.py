#!python

import argparse
import os
import sys
import logging
import logging.config
import json

from cellmaps_utils import logutils
from cellmaps_utils import constants
import cellmaps_ppidownloader
from cellmaps_ppidownloader.runner import CellmapsPPIDownloader
from cellmaps_ppidownloader.gene import APMSGeneNodeAttributeGenerator
from cellmaps_ppidownloader.gene import CM4AIGeneNodeAttributeGenerator

logger = logging.getLogger(__name__)


def _parse_arguments(desc, args):
    """
    Parses command line arguments

    :param desc: description to display on command line
    :type desc: str
    :param args: command line arguments usually :py:func:`sys.argv[1:]`
    :type args: list
    :return: arguments parsed by :py:mod:`argparse`
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=constants.ArgParseFormatter)
    parser.add_argument('outdir',
                        help='Directory to write results to')
    parser.add_argument('--cm4ai_table',
                        help='apms.tsv TSV file from CM4AI RO-Crate that has '
                             'at least the following columns: '
                             'Bait    Prey    logOddsScore    FoldChange.x    '
                             'BFDR.x')
    parser.add_argument('--edgelist',
                        help='APMS edgelist TSV file in format of:\n'
                             'GeneID1\tSymbol1\tGeneID2\tSymbol2\n'
                             '10159\tATP6AP2\t2\tA2M')
    parser.add_argument('--edgelist_geneid_one_col', default=APMSGeneNodeAttributeGenerator.GENEID_COL1,
                        help='Name of column containing ensemble Gene ID 1 in --edgelist file')
    parser.add_argument('--edgelist_symbol_one_col', default=APMSGeneNodeAttributeGenerator.SYMBOL_COL1,
                        help='Name of column containing Gene Symbol 1 in --edgelist file')
    parser.add_argument('--edgelist_geneid_two_col', default=APMSGeneNodeAttributeGenerator.GENEID_COL2,
                        help='Name of column containing ensemble Gene ID 2 in --edgelist file')
    parser.add_argument('--edgelist_symbol_two_col', default=APMSGeneNodeAttributeGenerator.SYMBOL_COL2,
                        help='Name of column containing Gene Symbol 2 in --edgelist file')
    parser.add_argument('--baitlist',
                        help='APMS baitlist TSV file in format of:\n'
                             'GeneSymbol\tGeneID\t# Interactors\n'
                             '"ADA"\t"100"\t1.')
    parser.add_argument('--baitlist_symbol_col',
                        default=APMSGeneNodeAttributeGenerator.BAITLIST_GENE_SYMBOL,
                        help='Name of column containing Gene Symbol in --baitlist file')
    parser.add_argument('--baitlist_geneid_col',
                        default=APMSGeneNodeAttributeGenerator.BAITLIST_GENE_ID,
                        help='Name of column containing ensemble Gene ID in --baitlist file')
    parser.add_argument('--baitlist_numinteractors_col',
                        default=APMSGeneNodeAttributeGenerator.BAITLIST_NUM_INTERACTORS,
                        help='Name of column containing # of interactors in --baitlist file')
    parser.add_argument('--provenance',
                        help='Path to file containing provenance '
                             'information about input files in JSON format. '
                             'This is required and not including will output '
                             'and error message with example of file')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'this format: https://docs.python.org/3/library/'
                             'logging.config.html#logging-config-fileformat '
                             'Setting this overrides -v parameter which uses '
                             ' default logger. (default None)')
    parser.add_argument('--skip_logging', action='store_true',
                        help='If set, output.log, error.log '
                             'files will not be created')
    parser.add_argument('--verbose', '-v', action='count', default=1,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module. Messages are '
                             'output at these python logging levels '
                             '-v = WARNING, -vv = INFO, '
                             '-vvv = DEBUG, -vvvv = NOTSET (default ERROR '
                             'logging)')
    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' +
                                 cellmaps_ppidownloader.__version__))

    return parser.parse_args(args)


def main(args):
    """
    Main entry point for program

    :param args: arguments passed to command line usually :py:func:`sys.argv[1:]`
    :type args: list

    :return: return value of :py:meth:`cellmaps_ppidownloader.runner.CellmapsPPIDownloader.run`
             or ``2`` if an exception is raised
    :rtype: int
    """
    withguids_json = json.dumps(CellmapsPPIDownloader.get_example_provenance(with_ids=True), indent=2)
    register_json = json.dumps(CellmapsPPIDownloader.get_example_provenance(), indent=2)

    desc = """
Version {version}

Supports loading of AP-MS data in Bioplex format via
--edgelist and --baitlist flags
or in CM4AI format via --cm4ai_table flag

For bioplex data:

To use pass in a TSV edgelist file to --edgelist

Format of TSV file:

TODO

The --baitlist flag should be given a TSV file containing APMS baits


Format of TSV file:

TODO

For CM4AI data:

To use pass in a CM4AI tsv file stored in RO-CRATE via --cm4ai_table flag

In addition, the --provenance flag is required and must be set to a path
to a JSON file.

If datasets are already registered with FAIRSCAPE then the following is sufficient:

{withguids}

If datasets are NOT registered, then the following is required:

{register}

Additional optional fields for registering datasets include
'url', 'used-by', 'associated-publication', and 'additional-documentation'


    """.format(version=cellmaps_ppidownloader.__version__,
               withguids=withguids_json,
               register=register_json)
    theargs = _parse_arguments(desc, args[1:])
    theargs.program = args[0]
    theargs.version = cellmaps_ppidownloader.__version__

    try:
        logutils.setup_cmd_logging(theargs)
        if theargs.provenance is None:
            sys.stderr.write('\n\n--provenance flag is required to run this tool. '
                             'Please pass '
                             'a path to a JSON file with the following data:\n\n')
            sys.stderr.write('If datasets are already registered with '
                             'FAIRSCAPE then the following is sufficient:\n\n')
            sys.stderr.write(withguids_json + '\n\n')
            sys.stderr.write('If datasets are NOT registered, then the following is required:\n\n')
            sys.stderr.write(register_json + '\n\n')
            return 1

        # load the provenance as a dict
        with open(theargs.provenance, 'r') as f:
            json_prov = json.load(f)

        if theargs.cm4ai_table is None:
            apmsgen = APMSGeneNodeAttributeGenerator(
                apms_edgelist=APMSGeneNodeAttributeGenerator.get_apms_edgelist_from_tsvfile(theargs.edgelist,
                                                                                            geneid_one_col=theargs.edgelist_geneid_one_col,
                                                                                            symbol_one_col=theargs.edgelist_symbol_one_col,
                                                                                            geneid_two_col=theargs.edgelist_geneid_two_col,
                                                                                            symbol_two_col=theargs.edgelist_symbol_two_col),
                apms_baitlist=APMSGeneNodeAttributeGenerator.get_apms_baitlist_from_tsvfile(theargs.baitlist,
                                                                                            symbol_col=theargs.baitlist_symbol_col,
                                                                                            geneid_col=theargs.baitlist_geneid_col,
                                                                                            numinteractors_col=theargs.baitlist_numinteractors_col))
        else:
            json_prov[CellmapsPPIDownloader.CM4AI_ROCRATE] = os.path.abspath(os.path.dirname(theargs.cm4ai_table))
            apmsgen = CM4AIGeneNodeAttributeGenerator(apms_edgelist=CM4AIGeneNodeAttributeGenerator.get_apms_edgelist_from_tsvfile(theargs.cm4ai_table))

        return CellmapsPPIDownloader(outdir=theargs.outdir,
                                     apmsgen=apmsgen,
                                     skip_logging=theargs.skip_logging,
                                     input_data_dict=theargs.__dict__,
                                     provenance=json_prov).run()
    except Exception as e:
        logger.exception('Caught exception: ' + str(e))
        return 2
    finally:
        logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
