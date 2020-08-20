package hw1;

public class XDotYDivXIsYRule implements Rule{
	private Var x;
	private Var y;
	private MathExpression premise;
	private MathExpression entail;
	
	public XDotYDivXIsYRule(Var x, Var y)
	{
		this.x = x;
		this.y = y;
		Op pre_op = new Op("*",this.x,this.y);
		this.premise = new Op("/",pre_op,this.x);
		this.entail = this.y;
	}

	public Var getX() {
		return x;
	}

	public Var getY() {
		return y;
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
