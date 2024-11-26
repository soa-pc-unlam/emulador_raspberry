package com.ashencostha.mqtt;


import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.RequiresApi;

import java.io.IOException;

import pl.droidsonroids.gif.GifDrawable;


public class MainActivity extends Activity  {


    private MqttHandler mqttHandler;

    private TextView txtDescription;

    private Switch swDoor;
    private Switch swAlarm;

    private ImageView imgDoor;
    private ImageView imgSiren;
    private GifDrawable gifDrawable;
    public IntentFilter filterReceive;
    public IntentFilter filterConncetionLost;
    private ReceptorOperacion receiver =new ReceptorOperacion();
    private ConnectionLost connectionLost =new ConnectionLost();

    @RequiresApi(api = Build.VERSION_CODES.TIRAMISU)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        try {
            txtDescription=(TextView)findViewById(R.id.txtDescription);
            swAlarm =(Switch) findViewById(R.id.swAlarm);
            swDoor  =(Switch) findViewById(R.id.swDoor);
            imgDoor =(ImageView) findViewById(R.id.imgDoor);
            imgSiren=(ImageView)findViewById(R.id.imgSiren);

            swDoor.setOnCheckedChangeListener(switchListener);
            swAlarm.setOnCheckedChangeListener(switchListener);
            imgDoor.setImageResource(R.drawable.close_door);

            mqttHandler = new MqttHandler(getApplicationContext());



            gifDrawable = new GifDrawable(getResources(), R.drawable.siren_alarm);

            imgSiren.setImageDrawable(gifDrawable);
            imgSiren.setVisibility(View.INVISIBLE);

            connect();

            configurarBroadcastReciever();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private void connect()

    {

        try {
            mqttHandler.connect(mqttHandler.BROKER_URL,mqttHandler.CLIENT_ID, mqttHandler.USER, mqttHandler.PASS);
            Thread.sleep(1000);
            subscribeToTopic(MqttHandler.TOPIC_MOVE_STATE);
            subscribeToTopic(MqttHandler.TOPIC_SYSTEM_STATE);
            subscribeToTopic(MqttHandler.TOPIC_STATE_ALARM);
            subscribeToTopic(MqttHandler.TOPIC_STATE_DOOR);

            Toast.makeText(this,"Conexion establecida",Toast.LENGTH_SHORT).show();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }



    }
    //Metodo que crea y configurar un broadcast receiver para comunicar el servicio que recibe los mensaje del servidor
    //con la activity principal
    @RequiresApi(api = Build.VERSION_CODES.TIRAMISU)
    private void configurarBroadcastReciever()
    {
        //se asocia(registra) la  accion RESPUESTA_OPERACION, para que cuando el Servicio de recepcion la ejecute
        //se invoque automaticamente el OnRecive del objeto receiver
        filterReceive = new IntentFilter(MqttHandler.ACTION_DATA_RECEIVE);
        filterConncetionLost = new IntentFilter(MqttHandler.ACTION_CONNECTION_LOST);

        filterReceive.addCategory(Intent.CATEGORY_DEFAULT);
        filterConncetionLost.addCategory(Intent.CATEGORY_DEFAULT);

        registerReceiver(receiver, filterReceive, Context.RECEIVER_NOT_EXPORTED);
        registerReceiver(connectionLost,filterConncetionLost, Context.RECEIVER_NOT_EXPORTED);

    }

    @Override
    protected void onDestroy() {
        mqttHandler.disconnect();
        super.onDestroy();
        unregisterReceiver(receiver);
    }
    private void publishMessage(String topic, String message){
       // Toast.makeText(this, "Publishing message: " + message, Toast.LENGTH_SHORT).show();
        mqttHandler.publish(topic,message);
    }
    private void subscribeToTopic(String topic){
       // Toast.makeText(this, "Subscribing to topic "+ topic, Toast.LENGTH_SHORT).show();
        mqttHandler.subscribe(topic);
    }

    //Metodo que actua como Listener de los eventos que ocurren en los componentes graficos de la activty
    CompoundButton.OnCheckedChangeListener switchListener = new CompoundButton.OnCheckedChangeListener() {
        @SuppressLint("NonConstantResourceId")
        @Override
        public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
            // Identificar el switch que cambió de estado
            switch (buttonView.getId()) {
                case R.id.swDoor:
                    if (isChecked) {
                        Toast.makeText(MainActivity.this, "Puerta abierta", Toast.LENGTH_SHORT).show();
                        imgDoor.setImageResource(R.drawable.open_door);
                        publishMessage(MqttHandler.TOPIC_CTRL_DOOR,"open");
                    } else {
                        Toast.makeText(MainActivity.this, "Puerta cerrada", Toast.LENGTH_SHORT).show();
                        imgDoor.setImageResource(R.drawable.close_door);
                        publishMessage(MqttHandler.TOPIC_CTRL_DOOR,"close");
                    }
                    break;

                case R.id.swAlarm:
                    if (isChecked) {
                        Toast.makeText(MainActivity.this, "Alarma activada", Toast.LENGTH_SHORT).show();
                        publishMessage(MqttHandler.TOPIC_CTRL_ALARM,"on");
                    } else {
                        Toast.makeText(MainActivity.this, "Alarma desactivada", Toast.LENGTH_SHORT).show();
                        txtDescription.setText("");
                        imgSiren.setVisibility(View.INVISIBLE);
                        gifDrawable.stop();
                        publishMessage(MqttHandler.TOPIC_CTRL_ALARM,"off");
                    }
                    break;
            }
        }
    };


    public class ConnectionLost extends BroadcastReceiver

    {

        public void onReceive(Context context, Intent intent) {

            Toast.makeText(getApplicationContext(),"Conexion Perdida",Toast.LENGTH_SHORT).show();

            connect();

        }

    }
    public class ReceptorOperacion extends BroadcastReceiver {
        public void onReceive(Context context, Intent intent) {
            try {
                String topic = intent.getStringExtra("topic");
                String msg = intent.getStringExtra("msg");

                switch (topic) {
                    case MqttHandler.TOPIC_MOVE_STATE:
                        txtDescription.setText("Movimiento detectado");
                        imgSiren.setVisibility(View.VISIBLE);
                        gifDrawable.start();

                        break;

                    case MqttHandler.TOPIC_STATE_ALARM:
                        swAlarm.setOnCheckedChangeListener(null); // Deshabilita temporalmente el listener
                        if("on".equals(msg))
                        {
                            swAlarm.setChecked(true);
                        }
                        else
                        {
                            swAlarm.setChecked(false);
                            txtDescription.setText("");
                            imgSiren.setVisibility(View.INVISIBLE);
                            gifDrawable.stop();
                        }
                        swAlarm.setOnCheckedChangeListener(switchListener); // Vuelve a habilitar el listener
                        break;

                    case MqttHandler.TOPIC_STATE_DOOR:
                        swDoor.setOnCheckedChangeListener(null); // Deshabilita temporalmente el listener

                        if ("open".equals(msg))
                        {
                            swDoor.setChecked(true); // Cambia el estado
                            imgDoor.setImageResource(R.drawable.open_door);
                        }else
                        {
                            swDoor.setChecked(false); // Cambia el estado
                            imgDoor.setImageResource(R.drawable.close_door);
                        }

                        swDoor.setOnCheckedChangeListener(switchListener); // Vuelve a habilitar el listener
                        break;

                    default:
                        break;
                }
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }

}
