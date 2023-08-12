package ConnectToJava;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class Connect {
	public static void main(String[] args) {
		Results();
	}

	public static void Results(){
		try {
	        URL url = new URL("http://localhost:5000/getPredictions/aapl/5");
	        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
	        conn.setRequestMethod("GET");
	        conn.setRequestProperty("Accept", "application/json");
	
	        if (conn.getResponseCode() != 200) {
	            throw new RuntimeException("Failed : HTTP error code : "
	                    + conn.getResponseCode());
	        }
	
	        BufferedReader br = new BufferedReader(new InputStreamReader(
	                (conn.getInputStream())));
	
	        String output;
	        System.out.println("Output from Server .... \n");
	        while ((output = br.readLine()) != null) {
	            System.out.println(output);
	        }
            
	        conn.disconnect();
	
	    } catch (MalformedURLException e) {
	        e.printStackTrace();
	    } catch (IOException e){
	    	e.printStackTrace();
	    }
	}
}