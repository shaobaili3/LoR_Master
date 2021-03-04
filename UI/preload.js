const remote = require("electron").remote;

window.closeWindow = function() {
    // console.log('Closing');
    var window = remote.getCurrentWindow();
    window.close();
	// remote.app.relaunch()
	// remote.app.exit(0);
};

window.minWindow = function() {
    var window = remote.getCurrentWindow();
    window.minimize();
}