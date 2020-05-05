#target photoshop

var exporterPath = File($.fileName).parent.fsName;

// Create the command file and setup it
var execFile = new File(exporterPath + "/run.bat");
execFile.encoding = "UTF-8";
//execFile.lineFeed = "Unix";
execFile.open("w");
 
// Write in the file
execFile.write("python \"" + exporterPath + "\\photoshop_actions.py\" TEST");
execFile.write("\npause");
 
// Execute file.
execFile.execute();



// WORK.
//var bat = new File(exporterPath + "/run.bat");
//bat.execute();

// freeze photoshop. not work.
//run_cmd = "python \"" + exporterPath + "\\photoshop_actions.py\" TEST";
//app.system(run_cmd);
//alert(run_cmd);
