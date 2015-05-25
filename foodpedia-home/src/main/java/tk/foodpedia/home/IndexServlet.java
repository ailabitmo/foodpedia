package tk.foodpedia.home;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.io.IOUtils;

@WebServlet(urlPatterns = "")
public class IndexServlet extends HttpServlet {

    private static final String HEADER_ACCEPT = "Accept";
    private static final String TEXT_TURTLE = "text/turtle";
    private InputStream voidTTL;
    
    @Override
    public void init() throws ServletException {
        super.init();
        
        try {
        voidTTL = new FileInputStream(getServletContext().getRealPath("/void.ttl"));
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    @Override
    public void destroy() {
        IOUtils.closeQuietly(voidTTL);
        super.destroy();
    }
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        final String accept = request.getHeader(HEADER_ACCEPT);
        if (accept != null && accept.equalsIgnoreCase(TEXT_TURTLE)) {
            response.setContentType(TEXT_TURTLE);
            final OutputStream out = response.getOutputStream();
            IOUtils.copy(voidTTL, out);
            out.flush();
        } else {
            getServletContext().getRequestDispatcher("/WEB-INF/pages/index.jsp")
                    .forward(request, response);
        }
    }

}
