from .__base__ import NaturalValuesNode

from .logic_ops import AndOp, OrOp
from .expr_ops import EqualOp, NotEqualOp, LessOp, LessOrEqualOp, GreatOp, GreatOrEqualOp
from .expr_ops import AddOp, SubOp, ModOp, DivOp, MultiOp
from .expr_ops import IndexSelf
from .atoms import GetAttr, GetItem
from .atoms import NaturalValue, SpaceSelfNode

"""
    NaturalValues := Cmp | Constraint
                  := Cmp & Constraint
                  := Cmp

             Expr := Expr == Expr 
             Expr := Expr != Expr 
             Expr := Expr >= Expr 
             Expr := Expr >  Expr 
             Expr := Expr <= Expr 
             Expr := Expr <  Expr 
          
             Expr := Expr + Expr
             Expr := Expr - Expr
             Expr := Expr * Expr
             Expr := Expr / Expr
             Expr := Expr % Expr
             
             Expr := Atom
             Expr := SelfIndex

             Atom := Atom[index]
             Atom := Atom[member]
             Atom := NaturalValue
             Atom := (Constraint)
             Atom := SpaceExpr
"""
