package com.example.textfields_tests;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.ArrayList;
import java.util.List;

public class PaymentArrayAdapter extends ArrayAdapter<Paymentplan> {
    private static final String TAG = "PersonlistAdapter";

    private Context mContext;
    private int mResource;
    LayoutInflater inflater;

    public PaymentArrayAdapter(@NonNull Context context, int resource, @NonNull ArrayList<Paymentplan> objects) {
        super(context, resource, objects);
        this.mContext = context;
        this.mResource = resource;
        this.inflater = LayoutInflater.from(context);
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        String provider = getItem(position).getProvider();
        int payers = getItem(position).getPayers();
        float price = getItem(position).getPrice();
        int months = getItem(position).getMonths();
        float interest = getItem(position).getInterest();
        boolean open = getItem(position).isOpen();

        if (convertView == null) {
            convertView = inflater.inflate(R.layout.view_textmodel, null);
        }

        TextView viewProvider = (TextView) convertView.findViewById(R.id.teksti_1);
        TextView viewPrice = (TextView) convertView.findViewById(R.id.pricefield);
        TextView viewMonths = (TextView) convertView.findViewById(R.id.monthsfield);
        TextView viewPayers = (TextView) convertView.findViewById(R.id.payersfield);

        viewProvider.setText(provider);
        viewPrice.setText("Price: " + price);
        viewMonths.setText("Months: " + months);
        viewPayers.setText("Payers: " + payers);
        if (open) {
            convertView.setBackgroundResource(R.color.colorOpenPaymentplans);
        } else {
            convertView.setBackgroundResource(R.color.colorClosedPaymentplans);
        }

        return convertView;
    }
}
