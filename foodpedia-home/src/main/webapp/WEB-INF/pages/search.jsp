<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>${lang == "ru"? "FOODpedia - База связанных данных (Linked Data) о продуктах питания и ингредиентах"
                 :"FOODpedia - Food Products and ingredients as Linked Data Dataset"}</title>

        <!-- Latest compiled and minified CSS -->
        <link href='http://fonts.googleapis.com/css?family=Ubuntu&subset=latin,cyrillic'
              rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
        <link rel="stylesheet" href="css/style.css">
        
        <!-- Google Analytics -->
        <script>
          (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
          (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
          m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
          })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

          ga('create', 'UA-57728144-1', 'auto');
          ga('send', 'pageview');
        </script>
    </head>
    <body class="container-fluid">
        <div class="row search-header">
            <div class="col-xs-3">
                <div class="logo search noselect">
                    <a href="/">
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
                <ul class="search-results">
                    <c:forEach var="result" items="${results}">
                        <li>
                            <span class="search-results-name">
                                <a href="/resource/${result.barcode}">${result.name}</a>
                            </span>
                            <span class="search-results-uri">
                                ${result.uri}
                            </span>
                        </li>
                    </c:forEach>
                </ul>
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
    </body>
</html>
