def load_input(day):
    try:
        with open(f"inputs/day-{day}.txt") as f:
            return f.readlines()
    except:
        print("Input file could not be read, did you copy it to inputs?")
        return []