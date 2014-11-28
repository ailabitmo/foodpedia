package tk.foodpedia.parser.additives;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.impl.PropertyImpl;

/**
 * Created by m.lapaev on 28.11.14.
 */

public class AdditiveProps {
    protected static final String RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
    protected static final String TODO = "http://foodpedia.tk/additiveontology#";

    static final String nAdditiveCode = "code";
    public static Property additiveCode = null;
    static final String nNames = "names";
    public static Property names = null;
    static final String nDescription = "description";
    public static Property description = null;
    static final String nHarmLevel = "harm_level";
    public static Property harmLevel = null;
    static final String nProductionWay = "production_way";
    public static Property productionWay = null;
    static final String nType = "type";
    public static Property type = null;

    static {
        try {
            additiveCode = new PropertyImpl(TODO, nAdditiveCode);
            names = new PropertyImpl(TODO, nNames);
            description = new PropertyImpl(TODO, nDescription);
            harmLevel = new PropertyImpl(TODO, nHarmLevel);
            productionWay = new PropertyImpl(TODO, nProductionWay);
            type = new PropertyImpl(TODO, nType);
        } catch (Throwable e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

}
