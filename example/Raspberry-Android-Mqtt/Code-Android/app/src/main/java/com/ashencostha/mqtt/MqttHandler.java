package com.ashencostha.mqtt;

import android.content.Context;
import android.content.Intent;
import android.util.Log;


import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.json.JSONObject;

public class MqttHandler implements MqttCallback {
    public static final String BROKER_URL = "tcp://broker.emqx.io:1883";
    public static final String CLIENT_ID = "mqttx_f9bfd3ww";
    public static final String USER="";
    public static final String PASS="";


    public static final String TOPIC_SYSTEM_STATE  = "/system/state";
    public static final String TOPIC_MOVE_STATE    = "/move/state";
    public static final String TOPIC_CTRL_ALARM    = "/alarm/ctrl";
    public static final String TOPIC_STATE_ALARM   = "/alarm/state";
    public static final String TOPIC_CTRL_DOOR     = "/door/ctrl";
    public static final String TOPIC_STATE_DOOR    = "/door/state";

    public static final String ACTION_DATA_RECEIVE ="com.example.intentservice.intent.action.DATA_RECEIVE";
    public static final String ACTION_CONNECTION_LOST ="com.example.intentservice.intent.action.CONNECTION_LOST";
    private MqttClient client;
    private Context mContext;

    public MqttHandler(Context mContext){

        this.mContext = mContext;

    }

    public void connect( String brokerUrl, String clientId,String username, String password) {
        try {


            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);
            options.setUserName(username);
            options.setPassword(password.toCharArray());


            ///////////////////////////////////
            // Set up the persistence layer
            MemoryPersistence persistence = new MemoryPersistence();

            client = new MqttClient(brokerUrl, clientId, persistence);
             client.connect(options);

            client.setCallback(this);
            //client.subscribe("#");
        } catch (MqttException e) {
            Log.d("Aplicacion",e.getMessage()+ "  "+e.getCause());
        }
    }

    public void disconnect() {
        try {
            client.disconnect();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void publish(String topic, String message) {
        try {
            MqttMessage mqttMessage = new MqttMessage(message.getBytes());
            mqttMessage.setQos(2);
            client.publish(topic, mqttMessage);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void subscribe(String topic) {
        try {
            client.subscribe(topic);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void connectionLost(Throwable cause) {
        Log.d("MAIN ACTIVITY","conexion perdida"+ cause.getMessage().toString());

        Intent i = new Intent(ACTION_CONNECTION_LOST);
        mContext.sendBroadcast(i);
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {


        //Se envian los valores sensados por el potenciometro, al bradcast reciever de la activity principal
        Intent i = new Intent(ACTION_DATA_RECEIVE);
        i.putExtra("topic",topic);
        i.putExtra("msg", String.valueOf(message));

        mContext.sendBroadcast(i);


        
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {

    }
}
