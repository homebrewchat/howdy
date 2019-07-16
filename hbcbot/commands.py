def calc_abv(args):
    usage = 'Usage: .abv <OG> <FG>'
    if len(args) != 2:
        return usage
    og = args[0]
    fg = args[1]
    try:
        abv = (float(og) - float(fg)) * 131
        return 'ABV is %.1f' % abv
    except Exception:
        # not passed numbers
        return usage
