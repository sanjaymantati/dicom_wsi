import submodules.character_validations as cv
from submodules.utils import get_all_keys
import logging
logger = logging.getLogger(__name__)

restricted_inputs = {
    'PatientSex': ['M', 'F', 'O'],
    'Modality': ['SM'],
    'BurnedInAnnotation': ['YES', 'NO'],
    'LossyImageCompression': ['00', '01'],
    'PhotometricInterpretation': ['MONOCHROME1', 'RGB', 'YBR_FULL_422', 'YBR_ICT', 'YBR_RCT'],
    'VolumetricProperties': ['VOLUME', 'MIXED', 'SAMPLED', 'DISTORTED'],
    'PositionReferenceIndicator': ['SLIDE_CORNER'],
    'ImageType': ['ORIGINAL, PRIMARY, VOLUME, NONE', 'DERIVED, PRIMARY, VOLUME, RESAMPLED',
                  'DERIVED, PRIMARY, LOCALIZER, RESAMPLED', 'ORIGINAL, PRIMARY, LABEL, NONE'],
    'SamplesPerPixel': ['1', '3']
}

required_fields = {
    'General': ['InputFile', 'OutFile', 'NumberOfLevels'],
    'Patient': [],
    'Specimen': ['ContainerIdentifier'],
    'GeneralStudy': ['StudyInstanceUID'],
    'GeneralSeries': ['Modality', 'SeriesInstanceUID'],
    'GeneralEquipment': [],
    'EnhancedGeneralEquipment': ['DeviceSerialNumber', 'Manufacturer', 'ManufacturerModelName', 'SoftwareVersions'],
    'WholeSlideMicroscopyImage': ['ImageType', 'ImagedVolumeWidth', 'ImagedVolumeHeight', 'ImagedVolumeDepth',
                                  'TotalPixelMatrixColumns', 'TotalPixelMatrixRows', 'TotalPixelMatrixOriginSequence',
                                  'XOffsetInSlideCoordinateSystem', 'YOffsetInSlideCoordinateSystem',
                                  'ImageOrientationSlide', 'AcquisitionDateTime', 'LossyImageCompression',
                                  'VolumetricProperties', 'SpecimenLabelInImage', 'BurnedInAnnotation', 'FocusMethod',
                                  'ExtendedDepthOfField'],
    'AcquisitionContext': [],
    'FrameOfReference': ['FrameOfReferenceUID'],
    'OpticalPath': ['NumberOfOpticalPaths', 'OpticalPathSequence'],
    'SOPCommon': ['SOPClassUID', 'SOPInstanceUID'],
    'ImagePixel': ['PixelData'],
    'MultiFrameFunctionalGroups': ['DimensionIndexPointer', 'FrameType', 'ContentDate', 'InstanceNumber',
                                   'NumberOfFrames', 'DimensionIndexSequence', 'DimensionOrganizationSequence',
                                   'PixelMeasuresSequence', 'SharedFunctionalGroupsSequence',
                                   'WholeSlideMicroscopyImageFrameTypeSequence', 'ContentTime',
                                   'DimensionOrganizationUID']
}

size_limits = {
    '2': ['PixelPaddingValue', 'BitsAllocated', 'BitsStored', 'Columns', 'HighBit', 'PixelRepresentation', 'Rows',
          'SamplesPerPixel', 'PlanarConfiguration', 'InConcatenationNumber'],
    '4': ['ImagedVolumeDepth', 'ImagedVolumeHeight', 'ImagedVolumeWidth', 'TotalPixelMatrixColumns',
          'TotalPixelMatrixRows', 'TotalPixelMatrixFocalPlanes', 'NumberOfOpticalPaths', 'DimensionIndexPointer',
          'FunctionalGroupPointer', 'ConcatenationFrameOffsetNumber'],
    '8': ['PatientBirthDate', 'StudyDate', 'SeriesDate', 'AcquisitionDuration', 'ContentDate'],
    '12': ['SeriesNumber', 'InstanceNumber', 'NumberOfFrames'],
    '16': ['PatientSex', 'ValueType', 'AccessionNumber', 'StudyID', 'StudyTime', 'Modality', 'SeriesTime',
           'BurnedInAnnotation', 'ExtendedDepthOfField', 'FocusMethod', 'ImageType', 'LossyImageCompression',
           'PhotometricInterpretation', 'SpecmenLabelInImage', 'VolumetricProperties', 'LossyImageCompressionMethod',
           'ImageOrientationSlide', 'XOffsetInSlideCoordinateSystem', 'YOffsetInSlideCoordinateSystem',
           'LossyImageCompressionRatio', 'ObjectiveLensPower', 'OpticalPathIdentifier', 'FrameType',
           'DimensionOrganizationType', 'PixelSpacing', 'SliceThickness', 'ContentTime'],
    '26': ['AcquisitionDateTime'],
    '64': ['PatientID', 'PatientName', 'ContainerIdentifier', 'SpecimenIdentifier', 'SpecimenShortDescription',
           'SpecimenUID', 'StudyDescription', 'ReferringPhysicianName', 'ConsultingPhysicianName',
           'NameOfPhysiciansReadingStudy', 'PhysiciansOfRecord', 'StudyInstanceUID', 'SeriesDescription',
           'OperatorsName', 'SeriesInstanceUID', 'DeviceSerialNumber', 'Manufacturer', 'ManufacturerModelName',
           'SoftwareVersions', 'PositionReferenceIndicator', 'FrameOfReferenceUID', 'SOPClassUID', 'SOPInstanceUID',
           'DimensionDescriptionLabel', 'DimensionOrganizationUID', 'ConcatenationUID',
           'SOPInstanceUIDOfConcatenationSource']
}

def validate_cfg(cfg):
    """
    Validate the dictionary to make sure all the required elements are present
    :param cfg: a dictionary of values, separated by module name
    :return: 0
    """

    MODULES = ['General', 'Patient', 'Specimen', 'GeneralStudy', 'GeneralSeries', 'GeneralEquipment', 'EnhancedGeneralEquipment',
               'WholeSlideMicroscopyImage', 'AcquisitionContext', 'FrameOfReference', 'OpticalPath', 'SOPCommon',
               'ImagePixel', 'MultiFrameFunctionalGroups']
    for m in MODULES:
        try:
            _validate(m, cfg[m])
            logging.debug('{} data validated'.format(m))
        except KeyError:
            logging.debug('{} not found in your configuration.  Please define'.format(m))
            exit(1)

    logging.debug('All data validated')

def _validation_wrapper(provided_keys, sample_dict):
    for k in provided_keys:
        if k in cv.CS_LIST:
            cv.cs_validator(k, sample_dict[k])
        elif k in cv.DS_LIST:
            cv.ds_validator(k, sample_dict[k])
        elif k in cv.INT_LIST:
            cv.int_validator(k, sample_dict[k])
        elif k in cv.TIME_LIST:
            cv.time_validator(k, sample_dict[k])
        elif k in cv.SIGNEDINT_LIST:
            cv.signedint_validator(k, sample_dict[k])
        elif k in cv.DT_LIST:
            cv.dt_validator(k, sample_dict[k])
        elif k in cv.INTSTRING_LIST:
            cv.intstring_validator(k, sample_dict[k])
        #logging.debug('Completed VR type validation for {}'.format(k))

        # Verify provided values are allowed
        if k in restricted_inputs.keys():
            logging.debug('k {} is found in {}'.format(sample_dict[k], restricted_inputs[k]))
            logging.debug('{}'.format(sample_dict))
            assert sample_dict[k] in restricted_inputs[k], \
                'You provided {} for {}, but it only allows {}'.format(sample_dict[k], k, restricted_inputs[k])
        logging.debug('Completed Allowed Values validation for {}'.format(k))

def _validate(module, sample_dict):
    required_keys = required_fields[module]
    try:
        provided_keys = get_all_keys(sample_dict, prefix=False)
    except AttributeError:
        logging.debug('{} has no values, skipping'.format(module))
        return 0

    # Check to make sure an entry exists for all required fields
    for k in required_keys:
        assert k in provided_keys, 'You are missing the sample field for {} \nin {} \nbut you provided {}'.\
            format(k, required_keys, provided_keys)

    _validation_wrapper(provided_keys, sample_dict)
