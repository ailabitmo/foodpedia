<%@tag description="The top level layout" pageEncoding="UTF-8"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>

<%@attribute name="lang" type="java.lang.String" required="true"%>
<%@attribute name="subtitle" type="java.lang.String"%>
<%@attribute name="head" fragment="true"%>

<fmt:setLocale value="${lang}"/>
<fmt:setBundle basename="tk.foodpedia.home.messages"/>

<!DOCTYPE html>
<html>
    <head>
        <title>
            <c:choose>
                <c:when test="${subtitle != null}">
                    FOODpedia - ${subtitle}
                </c:when>
                <c:otherwise>
                    <fmt:message key="global.title" />
                </c:otherwise>
            </c:choose>
        </title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Latest compiled and minified CSS -->
        <link href='http://fonts.googleapis.com/css?family=Ubuntu&subset=latin,cyrillic'
              rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
        <link rel="stylesheet" href="<c:url value="css/style.css"/>">
        
        <jsp:invoke fragment="head"/>

        <!-- Google Analytics -->
        <script>
            (function (i, s, o, g, r, a, m) {
                i['GoogleAnalyticsObject'] = r;
                i[r] = i[r] || function () {
                    (i[r].q = i[r].q || []).push(arguments)
                }, i[r].l = 1 * new Date();
                a = s.createElement(o),
                        m = s.getElementsByTagName(o)[0];
                a.async = 1;
                a.src = g;
                m.parentNode.insertBefore(a, m)
            })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

            ga('create', 'UA-57728144-1', 'auto');
            ga('send', 'pageview');
        </script>
    </head>
    <body class="container">
        <jsp:doBody/>
    </body>
</html>
