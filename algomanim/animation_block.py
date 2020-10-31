from gui.panels.customisation_type import CustomisationType

class AnimationBlock:
    def __init__(self, action_pairs, start_index, end_index, start_time):
        self.start_index = start_index
        self.end_index = end_index
        self.start_time = start_time
        self.action_pairs = action_pairs

    def desc(self):
        # Get all relevant animation information stored in the action pair metadata
        desc = f'Animation {self.start_index + 1} - {self.end_index + 1}'
        #anim_infos = dict.fromkeys(map(lambda action: action.metadata, self.action_pairs))
        #anim_info = set(f'{info.metadata.name}' for info in anim_infos if info is not None)

        #if anim_info:
        #    desc = '\n'.join(anim_info)
        #else:
        #    # Lacks metadata, assume custom animation
        #    desc = 'Custom Animation'''
        return desc

    def start_position(self):
        return self.start_time * 1000

    def end_position(self):
        return (self.start_time + self.runtime_val()) * 1000

    def first_pair(self):
        return self.action_pairs[0]

    def act(self):
        return self.first_pair().act()

    def runtime(self):
        return self.first_pair().get_runtime()

    def runtime_val(self):
        return self.first_pair().get_runtime_val()

    def can_set_runtime(self):
        return self.first_pair().can_set_runtime()

    def can_set_color(self):
        possible = False
        for action_pair in self.action_pairs:
            if action_pair.can_set_color():
                possible = True
                break
        return possible

    def get_color(self):
        for action_pair in self.action_pairs:
            if action_pair.can_set_color():
                return action_pair.get_color()
        return None

    def add_action_pair(self, action_pair):
        self.action_pairs.append(action_pair)
        self.end_index += 1

    def customizations(self):
        customizations = dict()
        if self.can_set_color():
            customizations[CustomisationType.COLOR] = self.get_color()

        if self.can_set_runtime():
            customizations[CustomisationType.RUNTIME] = self.runtime_val()

        return customizations

    def run(self):
        action = self.first_pair().curr_action()
        act = action.act
        run_time = self.runtime()
        act_can_set_runtime = action.can_set_runtime
        args = []
        for action_pair in self.action_pairs:
            result = action_pair.run()
            if isinstance(result, list):
                for arg in result:
                    args.append(arg)
            else:
                args.append(result)

        if run_time is None or not act_can_set_runtime:
            act(*args)
        else:
            act(*args, run_time=run_time)
