package com.example.textfields_tests;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.android.volley.Cache;
import com.android.volley.Network;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.BasicNetwork;
import com.android.volley.toolbox.DiskBasedCache;
import com.android.volley.toolbox.HurlStack;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Random;

public class MainActivity extends AppCompatActivity implements VolleyInterface {

    Random rd = new Random();
    String handle = "dummyhandle";

    static JSONArray itemBody = new JSONArray();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView window = findViewById(R.id.textView3);
        itemBody.put("lol");
        RelativeLayout layout = (RelativeLayout) findViewById(R.id.layout);
        window.setText("Loading: " + handle);
        window.setTextSize(40);

        getAllPaymentplans("dummyhandle");


    }

    public void createTables(ArrayList<Paymentplan> response) {
        PaymentArrayAdapter adapter = new PaymentArrayAdapter(getApplicationContext(), R.layout.view_textmodel, response);
        ListView lt = (ListView) findViewById(R.id.ListView_1);

        lt.setAdapter(adapter);


    }

    public JSONArray createArray(int size) {
        JSONArray newArray = new JSONArray();
        int i, price;


        for (i = 0; i < size; i++) {
            try {
                JSONObject plan = new JSONObject();
                plan.put("Provider", "dummy-" + i);
                plan.put("Price", 1000);
                plan.put("Months", 1);
                plan.put("Interest", 0);
                int randomInt = rd.nextInt(2);
                if (randomInt == 0) {
                    plan.put("Open", true);
                } else {
                    plan.put("Open", false);
                }
                plan.put("Payers", 1);
                newArray.put(plan);
            } catch (Exception e) {

            }
        }
        return newArray;
    }

    public ArrayList<Paymentplan> parseToArrayList(JSONArray response) {
        TextView window = findViewById(R.id.textView3);
        ArrayList<Paymentplan> responseBody = new ArrayList<Paymentplan>();
        window.setText("");
         int i = 0;

        while (!response.isNull(i)) {
            try {
                JSONObject obj = response.getJSONObject(i);

                String provider = obj.getString("provider");
                int months = obj.getInt("months");
                String price = obj.getString("price");
                float fPrice = Float.parseFloat(price);
                int luku = rd.nextInt(1); // All true
                boolean open;
                if (luku == 0) {
                    open = true;

                } else {
                    open = false;
                }
                Paymentplan plan = new Paymentplan(provider, fPrice, 0, 1, months, open);
                responseBody.add(plan);

                i++;
            } catch (Exception e) {
                i++;
            }
        }
        return responseBody;

    }

    public JSONArray getAllPaymentplans(String handle) {
        final TextView textBody = (TextView) findViewById(R.id.textView3);

        String url = "http://10.0.2.2:5000/api/" + handle + "/plans";
        RequestQueue requestQueue;
        JSONArray arr;

        Cache cache = new DiskBasedCache(getCacheDir(), 1024 * 1024);

        Network network = new BasicNetwork(new HurlStack());
        requestQueue = new RequestQueue(cache, network);
        requestQueue.start();

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {
                    JSONArray jsonArray = response.getJSONArray("items");
                    onSuccess(jsonArray);
                } catch (Exception e) {
                    textBody.setText("Error" + e);
                }

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                textBody.setText("Error: " + error);
            }
        });
        requestQueue.add(request);
        return new JSONArray();
    }

    @Override
    public void onSuccess(JSONArray arr) {
        ArrayList<Paymentplan> arrayList = parseToArrayList(arr);
        TextView window = findViewById(R.id.textView3);

        window.setText(arr.toString());
        ArrayList<Paymentplan> planList = parseToArrayList(arr);
        createTables(planList);

    }
}
