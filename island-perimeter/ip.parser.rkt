#lang brag
ip-program : "\n"* ip-row ("\n"+ ip-row)* "\n"*
ip-row : ip-whitespace* ip-cell* ip-vertical-wall ip-whitespace*
ip-cell : ip-vertical-wall ip-whitespace+ ip-mark ip-whitespace+
ip-whitespace : " "
ip-vertical-wall : "|"
ip-land : "X"
ip-water : " "
ip-mark : ip-land | ip-water
