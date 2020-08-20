package hw1;

import java.util.ArrayList;

public class PrintHTMLVisitor implements TextVisitor<String>{

	@Override
	public String visit(Document document) {
		// TODO Auto-generated method stub
		ArrayList<DocElement> doc_elements = document.getElements();
		String retStr = "<html><head><title>" + document.getTitle() + "</title></head><body>";
		for(DocElement doc_el: doc_elements)
		{
			retStr += doc_el.accept(this);
		}
		return retStr + "</body></html>";
	}

	@Override
	public String visit(EquationText equationText) {
		// TODO Auto-generated method stub
		return "<math>" + (equationText.getInnerMath().accept(new PrintMathMLVisitor())) + "</math>";
	}

	@Override
	public String visit(Paragraph paragraph) {
		// TODO Auto-generated method stub
		return "<p>" + paragraph.getText() + "</p>";
	}
	
}
