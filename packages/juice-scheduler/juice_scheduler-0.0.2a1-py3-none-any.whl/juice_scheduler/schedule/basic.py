import logging
from copy import deepcopy

from juice_scheduler.common.files import FileResources
from juice_scheduler.model.configuration import Configuration
from juice_scheduler.model.events import EventsHandler
from juice_scheduler.model.interval_list import DateStrInterval
from juice_scheduler.model.mission_phase import MissionPhaseHandler
from juice_scheduler.model.prime import PrimeHandler
from juice_scheduler.model.resources import ResourceHandler
from juice_scheduler.model.segmentation import Segmentation
from juice_scheduler.schedule.calibration import adjust_calibration_windows, select_calibrations
from juice_scheduler.schedule.minimum_duration import filter_minimum_duration

logger = logging.getLogger(__name__)

class Runner:

    @staticmethod
    def from_configuration(configuration: Configuration):

        conf_repo_path = configuration.get_conf_repo_path()
        crema_id = configuration.get_crema_id()
        prime_mapping_file_path = configuration.get_prime_mapping_path()

        file_resources = FileResources(conf_repo_path, crema_id)
        phase_handler = MissionPhaseHandler.from_file(file_resources.get_mission_phases_file())
        event_handler = EventsHandler.from_file(file_resources.get_event_file())
        prime_handler = PrimeHandler.from_file(prime_mapping_file_path)
        resource_handler = ResourceHandler.from_sht_file(configuration.get_segmentation_file())
        segmentation = Segmentation.from_sht_file(configuration.get_segmentation_file())

        return Runner(phase_handler, event_handler, prime_handler, resource_handler, segmentation)


    def __init__(self,
                 phase_handler: MissionPhaseHandler,
                 event_handler: EventsHandler,
                 prime_handler: PrimeHandler,
                 resource_handler: ResourceHandler,
                 segmentation: Segmentation):

        self.phase_handler = phase_handler
        self.event_handler = event_handler
        self.prime_handler = prime_handler
        self.resource_handler = resource_handler
        self.segmentation = segmentation


        # Store the opportunity/prime mapping
        self.prime_handler.load_segmentation(self.segmentation, self.event_handler)

    def run(self, runner_configuration):

        # Retrieve specific configuration parameters
        priority_list = runner_configuration.get("priority_list")
        phase_calib_selector = runner_configuration.get("phase_calib_selector")


        # Prepare the calibration
        original_calibration = self.segmentation.select_segment("JMAG_CALROLL")[0]
        calibration_selected = select_calibrations(self.phase_handler, phase_calib_selector, original_calibration)
        calibration_adjusted = adjust_calibration_windows(self.event_handler, calibration_selected)
        self.segmentation.base_map["JMAG_CALROLL"] = calibration_adjusted

        # Basic priorisation
        result = Segmentation("result")
        accum = DateStrInterval()

        for pattern in priority_list:
            step_accum = DateStrInterval()
            segment_definitions = self.segmentation.select_segment(pattern)
            if len(segment_definitions) == 0:
                logger.info("Nothing for pattern %s", pattern)

            for item in segment_definitions:
                new = deepcopy(item)
                # We removed the previous
                new.substract(accum)
                # And filter by minimum duration the result
                new = filter_minimum_duration(new)
                result.base_map[item.name] = new
                step_accum = step_accum.union(new.instances)

            accum = accum.union(step_accum)

        # Make the expansion of primes and resources
        result.expand_with_primes(self.prime_handler, self.resource_handler)

        return result

