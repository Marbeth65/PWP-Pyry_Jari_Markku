package com.example.textfields_tests;

public class Paymentplan {
    String provider;
    float price, interest;
    int payers, months;
    boolean open;

    public Paymentplan(String provider, float price, float interest, int payers, int months, boolean open) {
        this.provider = provider;
        this.price = price;
        this.interest = interest;
        this.payers = payers;
        this.months = months;
        this.open = open;
    }

    public String getProvider() {
        return provider;
    }

    public float getPrice() {
        return price;
    }

    public float getInterest() {
        return interest;
    }

    public int getPayers() {
        return payers;
    }

    public int getMonths() {
        return months;
    }

    public boolean isOpen() {
        return open;
    }

    public void setProvider(String provider) {
        this.provider = provider;
    }

    public void setPrice(float price) {
        this.price = price;
    }

    public void setInterest(float interest) {
        this.interest = interest;
    }

    public void setPayers(int payers) {
        this.payers = payers;
    }

    public void setMonths(int months) {
        this.months = months;
    }

    public void setOpen(boolean open) {
        this.open = open;
    }
}
