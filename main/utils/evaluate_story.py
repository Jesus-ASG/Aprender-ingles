def rateSkills(max_percentage):
    if not max_percentage:
        return '?'
    grades = ['S+', 'S', 'S-', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']
    iterations = 0
    delta = 4
    aux = 100

    ranges = []
    for _ in range(len(grades)):
        ranges.append(round(aux, 2))
        aux -= delta

    iterations = 0
    for i in range(len(ranges)-1):
        if ranges[i] >= max_percentage > ranges[i+1]:
            break
        else:
            iterations += 1
    return grades[iterations]