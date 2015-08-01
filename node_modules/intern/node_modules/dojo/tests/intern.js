define({
	proxyPort: 9000,
	proxyUrl: 'http://localhost:9000/',

	capabilities: {
		'selenium-version': '2.42.2'
	},

	environments: [
		{ browserName: 'internet explorer', version: '10', platform: 'Windows 2012' },
		{ browserName: 'internet explorer', version: '9', platform: 'Windows 2008' },
		{ browserName: 'firefox', version: '31', platform: [ 'Linux', 'Mac 10.6', 'Windows 2012' ] },
		{ browserName: 'chrome', platform: [ 'Linux', 'Mac 10.8', 'Windows 2008' ] },
		{ browserName: 'safari', version: '7', platform: 'Mac 10.8' }
	],

	maxConcurrency: 3,

	tunnel: 'NullTunnel',

	webdriver: {
		host: 'localhost',
		port: 4444
	},

	useLoader: {
		'host-node': '../../../../dojo'
	},
	loader: {
		// Packages that should be registered with the loader in each testing environment
		packages: [ { name: 'dojo2-core', location: '.' } ],
		map: {
			'intern': {
				'intern/node_modules/dojo/promise/instrumentation': 'dojo2-core/promise/instrumentation',
				'intern/node_modules/dojo/promise/tracer': 'dojo2-core/promise/tracer',
				'chai': 'intern/node_modules/chai/chai',
				'dojo': 'intern/node_modules/dojo'
			}
		}
	},

	suites: [ 'dojo2-core/tests/all' ],
	functionalSuites: [ ],
	excludeInstrumentation: /^(?:node_modules|tests)\//
});
