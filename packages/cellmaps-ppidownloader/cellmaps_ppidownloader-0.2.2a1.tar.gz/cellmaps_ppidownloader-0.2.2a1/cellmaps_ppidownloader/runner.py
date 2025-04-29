#! /usr/bin/env python

import os
import csv
import logging
import logging.config
import time
from datetime import date
from tqdm import tqdm
from cellmaps_utils import logutils
from cellmaps_utils import constants
from cellmaps_utils.provenance import ProvenanceUtil
import cellmaps_ppidownloader
from cellmaps_ppidownloader.exceptions import CellMapsPPIDownloaderError

logger = logging.getLogger(__name__)


class CellmapsPPIDownloader(object):
    """
    Class to run algorithm
    """

    EDGELIST_FILEKEY = 'edgelist'
    BAITLIST_FILEKEY = 'baitlist'
    CM4AI_ROCRATE = 'cm4ai_rocrate'

    def __init__(self, outdir=None,
                 imgsuffix='.jpg',
                 apmsgen=None,
                 skip_logging=True,
                 provenance=None,
                 input_data_dict=None,
                 provenance_utils=ProvenanceUtil(),
                 skip_failed=False):
        """
        Constructor

        :param outdir: directory where images will be downloaded to
        :type outdir: str
        :param apmsgen: gene node attribute generator for APMS data
        :type apmsgen: :py:class:`~cellmaps_downloader.gene.APMSGeneNodeAttributeGenerator`
        :param skip_logging: If ``True`` skip logging, if ``None`` or ``False`` do NOT skip logging
        :type skip_logging: bool
        :param provenance:
        :type provenance: dict
        :param input_data_dict:
        :type input_data_dict: dict
        """
        if outdir is None:
            raise CellMapsPPIDownloaderError('outdir is None')
        self._outdir = os.path.abspath(outdir)
        self._imgsuffix = imgsuffix
        self._start_time = int(time.time())
        self._end_time = -1
        self._apmsgen = apmsgen
        self._provenance = provenance
        self._input_data_dict = input_data_dict
        if skip_logging is None:
            self._skip_logging = False
        else:
            self._skip_logging = skip_logging
        self._inputdataset_ids = []
        self._softwareid = None
        self._apms_gene_attrid = None
        self._provenance_utils = provenance_utils
        self.skip_failed = skip_failed

        if self._input_data_dict is None or not self._input_data_dict:
            self._input_data_dict = {'outdir': self._outdir,
                                     'apmsgen': str(self._apmsgen),
                                     'skip_logging': self._skip_logging,
                                     'provenance': str(self._provenance)
                                     }

    @staticmethod
    def get_example_provenance(requiredonly=True,
                               with_ids=False):
        """
        Gets a dict of provenance parameters needed to add/register
        a dataset with FAIRSCAPE

        :param requiredonly: If ``True`` only output required fields,
                             otherwise output all fields. This value
                             is ignored if **with_ids** is ``True``
        :type requiredonly: bool
        :param with_ids: If ``True`` only output the fields
                         to set dataset guids and ignore value of
                         **requiredonly** parameter.
        :type with_ids: bool
        :return:
        """
        base_dict = {'name': 'Name for pipeline run',
                     'organization-name': 'Name of organization',
                     'project-name': 'Name of project',
                     'cell-line': 'Name of cell line. Ex: U2OS',
                     'treatment': 'Name of treatment, Ex: untreated',
                     'release': 'Name of release. Example: 0.1 alpha',
                     'gene-set': 'Name of gene set. Example chromatin'}
        if with_ids is not None and with_ids is True:
            guid_dict = ProvenanceUtil.example_dataset_provenance(with_ids=with_ids)
            base_dict.update({CellmapsPPIDownloader.EDGELIST_FILEKEY: guid_dict,
                              CellmapsPPIDownloader.BAITLIST_FILEKEY: guid_dict})
            return base_dict

        field_dict = ProvenanceUtil.example_dataset_provenance(requiredonly=requiredonly)

        base_dict.update({CellmapsPPIDownloader.EDGELIST_FILEKEY: field_dict,
                          CellmapsPPIDownloader.BAITLIST_FILEKEY: field_dict})
        return base_dict

    def _update_provenance_with_keywords(self):
        """
        Generates appropriate keywords from provenance data set in constructor

        :return: keywords as str values
        :rtype: list
        """
        if self._provenance is None:
            logger.warning('Provenance is None')
            return
        keywords = []
        for key in ['organization-name', 'project-name', 'release',
                    'cell-line', 'treatment', 'gene-set', 'name']:
            if key in self._provenance:
                keywords.append(self._provenance[key])
        keywords.extend(['AP-MS edgelist download'])
        self._provenance['keywords'] = keywords

    def _update_provenance_with_description(self):
        """
        Gets description from provenance
        :return:
        """
        if self._provenance is None:
            logger.warning('Provenance is None')
            return
        desc = ''
        for key in ['organization-name', 'project-name', 'release',
                    'cell-line', 'treatment', 'gene-set', 'name']:
            if key in self._provenance:
                if desc != '':
                    desc += ' '
                desc += self._provenance[key]
        self._provenance['description'] = desc + ' AP-MS Edgelist'

    def _create_output_directory(self):
        """
        Creates output directory if it does not already exist

        :raises CellmapsDownloaderError: If output directory is None or if directory already exists
        """
        if os.path.isdir(self._outdir):
            raise CellMapsPPIDownloaderError(self._outdir + ' already exists')

        os.makedirs(self._outdir, mode=0o755)

    def _register_software(self):
        """
        Registers this tool

        :raises CellMapsProvenanceError: If fairscape call fails
        """
        software_keywords = self._provenance['keywords']
        software_keywords.extend(['tools', cellmaps_ppidownloader.__name__])
        software_description = self._provenance['description'] + \
                               ' ' + \
                               cellmaps_ppidownloader.__description__
        self._softwareid = self._provenance_utils.register_software(self._outdir,
                                                                    name=cellmaps_ppidownloader.__name__,
                                                                    description=software_description,
                                                                    author=cellmaps_ppidownloader.__author__,
                                                                    version=cellmaps_ppidownloader.__version__,
                                                                    file_format='py',
                                                                    keywords=software_keywords,
                                                                    url=cellmaps_ppidownloader.__repo_url__)

    def _register_apms_gene_node_attrs(self):
        """
        Registers image_gene_node_attributes.tsv file with create as a dataset

        """
        keywords = self._provenance['keywords']
        keywords.extend(['gene', 'attributes', 'file'])
        description = self._provenance['description'] + ' AP-MS gene node attributes file'
        data_dict = {'name': cellmaps_ppidownloader.__name__ + ' output file',
                     'description': description,
                     'data-format': 'tsv',
                     'author': cellmaps_ppidownloader.__author__,
                     'version': cellmaps_ppidownloader.__version__,
                     'schema': 'https://raw.githubusercontent.com/fairscape/cm4ai-schemas/main/v0.1.0/cm4ai_schema_apmsloader_ppi_gene_node_attributes.json',
                     'date-published': date.today().strftime(self._provenance_utils.get_default_date_format_str())}
        self._apms_gene_attrid = self._provenance_utils.register_dataset(self._outdir,
                                                                         source_file=self.get_ppi_gene_node_attributes_file(),
                                                                         data_dict=data_dict)

    def _register_ppi_edgelist(self):
        """
        Registers image_gene_node_attributes.tsv file with create as a dataset

        """
        keywords = self._provenance['keywords']
        keywords.extend(['ppi', 'edgelist', 'file'])
        description = self._provenance['description'] + ' AP-MS ppi edgelist file'
        data_dict = {'name': cellmaps_ppidownloader.__name__ + ' ppi edgelist file',
                     'description': description,
                     'data-format': 'tsv',
                     'author': cellmaps_ppidownloader.__author__,
                     'version': cellmaps_ppidownloader.__version__,
                     'schema': 'https://raw.githubusercontent.com/fairscape/cm4ai-schemas/main/v0.1.0/cm4ai_schema_apmsloader_ppi_edgelist.json',
                     'date-published': date.today().strftime(self._provenance_utils.get_default_date_format_str())}
        self._provenance_utils.register_dataset(self._outdir, source_file=self.get_ppi_edgelist_file(),
                                                data_dict=data_dict)

    def _add_dataset_to_crate(self, data_dict=None,
                              source_file=None, skip_copy=True):
        """

        :param crate_path:
        :param data_dict:
        :return:
        """
        return self._provenance_utils.register_dataset(self._outdir,
                                                       source_file=source_file,
                                                       data_dict=data_dict,
                                                       skip_copy=skip_copy)

    def _register_computation(self):
        """

        :return:
        """
        keywords = self._provenance['keywords']
        keywords.extend(['computation', 'download'])
        description = self._provenance['description'] + ' run of ' + cellmaps_ppidownloader.__name__
        self._provenance_utils.register_computation(self._outdir,
                                                    name=cellmaps_ppidownloader.__computation_name__,
                                                    run_by=str(self._provenance_utils.get_login()),
                                                    command=str(self._input_data_dict),
                                                    description=description,
                                                    keywords=keywords,
                                                    used_software=[self._softwareid],
                                                    used_dataset=self._inputdataset_ids,
                                                    generated=[self._apms_gene_attrid])

    def _create_rocrate(self):
        """
        Creates rocrate for output directory

        :raises CellMapsProvenanceError: If there is an error
        """
        try:
            self._provenance_utils.register_rocrate(self._outdir,
                                                    name=self._provenance['name'],
                                                    organization_name=self._provenance['organization-name'],
                                                    project_name=self._provenance['project-name'],
                                                    description=self._provenance['description'],
                                                    keywords=self._provenance['keywords'])
        except TypeError as te:
            raise CellMapsPPIDownloaderError('Invalid provenance: ' + str(te))
        except KeyError as ke:
            raise CellMapsPPIDownloaderError('Key missing in provenance: ' + str(ke))

    def _register_input_datasets(self):
        """
        Registers cm4ai/apms dataset or samples and unique input
        datasets with FAIRSCAPE
        adding values to **self._inputdataset_ids**

        """
        edgelist_datasetid = None
        baitlist_datasetid = None
        if 'guid' in self._provenance[CellmapsPPIDownloader.EDGELIST_FILEKEY]:
            edgelist_datasetid = self._provenance[CellmapsPPIDownloader.EDGELIST_FILEKEY]['guid']
        if 'guid' in self._provenance[CellmapsPPIDownloader.BAITLIST_FILEKEY]:
            baitlist_datasetid = self._provenance[CellmapsPPIDownloader.BAITLIST_FILEKEY]['guid']

        if edgelist_datasetid is not None and baitlist_datasetid is not None:
            self._inputdataset_ids.append(edgelist_datasetid)
            self._inputdataset_ids.append(baitlist_datasetid)
            logger.debug('Both edgelist and baitlist have dataset ids. Just returning')
            return

        if edgelist_datasetid is None:
            if CellmapsPPIDownloader.EDGELIST_FILEKEY in self._input_data_dict and \
                self._input_data_dict[CellmapsPPIDownloader.EDGELIST_FILEKEY] is not None:
                # write file and add samples dataset
                edgelist_datasetid = self._add_dataset_to_crate(
                    data_dict=self._provenance[CellmapsPPIDownloader.EDGELIST_FILEKEY],
                    source_file=os.path.abspath(self._input_data_dict[CellmapsPPIDownloader.EDGELIST_FILEKEY]),
                    skip_copy=False)
                self._inputdataset_ids.append(edgelist_datasetid)
                logger.debug('Edgelist dataset id: ' + str(edgelist_datasetid))

        if baitlist_datasetid is None:
            if CellmapsPPIDownloader.BAITLIST_FILEKEY in self._input_data_dict and \
                self._input_data_dict[CellmapsPPIDownloader.BAITLIST_FILEKEY] is not None:
                # write file and add unique dataset
                baitlist_datasetid = self._add_dataset_to_crate(
                    data_dict=self._provenance[CellmapsPPIDownloader.BAITLIST_FILEKEY],
                    source_file=os.path.abspath(self._input_data_dict[CellmapsPPIDownloader.BAITLIST_FILEKEY]),
                    skip_copy=False)
                self._inputdataset_ids.append(baitlist_datasetid)
                logger.debug('Baitlist dataset id: ' + str(baitlist_datasetid))
        if CellmapsPPIDownloader.CM4AI_ROCRATE in self._provenance:
            parent_rocrate_id = self._provenance_utils.get_id_of_rocrate(
                self._provenance[CellmapsPPIDownloader.CM4AI_ROCRATE])
            self._inputdataset_ids.append(parent_rocrate_id)

    def _write_task_start_json(self):
        """
        Writes task_start.json file with information about
        what is to be run

        """
        data = {}

        if self._input_data_dict is not None:
            data.update({'commandlineargs': self._input_data_dict})

        logutils.write_task_start_json(outdir=self._outdir,
                                       start_time=self._start_time,
                                       version=cellmaps_ppidownloader.__version__,
                                       data=data)

    def get_ppi_gene_node_attributes_file(self):
        """
        Gets full path to ppi gene node attribute file under output directory
        created when invoking :py:meth:`~cellmaps_downloader.runner.CellmapsPPIDownloader.run`

        :return: Path to file
        :rtype: str
        """
        return os.path.join(self._outdir,
                            constants.PPI_GENE_NODE_ATTR_FILE)

    def get_ppi_gene_node_errors_file(self):
        """
        Gets full path to ppi gene node attribute errors file under output directory
        created when invoking :py:meth:`~cellmaps_downloader.runner.CellmapsPPIDownloader.run`

        :return: Path to file
        :rtype: str
        """
        return os.path.join(self._outdir,
                            constants.PPI_GENE_NODE_ERRORS_FILE)

    def _write_ppi_gene_node_attrs(self, gene_node_attrs=None,
                                   errors=None):
        """

        :param gene_node_attrs:
        :param errors:
        :return:
        """
        with open(self.get_ppi_gene_node_attributes_file(), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=constants.PPI_GENE_NODE_COLS, delimiter='\t')

            writer.writeheader()
            for key in gene_node_attrs:
                writer.writerow(gene_node_attrs[key])

        if errors is not None:
            with open(self.get_ppi_gene_node_errors_file(), 'w') as f:
                for e in errors:
                    f.write(str(e) + '\n')

    def get_ppi_edgelist_file(self):
        """

        :return:
        """
        return os.path.join(self._outdir,
                            constants.PPI_EDGELIST_FILE)

    def _write_ppi_network(self, edgelist=None,
                           gene_node_attrs=None):
        """

        :param edgelist:
        :param gene_node_attrs:
        :return:
        """
        with open(self.get_ppi_edgelist_file(), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=constants.PPI_EDGELIST_COLS, delimiter='\t')
            writer.writeheader()
            for edge in edgelist:
                if edge['GeneID1'] not in gene_node_attrs:
                    logger.error('Skipping ' + str(edge['GeneID1'] + ' cause it lacks a symbol'))
                    continue
                if edge['GeneID2'] not in gene_node_attrs:
                    logger.error('Skipping ' + str(edge['GeneID2'] + ' cause it lacks a symbol'))
                    continue

                genea = gene_node_attrs[edge['GeneID1']]['name']
                geneb = gene_node_attrs[edge['GeneID2']]['name']
                if genea is None or geneb is None:
                    logger.error('Skipping edge cause no symbol is found: ' + str(edge))
                    continue
                if len(genea) == 0 or len(geneb) == 0:
                    logger.error('Skipping edge cause no symbol is found: ' + str(edge))
                    continue
                writer.writerow({constants.PPI_EDGELIST_COLS[0]: genea,
                                 constants.PPI_EDGELIST_COLS[1]: geneb})

    def generate_readme(self):
        description = getattr(cellmaps_ppidownloader, '__description__', 'No description provided.')
        version = getattr(cellmaps_ppidownloader, '__version__', '0.0.0')

        with open(os.path.join(os.path.dirname(__file__), 'readme_outputs.txt'), 'r') as f:
            readme_outputs = f.read()

        readme = readme_outputs.format(DESCRIPTION=description, VERSION=version)
        with open(os.path.join(self._outdir, 'README.txt'), 'w') as f:
            f.write(readme)

    def run(self):
        """
        Downloads ppi data to output directory specified in constructor

        :raises CellMapsPPIDownloaderError: If there is an error
        :return: 0 upon success, otherwise failure
        """
        try:
            exitcode = 99
            self._create_output_directory()
            if self._skip_logging is False:
                logutils.setup_filelogger(outdir=self._outdir,
                                          handlerprefix='cellmaps_ppidownloader')
            self._write_task_start_json()

            self.generate_readme()

            self._update_provenance_with_description()
            self._update_provenance_with_keywords()
            self._create_rocrate()
            self._register_input_datasets()

            self._register_software()

            gene_node_attrs, errors = self._apmsgen.get_gene_node_attributes()

            # write apms attribute data
            self._write_ppi_gene_node_attrs(gene_node_attrs, errors)

            # write apms network
            self._write_ppi_network(edgelist=self._apmsgen.get_apms_edgelist(),
                                    gene_node_attrs=gene_node_attrs)

            self._register_apms_gene_node_attrs()
            self._register_ppi_edgelist()

            self._register_computation()
            exitcode = 0
            return exitcode
        finally:
            self._end_time = int(time.time())
            # write a task finish file
            logutils.write_task_finish_json(outdir=self._outdir,
                                            start_time=self._start_time,
                                            end_time=self._end_time,
                                            status=exitcode)
