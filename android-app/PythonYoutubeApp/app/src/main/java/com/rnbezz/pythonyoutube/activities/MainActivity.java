package com.rnbezz.pythonyoutube.activities;

import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.preference.PreferenceManager;
import android.support.annotation.IntegerRes;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.rnbezz.pythonyoutube.R;
import com.rnbezz.pythonyoutube.service.SocketService;

public class MainActivity extends AppCompatActivity {

    public static final String PREF_KEY_SERVER_IP = "server_ip";
    public static final String PREF_KEY_SERVER_PORT = "server_port";

    private EditText serverAddr;
    private Button connectButton;
    private SharedPreferences sharedPreferences;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        serverAddr = (EditText) findViewById(R.id.activity_main_ip_addr);
        connectButton = (Button) findViewById(R.id.activity_main_btn_connect);

        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        if (sharedPreferences.contains(PREF_KEY_SERVER_IP) && sharedPreferences.contains(PREF_KEY_SERVER_PORT)){
            String ip = sharedPreferences.getString(MainActivity.PREF_KEY_SERVER_IP, "");
            int port = sharedPreferences.getInt(MainActivity.PREF_KEY_SERVER_PORT, -1);
            serverAddr.setText((CharSequence)(ip + ":" + port));
        }

        Intent intent = getIntent();
        String action = intent.getAction();
        String type = intent.getType();

        if (Intent.ACTION_SEND.equals(action) && type != null) {
            if ("text/plain".equals(type)) {
                handleSendText(intent);
            }
        }

        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String[] serverIPandPort = serverAddr.getText().toString().split(":");
                SharedPreferences.Editor editor = MainActivity.this.sharedPreferences.edit();
                editor.putString(PREF_KEY_SERVER_IP, serverIPandPort[0]);
                editor.putInt(PREF_KEY_SERVER_PORT, Integer.valueOf(serverIPandPort[1]));
                editor.apply();
            }
        });
    }

    void handleSendText(Intent intent) {
        String url = intent.getStringExtra(Intent.EXTRA_TEXT);

        if (url != null) {
            if (!url.contains("https") && !url.contains("http")) {
                Toast.makeText(this, "Invalid url: " + url, Toast.LENGTH_LONG).show();
                return;
            }
            if (!url.contains("youtube") && !url.contains("youtu.be")) {
                Toast.makeText(this, "Invalid url: " + url, Toast.LENGTH_LONG).show();
                return;
            }

            SocketService.startActionAddUrl(this, url);
            Toast.makeText(this, url, Toast.LENGTH_LONG).show();
        }
    }
}
