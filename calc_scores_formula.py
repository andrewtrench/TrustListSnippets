

def cal_quality_score(contact, contact_confidence, policy, policy_confidence, authors, authors_confidence, ad_indicator,
                      ad_indicator_confidence, ad_density_above_45_score):
    """Calculate the quality score of a URL. Where there is a confidience score multiply the attribute by the
    confidence score. ie a quality contact page exists = 1 * 0.9 (if that was the confidence score.This will
    hopefully introduce some granularity to the quality score. The ad_density_above_45_score is a binary score of 0
    or 1. If the ad density is above 45% then the score is 1 and 0 if below. The weighting of minus 1 is to ensure if
    has a significant impact on the quality score."""

    quality_score = ((((contact * contact_confidence) * 2) + ((policy * policy_confidence) * 4) + (
                (authors * authors_confidence) * 3) + ((ad_indicator * ad_indicator_confidence) * 1) + (ad_density_above_45_score * -1)) * 10)

    return quality_score


def cal_attribute_score(ratio, ads_score, ssl, whois):
    """Same as above but for the attribute score. The major difference is the top end of 1500 for the ratio. With NYT
    coming in at around 1200, a high of 1500 seems like a good stab at a top end. We do the division of score by
    top-end to normalise the value for the calculation.
    """

    score = ((((ratio / 1500) * 4) + (ads_score * 3) + (whois * 2) + (ssl * 1)) * 10)
    return score
