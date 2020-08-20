package hw1;

public class CountAtomicsVisitor implements MathVisitor<Integer>{

	@Override
	public Integer visit(Op op) {
		// TODO Auto-generated method stub
		MathExpression first = op.getFirst();
		MathExpression second = op.getSecond();
		int numOfExp1 = first.accept(this);
		int numOfExp2 = second.accept(this);
		return numOfExp1+numOfExp2;
	}

	@Override
	public Integer visit(Num num) {
		// TODO Auto-generated method stub
		return 1;
	}

	@Override
	public Integer visit(Sym sym) {
		// TODO Auto-generated method stub
		return 1;
	}

	@Override
	public Integer visit(Var var) {
		// TODO Auto-generated method stub
		return 1;
	}
	
}
