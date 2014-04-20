/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.mycompany.goodsmatrixparser;

import java.io.IOException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

/**
 *
 * @author hp
 */
public class Parser {
    public static void main(String[] args) throws IOException{
       Product p = parseProduct("http://www.goodsmatrix.ru/goods/d/4810591000138.html");
        System.out.println(p.getName());
    }
    
    private static Product parseProduct(String url) throws IOException {
         Document doc = Jsoup.connect(url).get();
         Product p = new Product();
        Elements name = doc.select("span#ctl00_ContentPH_GoodsName");
        p.setName(name.get(0).text());
        Elements composition = doc.select("span#ctl00_ContentPH_Composition");
        p.setComposition(composition.get(0).text());
        Elements esl = doc.select("span#ctl00_ContentPH_ESL");
        p.setFoodEnergy(esl.get(0).text());
        return p;
    }
}
    

