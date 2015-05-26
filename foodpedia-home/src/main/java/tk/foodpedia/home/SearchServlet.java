package tk.foodpedia.home;

import com.ning.http.client.AsyncCompletionHandler;
import com.ning.http.client.AsyncHttpClient;
import com.ning.http.client.Response;
import java.io.IOException;
import javax.servlet.AsyncContext;
import javax.servlet.AsyncEvent;
import javax.servlet.AsyncListener;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import tk.foodpedia.home.models.SearchResult;

@WebServlet(urlPatterns = "/search", asyncSupported = true)
public class SearchServlet extends HttpServlet {

    private static final Logger logger = LoggerFactory.getLogger(
            SearchServlet.class);
    private static final String ENDPOINT = "http://endpoint:8890/sparql";
    private static final String GRAPH = "http://foodpedia.tk/";
    private static final String QUERY = ""
            + "PREFIX gr: <http://purl.org/goodrelations/v1#>\n"
            + "PREFIX food: <http://purl.org/foodontology#>\n"
            + "SELECT DISTINCT ?product ?name ?barcode where {\n"
            + "  ?product a food:Food ;\n"
            + "           gr:name ?name ;\n"
            + "           gr:hasEAN_UCC-13 ?barcode .\n"
            + "  {\n"
            + "    ?product gr:hasEAN_UCC-13 ?value .\n"
            + "    FILTER(STR(?value) = '%SEARCH%')\n"
            + "  } UNION {\n"
            + "    ?product gr:name ?value .\n"
            + "    ?value bif:contains '\"%SEARCH%\"' .\n"
            + "  }\n"
            + "  FILTER(langMatches(lang(?name), \"%LANG%\"))\n"
            + "}"
            + "OFFSET %OFFSET%\n"
            + "LIMIT 10";
    private static final String QUERY_PARAM = "q";
    private static final String LANG_PARAM = "lang";
    private static final String OFFSET_PARAM = "offset";
    private final AsyncHttpClient client = new AsyncHttpClient();

    @Override
    public void destroy() {
        client.close();

        super.destroy();
    }
    
    private String get(HttpServletRequest request, String name, String defaults) {
        final String param = request.getParameter(name);
        if(param != null && !param.isEmpty()) {
            return param;
        } else {
            return defaults;
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        if (request.getParameter(QUERY_PARAM) != null
                && !request.getParameter(QUERY_PARAM).isEmpty()) {
            final String q = request.getParameter(QUERY_PARAM);
            request.setAttribute(QUERY_PARAM, q);
            final String lang = get(request, LANG_PARAM, "ru");
            request.setAttribute(LANG_PARAM, lang);
            final String offset = get(request, OFFSET_PARAM, "0");
            request.setAttribute(OFFSET_PARAM, offset);
            final AsyncContext context = request.startAsync();
            context.setTimeout(60000);
            context.addListener(new AsyncListener() {

                @Override
                public void onComplete(AsyncEvent event) throws IOException {
                    System.out.println("onComplete");
                }

                @Override
                public void onTimeout(AsyncEvent event) throws IOException {
                    System.out.println("onTimeout");
                }

                @Override
                public void onError(AsyncEvent event) throws IOException {
                    System.out.println("onError");
                }

                @Override
                public void onStartAsync(AsyncEvent event) throws IOException {
                    System.out.println("onStartAsync");
                }
            });

            client.prepareGet(ENDPOINT)
                    .addHeader("Accept", "text/csv")
                    .addQueryParam("query", 
                            QUERY.replaceAll("%SEARCH%", q)
                                    .replaceAll("%LANG%", lang)
                                    .replaceAll("%OFFSET%", offset))
                    .addQueryParam("default-graph-uri", GRAPH)
                    .execute(new AsyncCompletionHandler<Response>() {

                        @Override
                        public Response onCompleted(Response result) throws Exception {
                            try {
                                request.setAttribute("results",
                                        SearchResult.Factory.fromCSV(result.getResponseBody()));

                                getServletContext()
                                .getRequestDispatcher("/WEB-INF/pages/search.jsp")
                                .forward(request, response);

                            } catch (IOException | IllegalStateException ex) {
                                response.setStatus(500);

                                logger.error(ex.getMessage(), ex);
                            }
                            context.complete();

                            return result;
                        }

                        @Override
                        public void onThrowable(Throwable t) {
                            super.onThrowable(t);
                        }
                    });
        } else {
            response.setStatus(400);
        }
    }
}
