import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Date;
import java.nio.file.Files;
import java.util.stream.Stream;
import java.io.IOException;
import java.text.DecimalFormat;

public class Covid
{
  // You can add your own variables between them.

  // You can add your own variables between them.

  // You must not change between them.
  private List<List<String>> rows;

  public Covid()
  {
    try
    {
      this.rows = Files
  				.lines(Paths.get("covid19.csv"))
  				.map(row -> Arrays.asList(row.split(",")))
  				.collect(Collectors.toList());
    }
    catch (IOException e)
    {
			e.printStackTrace();
		}
  }
  // You must not change between them.

  public void printOnlyCases(String location, String date)
  {  	
  	this.rows.stream().filter(e -> e.get(1).equals(location) && e.get(2).equals(date))
  						.mapToInt(e -> Integer.parseInt(e.get(3))-Integer.parseInt(e.get(5)))
  						.forEach(e -> System.out.printf("Result: %d", e));
  }

  public long getDateCount(String location)
  {
    long dateCount = this.rows.stream().filter(i -> i.get(1).equals(location))
    								.count();
    return dateCount;
  }

  public int getCaseSum(String date)
  {
    int sum = this.rows.stream().filter(i -> i.get(2).equals(date))
    								.mapToInt(e->Integer.parseInt(e.get(4)))
    								.sum();
    return sum;
  }

  public long getZeroRowsCount(String location)
  {
    long zeroRowsCount = this.rows.stream().filter(i -> i.get(1).equals(location) &&
					    							i.get(3).equals("0") && 
					    							i.get(4).equals("0") && 
					    							i.get(5).equals("0") && 
					    							i.get(6).equals("0"))
    									.count();
    return zeroRowsCount;
  }

  public double getAverageDeath(String location)
  {
    double averageDeath = this.rows.stream().filter(i -> i.get(1).equals(location))
    											.mapToDouble(e -> Double.parseDouble(e.get(6)))
    											.average().orElse(0.0);
    
    averageDeath = Double.parseDouble(new DecimalFormat("##.00").format(averageDeath));
    
    return averageDeath;
  }

  public String getFirstDeathDayInFirstTenRows(String location)
  {
    List<String> ans = (rows.stream().filter(i -> i.get(1).equals(location))
    									.limit(10)
    									.filter(i -> !i.get(6).equals("0"))
    									.findFirst()).orElse(null);
    return ans == null ? "Not Found" : ans.get(2);
  }

  public String[] getDateCountOfAllLocations()
  {
    String [] toReturn = this.rows.stream().map(e -> Arrays.asList(new String[] {e.get(0),e.get(1)}))
    										.distinct()
    										.map(e -> e.get(0) + ": "+  getDateCount(e.get(1)))
    										.collect(Collectors.toList())
    										.toArray(String[]::new);
    		
    return toReturn;
    
  }

  public List<String> getLocationsFirstDeathDay()
  {
    List<String> toReturn = this.rows.stream().filter(e -> e.get(5).equals(e.get(6)) && !e.get(5).equals("0"))
    		.map(e -> e.get(1) +": "+e.get(2))
    		.collect(Collectors.toList());
    return toReturn;
  }

  public String trimAndGetMax(String location, int trimCount)
  {
    String toReturn = null;
 
    toReturn = this.rows.stream().filter(e -> e.get(1).equals(location))
    					.sorted((e1,e2) -> new Integer(Integer.parseInt(e1.get(4))).compareTo(new Integer(Integer.parseInt(e2.get(4)))))
    					.skip(trimCount)
    					.sorted((e1,e2) -> new Integer(Integer.parseInt(e2.get(4))).compareTo(new Integer(Integer.parseInt(e1.get(4)))))
    					.skip(trimCount)
    					.sorted((e1,e2) -> new Integer(Integer.parseInt(e1.get(4))).compareTo(new Integer(Integer.parseInt(e2.get(4)))))
    					.max((e1,e2) -> new Integer(Integer.parseInt(e1.get(6))).compareTo(new Integer(Integer.parseInt(e2.get(6)))))
    					.map(e -> String.format("%s : %s", e.get(2),e.get(6)))
    					.orElse("Not Found");
    return toReturn;
  }

  public List<List<String>> getOnlyCaseUpDays(String location)
  {
    List<List<String>> toReturn = this.rows.stream().filter(e -> e.get(1).equals(location) && !e.get(4).equals("0"))
    							.collect(Collectors.toList());
    System.out.printf("Result: %d", toReturn.toArray().length);
    return toReturn;
  }

  public static void main(String[] args)
  {
  }
  
}
