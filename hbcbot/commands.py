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

def brix_sg(args):
    usage = 'Usage: .brix <Original BRIX> (<Final BRIX>)'
    if len(args) < 1 or len(args) > 2:
        return usage

    if len(args) == 1:
        brix = float(args[0])
        try:
            sg = (brix / (258.6 - ((brix / 258.2) * 227.1))) + 1
            return 'OG is %.3f' % sg
        except Exception:
            # not passed numbers
            return usage

    if len(args) == 2:
        try:
            obrix = float(args[0])
            fbrix = float(args[1])
            sg = (obrix / (258.6 - ((obrix / 258.2) * 227.1))) + 1
            fg = (1 -
                  (0.004493 * obrix) + (0.011774 * fbrix) +
                  (0.00027581 * obrix ** 2) - (0.0012717 * fbrix ** 2) -
                  (0.00000728 * obrix ** 3) + (0.000063293 * fbrix ** 3))
            message = 'OG is %.3f, FG is %.3f, ' % (sg, fg)
            message += calc_abv([sg, fg])
            return message
        except Exception:
            # not passed numbers
            return usage
