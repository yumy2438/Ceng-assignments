package hw1;

public class PrintMathMLVisitor implements MathVisitor<String>{

	@Override
	public String visit(Op op) {
		// TODO Auto-generated method stub
		String firstst = op.getFirst().accept(this);
		String secondst = op.getSecond().accept(this);
		if(!op.getOperand().equals("/"))
		{
			String operand = op.getOperand();
			if(operand.equals("*"))
			{
				operand = "&times;";
			}
			else if(operand.equals("|-"))
			{
				operand = "&vdash;";
			}
			return "<mrow><mo>(</mo>"+firstst+"<mo>"+operand+"</mo>"+secondst+"<mo>)</mo></mrow>";
		}
		else
		{
			return "<mrow><mfrac>"+firstst+secondst+"</mfrac></mrow>";	
		}
	}

	@Override
	public String visit(Num num) {
		// TODO Auto-generated method stub
		return "<mrow><mn>"+num.getValue()+"</mn></mrow>";
	}

	@Override
	public String visit(Sym sym) {
		// TODO Auto-generated method stub
		return "<mrow><mi>"+sym.getValue()+"</mi></mrow>";
	}

	@Override
	public String visit(Var var) {
		// TODO Auto-generated method stub
		MathExpression me = var.getPreviousMatch();
		if(me != null)
		{
			return "<mrow><msub><mi>V</mi><mn>"+var.getId()+"</mn></msub><mo>[</mo>"+ var.getPreviousMatch().accept(this) + 
					"<mo>]</mo></mrow>";
		}
		else
		{
			return "<mrow><msub><mi>V</mi><mn>"+ var.getId() + 
					"</mn></msub></mrow>";
		}
	}
	
}
