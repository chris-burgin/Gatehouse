define([
	'./tracer',
	'../has'
], function (tracer, has) {
	function logError(error, rejection, deferred) {
		var stack = '';
		if (error && error.stack) {
			stack += error.stack;
		}

		if (rejection && rejection.stack) {
			stack += '\n    ----------------------------------------\n    rejected' +
				rejection.stack.split('\n').slice(1).join('\n').replace(/^\s+/, ' ');
		}

		if (deferred && deferred.stack) {
			stack += '\n    ----------------------------------------\n' + deferred.stack;
		}

		console.error(stack || error);
	}

	function reportRejections(error, handled, rejection, deferred) {
		if (!handled) {
			logError(error, rejection, deferred);
		}
	}

	var errors = [];
	var activeTimeout = false;
	var unhandledWait = 1000;
	function trackUnhandledRejections(error, handled, rejection, deferred) {
		// use the existing tracking object if one exists
		if (!errors.some(function (rejection) {
			if (rejection.error === error) {
				if (handled) {
					rejection.handled = true;
				}
				return true;
			}
		})) {
			errors.push({
				deferred: deferred,
				error: error,
				handled: handled,
				rejection: rejection,
				timestamp: Date.now()
			});
		}

		if (!activeTimeout) {
			activeTimeout = setTimeout(logRejected, unhandledWait);
		}
	}

	function log(key) {
		return function () {
			if (typeof console !== 'undefined' && /* not null */ console && console.log) {
				var args = Array.prototype.slice.call(arguments, 0);
				args.unshift(key);

				if (console.log.apply) {
					console.log.apply(console, args);
				}
				// IE9 console does not inherit from Function so cannot just use Function#apply directly
				else {
					Function.prototype.bind.call(console.log, console).apply(console, args);
				}
			}
		};
	}

	function logRejected() {
		var now = Date.now();
		var reportBefore = now - unhandledWait;
		errors = errors.filter(function (rejection) {
			if (rejection.timestamp < reportBefore) {
				if (!rejection.handled) {
					logError(rejection.error, rejection.rejection, rejection.deferred);
				}
				return false;
			}
			return true;
		});

		if (errors.length) {
			activeTimeout = setTimeout(logRejected, errors[0].timestamp + unhandledWait - now);
		}
		else {
			activeTimeout = false;
		}
	}

	return function (Deferred) {
		// summary:
		//		Initialize instrumentation for the Deferred class.
		// description:
		//		Initialize instrumentation for the Deferred class.
		//		Done automatically by `dojo/Deferred` if the
		//		`deferredInstrumentation` and `useDeferredInstrumentation`
		//		config options are set.
		//
		//		Sets up `dojo/promise/tracer` to log to the console.
		//
		//		Sets up instrumentation of rejected deferreds so unhandled
		//		errors are logged to the console.

		var usage = has('config-useDeferredInstrumentation');
		if (usage) {
			tracer.on('resolved', log('resolved'));
			tracer.on('rejected', log('rejected'));
			tracer.on('progress', log('progress'));

			var args = [];
			if (typeof usage === 'string') {
				args = usage.split(',');
				usage = args.shift();
			}

			if (usage === 'report-rejections') {
				Deferred.instrumentRejected = reportRejections;
			}
			else if (usage === 'report-unhandled-rejections' || usage === true || usage === 1) {
				Deferred.instrumentRejected = trackUnhandledRejections;
				unhandledWait = parseInt(args[0], 10) || unhandledWait;
			}
			else {
				throw new Error('Unsupported instrumentation usage <' + usage + '>');
			}
		}
	};
});
