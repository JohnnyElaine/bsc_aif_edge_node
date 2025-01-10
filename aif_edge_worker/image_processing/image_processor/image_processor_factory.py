from aif_edge_worker.enums.computation_type import ComputationType
from aif_edge_worker.image_processing.image_processor.default_image_processor import DefaultImageProcessor
from aif_edge_worker.image_processing.image_processor.image_processor import ImageProcessor
from aif_edge_worker.image_processing.image_processor.yolo.bb_image_processor import BBYOLOImageProcessor
from aif_edge_worker.image_processing.image_processor.yolo.obb_image_processor import OBBYOLOImageProcessor


class ImageProcessorFactory:
    @staticmethod
    def create_image_processor(computation_type: ComputationType) -> ImageProcessor:
        match computation_type:
            case ComputationType.YOLO_OBB:
                return OBBYOLOImageProcessor()
            case ComputationType.YOLO_DETECTION:
                return BBYOLOImageProcessor()
            case ComputationType.NONE:
                return DefaultImageProcessor()