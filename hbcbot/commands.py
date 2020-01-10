def _abv(og, fg):
    return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)


def _brix_to_og(brix):
    return (brix / (258.6 - ((brix / 258.2) * 227.1))) + 1


def calc_abv(args):
    usage = 'Usage: .abv <OG> <FG>'
    if len(args) != 2:
        return usage

    try:
        og = float(args[0])
        fg = float(args[1])
        return 'ABV is %.1f' % _abv(og, fg)

    except Exception:
        # not passed numbers
        return usage


def brix_sg(args):
    usage = 'Usage: .brix <Original BRIX> (<Final BRIX>)'
    if len(args) < 1 or len(args) > 2:
        return usage

    if len(args) == 1:
        try:
            brix = float(args[0])
            return 'OG is %.3f' % _brix_to_og(brix)
        except Exception:
            # not passed numbers
            return usage

    if len(args) == 2:
        try:
            obrix = float(args[0])
            fbrix = float(args[1])
            sg = _brix_to_og(obrix)
            fg = (1 -
                  (0.004493 * obrix) + (0.011774 * fbrix) +
                  (0.00027581 * obrix ** 2) - (0.0012717 * fbrix ** 2) -
                  (0.00000728 * obrix ** 3) + (0.000063293 * fbrix ** 3))
            abv = _abv(sg, fg)

            message = ('OG: %(og).3f; FG: %(fg).3f, ABV: %(abv).1f' %
                       {'og': sg, 'fg': fg, 'abv': abv})
            return message

        except Exception:
            # not passed numbers
            return usage
