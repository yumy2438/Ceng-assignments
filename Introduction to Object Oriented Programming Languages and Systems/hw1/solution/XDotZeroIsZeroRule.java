package hw1;

public class XDotZeroIsZeroRule implements Rule{
	private Var x;
	private MathExpression premise;
	private MathExpression entail;
	public XDotZeroIsZeroRule(Var x)
	{
		this.x = x;
		Num num = new Num(0);
		this.premise = new Op("*",this.x,num);
		this.entail = new Num(0);
	}
	
	public Var getX()
	{
		return x;
	}

	@Override
	public MathExpression getPremise() {
		// TODO Auto-generated method stub
		return this.premise;
	}

	@Override
	public MathExpression getEntails() {
		// TODO Auto-generated method stub
		return this.entail;
	}

}
