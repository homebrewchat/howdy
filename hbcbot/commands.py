import os
import requests


def _abv(og, fg):
    return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)


def _brix_to_og(brix):
    return (brix / (258.6 - ((brix / 258.2) * 227.1))) + 1


def _hydro_temp_adj(mg, mtemp, ctemp):
    ag = mg * (
        (
            1.00130346
            - 0.000134722124 * mtemp
            + 0.00000204052596 * mtemp**2
            - 0.00000000232820948 * mtemp**3
        )
        / (
            1.00130346
            - 0.000134722124 * ctemp
            + 0.00000204052596 * ctemp**2
            - 0.00000000232820948 * ctemp**3
        )
    )
    return ag


def calc_abv(args):
    usage = "Usage: .abv <OG> <FG>"
    if len(args) != 2:
        return usage

    try:
        og = float(args[0])
        fg = float(args[1])
        return "ABV is %.1f" % _abv(og, fg)

    except Exception:
        # not passed numbers
        return usage


def brix_sg(args):
    usage = "Usage: .brix <Original BRIX> (<Final BRIX>)"
    if len(args) < 1 or len(args) > 2:
        return usage

    if len(args) == 1:
        try:
            brix = float(args[0])
            return "OG is %.3f" % _brix_to_og(brix)
        except Exception:
            # not passed numbers
            return usage

    if len(args) == 2:
        try:
            obrix = float(args[0])
            fbrix = float(args[1])
            sg = _brix_to_og(obrix)
            fg = (
                1
                - (0.004493 * obrix)
                + (0.011774 * fbrix)
                + (0.00027581 * obrix**2)
                - (0.0012717 * fbrix**2)
                - (0.00000728 * obrix**3)
                + (0.000063293 * fbrix**3)
            )
            abv = _abv(sg, fg)

            message = "OG: %(og).3f; FG: %(fg).3f, ABV: %(abv).1f" % {
                "og": sg,
                "fg": fg,
                "abv": abv,
            }
            return message

        except Exception:
            # not passed numbers
            return usage


def hydro_adj(args):
    usage = "Usage: .hydrometer <Measured Gravity> <Measured Temp>" "<Calibrated Temp>"
    if len(args) != 3:
        return usage

    try:
        mg = float(args[0])
        mtemp = float(args[1])
        ctemp = float(args[2])
        return "Adjusted Gravity is %.3f" % _hydro_temp_adj(mg, mtemp, ctemp)

    except Exception:
        # not passed numbers
        return usage


def untappd(args):
    usage = "Usage: .untappd <beer name>"
    if not args:
        return usage

    try:
        untappd_client_id = os.environ["UNTAPPD_CLIENT_ID"]
        untappd_client_secret = os.environ["UNTAPPD_CLIENT_SECRET"]
    except KeyError:
        return "Tyler, please add the Untappd API keys"

    api_url = f"https://api.untappd.com/v4/search/beer?q={args}&client_id={untappd_client_id}&client_secret={untappd_client_secret}"

    try:
        response = requests.get(api_url)
    except requests.exceptions.RequestException as e:
        return f"Unable to issue API query for Untappd, {e}"

    if response.status_code == 200:
        data = response.json()
        try:
            bid = data["response"]["beers"]["items"][0]["beer"]["bid"]
        except:
            return "Type in beer name accurately"
    else:
        return usage

    api_url = f"https://api.untappd.com/v4/beer/info/{bid}?limit=1&client_id={untappd_client_id}&client_secret={untappd_client_secret}"

    try:
        response = requests.get(api_url)
    except requests.exceptions.RequestException as e:
        return f"Unable to issue API query for Untappd, {e}"
    
    if response.status_code == 200:
        data = response.json()
        try:
            bbrewery = data["response"]["beer"]["brewery"]["brewery_name"]
            bname = data["response"]["beer"]["beer_name"]
            brating = round(data["response"]["beer"]["rating_score"],2)
            bcount = data["response"]["beer"]["rating_count"]
            babv = round(data["response"]["beer"]["beer_abv"],1)
            bibu = data["response"]["beer"]["beer_ibu"]
            bstyle = data["response"]["beer"]["beer_style"]
            bdesc = data["response"]["beer"]["beer_description"]
            blabel = data["response"]["beer"]["beer_label"]
            bheading_text = f"*{bbrewery} {bname}*"
            brating_text = f"*Average Rating*\n{brating} from {bcount} opinions" 
            bdesc_text = f"*Style:* {bstyle}\n*IBU:* {bibu} *ABV:* {babv}\n{bdesc}"
            beer_json = [{ "type": "section", "text": { "type": "mrkdwn", "text": bheading_text } },
                         { "type": "section", "block_id": "section567", "text": { "type": "mrkdwn", "text": bdesc_text },
                           "accessory": { "type": "image", "image_url":  blabel, "alt_text": "Beer label image" } },
                         { "type": "section", "block_id": "section789", "fields": [ { "type": "mrkdwn", "text": brating_text } ]
                         }]
        return beer_json
    else:
        return usage
