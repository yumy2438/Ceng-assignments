package hw1;

public class Sym implements MathExpression{
	private String value;
	
	public Sym(String value)
	{
		this.value = value;
	}
	
	public String getValue()
	{
		return value;
	}

	@Override
	public <T> T accept(MathVisitor<T> visitor) {
		// TODO Auto-generated method stub
		return visitor.visit(this);
	}

	@Override
	public boolean match(MathExpression me) {
		// TODO Auto-generated method stub
		if(me instanceof Sym)
		{
			if(((Sym) me).getValue().equals(this.value))
			{
				return true;
			}
		}
		return false;
	}
	
	

}
