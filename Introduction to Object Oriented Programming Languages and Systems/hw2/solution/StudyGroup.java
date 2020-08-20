package hw2;

public class StudyGroup {

	private String name;
	private Lab lab;
	
	
	public StudyGroup(String name, Lab lab)
	{
		this.name = name;
		this.lab = lab;
	}
	
	public String getName()
	{
		return name;
	}

	public Lab getLab()
	{
		return lab;
	}
	
	/*
	 * To start study in the lab lock function is called from the Lab class. The necessary explanations for it in the Lab class
	 * multiplex semaphore is for not to exceed the capacity of the lab.
	 * when a new student starts studying, the semaphore will be acquired until it allows.
	 */
	public void startStudyingWith()
	{
		try
		{
			this.lab.lock(this.name);
			this.lab.getMultiplex().acquire();			
		}
		catch(InterruptedException e)
		{
			System.out.println(e);
		}
		
	}
	/*
	 * To stop studying in the lab, unlock function is called from the Lab class. The necessary explanations for it in the Lab class.
	 * multiplex semaphore is for not to exceed the capacity of the lab.
	 * when the student stops studying, the semaphore will be released.
	 */
	public void stopStudyingWith()
	{
		this.lab.unlock();
		this.lab.getMultiplex().release();
	}
}

