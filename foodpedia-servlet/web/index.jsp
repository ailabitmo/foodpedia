<%@ page contentType="text/html;charset=Cp1251" language="java" %>
<html>
<head><title>Simple jsp page</title>
    <link rel="stylesheet" type="text/css" href="css/appearance.css">
    <script src="js/script.js" charset="Cp1251"></script>
</head>
<body>
<form method="GET" action="FoodPedia">
    <input name="Accept" value="text/html" type="hidden"> <br>
    <input type="submit" name="action" value="Submit HTML">
</form><hr/>
<form method="GET" action="FoodPedia">
    <input name="Accept" value="application/rdf+xml" type="hidden"> <br>
    <input type="submit" name="action" value="Submit RDF">
</form>
</body>
</html>