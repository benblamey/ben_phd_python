<title>
Pipeline Results
</title>

<style>

.box_rotate {
     -moz-transform: rotate(90deg);  /* FF3.5+ */
}
</style>

<?php

function flatten2 (&$append, $foo, $prefix = "") {

	if (strlen($prefix) > 0) {
		$prefix = $prefix . '.';
	}

	foreach ($foo as $k => $v) {
	
		if ($k == '_id') {
			continue;
		}
	
		if (is_array($v)) {
			flatten2($append, $v, "$prefix$k");
		} else {
			$append["$prefix$k"] = $v;
		}
	}
}


$m = new MongoClient(); // connect
$db = $m->selectDB("exp-results");
$exps = $db->exps;


$select = array();

// find everything in the collection
$cursor = $exps->find($select)->sort(array('startedTime'=>-1));

$experiments_to_show = array();
$keys = array();

// iterate through the results
foreach ($cursor as $document) {
    foreach ($document['exps'] as &$experiment) {
	
		$document2 = $document;
		unset($document2['exps']);
	
		$append = array();
		flatten2($append, $document2);
		flatten2($append, $experiment);
		
		$experiments_to_show[] = $append;
		
		foreach ($append as $k => $v) {
			$keys[$k] = 1;
		}
	}
}

$keys = array_keys($keys);
sort($keys);



?>
<p>
Most recent on the left.
</p>

<table border="1">
<?php foreach ($keys as $key) { ?>
	<tr>
		<td><?php echo $key ?></td>

	<?php
		//echo '<!--';
		//var_dump($experiment_to_show);
		//echo '//-->';
		
		foreach ($experiments_to_show as $experiment_to_show) {
	?>
		<td>
			<?php 
				if (array_key_exists($key, $experiment_to_show)) {
					$toprint = $experiment_to_show[$key];
					if (is_object($toprint)) {
						if (get_class($toprint) == "MongoDate") {
							echo date('M-d H:i:s', $toprint->sec); 
						} else {
							echo get_class($toprint);
						}
					} else {
						echo var_export($toprint, true);
					}
				}
			?>
		</td>

		<?php } ?>
	</tr>
<?php } ?>
</table>

