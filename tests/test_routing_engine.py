"""
Unit Tests for GraphRoutingEngine
"""

import pytest
import networkx as nx
from modules.routing_engine import (
    GraphRoutingEngine,
    RouteResult,
    ROAD_TYPES,
    ROAD_TYPE_MULTIPLIER,
    TRAFFIC_LEVELS,
    TRAFFIC_MULTIPLIER,
    VEHICLE_PROFILES,
    GRID_SIZE,
)


class TestGraphStructure:
    def test_grid_initialization(self, routing_engine):
        G = routing_engine.graph
        assert isinstance(G, nx.DiGraph)
        assert G.number_of_nodes() == GRID_SIZE * GRID_SIZE  # 100 nodes
        # Each internal node has 4 directed connections (2 horizontal, 2 vertical pairs)
        assert G.number_of_edges() > 0

    def test_node_attributes(self, routing_engine):
        G = routing_engine.graph
        for nid in G.nodes():
            data = G.nodes[nid]
            assert "lat" in data
            assert "lon" in data
            assert "row" in data
            assert "col" in data
            assert 0 <= data["row"] < GRID_SIZE
            assert 0 <= data["col"] < GRID_SIZE

    def test_edge_attributes(self, routing_engine):
        G = routing_engine.graph
        for u, v, data in G.edges(data=True):
            assert "base_distance" in data
            assert data["base_distance"] > 0
            assert data["road_type"] in ROAD_TYPES
            assert data["traffic_level"] in TRAFFIC_LEVELS


class TestHaversineAndGeometry:
    def test_haversine_identical_points(self):
        coord = (28.61, 77.21)
        dist = GraphRoutingEngine._haversine(coord, coord)
        assert dist == 0.0

    def test_haversine_known_distance(self):
        # 1 degree of latitude is roughly 111 km
        p1 = (28.0, 77.0)
        p2 = (29.0, 77.0)
        dist = GraphRoutingEngine._haversine(p1, p2)
        assert 110.0 <= dist <= 112.0

    def test_find_nearest_node(self, routing_engine):
        # Center of grid node (r=4, c=5) -> node 45
        coords = routing_engine.node_coords(45)
        found_node = routing_engine.find_nearest_node(coords[0], coords[1])
        assert found_node == 45

    def test_find_nearest_node_with_offset(self, routing_engine):
        coords_0 = routing_engine.node_coords(0)
        # Slightly offset but closest to 0
        found_node = routing_engine.find_nearest_node(coords_0[0] + 0.00001, coords_0[1] + 0.00001)
        assert found_node == 0


class TestRoutingLogic:
    @pytest.mark.parametrize("vehicle_type", list(VEHICLE_PROFILES.keys()))
    def test_route_for_all_vehicle_types(self, routing_engine, vehicle_type):
        res = routing_engine.route(source_node=0, target_node=55, vehicle_type=vehicle_type)
        assert isinstance(res, RouteResult)
        assert res.source_node == 0
        assert res.target_node == 55
        assert res.vehicle_type == vehicle_type
        assert len(res.path) >= 2
        assert res.path[0] == 0
        assert res.path[-1] == 55
        assert res.total_cost > 0
        assert res.estimated_time_min >= 1.5
        assert len(res.path_coords) == len(res.path)
        assert len(res.road_segments) == len(res.path) - 1

    def test_unknown_vehicle_defaults_to_ambulance(self, routing_engine):
        res = routing_engine.route(source_node=5, target_node=40, vehicle_type="spaceship")
        assert res.vehicle_type == "ambulance"

    def test_traffic_refresh(self, routing_engine):
        # Record initial traffic levels
        initial_traffic = [data["traffic_level"] for _, _, data in routing_engine.graph.edges(data=True)]
        routing_engine.refresh_traffic()
        new_traffic = [data["traffic_level"] for _, _, data in routing_engine.graph.edges(data=True)]
        # Across ~360 directed edges, some levels will differ
        assert initial_traffic != new_traffic

    def test_all_node_coords_copy(self, routing_engine):
        all_coords = routing_engine.all_node_coords
        assert len(all_coords) == 100
        # Check modifying returned dict does not mutate internal engine dict
        all_coords[999] = (0.0, 0.0)
        assert 999 not in routing_engine._node_coords
