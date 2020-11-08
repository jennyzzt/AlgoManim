# pylint: disable=W0105
from abc import ABC
from manimlib.imports import *
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata

class AlgoObject(ABC):
    def __init__(self, scene):
        super().__init__()
        # Every object is connected to a scene
        self.scene = scene
        # Every object has a grp
        self.grp = None
        # Optional to have a val
        self.val = None

    ''' Set obj position next to the given obj at vector side '''
    def set_next_to(self, obj, vector, metadata=None):
        meta = metadata if metadata else Metadata.create_fn_metadata()
        # Create action pair
        action = AlgoSceneAction.create_static_action(self.grp.next_to, [obj.grp, vector])
        action_pair = self.scene.add_action_pair(action, action, animated=False)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create_fn_lmetadata(action_pair, [self.val, obj.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    # Static function of set_relative_of to be executed later
    def static_set_relative_of(self, obj, vector):
        self.grp.move_to(obj.grp.get_center() + vector)

    ''' Set obj position relative to the given obj by a vector '''
    def set_relative_of(self, obj, vector, metadata=None):
        meta = metadata if metadata else Metadata.create_fn_metadata()
        # Create action pair
        action = AlgoSceneAction.create_static_action(self.static_set_relative_of, [obj, vector])
        action_pair = self.scene.add_action_pair(action, action, animated=False)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create_fn_lmetadata(action_pair, [self.val, obj.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Center object on screen '''
    def center(self, metadata=None, animated=True, w_prev=False):
        meta = metadata if metadata else Metadata.create_fn_metadata()
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp.center], transform=ApplyMethod), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.grp.center)
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create_fn_lmetadata(action_pair, [self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Show object on screen '''
    def show(self, metadata=None, animated=True, w_prev=False):
        meta = metadata if metadata else Metadata.create_fn_metadata()
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeIn), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.grp])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create_fn_lmetadata(action_pair, [self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Hide object from screen '''
    def hide(self, metadata=None, animated=True, w_prev=False):
        meta = metadata if metadata else Metadata.create_fn_metadata()
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeOut), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.remove, [self.grp])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create_fn_lmetadata(action_pair, [self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)
