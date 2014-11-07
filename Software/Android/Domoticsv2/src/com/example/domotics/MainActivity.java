package com.example.domotics;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
//import android.os.RemoteException;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
//import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.EditText;

import java.io.InputStream;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
//import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
//import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;

//import com.authorwjf.http_get.R;
//import com.authorwjf.http_get.Main.LongRunningGetIO;



import java.io.IOException;


public class MainActivity extends Activity  {

	Button buttonPCOFF, buttonPorta,buttonDimmerSala2,buttonSala1ON,buttonSala2ON,buttonCucinaON,buttonIngressoON,buttonSala1OFF,buttonSala2OFF,buttonCucinaOFF,buttonIngressoOFF;
	SeekBar DimmerTime;
	TextView pippo;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		addListenerOnButton();

		}
	
		public void addListenerOnButton() {

			DimmerTime = (SeekBar) findViewById(R.id.seekBar1);
			pippo = (TextView) findViewById(R.id.textView1);

			buttonPorta = (Button) findViewById(R.id.button7);

			buttonPCOFF = (Button) findViewById(R.id.button10);
			
			

			buttonSala1ON = (Button) findViewById(R.id.button1);
			buttonSala2ON = (Button) findViewById(R.id.button8);
			buttonCucinaON = (Button) findViewById(R.id.button2);
			buttonIngressoON = (Button) findViewById(R.id.button3);

			buttonSala1OFF = (Button) findViewById(R.id.button4);
			buttonSala2OFF = (Button) findViewById(R.id.button9);
			buttonCucinaOFF = (Button) findViewById(R.id.button5);
			buttonIngressoOFF = (Button) findViewById(R.id.button6);
			buttonDimmerSala2 = (Button) findViewById(R.id.button11);
			

			buttonPorta.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
				  	//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/reletimer/8/500"));
				    //startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/reletimer/8/500");
				}
			});	 

			buttonSala1ON.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
				  	//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releon/5"));
				    //startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/releon/5");
				}
			});	 
			
			buttonSala2ON.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
				  	//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releon/5"));
				    //startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/releon/1");
				}
			});	 
			
			buttonCucinaON.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
					//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releon/4"));
					//startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/releon/4");
				}
			});	 
			
			buttonIngressoON.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
					//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releon/3"));
					//startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/releon/3");
				}
			});

			buttonSala1OFF.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
				  	//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/5"));
				    //startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/releoff/5");
				}
			});	 
			
			buttonSala2OFF.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
				  	//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/5"));
				    //startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/releoff/1");
				}
			});	 

			buttonCucinaOFF.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
					//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/4"));
					//startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/releoff/4");
				}
			});	 
			
			buttonDimmerSala2.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
					//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/4"));
					//startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/reletimer/6/" + DimmerTime.getProgress());
				}
			});	 
			
			
			buttonPCOFF.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
					//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/4"));
					//startActivity(browserIntent);
				new LongRunningGetIO().execute("http://192.168.0.86:5000/shutdown");
				}
			});	
			
			
			
			buttonIngressoOFF.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
					//Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/3"));
					//startActivity(browserIntent);

				//EditText et = (EditText)findViewById(R.id.editText1);
				//new LongRunningGetIO().execute();
				
				
				//Button b = (Button)findViewById(R.id.button6);
				//b.setClickable(false);
				new LongRunningGetIO().execute("http://192.168.0.202:5000/releoff/3");

				}
			});
		}
		
		private class LongRunningGetIO extends AsyncTask <String, Integer, String> {
			
			protected String getASCIIContentFromEntity(HttpEntity entity) throws IllegalStateException, IOException {

			InputStream in = entity.getContent();
			StringBuffer out = new StringBuffer();
			int n = 1;
			while (n>0) 
			{
				byte[] b = new byte[4096];
		
				n =  in.read(b);
		
				if (n>0) out.append(new String(b, 0, n));
			}
			return out.toString();
	
		}							


		@Override
		protected String doInBackground(String... urls) {
			String text = null;

			HttpClient httpClient = new DefaultHttpClient();
			HttpContext localContext = new BasicHttpContext();
			HttpGet httpGet = new HttpGet(urls[0]);
			
			try 
			{
				HttpResponse response = httpClient.execute(httpGet, localContext);
			    HttpEntity entity = response.getEntity();
			    text = getASCIIContentFromEntity(entity);
			} 
			catch (Exception e) 
			{
				return e.getMessage();
			}
			return text;
		}
		
		@Override
		protected void onPostExecute(String results) {
			if (results!=null) {
				//EditText et = (EditText)findViewById(R.id.editText1);
				pippo.setText(results);
			}
		}
	}
}

