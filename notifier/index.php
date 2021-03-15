<?php

$md5_red = '117260b97c653f445937e3a1c4a0d97a';
$md5_green = 'f52b4d276a2c9879fe57b494d0bf0c85';
$md5_yellow = '64b6a1a2c60ae0faad7a84bf080c498f';


if (isset($_GET['red'])) {
	copy("/home/pi/Pictures/red.jpg", "/usr/share/rpd-wallpaper/temple.jpg");
} elseif (isset($_POST['red'])) {
	copy("/home/pi/Pictures/red.jpg", "/usr/share/rpd-wallpaper/temple.jpg");
} elseif (isset($_GET['green'])) {
	copy("/home/pi/Pictures/green.jpg", "/usr/share/rpd-wallpaper/temple.jpg");
} elseif (isset($_POST['green'])) {
	copy("/home/pi/Pictures/green.jpg", "/usr/share/rpd-wallpaper/temple.jpg");
} elseif (isset($_GET['yellow'])) {
	copy("/home/pi/Pictures/yellow.jpg", "/usr/share/rpd-wallpaper/temple.jpg");
} elseif (isset($_POST['yellow'])) {
	copy("/home/pi/Pictures/yellow.jpg", "/usr/share/rpd-wallpaper/temple.jpg");
}

?>

<!DOCTYPE html>
<html>
<head>
    <title>ACCESS CONTROL</title>
    <meta charset="utf-8" />
    <style>
    	body {
		background-color: black;
		color: white;
    		font-family: Arial, Helvetica, sans-serif;
    		line-height: 1.4;
		    font-size: 2em;
	}	


	.container {
		width: 80%;
		padding: 0 1rem;
		margin: auto;
	}

	.btn-green {
		    display: inline-block;
		    border: none;
		    background: #0F0;
		    color: #000;
		    padding: 7px 20px;
		    cursor: pointer;
		width: 100%;
			font-size: 2em;
	}
	.btn-red {
		    display: inline-block;
		    border: none;
		    background: #F00;
		    color: #000;
		    padding: 7px 20px;
		    cursor: pointer;
		width: 100%;
			font-size: 2em;
	}
	.btn-yellow {
		    display: inline-block;
		    border: none;
		    background: yellow;
		    color: #000;
		    padding: 7px 20px;
		    cursor: pointer;
		width: 100%;
			font-size: 2em;
	}
	.status-busy {
		background-color: yellow; 
		text-align: center;
		    color: #000;
	}
	.status-dnd {
		background-color: #F00;
		text-align: center;
		    color: #000;
	}
	.status-free {
		background-color: #0F0;
		text-align: center;
		    color: #000;
	}
	.title{
		background-color: #666;
		text-align: center;
		    color: #000;
	}

    </style>
</head>
<body>
<Section id="main">
	<div class="container">

<?php

// Call page render function
render_page();

// Finish off the HTML
?>
</body>
</html>

<?php



//////////////////////////////////
// Functions

function render_page() {
	
	// Import globals
	global $md5_red, $md5_green, $md5_yellow;

	// Get MD5 of current background

	$md5_bg = md5_file('/usr/share/rpd-wallpaper/temple.jpg');
		
	echo '
		<div class="title">
			CURRENT STATUS	
		</div>
		';

	// Check if the port is up or down, output appropriate status
	if ($md5_bg == $md5_red) {
		echo '
		<div class="status-dnd">
			DND
		</div>
		';
	} elseif ($md5_bg == $md5_green) {
		echo '
		<div class="status-free">
			FREE
		</div>
		';
	} elseif ($md5_bg == $md5_yellow) {
		echo '
		<div class="status-busy">
			BUSY
		</div>
		';
	} 
	// Generate main form
	echo '
		<BR><BR>
		<div class="form">
			<FORM method="post" class="form">
				<button type="submit" class="btn-green" name="green">FREE</button>
				<BR>
				<button type="submit" class="btn-yellow" name="yellow">BUSY</button>
				<BR>
				<button type="submit" class="btn-red" name="red">DND</button>
				<BR>
			</FORM>
		</div>
	</div>
</section>
';
}

?>
