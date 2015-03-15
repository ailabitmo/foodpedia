(function(angular, Object){
    
    var module = angular.module('ngSPARQL', ['ngSPARQL.config']);
    
    module.factory('sparql', function($http, $q, SPARQL_CONFIG) {
        
        function SPARQLClient() {
            this._compiledPrefixes = null;
        };
        
        SPARQLClient.prototype = {
            _getEndpoint: function(endpoint) {
                if(!endpoint) {
                    return SPARQL_CONFIG.ENDPOINTS[Object.keys(SPARQL_CONFIG.ENDPOINTS)[0]];
                }
                return endpoint;
            },
            _createConstructFromPatterns: function(patterns) {
                var query = "\n";
                patterns.forEach(function(pattern, index){
                    var subject = pattern[0] ? pattern[0] : '[]';
                    var predicate = pattern[1] ? pattern[1] : '?_var_' + index;
                    var object = pattern[2] ? pattern[2] : '[]';
                    
                    query += subject + " " + predicate + " " + object + " .\n";
                });
                query = "CONSTRUCT {" + query + "} WHERE {\n " + query + "}";
                return query;
            },
            _query: function(query, endpoint, newConfigs) {
                endpoint = this._getEndpoint(endpoint);
                var deferred = $q.defer();
                var configs = {
                    params: {
                        query: this.compilePrefixesString() + query
                    },
                    headers: { Accept: "application/sparql-results+json" }
                };
                angular.extend(configs, newConfigs);
                $http.get(endpoint, configs)
                .success(function(data) {
                    deferred.resolve(data);
                }).error(function(_, status){
                    deferred.reject(status);
                });
                return deferred.promise.catch(function(status) {
                    console.log("ERROR: HTTP status " + status);
                });
            }
        };
        
        /**
         * Executes SPARQL SELECT query and transform mappings to JSON.
         * 
         * @param {type} query
         * @param {type} endpoint - a key of one of SPARQL_CONFIG.ENDPOINTS pairs, 
         *                          otherwise the key of the first pair
         * @returns {$q@call;defer.promise} promise
         */
        SPARQLClient.prototype.select = function(query, endpoint) {
            return this._query(query, endpoint).then(bindingsToJson);
        };
        
        SPARQLClient.prototype.loadTriples = function(triples, endpoint) {
            return this._query(this._createConstructFromPatterns(triples), 
                    endpoint);
        };
        
        SPARQLClient.prototype.register = function(name, query) {
            var deferred = $q.defer();
            $http.post('rest/query/register/', {}, {
                params: {
                    name: name,
                    query: query
                }
            }).success(function(){
                deferred.resolve();
            }).error(function(_, status){
                deferred.reject(status);
            });
            return deferred.promise.catch(function(status){
                alert("[ERROR] at SPARQLClient.register. HTTP status is " + status);
            });
        };
        
        SPARQLClient.prototype.compilePrefixesString = function() {
            if(!this._compiledPrefixes) {
                var tmp = "";
                angular.forEach(SPARQL_CONFIG.PREFIXES, function(url, prefix) {
                    tmp += "PREFIX " + prefix + ": <" + url + "> \n" ;
                });
                this._compiledPrefixes = tmp;
            }
            return this._compiledPrefixes;
        };
        
        function bindingsToJson(bindings) {
            var results = [];
            if(bindings) {
                bindings.results.bindings.forEach(function(element){
                    var r = {};
                    Object.getOwnPropertyNames(element).forEach(function(name){
                        r[name] = element[name].value;
                    });
                    results.push(r);
                });
            }
            return results;
        };
        
        return new SPARQLClient();
    });
    
})(window.angular, window.Object);