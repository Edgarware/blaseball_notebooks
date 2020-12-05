"""
Helper functions to display Player info in Jupyter Notebooks
"""
from blaseball_mike.models import SimulationData, Player
from statistics import mean
import blaseball_reference.api as datablase
from IPython.display import HTML, display
from utils import *
from matplotlib import pyplot

def display_vibes(player, day=None):
    if not day:
        day = SimulationData.load().day + 1

    vibe = player.get_vibe(day)
    print(vibe_to_string(vibe))

def display_season_vibes(player):
    days = range(1, 100)
    if isinstance(player, list):
        vibes = [mean([y.get_vibe(x) for y in player]) for x in days]
    else:
        vibes = [player.get_vibe(x) for x in days]

    pyplot.plot(days, vibes)
    pyplot.axline(xy1=(1, 0.8), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1, 0.4), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1, 0.1), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1, -0.1), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1, -0.4), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1,-0.8), slope=0, linestyle=":", color="#888")
    pyplot.yticks(ticks=[0.9, 0.6, 0.25, 0, -0.25, -0.6, -0.9], labels=["Most Excellent", "Excellent", "Quality", "Neutral", "Less Than Ideal", "Far Less Than Ideal", "Honestly Terrible"])
    pyplot.xlabel("Day")
    pyplot.show()

def get_stars(values):
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]
    return pandas.DataFrame([{"Name":x.name, "Batting": x.batting_stars, "Pitching":x.pitching_stars,
                              "Baserunning":x.baserunning_stars, "Defense":x.defense_stars} for x in values]).set_index("Name")

def get_batting_stats(values, season=None):
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        ids = [x.id for x in values]
    else:
        ids = values.id

    if season:
        season = season - 1

    ret = datablase.player_stats(ids, "batting", season)
    return pandas.DataFrame(ret).set_index("player_id")

def get_pitching_stats(values, season=None):
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        ids = [x.id for x in values]
    else:
        ids = values.id

    if season:
        season = season - 1

    ret = datablase.player_stats(ids, "pitching", season)
    return pandas.DataFrame(ret).set_index("player_id")

def get_batting_stlats(values):
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    return pandas.DataFrame([{"Name": x.name, "Batting Rating": x.hitting_rating, "Buoyancy":x.buoyancy,
                                       "Divinity": x.divinity, "Martyrdom": x.martyrdom, "Moxie": x.moxie,
                                       "Musclitude": x.musclitude, "Patheticism": x.patheticism,
                                       "Thwackability": x.thwackability} for x in values]).set_index("Name")

def get_pitching_stlats(values):
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    return pandas.DataFrame([{"Name": x.name, "Pitching Rating": x.pitching_rating, "Coldness": x.coldness,
                                       "Overpowerment": x.overpowerment, "Ruthlessness": x.ruthlessness,
                                       "Shakespearianism": x.shakespearianism, "Suppression": x.suppression,
                                       "Unthwackability": x.unthwackability,
                                       "Number of Fingers": x.total_fingers} for x in values]).set_index("Name")

def get_baserunning_stlats(values):
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    return pandas.DataFrame([{"Name": x.name, "Baserunning Rating": x.baserunning_rating,
                                       "Base Thirst": x.base_thirst, "Continuation": x.continuation,
                                       "Ground Friction": x.ground_friction, "Indulgence": x.indulgence,
                                       "Laserlikeness": x.laserlikeness} for x in values]).set_index("Name")

def get_defense_stlats(values):
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    return pandas.DataFrame([{"Name": x.name, "Defense Rating": x.defense_rating,
                                       "Anticapitalism": x.anticapitalism, "Chasiness": x.chasiness,
                                       "Omniscience": x.omniscience, "Tenaciousness": x.tenaciousness,
                                       "Watchfulness": x.watchfulness} for x in values]).set_index("Name")

def _html_attr(attr_list, border_color):
    ret = ""
    for attr in attr_list:
        ret += \
            f"""
            <div style="font-weight:700;display:flex;margin-right:10px;padding-left:5px;padding-right:5px;height:32px;border-radius:5px;align-items:center;justify-content:center;color:{attr.color};background:{attr.background} none repeat scroll 0% 0%;border:2px solid {border_color}">
                {attr.title}
            </div>
        """
    return ret

def display_player(player, day=None):
    if not isinstance(player, Player):
        return

    if not day:
        sim = SimulationData.load()
        day = sim.day + 1

    retired = "RETIRED" in player._perm_attr_ids

    player_team = ""
    if player.league_team and not retired:
        player_team = f"""
            <div style="display:flex;flex-direction:row;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <div style="font-size:18px;display:flex;align-items:center;border-radius:50%;height:30px;width:30px;justify-content:center;flex-shrink:0;background-color:{player.league_team.main_color};">
                    {parse_emoji(player.league_team.emoji)}
                </div>
                <div style="padding:0 10px;">
                    {player.league_team.full_name}
                </div>
            </div>"""

    if retired or "COFFEE_EXIT" in player._perm_attr_ids:
        soul_name = "Soulsong"
    else:
        soul_name = "Soulscream"

    if retired:
        soul_color = "#5988ff"
    else:
        soul_color = "#F00"

    vibe = player.get_vibe(day)

    if player.deceased:
        player_status = f"""<div style="padding:15px 40px;display:flex;flex-direction:row;justify-content:space-between;align-items:center;background:#111;border-bottom:1px solid #fff;">
            <div style="padding:0 10px;display:flex;align-items:center;font-size:18px;">
                Deceased
            </div>
        </div>"""
    else:
        player_status = ""

    # ATTRIBUTES
    player_attributes = ""
    if len(player.perm_attr) > 0 or len(player.seas_attr) > 0 or len(player.week_attr) > 0 or len(player.game_attr) > 0 or player.bat.attr or player.armor.attr:
        player_attributes += """<div style="padding:5px 40px;display:flex;flex-direction:row;background:#111;border-bottom:1px solid #fff;">
        <div style="display:flex;flex-direction:row;padding:5px;border-radius:5px;background:#222;">"""
        if len(player.perm_attr) > 0:
            player_attributes += _html_attr(player.perm_attr, "#dbbc0b")
        if len(player.seas_attr) > 0:
            player_attributes += _html_attr(player.seas_attr, "#c2157a")
        if len(player.week_attr) > 0:
            player_attributes += _html_attr(player.week_attr, "#0a78a3")
        if len(player.game_attr) > 0:
            player_attributes += _html_attr(player.game_attr, "#639e47")
        if player.bat.attr:
            player_attributes += _html_attr([player.bat.attr], "#bababa")
        if player.armor.attr:
            player_attributes += _html_attr([player.armor.attr], "#bababa")
        player_attributes += "</div></div>"

    html = f"""
    <div style="width:500px;background:#000;border:1px solid #fff;color:#fff;display:flex;flex-direction:column;box-sizing:border-box;font-size:14px;">
        <div style="border-bottom:1px solid #fff;display:flex;flex-direction:column;align-items:flex-start;justify-content:space-between;padding:40px 40px 20px;">
            <div style="font-size:24px;">
                {player.name}
            </div>
            {player_team}
        </div>
        {player_status}
        {player_attributes}
        <div style="padding:20px 0;">
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Current Vibe
                </div>
                <span style="color:{vibe_to_color(vibe)};">
                    {vibe_to_string(vibe)}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    Batting
                </div>
                <span>
                    {stars_to_string(player.batting_stars)}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Pitching
                </div>
                <span>
                    {stars_to_string(player.pitching_stars)}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    Baserunning
                </div>
                <span>
                    {stars_to_string(player.baserunning_stars)}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Defense
                </div>
                <span>
                    {stars_to_string(player.defense_stars)}
                </span>
            </div>
            <div style="padding:10px;40px;display:flex;flex-direction:row;justify-content:space-around;">
                <div style="display:flex;flex-direction:column;justify-content:space-between;align-items:center;width:auto;min-width:150px;height:80px;margin:5px;padding:10px 0;background:#111;border-radius:5px;">
                    <div style="font-weight:700;">
                        ITEM
                    </div>
                    <div>
                        {player.bat.name}
                    </div>
                </div>
                <div style="display:flex;flex-direction:column;justify-content:space-between;align-items:center;width:auto;min-width:150px;height:80px;margin:5px;padding:10px 0;background:#111;border-radius:5px;">
                    <div style="font-weight:700;">
                        ARMOR
                    </div>
                    <div>
                        {player.armor.name}
                    </div>
                </div>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Evolution
                </div>
                <span>
                    Base
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    Pregame Ritual
                </div>
                <span>
                    {player.ritual}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Coffee Style
                </div>
                <span>
                    {player.coffee}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    Blood Type
                </div>
                <span>
                    {player.blood}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Fate
                </div>
                <span>
                    {player.fate}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    {soul_name}
                </div>
                <span style="max-width:240px;height:auto;border-radius:5px;font-size:16px;font-weight:700;font-style:italic;word-wrap:break-word;color:{soul_color}">
                    {player.soulscream[0:110]}
                </span>
            </div>
        </div>
    </div>
    """

    display(HTML(html))