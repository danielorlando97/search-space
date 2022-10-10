from .__base__ import UniversalVariableNode, AstRoot, UniversalVariableBinaryOperation
from .logic_ops import AndOp, OrOp
from .cmp_ops import EqualOp, NotEqualOp, LessOp, LessOrEqualOp, GreatOp, GreatOrEqualOp
from .expr_ops import AddOp, SubOp, MultiOp, DivOp
from .segmentation_branch import SegmentationAddOp, SegmentationSubOp, SegmentationMultiOp, SegmentationDivOp
from .segmentation_branch import SegmentationEqualOp, SegmentationNotEqualOp, SegmentationLessOp, SegmentationLessOrEqualOp, SegmentationGreatOp, SegmentationGreatOrEqualOp
from .segmentation_branch import SegmentationModOp, SegmentationExprNode
from .atoms import GetAttr, GetItem, NaturalValue, NotEvaluate, SelfNode, FunctionNode, AdvancedFunctionNode

"""
         Constraint := Cmp | Constraint
                    := Cmp & Constraint
                    := Cmp
                    := SegmentationExpr
 
                Cmp := Expr == Expr
                Cmp := Expr != Expr
                Cmp := Expr >= Expr
                Cmp := Expr > Expr
                Cmp := Expr <= Expr
                Cmp := Expr < Expr
                Cmp := Expr

   SegmentationExpr := SegmentationAtom == Expr
   SegmentationExpr := SegmentationAtom != Expr
   SegmentationExpr := SegmentationAtom <= Expr
   SegmentationExpr := SegmentationAtom < Expr
   SegmentationExpr := SegmentationAtom > Expr
   SegmentationExpr := SegmentationAtom >= Expr

   SegmentationAtom := SegmentationAtom + Expr  
   SegmentationAtom := SegmentationAtom - Expr  
   SegmentationAtom := SegmentationAtom * Expr  
   SegmentationAtom := SegmentationAtom / Expr  
   SegmentationAtom := SegmentationAtom % Expr  
   SegmentationAtom := Expr % Expr 


               Expr := Atom + Expr
               Expr := Atom - Expr
               Expr := Atom * Expr
               Expr := Atom / Expr
               Expr := Atom
     
               Atom := Atom[index]
               Atom := Atom[member]
               Atom := Self
               Atom := (Constraint)
               Atom := NaturalValue

       NaturalValue := FunctionCall
       NaturalValue := NaturalValuesAst
       NaturalValue := int, str, float, list .....

"""
