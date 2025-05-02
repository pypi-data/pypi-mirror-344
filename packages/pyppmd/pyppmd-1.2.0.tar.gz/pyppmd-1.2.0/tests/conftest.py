
def pytest_benchmark_update_json(config, benchmarks, output_json):
    """Calculate compression/decompression speed and add as extra_info"""
    for benchmark in output_json["benchmarks"]:
        if "data_size" in benchmark["extra_info"]:
            rate = benchmark["extra_info"].get("data_size", 0.0) / benchmark["stats"]["mean"]
            benchmark["extra_info"]["rate"] = rate


def pytest_benchmark_update_machine_info(config, machine_info):
    cpuinfo = pytest.importorskip("cpuinfo")

    cpu_info = cpuinfo.get_cpu_info()
    brand = cpu_info.get("brand_raw", None)
    if brand is None:
        brand = "{} core(s) {} CPU ".format(cpu_info.get("count", "unknown"), cpu_info.get("arch", "unknown"))
    machine_info["cpu"]["brand"] = brand
    machine_info["cpu"]["hz_actual_friendly"] = cpu_info.get("hz_actual_friendly", "unknown")
