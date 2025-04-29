from pathlib import Path
from vame.logging.logger import VameLogger
from vame.preprocessing.cleaning import lowconf_cleaning, outlier_cleaning
from vame.preprocessing.alignment import egocentrically_align_and_center
from vame.preprocessing.filter import savgol_filtering
from vame.preprocessing.scaling import rescaling
from vame.schemas.states import save_state, PreprocessingFunctionSchema


logger_config = VameLogger(__name__)
logger = logger_config.logger


@save_state(model=PreprocessingFunctionSchema)
def preprocessing(
    config: dict,
    centered_reference_keypoint: str,
    orientation_reference_keypoint: str,
    run_lowconf_cleaning: bool = True,
    run_egocentric_alignment: bool = True,
    run_outlier_cleaning: bool = True,
    run_savgol_filtering: bool = True,
    run_rescaling: bool = False,
    save_logs: bool = True,
) -> None:
    """
    Preprocess the data by:
        - Cleaning low confidence data points
        - Egocentric alignment
        - Outlier cleaning using IQR
        - Rescaling
        - Savitzky-Golay filtering

    Parameters
    ----------
    config : dict
        Configuration dictionary.
    centered_reference_keypoint : str, optional
        Keypoint to use as centered reference.
    orientation_reference_keypoint : str, optional
        Keypoint to use as orientation reference.
    run_lowconf_cleaning : bool, optional
        Whether to run low confidence cleaning.
    run_egocentric_alignment : bool, optional
        Whether to run egocentric alignment.
    run_outlier_cleaning : bool, optional
        Whether to run outlier cleaning.
    run_savgol_filtering : bool, optional
        Whether to run Savitzky-Golay filtering.
    run_rescaling : bool, optional
        Whether to run rescaling.
    save_logs : bool, optional
        Whether to save logs.

    Returns
    -------
    None
    """
    if save_logs:
        log_path = Path(config["project_path"]) / "logs" / "preprocessing.log"
        logger_config.add_file_handler(str(log_path))

    # Low-confidence cleaning
    if run_lowconf_cleaning:
        logger.info("Cleaning low confidence data points...")
        lowconf_cleaning(
            config=config,
            read_from_variable="position",
            save_to_variable="position_cleaned_lowconf",
            save_logs=save_logs,
        )

    # Egocentric alignment
    if run_egocentric_alignment:
        logger.info("Egocentrically aligning and centering...")
        egocentrically_align_and_center(
            config=config,
            centered_reference_keypoint=centered_reference_keypoint,
            orientation_reference_keypoint=orientation_reference_keypoint,
            read_from_variable="position_cleaned_lowconf",
            save_to_variable="position_egocentric_aligned",
            save_logs=save_logs,
        )

    # Outlier cleaning
    if run_outlier_cleaning:
        logger.info("Cleaning outliers using IQR method...")
        outlier_cleaning(
            config=config,
            read_from_variable="position_egocentric_aligned",
            save_to_variable="position_processed",
            save_logs=save_logs,
        )

    # Savgol filtering
    if run_savgol_filtering:
        logger.info("Applying Savitzky-Golay filter...")
        savgol_filtering(
            config=config,
            read_from_variable="position_processed",
            save_to_variable="position_processed",
            save_logs=save_logs,
        )

    # Rescaling
    if run_rescaling:
        logger.info("Rescaling...")
        rescaling(
            config=config,
            read_from_variable="position_processed",
            save_to_variable="position_scaled",
            save_logs=save_logs,
        )
