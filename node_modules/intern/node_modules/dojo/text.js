define([ './has' ], function (has) {
	var _getText;

	if (has('host-browser')) {
		_getText = function (url, callback) {
			var xhr = new XMLHttpRequest();

			xhr.onload = function () {
				callback(xhr.responseText);
			};

			xhr.open('GET', url, true);
			xhr.send(null);
		};
	}
	else if (has('host-node')) {
		var fs = require.nodeRequire('fs');
		_getText = function (url, callback) {
			fs.readFile(url, { encoding: 'utf8' }, function (error, data) {
				if (error) {
					throw error;
				}

				callback(data);
			});
		};
	}
	else {
		_getText = function () {
			throw new Error('dojo/text not supported on this platform');
		};
	}

	function getText(resourceId, load, moduleRequire) {
		var cacheId = 'url:' + resourceId;
		if (require.cache && require.cache[cacheId] != null) {
			load(require.cache[cacheId]);
		}
		else {
			_getText(moduleRequire ? moduleRequire.toUrl(resourceId) : resourceId, load);
		}
	}

	getText.dynamic = true;
	getText.load = function (resourceId, require, load) {
		getText(resourceId, load, require);
	};

	return getText;
});
