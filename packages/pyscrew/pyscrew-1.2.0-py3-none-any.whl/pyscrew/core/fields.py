"""
Field definitions for screw operation data.

This module contains dataclasses that define the field names used in:
1. JSON files containing measurement data
2. CSV file containing metadata and classification information

These constants provide a centralized reference for accessing data consistently
throughout the codebase.
"""

from dataclasses import dataclass


@dataclass
class JsonFields:
    """
    Constants for field names in the JSON files containing screw operation data.
    These classes define the naming conventions used in the raw JSON data files
    from the screw driving control.

    Note: The string values (e.g. "id code", "time values") are pre-defined by
    the screw driving control and cannot be changed. Our constant names use a
    more consistent style and align with the CSV field naming (e.g., mapping JSON's
    "result" to WORKPIECE_RESULT to match the CSV's "workpiece_result" field).
    """

    @dataclass
    class Run:
        """
        Run-level metadata fields in the JSON.
        These fields describe the overall properties of a complete screw operation run.

        Attributes:
            DATE: Date when the run was performed
            RESULT: Overall result from the screw driving control ("OK"/"NOK")
            DMC: Machine-defined identification code for each workpiece
            STEPS: Collection of tightening steps in the run
        """

        ID: str = "cycle"
        DATE: str = "date"
        WORKPIECE_RESULT: str = "result"
        WORKPIECE_ID: str = "id code"
        STEPS: str = "tightening steps"

    @dataclass
    class Step:
        """
        Step-level metadata fields in the JSON.
        These fields describe individual steps within a screw operation run.

        Attributes:
            NAME: Name identifier as set in screw driving control
            STEP_TYPE: Type classification (simply "standard")
            WORKPIECE_RESULT: Result status ("OK"/"NOK") for this step
            QUALITY_CODE: Quality assessment code
            GRAPH: Measurement data dictionary containing time, torque, angle, and gradient values
        """

        NAME: str = "name"
        STEP_TYPE: str = "step type"
        WORKPIECE_RESULT: str = "result"
        QUALITY_CODE: str = "quality code"
        GRAPH: str = "graph"

    @dataclass
    class Measurements:
        """
        Measurement field names in the JSON graph data.
        These are the keys used in the GRAPH dictionary for each measurement type.

        Attributes:
            TIME: Time measurements (0.0012s increments)
            TORQUE: Torque measurements
            ANGLE: Angle measurements (0.25° amplitude)
            GRADIENT: Gradient measurements
            STEP: Step values added during processing pipeline (not in raw data)
            CLASS: Class values added during processing pipeline (not in raw data)

        Note:
            "angleRed values" and "torqueRed values" exist but are always [0,...,0]
            and are not used in processing.
            STEP and CLASS fields are added during later processing and are not
            present in the raw JSON data.
        """

        TIME: str = "time values"
        TORQUE: str = "torque values"
        ANGLE: str = "angle values"
        GRADIENT: str = "gradient values"
        STEP: str = "step values"
        CLASS: str = "class values"


@dataclass
class CsvFields:
    """
    Constants for field names in the labels CSV file.
    These fields connect the JSON measurement data with metadata about runs
    and provide classification information.

    Attributes:
        RUN_ID: Unique identifier for each run
        FILE_NAME: Links to corresponding JSON file
        CLASS_VALUE: Scenario-specific classification label
        WORKPIECE_ID: Data matrix code identifying the workpiece
        WORKPIECE_DATE: Date of recording in the screw run
        WORKPIECE_USAGE: Number of times this workpiece has been used
        WORKPIECE_RESULT: Result from screw program ("OK"/"NOK")
        WORKPIECE_LOCATION: Screw position in workpiece ("left" or "right")
        SCENARIO_CONDITION: Condition of the experiment ("normal" or "faulty")
        SCENARIO_EXCEPTION: Flag indicating if there were issues during the experiment (0 for "no issues", 1 otherwise)
    """

    # Identifier fields
    RUN_ID: str = "run_id"
    FILE_NAME: str = "file_name"

    # Value fields
    CLASS_VALUE: str = "class_value"

    # Workpiece-related fields
    WORKPIECE_ID: str = "workpiece_id"
    WORKPIECE_DATE: str = "workpiece_date"
    WORKPIECE_USAGE: str = "workpiece_usage"
    WORKPIECE_RESULT: str = "workpiece_result"
    WORKPIECE_LOCATION: str = "workpiece_location"

    # Experiment-related fields
    SCENARIO_CONDITION: str = "scenario_condition"
    SCENARIO_EXCEPTION: str = "scenario_exception"

    @dataclass
    class DatasetFields:
        """
        Constants for field names in the dataset.
        These fields are used to access the processed data from the ScrewDataset.

        TODO: While currently not in use, this class finally moves away from the
        space-based naming convention of the json files to a more consistent
        underscore-based style. Will be added to the pipeline in the future.
        """

        TIME_VALUES: str = "time_values"
        TORQUE_VALUES: str = "torque_values"
        ANGLE_VALUES: str = "angle_values"
        GRADIENT_VALUES: str = "gradient_values"
        CLASS_VALUES: str = "class_values"
