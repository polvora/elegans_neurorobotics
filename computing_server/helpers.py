import re
import math


def frange(start, end=None, inc=None):
    if end is None:
        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = 1.0

    li = []
    while 1:
        nxt = start + len(li) * inc
        if inc > 0 and nxt >= end:
            break
        elif inc < 0 and nxt <= end:
            break
        li.append(nxt)

    return li


def parse_magnitude(string_unit_number):
    match = re.match(r"([-+]?[0-9]*\.?[0-9]+) ?([a-z]+)?", string_unit_number, re.I)
    if match:
        items = match.groups()

        unscaled_magnitude = float(items[0])

        if items[1] is None:
            return unscaled_magnitude
        else:
            unit = items[1][0]  # Obtains the first letter
            scaled_magnitude = unscaled_magnitude
            if unit == 'm':
                scaled_magnitude = unscaled_magnitude * 1e-3
            elif unit == 'u':
                scaled_magnitude = unscaled_magnitude * 1e-6
            elif unit == 'n':
                scaled_magnitude = unscaled_magnitude * 1e-9
            elif unit == 'p':
                scaled_magnitude = unscaled_magnitude * 1e-12

            return scaled_magnitude


def dict_split(d, n):
    q, r = divmod(len(d), n)
    print ('q:' + str(q))
    print ('r:' + str(r))

    result = list()
    i = 0
    r_max = r
    page = 0
    for k, v in d.items():
        if int(i / (q + (1 if r > 0 else 0))) > 0:
            page += 1
            i = 0
        if page not in result:
            result.append(dict())
        result[page].update({k: v})
        i += 1
        r = r_max - page

    return result


# https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length/37414115
def list_split(l, n):
    k, m = divmod(len(l), n)
    return [l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
