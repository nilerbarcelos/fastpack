#!/usr/bin/env python3
"""
Benchmark comparison between fastpack, json, and pickle.

Run: python benchmarks/compare.py
"""

import json
import pickle
import time
from datetime import datetime
from decimal import Decimal
from uuid import UUID

import fastpack


def benchmark(name: str, func, iterations: int = 10000) -> float:
    """Run a benchmark and return average time in microseconds."""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    avg_us = (elapsed / iterations) * 1_000_000
    return avg_us


def format_result(name: str, pack_us: float, unpack_us: float, size: int) -> str:
    """Format benchmark result as a table row."""
    return f"| {name:<12} | {pack_us:>10.2f} | {unpack_us:>10.2f} | {size:>8} |"


def run_benchmarks():
    """Run all benchmarks and print results."""

    # Test data
    simple_dict = {"name": "Ana", "age": 30, "active": True}

    complex_dict = {
        "id": 12345,
        "name": "Test User",
        "email": "user@example.com",
        "active": True,
        "score": 95.5,
        "tags": ["python", "developer", "senior"],
        "settings": {
            "theme": "dark",
            "notifications": True,
            "language": "pt-BR",
        },
        "history": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    }

    large_list = [{"id": i, "value": f"item_{i}"} for i in range(100)]

    # Datasets to benchmark
    datasets = [
        ("simple", simple_dict),
        ("complex", complex_dict),
        ("large_list", large_list),
    ]

    print("=" * 60)
    print("FASTPACK BENCHMARK")
    print("=" * 60)
    print()

    for dataset_name, data in datasets:
        print(f"Dataset: {dataset_name}")
        print("-" * 56)
        print("| Library      |  Pack (µs) | Unpack (µs) |    Size |")
        print("|--------------|------------|-------------|---------|")

        # JSON
        json_packed = json.dumps(data).encode()
        json_pack = benchmark("json_pack", lambda: json.dumps(data).encode())
        json_unpack = benchmark("json_unpack", lambda: json.loads(json_packed))
        print(format_result("json", json_pack, json_unpack, len(json_packed)))

        # Pickle
        pickle_packed = pickle.dumps(data)
        pickle_pack = benchmark("pickle_pack", lambda: pickle.dumps(data))
        pickle_unpack = benchmark("pickle_unpack", lambda: pickle.loads(pickle_packed))
        print(format_result("pickle", pickle_pack, pickle_unpack, len(pickle_packed)))

        # Fastpack
        fastpack_packed = fastpack.pack(data)
        fastpack_pack = benchmark("fastpack_pack", lambda: fastpack.pack(data))
        fastpack_unpack = benchmark("fastpack_unpack", lambda: fastpack.unpack(fastpack_packed))
        print(format_result("fastpack", fastpack_pack, fastpack_unpack, len(fastpack_packed)))

        # Size comparison
        print()
        json_size = len(json_packed)
        fastpack_size = len(fastpack_packed)
        reduction = (1 - fastpack_size / json_size) * 100
        print(f"Size reduction vs JSON: {reduction:.1f}%")
        print()

    # Python types (only fastpack supports these natively)
    print("=" * 60)
    print("PYTHON TYPES (fastpack only)")
    print("=" * 60)
    print()

    python_data = {
        "timestamp": datetime(2024, 12, 15, 14, 30, 0),
        "amount": Decimal("99.99"),
        "id": UUID("12345678-1234-5678-1234-567812345678"),
        "tags": {"new", "featured", "sale"},
        "coords": (10, 20, 30),
    }

    fastpack_packed = fastpack.pack(python_data)
    fastpack_pack = benchmark("fastpack_pack", lambda: fastpack.pack(python_data))
    fastpack_unpack = benchmark("fastpack_unpack", lambda: fastpack.unpack(fastpack_packed))

    print(f"Pack time:   {fastpack_pack:.2f} µs")
    print(f"Unpack time: {fastpack_unpack:.2f} µs")
    print(f"Size:        {len(fastpack_packed)} bytes")
    print()

    # Streaming benchmark
    print("=" * 60)
    print("STREAMING (1000 items)")
    print("=" * 60)
    print()

    stream_data = [{"id": i, "value": f"item_{i}"} for i in range(1000)]

    # pack_many
    many_packed = fastpack.pack_many(stream_data)
    pack_many_time = benchmark("pack_many", lambda: fastpack.pack_many(stream_data), iterations=100)
    unpack_many_time = benchmark("unpack_many", lambda: fastpack.unpack_many(many_packed), iterations=100)

    print(f"pack_many:   {pack_many_time:.2f} µs")
    print(f"unpack_many: {unpack_many_time:.2f} µs")
    print(f"Size:        {len(many_packed)} bytes")
    print()


if __name__ == "__main__":
    run_benchmarks()
