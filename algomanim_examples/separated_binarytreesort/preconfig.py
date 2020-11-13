from algomanim.shape import Shape

# pylint: disable=W0613
def my_preconfig(scene, settings):
    settings['node_size'] = 0.5
    settings['node_shape'] = Shape.CIRCLE
    settings['highlight_color'] = "#e74c3c" # red
