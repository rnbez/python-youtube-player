package com.rnbezz.pythonyoutube.service;

import android.app.IntentService;
import android.content.Intent;
import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.util.Log;
import android.widget.Toast;

import com.rnbezz.pythonyoutube.activities.MainActivity;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

/**
 * An {@link IntentService} subclass for handling asynchronous task requests in
 * a service on a separate handler thread.
 * <p>
 * TODO: Customize class - update intent actions, extra parameters and static
 * helper methods.
 */
public class SocketService extends IntentService {
    private static final String ACTION_ADD_URL = "com.rnbezz.pythonyoutube.service.action.ADD_URL";

    private static final String EXTRA_SERVER_IP = "com.rnbezz.pythonyoutube.service.extra.SERVER_IP";
    private static final String EXTRA_SERVER_PORT = "com.rnbezz.pythonyoutube.service.extra.SERVER_PORT";
    private static final String EXTRA_ADD_URL = "com.rnbezz.pythonyoutube.service.extra.ADD_URL";

    private static final String COMMAND_ADD_URL = "/add ";

//    private static final String SERVER_IP = "155.246.216.116";
//    private static final int SERVER_PORT = 9999;


    public SocketService() {
        super("SocketService");
    }

    /**
     * Starts this service to perform action Foo with the given parameters. If
     * the service is already performing a task this action will be queued.
     *
     * @see IntentService
     */
    // TODO: Customize helper method
    public static void startActionAddUrl(Context context, String url) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(context);
        String ip = prefs.getString(MainActivity.PREF_KEY_SERVER_IP, "");
        int port = prefs.getInt(MainActivity.PREF_KEY_SERVER_PORT, -1);

        if (ip.isEmpty() || port == -1){
            Toast.makeText(context, "You must provide a valid IP addres and Port", Toast.LENGTH_LONG).show();
            return;
        }

        Intent intent = new Intent(context, SocketService.class);
        intent.setAction(ACTION_ADD_URL);
        intent.putExtra(EXTRA_ADD_URL, url);
        intent.putExtra(EXTRA_SERVER_IP, ip);
        intent.putExtra(EXTRA_SERVER_PORT, port);
        context.startService(intent);
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        if (intent != null) {
            final String action = intent.getAction();
            if (ACTION_ADD_URL.equals(action)) {
                final String url = intent.getStringExtra(EXTRA_ADD_URL);
                String ip = intent.getStringExtra(EXTRA_SERVER_IP);
                int port = intent.getIntExtra(EXTRA_SERVER_PORT, 0);
                String response = send(ip, port, COMMAND_ADD_URL + url);
                Log.d("socket", response.replace(COMMAND_ADD_URL, ""));

            }
//            else if (ACTION_BAZ.equals(action)) {
//                final String param1 = intent.getStringExtra(EXTRA_ADD_URL);
//                final String param2 = intent.getStringExtra(EXTRA_PARAM2);
////                handleActionBaz(param1, param2);
//            }
        }
    }

    /**
     * Handle action Foo in the provided background thread with the provided
     * parameters.
     */
    private String send(String ip, int port, String message) {
        // TODO: Handle action Foo

        Socket socket = null;

        try {

            InetAddress serverAddr = InetAddress.getByName(ip);

            if (serverAddr != null) {
                socket = new Socket(serverAddr, port);
                PrintWriter out = new PrintWriter(
                        new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())),
                        true);


                BufferedReader in =
                        new BufferedReader(
                                new InputStreamReader(socket.getInputStream(), "UTF-8"));


                out.println(message);
                char[] receiveData = new char[1024 * 4];
                in.read(receiveData, 0, 1024 * 4);
                String response = String.valueOf(receiveData);
                Log.d("socket",response);
                return response;
            }

        } catch (UnknownHostException e1) {
            e1.printStackTrace();
        } catch (IOException e1) {
            e1.printStackTrace();
        }
        finally{
            if (socket != null)
                try {
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
        }
        return "";
    }
}
