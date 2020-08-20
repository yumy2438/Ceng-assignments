package hw1;

import java.util.ArrayList;

public class Document implements DocElement {
	private String title;
	private ArrayList<DocElement> docList;

	public Document(String title) {
		//super();
		docList = new ArrayList<DocElement>();
		this.title = title;
	}
	
	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}
	
	public ArrayList<DocElement> getElements()
	{
		return docList;
	}
	
	public void setElements(ArrayList<DocElement> arr)
	{
		//the collection is reset tot the elements inside arr
		docList.clear();
		for(DocElement docElement: arr)
		{
			docList.add(docElement);
		}
	}
	
	public void add(DocElement de)
	{
		//adds me to the colelction
		docList.add(de);
	}

	@Override
	public <T> T accept(TextVisitor<T> visitor) {
		// TODO Auto-generated method stub
		return visitor.visit(this);
	}
	


}
