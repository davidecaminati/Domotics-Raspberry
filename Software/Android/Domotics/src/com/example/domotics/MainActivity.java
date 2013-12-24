package com.example.domotics;


import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Button;
import android.view.View;
import android.view.View.OnClickListener;

public class MainActivity extends Activity {

	Button buttonSalaON,buttonCucinaON,buttonIngressoON,buttonSalaOFF,buttonCucinaOFF,buttonIngressoOFF;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		addListenerOnButton();

	}
		public void addListenerOnButton() {

			buttonSalaON = (Button) findViewById(R.id.button1);
			buttonCucinaON = (Button) findViewById(R.id.button2);
			buttonIngressoON = (Button) findViewById(R.id.button3);

			buttonSalaOFF = (Button) findViewById(R.id.button4);
			buttonCucinaOFF = (Button) findViewById(R.id.button5);
			buttonIngressoOFF = (Button) findViewById(R.id.button6);
			

			buttonSalaON.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View arg0) {
					  	Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releon/5"));
					    startActivity(browserIntent);
					}
				});	 
			
			buttonCucinaON.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View arg0) {
						Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releon/4"));
						startActivity(browserIntent);
					}
				});	 
			
			buttonIngressoON.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View arg0) {
						Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releon/3"));
						startActivity(browserIntent);
					}
				});
			buttonSalaOFF.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View arg0) {
					  	Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/5"));
					    startActivity(browserIntent);
					}
				});	 
			
			buttonCucinaOFF.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View arg0) {
						Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/4"));
						startActivity(browserIntent);
					}
				});	 
			
			buttonIngressoOFF.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View arg0) {
						Intent browserIntent =  new Intent(Intent.ACTION_VIEW, Uri.parse("http://192.168.0.202:5000/releoff/3"));
						startActivity(browserIntent);
					}
				});
		}

}
