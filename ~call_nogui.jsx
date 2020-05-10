#target photoshop

var exporterPath = File($.fileName).parent.fsName;

// Create the command file and setup it
var execFile = new File(exporterPath + "/run.bat");
execFile.encoding = "UTF-8";
execFile.open("w");
 
// Write in the file
execFile.write("pythonw \"" + exporterPath + "\\photoshop_actions.py\" NOGUI");
//execFile.write("\npause");
 
// Execute file.
execFile.execute();
