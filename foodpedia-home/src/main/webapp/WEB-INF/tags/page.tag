<%@tag description="The layout for a static page" pageEncoding="UTF-8"%>
<%@taglib tagdir="/WEB-INF/tags" prefix="t"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<%@attribute name="title" type="java.lang.String"%>
<%@attribute name="head" fragment="true"%>

<c:set var="lang" value="${lang != null ? lang : param.lang != null ? param.lang : 'ru'}"></c:set>
<fmt:setLocale value="${lang}"/>
<fmt:setBundle basename="tk.foodpedia.home.messages"/>

<t:default lang="${lang}" subtitle="${title}">
    <jsp:attribute name="head">
        <jsp:invoke fragment="head"/>
    </jsp:attribute>
    <jsp:body>
        <div class="header-block">
            <ul class="lang-switch">
                <li><a href="?lang=ru"><img src="assets/ru.svg" alt="Ru"/></a></li>
                <li><a href="?lang=en"><img src="assets/gb.svg" alt="En"/></a></li>
            </ul>
        </div>
        <div class="row">
            <div class="col-xs-3">
                <div class="logo search noselect">
                    <a href="/?lang=${lang}">
                        <span style="color: #6aa84f">FOOD</span><span style="color: #f1c232">pedia</span>
                    </a>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12"><hr/></div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="row">
                    <div class="col-md-12">
                        <h1>${title}</h1>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12"><hr/></div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <jsp:doBody/>
                    </div>
                </div>
            </div>
        </div>
    </jsp:body>
</t:default>