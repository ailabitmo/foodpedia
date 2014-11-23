package tk.foodpedia.goodsmatrixparser;

import java.io.*;
/**
 * Created by m.lapaev on 20.11.14.
 */
public class TESTTEST {
    public static final String PROTEIN = "белк";
    public static final String FAT = "жир";
    public static final String CARB = "углев";
    public static final String ENERG = "цен";
    public static final String GRAMM = "г";
    public static final String KCAL = "ккал";
    public static void main(String[] args) {
        BufferedReader br = null;
        try {  br = new BufferedReader(new FileReader(new File("D:\\projects\\aspirantura\\foods\\sports.dat")));  } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        String line;
        try {
            while ((line = br.readLine()) != null) {
                if (line.indexOf("foodpedia-owl:esl") != -1) {
                    GDA gda = new GDA();
                    String lower = line.toLowerCase();
                    if (lower.indexOf(PROTEIN) != -1) { gda.proteins = parseFloat(lower.split(PROTEIN)[1].split(GRAMM)[0]); }
                    if (lower.indexOf(FAT) != -1) { gda.fats = parseFloat(lower.split(FAT)[1].split(GRAMM)[0]); }
                    if (lower.indexOf(CARB) != -1) { gda.carbs = parseFloat(lower.split(CARB)[1].split(GRAMM)[0]); }
                    if (lower.indexOf(ENERG) != -1) { gda.kcal = parseFloat(lower.split(ENERG)[1].split(KCAL)[0]); }
                    System.out.println("[" + line.split("foodpedia-owl:esl")[1].trim() + "]" + gda);
                }
            }
        } catch (IOException e) {  e.printStackTrace(); }
    }

    private static float parseFloat(String str) {
        StringBuffer floatString = new StringBuffer();
        for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);
            if (ch == '.' || ch == ',' || (ch >= '0' && ch <= '9')) {
                floatString.append(ch);
            }
        }
        return Float.valueOf(floatString.toString().replace(',', '.'));
    }
}

class GDA {
    public float proteins;
    public float fats;
    public float carbs;
    public float kcal;

    public String toString() {
        return "{Proteins: " + proteins +
                ", Fats: " + fats +
                ", Carbohydrates: " + carbs +
                ", Energy: " + kcal + "}";
    }
}