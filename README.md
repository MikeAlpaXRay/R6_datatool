<h1>r6stats</h1>
Date: 2021.03.06 <br>
Tool to convert the CSV-File form the <a href="https://r6analyst.com/">R6 ANALYST</a> to compact fileformat.
<br>
Goal to enable datasience not based on Excel
<h2>Datastructure</h2>
Data is saved in two files. player data and team data respectively.

<h3>Playerdata (once per Player in Match)</h3>

- name (string)
- matches (Pandas Dataframe)
  - Match ID
  - Timestamp
  - Winner
  - Player Rating
  - ATK Rating
  - DEF Rating
  - KOST
  - KPR
  - SRV
  - Kills
  - Refrags
  - Headshots
  - Underdog Kills
  - 1vX
  - Multikill Rounds
  - Deaths
  - Traded
  - Deaths
  - Traded by Enemy
  - Opening Kills
  - Opening Deaths
  - Entry Kills
  - Entry Deaths
  - Planted Defuser
  - Disabled Defuser
  - Teamkills
  - Teamkilled
    
<h3>Teamobject (once per Team in Match)</h3>

- name (string)
- matches (Pandas Dataframe)
  - Match ID
  - Timestamp
  - Gamemode
  - Comp Info
  - Banned Map
  - Banned Op
  - Map
  - Outcome
  - Own Score
  - Enemy Score
  - Rounds (Pandas Dataframe)
    - Round(Index)
    - Site
    - Side
    - Result
    - Victory Type
    - _Operatorstats (Pandas Dataframe)_
      - _Player_
      - _Operator_
