# SAT-solver based on resolution method in 2-CNF using PLY

Given a Boolean formula in 2-CNF, use the resolution method to determine whether it is satisfiable. Clauses of the 2-CNF can be of one of the two forms: α \\/ β or α -> β, where α and β are literals (p or ~p, where p is a variable). The CNF is presented in the usual notation, for example: (p -> q) /\ (~r \\/ s) /\ (~q -> p)

# Example

```
$ python hw_ply.py
input > (p -> q) /\ (~r \/ s) /\ (~q -> p)

Resolution: (~p\/q)/\(~r\/s)/\(q\/p)/\(None\/q)
Satisfiable: True

input > (p->q) /\ (q->r) /\ (r->s) /\ p /\ ~s

Resolution: (~p\/q)/\(~q\/r)/\(~r\/s)/\(p\/None)/\(~s\/None)/\(~p\/r)/\(q\/None)/\(~q\/s)/\(~r\/None)/\(~p\/s)/\(r\/None)/\(~q\/None)/\(~p\/None)/\(None\/s)/\(None\/None)
Satisfiable: False
```

_HSE, Discrete Mathematics for Algorithm and Software Design_
