<?php
require "includes/dbconn.php";

$title="";
switch ($_GET["t"]) {
    case "a":
        $title = "ATBAs";
        break;
    case "s":
        $title = "SPA/SMA";
        break;
    case "r":
        $title = "Reporting Area";
        break;
    case "p":
        $title = "PMNM Boundary";
        break;
    default:
        $title = "SPA/SMA";
        break;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="HTML5 Admin is an HTML5 Administration template easy to modify and maintain based on Bootstrap 3">
<meta name="author" content="HTML5 Admin"><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="shortcut icon" href="images/favicon.png">
<title>SAIS Vessel Tracks</title>
<link rel="stylesheet" href="css/vendor/bootstrap.css?ver=1.1">
<link rel="stylesheet" href="css/vendor/font-awesome.css?ver=1.1">
<link rel="stylesheet" href="css/overrides/bootstrap-overrides.css?ver=1.1">
<link rel="stylesheet" href="css/HTML5admin.css?ver=1.1">
<link rel="stylesheet" href="css/vendor/jquery.dataTables.css?ver=1.1">
<link rel="stylesheet" href="css/overrides/datatables-overrides.css?ver=1.1">
<link rel="stylesheet" href="css/vendor/bootstrap-slider.css?ver=1.1">
<link rel="stylesheet" href="css/vendor/animate.css?ver=1.1">
</head>
<body>
	<header class="navbar navbar-fixed-top">
		<div class="container">
<h3>PMNM Vessel Data </h3>
		</div>
	</header>
	<div class="container">
		<div class="row">
			<div class="col-md-2">
				<div class="h5a-sidebar hidden-print affix-top">
					<ul class="nav h5a-sidenav nav-list accordion">
						<li class="active" data-toggle="in" data-target="#nav-ui"><a><i class="fa fa-laptop"></i> Forms</a>
							<ul class="nav nav-list in" id="nav-ui">
								<li><a href="ui.html"><i class="fa fa-wrench"></i> Style &amp; Utilities</a></li>
								<li><a href="ui_validation.html"><i class="fa fa-check"></i> Validation</a></li>
								<li><a href="icons.html"><i class="fa fa-edit"></i> Icons</a></li>
								<li><a href="ui_uploader.html"><i class="fa fa-upload"></i> Uploader</a></li>
							</ul>
						</li>
						<li data-toggle="collapse" data-target="#nav-pages"><a><i class="fa fa-rocket"></i> Satellite Data</a>
							<ul class="nav nav-list collapse" id="nav-pages">
								<li class="active"><a href="tracks.php?t=s"><i class="fa fa-star"></i> Tracks intersecting SPA/SMA</a></li>
								<li><a href="tracks.php?t=a"><i class="fa fa-star"></i> Tracks intersecting ATBAs</a></li>
								<li><a href="tracks.php?t=r"><i class="fa fa-star"></i> Tracks intersecting Reporting Area</a></li>
							</ul>
						</li>
						<li data-toggle="collapse" data-target="#imo-pages"><a><i class="fa fa-anchor"></i> Ship Reporting</a>
							<ul class="nav nav-list collapse" id="imo-pages">
								<li><a href="pages/boilerplate.html"><i class="fa fa-star"></i> Boilerplate</a></li><li><a href="pages/invoice.html"><i class="fa fa-money"></i> Invoice</a></li>
								<li><a href="pages/card.html"><i class="fa fa-tag"></i> Card</a></li>
								<li><a href="pages/search_results.html"><i class="fa fa-search"></i> Search Results</a></li>
								<li><a href="pages/calendar.html"><i class="fa fa-calendar"></i> Calendar</a></li>
								<li><a href="pages/stackers.html"><i class="fa fa-stack-overflow"></i> Stackers</a></li>
								<li><a href="pages/tables.html"><i class="fa fa-euro"></i> Tables</a></li>
								<li><a href="pages/errors.html"><i class="fa fa-exclamation-triangle"></i> Login/Errors</a></li>
								<li><a href="pages/file_browser.html"><i class="fa fa-folder-open"></i> File Browser</a></li>
							</ul>
						</li>
						<li data-toggle="collapse" data-target="#nav-emails"><a><i class="fa fa-envelope-o"></i> Emails</a>
							<ul class="nav nav-list collapse" id="nav-emails">
								<li><a href="emails/system.html" target="_blank"><i class="fa fa-envelope-o"></i> System <sup><i class="fa fa-external-link"></i></sup></a></li>
								<li><a href="emails/call_to_action.html" target="_blank"><i class="fa fa-info-circle"></i> Call-To-Action <sup><i class="fa fa-external-link"></i></sup></a></li>
								<li><a href="emails/news.html" target="_blank"><i class="fa fa-globe"></i> News <sup><i class="fa fa-external-link"></i></sup></a></li>
							</ul>
						</li>
						<li><a data-toggle="collapse" data-target="#nav-menu"><i class="fa fa-sitemap"></i> Pure CSS Menu</a><ul class="nav nav-list collapse" id="nav-menu">
							<li><a data-toggle="collapse" data-target="#nav-menu-2">With</a>
								<ul class="nav nav-list collapse" id="nav-menu-2">
									<li><a data-toggle="collapse" data-target="#nav-menu-3">Infinite</a>
										<ul class="nav nav-list collapse" id="nav-menu-3">
											<li><a href="#"><i class="fa fa-gift"></i> Levels</a></li>
										</ul>
									</li>
								</ul>
							</li>
						</ul>
					</li>
				</ul>
				</div>
			</div>
			<div class="col-md-10" role="main">
			<h1>Tracks intersecting <?php echo $title; ?>  <small></small></h1>
			<p>Tracks that intersect one or more SPAs or the SMA. Click a Track ID to get the details of that track or the vessel name to get the vessel's details. Valid indicates whether the track has been deemed to be valid, as many are spurious. Reviewed indicates whether the track has been reviewed for validity and accuracy.</p>
			<div class="bs-example">
				<table cellpadding="0" cellspacing="0" border="0" id="demoUsers">
					<thead>
						<tr><th>Track ID</th><th>Start Date</th><th>End Date</th><th>Vessel Name</th><th class="html">Features Intersected</th><th>Points</th><th>Valid?</th><th>Reviewed?</th></tr>
					</thead>
					<tbody>
<?php
if($_GET["t"] == "s"){
$sql = "SELECT fk_trackid, sdformatted, edformatted, name, mmsi, features_intersected, pointcount, invalid, ta_id ";
$sql   .= "FROM vw_track_details ";
$sql   .= "WHERE features_intersected IS NOT NULL ";
$sql   .= "ORDER BY startdate desc";
} elseif($_GET["t"] == "a") {
$sql = "SELECT fk_trackid, sdformatted, edformatted, name, mmsi, atbas_intersected, pointcount, invalid, ta_id ";
$sql   .= "FROM vw_track_details ";
$sql   .= "WHERE atbas_intersected IS NOT NULL ";
$sql   .= "ORDER BY startdate desc";
}
$result = pg_query($db, $sql);
if (!$result) {
    die("Error in SQL query: " . pg_last_error());
}
$results = array(array());
while ($row = pg_fetch_array($result)) {
    $results[] = $row;
}
     for ($i=1; $i<count($results); $i++) { 
        if($results[$i][3]==""){$name=$results[$i][4];} else {$name=$results[$i][3];}
        if($results[$i][8]==""){$reviewed="No";} else {$reviewed="Yes";}
        echo "<tr><td><a href=\"trackdetails.php?t=" . $results[$i][0] . "\" class=\"tooltip-test\">" . $results[$i][0] . "</a></td><td>" . $results[$i][1] . "</td><td>" . $results[$i][2] . "</td><td><a href=\"shipdetails.php?s=" . $results[$i][4] . "\">" . $name . "</a></td><td>" . str_replace(",",", ",str_replace("\"","",str_replace("}","", str_replace("{","",$results[$i][5])))) . "</td><td>" . $results[$i][6] . "</td><td>" . $results[$i][7] . "</td><td>" . $reviewed . "</td></tr>";
    }
?>

					</tbody>
				</table>
				<br><br>
			</div>
			<h1>SIMPLE TABLE <small>to list simple data</small></h1>
			<div class="bs-example">
				<table class="item">
					<tr><td><i class="fa fa-key"></i> ID</td><td>556</td></tr>
					<tr><td>Company-Code</td><td><input type="text" class="form-control h5a-input" placeholder="CompanyCode?" value="33223-556H-TT"></td></tr>
					<tr><td><i class="fa fa-arrows"></i> Size</td><td class="red">-556 mm/hh</td></tr>
					<tr><td><i class="fa fa-user"></i> Niceness</td><td class="green">Super Kewl</td></tr>
					<tr><td><i class="fa fa-tag"></i> TAGS</td><td>Super, Kewl, 556, wow,<br>nice, hop, html5, admin, responsive<br>more, lines</td></tr>
					<tr><td><i class="fa fa-edit"></i> Colors</td><td><span class="badge green"></span> <span class="badge red"></span> <span class="badge orange"></span> <span class="badge blue"></span></td></tr>
					<tr><td><i class="fa fa-cog"></i> Type</td><td>556H-TT</td></tr>
					<tr><td><i class="fa fa-globe"></i> Website</td><td><a href="http://www.sharedesk.net">ShareDesk - Shared Offices</a></td></tr>
					<tr><td><i class="fa fa-twitter"></i> Twitter</td><td><a href="http://www.twitter.com/sharedesk">@sharedesk</a></td></tr>
				</table>
			</div>
		</div>
	</div>
</div>
<script src="js/vendor/jquery.min.js?ver=1.1"></script>
<script src="js/vendor/bootstrap.min.js?ver=1.1"></script>
<script src="js/vendor/jquery.sparkline.min.js?ver=1.1"></script>
<script src="js/vendor/flot/jquery.flot.min.js?ver=1.1"></script>
<script src="js/vendor/flot/jquery.flot.pie.js?ver=1.1"></script>
<script src="js/vendor/flot/jquery.flot.stack.js?ver=1.1"></script>
<script src="js/vendor/flot/jquery.flot.resize.js?ver=1.1"></script>
<script src="js/vendor/jquery.dataTables.min.js?ver=1.1"></script>
<script src="js/vendor/jquery.knob.min.js?ver=1.1"></script>
<script src="js/vendor/jquery.validate.min.js?ver=1.1"></script>
<script src="js/pages/tables.js?ver=1.1"></script>
<script type="text/javascript">(function(a){if(window.filepicker){return}var b=a.createElement("script");b.type="text/javascript";b.async=!0;b.src=("https:"===a.location.protocol?"https:":"http:")+"//api.filepicker.io/v1/filepicker.js?ver=1.1";var c=a.getElementsByTagName("script")[0];c.parentNode.insertBefore(b,c);var d={};d._queue=[];var e="pick,pickMultiple,pickAndStore,read,write,writeUrl,export,convert,store,storeUrl,remove,stat,setKey,constructWidget,makeDropPane".split(",");var f=function(a,b){return function(){b.push([a,arguments])}};for(var g=0;g<e.length;g++){d[e[g]]=f(e[g],d._queue)}window.filepicker=d})(document);</script>
<script src="js/dashboard.js?ver=1.1"></script>
</body>
</html>
