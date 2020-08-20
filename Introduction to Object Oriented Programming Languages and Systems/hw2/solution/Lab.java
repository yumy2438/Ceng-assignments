package hw2;

import java.util.concurrent.*;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Lab {
	private String name;
	private int capacity;
	
	private Semaphore multiplex;
	private Condition emptyCondition;
	private String currentGroup;
	private int counter;
	// a lock variable for counter variable.
	private Lock lockCounter = new ReentrantLock();
	// a semaphore variable for preventing deadlock.
	private Semaphore turnstile = new Semaphore(1);
	
	
	public Lab(String name, int capacity)
	{
		this.name = name;
		this.capacity = capacity;
		
		//this semaphore variable for lab not to exceed the capacity
		this.multiplex = new Semaphore(capacity);
		
		//this integer variable holds how many students are in the lab information.
		this.counter = 0;
		
		//this string variable holds who is in the lab information.
		this.currentGroup = "";
		
		//a condition variable for lab to learn lab is occupied. 
		this.emptyCondition = lockCounter.newCondition();
	}
	
	// Necessary Getters 
	public String getName()
	{
		return name;
	}
	
	public int getCapacity()
	{
		return capacity;
	}
	
	public Semaphore getMultiplex()
	{
		return this.multiplex;
	}

	/*
	 * Study group that is given as groupname parameter occupies the lab if it can.
	 * First, I put a turnstile parameter. It prevents the deadlock.
	 * If there is no any study group that studies in the lab, currentgroup name will be set.
	 * If a study group rather than current one wants to study, they will wait emptyCondition variable.
	 * lockCounter is for synchronizing the counter variable.
	 */
	public void lock(String groupName)
	{	
		try {
			turnstile.acquire();
		} catch (InterruptedException e) {
			System.out.println(e);
		}
		this.lockCounter.lock();
		try
		{
			while(this.currentGroup != "" && !this.currentGroup.equals(groupName))
			{
				this.emptyCondition.await();
			}
			this.counter+=1;
			if(this.counter == 1)
			{
				this.currentGroup = groupName;
			}
		}catch(InterruptedException e)
		{
			System.out.println(e);
		}
		finally
		{
			this.lockCounter.unlock();
		}
		turnstile.release();
	}
	/*
	 * When a study group member wants to leave, this function will be called.
	 * It decreases the counter variable.
	 * If counter variable is 0, then it will set the currentGroup as empty and notify the emptyCondition variable.
	 */
	public void unlock()
	{
		this.lockCounter.lock();
		try
		{
			this.counter-=1;
			if(this.counter == 0)
			{
				this.currentGroup = "";
				this.emptyCondition.signal();
			}
		}
		finally
		{
			this.lockCounter.unlock();			
		}
	}
	
}
