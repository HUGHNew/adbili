from constant import Entry


def time_range_filter(entry: Entry, min_sec:int, max_sec:int,) -> bool:
    return min_sec < entry.total_time_milli/1000 < max_sec