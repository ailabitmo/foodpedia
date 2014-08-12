package com.mycompany.goodsmatrixparser;
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Resource;
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

    public static void main(String[] args) throws IOException {
        //     ShutdownHook shutdownHook = new ShutdownHook(out);
        //   Runtime.getRuntime().addShutdownHook(shutdownHook);
        System.out.println("Начало работы");
        model = ModelFactory.createDefaultModel();
        //model = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM);
        model.setNsPrefix("rdf", ProdProps.RDF);
        model.setNsPrefix("food", ProdProps.FOOD);
        model.setNsPrefix("gr", ProdProps.GR);
        out = new FileWriter("D:\\goods.dat");
        goPars("http://www.goodsmatrix.ru/goods-catalogue/Goods/Foodstuffs.html");//"http://www.goodsmatrix.ru/goods-catalogue/Foodstuffs/Groceries.html");//http://goodsmatrix.ru/goods-catalogue/Goods/Foodstuffs.html");
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
            goPars(url);
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
                            = model.createResource(realURL)
                            .addProperty(ProdProps.type, "food:Food")
                            .addProperty(ProdProps.goodsName, doc.select("span#ctl00_ContentPH_GoodsName").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_GoodsName").get(0).text())
                            .addProperty(ProdProps.barCode, doc.select("span#ctl00_ContentPH_BarCodeL").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_BarCodeL").get(0).text())
                            .addProperty(ProdProps.bestBefore, doc.select("span#ctl00_ContentPH_KeepingTime").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_KeepingTime").get(0).text())
                            .addProperty(ProdProps.comment, doc.select("span#ctl00_ContentPH_Comment").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_Comment").get(0).text())
                            .addProperty(ProdProps.ingredients, doc.select("span#ctl00_ContentPH_Composition").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_Composition").get(0).text())
                            .addProperty(ProdProps.nettoWeight, doc.select("span#ctl00_ContentPH_Net").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_Net").get(0).text())
                            .addProperty(ProdProps.standart, doc.select("span#ctl00_ContentPH_Gost").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_Gost").get(0).text())
                            .addProperty(ProdProps.storeConditions, doc.select("span#ctl00_ContentPH_StoreCond").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_StoreCond").get(0).text())
                            .addProperty(ProdProps.ESL, doc.select("span#ctl00_ContentPH_ESL").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_ESL").get(0).text())
                            .addProperty(ProdProps.packType, doc.select("span#ctl00_ContentPH_PackingType").isEmpty() ?
                                    "" : doc.select("span#ctl00_ContentPH_PackingType").get(0).text());

                    // Print RDF/XML of model to system output
                    model.write(new PrintWriter(out), "TURTLE");

                } catch (Exception e) {
                    System.out.println("Failed: " + e);
                }
            }
        } catch (IOException ex) {
            System.out.println("ОШИБКА  " + url + "   parsList");
            parsList(url);
        }
    }

    public static String realURL(String url) throws IOException // Возвращает страницу продукта (предыдущая страница альтернативные продукты)
    {
        Elements realURL = Jsoup.connect(url).get().select("a[id=ctl00_ContentPH_SGDG_ctl02_A6]");
        return realURL.get(0).attr("href");
    }

    public static Product parseProduct(String url) throws IOException {
        Product p = new Product();
        Document doc = Jsoup.connect(url).get();
        if (doc.select("span#ctl00_ContentPH_GoodsName").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements goodsName = doc.select("span#ctl00_ContentPH_GoodsName");//Название
            p.setGoodsName(goodsName.get(0).text());
            System.out.println(goodsName.get(0).text());
        }

        if (doc.select("span#ctl00_ContentPH_BarCodeL").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements barCodeL = doc.select("span#ctl00_ContentPH_BarCodeL");//Штрих код
            p.setBarCodeL(barCodeL.get(0).text());
            System.out.println(barCodeL.get(0).text());
        }

        if (doc.select("span#ctl00_ContentPH_Composition").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements composition = doc.select("span#ctl00_ContentPH_Composition");//Состав
            p.setComposition(composition.text());
            System.out.println(composition.get(0).text());
        }

        if (doc.select("span#ctl00_ContentPH_Comment").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements comment = doc.select("span#ctl00_ContentPH_Comment");//Описание
            p.setComment(comment.get(0).text());
            System.out.println(comment.get(0).text());
        }

        if (doc.select("span#ctl00_ContentPH_Gost").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements gost = doc.select("span#ctl00_ContentPH_Gost");//Гост
            p.setGost(gost.get(0).text());
            System.out.println(gost.get(0).text());
        }

        if (doc.select("span#ctl00_ContentPH_Net").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements netto = doc.select("span#ctl00_ContentPH_Net");//Масса нетто
            p.setNetto(netto.get(0).text());
            System.out.println(netto.get(0).text());
        }

        if (doc.select("span#ctl00_ContentPH_KeepingTime").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements keepingTime = doc.select("span#ctl00_ContentPH_KeepingTime");//Срок годности
            p.setKeepingTime(keepingTime.get(0).text());
            System.out.println(keepingTime.get(0).text());
        }

        if (doc.select("span#ctl00_ContentPH_StoreCond").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements storeCond = doc.select("span#ctl00_ContentPH_StoreCond");//Условия хранения
            p.setStoreCond(storeCond.get(0).text());
            System.out.println(storeCond.get(0).text());
        }


        if (doc.select("span#ctl00_ContentPH_ESL").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements esl = doc.select("span#ctl00_ContentPH_ESL");//Энергетическая ценность
            p.setEsl(esl.get(0).text());
            System.out.println(esl.get(0).text());
        }

        if (doc.select("span#ctl00_ContentPH_PackingType").isEmpty()) {
            p.setGoodsName("");
            System.out.println("");
        } else {
            Elements packingType = doc.select("span#ctl00_ContentPH_PackingType");//Упаковка
            p.setPackingType(packingType.get(0).text());
            System.out.println(packingType.get(0).text());
        }


        return p;
    }
}

class ShutdownHook extends Thread {
    private static FileWriter out;

    public ShutdownHook(FileWriter out) {
        this.out = out;
    }

    public void run() {
        try {
            out.close();
            System.out.println("Shutting down");
        } catch (IOException e) {
            e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
        }
    }
}