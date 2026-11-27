"""
Unit Tests for MeshProtocolSimulator
"""

import pytest
import time
import struct
from modules.mesh_simulator import (
    MeshProtocolSimulator,
    MeshPacket,
    TransmissionResult,
    HopLog,
    STRUCT_SIZE,
    _encode_packet,
    _decode_and_verify,
    _flip_random_bit,
    _generate_hop_topology,
    _simulate_rssi,
    _simulate_distance,
)


class TestPacketEncodingAndCRC:
    def test_encode_packet_size(self):
        pkt = MeshPacket(
            latitude=28.612000,
            longitude=77.213000,
            urgency=8.5,
            timestamp=int(time.time()),
            sequence=1,
            flags=1,
        )
        encoded = _encode_packet(pkt)
        # Payload (20 bytes) + CRC-32 (4 bytes) = 24 bytes
        assert len(encoded) == STRUCT_SIZE + 4
        assert len(encoded) == 24

    def test_decode_valid_packet(self):
        pkt = MeshPacket(
            latitude=28.612000,
            longitude=77.213000,
            urgency=8.5,
            timestamp=1700000000,
            sequence=10,
        )
        encoded = _encode_packet(pkt)
        is_valid, exp_crc, recv_crc = _decode_and_verify(encoded)
        assert is_valid is True
        assert exp_crc == recv_crc
        assert len(exp_crc) == 8  # 8 hex characters for 32-bit CRC

    def test_decode_truncated_packet(self):
        short_bytes = b"\x00" * 15
        is_valid, exp_crc, recv_crc = _decode_and_verify(short_bytes)
        assert is_valid is False
        assert recv_crc == "TRUNCATED"

    def test_decode_packet_with_trailing_bytes(self):
        pkt = MeshPacket(
            latitude=28.612,
            longitude=77.213,
            urgency=5.0,
            timestamp=1700000000,
            sequence=2,
        )
        encoded = _encode_packet(pkt)
        padded = encoded + b"\x00\x00\x00"  # 3 extra bytes appended
        is_valid, exp_crc, recv_crc = _decode_and_verify(padded)
        assert is_valid is True
        assert exp_crc == recv_crc

    def test_bit_flip_detection(self):
        pkt = MeshPacket(
            latitude=28.612,
            longitude=77.213,
            urgency=7.0,
            timestamp=1700000000,
            sequence=5,
        )
        original = _encode_packet(pkt)
        corrupted = _flip_random_bit(original)

        assert original != corrupted
        assert len(original) == len(corrupted)

        is_valid, exp_crc, recv_crc = _decode_and_verify(corrupted)
        assert is_valid is False
        assert exp_crc != recv_crc


class TestRFAndTopologySimulation:
    def test_hop_topology_count(self):
        nodes = _generate_hop_topology(5)
        assert len(nodes) == 5
        for node in nodes:
            assert "-" in node

    def test_simulated_rssi_range(self):
        for _ in range(50):
            rssi = _simulate_rssi()
            assert -85.0 <= rssi <= -40.0

    def test_simulated_distance_range(self):
        for _ in range(50):
            dist = _simulate_distance()
            assert 5.0 <= dist <= 50.0


class TestMeshTransmission:
    def test_transmit_sync_basic(self, mesh_simulator):
        res = mesh_simulator.transmit_sync(
            latitude=28.61,
            longitude=77.21,
            urgency=7.5,
            num_hops=4,
        )
        assert isinstance(res, TransmissionResult)
        assert res.total_hops == 4
        assert 0 <= res.hops_completed <= 4
        assert 0.0 <= res.delivery_ratio <= 1.0
        assert res.total_latency_ms > 0
        assert len(res.hop_logs) == 4
        assert res.final_status in ("DELIVERED", "FAILED")
        assert len(res.raw_payload_hex) == 48  # 24 bytes in hex = 48 chars

    def test_sequence_increments(self, mesh_simulator):
        initial_seq = mesh_simulator._sequence_counter
        mesh_simulator.transmit_sync(28.61, 77.21, 6.0, num_hops=3)
        assert mesh_simulator._sequence_counter == initial_seq + 1
        mesh_simulator.transmit_sync(28.61, 77.21, 6.0, num_hops=3)
        assert mesh_simulator._sequence_counter == initial_seq + 2

    def test_async_transmit(self, mesh_simulator):
        import asyncio
        res = asyncio.run(mesh_simulator.transmit(
            latitude=28.62,
            longitude=77.22,
            urgency=9.0,
            num_hops=3,
        ))
        assert isinstance(res, TransmissionResult)
        assert res.total_hops == 3
        assert len(res.hop_logs) == 3
