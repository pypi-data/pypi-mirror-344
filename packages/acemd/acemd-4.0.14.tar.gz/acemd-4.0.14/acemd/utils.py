def plumed_parser(fn):
    # Hack to workaround https://github.com/openmm/openmm-plumed/pull/27
    # Joins continuation lines and strips comments
    out = []
    continuing = False
    with open(fn) as f:
        for line in f:
            line = line.strip()
            if "#" in line:
                line = line[: line.find("#")]  # Strip comments
            dots = line.find("...")
            if not continuing:
                if dots == -1:
                    out.append(line)
                else:
                    out.append(line[:dots])
                    continuing = True
            else:
                if dots == -1:
                    out[-1] = out[-1] + " " + line
                else:
                    out[-1] = out[-1] + " " + line[:dots]
                    continuing = False
    return "\n".join(out)
