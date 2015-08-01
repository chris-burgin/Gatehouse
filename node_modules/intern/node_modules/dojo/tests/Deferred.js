define([
	'intern!tdd',
	'intern/chai!assert',
	'../Deferred'
], function (test, assert, Deferred) {
	test.suite('Deferred', function () {
		test.test('instrumentation', function () {
			var dfd = this.async(2000);

			var testDfd = new Deferred();
			testDfd.reject(new Error('Oops'));

			var receivedError;
			var oldError = console.error;
			console.error = function (error) {
				receivedError = error;
			};

			setTimeout(dfd.callback(function () {
				try {
					assert.ok(receivedError, 'Unhandled error should be logged to console');
				}
				catch (error) {
					console.error = oldError;
					throw error;
				}
			}), 1200);
		});
	});
});
