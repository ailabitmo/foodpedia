<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@taglib tagdir="/WEB-INF/tags" prefix="t"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<c:set var="lang" value="${lang != null ? lang : param.lang != null ? param.lang : 'ru'}"></c:set>

<t:page title="About">
    <c:if test='${lang.equalsIgnoreCase("en")}'>
        <p>
            <b>FOODpedia</b> - is community effort to extract information about food products 
            and their ingredients from existing sources such as 
            <a href="http://goodsmatrix.ru/">GoodsMatrix</a> or <a href="http://www.gs1ru.org/">GS1</a>
            and make this information available on the Web in a more structured way 
            following the <a href="http://en.wikipedia.org/wiki/Linked_data">Linked Data</a> principles.
        </p>
        <p>
            For a recent overview paper about FOODpedia, please refer to:
        </p>
        <ul>
            <li>
                Maxim Kolchin, Alexander Chistyakov, Maxim Lapaev, Rezeda Khaydarova: 
                FOODpedia: Russian food products as a Linked Data Dataset. 
                In: The Semantic Web: ESWC 2015 Satellite Events, 
                Lecture Notes in Computer Science, 2015. <i>(to appear)</i>
            </li>
        </ul>
    </c:if>
    <c:if test='${lang.equalsIgnoreCase("ru")}'>
        <p>
            <b>FOODpedia</b> - is community effort to extract information about food products 
            and their ingredients from existing sources such as 
            <a href="http://goodsmatrix.ru/">GoodsMatrix</a> or <a href="http://www.gs1ru.org/">GS1</a>
            and make this information available on the Web in a more structured way 
            following the <a href="http://en.wikipedia.org/wiki/Linked_data">Linked Data</a> principles.
        </p>
        <p>
            For a recent overview paper about FOODpedia, please refer to:
        </p>
        <ul>
            <li>
                Maxim Kolchin, Alexander Chistyakov, Maxim Lapaev, Rezeda Khaydarova: 
                FOODpedia: Russian food products as a Linked Data Dataset. 
                In: The Semantic Web: ESWC 2015 Satellite Events, 
                Lecture Notes in Computer Science, 2015. <i>(to appear)</i>
            </li>
        </ul>
    </c:if>
</t:page>