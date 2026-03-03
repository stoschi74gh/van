def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) < 4:
        return None

    device = parts[0]
    sensor_name = parts[1]
    model = parts[2]

    try:
        values = [float(v) for v in parts[3:]]
    except ValueError:
        return None

    return device, sensor_name, model, values
