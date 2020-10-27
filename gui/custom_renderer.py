#!/usr/bin/env python

"""
Functions for rendering manim animation into a video using algomanim API
and constructing anim dicts for AnimationBar widget
"""

from argparse import Namespace
import manimlib.config
import manimlib.constants
from manimlib.extract_scene import get_scene_classes_from_module, get_scenes_to_render
from gui.video_quality import VideoQuality
from gui.panels.customisation_type import CustomisationType


# Modification of internal manim function using algomanim API
def extract_scene(file_path, scene_name, video_quality):
    args = Namespace(color=None,
                     file=file_path,
                     file_name=None,
                     high_quality=video_quality == VideoQuality.high,
                     leave_progress_bars=False,
                     low_quality=video_quality == VideoQuality.low,
                     media_dir="./media/algomanim",
                     medium_quality=video_quality == VideoQuality.med,
                     preview=True,
                     quiet=False,
                     resolution=None,
                     save_as_gif=False,
                     save_last_frame=False,
                     save_pngs=False,
                     scene_names=[scene_name],
                     show_file_in_finder=False,
                     sound=False,
                     start_at_animation_number=None,
                     tex_dir=None,
                     transparent=False,
                     video_dir=None,
                     video_output_dir="./media/algomanim/videos",
                     write_all=False,
                     write_to_movie=False)
    config = manimlib.config.get_configuration(args)
    manimlib.constants.initialize_directories(config)

    module = config["module"]
    all_scene_classes = get_scene_classes_from_module(module)
    scene_class = get_scenes_to_render(all_scene_classes, config)[0]

    scene_kwargs = {
        key: config[key] for key in ["camera_config",
                                     "file_writer_config",
                                     "skip_animations",
                                     "start_at_animation_number",
                                     "end_at_animation_number",
                                     "leave_progress_bars",
                                     ]
    }

    return scene_class(**scene_kwargs)


# Constructs anim dicts for use in AnimationBar widget
def construct_anims(scene, action_pairs):
    anims = []
    start_time = 0
    start_index = 0
    for (i, action_pair) in enumerate(action_pairs):
        action = action_pair.curr_action()
        run_time = 1 if action_pair.run_time is None else action_pair.run_time
        customisations = dict()
        if action_pair.can_change_runtime():
            customisations[CustomisationType.RUNTIME] = action_pair.get_runtime()

        if action_pair.can_change_color():
            customisations[CustomisationType.COLOR] = action_pair.get_color()

        anim = {'start_index': start_index,
                'end_index': start_index,
                'action_pairs': [action_pair],
                'run_time': run_time,
                'start_time': start_time,
                'customisations': customisations}
        start_time += run_time
        for action_pair2 in action_pairs[i + 1:]:
            action2 = action_pair2.curr_action()
            if action2.w_prev:
                if action2.act == action.act:
                    anim['end_index'] += 1
                    anim['action_pairs'].append(action_pair2)
                    if action_pair2.can_change_color():
                        anim['customisations'][CustomisationType.COLOR] = action_pair2.get_color()
                    action_pairs.remove(action_pair2)
            elif (action2.act != scene.play and action2.act != scene.wait) and \
                    (action.act != scene.play and action.act != scene.wait):
                anim['end_index'] += 1
                anim['action_pairs'].append(action_pair2)
                if action_pair2.can_change_color():
                    anim['customisations'][CustomisationType.COLOR] = action_pair2.get_color()
                action_pairs.remove(action_pair2)
            else:
                break
        start_index = anim['end_index'] + 1
        anims.append(anim)

    return anims


# Renders video and returns anim dicts for use in AnimationBar widget
def custom_renderer(file_path, scene_name, video_quality):
    # Output video file
    scene = extract_scene(file_path, scene_name, video_quality)

    # Construct animation representation
    action_pairs = scene.action_pairs.copy()
    return construct_anims(scene=scene, action_pairs=action_pairs)
