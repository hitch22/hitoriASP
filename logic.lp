% R stands for Row, C stands for Column, N stands for Number
% Numbers 0~9 are valid inputs
num(0..9).
% The grid is made up of 5 rows and 5 cols, 5x5, 0 indexed
row(0..4).
col(0..4).

% For each squre, choose to be black or not(choice rule). Each cell has to be either black or not
0{black(R,C)}1 :- row(R), col(C).
c(R,C) :- cv(R,C,N).

% Handles duplicates. 2 cvs of the same row and different C of the same N are both white cannot be an answer(constraint)
% list all possibilities and C & C1 cannot be the same
:- cv(R,C,N), cv(R,C1,N), C!=C1, not black(R,C), not black(R,C1).
:- cv(R,C,N), cv(R1,C,N), R!=R1, not black(R,C), not black(R1,C).

% blacked out cells cannot be next to each other
:- black(R,C), black(R,C1), C1 = C+1, row(R), col(C), col(C1).
:- black(R,C), black(R,C1), C1 = C-1, row(R), col(C), col(C1).

:- black(R,C), black(R1,C), R1 = R+1, row(R), row(R1),  col(C).
:- black(R,C), black(R1,C), R1 = R-1, row(R), row(R1), col(C).

% continuous whites cells
continuous(R,C, R,C1) :- c(R,C), c(R,C1), C1=C+1,row(R), col(C), col(C1), not black(R,C), not black(R,C1).
continuous(R,C, R,C1) :- c(R,C), c(R,C1), C1=C-1,row(R), col(C), col(C1), not black(R,C), not black(R,C1).
continuous(R,C, R1,C) :- c(R,C), c(R1,C), R1=R+1, row(R), row(R1), col(C), not black(R,C), not black(R,C), not black(R1,C).
continuous(R,C, R1,C) :- c(R,C), c(R1,C), R1=R-1, row(R), row(R1), col(C), not black(R,C), not black(R,C), not black(R1,C).
% transitive connection
continuous(R1,C1,R2,C2) :- continuous(R1,C1,R3,C3), continuous(R2,C2,R3,C3).

% white cells have to be continuous
:- not continuous(R1,C1, R2,C2), row(R1), row(R2), col(C1), col(C2), not black(R1,C1), not black(R2,C2).

% set the solver to display only the black cells so that python will pick up the black coords exclusively and mark the interface black.
#show black/2.
