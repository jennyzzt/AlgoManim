# pylint: disable=W0105, R0913
from abc import ABC
from manimlib.imports import *
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata

'''
Base class for objects created with this library

Note that the convention for creating a fn that results in an action_pair is:
1. Create metadata if metadata was not previously initialised
2. Create action pair
3. Create LowerMetadata
4. Add metadata if metadata is initialised in the fn
'''
class AlgoObject(ABC):
    def __init__(self, scene):
        super().__init__()
        # Every object is connected to a scene
        self.scene = scene
        # Every object has a grp
        self.grp = None
        # Custom texts associated with this obj
        self.text = {' ': TexMobject(' ')}
        # Optional to have a val
        self.val = None

    ''' Set obj position next to the given obj at vector side '''
    def set_next_to(self, obj, vector, metadata=None):
        meta = Metadata.check_and_create(metadata)
        # Create action pair
        action = AlgoSceneAction.create_static_action(self.grp.next_to, [obj.grp, vector])
        action_pair = self.scene.add_action_pair(action, action, animated=False)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val, obj.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    # Static function of set_relative_of to be executed later
    def static_set_relative_of(self, obj, vector):
        self.grp.move_to(obj.grp.get_center() + vector)

    ''' Set obj position relative to the given obj by a vector '''
    def set_relative_of(self, obj, vector, metadata=None):
        meta = Metadata.check_and_create(metadata)
        # Create action pair
        action = AlgoSceneAction.create_static_action(self.static_set_relative_of, [obj, vector])
        action_pair = self.scene.add_action_pair(action, action, animated=False)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val, obj.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    # Static function of swap_with to be executed later
    def static_swap_with(self, obj):
        self_center = self.grp.get_center()
        obj_center = obj.grp.get_center()
        self.grp.move_to(obj_center)
        obj.grp.move_to(self_center)

    ''' Swap the positions of this obj and the given one '''
    def swap_with(self, obj, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Create action pair
        anim_action1 = self.scene.create_play_action(
            AlgoTransform([self.grp, obj.grp], transform=CyclicReplace), w_prev=w_prev
        )
        anim_action2 = self.scene.create_play_action(
            AlgoTransform([obj.grp, self.grp], transform=CyclicReplace), w_prev=True
        )
        static_action1 = AlgoSceneAction.create_static_action(self.static_swap_with, [obj])
        static_action2 = AlgoSceneAction.create_empty_action()
        action_pair1 = self.scene.add_action_pair(anim_action1, static_action1, animated=animated)
        action_pair2 = self.scene.add_action_pair(anim_action2, static_action2, animated=animated)
        # Create LowerMetadata
        lower_meta1 = LowerMetadata.create(action_pair1, [self.val, obj.val])
        lower_meta2 = LowerMetadata.create(action_pair2, [self.val, obj.val])
        meta.add_lower(lower_meta1)
        meta.add_lower(lower_meta2)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Center object on screen '''
    def center(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp.center], transform=ApplyMethod), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.grp.center)
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Show object on screen '''
    def show(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeIn), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.grp])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Hide object from screen '''
    def hide(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeOut), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.remove, [self.grp])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Add custom text associated to this obj '''
    def add_text(self, text, key=' ', vector=UP, metadata=None, animated=False, w_prev=True):
        meta = Metadata.check_and_create(metadata)
        # If key exists, hide it
        if key in self.text:
            # Create hide action pair
            anim_action = self.scene.create_play_action(
                AlgoTransform([self.text[key]], transform=FadeOut), w_prev=w_prev
            )
            static_action = AlgoSceneAction.create_static_action(self.scene.remove,
                                                                 [self.text[key]])
            action_pair = self.scene.add_action_pair(anim_action, static_action)
            # Create hide LowerMetadata
            lower_meta = LowerMetadata('hide', action_pair)
            meta.add_lower(lower_meta)
        # Add new text object to text dictionary
        self.text[key] = TexMobject(text)
        # Move it next to the obj with given vector
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.text[key].next_to, self.grp, vector], transform=ApplyMethod)
        )
        static_action = AlgoSceneAction.create_static_action(self.text[key].next_to,
                                                             [self.grp, vector])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create set_next_to LowerMetadata
        lower_meta = LowerMetadata('set_next_to', action_pair)
        meta.add_lower(lower_meta)
        # Add text to screen
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.text[key]], transform=Write)
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.text[key]])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create add_text LowerMetadata
        lower_meta = LowerMetadata.create(action_pair)
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Remove text associated to this obj '''
    def remove_text(self, key=None, metadata=None, animated=False, w_prev=True):
        meta = Metadata.check_and_create(metadata)
        # If no key is given, remove all text
        if not key:
            for k in list(self.text):
                # Create hide action pair
                anim_action = self.scene.create_play_action(
                    AlgoTransform([self.text[k]], transform=FadeOut), w_prev=w_prev
                )
                static_action = AlgoSceneAction.create_static_action(self.scene.remove,
                                                                     [self.text[k]])
                action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                         animated=animated)
                # Create hide LowerMetadata
                lower_meta = LowerMetadata('remove_text', action_pair)
                meta.add_lower(lower_meta)
                del self.text[k]
            # Reset text attribute
            self.text = {" ": TexMobject(" ")}
        # Else if key exists
        elif key in self.text:
            # Create hide action pair
            anim_action = self.scene.create_play_action(
                AlgoTransform([self.text[key]], transform=FadeOut), w_prev=w_prev
            )
            static_action = AlgoSceneAction.create_static_action(self.scene.remove,
                                                                 [self.text[key]])
            action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                     animated=animated)
            # Create hide LowerMetadata
            lower_meta = LowerMetadata('remove_text', action_pair)
            meta.add_lower(lower_meta)
            del self.text[key]
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)