<h1>r6stats</h1>
Date: 2021.03.06 <br>
Tool to convert the CSV-File form the <a href="https://r6analyst.com/">R6 ANALYST</a> to compact fileformat.
<br>
Goal to enable datasience not based on Excel
<h2>Installation</h2>

download git data
```
conda env create -n R6_datatool --file environment.yaml python=3.8.8
```
Change path in [addData.bat](https://github.com/MikeAlpaXRay/R6_datatool/blob/main/addData.bat) and if desired DEFAULT user, respectively.
In [user_constants.py](https://github.com/MikeAlpaXRay/R6_datatool/blob/main/user_constants.py) if desired change values of constants.
<br>

<h2>Maintenance</h2>
In [program_constants.py](https://github.com/MikeAlpaXRay/R6_datatool/blob/main/program_constants.py) it is possible to add new operators or change map pools.

<h2>Usage</h2>
Drag and Drop unaltered csv file into bat file. Enter the values according to the console output.

<h2>Datastructure</h2>
Data is saved in two files, via pickle. player data and team data respectively.

<h3>Playerdata</h3>
<details>
<summary>Click for details...</summary>
  
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
    
</details>
<h3>Teamobject</h3>
<details>
<summary>Click for details...</summary>

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
</details>
