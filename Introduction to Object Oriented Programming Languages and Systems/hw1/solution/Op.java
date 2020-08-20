package hw1;

public class Op implements MathExpression {
	private String operand;
	private MathExpression first;
	private MathExpression second;
	
	public Op(String operand, MathExpression first, MathExpression second)
	{
		//Operand can be +,*,/,|-
		//MathExp can be num,sym or var
		this.operand = operand;
		this.first = first;//?
		this.second = second;//?
	}
	
	public String getOperand()
	{
		return operand;
	}
	
	public MathExpression getFirst()
	{
		return first;
	}
	
	public MathExpression getSecond()
	{
		return second;
	}
	
	@Override
	public <T> T accept(MathVisitor<T> visitor) {
		// TODO Auto-generated method stub
		return visitor.visit(this);
	}

	@Override
	public boolean match(MathExpression me) {
		// TODO Auto-generated method stub
		if (me instanceof Op)
		{
			Op meOp = (Op) me;
			String operandme = meOp.getOperand();
			if(this.operand.equals(operandme))
			{
				boolean res1 = this.first.match(meOp.first);
				boolean res2 = this.second.match(meOp.second);
				return (res1 && res2);
			}
		}
		return false;
	}

}
