package hw1;

public class EquationText implements DocElement{
	MathExpression innerMath;
	
	public EquationText(MathExpression innerMath)
	{
		this.innerMath = innerMath;
	}
	
	public MathExpression getInnerMath() {
		return innerMath;
	}

	@Override
	public <T> T accept(TextVisitor<T> visitor) {
		// TODO Auto-generated method stub
		return visitor.visit(this);
	}

}
