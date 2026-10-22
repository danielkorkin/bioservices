#
# This file is part of a bioservices software
#
# Copyright (c) 2023 - EBI-EMBL
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://bioservices.readthedocs.io
#
##############################################################################
"""Interface to the AlphaFold Protein Structure Database

.. topic:: What is the AlphaFold Protein Structure Database?

    :URL: https://alphafold.ebi.ac.uk
    :REST: https://alphafold.ebi.ac.uk/api

"""

from __future__ import annotations

from bioservices.services import REST

__all__ = ["AFDB"]
id_type_S = ["sequence", "md5"]


class AFDB:
    """Interface to the AlphaFold Protein Structure Database api <https://alphafold.ebi.ac.uk>

    The AlphaFold Protein Structure Database (AlphaFold DB) is a free, open-access repository of high-accuracy 3D protein structure predictions

    Example::

    """

    _base_url = "https://alphafold.ebi.ac.uk"
    _url = f"{_base_url}/api"

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages
        :param bool cache: use HTTP cache
        """
        self.services = REST(
            name="AFDB",
            url=AFDB._url,
            cache=cache,
            requests_per_sec=10,
            verbose=verbose,
        )

    def get_prediction(
        self,
        qualifier: str,
        checksum: str | None = None,
        include_complexes: bool | None = None,
    ):
        """Get prediction

        :param str qualifier: Identifier for the search, allowed values: UniProt accession, or model ID. (eg. Q5VSL9)
        :param str checksum: MD5 checksum of the UniProt sequence
        :param bool include_complexes: Whether to include complex models in the results
        :return: list of matching prediction dicts.
        :raises HTTP 400 Bad Request: If *qualifier* is not found

        Example::

            >>> from bioservices import AFDB
            >>> afdb = AFDB()
            >>> bigg.get_prediction("Q5VSL9")
        """

        url_parameters = ""
        if checksum is not None:
            url_parameters += f"?sequence_checksum={checksum}"

        if include_complexes is not None:
            if url_parameters == "":
                url_parameters += f"?include_complexes={include_complexes}"
            else:
                url_parameters += f"&include_complexes={include_complexes}"

        return self.services.http_get(f"/prediction/{qualifier}{url_parameters}")

    def get_complex(self, qualifier: str):
        """Get all complex models for a UniProt accession or a model ID.

        :param str qualifier: Identifier for the search, allowed values: UniProt accession, or model ID.
        :return: list of matching qualifier dicts with keys ``toolUsed``, ``providerId``, ``entityType``, ``isUniProt``, ``modelEntityId``, ``modelCreatedDate``, ``sequenceVersionDate``, ``globalMetricValue``, ``fractionPlddtVeryLow``, ``fractionPlddtLow``, ``fractionPlddtConfident``, ``fractionPlddtVeryHigh``, ``latestVersion``, ``allVersions``, ``sequence``, ``sequenceStart``, ``sequenceEnd``, ``sequenceChecksum``, ``isUniProtReviewed``, ``gene``, ``uniprotAccession``, ``uniprotId``, ``uniprotDescription``, ``taxId``, ``organismScientificName``, ``isUniProtReferenceProteome``, ``chainId``, ``bcifUrl``, ``cifUrl``, ``pdbUrl``, ``paeImageUrl``, ``msaUrl``, ``plddtDocUrl``, ``paeDocUrl``, ``amAnnotationsUrl``, ``amAnnotationsHg19Url``, ``amAnnotationsHg38Url``, ``isComplex``, ``entryId``, ``uniprotSequence``, ``uniprotStart``, ``uniprotEnd``, ``isReferenceProteome``, and ``isReviewed``.
        """
        return self.services.http_get(f"/complex/{qualifier}")

    def sequence_summary(self, id_: str, type_: str | None = None, rows: int | None = None):
        """Retrieve a summary of AlphaFold-predicted structure models available for a sequence.

        :param str id_: Identifier for the type specified in the type parameter
        :param str type_: Type of the identifier. Available values: sequence, md5
        :param int rows: Number of results to return (max 500).
        :return:

        :raises TypeError:
        """
        if (type_ is not None) & (type_ not in id_type_S):
            raise TypeError("type_ must be None, sequence, or md5")

        params = f"?id={id_}"
        if type_:
            params += f"&type={type_}"
        if rows:
            params += f"&rows={rows}"

        url = f"/sequence/summary{params}"

        return self.services.http_get(url)

    def get_annotation(self, uniprot_accession: str, type_: str):
        """Get all annotations for a UniProt residue range

        :param str uniprot_accession: UniProt accession
        :param str type_: Type of annotation (e.g., MUTAGEN for AlphaMissense)

        :raises TypeError:
        """
        if type_ != "MUTAGEN":
            raise TypeError("Type of annotation must be MUTAGEN")

        return self.services.http_get(f"/annotations/{uniprot_accession}.json?type={type_}")
