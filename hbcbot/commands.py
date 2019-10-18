def calc_abv(args):
    usage = 'Usage: .abv <OG> <FG>'
    if len(args) != 2:
        return usage
    og = args[0]
    fg = args[1]
    try:
        abv = ((76.08 * (float(og)-float(fg)) / (1.775-float(og))) *
               (float(fg) / 0.794))
        return 'ABV is %.1f' % abv
    except Exception:
        # not passed numbers
        return usage
