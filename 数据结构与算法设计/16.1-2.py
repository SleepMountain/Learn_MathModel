def greedy_activity_selector(activities):
    activities.sort(key=lambda x: x[0], reverse=True)


    selected = [activities[0]]
    last_finish_time = activities[0][1]

    for start, finish in activities[1:]:
        if finish <= last_finish_time:
            selected.append((start, finish))
            last_finish_time = finish

    return selected


activities = [(1, 4), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10)]

selected_activities = greedy_activity_selector(activities)
print("Selected Activities (with caveats):", selected_activities)