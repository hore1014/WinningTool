from capacity import lookupCapacityDemand as cd
from math import ceil

import production


def calculate_article_assembly_time(production):
    article_assembly_times = cd.assembly_time.copy()
    for station in article_assembly_times:
        # for every station look up the parts that are assembled at this station and calculate assembly time needed for planned part production
        for key in cd.assembly_time[station]:
            article_assembly_times[station][key] = production[key] * \
                cd.assembly_time[station][key]

    return article_assembly_times


def calculate_capacity(production, tooling_factors):
    results = {"Station_1": 0, "Station_2": 0, "Station_3": 0, "Station_4": 0, "Station_5": 0, "Station_6": 0, "Station_7": 0,
               "Station_8": 0, "Station_9": 0, "Station_10": 0, "Station_11": 0, "Station_12": 0, "Station_13": 0, "Station_14": 0, "Station_15": 0, }

    assembly_times = calculate_article_assembly_time(production)
    for station in results:
        total_assembly_time = 0
        total_tooling_time = 0
        # adding up assemly and tooling times
        for key in assembly_times[station]:
            total_assembly_time += assembly_times[station][key]
            # no tooling time needed if production is 0
            total_tooling_time += cd.tooling_time[station][key] if production[key] != 0 else 0
        total_tooling_time = total_tooling_time * tooling_factors[station]
        # round up to next 5 minutes
        total_tooling_time = int(ceil(total_tooling_time / 5) * 5)
        results[station] = total_assembly_time + total_tooling_time

    return results


def calculate_shifts(capacity):
    # Station: (Number of shifts, overtime in minutes)
    results = {"Station_1": (0, 0), "Station_2": (0, 0), "Station_3": (0, 0), "Station_4": (0, 0), "Station_5": (0, 0), "Station_6": (0, 0), "Station_7": (0, 0),
               "Station_8": (0, 0), "Station_9": (0, 0), "Station_10": (0, 0), "Station_11": (0, 0), "Station_12": (0, 0), "Station_13": (0, 0), "Station_14": (0, 0), "Station_15": (0, 0), }

    for station in capacity:
        match capacity[station]:
            # first shift has max 2400 minutes
            case minutes if minutes > 0 and minutes < 2401:
                results[station] = (1, 0)

            # max 1200 minutes overtime per shift
            case minutes if minutes > 2400 and minutes < 3601:
                results[station] = (1, minutes - 2400)

            # second shift adds max 2400 minutes
            case minutes if minutes > 3600 and minutes < 4801:
                results[station] = (2, 0)

            # max 1200 minutes overtime per shift
            case minutes if minutes > 4800 and minutes < 6001:
                results[station] = (2, minutes - 4800)

            # third shift adds another max 2400 minutes
            case minutes if minutes > 6000 and minutes < 7201:
                results[station] = (3, 0)

            # 7200 minutes is maximum capacity
            case minutes if minutes > 7200:
                results[station] = (9, 9)

            # no production at this station
            case _:
                results[station] = (0, 0)

    return results
