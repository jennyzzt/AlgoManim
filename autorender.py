#!/usr/bin/env python
from argparse import Namespace
import manimlib.config
import manimlib.constants
from manimlib.extract_scene import get_scene_classes_from_module, get_scenes_to_render

def extract_scene(file_path, scene_name):
    args = Namespace(color=None, file=file_path, file_name=None,
        high_quality=False, leave_progress_bars=False, low_quality=True, media_dir=None,
        medium_quality=False, preview=True, quiet=False, resolution=None, save_as_gif=False,
        save_last_frame=False, save_pngs=False, scene_names=[scene_name],
        show_file_in_finder=False, sound=False, start_at_animation_number=None,
        tex_dir=None, transparent=False, video_dir=None, video_output_dir=None,
        write_all=False, write_to_movie=False)
    config = manimlib.config.get_configuration(args)
    manimlib.constants.initialize_directories(config)

    module = config["module"]
    all_scene_classes = get_scene_classes_from_module(module)
    scene_class = get_scenes_to_render(all_scene_classes, config)[0]

    scene_kwargs = dict([
        (key, config[key])
        for key in [
            "camera_config",
            "file_writer_config",
            "skip_animations",
            "start_at_animation_number",
            "end_at_animation_number",
            "leave_progress_bars",
        ]
    ])

    return scene_class(**scene_kwargs)

def main():
    scene = extract_scene('algomanim/bubblesort.py', 'BubbleSortScene')
    action_pairs = scene.action_pairs.copy()
    anims = []
    for (i, action_pair) in enumerate(action_pairs):
        action = action_pair.curr_action()
        run_time = 1 if action_pair.run_time is None else action_pair.run_time
        anim = {'start_index': i, 'end_index': i, 'action_pairs': [action_pair],
            'run_time': run_time}
        for action_pair2 in action_pairs[i+1:]:
            action2 = action_pair2.curr_action()
            if action2.w_prev:
                if action2.act == action.act:
                    anim['end_index'] += 1
                    anim['action_pairs'].append(action_pair2)
                    action_pairs.remove(action_pair2)
            else:
                break
        anims.append(anim)

    total_run_time = sum([anim['run_time'] for anim in anims])
    print(f'Total runtime: {total_run_time}s')
    for (i, anim) in enumerate(anims):
        add_desc = '' if anim['end_index'] == anim['start_index'] else \
            f' - {anim["end_index"]}'
        print(f'[{anim["run_time"]}] Animation {anim["start_index"]}{add_desc}')

if __name__ == "__main__":
    main()
