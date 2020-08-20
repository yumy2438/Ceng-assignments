package hw1;

public class Num implements MathExpression{
	private int value;
	
	public Num(int value)
	{
		this.value = value;
	}
	
	public int getValue()
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
		if(me instanceof Num)
		{
			if (((Num) me).getValue() == this.value)
			{
				return true;
			}
		}
		return false;
	}
	
}
