#!/usr/bin/env python3
"""
Generate _publications/*.md files for academicpages from a list of publications.

Run from the website/ root directory:
    python3 scripts/generate_publications.py

This writes one file per publication into _publications/.
Edit the PUBLICATIONS list below to add/remove entries.
"""
import os
import re
from pathlib import Path

# Each entry: (year, slug, title, authors_html, venue, doi, page_info)
# doi is the bare DOI (no https://); set to None or "" if no DOI.
# page_info is a free-text venue suffix like "76(1): 365-380."
PUBLICATIONS = [
    # Forthcoming
    (2026, "surviving-the-screens",
     "Surviving the Screens: The Problem of Hidden Inattentive Respondents in Online Surveys",
     "Scott Blatte and Brian F. Schaffner",
     "Political Science Research and Methods", "10.1017/psrm.2025.10065",
     "Forthcoming."),
    (2026, "are-local-policy-attitudes-distinct",
     "Are Local Policy Attitudes Distinct?",
     "Brian F. Schaffner, Jesse H. Rhodes, and Raymond J. La Raja",
     "Political Science Research and Methods", "10.1017/psrm.2024.58",
     "Forthcoming."),
    # 2025
    (2025, "conservatives-mental-wellbeing",
     "Do Conservatives Really Have Better Mental Well-Being than Liberals?",
     "Brian F. Schaffner, Thomas Hershewe, Zoe Kava, and Jael Strell",
     "PLOS ONE", "10.1371/journal.pone.0321573",
     "20(4): e0321573."),
    # 2024
    (2024, "critical-race-theory-mobilization",
     "Critical Race Theory and Asymmetric Mobilization",
     "Pia Deshpande, Scott Blatte, Yonatan Margalit, Carolina Olea Lezama, Brian F. Schaffner, Aadhya Shivakumar, and David Wingens",
     "Political Behavior", "10.1007/s11109-023-09889-4",
     "46: 1677–1699."),
    # 2023
    (2023, "response-decoupling-transgressions",
     "Response Decoupling and Partisans' Evaluations of Politicians' Transgressions",
     "Omer Yair and Brian F. Schaffner",
     "Political Behavior", "10.1007/s11109-022-09796-0",
     "45: 1711–1733."),
    (2023, "perceptions-climate-change",
     "Explaining Perceptions of Climate Change in the U.S.",
     "Chiara Binelli, Matthew Loveless, and Brian F. Schaffner",
     "Political Research Quarterly", "10.1177/10659129211070856",
     "76(1): 365–380."),
    # 2022
    (2022, "strategic-discrimination-2020",
     "Strategic Discrimination in the 2020 Democratic Primary",
     "Jon Green, Brian F. Schaffner, and Sam Luks",
     "Public Opinion Quarterly", "10.1093/poq/nfac051",
     "86(4): 886–898."),
    (2022, "latino-candidates-turnout",
     "The Conditional Effects of Latino Candidates and Partisanship on Latino Turnout",
     "Ivelisse Cuevas Molina, Tatishe Nteta, Brian F. Schaffner, and Wouter Van Erve",
     "American Politics Research", "10.1177/1532673X221090753",
     "50(5): 723–730."),
    (2022, "cps-voting-supplement",
     "The CPS Voting and Registration Supplement Overstates Minority Turnout",
     "Stephen Ansolabehere, Bernard L. Fraga, and Brian F. Schaffner",
     "Journal of Politics", "10.1086/717260",
     "84(3): 1850–1855."),
    (2022, "cash-lottery-turnout",
     "A Cash Lottery Increases Voter Turnout",
     "Raymond J. La Raja and Brian F. Schaffner",
     "PLOS ONE", "10.1371/journal.pone.0268640",
     "17(5): e0268640."),
    (2022, "optimizing-sexism",
     "Optimizing the Measurement of Sexism in Political Surveys",
     "Brian F. Schaffner",
     "Political Analysis", "10.1017/pan.2021.6",
     "30(3): 364–380."),
    (2022, "conservative-bias-local-govts",
     "The Conservative Bias in America's Local Governments",
     "Jesse H. Rhodes, Brian F. Schaffner, and Raymond J. La Raja",
     "Political Science Quarterly", "10.1002/polq.13313",
     "137(1): 125–154."),
    (2022, "heightened-racism-sexism",
     "The Heightened Importance of Racism and Sexism in the 2018 U.S. Midterm Elections",
     "Brian F. Schaffner",
     "British Journal of Political Science", "10.1017/S0007123420000319",
     "52(1): 492–500."),
    # 2021
    (2021, "ideology-issue-importance",
     "Political Ideology and Issue Importance",
     "Douglas Rice, Brian F. Schaffner, and David J. Barney",
     "Political Research Quarterly", "10.1177/1065912920967744",
     "74(4): 1081–1096."),
    (2021, "labor-unions-protest",
     "Labor Unions and Non-Member Political Protest Mobilization in the U.S.",
     "Greg Lyon and Brian F. Schaffner",
     "Political Research Quarterly", "10.1177/1065912920950826",
     "74(4): 998–1008."),
    # 2020
    (2020, "going-with-the-flows",
     "Going with the Flows: Information that Changes Americans' Immigration Preferences",
     "Scott Blinder and Brian F. Schaffner",
     "International Journal of Public Opinion Research", "10.1093/ijpor/edz007",
     "32(1): 153–164."),
    # 2019
    (2019, "elusive-likely-voter",
     "The Elusive Likely Voter: Improving Electoral Predictions with More Informed Vote Propensity Models",
     "Anthony Rentsch, Brian F. Schaffner, and Justin H. Gross",
     "Public Opinion Quarterly", "10.1093/poq/nfz052",
     "83(4): 782–804."),
    (2019, "mass-shootings-gun-control",
     "Reexamining the Effect of Mass Shootings on Public Support for Gun Control",
     "David J. Barney and Brian F. Schaffner",
     "British Journal of Political Science", "10.1017/S0007123418000352",
     "49(4): 1555–1565."),
    # 2018
    (2018, "walking-the-walk",
     "Walking the Walk? Experiments on the Effect of Pledging to Vote on Youth Turnout",
     "Mia Costa, Brian F. Schaffner, and Alicia Prevost",
     "PLOS ONE", "10.1371/journal.pone.0197066",
     "13(5): e0197066."),
    (2018, "donor-strategies-midterm",
     "Detecting and Understanding Donor Strategies in Mid-term Elections",
     "Jesse H. Rhodes, Brian F. Schaffner, and Raymond J. La Raja",
     "Political Research Quarterly", "10.1177/1065912917749323",
     "71(3): 503–516."),
    (2018, "misinformation-inauguration",
     "Misinformation or Expressive Responding? What an Inauguration Crowd Can Tell Us about the Source of Political Misinformation in Surveys",
     "Brian F. Schaffner and Samantha C. Luks",
     "Public Opinion Quarterly", "10.1093/poq/nfx042",
     "82(1): 135–147."),
    (2018, "white-polarization-2016",
     "Understanding White Polarization in the 2016 Vote for President: The Sobering Role of Racism and Sexism",
     "Brian F. Schaffner, Matthew MacWilliams, and Tatishe Nteta",
     "Political Science Quarterly", "10.1002/polq.12737",
     "133(1): 9–34."),
    (2018, "gender-evaluate-representatives",
     "How Gender Conditions the Way Citizens Evaluate and Engage with Their Representatives",
     "Mia Costa and Brian F. Schaffner",
     "Political Research Quarterly", "10.1177/1065912917722235",
     "71(1): 46–58."),
    (2018, "rethinking-representation",
     "Rethinking Representation from a Communal Perspective",
     "Mia Costa, Kaylee Johnson, and Brian F. Schaffner",
     "Political Behavior", "10.1007/s11109-017-9393-9",
     "40(2): 301–320."),
    (2017, "testing-unequal-representation",
     "Testing Models of Unequal Representation: Democratic Populists and Republican Oligarchs?",
     "Jesse H. Rhodes and Brian F. Schaffner",
     "Quarterly Journal of Political Science", "10.1561/100.00016077",
     "12(2): 185–204."),
    (2017, "misinformation-motivated-reasoning",
     "Misinformation and Motivated Reasoning: Responses to Economic News in a Politicized Environment",
     "Brian F. Schaffner and Cameron Roche",
     "Public Opinion Quarterly", "10.1093/poq/nfw043",
     "81(1): 86–110."),
    # 2015
    (2015, "distractions-survey",
     "Distractions: The Incidence and Consequences of Interruptions for Survey Respondents",
     "Stephen Ansolabehere and Brian F. Schaffner",
     "Journal of Survey Statistics and Methodology", "10.1093/jssam/smv003",
     "3(2): 216–239."),
    # 2014
    (2014, "survey-mode-still-matter",
     "Does Survey Mode Still Matter? Findings from a 2010 Multi-Mode Comparison",
     "Stephen Ansolabehere and Brian F. Schaffner",
     "Political Analysis", "10.1093/pan/mpt025",
     "22(3): 285–303."),
    (2014, "risk-attitudes-incumbency",
     "Risk Attitudes and the Incumbency Advantage",
     "David L. Eckles, Cindy D. Kam, Cherie Maestas, and Brian F. Schaffner",
     "Political Behavior", "10.1007/s11109-013-9258-9",
     "36(4): 731–749."),
    (2014, "campaign-finance-spending-bans",
     "The Effects of Campaign Finance Spending Bans on Electoral Outcomes: Evidence from the States",
     "Raymond J. La Raja and Brian F. Schaffner",
     "Electoral Studies", "10.1016/j.electstud.2013.08.002",
     "33: 102–114."),
    (2013, "ground-zero-mosque",
     "Support at Any Distance? The Role of Location and Prejudice in Public Opposition to the 'Ground Zero Mosque'",
     "Brian F. Schaffner",
     "PS: Political Science & Politics", "10.1017/S104909651300111X",
     "46(4): 753–759."),
    (2013, "targeted-campaign-appeals",
     "Targeted Campaign Appeals and the Value of Ambiguity",
     "Eitan D. Hersh and Brian F. Schaffner",
     "Journal of Politics", "10.1017/S0022381613000182",
     "75(2): 520–534."),
    (2013, "substance-and-symbolism",
     "Substance and Symbolism: Race, Ethnicity, and Campaign Appeals in the United States",
     "Tatishe Nteta and Brian F. Schaffner",
     "Political Communication", "10.1080/10584609.2012.737425",
     "30(2): 232–253."),
    (2011, "racial-salience-obama",
     "Racial Salience and the Obama Vote",
     "Brian F. Schaffner",
     "Political Psychology", "10.1111/j.1467-9221.2011.00848.x",
     "32(6): 963–988."),
    (2011, "risk-tolerance-military",
     "Risk Tolerance and Support for Potential Military Interventions",
     "David L. Eckles and Brian F. Schaffner",
     "Public Opinion Quarterly", "10.1093/poq/nfr022",
     "75(3): 533–544."),
    (2011, "financial-human-capital",
     "Assessing the Importance of Financial and Human Capital for Interest Group Sector Strength across American Communities",
     "Maryann Barakso, Jessica Gerrity, and Brian F. Schaffner",
     "British Journal of Political Science", "10.1017/S0007123411000032",
     "41(3): 557–580."),
    (2010, "residential-mobility-cell-only",
     "Residential Mobility, Family Structure, and the Cell-Only Population",
     "Stephen Ansolabehere and Brian F. Schaffner",
     "Public Opinion Quarterly", "10.1093/poq/nfq018",
     "74(2): 244–259."),
    (2008, "digital-divide-internet-voting",
     "Digital Divide or Just Another Absentee Ballot? Evaluating Internet Voting in the 2004 Michigan Democratic Primary",
     "Alicia Prevost and Brian F. Schaffner",
     "American Politics Research", "10.1177/1532673X08318586",
     "36(4): 510–529."),
    (2008, "exit-voice-interest-groups",
     "Exit, Voice, and Interest Group Governance",
     "Maryann Barakso and Brian F. Schaffner",
     "American Politics Research", "10.1177/1532673X07306545",
     "36(2): 186–209."),
    (2007, "winning-coverage-senate",
     "Winning Coverage in the U.S. Senate",
     "Patrick J. Sellers and Brian F. Schaffner",
     "Political Communication", "10.1080/10584600701641516",
     "24(4): 377–391."),
    (2007, "legislative-committees-representativeness",
     "Political Parties and the Representativeness of Legislative Committees",
     "Brian F. Schaffner",
     "Legislative Studies Quarterly", "10.3162/036298007781699672",
     "32(3): 475–497."),
    (2007, "republican-bias-nonpartisan",
     "A New Look at the Republican Bias in Nonpartisan Elections",
     "Brian F. Schaffner, Matthew J. Streb, and Gerald C. Wright",
     "Political Research Quarterly", "10.1177/1065912907301812",
     "60(2)."),
    (2006, "local-news-incumbency",
     "Local News Coverage and the Incumbency Advantage in the U.S. House",
     "Brian F. Schaffner",
     "Legislative Studies Quarterly", "10.3162/036298006X201904",
     "31(4): 491–511."),
    (2006, "winning-coverage-womens-movement",
     "Winning Coverage: News Media Portrayals of the Women's Movement, 1969–2004",
     "Maryann Barakso and Brian F. Schaffner",
     "Harvard International Journal of Press/Politics", None,
     "11(4)."),
    (2006, "geography-campaign-advertising",
     "The Political Geography of Campaign Advertising in U.S. House Elections",
     "Brian F. Schaffner",
     "Political Geography", None,
     "25(7): 775–788."),
    (2006, "sexual-identity-gap",
     "Rights or Benefits? Explaining the Sexual Identity Gap in American Political Behavior",
     "Brian F. Schaffner and Nenad Senic",
     "Political Research Quarterly", "10.1177/106591290605900111",
     "59(1): 123–132."),
    (2005, "priming-gender",
     "Priming Gender: Campaigning on Women's Issues in U.S. Senate Elections",
     "Brian F. Schaffner",
     "American Journal of Political Science", None,
     "49(4): 803–817."),
    (2004, "term-limits-redistricting",
     "Incumbents Out, Party In? Term Limits and Partisan Redistricting in State Legislatures",
     "Brian F. Schaffner, Michael W. Wagner, and Jonathan Winburn",
     "State Politics and Policy Quarterly", None,
     "4(4): 396–414."),
    (2004, "reinforcing-stereotypes",
     "Reinforcing Stereotypes? Race and Local Coverage of U.S. House Members",
     "Brian F. Schaffner and Mark Gadson",
     "Social Science Quarterly", "10.1111/j.0038-4941.2004.00235.x",
     "85(3)."),
    (2003, "senators-approval-ratings",
     "Tactical and Contextual Determinants of U.S. Senators' Approval Ratings",
     "Brian F. Schaffner, Wendy J. Schiller, and Patrick J. Sellers",
     "Legislative Studies Quarterly", None,
     "28(2): 203–223."),
    (2003, "structural-determinants-news",
     "The Structural Determinants of Local Congressional News Coverage",
     "Brian F. Schaffner and Patrick J. Sellers",
     "Political Communication", "10.1080/105846003901365",
     "20(1): 41–57."),
    (2002, "influence-of-party",
     "The Influence of Party: Evidence from the State Legislatures",
     "Gerald C. Wright and Brian F. Schaffner",
     "American Political Science Review", "10.1017/S0003055402000229",
     "96(2): 367–379."),
    (2002, "partisan-heuristic",
     "The Partisan Heuristic in Low-Information Elections",
     "Brian F. Schaffner and Matthew J. Streb",
     "Public Opinion Quarterly", "10.1086/343755",
     "66(4): 559–581."),
    (2001, "teams-without-uniforms",
     "Teams Without Uniforms: The Nonpartisan Ballot in State and Local Elections",
     "Brian F. Schaffner, Matthew J. Streb, and Gerald C. Wright",
     "Political Research Quarterly", "10.1177/106591290105400101",
     "54(1): 7–30."),
]


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


def write_publication(year, slug, title, authors, venue, doi, page_info):
    date = f"{year}-01-01"
    permalink = f"/publication/{date}-{slug}"
    if doi:
        paperurl = f"https://doi.org/{doi}"
    else:
        paperurl = ""

    citation_html = f"{authors}. ({year}). \"{title}.\" *{venue}* {page_info}"
    citation_safe = citation_html.replace('"', '&quot;')

    # Note: academicpages auto-renders "Published in {venue}, {year}" from the
    # YAML front-matter on both the listing page and the per-paper page. We
    # therefore deliberately omit the `excerpt` field (which would otherwise
    # appear as a second "Published in ..." line on the listing) and don't
    # repeat the venue/year in the body.

    body = f"""---
title: "{title}"
collection: publications
category: manuscripts
permalink: {permalink}
date: {date}
venue: '{venue}'
"""
    if paperurl:
        body += f"paperurl: '{paperurl}'\n"
    body += f"citation: '{citation_safe}'\n---\n\n"

    if doi:
        body += f"**[Read the paper (DOI)](https://doi.org/{doi})**\n"

    filename = f"_publications/{date}-{slug}.md"
    Path(filename).write_text(body, encoding="utf-8")
    return filename


def main():
    out_dir = Path("_publications")
    out_dir.mkdir(exist_ok=True)
    written = []
    for pub in PUBLICATIONS:
        written.append(write_publication(*pub))
    print(f"Wrote {len(written)} publication files to _publications/")
    for f in written:
        print(f"  {f}")


if __name__ == "__main__":
    main()
