from waspy.iba.rbs_entities import Plot, Graph, GraphGroup
import unittest


class TestPlots(unittest.TestCase):

    def test_plot(self):
        plot_1 = Plot(title="d01", points=[0, 1, 2, 3, 4, 5])
        self.assertEqual(plot_1.points, [0, 1, 2, 3, 4, 5])

    def test_graph(self):
        plot_1 = Plot(title="d01", points=[5, 6, 7, 8, 9, 10])
        plot_2 = Plot(title="d02", points=[0, 1, 2, 3, 4, 5])
        graph = Graph(title="graph_01", plots=[plot_1, plot_2])
        self.assertEqual(graph.plots[0].points, [5, 6, 7, 8, 9, 10])

    def test_graph_group(self):
        plot_1 = Plot(title="d01", points=[5, 6, 7, 8, 9, 10])
        plot_2 = Plot(title="d02", points=[0, 1, 2, 3, 4, 5])
        graph_1 = Graph(title="graph_01", plots=[plot_1, plot_2])

        plot_3 = Plot(title="d01", points=[3, 2, 1])
        plot_4 = Plot(title="d02", points=[1, 2, 3])
        graph_2 = Graph(title="graph_01", plots=[plot_3, plot_4])

        graph_group = GraphGroup(title="graph_group", graphs=[graph_1, graph_2])
        self.assertEqual(graph_group.graphs[0].plots[0].points, [5, 6, 7, 8, 9, 10])
        self.assertEqual(graph_group.graphs[0].plots[1].points, [0, 1, 2, 3, 4, 5])
        self.assertEqual(graph_group.graphs[1].plots[0].points, [3, 2, 1])
        self.assertEqual(graph_group.graphs[1].plots[1].points, [1, 2, 3])
