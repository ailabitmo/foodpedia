<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@taglib tagdir="/WEB-INF/tags" prefix="t"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<c:set var="lang" value="${lang != null ? lang : param.lang != null ? param.lang : 'ru'}"></c:set>

<t:page title="Overview">
    <jsp:attribute name="head">
        <script src="/js/jquery-1.11.3.min.js"></script>
        <script src="/js/highcharts.js"></script>
        <script src="/js/highcharts-3d.js"></script>
        <script src="/js/exporting.js"></script>
        <script type="text/javascript">
            $(function() {
                $('#properties').highcharts({
                    chart: {type: 'column'},
                    title: {text: '# of food products / property'},
                    plotOptions: {
                        series: {
                            dataLabels: {
                              enabled: 'true'  
                            },
                            colorByPoint: 'true'
                        }
                    },
                    xAxis: {
                        categories: [
                            'gr:name', 'gr:hasEAN_UCC-13', 
                            'food:ingredientsListAsText', 'foodpedia-owl:netto_mass',
                            'gr:description', 'foodpedia-owl:esl',
                            'food:energyPer100gAsDouble', 'foodpedia-owl:standart',
                            'food:containsIngredient', 'food:carbohydratesPer100gAsDouble',
                            'food:proteinsPer100gAsDouble', 'food:fatPer100gAsDouble',
                            'foodpedia-owl:pack_type', 'foodpedia-owl:best_before',
                            'foodpedia-owl:store_cond'
                        ]
                    },
                    yAxis: {
                        title: { text: '# of food products' }
                    },
                    series: [{
                        name: '# of food products / property',
                        data: [
                            63571, 63571, 61023, 59161, 54556, 42977, 42194, 
                            42180,40768, 38990, 38353, 37868, 37370, 32100, 
                            26536
                        ]
                    }]
                });
            });
            
            $(function() {
                $('#links').highcharts({
                    chart: {
                        type: 'pie',
                        options3d: {
                            enabled: 'true',
                            alpha: 45,
                            beta: 0
                        }
                    },
                    title: { text: '# of links to LOD datasets (AGROVOC & DBpedia)' },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            innerSize: 100,
                            depth: 45
                        }
                    },
                    series: [{
                            name: 'Links',
                            data: [
                                ['AGROVOC', 39200],
                                ['AGROVOC + DBpedia', 40768],
                                ['No links', 22803],
                                ['DBpedia', 10578]
                            ]
                    }]
                });
            });
            
            $(function() {
                $('#ingredients').highcharts({
                    chart: {
                        type: 'column',
                        inverted: 'true'
                    },
                    title: {text: '# of food products / ingredients'},
                    plotOptions: {
                        series: {
                            dataLabels: {
                              enabled: 'true'  
                            },
                            colorByPoint: 'true'
                        }
                    },
                    xAxis: {
                        categories: [
                            'Sugar', 'Water', 'Drinking water', 'White sugar',
                            'Citric acid', 'Beef', 'Margarine', 'Pork', 'Starch',
                            'E330', 'Cocoa powder', 'Spices', 'E211', 'Vanillin',
                            'Vinegar', 'E322', 'Curd', 'E471', 'Cream', 'E621'
                        ]
                    },
                    series: [{
                        name: '# of food products / ingredient',
                        data: [
                            18272, 10397, 5004, 2531, 2335, 2209, 2154, 1776,
                            1673, 1667, 1493, 1462, 1358, 1282, 1223, 1163, 1110,
                            1052, 1016
                        ]
                    }]
                });
            });
        </script>
    </jsp:attribute>
    <jsp:body>
        <div id="properties" style="width: 100%; margin: 0 auto"></div>
        <div id="links" style="width: 100%; margin: 0 auto"></div>
        <div id="ingredients" style="width: 100%; margin: 0 auto"></div>
    </jsp:body>
</t:page>