
cv(0,0,4).
cv(0,1,1).
cv(0,2,5).
cv(0,3,3).
cv(0,4,2).

cv(1,0,1).
cv(1,1,2).
cv(1,2,3).
cv(1,3,5).
cv(1,4,5).

cv(2,0,3).
cv(2,1,4).
cv(2,2,4).
cv(2,3,5).
cv(2,4,1).

cv(3,0,3).
cv(3,1,5).
cv(3,2,1).
cv(3,3,5).
cv(3,4,4).

cv(4,0,5).
cv(4,1,2).
cv(4,2,5).
cv(4,3,1).
cv(4,4,3).


%c(R,C) :- cv(R,C,V).
% numbers 0~9 are valid inputs
num(0..9).
% row and cols of 5x5, 0 indexed
row(0..4).
col(0..4).

% for each squre, choose to be black or not
% each cell has to be either black or not
0{black(R,C)}1 :- row(R), col(C).
c(R,C) :- cv(R,C,N).

% handles duplicates because 2 cvs with same Row and different C of the same N are both white cannot be an answer(constraint)
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

%*
black(1,1).
black(1,3).
black(2,2).
black(3,0).
black(3,3).
black(4,2).
*%
%:- not continuous(R,C1, R,C2), row(R), col(C1),col(C2).
%:- not continuous(R1,C, R2,C), row(R1), row(R2), col(C).




%#show black/2.
