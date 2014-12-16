package tk.foodpedia.parser.additives;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.vocabulary.RDF;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import tk.foodpedia.parser.goodsmatrix.ProdProps;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

/**
 * Created by m.lapaev on 28.11.14.
 */
public class Parser {
    public static final String BASE = "http://dobavkam.net/additives";
    private static Model model;
    private static FileWriter out;
    static Resource rc;

    public static void main(String[] args) {
        model = ModelFactory.createDefaultModel();
        model.setNsPrefix("rdf", AdditiveProps.RDF);
        model.setNsPrefix("foodpedia-additive", AdditiveProps.TODO);
        rc = model.createResource("http://purl.org/foodontology#Additive");
        try {
            out = new FileWriter("additives.dat");
            Document doc = Jsoup.connect(BASE).get();
            Elements additives = doc.getElementsByAttributeValueStarting("class", "additive-image-small");
            String url = "";
            ArrayList<String> urls = new ArrayList<String>();
            for (Element el : additives) {
                url = BASE + "/e" + el.getElementsByClass("field-content").text().substring(1);
                urls.add(url);
            }
            for (String u : urls) {
                Additive ad = parseAdditive(u);
                System.out.println(ad.getUrl());
                addToRDF(ad);
            }
            model.write(new PrintWriter(out), "TURTLE");
            out.flush();
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static Additive parseAdditive(String url) {
        url = validateLink(url);
        Additive additive = null;
        try {
            Document doc = Jsoup.connect(url).get();
            additive = new Additive();
            additive.setUrl(url);
            additive.setCode(url.split("/")[4]);
            Elements els = doc.getElementsByAttributeValueStarting("class", "spoiler-body");
            if (els.size() > 0) {
                additive.setNames(els.get(0).text());
            }
            els = doc.getElementsByAttributeValueStarting("class", "additive-image-big");
            if (els.size() > 0) {
                additive.setHarm(els.attr("class").split("\n")[1].split(" ")[1].split("-")[1]);

                additive.setProductionWay(els.attr("class").split("\n")[1].split(" ")[0]);
            }
            els = doc.getElementsByAttributeValueStarting("class", "body");
            if (els.size() > 0) {
                additive.setDescription(els.html());
            }
            els = doc.getElementsByAttributeValueStarting("class", "active-trail");
            if (els.size() > 1) {
                additive.setType(els.get(1).text());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return additive;
    }

    private static void addToRDF(Additive additive) {
        Resource goods
                = model.createResource(additive.getUrl())
                .addProperty(RDF.type, rc);
        if (!additive.getCode().equals("")) {
            goods.addProperty(AdditiveProps.additiveCode, additive.getCode());
        }
        if (!additive.getNames().equals("")) {
            goods.addProperty(AdditiveProps.names, additive.getNames());
        }
        if (!additive.getHarm().equals("")) {
            goods.addProperty(AdditiveProps.harmLevel, additive.getHarm());
        }
        if (!additive.getProductionWay().equals("")) {
            goods.addProperty(AdditiveProps.productionWay, additive.getProductionWay());
        }
        if (!additive.getType().equals("")) {
            goods.addProperty(AdditiveProps.type, additive.getType());
        }
        if (!additive.getDescription().equals("")) {
            goods.addProperty(AdditiveProps.description, additive.getDescription());
        }
    }

    private static String validateLink(String url) {
        return url.replaceAll("е", "e").replaceAll("а", "a").replaceAll("с", "c");
    }
}

class Additive {
    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getNames() {
        return names;
    }

    public void setNames(String names) {
        this.names = names;
    }

    public String getHarm() {
        return harm;
    }

    public void setHarm(String harm) {
        this.harm = harm;
    }

    public String getProductionWay() {
        return productionWay;
    }

    public void setProductionWay(String productionWay) {
        this.productionWay = productionWay;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    private String code = "";
    private String names = "";
    private String harm = "";
    private String productionWay = "";
    private String description = "";
    private String type = "";
    private String url = "";

    public String toString() {
        return code + " : {Harmful: " + harm
                + "; Production way: " + productionWay
                + "; Type: " + type
                + "\nURL: " + url
                + "\nAlternative names: " + names
                + "\nDescription: " + description.substring(0, 100) + "}\n";
    }
}
