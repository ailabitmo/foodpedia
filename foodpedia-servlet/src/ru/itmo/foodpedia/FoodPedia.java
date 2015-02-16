package ru.itmo.foodpedia;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * @author Maksim Lapaev
 *         Date: 16.02.15
 *         Time: 16:31
 */
public class FoodPedia extends HttpServlet {

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        request.getContentType();
        String accept = request.getHeader("Accept");
        if (accept != null && accept.indexOf("text/html") >= 0) {
            response.sendRedirect("http://github.com");
        } else if (accept != null && accept.indexOf("application/rdf+xml") >= 0) {
            response.sendRedirect("http://purl.org/foodontology");
        }
    }

}


