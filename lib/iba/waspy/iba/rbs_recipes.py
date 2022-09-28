import logging
from typing import Dict, List

from waspy.iba.file_writer import FileWriter
from waspy.iba.plot import serialize_histogram_header, format_caen_histogram, plot_graph, plot_energy_yields, \
    plot_graph_group
from waspy.iba.rbs_entities import get_positions_as_coordinate, RbsRecipe, RbsData, CoordinateRange, Graph, Plot, \
    RbsChanneling, get_positions_as_float, Window, PositionCoordinates, GraphGroup
from waspy.iba.rbs_setup import RbsSetup
from waspy.iba.rbs_yield_angle_fit import fit_and_smooth, get_angle_for_minimum_yield


def run_rbs_recipe(vary_coordinate: CoordinateRange, charge_total: int, rbs: RbsSetup) -> RbsData:
    positions = get_positions_as_coordinate(vary_coordinate)
    rbs.prepare_counting_with_target(charge_total / len(positions))
    rbs.start_data_acquisition()
    for index, position in enumerate(positions):
        rbs.move_and_count(position)
    rbs.stop_data_acquisition()
    return rbs.get_status(True)


# TODO: this function should return the Graph and the text data set as is. Writing to files should be done elsewhere
def store_recipe_data(recipe_name: str, sample: str, rbs_data: RbsData, file_writer: FileWriter, beam_params: Dict):
    plots = []

    for [detector_name, histogram] in rbs_data.histograms:
        header = serialize_histogram_header(rbs_data, detector_name, recipe_name, sample, beam_params)
        full_data = header + "\n" + format_caen_histogram(histogram)
        file_writer.write_text_to_disk(recipe_name + "_" + detector_name + ".txt", full_data)
        plots.append(Plot(title=detector_name, points=histogram))

    rbs_graph = Graph(title=recipe_name, plots=plots)
    fig = plot_graph(rbs_graph)
    file_writer.write_matplotlib_fig_to_disk(recipe_name + ".png", fig)


# TODO: return diagnostics with start and end time ?
def run_random(recipe: RbsRecipe, rbs: RbsSetup, file_writer: FileWriter, beam_params: Dict):
    rbs.move(recipe.start_position)
    rbs_data = run_rbs_recipe(recipe.vary_coordinate, recipe.charge_total, rbs)
    store_recipe_data(recipe.name, recipe.sample, rbs_data, file_writer, beam_params)


# TODO: remove FileWriter dependency. Writing should happen in another call
# Comments inline in function -> split off other functions
def run_channeling(recipe: RbsChanneling, rbs: RbsSetup, file_writer: FileWriter, beam_params: Dict):
    rbs.move(recipe.start_position)

    # AYS
    for index, coordinate_range in enumerate(recipe.yield_coordinate_ranges):
        recipe_name = recipe.name + str(index) + str(coordinate_range.name)

        # Gather yields
        file_writer.cd_folder(recipe_name)
        energy_yields = []
        for step in get_positions_as_float(coordinate_range):
            single = CoordinateRange.init_single(coordinate_range.name, step)
            rbs_data = run_rbs_recipe(single, recipe.yield_charge_total, rbs)

            data_to_optimize = rbs_data.histograms[recipe.yield_optimize_detector_identifier]
            energy_yields.append(get_sum(data_to_optimize, recipe.yield_integration_window))
            step_name = f'{recipe_name}_{coordinate_range.name}_{step}'
            store_recipe_data(step_name, recipe.sample, rbs_data, file_writer, beam_params)

        file_writer.cd_folder_up()
        angles = get_positions_as_float(coordinate_range)
        content = ""
        for [angle, energy_yield] in zip(angles, energy_yields):
            content += f'{angle}, {energy_yield}\n'
        file_writer.write_text_to_disk(recipe_name)

        # Move to minimum
        try:
            smooth_angles, smooth_yields = fit_and_smooth(angles, energy_yields)
            min_angle = get_angle_for_minimum_yield(smooth_angles, smooth_yields)
            min_position = convert_float_to_coordinate(coordinate_range.name, min_angle)
            plot_energy_yields(recipe.name, angles, energy_yields, smooth_angles, smooth_yields)
            rbs.move(min_position)
            # TODO: send something to db (stepwise_least finish) (callback? - also callback for file writing?)
        except RuntimeError as e:
            logging.error(e)
            # TODO: send something to db (terminate) (callback? - also callback for file writing?)

    # FIXED
    single = CoordinateRange.init_single("none", None)
    fixed_data = run_rbs_recipe(single, recipe.compare_charge_total, rbs)
    store_recipe_data(recipe.name + "_fixed", recipe.sample, fixed_data, file_writer, beam_params)

    # RANDOM
    random_data = run_rbs_recipe(recipe.random_coordinate_range, recipe.compare_charge_total, rbs)
    store_recipe_data(recipe.name + "_random", recipe.sample, fixed_data, file_writer, beam_params)

    graphs = []

    for detector_name in fixed_data.histograms.keys():
        fixed_plot = Plot(title=f'fixed', points=fixed_data.histograms[detector_name])
        random_plot = Plot(title=f'random', points=random_data.histograms[detector_name])
        graph = Graph(title=f'{detector_name}', plots=[fixed_plot, random_plot], x_label="energy level", y_label="yield")
        graphs.append(graph)

    graph_group = GraphGroup(title=f'{recipe.name}', graphs=graphs)
    fig = plot_graph_group(graph_group)
    file_writer.write_matplotlib_fig_to_disk(recipe.name +".png", fig)


def get_sum(data: List[int], window: Window) -> int:
    return sum(data[window.start:window.end])


def convert_float_to_coordinate(coordinate_name: str, position: float) -> PositionCoordinates:
    return PositionCoordinates.parse_obj({coordinate_name: position})
