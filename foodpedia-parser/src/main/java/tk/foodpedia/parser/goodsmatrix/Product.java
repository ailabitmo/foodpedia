package com.mycompany.goodsmatrixparser;/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author hp
 */
public class Product {

    private String goodsName;
    private String barCodeL;
    private String composition;
    private String comment;
    private String gost;
    private String netto;
    private String keepingTime;
    private String storeCond;
    private String esl;
    private String packingType;

    public Product() {
        goodsName="";
        barCodeL="";
        composition="";
        comment="";
        gost="";
        netto="";
        keepingTime="";
        storeCond="";
        esl="";
        packingType="";

    }

    public Product(Product product) {
        goodsName=product.getGoodsName();
        barCodeL=product.getBarCodeL();
        composition=product.getComposition();
        comment=product.getComment();
        gost=product.getGost();
        netto=product.getNetto();
        keepingTime=product.getKeepingTime();
        storeCond=product.getStoreCond();
        esl=product.getEsl();
        packingType=product.getPackingType();

    }



    public String getBarCodeL() {
        return barCodeL;
    }

    public String getComposition() {
        return composition;
    }

    public String getEsl() {
        return esl;
    }

    public String getComment() {
        return comment;
    }

    public String getGoodsName() {
        return goodsName;
    }

    public String getGost() {
        return gost;
    }

    public String getKeepingTime() {
        return keepingTime;
    }

    public String getNetto() {
        return netto;
    }

    public String getPackingType() {
        return packingType;
    }

    public String getStoreCond() {
        return storeCond;
    }

    /**
     * @param goodsName the goodsName to set
     */
    public void setGoodsName(String goodsName) {
        this.goodsName = goodsName;
    }

    /**
     * @param barCodeL the barCodeL to set
     */
    public void setBarCodeL(String barCodeL) {
        this.barCodeL = barCodeL;
    }

    /**
     * @param composition the composition to set
     */
    public void setComposition(String composition) {
        this.composition = composition;
    }

    /**
     * @param comment the comment to set
     */
    public void setComment(String comment) {
        this.comment = comment;
    }

    /**
     * @param gost the gost to set
     */
    public void setGost(String gost) {
        this.gost = gost;
    }

    /**
     * @param netto the netto to set
     */
    public void setNetto(String netto) {
        this.netto = netto;
    }

    /**
     * @param keepingTime the keepingTime to set
     */
    public void setKeepingTime(String keepingTime) {
        this.keepingTime = keepingTime;
    }

    /**
     * @param storeCond the storeCond to set
     */
    public void setStoreCond(String storeCond) {
        this.storeCond = storeCond;
    }

    /**
     * @param esl the esl to set
     */
    public void setEsl(String esl) {
        this.esl = esl;
    }

    /**
     * @param packingType the packingType to set
     */
    public void setPackingType(String packingType) {
        this.packingType = packingType;
    }




}
