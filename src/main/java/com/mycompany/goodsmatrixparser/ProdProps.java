package com.mycompany.goodsmatrixparser;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.impl.PropertyImpl;

public class ProdProps extends Object {

    // URI for vocabulary elements
    protected static final String RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
    protected static final String GR = "http://www.heppnetz.de/ontologies/goodrelations/v1#";
    protected static final String FOOD = "https://raw.githubusercontent.com/ailabitmo/food-ontology/master/food.owl#";

    // Return URI for vocabulary elements
    public static String getURI() {
        return FOOD;
    }

    // Define the property labels and objects
    static final String nType = "type";
    public static Property type = null;
    static final String nGoodsName = "name";
    public static Property goodsName = null;
    static final String nBarCode = "hasEAN_UCC-13";
    public static Property barCode = null;
    static final String nIngredients = "ingredientsListAsText";
    public static Property ingredients = null;
    static final String nComment = "comment";
    public static Property comment = null;
    static final String nStandart = "standart";
    public static Property standart = null;
    static final String nNettoWeight = "netto_mass";
    public static Property nettoWeight = null;
    static final String nBestBefore = "best_before";
    public static Property bestBefore = null;
    static final String nStoreConditions = "store_cond";
    public static Property storeConditions = null;
    static final String nESL = "esl";
    public static Property ESL = null;
    static final String nPackType = "pack_type";
    public static Property packType = null;


    // Instantiate the properties and the resource
    static {
        try {
            // Instantiate the properties
            type = new PropertyImpl(RDF, nType);
            goodsName = new PropertyImpl(GR, nGoodsName);
            barCode = new PropertyImpl(GR, nBarCode);
            ingredients = new PropertyImpl(FOOD, nIngredients);
            comment = new PropertyImpl(GR, nComment);
            storeConditions = new PropertyImpl(GR, nStoreConditions);
            ESL = new PropertyImpl(GR, nESL);
            packType = new PropertyImpl(GR, nPackType);
            standart = new PropertyImpl(GR, nStandart);
            nettoWeight = new PropertyImpl(GR, nNettoWeight);
            bestBefore = new PropertyImpl(GR, nBestBefore);
        } catch (Throwable e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

}