package hw1;

public class Var implements MathExpression{
	private int id;
	private MathExpression me;
	
	public Var(int id)
	{
		this.id = id;
		this.me = null;
	}
	
	public int getId()
	{
		return id;
	}
	
	public MathExpression getPreviousMatch()
	{
		return me;
	}
	
	public void setPreviousMatch(MathExpression me)
	{
		this.me = me;
	}

	@Override
	public <T> T accept(MathVisitor<T> visitor) {
		// TODO Auto-generated method stub
		return visitor.visit(this);
	}

	@Override
	public boolean match(MathExpression me) {
		// TODO Auto-generated method stub
		if(this.getPreviousMatch() == null)
		{
			this.setPreviousMatch(me);
			return true;
		}
		else
		{
			MathExpression this_prev = this.getPreviousMatch();
			return this_prev.match(me);
		}
	}
	

}
