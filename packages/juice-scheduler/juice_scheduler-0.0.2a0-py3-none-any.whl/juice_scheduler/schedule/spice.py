from __future__ import annotations

import logging
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from juice_scheduler.model.configuration import Configuration

from juice_scheduler.common.date_utils import filename_timestamp
from juice_scheduler.common.files import FileResources
from juice_scheduler.common.rest_api import RestApiConnector
from juice_scheduler.model.interval_list import DateStrInterval
from juice_scheduler.model.prime import PrimeHandler
from juice_scheduler.model.resources import ResourceHandler
from juice_scheduler.model.segmentation import Segmentation
from juice_scheduler.ptr.xml_ptr_builder import XMLPtrBuilder
from juice_scheduler.schedule.minimum_duration import filter_minimum_duration


class SpiceRunner:

    @staticmethod
    def from_configuration(configuration: Configuration):

        conf_repo_path = configuration.get_conf_repo_path()
        crema_id = configuration.get_crema_id()

        file_resources = FileResources(conf_repo_path, crema_id)

        sht_file = configuration.get_segmentation_file()
        segmentation = Segmentation.from_sht_file(sht_file) if sht_file is not None else Segmentation("empty")

        for spice_file in file_resources.get_spice_files():
            segmentation.add_csv_file(spice_file)

        return SpiceRunner(segmentation)


    def __init__(self,
                 segmentation: Segmentation):
        self.segmentation = segmentation
        self.ptr_path = None
        self.json_path = None
        self.ptr = None
        self.result_segmentation = None


    def run(self, runner_configuration):

        # Retrieve specific configuration parameters
        priority_list = runner_configuration.get("priority_list")
        trajectory = runner_configuration.get("trajectory")
        dry_run = runner_configuration.get("dry_run", False)

        # Basic priorisation
        self.result_segmentation = Segmentation("result")
        accum = DateStrInterval()

        for pattern in priority_list:
            step_accum = DateStrInterval()
            segment_definitions = self.segmentation.select_segment(pattern)
            if len(segment_definitions) == 0:
                logging.info("Nothing for pattern %s", pattern)

            for item in segment_definitions:
                new = deepcopy(item)
                # We removed the previous
                new.substract(accum)
                # And filter by minimum duration the result
                new = filter_minimum_duration(new)
                self.result_segmentation.base_map[item.name] = new
                step_accum = step_accum.union(new.instances)

            accum = accum.union(step_accum)

        # Make the trivial expansion
        self.result_segmentation.expand_with_primes(PrimeHandler(), ResourceHandler())

        logging.info("Getting ptr snippets")
        # We prepare the snippet map
        mnemonics = list(self.result_segmentation.index_segments().keys())
        ptr_map = self.get_ptr_snippets(trajectory, mnemonics)

        gap_size = runner_configuration.get("gap_size_limit", 240)
        logging.info("Dissolving gaps < %.3f seconds", gap_size)
        # We dissolve the gaps with duration less that 240 seconds
        self.result_segmentation.dissolve_gaps(gap_size)


        minimum_size = runner_configuration.get("tiny_slot_limit", 240)
        logging.info("Dissolving slots < %.3f seconds", gap_size)
        # We dissolve the slots with duration less that 240 seconds
        self.result_segmentation.dissolve_tiny_slots(minimum_size)

        # We create the PTR
        ptr_builder = XMLPtrBuilder(ptr_map)
        sorted_segments = sorted(self.result_segmentation.segment_list, key=lambda item: item.lower)
        self.ptr = ptr_builder.generate_ptr(sorted_segments)

        if not dry_run:
            # Dump of the results
            output_filename = f"SPICE_{trajectory}_{filename_timestamp()}"

            # Write the PTR
            self.ptr_path = Path(f"{output_filename}.ptx")
            with self.ptr_path.open("w") as f:
                f.write(self.ptr)
            logging.info("PTR written to %s", self.ptr_path)

            # Write the result segmentation
            self.json_path = Path(f"{output_filename}.json")
            self.result_segmentation.dump_sht_file(self.json_path)
            logging.info("JSON written to %s", self.json_path)



    def get_ptr_snippets(self, trajectory: str, mnemonics: list[str]):

        """
        Retrieves PTR snippets for the given trajectory and list of mnemonics.

        This method connects to a REST API to fetch segment definitions associated
        with the provided trajectory. It filters the segments based on the given
        mnemonics and retrieves the corresponding pointing request snippets for each
        segment. If a segment does not have a pointing request file, a default block
        reference snippet is used.

        Args:
            trajectory (str): The trajectory identifier for which to retrieve segment definitions.
            mnemonics (list[str]): A list of mnemonic strings to filter the segment definitions.

        Returns:
            dict: A dictionary mapping each mnemonic from the filtered segments to its
            corresponding pointing request snippet.
        """

        ptr_map = {}
        rest_api = RestApiConnector("https://juicesoc.esac.esa.int/rest_api/")
        segment_definitions = rest_api.get_segment_definitions(trajectory)
        segment_definitions = filter(lambda seg_def: seg_def["mnemonic"] in mnemonics, segment_definitions)
        for seg_def in segment_definitions:
            snippet_url = seg_def.get("pointing_request_file")
            snippet = rest_api.get_file(snippet_url) if snippet_url is not None else '<block ref="NAV_EUR"> </block>'
            ptr_map[seg_def["mnemonic"]] = snippet
        return ptr_map
