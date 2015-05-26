<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@taglib tagdir="/WEB-INF/tags" prefix="t"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>

<c:set var="lang" value="${lang != null ? lang : param.lang != null ? param.lang : 'ru'}"></c:set>
<fmt:setLocale value="${lang}"/>
<fmt:setBundle basename="tk.foodpedia.home.messages"/>

<t:default lang="${lang}">
    <div class="row">
        <div class="col-md-12">
            <div class="header-block">
                <ul class="lang-switch">
                    <li><a href="?q=${q}&lang=ru&offset=${offset}"><img src="assets/ru.svg" alt="Ru"/></a></li>
                    <li><a href="?q=${q}&lang=en&offset=${offset}"><img src="assets/gb.svg" alt="En"/></a></li>
                </ul>
            </div>
        </div>
    </div>
    <div class="row search-header">
        <div class="col-xs-3">
            <div class="logo search noselect">
                <a href="/?lang=${lang}">
                    <span style="color: #6aa84f">FOOD</span><span style="color: #f1c232">pedia</span>
                </a>
            </div>
        </div>
        <div class="col-xs-9">
            <form class="search-form form-inline" action="/search" method="GET">
                <div class="form-group col-xs-10">
                    <input type="text" class="form-control" name="q" 
                           value='${q}'/>
                </div>
                <input type="hidden" name="lang" value="${lang}"/>
                <button type="submit" class="btn btn-default">
                    <span class="glyphicon glyphicon-search" aria-hidden="true"></span>
                </button>
            </form>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12"><hr/></div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <c:choose>
                <c:when test="${results.isEmpty()}">
                    <div class="search-results-no">
                        <fmt:message key="search.results.no"/>
                    </div>
                </c:when>

                <c:otherwise>
                    <ul class="search-results">
                        <c:forEach var="result" items="${results}">
                            <li>
                                <span class="search-results-name">
                                    <a href="${result.uri}">${result.name}</a>
                                </span>
                                <span class="search-results-uri">
                                    ${result.uri}
                                </span>
                            </li>
                        </c:forEach>
                    </ul>
                </c:otherwise>
            </c:choose>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <nav style="text-align: center;">
                <ul class="pagination pagination-lg">
                    <li class="${Integer.parseInt(offset) <= 0 ? "disabled" : ""}">
                        <a href="/search?q=${q}&lang=${lang}&offset=${Integer.parseInt(offset) - 10}" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                    <li class="${results.size() < 10 ? "disabled" : ""}">
                        <a href="/search?q=${q}&lang=${lang}&offset=${Integer.parseInt(offset) + 10}" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
</t:default>