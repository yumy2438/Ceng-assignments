package hw1;

public interface Rule {
	default void clear()
	{
		this.getPremise().accept(new ClearVarsVisitor());
		this.getEntails().accept(new ClearVarsVisitor());
	}
	default boolean apply(MathExpression me)
	{
		this.clear();
		boolean match_result = this.getPremise().match(me); // x+x
		if(!match_result)
		{
			this.clear();
		}
		return match_result;
	}

	MathExpression getPremise();
	MathExpression getEntails();
	default MathExpression entails(MathExpression me) {
		this.apply(me);
		return this.getEntails();
	}
	
}
