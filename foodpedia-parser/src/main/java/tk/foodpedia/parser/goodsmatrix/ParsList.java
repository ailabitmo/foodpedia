package tk.foodpedia.parser.goodsmatrix;/*
* To change this license header, choose License Headers in Project Properties.
* To change this template file, choose Tools | Templates
* and open the template in the editor.
*/

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.vocabulary.RDF;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

/**
* @author валерий
*/
public class ParsList {
    private static Model model;
    private static FileWriter out;
    static long count = 100;
    static long current = 0;
    static Resource rc;

    public static void main(String[] args) throws IOException {
        System.out.println("Начало работы");
        model = ModelFactory.createDefaultModel();
        //model = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM);
        model.setNsPrefix("rdf", ProdProps.RDF);
        model.setNsPrefix("food", ProdProps.FOOD);
        model.setNsPrefix("gr", ProdProps.GR);
        model.setNsPrefix("foodpedia-owl", ProdProps.TODO);
        rc = model.createResource("http://purl.org/foodontology#Food");
        out = new FileWriter("confectionary.dat");
//        AddShutdownHookSample sample = new AddShutdownHookSample();
//        sample.attachShutDownHook(model, out);
        //goPars("http://www.goodsmatrix.ru/goods-catalogue/Mustard/Dijon-mustard.html");
        goPars("http://www.goodsmatrix.ru/goods-catalogue/Foodstuffs/Confectionary.html");//"http://www.goodsmatrix.ru/goods-catalogue/Foodstuffs/Groceries.html");//http://goodsmatrix.ru/goods-catalogue/Goods/Foodstuffs.html");
        model.write(new PrintWriter(out), "TURTLE");
        out.flush();
        out.close();
    }


    static void goPars(String url) //Парсинг
    {
        try // throws IOException
        {
            Document doc = Jsoup.connect(url).get();
            Elements lastPars = doc.select("a[runat=server]");
            Elements pars = doc.select("a[class=grtext4]");
            if (pars.indexOf(lastPars.last()) == pars.indexOf(pars.last())) // если на странице нет новых элементов, то найдена страница списка товаров
            {
                System.out.println(url);
                parsList(url);
                return;
            }

            int index = pars.indexOf(lastPars.last());
            index++;
            for (int i = index; i <= pars.indexOf(pars.last()); i++)// Парсинг всех новых элементов на странице
            {
                goPars(pars.get(i).attr("href"));
            }
            return;
        } catch (IOException ex) {
            System.out.println("ОШИБКА  " + url + "  goPars");
            //goPars(url);
        }
    }


    public static String editURL(String url)// изменение URL на список продуктов (не измененный не парсится) 37-41
    {
        if (url.charAt(48) == '?') {
            String map = "http://www.goodsmatrix.ru/Map";
            String newURL = map + url.substring(26);
            return newURL;
        }
        String map = "http://www.goodsmatrix.ru/map/";
        String newURL = map + url.substring(42);
        return newURL;
    }

    static void parsList(String url) // парсинг списка продуктов
    {
        try // парсинг списка продуктов
        {
            String editURL = editURL(url);
            Elements list = Jsoup.connect(editURL).get().select("a[href^=http://www.goodsmatrix.ru/goods-analogue/]");
            for (int i = 0; i < list.indexOf(list.last()); i++, i++) // Выводит URL страницы продукта
            {
                String realURL = realURL(list.get(i).attr("href"));
                //   Product p = parseProduct(realURL);

                try {
                    Document doc = Jsoup.connect(realURL).get();
                    Resource goods
                            = model.createResource(realURL.replace("www.goodsmatrix.ru/goods","foodpedia.tk/resource").replace(".html",""))
                            .addProperty(RDF.type, rc);
                    if (containsData(doc.select("span#ctl00_ContentPH_GoodsName"))) {
                        goods.addProperty(ProdProps.goodsName, doc.select("span#ctl00_ContentPH_GoodsName").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_BarCodeL"))) {
                        goods.addProperty(ProdProps.barCode, doc.select("span#ctl00_ContentPH_BarCodeL").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_KeepingTime"))) {
                        goods.addProperty(ProdProps.bestBefore, doc.select("span#ctl00_ContentPH_KeepingTime").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_Comment"))) {
                        goods.addProperty(ProdProps.comment, doc.select("span#ctl00_ContentPH_Comment").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_Composition"))) {
                        goods.addProperty(ProdProps.ingredients, doc.select("span#ctl00_ContentPH_Composition").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_Net"))) {
                        goods.addProperty(ProdProps.nettoWeight, doc.select("span#ctl00_ContentPH_Net").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_Gost"))) {
                        goods.addProperty(ProdProps.standart, doc.select("span#ctl00_ContentPH_Gost").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_StoreCond"))) {
                        goods.addProperty(ProdProps.storeConditions, doc.select("span#ctl00_ContentPH_StoreCond").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_ESL"))) {
                        goods.addProperty(ProdProps.ESL, doc.select("span#ctl00_ContentPH_ESL").get(0).text().replace('"', '\"'));
                    }
                    if (containsData(doc.select("span#ctl00_ContentPH_PackingType"))) {
                        goods.addProperty(ProdProps.packType, doc.select("span#ctl00_ContentPH_PackingType").get(0).text().replace('"', '\"'));
                    }
                    // Print RDF/XML of model to system output
                    current++;
                    System.out.println("Product: " + current + " out of " + count);
                    if (current >= count) {
//                        System.out.println("LAST: " + url);
//                        model.write(new PrintWriter(out), "TURTLE");
//                        out.flush();
//                        out.close();
//                        System.exit(0);
                    }
                } catch (Exception e) {
                    System.out.println("Failed: " + e);
                }
            }
        } catch (IOException ex) {
            System.out.println("ОШИБКА  " + url + "   parsList");
            parsList(url);
        }
    }

    public static boolean containsData(Elements elements) {
        return !(elements.isEmpty() || elements.get(0).text().equals(""));
    }

    public static String realURL(String url) throws IOException // Возвращает страницу продукта (предыдущая страница альтернативные продукты)
    {
        Elements realURL = Jsoup.connect(url).get().select("a[id=ctl00_ContentPH_SGDG_ctl02_A6]");
        return realURL.get(0).attr("href");
    }
}

class AddShutdownHookSample {
    public void attachShutDownHook(final Model model, final FileWriter out) {
        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                model.write(new PrintWriter(out), "TURTLE");
                try {
                    out.flush();
                    out.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                System.out.println("Inside Add Shutdown Hook");
            }
        });
        System.out.println("Shut Down Hook Attached.");
    }
}
