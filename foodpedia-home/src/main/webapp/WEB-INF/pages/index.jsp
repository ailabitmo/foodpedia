<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@taglib tagdir="/WEB-INF/tags" prefix="t"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<c:set var="lang" value="${lang != null ? lang : param.lang != null ? param.lang : 'ru'}"></c:set>
<fmt:setLocale value="${lang}"/>
<fmt:setBundle basename="tk.foodpedia.home.messages"/>

<t:default lang="${lang}">
    <div class="header-block">
        <ul class="lang-switch">
            <li><a href="?lang=ru"><img src="assets/ru.svg" alt="Ru"/></a></li>
            <li><a href="?lang=en"><img src="assets/gb.svg" alt="En"/></a></li>
        </ul>
    </div>
    <div class="row">
        <div class="col-md-8 center-block" style="float: none">
            <div class="logo main">
                <h1 class="noselect"><span style="color: #6aa84f">FOOD</span><span style="color: #f1c232">pedia</span></h1>
            </div>
            <div>
                <form role="form" method="GET" action="search" novalidate>
                    <div class="input-group">
                        <input type="text" class="form-control" name="q"
                               placeholder="<fmt:message key="main.search.placeholder"/>">
                        <span class="input-group-btn">
                            <button class="btn btn-default" type="submit">
                                <fmt:message key="main.search.button"/>
                            </button>
                        </span>
                    </div>
                    <input type="hidden" name="lang" value="${lang}"/>
                </form>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-md-8 center-block" style="float: none; text-align: center; margin-top: 1%">
            <i><fmt:message key="main.beta"/></i>
        </div>
    </div>
    <div class="row thumbnail-block">
        <div class="col-md-8 center-block" style="float: none">
            <div class="row center-block">
                <div class="col-sm-4 col-md-4">
                    <div class="thumbnail">
                        <div class="caption">
                            <h3><fmt:message key="main.thumbnail.explore"/></h3>
                            <p><fmt:message key="main.thumbnail.explore.content"/></p>
                        </div>
                    </div>
                </div>
                <div class="col-sm-4 col-md-4">
                    <div class="thumbnail">
                        <div class="caption">
                            <h3><fmt:message key="main.thumbnail.use"/></h3>
                            <p><fmt:message key="main.thumbnail.use.content"/></p>
                        </div>
                    </div>
                </div>
                <div class="col-sm-4 col-md-4">
                    <div class="thumbnail">
                        <div class="caption">
                            <h3><fmt:message key="main.thumbnail.about"/></h3>
                            <p><fmt:message key="main.thumbnail.about.content"/></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</t:default>