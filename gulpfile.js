var pkg = require('./package.json'),
    gulp = require('gulp'),
    rename = require('gulp-rename'),
    autoprefixer = require('gulp-autoprefixer'),
    minifycss = require('gulp-minify-css'),
    myth = require('gulp-myth'),
    contact = require('gulp-concat');


gulp.task('css', function() {
  return gulp.src('static/*.css')
  .pipe(myth())
  .pipe(autoprefixer({
          browsers: ['> 2%'],
          cascade: false
        }))
  .pipe(contact('style.min.css'))
  .pipe(minifycss({compatibility: 'ie8'}))
  .pipe(gulp.dest('static/css'));
});

gulp.task('watch', function() {
  gulp.watch('static/*.css', ['css']);
});

gulp.task('default', ['css']);
