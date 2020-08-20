package hw1;

public class XPlusXIs2XRule implements Rule {
	private Var x;
	private MathExpression premise;
	private MathExpression entail;

	public XPlusXIs2XRule(Var x) {
		//super();
		this.x = x;
		this.premise = new Op("+",this.x,this.x);
		Num num = new Num(2);
		this.entail = new Op("*",num,this.x);
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
