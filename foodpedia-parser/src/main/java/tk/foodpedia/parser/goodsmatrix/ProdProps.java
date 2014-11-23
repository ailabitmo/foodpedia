package tk.foodpedia.goodsmatrixparser;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.impl.PropertyImpl;

public class ProdProps extends Object {

    // URI for vocabulary elements
    protected static final String RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
    protected static final String GR = "http://purl.org/goodrelations/v1#";
    protected static final String FOOD = "http://purl.org/foodontology#";
    protected static final String TODO = "http://foodpedia.tk/ontology#";

    // Return URI for vocabulary elements
    public static String getURI() {
        return FOOD;
    }

    // Define the property labels and objects
    //OK
    static final String nGoodsName = "name";
    public static Property goodsName = null;
    //OK
    static final String nBarCode = "hasEAN_UCC-13";
    public static Property barCode = null;
    static final String nIngredients = "ingredientsListAsText";
    public static Property ingredients = null;
    //OK
    static final String nComment = "description";
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
            goodsName = new PropertyImpl(GR, nGoodsName);
            barCode = new PropertyImpl(GR, nBarCode);
            ingredients = new PropertyImpl(FOOD, nIngredients);
            comment = new PropertyImpl(GR, nComment);
            storeConditions = new PropertyImpl(TODO, nStoreConditions);
            ESL = new PropertyImpl(TODO, nESL);
            packType = new PropertyImpl(TODO, nPackType);
            standart = new PropertyImpl(TODO, nStandart);
            nettoWeight = new PropertyImpl(TODO, nNettoWeight);
            bestBefore = new PropertyImpl(TODO, nBestBefore);
        } catch (Throwable e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

}