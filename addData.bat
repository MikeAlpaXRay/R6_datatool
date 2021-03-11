:: Activates Python Enviroment
call conda activate R6_datatool
:: python "Filepath\add_data.py" %* USER
:: Change to personal Filepath
:: Change USER to desired username
python "E:\Cloud\Drive\Engines Rainbow Six\4_Stats\1_R6_datattool\add_data.py" %* DEFAULT
call conda deactivate
pause

