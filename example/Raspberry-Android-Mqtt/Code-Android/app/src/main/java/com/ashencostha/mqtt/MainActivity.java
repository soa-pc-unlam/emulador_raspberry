package com.ashencostha.mqtt;


import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends Activity  {


    private MqttHandler mqttHandler;

    private TextView txtJson;
    private TextView txtTemp;
    private Button cmdLedApagar;
    private Button cmdLedEncender;

    public IntentFilter filterReceive;
    public IntentFilter filterConncetionLost;
    private ReceptorOperacion receiver =new ReceptorOperacion();
    private ConnectionLost connectionLost =new ConnectionLost();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txtJson=(TextView)findViewById(R.id.txtJson);
        txtTemp=(TextView)findViewById(R.id.txtValorTemp);
        cmdLedApagar =(Button)findViewById(R.id.cmdLedApagar);
        cmdLedEncender =(Button)findViewById(R.id.cmdLedEncender);

        cmdLedApagar.setOnClickListener(botonesListeners);
        cmdLedEncender.setOnClickListener(botonesListeners);

        mqttHandler = new MqttHandler(getApplicationContext());

        connect();

        configurarBroadcastReciever();
    }

    private void connect()
    {
        mqttHandler.connect(mqttHandler.BROKER_URL,mqttHandler.CLIENT_ID, mqttHandler.USER, mqttHandler.PASS);


        try {

            Thread.sleep(1000);
            //subscribeToTopic(MqttHandler.TOPIC_BOTON);
            subscribeToTopic(MqttHandler.TOPIC_TEMPERATURA);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }



    }
    //Metodo que crea y configurar un broadcast receiver para comunicar el servicio que recibe los mensaje del servidor
    //con la activity principal
    private void configurarBroadcastReciever()
    {
        //se asocia(registra) la  accion RESPUESTA_OPERACION, para que cuando el Servicio de recepcion la ejecute
        //se invoque automaticamente el OnRecive del objeto receiver
        filterReceive = new IntentFilter(MqttHandler.ACTION_DATA_RECEIVE);
        filterConncetionLost = new IntentFilter(MqttHandler.ACTION_CONNECTION_LOST);

        filterReceive.addCategory(Intent.CATEGORY_DEFAULT);
        filterConncetionLost.addCategory(Intent.CATEGORY_DEFAULT);

        registerReceiver(receiver, filterReceive);
        registerReceiver(connectionLost,filterConncetionLost);

    }

    @Override
    protected void onDestroy() {
        mqttHandler.disconnect();
        super.onDestroy();
        unregisterReceiver(receiver);
    }
    private void publishMessage(String topic, String message){
        Toast.makeText(this, "Publishing message: " + message, Toast.LENGTH_SHORT).show();
        mqttHandler.publish(topic,message);
    }
    private void subscribeToTopic(String topic){
        Toast.makeText(this, "Subscribing to topic "+ topic, Toast.LENGTH_SHORT).show();
        mqttHandler.subscribe(topic);
    }

    //Metodo que actua como Listener de los eventos que ocurren en los componentes graficos de la activty
    private View.OnClickListener botonesListeners = new View.OnClickListener() {
        @Override
        public void onClick(View view) {

            switch (view.getId())
            {
                //Si se ocurrio un evento en el boton OK
                case R.id.cmdLedApagar:
                    publishMessage(MqttHandler.TOPIC_LUZ,"0");

                    break;
                case R.id.cmdLedEncender:
                    publishMessage(MqttHandler.TOPIC_LUZ,"1");

                    break;
                default:
                    Toast.makeText(getApplicationContext(),"Error en Listener de botones",Toast.LENGTH_LONG).show();
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

            //Se obtiene los valores que envio el servicio atraves de un untent
            //NOtAR la utilizacion de un objeto Bundle es opcional.
            String msgJson = intent.getStringExtra("msgJson");
            txtJson.setText(msgJson);

            try {
                JSONObject jsonObject = new JSONObject(msgJson);
                String value = jsonObject.getString("value");
                txtTemp.setText(value+"°");
            } catch (JSONException e) {
                throw new RuntimeException(e);
            }
        }

    }

}
