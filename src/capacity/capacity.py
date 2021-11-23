from capacity import lookupCapacityDemand as cd
from math import ceil


def calculate_article_assembly_time(production):
    article_assembly_times = cd.assembly_time.copy()
    print("\nBearbeitungszeit kalkulieren:\n")
    for station in article_assembly_times:
        print(f"Station: {station}\n")
        for key in cd.assembly_time[station]:
            print(f"Artikel: {key}")
            article_assembly_times[station][key] = production[key] * \
                cd.assembly_time[station][key]
            print(
                f"Bearbeitungszeit: {production[key]} * {cd.assembly_time[station][key]} = {article_assembly_times[station][key]} Minuten\n")

    print(article_assembly_times)
    return article_assembly_times


def calculate_article_tooling_time():
    article_tooling_times = cd.tooling_time.copy()
    print("\nRüstzeit kalkulieren:\n")
    for station in article_tooling_times:
        print(f"Station: {station}\n")
        for key in cd.tooling_time[station]:
            print(f"Artikel: {key}")
            article_tooling_times[station][key] = cd.tooling_time[station][key]
            print(
                f"Rüstzeit: {cd.tooling_time[station][key]} = {article_tooling_times[station][key]} Minuten\n")

    print(article_tooling_times)
    return article_tooling_times


def calculate_capacity(production, tooling_factors):
    results = {"Station_1": 0, "Station_2": 0, "Station_3": 0, "Station_4": 0, "Station_5": 0, "Station_6": 0, "Station_7": 0,
               "Station_8": 0, "Station_9": 0, "Station_10": 0, "Station_11": 0, "Station_12": 0, "Station_13": 0, "Station_14": 0, "Station_15": 0, }

    assembly_times = calculate_article_assembly_time(production)
    tooling_times = calculate_article_tooling_time()
    print("\nKapazität kalkulieren:\n")
    for station in results:
        print(f"Station: {station}")
        total_assembly_time = 0
        total_tooling_time = 0
        for key in assembly_times[station]:
            print(f"Artikel: {key}\n")
            total_assembly_time += assembly_times[station][key]
            total_tooling_time += tooling_times[station][key]
        total_tooling_time = total_tooling_time * tooling_factors[station]
        print(f"Ungerundete Rüstzeit: {total_tooling_time} Minuten\n")
        total_tooling_time = int(ceil(total_tooling_time / 5) * 5)
        print(f"Gesamte Bearbeitungszeit: {total_assembly_time} Minuten")
        print(f"Gesamte Rüstzeit: {total_tooling_time} Minuten\n")
        results[station] = total_assembly_time + total_tooling_time

    return results
