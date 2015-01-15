#!/bin/bash

echo "@prefix conf: <http://richard.cyganiak.de/2007/pubby/config.rdf#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix gr: <http://purl.org/goodrelations/v1#> .

<> a conf:Configuration;
    conf:projectName \"FOODpedia.tk\";
    conf:projectHomepage <$1/>;
    conf:webBase <$1/>;
    conf:usePrefixesFrom <prefixes.n3>;
    conf:defaultLanguage \"en\";
    conf:indexResource <http://foodpedia.tk/resource/4620001270248>;
    conf:labelProperty gr:name;

    conf:dataset [
        conf:sparqlEndpoint <$2>;
        conf:datasetBase <http://foodpedia.tk/resource/>;
        conf:webResourcePrefix \"resource/\";
        conf:fixUnescapedCharacters \"(),'!$&*+;=@\";
    ];
    .">/usr/local/tomcat/webapps/ROOT/WEB-INF/config.ttl

