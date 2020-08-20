package hw1;

public class ClearVarsVisitor implements MathVisitor<Void>{

	@Override
	public Void visit(Op op) {
		// TODO Auto-generated method stub
		MathExpression me1 = op.getFirst();
		MathExpression me2 = op.getSecond();
		me1.accept(this);
		me2.accept(this);
		return null;
	}

	@Override
	public Void visit(Num num) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Void visit(Sym sym) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Void visit(Var var) {
		// TODO Auto-generated method stub
		var.setPreviousMatch(null);
		return null;
	}
	

}
