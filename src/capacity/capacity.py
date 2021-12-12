from . import lookupCapacityDemand as cd
from math import ceil


def calculate_article_assembly_time(production, processing, queued, missing):
    article_assembly_times = {
        "Station_1": {"E29": 0, "E49": 0, "E54": 0, },
        "Station_2": {"E30": 0, "E50": 0, "E55": 0, },
        "Station_3": {"E31": 0, "E51": 0, "E56": 0, },
        "Station_4": {"P1": 0, "P2": 0, "P3": 0, },
        "Station_5": {},
        "Station_6": {"E16": 0, "E18": 0, "E19": 0, "E20": 0, },
        "Station_7": {"E10": 0, "E11": 0, "E12": 0, "E13": 0, "E14": 0, "E15": 0, "E18": 0, "E19": 0, "E20": 0, "E26": 0, },
        "Station_8": {"E10": 0, "E11": 0, "E12": 0, "E13": 0, "E14": 0, "E15": 0, "E18": 0, "E19": 0, "E20": 0, },
        "Station_9": {"E10": 0, "E11": 0, "E12": 0, "E13": 0, "E14": 0, "E15": 0, "E18": 0, "E19": 0, "E20": 0, },
        "Station_10": {"E4": 0, "E5": 0, "E6": 0, "E7": 0, "E8": 0, "E9": 0, },
        "Station_11": {"E4": 0, "E5": 0, "E6": 0, "E7": 0, "E8": 0, "E9": 0, },
        "Station_12": {"E10": 0, "E11": 0, "E12": 0, "E13": 0, "E14": 0, "E15": 0, },
        "Station_13": {"E10": 0, "E11": 0, "E12": 0, "E13": 0, "E14": 0, "E15": 0, },
        "Station_14": {"E16": 0, },
        "Station_15": {"E17": 0, "E26": 0, },
    }
    for station in article_assembly_times:
        # for every station look up the parts that are assembled at this station and calculate assembly time needed for planned part production
        for key in article_assembly_times[station]:
            production_article = production[key]["sum"] if key in production else 0
            processing_article = processing[key] if key in processing else 0
            queued_article = queued[key] if key in queued else 0
            missing_article = missing[key] if key in missing else 0

            amount = production_article + processing_article + \
                queued_article + missing_article
            article_assembly_times[station][key] = amount * \
                cd.assembly_time[station][key]

    return article_assembly_times


def calculate_capacity(production, processing, queued, missing, tooling_factors):
    results = {"Station_1": {}, "Station_2": {}, "Station_3": {}, "Station_4": {}, "Station_5": {}, "Station_6": {}, "Station_7": {},
               "Station_8": {}, "Station_9": {}, "Station_10": {}, "Station_11": {}, "Station_12": {}, "Station_13": {}, "Station_14": {}, "Station_15": {}, }

    assembly_times = calculate_article_assembly_time(
        production, processing, queued, missing)
    for station in results:
        # print(f"\nStation {station}:")
        total_assembly_time = 0
        total_tooling_time = 0
        tuple_part_1 = 0
        tuple_part_2 = 0
        # adding up assemly and tooling times
        for key in assembly_times[station]:
            tuple_part_1 = assembly_times[station][key]
            total_assembly_time += assembly_times[station][key]
            # print(f"Bearbeitungszeit Artikel {key}: {tuple_part_1}")
            # no tooling time needed if production is 0
            tuple_part_2 = cd.tooling_time[station][key] if (assembly_times[station][key] != 0) else (
                0) + cd.tooling_time[station][key] if (key in processing or key in queued or key in missing) else (0)
            total_tooling_time += cd.tooling_time[station][key] if assembly_times[station][key] != 0 else 0
            total_tooling_time += cd.tooling_time[station][key] if key in processing or key in queued or key in missing else 0
            # print(f"Rüstzeit Artikel {key}: {tuple_part_2}")
            # adding processing time and tooling time for every article as tuple to results
            results[station][key] = (tuple_part_1, tuple_part_2)
        total_tooling_time = total_tooling_time * tooling_factors[station]
        # round up to next 5 minutes
        total_tooling_time = int(ceil(total_tooling_time / 5) * 5)
        results[station]["sum"] = total_assembly_time + total_tooling_time

    return results


def calculate_shifts(capacity):
    # Station: (Number of shifts, overtime in minutes)
    results = {"Station_1": (0, 0), "Station_2": (0, 0), "Station_3": (0, 0), "Station_4": (0, 0), "Station_5": (0, 0), "Station_6": (0, 0), "Station_7": (0, 0),
               "Station_8": (0, 0), "Station_9": (0, 0), "Station_10": (0, 0), "Station_11": (0, 0), "Station_12": (0, 0), "Station_13": (0, 0), "Station_14": (0, 0), "Station_15": (0, 0), }

    for station in capacity:
        minutes = capacity[station]
        # first shift has max 2400 minutes
        if (minutes > 0 and minutes < 2401):
            results[station] = (1, 0)

        # max 1200 minutes overtime per shift
        elif (minutes > 2400 and minutes < 3601):
            results[station] = (1, minutes - 2400)

        # second shift adds max 2400 minutes
        elif (minutes > 3600 and minutes < 4801):
            results[station] = (2, 0)

        # max 1200 minutes overtime per shift
        elif (minutes > 4800 and minutes < 6001):
            results[station] = (2, minutes - 4800)

        # third shift adds another max 2400 minutes
        elif (minutes > 6000 and minutes < 7201):
            results[station] = (3, 0)

        # 7200 minutes is maximum capacity
        elif (minutes > 7200):
            results[station] = (9, 9)

        # no production at this station
        else:
            results[station] = (0, 0)

    return results
