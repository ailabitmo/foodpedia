package tk.foodpedia.home.models;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;

public class SearchResult {

    private final String uri;
    private final String name;
    private final String barcode;

    public SearchResult(String uri, String name, String barcode) {
        this.uri = uri;
        this.name = name;
        this.barcode = barcode;
    }

    public String getUri() {
        return uri;
    }

    public String getName() {
        return name;
    }

    public String getBarcode() {
        return barcode;
    }
    
    public static class Factory {
        
        public static List<SearchResult> fromCSV(String csv) throws IOException {
            final List<SearchResult> results = new ArrayList<>();
            try(CSVParser parser = CSVFormat.RFC4180
                    .withHeader().parse(new StringReader(csv))) {
                final Iterator<CSVRecord> iter = parser.iterator();
                while(iter.hasNext()) {
                    final CSVRecord record = iter.next();
                    final SearchResult r = new SearchResult(
                            record.get("product"), 
                            record.get("name"), 
                            record.get("barcode"));
                    results.add(r);
                }
            }
            return results;
        }
        
    }
    
}
