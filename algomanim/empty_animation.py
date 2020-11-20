from algomanim.metadata import Metadata
from algomanim.metadata_block import MetadataBlock


class EmptyMetadataBlock(MetadataBlock):
    def __init__(self, index):
        super(EmptyMetadataBlock, self).__init__(EmptyMetadata(), [], -1, 0.5)
        self.index = index


class EmptyMetadata(Metadata):
    def __init__(self):
        # make it animated so it will be displayed
        super(EmptyMetadata, self).__init__("custom_animation", animated=True)

    def desc(self, sep='\n'):
        return "Add custom animation"


def is_empty_anim(anim):
    return type(anim) == EmptyMetadataBlock


def empty_animation(position):
    return EmptyMetadataBlock(position)
